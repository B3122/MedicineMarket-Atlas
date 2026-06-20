#!/usr/bin/env python3
"""CLI for rule-based duplicate citation detection.

Compares every pair of evidence records in a JSONL file and detects
duplicate citations using exact DOI match, exact PMID match, and
title similarity (Jaccard ≥ 90 %).  The script groups mutually
duplicate records and writes a deduplication report.

The script never auto-merges records — every duplicate group requires
human review, preserving audit traceability.

Usage
-----
    python deduplicate-citations.py <input.jsonl> --out <report.json>

Match rules (ordered, short-circuit on first match)
---------------------------------------------------
    1. Exact DOI match (case-insensitive, skipping ``"unknown"``)
    2. Exact PMID match (skipping ``"unknown"``)
    3. Title Jaccard token similarity ≥ 0.90

Exit codes
----------
    0   Analysis complete (may find duplicates or not).
    2   Input file not found or missing required arguments.
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
# Ensure the skill root is on sys.path so ``scripts._common`` is importable
# ---------------------------------------------------------------------------
_SKILL_ROOT = Path(__file__).resolve().parent.parent
if str(_SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(_SKILL_ROOT))

from scripts._common import read_jsonl, log_info, log_error  # noqa: E402


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


# ---------------------------------------------------------------------------
# Title similarity
# ---------------------------------------------------------------------------

def _title_similarity(title_a: str, title_b: str) -> float:
    """Compute Jaccard similarity of word tokens between two titles.

    Tokens shorter than 3 characters are discarded (removes noise from
    stop-words, single letters, and punctuation fragments).  Returns a
    float in [0.0, 1.0].

    Parameters
    ----------
    title_a : str
        First title string.
    title_b : str
        Second title string.

    Returns
    -------
    float
        Jaccard similarity (0.0 when either title has no meaningful tokens).
    """
    ta = {t for t in _norm(title_a).split() if len(t) > 2}
    tb = {t for t in _norm(title_b).split() if len(t) > 2}
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


#: Minimum Jaccard similarity to consider two titles as a match.
_TITLE_SIMILARITY_THRESHOLD: float = 0.90


# ---------------------------------------------------------------------------
# Citation field extraction
# ---------------------------------------------------------------------------


def _citation_field(record: Dict, field: str) -> str:
    """Safely extract a field from ``record["citation"]``.

    Returns ``""`` when the citation field is missing or not a string.

    Parameters
    ----------
    record : dict
        Evidence record.
    field : str
        Field name within ``citation`` (e.g. ``"doi"``, ``"pmid"``, ``"title"``).

    Returns
    -------
    str
        The field value, or ``""`` if missing.
    """
    citation = record.get("citation", {})
    if not isinstance(citation, dict):
        return ""
    val = citation.get(field, "")
    return val if isinstance(val, str) else ""


# ---------------------------------------------------------------------------
# Pair evaluation
# ---------------------------------------------------------------------------


def _evaluate_pair(r1: Dict, r2: Dict, idx1: int, idx2: int) -> Optional[Dict]:
    """Compare two evidence records and return a match dict or ``None``.

    Detects duplicates by (in order):
    1. Exact DOI match.
    2. Exact PMID match.
    3. Title Jaccard similarity ≥ threshold.

    Returns
    -------
    dict or None
        ``None`` when the pair is not a duplicate.  Otherwise a dict with
        keys ``i``, ``j``, and ``match_reason``.
    """
    doi_a = _norm(_citation_field(r1, "doi"))
    doi_b = _norm(_citation_field(r2, "doi"))
    pmid_a = _norm(_citation_field(r1, "pmid"))
    pmid_b = _norm(_citation_field(r2, "pmid"))
    title_a = _norm(_citation_field(r1, "title"))
    title_b = _norm(_citation_field(r2, "title"))

    # 1. Exact DOI match (skip unknown)
    if doi_a and doi_b and doi_a == doi_b and not _is_unknown(doi_a):
        return {"i": idx1, "j": idx2, "match_reason": "doi"}

    # 2. Exact PMID match (skip unknown)
    if pmid_a and pmid_b and pmid_a == pmid_b and not _is_unknown(pmid_a):
        return {"i": idx1, "j": idx2, "match_reason": "pmid"}

    # 3. Title similarity
    if title_a and title_b and not _is_unknown(title_a) and not _is_unknown(title_b):
        sim = _title_similarity(title_a, title_b)
        if sim >= _TITLE_SIMILARITY_THRESHOLD:
            return {
                "i": idx1,
                "j": idx2,
                "match_reason": f"title_jaccard_{sim:.3f}",
            }

    return None


# ---------------------------------------------------------------------------
# Union-Find for grouping duplicate records
# ---------------------------------------------------------------------------

class _UnionFind:
    """Disjoint-set / union-find data structure for grouping indices."""

    def __init__(self, n: int) -> None:
        """Initialise with *n* singleton sets (indices 0 .. n-1)."""
        self._parent = list(range(n))
        self._rank = [0] * n

    def find(self, x: int) -> int:
        """Find the representative (root) of the set containing *x*."""
        while self._parent[x] != x:
            self._parent[x] = self._parent[self._parent[x]]  # path compression
            x = self._parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        """Merge the sets containing *x* and *y*."""
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return
        if self._rank[rx] < self._rank[ry]:
            self._parent[rx] = ry
        elif self._rank[rx] > self._rank[ry]:
            self._parent[ry] = rx
        else:
            self._parent[ry] = rx
            self._rank[rx] += 1

    def groups(self) -> Dict[int, List[int]]:
        """Return ``{root: [indices...]}`` for each set larger than one."""
        result: Dict[int, List[int]] = {}
        for i in range(len(self._parent)):
            root = self.find(i)
            result.setdefault(root, []).append(i)
        return {r: sorted(v) for r, v in result.items() if len(v) > 1}


# ---------------------------------------------------------------------------
# Record summary for report
# ---------------------------------------------------------------------------

def _record_summary(record: Dict, index: int) -> Dict:
    """Build a compact summary of a record for the deduplication report.

    Parameters
    ----------
    record : dict
        Evidence record.
    index : int
        Zero-based index in the input.

    Returns
    -------
    dict
        Summary with ``index``, ``source_id``, ``doi``, ``pmid``, and ``title``.
    """
    return {
        "index": index,
        "source_id": record.get("source_id", ""),
        "doi": _citation_field(record, "doi"),
        "pmid": _citation_field(record, "pmid"),
        "title": _citation_field(record, "title"),
    }


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def _detect_duplicates(
    input_path: Path,
    out_path: Path,
) -> int:
    """Load records, compare all pairs, group duplicates, write report.

    Parameters
    ----------
    input_path : Path
        Input ``.jsonl`` file.
    out_path : Path
        Output path for the JSON deduplication report.

    Returns
    -------
    int
        Exit code: 0 (success), 2 (file not found), or 3 (parse error).
    """
    # ---- Load ---------------------------------------------------------------
    try:
        records = read_jsonl(input_path)
    except FileNotFoundError:
        log_error(f"File not found: {input_path}")
        return 2
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSONL at {input_path}: {exc}")
        return 3

    n = len(records)
    if n < 2:
        log_info(f"Only {n} record(s) — nothing to compare")
        _write_report(out_path, input_path, records, [])
        return 0

    # ---- Compare all unique pairs -------------------------------------------
    uf = _UnionFind(n)
    match_reasons: Dict[Tuple[int, int], str] = {}

    for i in range(n):
        for j in range(i + 1, n):
            result = _evaluate_pair(records[i], records[j], i, j)
            if result is not None:
                uf.union(i, j)
                match_reasons[(i, j)] = result["match_reason"]

    # ---- Build duplicate groups ---------------------------------------------
    groups_map = uf.groups()
    duplicate_groups: List[Dict] = []
    for group_idx, (_, indices) in enumerate(sorted(groups_map.items()), start=1):
        # Collect reasons for all edges within this group.
        reasons: List[str] = []
        for a in range(len(indices)):
            for b in range(a + 1, len(indices)):
                key = (indices[a], indices[b])
                if key in match_reasons:
                    if match_reasons[key] not in reasons:
                        reasons.append(match_reasons[key])

        duplicate_groups.append(
            {
                "group_id": f"dup-{group_idx:04d}",
                "records": [_record_summary(records[i], i) for i in indices],
                "match_reasons": reasons,
            }
        )

    # ---- Write output -------------------------------------------------------
    _write_report(out_path, input_path, records, duplicate_groups)

    log_info(
        f"Compared {n} record(s) → {len(duplicate_groups)} duplicate group(s), "
        f"{sum(len(g['records']) for g in duplicate_groups)} record(s) flagged"
    )
    return 0


def _write_report(
    out_path: Path,
    input_path: Path,
    records: List[Dict],
    duplicate_groups: List[Dict],
) -> None:
    """Write the deduplication report as JSON.

    Parameters
    ----------
    out_path : Path
        Output file path.
    input_path : Path
        Path to the input file.
    records : list[dict]
        All input records (used for total count).
    duplicate_groups : list[dict]
        Detected duplicate groups.
    """
    output: Dict[str, Any] = {
        "input": str(input_path),
        "total_records": len(records),
        "duplicate_groups": duplicate_groups,
        "action": "require_human_review",
    }
    try:
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(output, fh, ensure_ascii=False, indent=2)
    except OSError as exc:
        log_error(f"Failed to write output to {out_path}: {exc}")
        raise
    log_info(f"Wrote deduplication report to {out_path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """Parse arguments and run citation deduplication."""
    parser = argparse.ArgumentParser(
        description="Detect duplicate citations by DOI, PMID, and title similarity",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to a .jsonl file containing evidence records",
    )
    parser.add_argument(
        "--out",
        type=str,
        required=True,
        help="Path to write the JSON deduplication report (required)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out)

    if not input_path.is_file():
        log_error(f"File not found: {input_path}")
        return 2

    return _detect_duplicates(input_path, out_path)


if __name__ == "__main__":
    sys.exit(main())
