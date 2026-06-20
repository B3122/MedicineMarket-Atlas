#!/usr/bin/env python3
"""Verify that every source ID cited in the report exists in the source inventory.

Usage
-----
    python check-source-ids.py <report.md> --sources <sources.jsonl> [--out findings.json]

Exit codes
----------
    0   All cited source IDs found in inventory.
    1   One or more orphan citations (cited but not in inventory).
    2   File not found or missing arguments.
    3   Read or parse error (malformed JSONL).

Neither the report nor the source inventory is modified.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional, Set

# ---------------------------------------------------------------------------
# Ensure the skill root is on sys.path so ``scripts._common`` is importable
# when this script is run as ``python scripts/check-source-ids.py``.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import log_info, log_error, read_jsonl  # noqa: E402


# ---------------------------------------------------------------------------
# Source ID pattern
# ---------------------------------------------------------------------------

#: Compiled regex for source IDs: lowercase prefix, date YYYYMMDD, 3-digit seq.
#: Matches patterns like ``jd-20250620-001`` or ``src-20250115-042``.
_SOURCE_ID_RE = re.compile(r"\b([a-z][a-z0-9]*-\d{8}-\d{3})\b")

#: Fenced code block marker.
_CODE_FENCE_RE = re.compile(r"^\s*```")

#: HTML-style comment (to skip).
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _extract_cited_ids(text: str) -> Set[str]:
    """Extract source ID citations from report text, skipping code blocks.

    Parameters
    ----------
    text : str
        Full report markdown content.

    Returns
    -------
    set[str]
        Unique source IDs cited in the report.
    """
    # Remove HTML comments first.
    text = _HTML_COMMENT_RE.sub("", text)

    cited: Set[str] = set()
    in_code_block = False

    for line in text.splitlines():
        if _CODE_FENCE_RE.match(line):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        for match in _SOURCE_ID_RE.finditer(line):
            cited.add(match.group(1))

    return cited


def _load_inventory_ids(path: Path) -> Set[str]:
    """Load source IDs from the inventory JSONL file.

    Parameters
    ----------
    path : Path
        Path to the source inventory ``.jsonl`` file.

    Returns
    -------
    set[str]
        All source IDs present in the inventory.

    Raises
    ------
    FileNotFoundError
        If the inventory file does not exist.
    json.JSONDecodeError
        If any line is malformed JSON.
    """
    records = read_jsonl(path)
    ids: Set[str] = set()
    for rec in records:
        # Source ID field: try common field names.
        sid = rec.get("source_id") or rec.get("id") or rec.get("record_id")
        if sid:
            ids.add(str(sid))
    return ids


def _check_source_ids(
    report_path: Path,
    sources_path: Path,
    out_path: Optional[Path] = None,
) -> int:
    """Read the report and inventory, cross-reference cited IDs, report results.

    Parameters
    ----------
    report_path : Path
        Path to the report ``.md`` file.
    sources_path : Path
        Path to the source inventory ``.jsonl`` file.
    out_path : Path or None
        Optional path for a JSON findings report.

    Returns
    -------
    int
        Exit code: 0 (all matched), 1 (orphans found), 2 (bad file/args),
        or 3 (read/parse error).
    """
    # ---- Read report --------------------------------------------------------
    try:
        report_text = report_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        log_error(f"Report not found: {report_path}")
        return 2
    except (OSError, UnicodeDecodeError) as exc:
        log_error(f"Failed to read report {report_path}: {exc}")
        return 3

    # ---- Extract cited IDs --------------------------------------------------
    cited_ids = _extract_cited_ids(report_text)
    log_info(f"Found {len(cited_ids)} cited source ID(s) in report")

    if not cited_ids:
        log_info("No source IDs cited in report — nothing to verify")
        if out_path:
            try:
                with open(out_path, "w", encoding="utf-8") as fh:
                    json.dump(
                        {
                            "input_report": str(report_path),
                            "input_sources": str(sources_path),
                            "passed": True,
                            "cited_count": 0,
                            "orphan_count": 0,
                            "orphans": [],
                        },
                        fh,
                        indent=2,
                        ensure_ascii=False,
                    )
            except OSError:
                log_error(f"Failed to write report to {out_path}")
                return 3
        return 0

    # ---- Load inventory -----------------------------------------------------
    try:
        inventory_ids = _load_inventory_ids(sources_path)
    except FileNotFoundError:
        log_error(f"Source inventory not found: {sources_path}")
        return 2
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSONL at {sources_path}: {exc}")
        return 3

    log_info(f"Loaded {len(inventory_ids)} source ID(s) from inventory")

    # ---- Cross-reference ----------------------------------------------------
    orphans = sorted(cited_ids - inventory_ids)

    if orphans:
        log_error(f"FAIL: {len(orphans)} orphan citation(s) found")
        for oid in orphans:
            log_error(f"  Orphan: {oid}")
        if out_path:
            try:
                with open(out_path, "w", encoding="utf-8") as fh:
                    json.dump(
                        {
                            "input_report": str(report_path),
                            "input_sources": str(sources_path),
                            "passed": False,
                            "cited_count": len(cited_ids),
                            "inventory_count": len(inventory_ids),
                            "orphan_count": len(orphans),
                            "orphans": orphans,
                        },
                        fh,
                        indent=2,
                        ensure_ascii=False,
                    )
            except OSError:
                log_error(f"Failed to write report to {out_path}")
                return 3
        return 1

    log_info(f"PASS: all {len(cited_ids)} cited source ID(s) found in inventory")
    if out_path:
        try:
            with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(
                    {
                        "input_report": str(report_path),
                        "input_sources": str(sources_path),
                        "passed": True,
                        "cited_count": len(cited_ids),
                        "inventory_count": len(inventory_ids),
                        "orphan_count": 0,
                        "orphans": [],
                    },
                    fh,
                    indent=2,
                    ensure_ascii=False,
                )
        except OSError:
            log_error(f"Failed to write report to {out_path}")
            return 3
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments and run source ID check."""
    parser = argparse.ArgumentParser(
        description="Cross-reference report source citations with inventory",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to the report .md file",
    )
    parser.add_argument(
        "--sources",
        type=str,
        required=True,
        help="Path to the source inventory .jsonl file",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Optional path to write a JSON findings report",
    )
    args = parser.parse_args()

    report_path = Path(args.input)
    sources_path = Path(args.sources)
    out_path = Path(args.out) if args.out else None

    log_info(f"Checking citations in: {report_path}")
    log_info(f"Source inventory: {sources_path}")
    exit_code = _check_source_ids(report_path, sources_path, out_path)
    log_info(
        f"Done checking {report_path}"
        + (f" | Report: {args.out}" if args.out else "")
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
