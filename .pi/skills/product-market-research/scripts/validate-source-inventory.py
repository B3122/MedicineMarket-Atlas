#!/usr/bin/env python3
"""
validate-source-inventory.py — Validate source inventory records.

Checks
------
- Source ID uniqueness within the inventory
- Schema conformance (source.schema.json + _defs.json)
- URL presence (non-empty string in required field)
- Collection date validity (ISO 8601 partial/full)
- Source type, platform, title presence (via schema required fields)
- Snapshot path format (via schema optional field)
- Optional: orphan / broken-reference cross-check with reference files

Exit codes
----------
0 = all valid
1 = validation errors (duplicates, schema violations, broken refs, orphans)
2 = file or parameter errors (file not found, missing required args)
3 = processing errors (corrupted JSONL, schema load failure)

Usage
-----
    python scripts/validate-source-inventory.py sources.jsonl [references.jsonl ...]

The script logs progress and all errors to stderr.  It NEVER writes to or
modifies any input file.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

import jsonschema
from jsonschema import ValidationError, RefResolver

# ---------------------------------------------------------------------------
# Path setup — ensure project root is on sys.path for scripts._common
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import read_jsonl, log_info, log_error

# ---------------------------------------------------------------------------
# Schema loading
# ---------------------------------------------------------------------------


def _load_schema() -> Tuple[Dict, RefResolver]:
    """Load *source.schema.json* and prepare a ``RefResolver`` for
    ``_defs.json``.

    Returns
    -------
    (schema_dict, resolver)
    """
    schema_dir = _PROJECT_ROOT / "schemas"
    schema_path = schema_dir / "source.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        log_error(f"Schema file not found: {schema_path}")
        raise
    except json.JSONDecodeError as exc:
        log_error(f"Schema file is not valid JSON: {schema_path} — {exc}")
        raise

    resolver = RefResolver(
        base_uri=schema_path.as_uri(),
        referrer=schema,
    )
    return schema, resolver


# ---------------------------------------------------------------------------
# Record-level validation
# ---------------------------------------------------------------------------


def _validate_single(
    record: Dict,
    line_no: int,
    schema: Dict,
    resolver: RefResolver,
) -> List[str]:
    """Validate a single source record against the JSON Schema.

    Returns a (possibly empty) list of error message strings.
    """
    try:
        jsonschema.validate(instance=record, schema=schema, resolver=resolver)
    except ValidationError as exc:
        return [f"  Line {line_no}: schema violation — {exc.message}"]
    return []


# ---------------------------------------------------------------------------
# Reference-file helpers
# ---------------------------------------------------------------------------


def _collect_referenced_ids(ref_paths: List[Path]) -> Tuple[Set[str], bool]:
    """Read all reference JSONL files and collect every ``source_id`` value.

    Parameters
    ----------
    ref_paths
        List of paths to JSONL files that contain records with a ``source_id``
        field (e.g. listing records, price observations, products).

    Returns
    -------
    (referenced_ids, had_errors)
        ``had_errors`` is ``True`` when at least one file could not be read
        (not found or corrupted).
    """
    all_ids: Set[str] = set()
    had_errors = False

    for rp in ref_paths:
        try:
            records = read_jsonl(rp)
        except FileNotFoundError:
            log_error(f"Reference file not found: {rp}")
            had_errors = True
            continue
        except json.JSONDecodeError as exc:
            log_error(f"Reference file corrupted (invalid JSONL): {rp} — {exc}")
            had_errors = True
            continue

        for rec in records:
            sid = rec.get("source_id")
            if sid is not None:
                all_ids.add(str(sid))

    return all_ids, had_errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate source inventory records.",
    )
    parser.add_argument(
        "sources",
        type=str,
        help="Path to the source inventory JSONL file.",
    )
    parser.add_argument(
        "references",
        type=str,
        nargs="*",
        help="Zero or more reference JSONL files for orphan / broken-ref detection.",
    )
    args = parser.parse_args()

    sources_path = Path(args.sources)
    ref_paths = [Path(r) for r in args.references]

    log_info(f"Input: {sources_path}")
    if ref_paths:
        log_info(f"Reference files ({len(ref_paths)}): {', '.join(str(p) for p in ref_paths)}")

    # ------------------------------------------------------------------
    # 1. Load schema
    # ------------------------------------------------------------------
    try:
        schema, resolver = _load_schema()
    except (FileNotFoundError, json.JSONDecodeError):
        return 3

    # ------------------------------------------------------------------
    # 2. Read source inventory
    # ------------------------------------------------------------------
    try:
        records = read_jsonl(sources_path)
    except FileNotFoundError:
        log_error(f"File not found: {sources_path}")
        return 2
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSONL in {sources_path}: {exc}")
        return 3

    log_info(f"Loaded {len(records)} source record(s).")

    # ------------------------------------------------------------------
    # 3. Validate each record & track duplicates
    # ------------------------------------------------------------------
    schema_errors: List[str] = []
    id_to_lines: Dict[str, List[int]] = defaultdict(list)

    for idx, rec in enumerate(records):
        line_no = idx + 1

        # Track source_id for duplicate detection
        sid = rec.get("source_id")
        if sid is not None:
            id_to_lines[str(sid)].append(line_no)

        # Schema validation
        schema_errors.extend(_validate_single(rec, line_no, schema, resolver))

    # ------------------------------------------------------------------
    # 4. Report duplicates
    # ------------------------------------------------------------------
    duplicate_count = 0
    for sid in sorted(id_to_lines):
        lines = id_to_lines[sid]
        if len(lines) > 1:
            duplicate_count += len(lines) - 1
            log_error(
                f"Duplicate source_id '{sid}' appears on lines "
                f"{', '.join(str(l) for l in lines)}"
            )

    # ------------------------------------------------------------------
    # 5. Report schema errors
    # ------------------------------------------------------------------
    for err in schema_errors:
        log_error(err)

    # ------------------------------------------------------------------
    # 6. Cross-reference with reference files (optional)
    # ------------------------------------------------------------------
    broken_refs: Set[str] = set()
    orphans: Set[str] = set()
    ref_had_errors = False

    if ref_paths:
        inventory_ids = set(id_to_lines.keys())
        ref_ids, ref_had_errors = _collect_referenced_ids(ref_paths)

        # Source IDs that are referenced but do NOT exist in the inventory
        broken_refs = ref_ids - inventory_ids
        # Source IDs that exist in the inventory but are NOT referenced
        orphans = inventory_ids - ref_ids

        for sid in sorted(broken_refs):
            log_error(
                f"Broken reference: source_id '{sid}' referenced but "
                f"not present in inventory"
            )
        for sid in sorted(orphans):
            log_error(
                f"Orphaned source: source_id '{sid}' present in inventory "
                f"but not referenced by any record"
            )

    # ------------------------------------------------------------------
    # 7. Determine exit code
    # ------------------------------------------------------------------
    has_validation_errors = bool(
        schema_errors or duplicate_count or broken_refs or orphans
    )

    if ref_had_errors:
        log_error("One or more reference files could not be read (exit code 2).")
        return 2

    if has_validation_errors:
        log_info("Source inventory validation FAILED (exit code 1).")
        return 1

    log_info("Source inventory validation PASSED (exit code 0).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
