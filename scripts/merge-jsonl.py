#!/usr/bin/env python3
"""CLI that merges multiple JSONL files, deduplicating records by a configurable key.

Each file is read in order; within each file, records are processed top to
bottom.  When two records share the same key value, the *first* occurrence
wins — later duplicates are silently discarded.

Usage
-----
    python scripts/merge-jsonl.py file1.jsonl file2.jsonl \\
        --key product_id --out merged.jsonl

    # Merge with verbose dedup reporting:
    python scripts/merge-jsonl.py file1.jsonl file2.jsonl \\
        --key product_id --out merged.jsonl --report-duplicates

Input
-----
Two or more JSONL files.  Each non-empty line must contain a valid JSON object
(dict) with the dedup key field present.

Exit codes
----------
0   Merge successful — output written.
2   File not found, fewer than two input files, missing --key or --out, or
    the dedup key is absent from one or more records.
3   Corrupted JSONL (unparseable line) or output write error.

The input files are never modified.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so ``scripts._common`` is importable
# regardless of working directory.
# ---------------------------------------------------------------------------
_T = Path(__file__).resolve().parent.parent
if str(_T) not in sys.path:
    sys.path.insert(0, str(_T))

from scripts._common import read_jsonl, write_jsonl, log_info, log_error


# ---------------------------------------------------------------------------
# Core merge logic
# ---------------------------------------------------------------------------


def merge_jsonl_files(
    file_paths: List[Path],
    key: str,
    report_duplicates: bool = False,
) -> List[Dict[str, Any]]:
    """Merge multiple JSONL files, deduplicating by *key*.

    Parameters
    ----------
    file_paths : list of Path
        JSONL files to merge in processing order.
    key : str
        Field name used as the deduplication key.  Must exist in every record.
    report_duplicates : bool
        When ``True``, log a message for every duplicate that is discarded.

    Returns
    -------
    list of dict
        Merged and deduplicated records in the order they were first
        encountered.

    Raises
    ------
    SystemExit
        Exit 2 when the key is missing from a record.
        Exit 3 on corrupted JSONL.
    """
    seen: set = set()
    merged: List[Dict[str, Any]] = []
    read_count = 0
    dup_count = 0

    for fpath in file_paths:
        try:
            records = read_jsonl(fpath)
        except FileNotFoundError:
            log_error(f"File not found: {fpath}")
            sys.exit(2)
        except json.JSONDecodeError as exc:
            log_error(f"Corrupted JSONL at {fpath}: {exc}")
            sys.exit(3)

        log_info(f"Read {len(records)} record(s) from {fpath}")

        for idx, rec in enumerate(records):
            read_count += 1

            # -- Validate the dedup key exists --
            if key not in rec:
                line_num = idx + 1
                log_error(
                    f"Dedup key {key!r} missing from line {line_num} "
                    f"of {fpath} — cannot deduplicate"
                )
                sys.exit(2)

            key_val = rec[key]

            # Convert to a hashable sentinel when None / non-string
            if key_val is None:
                log_error(
                    f"Dedup key {key!r} is None at line {idx + 1} of "
                    f"{fpath} — cannot deduplicate"
                )
                sys.exit(2)

            # Work around unhashable types (lists, dicts) by serialising
            hashable = _make_hashable(key_val)

            if hashable in seen:
                dup_count += 1
                if report_duplicates:
                    log_info(
                        f"Duplicate {key}={key_val!r} from {fpath}:{idx + 1} "
                        f"— keeping first occurrence"
                    )
                continue

            seen.add(hashable)
            merged.append(rec)

    log_info(
        f"Merged {read_count} total record(s) → "
        f"{len(merged)} unique(s) "
        f"({dup_count} duplicate(s) discarded)"
    )
    return merged


def _make_hashable(value: Any) -> Any:
    """Convert *value* to a hashable type for set membership testing.

    Parameters
    ----------
    value : Any
        Potentially unhashable value (list, dict).

    Returns
    -------
    Any
        A hashable equivalent: strings, numbers, and tuples are returned
        as-is; lists and dicts are serialised to JSON strings.
    """
    if isinstance(value, (list, dict)):
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    return value


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments, merge files, write output, and return exit code."""
    parser = argparse.ArgumentParser(
        description="Merge multiple JSONL files, deduplicating by key.",
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=str,
        help="Two or more .jsonl files to merge (in order)",
    )
    parser.add_argument(
        "--key",
        type=str,
        required=True,
        help="Field name to use for deduplication",
    )
    parser.add_argument(
        "--out",
        type=str,
        required=True,
        help="Output .jsonl file path",
    )
    parser.add_argument(
        "--report-duplicates",
        action="store_true",
        default=False,
        help="Log each discarded duplicate to stderr",
    )
    args = parser.parse_args()

    # -- Validate arg count --
    if len(args.files) < 2:
        log_error("At least two input files required for merging")
        return 2

    # -- Resolve paths --
    file_paths = [Path(f) for f in args.files]
    out_path = Path(args.out)

    # -- Process --
    merged = merge_jsonl_files(
        file_paths,
        args.key,
        report_duplicates=args.report_duplicates,
    )

    # -- Write output --
    try:
        write_jsonl(out_path, merged)
    except OSError as exc:
        log_error(f"Failed to write output to {out_path}: {exc}")
        return 3

    log_info(f"Merged output written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
