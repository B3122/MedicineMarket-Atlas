#!/usr/bin/env python3
"""CLI validator for listing records against ``listing.schema.json``.

Usage
-----
    python scripts/validate-listings.py path/to/listings.jsonl [--out report.json]

Exit codes
----------
    0   All records valid.
    1   One or more validation errors.
    2   File not found or missing arguments.
    3   Corrupted JSONL or schema-loading error.

The input file is never modified.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so ``scripts._common`` is importable
# when this script is run as ``python scripts/validate-listings.py``.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import read_jsonl, log_info, log_error

try:
    from jsonschema import Draft7Validator, RefResolver
except ImportError:
    log_error("jsonschema is required — install with: pip install jsonschema")
    sys.exit(3)


# ---------------------------------------------------------------------------
# Schema loading
# ---------------------------------------------------------------------------


def _load_validator(schema_dir: Path) -> Draft7Validator:
    """Load ``listing.schema.json`` and resolve ``$ref`` via ``RefResolver``.

    Parameters
    ----------
    schema_dir : Path
        Directory containing ``listing.schema.json`` and ``_defs.json``.

    Returns
    -------
    Draft7Validator
        A prepared validator ready to ``.iter_errors(record)``.
    """
    schema_path = schema_dir / "listing.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    resolver = RefResolver(
        base_uri=schema_path.as_uri(),
        referrer=schema,
    )
    return Draft7Validator(schema, resolver=resolver)


# ---------------------------------------------------------------------------
# Core validation logic
# ---------------------------------------------------------------------------


def _validate_records(
    path: Path,
    validator: Draft7Validator,
    out_path: Optional[Path] = None,
) -> int:
    """Read, parse, and validate every record; report errors to stderr.

    Parameters
    ----------
    path : Path
        Input ``.jsonl`` file.
    validator : Draft7Validator
        Pre-configured schema validator.
    out_path : Path or None
        Optional path for a JSON validation report.

    Returns
    -------
    int
        Exit code: 0 (success), 1 (validation errors), 2 (bad file/args),
        or 3 (parse / processing error).
    """
    # ---- Read & parse -----------------------------------------------------
    try:
        records = read_jsonl(path)
    except FileNotFoundError:
        log_error(f"File not found: {path}")
        return 2
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSONL at {path}: {exc}")
        return 3

    # ---- Validate each record ----------------------------------------------
    errors: List[Dict[str, Union[int, str]]] = []
    for idx, record in enumerate(records):
        line_num = idx + 1  # 1-indexed record number
        for ve in validator.iter_errors(record):
            field = (
                ".".join(str(p) for p in ve.absolute_path)
                if ve.absolute_path
                else "(root)"
            )
            errors.append(
                {
                    "line": line_num,
                    "field": field,
                    "message": ve.message,
                }
            )

    # ---- Report results ----------------------------------------------------
    if errors:
        log_error(f"FAIL: {len(errors)} validation error(s)")
        for err in errors:
            log_error(
                f"  Line {err['line']}, field '{err['field']}': {err['message']}"
            )
        if out_path:
            try:
                with open(out_path, "w", encoding="utf-8") as fh:
                    json.dump(
                        {
                            "input": str(path),
                            "valid": False,
                            "error_count": len(errors),
                            "errors": errors,
                        },
                        fh,
                        indent=2,
                        ensure_ascii=False,
                    )
            except OSError:
                log_error(f"Failed to write report to {out_path}")
                return 3
        return 1

    log_info(f"PASS: {len(records)} record(s) validated")
    if out_path:
        try:
            with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(
                    {
                        "input": str(path),
                        "valid": True,
                        "record_count": len(records),
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
    """Parse arguments and run validation."""
    parser = argparse.ArgumentParser(
        description="Validate listing records against listing.schema.json",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to a .jsonl file containing listing records",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Optional path to write a JSON validation report",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out) if args.out else None
    schema_dir = _PROJECT_ROOT / "schemas"

    # ---- Load schema -------------------------------------------------------
    try:
        validator = _load_validator(schema_dir)
    except Exception as exc:
        log_error(f"Failed to load schema: {exc}")
        return 3

    # ---- Validate ----------------------------------------------------------
    log_info(f"Validating: {input_path}")
    exit_code = _validate_records(input_path, validator, out_path)
    log_info(
        f"Done validating {input_path}"
        + (f" | Report: {args.out}" if args.out else "")
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
