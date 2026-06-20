#!/usr/bin/env python3
"""CLI for merging price-observation / listing records into product records.

Groups input records sharing the same ``product_master_id`` (or, as a
fallback, ``product_version_id``) and merges them into a single product
record per group.  Every contributing record is preserved **as-is** inside a
``price_observations`` array — no observation data is collapsed or
overwritten.  Each merged record also receives a ``source_ids`` array that
aggregates all unique source identifiers from the group.

Usage
-----
    python scripts/merge-platform-records.py input.jsonl --out output.jsonl

Exit codes
----------
    0   All records processed successfully.
    2   Input file not found or missing arguments.
    3   Corrupted JSONL or processing error.

The input file is never modified.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Union

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so ``scripts._common`` is importable
# when this script is run as ``python scripts/merge-platform-records.py``.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import read_jsonl, write_jsonl, log_info, log_error


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

#: Fields that are specific to an individual observation and should NOT be
#: kept as top-level fields on the merged product record.  Everything else
#: from the first record of the group is treated as product identity.
_OBSERVATION_ONLY_FIELDS = frozenset({
    "source_id",
    "source_ids",
    "listing_id",
    "observation_id",
    "price",
    "currency",
    "price_type",
    "unit_price",
    "unit_price_currency",
    "unit_price_unit",
    "collection_date",
    "seller_type",
    "gift_or_bonus",
    "data_quality_score",
    "inferred_dose",
    "inference_method",
    "record_version",
})


def _collect_source_ids(group: List[Dict]) -> List[str]:
    """Aggregate every unique ``source_id`` or entry in ``source_ids``.

    Parameters
    ----------
    group : list of dict
        All records belonging to one product group.

    Returns
    -------
    list of str
        Unique source identifiers in insertion order.
    """
    seen: set = set()
    ordered: List[str] = []
    for rec in group:
        # Single source_id
        sid = rec.get("source_id")
        if isinstance(sid, str) and sid not in seen:
            seen.add(sid)
            ordered.append(sid)
        # Array source_ids
        sids = rec.get("source_ids")
        if isinstance(sids, list):
            for s in sids:
                if isinstance(s, str) and s not in seen:
                    seen.add(s)
                    ordered.append(s)
    return ordered


def _max_record_version(group: List[Dict]) -> int:
    """Return the maximum ``record_version`` across the group (default ``1``)."""
    versions = [
        rec["record_version"]
        for rec in group
        if isinstance(rec.get("record_version"), int)
    ]
    return max(versions) if versions else 1


def _merge_group(key: str, group: List[Dict]) -> Dict:
    """Merge a group of records sharing the same product identifier.

    Parameters
    ----------
    key : str
        The ``product_master_id`` (or ``product_version_id``) for the group.
    group : list of dict
        All records that belong to this product.

    Returns
    -------
    dict
        A single merged product record.
    """
    first = group[0]

    # ---- Build product-identity fields from the first record ----------------
    merged: Dict = {}
    for k, v in first.items():
        if k in _OBSERVATION_ONLY_FIELDS:
            continue
        merged[k] = v

    # ---- Ensure the merge key is always present -----------------------------
    if "product_master_id" not in merged:
        merged["product_master_id"] = key
    if "product_version_id" not in merged and "product_version_id" in first:
        merged["product_version_id"] = first["product_version_id"]

    # ---- Aggregated fields --------------------------------------------------
    merged["source_ids"] = _collect_source_ids(group)
    merged["record_version"] = _max_record_version(group)

    # ---- Collect every record as a price observation ------------------------
    observations: List[Dict] = []
    for rec in group:
        # Preserve the full record as-is (each observation keeps its own
        # platform, date, source, price, etc.)
        obs = dict(rec)
        # Remove the product-level identifier from the observation copy to
        # avoid unnecessary redundancy — the observation lives under a
        # merged record that already carries it.
        obs.pop("product_master_id", None)
        observations.append(obs)

    merged["price_observations"] = observations

    return merged


# ---------------------------------------------------------------------------
# Core processing
# ---------------------------------------------------------------------------


def _process_records(
    path: Path,
    out_path: Optional[Path] = None,
) -> int:
    """Read, group, merge, and write platform records.

    Parameters
    ----------
    path : Path
        Input ``.jsonl`` file.
    out_path : Path or None
        Optional output path for merged JSONL.

    Returns
    -------
    int
        Exit code: 0 (success), 2 (file not found), 3 (parse / processing error).
    """
    # ---- Read & parse -------------------------------------------------------
    try:
        records = read_jsonl(path)
    except FileNotFoundError:
        log_error(f"File not found: {path}")
        return 2
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSONL at {path}: {exc}")
        return 3

    # ---- Group by product identity ------------------------------------------
    groups: Dict[str, List[Dict]] = OrderedDict()
    skipped = 0
    for rec in records:
        key = rec.get("product_master_id")
        if key is None or not isinstance(key, str) or not key.strip():
            key = rec.get("product_version_id")
        if key is None or not isinstance(key, str) or not key.strip():
            # No merge key → emit as a singleton product record later
            # Use a unique sentinel so it gets its own group
            key = f"__nokey__{skipped}"
            skipped += 1
        groups.setdefault(key, []).append(rec)

    # ---- Merge each group ---------------------------------------------------
    merged_records: List[Dict] = []
    for key, group in groups.items():
        merged_records.append(_merge_group(key, group))

    # ---- Write output -------------------------------------------------------
    if out_path:
        try:
            write_jsonl(out_path, merged_records)
        except OSError as exc:
            log_error(f"Failed to write output to {out_path}: {exc}")
            return 3
        log_info(f"Wrote {len(merged_records)} merged record(s) to {out_path}")

    log_info(
        f"Done: {len(merged_records)} product record(s) "
        f"from {len(records)} input observation(s)"
    )
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments and run merging."""
    parser = argparse.ArgumentParser(
        description=(
            "Merge price-observation / listing records into product records "
            "by product_master_id."
        ),
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to a .jsonl file containing platform records",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Path to write merged JSONL output",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out) if args.out else None

    log_info(f"Merging platform records from: {input_path}")
    exit_code = _process_records(input_path, out_path)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
