#!/usr/bin/env python3
"""CLI that generates a markdown evidence table from validated evidence JSONL.

Reads evidence records and produces a formatted markdown table with standard
columns: Study, Design, Population, Intervention, Outcomes, Effect, Certainty.
Supports optional filtering by study design and outcome keyword.

Usage
-----
    python scripts/build-evidence-table.py input.jsonl --out table.md
    python scripts/build-evidence-table.py input.jsonl --out table.md --filter-design rct
    python scripts/build-evidence-table.py input.jsonl --out table.md --filter-outcome mortality

Input
-----
JSONL file with validated evidence records matching ``evidence.schema.json``.
Each record is expected to contain at least the required schema fields.

Output
------
A markdown-formatted file with a header row, separator row, and one body
row per record that passes the optional filters. Missing data is rendered
as ``unknown`` — never fabricated.

Exit codes
----------
0   Table generated and written successfully.
2   File not found, missing ``--out`` argument, or write error.
3   Corrupted JSONL (unparseable line).

The input file is never modified.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so ``scripts._common`` is importable
# when this script is run as ``python scripts/build-evidence-table.py``.
# ---------------------------------------------------------------------------
_SKILL_ROOT = Path(__file__).resolve().parent.parent
if str(_SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(_SKILL_ROOT))

from scripts._common import read_jsonl, log_info, log_error  # noqa: E402

# ---------------------------------------------------------------------------
# Output column definitions
# ---------------------------------------------------------------------------

#: Ordered list of output column headers for the markdown table.
TABLE_COLUMNS: List[str] = [
    "Study",
    "Design",
    "Population",
    "Intervention",
    "Outcomes",
    "Effect",
    "Certainty",
]

#: Sentinel value used for any missing or unavailable data.
SENTINEL: str = "unknown"


def _extract_study_label(record: Dict[str, Any]) -> str:
    """Build a short study label from the citation and/or source ID.

    Prefers the citation title; falls back to the citation DOI, then the
    record ``source_id``; returns the sentinel if nothing is available.

    Parameters
    ----------
    record : dict
        One evidence record.

    Returns
    -------
    str
        A human-readable label for the study.
    """
    citation: Dict[str, Any] = record.get("citation", {}) or {}
    title: str = citation.get("title", "")
    if title and title.strip():
        return title.strip()
    doi: str = citation.get("doi", "")
    if doi and doi.strip() and doi != SENTINEL:
        return doi.strip()
    source_id: str = record.get("source_id", "")
    if source_id and source_id.strip():
        return source_id.strip()
    return SENTINEL


def _extract_design(record: Dict[str, Any]) -> str:
    """Extract the study design field, normalising to a human-readable label.

    Parameters
    ----------
    record : dict
        One evidence record.

    Returns
    -------
    str
        A readable study design string, or the sentinel.
    """
    raw: str = record.get("study_design", "")
    if not raw or raw == SENTINEL:
        return SENTINEL

    # Map internal schema values to display labels
    design_map: Dict[str, str] = {
        "rct": "RCT",
        "systematic_review": "Systematic Review",
        "meta_analysis": "Meta-Analysis",
        "observational_cohort": "Observational Cohort",
        "observational_case_control": "Case-Control",
        "cross_sectional": "Cross-Sectional",
        "case_report": "Case Report",
        "expert_opinion": "Expert Opinion",
    }
    return design_map.get(raw, raw.replace("_", " ").title())


def _extract_population(record: Dict[str, Any]) -> str:
    """Build a population description from the record.

    Combines the ``population`` description string with the ``sample_size``
    field for compact display.

    Parameters
    ----------
    record : dict
        One evidence record.

    Returns
    -------
    str
        A population description, or the sentinel.
    """
    pop: str = record.get("population", "")
    sample: str = record.get("sample_size", "")

    parts: List[str] = []
    if pop and pop.strip() and pop != SENTINEL:
        parts.append(pop.strip())
    if sample and str(sample).strip() and str(sample) != SENTINEL:
        parts.append(f"n={sample}")
    return "; ".join(parts) if parts else SENTINEL


def _extract_intervention(record: Dict[str, Any]) -> str:
    """Extract the intervention or exposure description.

    Parameters
    ----------
    record : dict
        One evidence record.

    Returns
    -------
    str
        Intervention description, or the sentinel.
    """
    raw: str = record.get("intervention", "")
    if not raw or raw == SENTINEL:
        return SENTINEL
    return raw.strip()


def _extract_outcomes(record: Dict[str, Any]) -> str:
    """Extract and join outcome strings into a compact display.

    Parameters
    ----------
    record : dict
        One evidence record.

    Returns
    -------
    str
        Comma-separated outcome names, or the sentinel.
    """
    outcomes: Any = record.get("outcomes")
    if outcomes is None:
        return SENTINEL
    if isinstance(outcomes, list):
        items: List[str] = [str(o) for o in outcomes if o is not None]
        return ", ".join(items) if items else SENTINEL
    if isinstance(outcomes, str):
        val: str = outcomes.strip()
        return val if val else SENTINEL
    return SENTINEL


def _extract_effect(record: Dict[str, Any]) -> str:
    """Format the primary effect estimate into a compact string.

    Uses the first entry in ``effect_estimates`` when available.  Includes
    the metric, point estimate, and 95% confidence interval when present.

    Parameters
    ----------
    record : dict
        One evidence record.

    Returns
    -------
    str
        Formatted effect estimate string, or the sentinel.
    """
    estimates: Any = record.get("effect_estimates")
    if not estimates or not isinstance(estimates, list) or len(estimates) == 0:
        return SENTINEL

    est: Dict[str, Any] = estimates[0]
    metric: str = est.get("metric", "")
    value: str = est.get("value", "")
    ci_lower: str = est.get("ci_lower", "")
    ci_upper: str = est.get("ci_upper", "")

    if not value or value == SENTINEL:
        return SENTINEL

    parts: List[str] = []
    if metric and metric != SENTINEL:
        parts.append(f"{metric}")
    parts.append(str(value))

    if ci_lower and ci_lower != SENTINEL and ci_upper and ci_upper != SENTINEL:
        parts.append(f"(95% CI {ci_lower}–{ci_upper})")
    elif ci_lower and ci_lower != SENTINEL:
        parts.append(f"(95% CI {ci_lower}–?)")
    elif ci_upper and ci_upper != SENTINEL:
        parts.append(f"(95% CI ?–{ci_upper})")

    return " ".join(parts)


def _extract_certainty(record: Dict[str, Any]) -> str:
    """Extract the evidence certainty level.

    Uses ``evidence_level`` from the record; maps schema values to
    display labels.

    Parameters
    ----------
    record : dict
        One evidence record.

    Returns
    -------
    str
        Readable certainty label, or the sentinel.
    """
    raw: str = record.get("evidence_level", "")
    if not raw or raw == SENTINEL:
        return SENTINEL

    certainty_map: Dict[str, str] = {
        "high": "High",
        "moderate": "Moderate",
        "low": "Low",
        "very_low": "Very Low",
    }
    return certainty_map.get(raw, raw.replace("_", " ").title())


def _apply_filters(
    records: List[Dict[str, Any]],
    filter_design: Optional[str],
    filter_outcome: Optional[str],
) -> List[Dict[str, Any]]:
    """Return records matching the optional study-design and outcome filters.

    Parameters
    ----------
    records : list[dict]
        All parsed evidence records.
    filter_design : str or None
        If set, keep only records whose ``study_design`` matches this value
        (case-insensitive substring match).
    filter_outcome : str or None
        If set, keep only records where any outcome string contains this
        keyword (case-insensitive).

    Returns
    -------
    list[dict]
        Filtered records.
    """
    filtered: List[Dict[str, Any]] = []
    for record in records:
        if filter_design:
            design: str = record.get("study_design", "")
            if filter_design.lower() not in design.lower():
                continue
        if filter_outcome:
            outcomes: Any = record.get("outcomes")
            match_found: bool = False
            if isinstance(outcomes, list):
                for o in outcomes:
                    if o is not None and filter_outcome.lower() in str(o).lower():
                        match_found = True
                        break
            elif isinstance(outcomes, str):
                if filter_outcome.lower() in outcomes.lower():
                    match_found = True
            if not match_found:
                continue
        filtered.append(record)
    return filtered


def _build_markdown_table(records: List[Dict[str, Any]]) -> str:
    """Build a markdown evidence table from a list of evidence records.

    Parameters
    ----------
    records : list[dict]
        Evidence records to include in the table.

    Returns
    -------
    str
        A complete markdown-formatted table as a string.
    """
    lines: List[str] = []

    # Header row
    header: str = "| " + " | ".join(TABLE_COLUMNS) + " |"
    lines.append(header)

    # Separator row
    separator: str = "|" + "|".join(" --- " for _ in TABLE_COLUMNS) + "|"
    lines.append(separator)

    # Data rows
    for record in records:
        study: str = _extract_study_label(record)
        design: str = _extract_design(record)
        population: str = _extract_population(record)
        intervention: str = _extract_intervention(record)
        outcomes: str = _extract_outcomes(record)
        effect: str = _extract_effect(record)
        certainty: str = _extract_certainty(record)

        # Escape pipe characters in cell content for correct markdown rendering
        values: List[str] = [
            study.replace("|", "\\|"),
            design.replace("|", "\\|"),
            population.replace("|", "\\|"),
            intervention.replace("|", "\\|"),
            outcomes.replace("|", "\\|"),
            effect.replace("|", "\\|"),
            certainty.replace("|", "\\|"),
        ]
        row: str = "| " + " | ".join(values) + " |"
        lines.append(row)

    return "\n".join(lines) + "\n"


def main() -> int:
    """Parse arguments, read, filter, and build the evidence table."""
    parser = argparse.ArgumentParser(
        description="Generate a markdown evidence table from validated evidence records.",
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
        help="Output file path for the markdown table (.md)",
    )
    parser.add_argument(
        "--filter-design",
        type=str,
        default=None,
        help="Filter records by study design (case-insensitive substring match)",
    )
    parser.add_argument(
        "--filter-outcome",
        type=str,
        default=None,
        help="Filter records by outcome keyword (case-insensitive substring match)",
    )
    args = parser.parse_args()

    input_path: Path = Path(args.input)
    output_path: Path = Path(args.out)

    if not input_path.exists():
        log_error(f"File not found: {input_path}")
        return 2

    try:
        records: List[Dict[str, Any]] = read_jsonl(input_path)
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSONL at {input_path}: {exc}")
        return 3

    if not records:
        log_error(f"No records found in {input_path}")
        return 2

    log_info(f"Read {len(records)} record(s) from {input_path}")

    # Apply optional filters
    if args.filter_design:
        log_info(f"Filtering by study design: {args.filter_design!r}")
    if args.filter_outcome:
        log_info(f"Filtering by outcome keyword: {args.filter_outcome!r}")

    filtered: List[Dict[str, Any]] = _apply_filters(
        records,
        args.filter_design,
        args.filter_outcome,
    )
    log_info(f"{len(filtered)} record(s) after filtering")

    if not filtered:
        log_info("No records match the filter criteria; writing empty table")
        # Write a minimal table with header only
        header: str = "| " + " | ".join(TABLE_COLUMNS) + " |\n"
        separator: str = "|" + "|".join(" --- " for _ in TABLE_COLUMNS) + "|\n"
        try:
            output_path.write_text(header + separator, encoding="utf-8")
        except OSError as exc:
            log_error(f"Cannot write to {output_path}: {exc}")
            return 2
        return 0

    # Build and write the table
    table_md: str = _build_markdown_table(filtered)

    try:
        output_path.write_text(table_md, encoding="utf-8")
        log_info(f"Evidence table written to {output_path}")
    except OSError as exc:
        log_error(f"Cannot write to {output_path}: {exc}")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
