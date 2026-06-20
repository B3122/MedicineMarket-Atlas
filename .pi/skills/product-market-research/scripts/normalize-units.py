#!/usr/bin/env python3
"""Normalize mass/volume units in listing records to base units (mg/mL).

Reads a JSONL file of listing records, parses the ``package_size`` field,
and normalises mass units to mg, volume units to mL, while preserving
count-unit values as-is.  Each record is augmented with a ``normalized``
sub-object that contains the normalised value, unit category, and original
unit.  The original ``package_size`` field is never modified.

Usage
-----
    python scripts/normalize-units.py input.jsonl --out output.jsonl

Exit codes
----------
    0   All records processed successfully.
    1   One or more records have unparseable or missing units.
    2   Input file not found or missing required arguments.
    3   Corrupted JSONL or other processing error.

The input file is never modified.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so ``scripts._common`` is importable
# when this script is run as ``python scripts/normalize-units.py``.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import (
    _QUANTITY_RE,
    _UNIT_ALIASES,
    parse_quantity,
    read_jsonl,
    write_jsonl,
    log_info,
    log_error,
)


# ---------------------------------------------------------------------------
# Normalisation logic
# ---------------------------------------------------------------------------

#: Canonical key names for each quantity category in the normalised output.
_CATEGORY_KEY = {
    "mass": "mass_mg",
    "volume": "volume_mL",
    "count": "count",
}

#: Pattern to find the first number+unit pair inside a compound string.
#: Similar to ``_QUANTITY_RE`` but without ``^`` / ``$`` anchors so that
#: ``re.search`` can locate a parseable segment anywhere in the input.
_COMPOUND_FALLBACK_RE = re.compile(
    r"([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*"
    r"(μg|µg|mcg|ug|mg|g|mL|ml|milliliter|milliliters|millilitre|millilitres"
    r"|L|l|liter|liters|litre|litres"
    r"|caps|capsule|capsules|cap|tabs|tablet|tablets|tab|bags|bag|each|units?)",
    re.IGNORECASE,
)


def _normalize_record(record: Dict, line_num: int) -> Tuple[Dict, bool]:
    """Parse ``package_size`` and attach a ``normalized`` sub-object.

    Parameters
    ----------
    record : dict
        A single listing record.  Must contain a ``package_size`` field.
    line_num : int
        1-based line number for error reporting.

    Returns
    -------
    tuple[dict, bool]
        The (possibly augmented) record and a boolean indicating whether a
        unit conversion was actually performed (i.e. the value was normalised
        to a different unit than the original).

    Raises
    ------
    ValueError
        If ``package_size`` is missing, empty, or its unit cannot be parsed.
    """
    package_size = record.get("package_size")
    if not package_size or not isinstance(package_size, str):
        raise ValueError(
            f"Line {line_num}: missing_unit - package_size field is missing or empty"
        )

    try:
        parsed = parse_quantity(package_size)
    except ValueError as exc:
        # Distinguish cross-category incompatibility from plain parse failures.
        msg = str(exc)
        if "incompatible" in msg:
            raise ValueError(
                f"Line {line_num}: incompatible - {msg}"
            ) from exc

        # Compound string fallback: try to extract the first parseable
        # number+unit pair (e.g. "5 mL" from "10 ampoules (5 mL each)").
        match = _COMPOUND_FALLBACK_RE.search(package_size)
        if match:
            extracted = f"{match.group(1)} {match.group(2)}"
            log_info(
                f"Line {line_num}: warning - compound package_size "
                f"{package_size!r}, using first parseable segment {extracted!r}"
            )
            parsed = parse_quantity(extracted)
        else:
            raise ValueError(
                f"Line {line_num}: missing_unit - cannot parse package_size "
                f"{package_size!r}: {msg}"
            ) from exc

    value: float = parsed["value"]
    unit: str = parsed["unit"]

    if unit == "mg":
        category = "mass"
    elif unit == "mL":
        category = "volume"
    else:
        category = "count"

    original_unit = _extract_original_canonical(package_size)
    did_convert = original_unit is not None and original_unit != unit

    # Build the normalized sub-object.
    normalized: Dict = {
        _CATEGORY_KEY[category]: value,
        "unit_category": category,
    }
    if original_unit is not None:
        normalized["original_unit"] = original_unit

    result = dict(record)
    result["normalized"] = normalized
    return result, did_convert


def _extract_original_canonical(package_size: str) -> Optional[str]:
    """Extract the original canonical unit from a package_size string.

    Uses the shared regex from ``_common`` to get the raw unit token, then
    resolves any alias to its canonical form (e.g. ``"milligrams" → "mg"``).

    Returns ``None`` if the string cannot be parsed.
    """
    match = _QUANTITY_RE.match(package_size)
    if not match:
        return None
    raw_unit = match.group(2).lower()
    return _UNIT_ALIASES.get(raw_unit, raw_unit)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments, normalise units, write output, and return exit code."""
    parser = argparse.ArgumentParser(
        description=(
            "Normalise mass/volume units in listing records to base units "
            "(mg for mass, mL for volume).  Count units are preserved as-is.  "
            "Each record is augmented with a ``normalized`` sub-object."
        ),
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to a .jsonl file containing listing records",
    )
    parser.add_argument(
        "--out",
        type=str,
        required=True,
        help="Path to write the normalised .jsonl output",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.out)

    # ---- Read ---------------------------------------------------------------
    try:
        records = read_jsonl(input_path)
    except FileNotFoundError:
        log_error(f"File not found: {input_path}")
        return 2
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSONL at {input_path}: {exc}")
        return 3

    # ---- Normalise each record ----------------------------------------------
    normalised: List[Dict] = []
    errors: List[str] = []
    conversion_count = 0

    for idx, record in enumerate(records):
        line_num = idx + 1
        try:
            result, did_convert = _normalize_record(record, line_num)
            normalised.append(result)
            if did_convert:
                conversion_count += 1
        except ValueError as exc:
            errors.append(str(exc))

    # ---- Report errors (if any) ---------------------------------------------
    if errors:
        for err in errors:
            log_error(err)
        log_error(
            f"FAIL: {len(errors)} record(s) with unparseable or missing units"
        )
        return 1

    # ---- Write output -------------------------------------------------------
    try:
        write_jsonl(output_path, normalised)
    except OSError as exc:
        log_error(f"Cannot write output {output_path}: {exc}")
        return 3

    # ---- Summary ------------------------------------------------------------
    total = len(normalised)
    log_info(f"Processed {total} record(s), {conversion_count} with unit conversion(s)")
    log_info(f"Output written to {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
