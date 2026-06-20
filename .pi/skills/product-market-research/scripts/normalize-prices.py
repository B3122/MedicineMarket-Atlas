#!/usr/bin/env python3
"""CLI for normalizing prices in listing records.

Computes per-package unit price, flags bundles and gifts,
and preserves original price, currency, and date fields.

Usage
-----
    python scripts/normalize-prices.py input.jsonl --out output.jsonl

Exit codes
----------
    0   All records processed successfully.
    1   One or more records have missing or unknown currency.
    2   File not found.
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
# when this script is run as ``python scripts/normalize-prices.py``.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import read_jsonl, write_jsonl, log_info, log_error


# ---------------------------------------------------------------------------
# Currency check
# ---------------------------------------------------------------------------


def _is_currency_missing(record: Dict) -> bool:
    """Check whether a record's currency is absent, empty, or ``"unknown"``.

    Parameters
    ----------
    record : dict
        A single listing record.

    Returns
    -------
    bool
        ``True`` if the currency cannot be determined.
    """
    currency = record.get("currency")
    if currency is None:
        return True
    if not isinstance(currency, str):
        return True
    stripped = currency.strip()
    if not stripped:
        return True
    if stripped.lower() == "unknown":
        return True
    return False


# ---------------------------------------------------------------------------
# Normalization logic
# ---------------------------------------------------------------------------


def _normalize_record(record: Dict) -> Dict:
    """Add a ``normalized`` sub-object to *record* with computed fields.

    Parameters
    ----------
    record : dict
        A single listing record (mutated in place).

    Returns
    -------
    dict
        The same record with a ``normalized`` key added.
    """
    normalized: Dict[str, Union[float, bool, None]] = {}

    # ---- Unit price -------------------------------------------------------
    price = record.get("price")
    package_qty = record.get("package_quantity")

    if (
        isinstance(price, (int, float))
        and isinstance(package_qty, (int, float))
        and package_qty > 0
    ):
        normalized["unit_price"] = price / package_qty
    else:
        normalized["unit_price"] = None

    # ---- Bundle detection -------------------------------------------------
    price_type = record.get("price_type")
    normalized["is_bundle"] = bool(price_type == "bundle_price")

    # ---- Gift detection ---------------------------------------------------
    gift_or_bonus = record.get("gift_or_bonus")
    normalized["is_gift"] = bool(
        gift_or_bonus is not None
        and isinstance(gift_or_bonus, str)
        and gift_or_bonus.strip()
    )

    record["normalized"] = normalized
    return record


def _process_records(
    path: Path,
    out_path: Optional[Path] = None,
) -> int:
    """Read, normalize, and write listing records.

    Parameters
    ----------
    path : Path
        Input ``.jsonl`` file.
    out_path : Path or None
        Optional output path.

    Returns
    -------
    int
        Exit code: 0 (success), 1 (missing currency), 2 (file not found),
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

    # ---- Validate currency ------------------------------------------------
    missing_currency = False
    for idx, rec in enumerate(records):
        if _is_currency_missing(rec):
            lid = rec.get("listing_id", "?")
            log_error(f"Line {idx + 1}: missing currency in record {lid}")
            missing_currency = True

    if missing_currency:
        return 1

    # ---- Normalize --------------------------------------------------------
    for rec in records:
        _normalize_record(rec)

    # ---- Write output -----------------------------------------------------
    if out_path:
        try:
            write_jsonl(out_path, records)
        except OSError as exc:
            log_error(f"Failed to write output to {out_path}: {exc}")
            return 3
        log_info(f"Wrote {len(records)} normalized record(s) to {out_path}")

    log_info(f"Done: {len(records)} record(s) normalized")
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments and run price normalisation."""
    parser = argparse.ArgumentParser(
        description="Normalize prices in listing records",
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
        help="Path to write normalized JSONL output",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out) if args.out else None

    log_info(f"Normalizing prices from: {input_path}")
    exit_code = _process_records(input_path, out_path)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
