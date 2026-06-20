#!/usr/bin/env python3
"""CLI for calculating daily cost from price-observation records.

Reads a JSONL file of price-observation records and computes the daily
cost for each record that has a valid price, package quantity, and daily
dose.  Records with inferred (not declared) dosage are rejected.  Records
without a daily dose are given a null daily cost.

Never infers daily dosage.

Usage
-----
    python scripts/calculate-daily-cost.py input.jsonl --out output.jsonl

Exit codes
----------
    0   All records processed (non-calculable records skipped).
    1   Inferred dosage rejected, or all records lack daily dose info.
    2   Input file not found.
    3   Corrupted JSONL or processing error.

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
# when this script is run as ``python scripts/calculate-daily-cost.py``.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import read_jsonl, write_jsonl, log_info, log_error


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_dose_inferred(record: Dict) -> bool:
    """Check whether the daily dose in *record* was inferred rather than declared.

    The price-observation schema uses ``daily_cost_source == "assumption"``
    as the standard inference flag.  A ``daily_dose_source == "inferred"``
    field is also recognised as an alternative indicator.

    Parameters
    ----------
    record : dict
        A single price-observation record.

    Returns
    -------
    bool
        ``True`` if the dose was inferred.
    """
    if record.get("daily_cost_source") == "assumption":
        return True
    if record.get("daily_dose_source") == "inferred":
        return True
    return False


def _has_valid_dose(record: Dict) -> bool:
    """Check whether *record* has a usable daily dose value.

    Parameters
    ----------
    record : dict
        A single price-observation record.

    Returns
    -------
    bool
        ``True`` if ``daily_dose_used`` is a positive number.
    """
    dose = record.get("daily_dose_used")
    return isinstance(dose, (int, float)) and dose > 0


def _calculate_record(record: Dict) -> Dict:
    """Add a ``normalized`` sub-object with the daily cost computation.

    The returned record always contains a ``normalized`` key.  When the
    required inputs are present and valid the sub-object includes the
    calculated cost; otherwise ``daily_cost`` is set to ``null`` with a
    descriptive ``formula`` explaining why.

    Parameters
    ----------
    record : dict
        A single price-observation record (mutated in place).

    Returns
    -------
    dict
        The same record with ``normalized`` key added.
    """
    normalized: Dict[str, Union[float, str, list, None]] = {}

    price = record.get("price")
    package_qty = record.get("package_quantity")
    daily_dose = record.get("daily_dose_used")
    daily_dose_unit = record.get("daily_dose_unit", "")
    currency = record.get("currency", "")

    # ---- Validate inputs --------------------------------------------------
    price_ok = isinstance(price, (int, float))
    qty_ok = isinstance(package_qty, (int, float)) and (package_qty is not None and package_qty > 0)
    dose_ok = isinstance(daily_dose, (int, float)) and (daily_dose is not None and daily_dose > 0)
    currency_ok = isinstance(currency, str) and currency.strip() != ""

    can_calculate = price_ok and qty_ok and dose_ok and currency_ok

    if can_calculate:
        # Safe to divide -- qty_ok ensures package_qty > 0
        daily_cost = (price / package_qty) * daily_dose  # type: ignore[operator]

        # Build a readable formula string
        formula = (
            f"({price:.2f} / {package_qty}) * {daily_dose} = {daily_cost:.2f} {currency}/d"
        )

        # Assumptions list
        assumptions: List[str] = []
        dose_source = record.get("daily_cost_source", "")
        if dose_source:
            assumptions.append(
                f"assumed {daily_dose} {daily_dose_unit} per day per {dose_source}"
            )

        normalized["daily_cost"] = round(daily_cost, 2)
        normalized["formula"] = formula
        normalized["daily_dose_used"] = daily_dose
        normalized["daily_dose_unit"] = daily_dose_unit if daily_dose_unit else None
        normalized["daily_cost_source"] = dose_source if dose_source else None
        normalized["assumptions"] = assumptions
    else:
        # Determine why calculation is impossible
        if not dose_ok:
            reason = "Cannot calculate: daily_dose_used is missing or invalid"
        elif not price_ok:
            reason = "Cannot calculate: price is missing or invalid"
        elif not qty_ok:
            reason = "Cannot calculate: package_quantity is missing or invalid"
        elif not currency_ok:
            reason = "Cannot calculate: currency is missing or invalid"
        else:
            reason = "Cannot calculate: insufficient inputs"

        normalized["daily_cost"] = None
        normalized["formula"] = reason
        normalized["daily_dose_used"] = None
        normalized["daily_dose_unit"] = None
        normalized["daily_cost_source"] = None
        normalized["assumptions"] = []

    record["normalized"] = normalized
    return record


# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------


def _process_records(
    path: Path,
    out_path: Optional[Path] = None,
) -> int:
    """Read, validate, compute, and write price-observation records.

    Parameters
    ----------
    path : Path
        Input ``.jsonl`` file.
    out_path : Path or None
        Optional output path.

    Returns
    -------
    int
        Exit code: 0 (success), 1 (inferred / all-missing dose),
        2 (file not found), or 3 (parse error).
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

    # ---- Check: inferred dosage (reject immediately) ----------------------
    for rec in records:
        if _is_dose_inferred(rec):
            oid = rec.get("observation_id", "?")
            log_error(f"Record {oid}: inferred dosage rejected")

    if any(_is_dose_inferred(rec) for rec in records):
        log_error("FAIL: inferred_dosage_rejected")
        return 1

    # ---- Check: all records missing dose? ---------------------------------
    calculable_count = sum(1 for rec in records if _has_valid_dose(rec))

    # ---- Compute ----------------------------------------------------------
    processed: List[Dict] = []
    for rec in records:
        _calculate_record(rec)
        processed.append(rec)

    # ---- Exit 1 when no record has a valid daily dose ---------------------
    if calculable_count == 0:
        log_error("FAIL: daily_dosage_missing")
        return 1

    # ---- Write output -----------------------------------------------------
    if out_path is not None:
        try:
            write_jsonl(out_path, processed)
        except OSError as exc:
            log_error(f"Cannot write output {out_path}: {exc}")
            return 3
        log_info(f"Wrote {len(processed)} record(s) to {out_path}")

    log_info(
        f"Done: {len(processed)} record(s) processed, "
        f"{calculable_count} with daily cost calculated"
    )
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments and run daily cost calculation."""
    parser = argparse.ArgumentParser(
        description="Calculate daily cost from price-observation records",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to a .jsonl file containing price-observation records",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Path to write output JSONL with normalized daily cost",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out) if args.out else None

    log_info(f"Calculating daily costs from: {input_path}")
    exit_code = _process_records(input_path, out_path)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
