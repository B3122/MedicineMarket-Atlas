#!/usr/bin/env python3
"""CLI for rule-based duplicate product detection.

Compares every pair of product records in a JSONL file and scores
their similarity using weighted fields.  Outputs candidate duplicate
pairs with confidence levels and human-readable reasons.

The script never auto-merges records — every candidate requires human
review, preserving audit traceability.

Usage
-----
    python scripts/detect-duplicate-products.py input.jsonl --out output.json

Weights (rules-based, not AI)
-----------------------------
* registration_id (exact match)         → high
* manufacturer + brand + dosage_form   → medium
* brand + name/ingredient similarity   → low

Exit codes
----------
    0   All records processed (candidates may be empty).
    2   Input file not found.
    3   Corrupted JSONL (parse error).

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
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import read_jsonl, log_info, log_error


# ---------------------------------------------------------------------------
# String normalisation helpers
# ---------------------------------------------------------------------------

def _norm(val: Any) -> str:
    """Strip, lowercase, and collapse whitespace on a string value."""
    if not isinstance(val, str):
        return ""
    return re.sub(r"\s+", " ", val.strip()).lower()


_UNKNOWN_TOKENS: frozenset = frozenset({"", "unknown", "n/a", "none"})


def _is_unknown(val: Any) -> bool:
    """Return True when *val* is empty, None, or a sentinel unknown value."""
    if not val or not isinstance(val, str):
        return True
    return _norm(val) in _UNKNOWN_TOKENS


def _token_similarity(a: str, b: str) -> float:
    """Jaccard similarity of word tokens between two strings."""
    ta = {t for t in a.split() if len(t) > 1}
    tb = {t for t in b.split() if len(t) > 1}
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))


# ---------------------------------------------------------------------------
# Name / ingredient similarity
# ---------------------------------------------------------------------------

def _has_name_similarity(r1: Dict, r2: Dict) -> bool:
    """Check whether two records share product-name or ingredient signals."""
    # --- standard_name ---
    sn1 = _norm(r1.get("standard_name", ""))
    sn2 = _norm(r2.get("standard_name", ""))
    if sn1 and sn2 and _token_similarity(sn1, sn2) >= 0.3:
        return True

    # --- generic_name ---
    gn1 = _norm(r1.get("generic_name", ""))
    gn2 = _norm(r2.get("generic_name", ""))
    if gn1 and gn2 and _token_similarity(gn1, gn2) >= 0.3:
        return True

    # --- shared active ingredient name (ignoring "unknown") ---
    ai1 = {
        _norm(a.get("name", ""))
        for a in r1.get("active_ingredients", [])
        if not _is_unknown(a.get("name"))
    }
    ai2 = {
        _norm(a.get("name", ""))
        for a in r2.get("active_ingredients", [])
        if not _is_unknown(a.get("name"))
    }
    if ai1 & ai2:
        return True

    return False


def _shared_ingredient_names(r1: Dict, r2: Dict) -> List[str]:
    """Return sorted list of shared, non-unknown ingredient names."""
    ai1 = {
        _norm(a.get("name", ""))
        for a in r1.get("active_ingredients", [])
        if not _is_unknown(a.get("name"))
    }
    ai2 = {
        _norm(a.get("name", ""))
        for a in r2.get("active_ingredients", [])
        if not _is_unknown(a.get("name"))
    }
    return sorted(ai1 & ai2)


# ---------------------------------------------------------------------------
# Pair evaluation
# ---------------------------------------------------------------------------

def _record_id(rec: Dict, idx: int) -> str:
    """Return the preferred human-readable identifier for a record."""
    mid = rec.get("product_master_id")
    if mid and not _is_unknown(mid):
        return str(mid)
    vid = rec.get("product_version_id")
    if vid and not _is_unknown(vid):
        return str(vid)
    return f"#record-{idx + 1}"


FIELD_LABELS: Dict[str, str] = {
    "manufacturer": "manufacturer",
    "brand": "brand",
    "dosage_form": "dosage form",
    "region": "region",
}


def _evaluate_pair(
    r1: Dict, r2: Dict, idx1: int, idx2: int
) -> Optional[Dict]:
    """Compare two product records and return a candidate dict or ``None``.

    Returns
    -------
    dict or None
        ``None`` when the pair does not reach the minimum similarity
        threshold.  Otherwise a dict with keys ``pair``, ``confidence``,
        ``reasons``, and ``action``.
    """
    id1 = _record_id(r1, idx1)
    id2 = _record_id(r2, idx2)

    # -- 1. Registration ID (exact match -> HIGH) --
    reg1 = r1.get("registration_id")
    reg2 = r2.get("registration_id")
    reg1_n = _norm(reg1) if isinstance(reg1, str) else ""
    reg2_n = _norm(reg2) if isinstance(reg2, str) else ""
    if reg1_n and reg2_n and reg1_n == reg2_n:
        return {
            "pair": [id1, id2],
            "confidence": "high",
            "reasons": [
                f"Same registration/filing number: {reg1_n}",
            ],
            "action": "require_human_review",
        }

    # -- 2. Field-level matching --
    def _fval(rec: Dict, key: str) -> str:
        v = rec.get(key)
        return _norm(v) if isinstance(v, str) else ""

    mfr1 = _fval(r1, "manufacturer")
    mfr2 = _fval(r2, "manufacturer")
    brand1 = _fval(r1, "brand")
    brand2 = _fval(r2, "brand")
    df1 = _fval(r1, "dosage_form")
    df2 = _fval(r2, "dosage_form")
    pq1 = _fval(r1, "package_quantity")
    pq2 = _fval(r2, "package_quantity")
    rg1 = _fval(r1, "region")
    rg2 = _fval(r2, "region")

    mfr_ok = bool(mfr1 and mfr2 and mfr1 == mfr2)
    brand_ok = bool(brand1 and brand2 and brand1 == brand2)
    df_ok = bool(df1 and df2 and df1 == df2 and not _is_unknown(df1))
    pq_ok = bool(pq1 and pq2 and pq1 == pq2)
    rg_ok = bool(rg1 and rg2 and rg1 == rg2)
    name_ok = _has_name_similarity(r1, r2)

    # Accumulate score for fallback classification.
    score = 0
    if mfr_ok:
        score += 30
    if brand_ok:
        score += 25
    if df_ok:
        score += 20
    if name_ok:
        score += 15
    if pq_ok:
        score += 5
    if rg_ok:
        score += 5

    # -- 3. Classify confidence --
    reasons: List[str] = []

    if mfr_ok and brand_ok and df_ok:
        reasons.append("Same manufacturer, brand, and dosage form")
        shared = _shared_ingredient_names(r1, r2)
        if shared:
            reasons.append(f"Shared active ingredient(s): {', '.join(shared)}")
        return {
            "pair": [id1, id2],
            "confidence": "medium",
            "reasons": reasons,
            "action": "require_human_review",
        }

    if brand_ok and name_ok:
        reasons.append("Same brand with shared active ingredient or similar product name")
        return {
            "pair": [id1, id2],
            "confidence": "low",
            "reasons": reasons,
            "action": "require_human_review",
        }

    if score >= 30:
        if mfr_ok:
            reasons.append("Same manufacturer")
        if brand_ok:
            reasons.append("Same brand")
        if df_ok:
            reasons.append("Same dosage form")
        if name_ok:
            shared = _shared_ingredient_names(r1, r2)
            if shared:
                reasons.append(f"Shared active ingredient(s): {', '.join(shared)}")
            else:
                reasons.append("Similar product name")
        return {
            "pair": [id1, id2],
            "confidence": "low",
            "reasons": reasons,
            "action": "require_human_review",
        }

    return None


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def _detect_duplicates(
    input_path: Path,
    out_path: Optional[Path] = None,
) -> int:
    """Load records, compare all pairs, write candidate output.

    Parameters
    ----------
    input_path : Path
        Input ``.jsonl`` file.
    out_path : Path or None
        Optional output path for the JSON result.

    Returns
    -------
    int
        Exit code: 0 (success), 2 (file not found), or 3 (parse error).
    """
    # ---- Load -----------------------------------------------------------
    try:
        records = read_jsonl(input_path)
    except FileNotFoundError:
        log_error(f"File not found: {input_path}")
        return 2
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSONL at {input_path}: {exc}")
        return 3

    # ---- Compare all unique pairs ---------------------------------------
    candidates: List[Dict] = []
    n = len(records)

    for i in range(n):
        for j in range(i + 1, n):
            result = _evaluate_pair(records[i], records[j], i, j)
            if result is not None:
                candidates.append(result)

    # ---- Write output ---------------------------------------------------
    output = {"candidates": candidates}

    if out_path:
        try:
            with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(output, fh, ensure_ascii=False, indent=2)
        except OSError as exc:
            log_error(f"Failed to write output to {out_path}: {exc}")
            return 3
        log_info(
            f"Wrote {len(candidates)} candidate pair(s) to {out_path}"
        )

    log_info(
        f"Compared {n} record(s) → {len(candidates)} candidate pair(s)"
    )
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """Parse arguments and run duplicate detection."""
    parser = argparse.ArgumentParser(
        description="Detect duplicate product records using rule-based weights",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to a .jsonl file containing product records",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Path to write the JSON output (default: stdout)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out) if args.out else None

    return _detect_duplicates(input_path, out_path)


if __name__ == "__main__":
    sys.exit(main())
