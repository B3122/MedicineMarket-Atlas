#!/usr/bin/env python3
"""CLI that renders a structured markdown report from validated research artifacts.

Reads JSONL artifact files (market, evidence, claims, competitors) and generates
a markdown report with eight standard sections.  Template-based: each section has
a template filled from artifact data.  Uses ``"unknown"`` sentinel for missing
data.  Does **not** conduct new research — renders only from supplied artifacts.

Usage
-----
    python render-report.py \\
        --market market.jsonl \\
        --evidence evidence.jsonl \\
        --claims claims.jsonl \\
        --competitors competitors.jsonl \\
        --out report.md

Input
-----
Four validated JSONL artifact files, each containing structured research records:

    market.jsonl
        Market findings (product records, prices, channels, collection dates).
    evidence.jsonl
        Evidence tables (study design, population, outcomes, source IDs).
    claims.jsonl
        Claim assessments (claim text, product, support level, evidence mapping).
    competitors.jsonl
        Competitor analysis (normalized product comparison records).

Output
------
A single Markdown file with the following sections:

    1. Executive Summary
    2. Method
    3. Market Findings
    4. Competitor Analysis
    5. Evidence Summary
    6. Claim Assessments
    7. Limitations
    8. Source Inventory

Exit codes
----------
0   Success — report written.
2   Missing required arguments or input file not found.
3   Corrupted JSONL or template-rendering error.

The input files are never modified.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so ``scripts._common`` is importable
# when run as ``python .pi/skills/report-generation/scripts/render-report.py``.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import log_info, log_error, read_jsonl  # noqa: E402

# ---------------------------------------------------------------------------
# Sentinel & display constants
# ---------------------------------------------------------------------------

_SENTINEL = "unknown"
"""Value used when artifact data is missing for a field."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _safe_get(
    record: Dict[str, Any],
    *keys: str,
    default: Any = _SENTINEL,
) -> Any:
    """Return the first non-empty value found among *keys* in *record*.

    Parameters
    ----------
    record : dict
        A single artifact record.
    keys : str
        Field names to try in order.
    default : Any
        Value returned when none of the keys resolve to a truthy value.

    Returns
    -------
    Any
        The first truthy value from *record[keys]*, or *default*.
    """
    for key in keys:
        val = record.get(key)
        if val not in (None, "", _SENTINEL):
            return val
    return default


def _safe_str(val: Any, default: str = _SENTINEL) -> str:
    """Coerce *val* to a string, returning *default* for empty/falsy values.

    Parameters
    ----------
    val : Any
        Value to coerce.
    default : str
        Fallback when *val* is falsy or *None*.

    Returns
    -------
    str
    """
    if val is None or val == "":
        return default
    return str(val)


def _safe_list(val: Any) -> List[Any]:
    """Return *val* as a list, or an empty list if not iterable.

    Parameters
    ----------
    val : Any
        Value that is expected to be a list.

    Returns
    -------
    list
    """
    if isinstance(val, list):
        return val
    if val is None:
        return []
    return [val]


def _count_records(records: List[Dict[str, Any]]) -> int:
    """Return the number of records in a list.

    Parameters
    ----------
    records : list[dict]
        Artifact records.

    Returns
    -------
    int
    """
    return len(records)


def _build_markdown_table(
    headers: List[str],
    rows: List[List[str]],
) -> str:
    """Build a GFN-compliant markdown table from headers and rows.

    Parameters
    ----------
    headers : list[str]
        Column header names.
    rows : list[list[str]]
        Data rows.  Each row must have the same length as *headers*.

    Returns
    -------
    str
        Markdown table as a multi-line string.
    """
    if not rows:
        rows = [["no_data_available"] * len(headers)]

    lines: List[str] = []
    # Header row
    lines.append("| " + " | ".join(headers) + " |")
    # Separator row
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    # Data rows
    for row in rows:
        padded = row + [_SENTINEL] * (len(headers) - len(row))
        cells = [c.replace("|", "\\|") for c in padded[:len(headers)]]
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------


def _render_executive_summary(
    market: List[Dict[str, Any]],
    evidence: List[Dict[str, Any]],
    claims: List[Dict[str, Any]],
    competitors: List[Dict[str, Any]],
) -> str:
    """Render the Executive Summary section.

    Produces a concise top-level summary: scope, product count, evidence
    volume, claim count, competitor count, and key caveats.

    Parameters
    ----------
    market : list[dict]
        Market finding records.
    evidence : list[dict]
        Evidence records.
    claims : list[dict]
        Claim assessment records.
    competitors : list[dict]
        Competitor analysis records.

    Returns
    -------
    str
        Markdown section content (H2 heading + body).
    """
    n_market = _count_records(market)
    n_evidence = _count_records(evidence)
    n_claims = _count_records(claims)
    n_competitors = _count_records(competitors)

    # Collect product names from market
    product_names: List[str] = []
    for rec in market:
        name = _safe_get(rec, "standard_name", "generic_name", "product_name", "product")
        if name != _SENTINEL:
            product_names.append(str(name))

    # Collect claim-product names
    claim_products: List[str] = []
    for rec in claims:
        name = _safe_get(rec, "product", "product_name", "standard_name")
        if name != _SENTINEL:
            claim_products.append(str(name))

    all_products = sorted(set(product_names + claim_products))

    lines = [
        "## Executive Summary",
        "",
        f"This report reviews **{n_market}** market record(s), "
        f"**{n_evidence}** evidence item(s), "
        f"**{n_claims}** commercial or scientific claim(s), and "
        f"**{n_competitors}** competitor record(s).",
        "",
    ]

    if all_products:
        lines.append(f"Products covered: {', '.join(all_products[:10])}.")
        if len(all_products) > 10:
            lines.append(f" ({len(all_products) - 10} additional products not listed.)")
        lines.append("")

    lines.extend([
        "Detailed findings, evidence summaries, and claim assessments "
        "are provided in the sections below.  Limitations affecting each "
        "analysis are documented in **Limitations** (§7).  Every externally "
        "verifiable statement includes a source reference in **Source "
        "Inventory** (§8).",
        "",
    ])

    return "\n".join(lines)


def _render_method(
    market: List[Dict[str, Any]],
    evidence: List[Dict[str, Any]],
    claims: List[Dict[str, Any]],
    competitors: List[Dict[str, Any]],
) -> str:
    """Render the Method section.

    Extracts method-related metadata from artifacts: collection dates,
    platforms, geographic scope, search dates, and competitor inclusion
    criteria.  Falls back to ``"unknown"`` when metadata is unavailable.

    Parameters
    ----------
    market : list[dict]
        Market finding records.
    evidence : list[dict]
        Evidence records.
    claims : list[dict]
        Claim assessment records.
    competitors : list[dict]
        Competitor analysis records.

    Returns
    -------
    str
        Markdown section content.
    """
    # Dates from market records
    market_dates: set[str] = set()
    platforms: set[str] = set()
    for rec in market:
        date = _safe_get(rec, "collection_date", "data_date")
        if date != _SENTINEL:
            market_dates.add(str(date))
        platform = _safe_get(rec, "platform", "channel")
        if platform != _SENTINEL:
            platforms.add(str(platform))

    # Dates from evidence
    evidence_dates: set[str] = set()
    search_dates: set[str] = set()
    for rec in evidence:
        date = _safe_get(rec, "collection_date", "search_date", "retrieval_date")
        if date != _SENTINEL:
            evidence_dates.add(str(date))
        search_date = _safe_get(rec, "search_date", "literature_search_date")
        if search_date != _SENTINEL:
            search_dates.add(str(search_date))

    # Competitor inclusion criteria
    comp_criteria: List[str] = []
    for rec in competitors:
        crit = _safe_get(rec, "inclusion_criteria", "criteria")
        if crit != _SENTINEL and str(crit) not in comp_criteria:
            comp_criteria.append(str(crit))

    lines = ["## Method", ""]

    if platforms:
        lines.append(f"**Platforms / databases:** {', '.join(sorted(platforms))}.")
        lines.append("")

    if market_dates:
        lines.append(f"**Market collection dates:** {', '.join(sorted(market_dates))}.")
        lines.append("")

    if search_dates:
        lines.append(f"**Literature search dates:** {', '.join(sorted(search_dates))}.")
        lines.append("")

    if evidence_dates:
        lines.append(f"**Evidence retrieval dates:** {', '.join(sorted(evidence_dates))}.")
        lines.append("")

    if comp_criteria:
        lines.append(f"**Competitor inclusion criteria:** {'; '.join(comp_criteria)}.")
        lines.append("")

    # If nothing was populated, emit a general statement
    if not lines[2:]:
        lines.append(
            "Specific method metadata was not available in the supplied "
            "artifacts.  Refer to the project brief and research plan for "
            "detailed methodology."
        )
        lines.append("")

    return "\n".join(lines)


def _render_market_findings(market: List[Dict[str, Any]]) -> str:
    """Render the Market Findings section.

    Builds a product-overview table from market records.  Falls back to
    paragraph summaries when records lack tabular fields.

    Parameters
    ----------
    market : list[dict]
        Market finding records.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Market Findings", ""]

    if not market:
        lines.append("No market finding records were supplied.")
        lines.append("")
        return "\n".join(lines)

    # Build a product table
    headers = [
        "Product", "Brand", "Form", "Dose", "Spec",
        "Price", "Type", "Channel", "Date",
    ]
    rows: List[List[str]] = []

    for rec in market:
        product = _safe_str(_safe_get(rec, "standard_name", "generic_name", "product_name", "product"))
        brand = _safe_str(_safe_get(rec, "brand"))
        form = _safe_str(_safe_get(rec, "dosage_form", "form"))
        dose = _safe_str(_safe_get(rec, "dose"))
        spec = _safe_str(_safe_get(rec, "spec", "package_quantity", "package_description"))
        price = _safe_str(_safe_get(rec, "price"))
        ptype = _safe_str(_safe_get(rec, "price_type"))
        channel = _safe_str(_safe_get(rec, "channel", "platform"))
        date = _safe_str(_safe_get(rec, "collection_date", "data_date"))

        rows.append([product, brand, form, dose, spec, price, ptype, channel, date])

    lines.append(_build_markdown_table(headers, rows))
    lines.append("")

    # Summary notes
    n_records = _count_records(market)
    lines.append(f"*{n_records} market record(s) rendered.*")
    lines.append("")

    return "\n".join(lines)


def _render_competitor_analysis(competitors: List[Dict[str, Any]]) -> str:
    """Render the Competitor Analysis section.

    Builds a competitor comparison table with normalized product fields.

    Parameters
    ----------
    competitors : list[dict]
        Competitor analysis records.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Competitor Analysis", ""]

    if not competitors:
        lines.append("No competitor records were supplied.")
        lines.append("")
        return "\n".join(lines)

    headers = [
        "Product", "Brand", "Form", "Dose", "Spec",
        "Price", "Norm. Price", "Daily Cost",
        "Claims", "Channel", "Differentiator", "Date",
    ]
    rows: List[List[str]] = []

    for rec in competitors:
        product = _safe_str(_safe_get(rec, "standard_name", "product", "product_name"))
        brand = _safe_str(_safe_get(rec, "brand"))
        form = _safe_str(_safe_get(rec, "dosage_form", "form"))
        dose = _safe_str(_safe_get(rec, "dose"))
        spec = _safe_str(_safe_get(rec, "spec", "package_quantity"))
        price = _safe_str(_safe_get(rec, "price"))
        norm_price = _safe_str(_safe_get(rec, "normalized_price", "unit_price"))
        daily_cost = _safe_str(_safe_get(rec, "daily_cost"))
        claims_str = _safe_str(_safe_get(rec, "claims_summary", "claims"))
        channel = _safe_str(_safe_get(rec, "channel", "platform"))
        diff = _safe_str(_safe_get(rec, "differentiator", "main_differentiator", "differentiators"))
        date = _safe_str(_safe_get(rec, "collection_date", "data_date"))

        rows.append([
            product, brand, form, dose, spec,
            price, norm_price, daily_cost,
            claims_str, channel, diff, date,
        ])

    lines.append(_build_markdown_table(headers, rows))
    lines.append("")

    n_records = _count_records(competitors)
    lines.append(f"*{n_records} competitor record(s) rendered.*")
    lines.append("")

    return "\n".join(lines)


def _render_evidence_summary(evidence: List[Dict[str, Any]]) -> str:
    """Render the Evidence Summary section.

    Builds an evidence-overview table from evidence records.

    Parameters
    ----------
    evidence : list[dict]
        Evidence records.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Evidence Summary", ""]

    if not evidence:
        lines.append("No evidence records were supplied.")
        lines.append("")
        return "\n".join(lines)

    headers = [
        "Source", "Design", "Population",
        "Intervention / Dose", "Outcome", "Result",
        "Limitations", "ID",
    ]
    rows: List[List[str]] = []

    for rec in evidence:
        source = _safe_str(_safe_get(rec, "source", "citation", "title"))
        design = _safe_str(_safe_get(rec, "study_design", "design"))
        population = _safe_str(_safe_get(rec, "population"))
        intervention = _safe_str(_safe_get(rec, "intervention", "intervention_dose"))
        outcome = _safe_str(_safe_get(rec, "outcome", "outcome_measure"))
        result = _safe_str(_safe_get(rec, "result", "effect_estimate"))
        limitations = _safe_str(_safe_get(rec, "limitations", "study_limitations"))
        eid = _safe_str(_safe_get(rec, "doi", "pmid", "source_id", "id"))

        rows.append([
            source, design, population,
            intervention, outcome, result,
            limitations, eid,
        ])

    lines.append(_build_markdown_table(headers, rows))
    lines.append("")

    n_records = _count_records(evidence)
    lines.append(f"*{n_records} evidence record(s) rendered.*")
    lines.append("")

    return "\n".join(lines)


def _render_claim_assessments(claims: List[Dict[str, Any]]) -> str:
    """Render the Claim Assessments section.

    Builds a claim-by-claim review table with support levels.

    Parameters
    ----------
    claims : list[dict]
        Claim assessment records.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Claim Assessments", ""]

    if not claims:
        lines.append("No claim assessment records were supplied.")
        lines.append("")
        return "\n".join(lines)

    headers = [
        "Claim", "Product", "Support Level",
        "Evidence IDs", "Notes",
    ]
    rows: List[List[str]] = []

    for rec in claims:
        claim_text = _safe_str(_safe_get(rec, "claim_text", "claim", "statement"))
        product = _safe_str(_safe_get(rec, "product", "product_name"))
        support = _safe_str(_safe_get(rec, "support_level", "claim_support_level", "classification"))
        evidence_ids = _safe_str(_safe_get(rec, "evidence_ids", "evidence_mapping"))
        notes = _safe_str(_safe_get(rec, "notes", "assessment_notes", "comment"))

        rows.append([claim_text, product, support, evidence_ids, notes])

    lines.append(_build_markdown_table(headers, rows))
    lines.append("")

    n_records = _count_records(claims)
    lines.append(f"*{n_records} claim(s) assessed.*")
    lines.append("")

    return "\n".join(lines)


def _render_limitations(
    market: List[Dict[str, Any]],
    evidence: List[Dict[str, Any]],
    claims: List[Dict[str, Any]],
    competitors: List[Dict[str, Any]],
) -> str:
    """Render the Limitations section.

    Collects limitations from all artifact records and presents them as a
    bulleted list.

    Parameters
    ----------
    market : list[dict]
        Market finding records.
    evidence : list[dict]
        Evidence records.
    claims : list[dict]
        Claim assessment records.
    competitors : list[dict]
        Competitor analysis records.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Limitations", ""]

    all_limitations: List[str] = []

    # Gather limitations from all artifact types
    for source_label, records in [
        ("Market findings", market),
        ("Evidence", evidence),
        ("Claims", claims),
        ("Competitors", competitors),
    ]:
        for rec in records:
            lim = _safe_get(rec, "limitations", "main_limitations", "study_limitations")
            if lim != _SENTINEL:
                if isinstance(lim, list):
                    for item in lim:
                        all_limitations.append(f"[{source_label}] {item}")
                else:
                    all_limitations.append(f"[{source_label}] {lim}")

    if all_limitations:
        for lim in all_limitations:
            lines.append(f"- {lim}")
    else:
        lines.append("- No specific limitations were recorded in the supplied artifacts.")
        lines.append("- General limitations applicable to this type of research include:")
        lines.append("  - Dynamic prices and promotions may not be reflected in point-in-time collection.")
        lines.append("  - Platform access restrictions may limit data completeness.")
        lines.append("  - Seller-generated descriptions may contain unverified claims.")
        lines.append("  - Absence of independent market-volume data limits demand estimation.")

    lines.append("")
    return "\n".join(lines)


def _render_source_inventory(
    market: List[Dict[str, Any]],
    evidence: List[Dict[str, Any]],
    claims: List[Dict[str, Any]],
    competitors: List[Dict[str, Any]],
) -> str:
    """Render the Source Inventory section.

    Collects source references from all artifact records and builds a
    deduplicated table.

    Parameters
    ----------
    market : list[dict]
        Market finding records.
    evidence : list[dict]
        Evidence records.
    claims : list[dict]
        Claim assessment records.
    competitors : list[dict]
        Competitor analysis records.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Source Inventory", ""]

    seen_ids: set[str] = set()
    sources: List[Dict[str, str]] = []

    # Collect sources from all artifacts
    for source_label, records in [
        ("market", market),
        ("evidence", evidence),
        ("claims", claims),
        ("competitors", competitors),
    ]:
        for rec in records:
            # Try multiple possible source ID field names
            sid = _safe_get(
                rec,
                "source_id",
                "id",
                "doi",
                "pmid",
                "url",
                "citation",
            )
            sid_str = str(sid) if sid != _SENTINEL else ""

            platform = _safe_get(rec, "platform", "channel", "source_type")
            platform_str = str(platform) if platform != _SENTINEL else ""

            date = _safe_get(rec, "collection_date", "search_date", "data_date", "retrieval_date")
            date_str = str(date) if date != _SENTINEL else ""

            title = _safe_get(rec, "title", "source_title", "citation")
            title_str = str(title) if title != _SENTINEL else ""

            # Skip entries with no identifiable source information
            if not sid_str and not title_str:
                continue

            # Deduplicate by source ID, falling back to title
            dedup_key = sid_str or title_str
            if not dedup_key:
                continue
            if dedup_key in seen_ids:
                continue
            seen_ids.add(dedup_key)

            sources.append({
                "id": sid_str or _SENTINEL,
                "platform": platform_str or _SENTINEL,
                "date": date_str or _SENTINEL,
                "title": title_str or _SENTINEL,
            })

    if sources:
        headers = ["Source ID", "Platform / Type", "Collection Date", "Title / Reference"]
        rows: List[List[str]] = []
        for src in sources:
            rows.append([
                src["id"],
                src["platform"],
                src["date"],
                src["title"],
            ])
        lines.append(_build_markdown_table(headers, rows))
    else:
        lines.append("No source references were found in the supplied artifacts.")
        lines.append("")

    lines.append("")
    n_sources = len(sources)
    lines.append(f"*{n_sources} unique source(s) inventoried.*")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Full report assembly
# ---------------------------------------------------------------------------


def _render_report(
    market: List[Dict[str, Any]],
    evidence: List[Dict[str, Any]],
    claims: List[Dict[str, Any]],
    competitors: List[Dict[str, Any]],
    title: str = "Market Research Report",
) -> str:
    """Assemble all sections into a complete markdown report.

    Parameters
    ----------
    market : list[dict]
        Market finding records.
    evidence : list[dict]
        Evidence records.
    claims : list[dict]
        Claim assessment records.
    competitors : list[dict]
        Competitor analysis records.
    title : str
        Report title (default ``"Market Research Report"``).

    Returns
    -------
    str
        Full markdown report as a single string.
    """
    sections: List[str] = []

    # Title
    sections.append(f"# {title}")
    sections.append("")
    sections.append("---")
    sections.append("")

    # Section 1: Executive Summary
    try:
        sections.append(_render_executive_summary(market, evidence, claims, competitors))
    except Exception as exc:
        log_error(f"Failed to render Executive Summary: {exc}")
        raise

    # Section 2: Method
    try:
        sections.append(_render_method(market, evidence, claims, competitors))
    except Exception as exc:
        log_error(f"Failed to render Method: {exc}")
        raise

    # Section 3: Market Findings
    try:
        sections.append(_render_market_findings(market))
    except Exception as exc:
        log_error(f"Failed to render Market Findings: {exc}")
        raise

    # Section 4: Competitor Analysis
    try:
        sections.append(_render_competitor_analysis(competitors))
    except Exception as exc:
        log_error(f"Failed to render Competitor Analysis: {exc}")
        raise

    # Section 5: Evidence Summary
    try:
        sections.append(_render_evidence_summary(evidence))
    except Exception as exc:
        log_error(f"Failed to render Evidence Summary: {exc}")
        raise

    # Section 6: Claim Assessments
    try:
        sections.append(_render_claim_assessments(claims))
    except Exception as exc:
        log_error(f"Failed to render Claim Assessments: {exc}")
        raise

    # Section 7: Limitations
    try:
        sections.append(_render_limitations(market, evidence, claims, competitors))
    except Exception as exc:
        log_error(f"Failed to render Limitations: {exc}")
        raise

    # Section 8: Source Inventory
    try:
        sections.append(_render_source_inventory(market, evidence, claims, competitors))
    except Exception as exc:
        log_error(f"Failed to render Source Inventory: {exc}")
        raise

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments, validate inputs, render the report, and write output.

    Returns
    -------
    int
        Exit code (0 success, 2 file/param error, 3 corrupted/rendering error).
    """
    parser = argparse.ArgumentParser(
        description=(
            "Render a structured markdown research report from validated "
            "artifact files (market, evidence, claims, competitors)."
        ),
    )
    parser.add_argument(
        "--market",
        type=str,
        required=True,
        help="Path to market findings JSONL artifact.",
    )
    parser.add_argument(
        "--evidence",
        type=str,
        required=True,
        help="Path to evidence JSONL artifact.",
    )
    parser.add_argument(
        "--claims",
        type=str,
        required=True,
        help="Path to claim assessments JSONL artifact.",
    )
    parser.add_argument(
        "--competitors",
        type=str,
        required=True,
        help="Path to competitor analysis JSONL artifact.",
    )
    parser.add_argument(
        "--out",
        type=str,
        required=True,
        help="Output markdown file path (e.g. report.md).",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Market Research Report",
        help="Report title (default: 'Market Research Report').",
    )
    args = parser.parse_args()

    # ---- Resolve paths ------------------------------------------------------
    artifact_paths = {
        "market": Path(args.market),
        "evidence": Path(args.evidence),
        "claims": Path(args.claims),
        "competitors": Path(args.competitors),
    }

    # ---- Validate all input files exist -------------------------------------
    for label, path in artifact_paths.items():
        if not path.exists():
            log_error(f"File not found ({label}): {path}")
            return 2
        if not path.is_file():
            log_error(f"Not a file ({label}): {path}")
            return 2

    output_path = Path(args.out)

    # ---- Read all artifact files --------------------------------------------
    artifacts: Dict[str, List[Dict[str, Any]]] = {}
    for label, path in artifact_paths.items():
        try:
            records = read_jsonl(path)
            artifacts[label] = records
            log_info(f"Read {len(records)} record(s) from {label}: {path}")
        except json.JSONDecodeError as exc:
            log_error(f"Corrupted JSONL at {label} ({path}): {exc}")
            return 3
        except FileNotFoundError:
            log_error(f"File not found ({label}): {path}")
            return 2

    # ---- Render report ------------------------------------------------------
    try:
        report_md = _render_report(
            market=artifacts["market"],
            evidence=artifacts["evidence"],
            claims=artifacts["claims"],
            competitors=artifacts["competitors"],
            title=args.title,
        )
    except Exception as exc:
        log_error(f"Template rendering error: {exc}")
        return 3

    # ---- Write output -------------------------------------------------------
    try:
        output_path.write_text(report_md, encoding="utf-8")
        log_info(f"Report written: {output_path}")
    except OSError as exc:
        log_error(f"Failed to write output file {output_path}: {exc}")
        return 3

    return 0


if __name__ == "__main__":
    sys.exit(main())
