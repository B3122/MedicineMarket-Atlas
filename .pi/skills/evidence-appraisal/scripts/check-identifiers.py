#!/usr/bin/env python3
"""CLI that validates DOI, PMID, and trial-registry identifiers in evidence records.

Checks identifier format only — no network resolution is attempted. Format
patterns follow common identifier conventions:

- DOI: must start with ``10.`` followed by at least four digits, then a slash
  and one or more characters.
- PMID: must consist entirely of digits.
- Trial registry ID: must match one of the known registry patterns:
  ``NCT##########`` (ClinicalTrials.gov), ``ISRCTN#########`` (ISRCTN),
  ``ChiCTR-###-########`` (Chinese Clinical Trial Registry).

Usage
-----
    python scripts/check-identifiers.py input.jsonl
    python scripts/check-identifiers.py input.jsonl --out report.json

Input
-----
JSONL file where each line is an evidence record (see ``evidence.schema.json``).
Identifiers are located in the ``citation`` object (``doi``, ``pmid``) and at
top-level fields (``trial_registration``).

Output
------
When ``--out`` is supplied, writes a JSON report file:

.. code-block:: json

    {
        "valid":   [{"line": 1, "doi": "10.1000/abc123", ...}, ...],
        "invalid": [{"line": 2, "doi": "bad-doi", "reason": "..."}, ...],
        "unknown": [{"line": 3, "identifiers": []}, ...]
    }

Exit codes
----------
0   All identifiers valid or unknown (no invalid identifiers found).
1   One or more invalid identifiers found.
2   File not found, permission error, or missing required arguments.
3   Corrupted JSONL (unparseable line).

The input file is never modified.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so ``scripts._common`` is importable
# when this script is run as ``python scripts/check-identifiers.py``.
# ---------------------------------------------------------------------------
_SKILL_ROOT = Path(__file__).resolve().parent.parent
if str(_SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(_SKILL_ROOT))

from scripts._common import read_jsonl, log_info, log_error  # noqa: E402

# ---------------------------------------------------------------------------
# Identifier pattern definitions
# ---------------------------------------------------------------------------

#: Compiled regex for DOI format: ``10.`` prefix, at least 4 digits, slash,
#: one or more trailing characters.
DOI_PATTERN: re.Pattern = re.compile(r"^10\.[0-9]{4,}\/.+$")

#: Compiled regex for PMID: one or more digits only.
PMID_PATTERN: re.Pattern = re.compile(r"^\d+$")

#: Compiled regex for ClinicalTrials.gov ``NCT`` followed by 8 digits.
NCT_PATTERN: re.Pattern = re.compile(r"^NCT\d{8}$")

#: Compiled regex for ISRCTN: ``ISRCTN`` followed by 8 digits.
ISRCTN_PATTERN: re.Pattern = re.compile(r"^ISRCTN\d{8}$")

#: Compiled regex for ChiCTR: ``ChiCTR``, dash, 3 chars/digits, dash, 8 digits.
CHICTR_PATTERN: re.Pattern = re.compile(r"^ChiCTR-[A-Za-z0-9]{3}-\d{8}$")

#: Known trial-registry identifier patterns in lookup order.
TRIAL_REGISTRY_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("NCT", NCT_PATTERN),
    ("ISRCTN", ISRCTN_PATTERN),
    ("ChiCTR", CHICTR_PATTERN),
]

#: Valid sentinel values that indicate the identifier is intentionally absent.
_SENTINEL_VALUES: Tuple[str, ...] = ("unknown", "not_applicable", "not_stated")


def _is_sentinel(value: Any) -> bool:
    """Return ``True`` if *value* is a recognised sentinel indicating absence.

    Parameters
    ----------
    value : Any
        The field value to check.

    Returns
    -------
    bool
        ``True`` when *value* is ``None`` or one of the sentinel strings.
    """
    if value is None:
        return True
    if isinstance(value, str) and value.lower() in _SENTINEL_VALUES:
        return True
    return False


def _collect_identifiers(record: Dict[str, Any]) -> Dict[str, Any]:
    """Extract DOI, PMID, and trial registration from an evidence record.

    Identifiers are looked up in the ``citation`` sub-object and at the
    top level of the record.

    Parameters
    ----------
    record : dict
        One evidence record parsed from the input JSONL.

    Returns
    -------
    dict
        Keys ``doi``, ``pmid``, ``trial_registration`` with their raw
        values (or ``None`` when absent).
    """
    citation: Dict[str, Any] = record.get("citation", {}) or {}

    doi: Optional[str] = citation.get("doi")
    pmid: Optional[str] = citation.get("pmid")
    trial_reg: Optional[str] = (
        record.get("trial_registration")
        or citation.get("trial_registration")
        or record.get("trial_registry_id")
    )

    return {
        "doi": doi,
        "pmid": pmid,
        "trial_registration": trial_reg,
    }


def _validate_doi(raw: Any) -> Optional[str]:
    """Validate a raw DOI string against the standard format.

    Parameters
    ----------
    raw : Any
        The raw DOI value from the record.

    Returns
    -------
    Optional[str]
        ``None`` when valid or sentinel; an error-reason string when invalid.
    """
    if _is_sentinel(raw):
        return None
    if not isinstance(raw, str):
        return f"Expected string for DOI, got {type(raw).__name__}: {raw!r}"
    val: str = raw.strip()
    if not val:
        return None  # empty string treated as absent
    if DOI_PATTERN.match(val):
        return None
    return f"Invalid DOI format: {val!r} (expected 10.xxxx/...)"


def _validate_pmid(raw: Any) -> Optional[str]:
    """Validate a raw PMID string (must be all digits).

    Parameters
    ----------
    raw : Any
        The raw PMID value from the record.

    Returns
    -------
    Optional[str]
        ``None`` when valid or sentinel; an error-reason string when invalid.
    """
    if _is_sentinel(raw):
        return None
    if not isinstance(raw, str):
        return f"Expected string for PMID, got {type(raw).__name__}: {raw!r}"
    val: str = raw.strip()
    if not val:
        return None
    if PMID_PATTERN.match(val):
        return None
    return f"Invalid PMID format: {val!r} (expected digits only)"


def _validate_trial_registration(raw: Any) -> Optional[str]:
    """Validate a trial registry ID against known patterns.

    Parameters
    ----------
    raw : Any
        The raw trial-registration value from the record.

    Returns
    -------
    Optional[str]
        ``None`` when valid or sentinel; an error-reason string when invalid.
    """
    if _is_sentinel(raw):
        return None
    if not isinstance(raw, str):
        return f"Expected string for trial registration, got {type(raw).__name__}: {raw!r}"
    val: str = raw.strip()
    if not val:
        return None
    for registry_name, pattern in TRIAL_REGISTRY_PATTERNS:
        if pattern.match(val):
            return None
    return (
        f"Invalid trial registration ID: {val!r} "
        f"(expected NCT##########, ISRCTN#########, or ChiCTR-###-########)"
    )


def _build_report_entry(
    line_num: int,
    identifiers: Dict[str, Any],
    errors: Dict[str, str],
) -> Dict[str, Any]:
    """Build a single report entry for one record.

    Parameters
    ----------
    line_num : int
        1-based line number in the input file.
    identifiers : dict
        Raw identifier values keyed by type (``doi``, ``pmid``,
        ``trial_registration``).
    errors : dict
        Error messages keyed by identifier type (only present for invalid
        identifiers).

    Returns
    -------
    dict
        A report entry with keys ``line`` and identifier values and/or
        ``reason`` for invalids.
    """
    entry: Dict[str, Any] = {"line": line_num}
    for id_type in ("doi", "pmid", "trial_registration"):
        raw = identifiers.get(id_type)
        if raw is not None:
            entry[id_type] = raw
    if errors:
        entry["reason"] = "; ".join(
            f"{id_type}: {msg}" for id_type, msg in errors.items()
        )
    return entry


def _check_file(records: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], bool]:
    """Validate all identifier fields across every record.

    Parameters
    ----------
    records : list[dict]
        Parsed evidence records from the input file.

    Returns
    -------
    tuple[dict, bool]
        A ``(report, has_invalid)`` pair where *report* is a dict with
        ``valid``, ``invalid``, and ``unknown`` keys, and *has_invalid*
        is ``True`` when at least one identifier has failed validation.
    """
    valid: List[Dict[str, Any]] = []
    invalid: List[Dict[str, Any]] = []
    unknown: List[Dict[str, Any]] = []

    for idx, record in enumerate(records):
        line_num: int = idx + 1
        identifiers: Dict[str, Any] = _collect_identifiers(record)
        errors: Dict[str, str] = {}

        doi_err: Optional[str] = _validate_doi(identifiers["doi"])
        if doi_err:
            errors["doi"] = doi_err

        pmid_err: Optional[str] = _validate_pmid(identifiers["pmid"])
        if pmid_err:
            errors["pmid"] = pmid_err

        trial_err: Optional[str] = _validate_trial_registration(
            identifiers["trial_registration"]
        )
        if trial_err:
            errors["trial_registration"] = trial_err

        entry: Dict[str, Any] = _build_report_entry(line_num, identifiers, errors)

        has_identifiers: bool = any(
            v is not None and str(v).strip() != ""
            for v in identifiers.values()
        )
        if errors:
            invalid.append(entry)
            log_error(
                f"Line {line_num}: invalid identifier(s) — {entry['reason']}"
            )
        elif has_identifiers:
            valid.append(entry)
            log_info(f"Line {line_num}: all identifiers valid")
        else:
            unknown.append(entry)
            log_info(f"Line {line_num}: no identifiers present")

    for entry in unknown:
        entry.setdefault("identifiers", [])

    report: Dict[str, Any] = {
        "valid": valid,
        "invalid": invalid,
        "unknown": unknown,
    }
    return report, bool(invalid)


def main() -> int:
    """Parse arguments, read input, validate identifiers, and write report."""
    parser = argparse.ArgumentParser(
        description="Validate DOI, PMID, and trial-registry ID format in evidence records.",
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

    input_path: Path = Path(args.input)

    if not input_path.exists():
        log_error(f"File not found: {input_path}")
        return 2

    try:
        records: List[Dict[str, Any]] = read_jsonl(input_path)
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSONL at {input_path}: {exc}")
        return 3

    report, has_invalid = _check_file(records)

    if args.out:
        out_path: Path = Path(args.out)
        try:
            out_path.write_text(
                json.dumps(report, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            log_info(f"Report written to {out_path}")
        except OSError as exc:
            log_error(f"Cannot write report to {out_path}: {exc}")
            return 2

    if has_invalid:
        log_error(
            f"Validation complete: {len(report['invalid'])} invalid identifier(s) found"
        )
        return 1

    log_info(
        f"Validation complete: {len(report['valid'])} valid, "
        f"{len(report['unknown'])} with no identifiers"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
