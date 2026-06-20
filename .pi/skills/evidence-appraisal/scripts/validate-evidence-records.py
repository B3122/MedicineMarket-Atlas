#!/usr/bin/env python3
"""CLI validator for evidence records against ``evidence.schema.json``.

Usage
-----
    python validate-evidence-records.py <input.jsonl> [--out report.json]

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
# Ensure the skill root is on sys.path so ``scripts._common`` is importable
# when this script is run as ``python scripts/validate-evidence-records.py``.
# ---------------------------------------------------------------------------
_SKILL_ROOT = Path(__file__).resolve().parent.parent
if str(_SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(_SKILL_ROOT))

from scripts._common import read_jsonl, log_info, log_error  # noqa: E402

try:
    from jsonschema import Draft7Validator, RefResolver
except ImportError:
    log_error("jsonschema is required — install with: pip install jsonschema")
    sys.exit(3)


# ---------------------------------------------------------------------------
# Project-root resolution
# ---------------------------------------------------------------------------


def _find_project_root() -> Path:
    """Walk up from this script's directory to locate the project root.

    Stops at the first ancestor that contains a ``schemas/`` directory or a
    ``.git`` directory (checked in that order).  Falls back to the repository
    root (parent of the skill root) when neither marker is found.

    Returns
    -------
    Path
        Absolute path to the project root directory.
    """
    current = Path(__file__).resolve().parent  # scripts/
    for ancestor in [current] + list(current.parents):
        if (ancestor / "schemas").is_dir():
            return ancestor
        if (ancestor / ".git").is_dir():
            return ancestor
    # Fallback: great-grandparent of scripts/ (walk up past skill dir, past .pi/)
    return current.parent.parent.parent


# ---------------------------------------------------------------------------
# Schema loading
# ---------------------------------------------------------------------------


def _load_validator(schema_path: Path, defs_path: Path) -> Draft7Validator:
    """Load ``evidence.schema.json`` and resolve ``$ref`` via ``RefResolver``.

    Parameters
    ----------
    schema_path : Path
        Path to ``evidence.schema.json``.
    defs_path : Path
        Path to ``_defs.json`` used for ``$ref`` resolution.

    Returns
    -------
    Draft7Validator
        A prepared validator ready to ``.iter_errors(record)``.
    """
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    # RefResolver uses the base URI to resolve relative ``$ref`` strings.
    # The evidence schema references ``_defs.json#/definitions/...`` which
    # resolves relative to the base URI (the schema directory).
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

    if not records:
        log_info(f"No records found in {path}")
        if out_path:
            _write_report(out_path, path, valid_count=0, invalid_count=0, errors=[])
        return 0

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
    valid_count = len(records) - len({e["line"] for e in errors})
    invalid_count = len({e["line"] for e in errors})

    if errors:
        log_error(f"FAIL: {valid_count} valid, {invalid_count} invalid — "
                   f"{len(errors)} total error(s)")
        for err in errors:
            log_error(
                f"  Line {err['line']}, field '{err['field']}': {err['message']}"
            )
        if out_path:
            try:
                _write_report(
                    out_path, path, valid_count, invalid_count, errors
                )
            except OSError:
                log_error(f"Failed to write report to {out_path}")
                return 3
        return 1

    log_info(f"PASS: {valid_count} record(s) validated")
    if out_path:
        try:
            _write_report(
                out_path, path, valid_count, invalid_count, errors
            )
        except OSError:
            log_error(f"Failed to write report to {out_path}")
            return 3
    return 0


def _write_report(
    out_path: Path,
    input_path: Path,
    valid_count: int,
    invalid_count: int,
    errors: List[Dict],
) -> None:
    """Write a JSON validation report to *out_path*.

    Parameters
    ----------
    out_path : Path
        Output file path.
    input_path : Path
        Path to the input file being validated.
    valid_count : int
        Number of valid records.
    invalid_count : int
        Number of invalid records.
    errors : list[dict]
        Validation error details.
    """
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(
            {
                "input": str(input_path),
                "valid_count": valid_count,
                "invalid_count": invalid_count,
                "errors": errors,
            },
            fh,
            indent=2,
            ensure_ascii=False,
        )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments and run evidence-record validation."""
    parser = argparse.ArgumentParser(
        description="Validate evidence records against evidence.schema.json",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to a .jsonl file containing evidence records",
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

    # ---- Resolve project root and schema paths -----------------------------
    project_root = _find_project_root()
    schema_dir = project_root / "schemas"
    schema_path = schema_dir / "evidence.schema.json"
    defs_path = schema_dir / "_defs.json"

    if not schema_path.is_file():
        log_error(f"Schema file not found: {schema_path}")
        return 3

    # ---- Load schema -------------------------------------------------------
    try:
        validator = _load_validator(schema_path, defs_path)
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
