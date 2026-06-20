#!/usr/bin/env python3
"""Project-level report renderer that assembles cross-skill research artifacts
into a structured markdown report.

Reads the required project brief alongside optional market, evidence,
competitor, claim, and audit artifact files and produces a single,
well-structured markdown report suitable for stakeholder review.  Sections
that depend on missing artifacts are rendered as placeholder stubs with a
data-availability note.

Usage
-----
    python scripts/render-report.py \\
        --brief brief.md \\
        --plan plan.json \\
        --market market.jsonl \\
        --evidence evidence.jsonl \\
        --competitors competitors.jsonl \\
        --claims claims.jsonl \\
        --audit audit.jsonl \\
        --out report.md

    # Minimal invocation (only brief and plan required):
    python scripts/render-report.py \\
        --brief brief.md --plan plan.json --out report.md

Input
-----
- **--brief** (required): Markdown research brief.
- **--plan** (required): JSON research plan (task-planner output).
- **--market**: JSONL market research records.
- **--evidence**: JSONL academic evidence records.
- **--competitors**: JSONL competitor analysis records.
- **--claims**: JSONL claim verification records.
- **--audit**: JSONL audit finding records.

Output
------
A single markdown file with 13 numbered sections plus appendices.  The report
is a synthesis document; it structures available data, computes summary
statistics, and flags gaps but does *not* generate original strategic
conclusions — those belong to the analyst reviewing the report.

Exit codes
----------
0   Report generated successfully.
2   Missing required arguments or required file not found.
3   Corrupted input or template error.

All input files are read-only.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Project root on sys.path for ``scripts._common`` import.
# ---------------------------------------------------------------------------
_T = Path(__file__).resolve().parent.parent
if str(_T) not in sys.path:
    sys.path.insert(0, str(_T))

from scripts._common import read_jsonl, log_info, log_error


# ---------------------------------------------------------------------------
# Input loading helpers
# ---------------------------------------------------------------------------


def _load_json(path: Path) -> Dict[str, Any]:
    """Load a JSON file, exiting with code 2 or 3 on failure.

    Parameters
    ----------
    path : Path
        Path to the ``.json`` file.

    Returns
    -------
    dict
        Parsed JSON object.
    """
    if not path.exists():
        log_error(f"Required file not found: {path}")
        sys.exit(2)
    try:
        with open(str(path), "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSON at {path}: {exc}")
        sys.exit(3)


def _load_text(path: Path) -> str:
    """Load a text/markdown file, exiting with code 2 on failure.

    Parameters
    ----------
    path : Path
        Path to the text file.

    Returns
    -------
    str
        File contents as a string.
    """
    if not path.exists():
        log_error(f"Required file not found: {path}")
        sys.exit(2)
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        log_error(f"Failed to read {path}: {exc}")
        sys.exit(2)


def _load_optional_jsonl(path: Optional[str]) -> Optional[List[Dict[str, Any]]]:
    """Load an optional JSONL file, returning ``None`` when absent.

    Parameters
    ----------
    path : str or None
        Optional path to a ``.jsonl`` file.

    Returns
    -------
    list[dict] or None
        Records when the file exists; ``None`` when *path* is ``None``.
    """
    if path is None:
        return None
    p = Path(path)
    if not p.exists():
        log_info(f"Optional file not found — skipping: {p}")
        return None
    try:
        return read_jsonl(p)
    except json.JSONDecodeError as exc:
        log_error(f"Corrupted JSONL at {p}: {exc}")
        sys.exit(3)


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------

# Template for sections that depend on missing data.
_DATA_UNAVAILABLE = (
    "_Data for this section was not available at report generation time._\n"
    "_Re-run with the appropriate artifact file to populate this section._\n\n"
)


def _render_title_metadata(brief_text: str, plan: Dict[str, Any]) -> str:
    """Render section 1: Title and Metadata.

    Parameters
    ----------
    brief_text : str
        Raw markdown of the research brief.
    plan : dict
        Parsed research plan JSON.

    Returns
    -------
    str
        Markdown section content.
    """
    title = plan.get("title") or plan.get("project_name") or "Market Research Report"
    created = plan.get("created") or plan.get("created_date", "")
    version = plan.get("plan_version", plan.get("version", "1.0"))
    project_id = plan.get("project_id", "")

    # Extract first heading or first non-empty line from brief as subtitle
    brief_lines = brief_text.strip().split("\n")
    subtitle = ""
    for line in brief_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            subtitle = stripped
            break
        elif stripped.startswith("#"):
            subtitle = stripped.lstrip("#").strip()
            break

    lines: List[str] = []
    lines.append(f"# {title}\n")
    if subtitle:
        lines.append(f"> {subtitle}\n")
    lines.append("## Metadata\n")
    lines.append(f"- **Report generated**: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"- **Project ID**: {project_id}")
    lines.append(f"- **Plan version**: {version}")
    lines.append(f"- **Plan date**: {created}")
    lines.append("- **Renderer**: `scripts/render-report.py` v1.0\n")
    return "\n".join(lines)


def _render_executive_summary(
    plan: Dict[str, Any],
    market: Optional[List[Dict[str, Any]]],
    audit: Optional[List[Dict[str, Any]]],
) -> str:
    """Render section 2: Executive Summary.

    Parameters
    ----------
    plan : dict
        Research plan.
    market : list[dict] or None
        Market research records.
    audit : list[dict] or None
        Audit findings.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Executive Summary\n"]
    objectives = plan.get("research_objectives", plan.get("objectives", []))
    if isinstance(objectives, list) and objectives:
        lines.append("### Research Objectives\n")
        for obj in objectives:
            if isinstance(obj, dict):
                lines.append(f"- **{obj.get('id', '')}**: {obj.get('description', obj.get('title', ''))}")
            else:
                lines.append(f"- {obj}")
        lines.append("")

    # Key metrics from market data
    if market:
        lines.append("### Key Findings at a Glance\n")
        products = set()
        brands = set()
        sources = set()
        for rec in market:
            name = rec.get("standard_name") or rec.get("generic_name", "")
            if name:
                products.add(name)
            brand = rec.get("brand", "")
            if brand:
                brands.add(brand)
            for sid in rec.get("source_ids", rec.get("source_id", [])):
                if isinstance(sid, str):
                    sources.add(sid)
        lines.append(f"- **Products identified**: {len(products)}")
        lines.append(f"- **Brands covered**: {len(brands)}")
        lines.append(f"- **Data sources**: {len(sources)}")
        lines.append(f"- **Market records**: {len(market)}\n")

    # Audit status
    if audit:
        lines.append("### Audit Status\n")
        passed = sum(1 for f in audit if f.get("pass_fail_decision") == "pass")
        with_minor = sum(
            1 for f in audit if f.get("pass_fail_decision") == "pass_with_minor_revisions"
        )
        failed = sum(
            1 for f in audit if f.get("pass_fail_decision") == "fail_requires_major_revisions"
        )
        lines.append(f"- **Pass**: {passed}")
        lines.append(f"- **Pass with minor revisions**: {with_minor}")
        lines.append(f"- **Fail / requires major revisions**: {failed}")
        if failed > 0:
            lines.append("\n> ⚠ **Attention**: This report has unresolved critical audit findings.\n")
        lines.append("")
    else:
        lines.append("_No audit data available. Report has not been independently audited._\n")

    return "\n".join(lines)


def _render_research_questions(plan: Dict[str, Any]) -> str:
    """Render section 3: Research Questions.

    Parameters
    ----------
    plan : dict
        Research plan.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Research Questions\n"]
    questions = plan.get("research_questions", plan.get("questions", []))
    if not questions:
        lines.append("_No explicit research questions defined in the plan._\n")
        return "\n".join(lines)

    for i, q in enumerate(questions, 1):
        if isinstance(q, dict):
            text = q.get("question") or q.get("text", "")
            rationale = q.get("rationale", "")
            lines.append(f"### RQ{i}: {text}")
            if rationale:
                lines.append(f"_Rationale:_ {rationale}")
        else:
            lines.append(f"### RQ{i}: {q}")
        lines.append("")
    return "\n".join(lines)


def _render_method(plan: Dict[str, Any]) -> str:
    """Render section 4: Method.

    Parameters
    ----------
    plan : dict
        Research plan.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Method\n"]

    # Research approach
    scope = plan.get("scope") or plan.get("research_scope", {})
    if isinstance(scope, dict):
        lines.append("### Scope\n")
        for k, v in scope.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")

    # Data sources
    data_sources = plan.get("data_sources", plan.get("sources", []))
    if data_sources:
        lines.append("### Data Sources\n")
        for src in data_sources:
            if isinstance(src, dict):
                lines.append(
                    f"- **{src.get('type', src.get('name', ''))}**: "
                    f"{src.get('description', '')}"
                )
            else:
                lines.append(f"- {src}")
        lines.append("")

    # Platforms / tasks
    platform_tasks = plan.get("platform_tasks", plan.get("tasks", []))
    if platform_tasks:
        lines.append("### Research Activities\n")
        for task in platform_tasks:
            if isinstance(task, dict):
                lines.append(
                    f"- **{task.get('task_id', '')}** ({task.get('task_type', '')}): "
                    f"{task.get('description', task.get('title', ''))} "
                    f"[priority: {task.get('priority', 'medium')}]"
                )
            else:
                lines.append(f"- {task}")
        lines.append("")

    # Evidence standards
    evidence_standards = plan.get("evidence_standards", plan.get("methodology_notes", ""))
    if evidence_standards:
        lines.append("### Evidence Standards\n")
        if isinstance(evidence_standards, str):
            lines.append(evidence_standards)
        elif isinstance(evidence_standards, list):
            for std in evidence_standards:
                lines.append(f"- {std}")
        lines.append("")

    return "\n".join(lines)


def _render_market_landscape(
    market: Optional[List[Dict[str, Any]]],
) -> str:
    """Render section 5: Market Landscape.

    Parameters
    ----------
    market : list[dict] or None
        Market research records.

    Returns
    -------
    str
        Markdown section content.
    """
    if market is None:
        return "## Market Landscape\n\n" + _DATA_UNAVAILABLE

    lines = ["## Market Landscape\n"]

    # Product overview table
    lines.append("### Product Overview\n")
    lines.append(
        "| Product | Brand | Dosage Form | Dose | Package | Data Source(s) |"
    )
    lines.append("|---------|-------|-------------|------|---------|---------------|")
    for rec in market:
        product = rec.get("standard_name") or rec.get("generic_name", "unknown")
        brand = rec.get("brand", "unknown")
        form = rec.get("dosage_form", "")
        ingredients = rec.get("active_ingredients", [])
        dose = ""
        if ingredients and isinstance(ingredients, list) and len(ingredients) > 0:
            d = ingredients[0].get("per_unit_dose", "")
            u = ingredients[0].get("per_unit_dose_unit", "")
            if d:
                dose = f"{d} {u}".strip()
        pkg = rec.get("package_quantity", rec.get("package_description", ""))
        sources = rec.get("source_ids", rec.get("source_id", []))
        if isinstance(sources, list):
            src_str = ", ".join(str(s) for s in sources[:3])
            if len(sources) > 3:
                src_str += f", ... ({len(sources)} total)"
        else:
            src_str = str(sources)
        lines.append(
            f"| {product} | {brand} | {form} | {dose} | {pkg} | {src_str} |"
        )
    lines.append("")

    # Price summary
    prices_found = False
    for rec in market:
        obs_list = rec.get("price_observations", [])
        if obs_list:
            prices_found = True
            break

    if prices_found:
        lines.append("### Price Summary\n")
        lines.append(
            "| Product | Price | Currency | Price Type | Unit Price | Daily Cost | Source |"
        )
        lines.append(
            "|---------|-------|----------|------------|------------|------------|--------|"
        )
        for rec in market:
            product = rec.get("standard_name") or rec.get("generic_name", "unknown")
            obs_list = rec.get("price_observations", [])
            for obs in obs_list if isinstance(obs_list, list) else []:
                price = obs.get("price", "")
                currency = obs.get("currency", "")
                price_type = obs.get("price_type", "")
                unit_price = obs.get("unit_price", "")
                daily_cost = obs.get("daily_cost", "")
                source = obs.get("source_platform", obs.get("source_id", ""))
                lines.append(
                    f"| {product} | {price} | {currency} | {price_type} | "
                    f"{unit_price} | {daily_cost} | {source} |"
                )
        lines.append("")

    # Channel distribution
    channels: Dict[str, int] = {}
    for rec in market:
        for ch in rec.get("channels", rec.get("source_ids", [])):
            if isinstance(ch, str):
                channels[ch] = channels.get(ch, 0) + 1
    if channels:
        lines.append("### Channel Distribution\n")
        for ch, count in sorted(channels.items(), key=lambda x: -x[1]):
            lines.append(f"- **{ch}**: {count} record(s)")
        lines.append("")

    return "\n".join(lines)


def _render_competitor_analysis(
    competitors: Optional[List[Dict[str, Any]]],
) -> str:
    """Render section 6: Competitor Analysis.

    Parameters
    ----------
    competitors : list[dict] or None
        Competitor analysis records.

    Returns
    -------
    str
        Markdown section content.
    """
    if competitors is None:
        return "## Competitor Analysis\n\n" + _DATA_UNAVAILABLE

    lines = ["## Competitor Analysis\n"]

    lines.append("### Competitor Comparison\n")
    lines.append(
        "| Product | Brand | Manufacturer | Dosage Form | Dose | "
        "Package | Price | Claims | Channel(s) |"
    )
    lines.append(
        "|---------|-------|--------------|-------------|------|"
        "---------|-------|--------|------------|"
    )
    for rec in competitors:
        product = rec.get("standard_name") or rec.get("generic_name") or rec.get("product", "")
        brand = rec.get("brand", "")
        manufacturer = rec.get("manufacturer", "")
        form = rec.get("dosage_form", "")
        ingredients = rec.get("active_ingredients", [])
        dose = ""
        if ingredients and isinstance(ingredients, list) and len(ingredients) > 0:
            d = ingredients[0].get("per_unit_dose", "")
            u = ingredients[0].get("per_unit_dose_unit", "")
            if d:
                dose = f"{d} {u}".strip()
        pkg = rec.get("package_quantity", rec.get("package_description", ""))
        price = rec.get("price", rec.get("normalized_price", ""))
        claims_summary = rec.get("claims_summary", "")
        if isinstance(claims_summary, str) and len(claims_summary) > 60:
            claims_summary = claims_summary[:57] + "..."
        channels = rec.get("channels", rec.get("source_ids", []))
        if isinstance(channels, list):
            ch_str = ", ".join(str(c) for c in channels[:2])
        else:
            ch_str = str(channels) if channels else ""
        lines.append(
            f"| {product} | {brand} | {manufacturer} | {form} | {dose} | "
            f"{pkg} | {price} | {claims_summary} | {ch_str} |"
        )
    lines.append("")

    # Count
    lines.append(f"_Total competitor entries: {len(competitors)}_\n")

    return "\n".join(lines)


def _render_evidence_review(
    evidence: Optional[List[Dict[str, Any]]],
) -> str:
    """Render section 7: Evidence Review.

    Parameters
    ----------
    evidence : list[dict] or None
        Academic evidence records.

    Returns
    -------
    str
        Markdown section content.
    """
    if evidence is None:
        return "## Evidence Review\n\n" + _DATA_UNAVAILABLE

    lines = ["## Evidence Review\n"]

    # Summary statistics
    study_types: Dict[str, int] = {}
    evidence_levels: Dict[str, int] = {}
    for rec in evidence:
        st = rec.get("study_design", rec.get("study_type", "unknown"))
        study_types[st] = study_types.get(st, 0) + 1
        el = rec.get("evidence_level", rec.get("level", "unknown"))
        evidence_levels[el] = evidence_levels.get(el, 0) + 1

    lines.append("### Evidence Summary\n")
    lines.append(f"- **Total evidence records**: {len(evidence)}")
    lines.append(f"- **Study designs**: {', '.join(f'{k} ({v})' for k, v in study_types.items())}")
    lines.append(f"- **Evidence levels**: {', '.join(f'{k} ({v})' for k, v in evidence_levels.items())}")
    lines.append("")

    # Evidence table
    lines.append("### Evidence Records\n")
    lines.append(
        "| Title / ID | Study Design | Evidence Level | Risk of Bias | "
        "Key Finding | PMID / DOI |"
    )
    lines.append(
        "|------------|-------------|---------------|--------------|"
        "-------------|------------|"
    )
    for rec in evidence:
        title = rec.get("title") or rec.get("citation", {}).get("title", "")
        if isinstance(title, str) and len(title) > 70:
            title = title[:67] + "..."
        design = rec.get("study_design", rec.get("study_type", ""))
        level = rec.get("evidence_level", rec.get("level", ""))
        bias = rec.get("risk_of_bias", rec.get("bias_assessment", ""))
        finding = rec.get("key_finding", rec.get("main_finding", rec.get("abstract", "")))
        if isinstance(finding, str) and len(finding) > 80:
            finding = finding[:77] + "..."
        pmid = rec.get("pmid") or rec.get("citation", {}).get("pmid", "")
        doi = rec.get("doi") or rec.get("citation", {}).get("doi", "")
        id_str = f"PMID:{pmid}" if pmid else f"DOI:{doi}" if doi else ""
        lines.append(
            f"| {title} | {design} | {level} | {bias} | {finding} | {id_str} |"
        )
    lines.append("")

    return "\n".join(lines)


def _render_claim_verification(
    claims: Optional[List[Dict[str, Any]]],
) -> str:
    """Render section 8: Claim Verification.

    Parameters
    ----------
    claims : list[dict] or None
        Claim verification records.

    Returns
    -------
    str
        Markdown section content.
    """
    if claims is None:
        return "## Claim Verification\n\n" + _DATA_UNAVAILABLE

    lines = ["## Claim Verification\n"]

    # Summary
    support_counts: Dict[str, int] = {}
    for rec in claims:
        sl = rec.get("support_level", rec.get("overall_support", "cannot-determine"))
        support_counts[sl] = support_counts.get(sl, 0) + 1

    lines.append("### Verification Summary\n")
    for level, count in sorted(support_counts.items()):
        lines.append(f"- **{level}**: {count} claim(s)")
    lines.append(f"- **Total claims reviewed**: {len(claims)}")
    lines.append("")

    # Claim-by-claim table
    lines.append("### Claim Details\n")
    lines.append(
        "| Claim | Product | Support Level | Verdict | Evidence Mapped |"
    )
    lines.append(
        "|-------|---------|---------------|---------|----------------|"
    )
    for rec in claims:
        claim_text = rec.get("claim_text", rec.get("claim", rec.get("id", "")))
        if isinstance(claim_text, str) and len(claim_text) > 60:
            claim_text = claim_text[:57] + "..."
        product = rec.get("product_name", rec.get("product", ""))
        support = rec.get("support_level", rec.get("overall_support", ""))
        verdict = rec.get("verdict", rec.get("review_verdict", ""))
        evidence_count = len(
            rec.get("evidence_mapping", rec.get("evidence_ids", []))
        )
        lines.append(
            f"| {claim_text} | {product} | {support} | {verdict} | {evidence_count} |"
        )
    lines.append("")

    return "\n".join(lines)


def _render_regulatory_context(
    market: Optional[List[Dict[str, Any]]],
    evidence: Optional[List[Dict[str, Any]]],
) -> str:
    """Render section 9: Regulatory Context.

    Parameters
    ----------
    market : list[dict] or None
        Market research records.
    evidence : list[dict] or None
        Academic evidence records.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Regulatory Context\n"]

    regulatory = []
    if market:
        for rec in market:
            for field in ["regulatory_status", "nmpa_approval_number", "nda_number", "otc_rx"]:
                val = rec.get(field, "")
                if val and val not in ("", "unknown", "not_applicable"):
                    regulatory.append(
                        f"- **{field}** ({rec.get('standard_name', rec.get('generic_name', ''))}): {val}"
                    )
    if evidence:
        for rec in evidence:
            reg_info = rec.get("regulatory_context", rec.get("regulatory", {}))
            if isinstance(reg_info, dict):
                for k, v in reg_info.items():
                    if v and v not in ("", "unknown"):
                        regulatory.append(f"- **{k}**: {v}")

    if regulatory:
        for item in regulatory:
            lines.append(item)
    else:
        lines.append("_No regulatory data available in the provided artifacts._")
    lines.append("")

    return "\n".join(lines)


def _render_limitations(
    audit: Optional[List[Dict[str, Any]]],
) -> str:
    """Render section 10: Limitations.

    Parameters
    ----------
    audit : list[dict] or None
        Audit findings.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Limitations\n"]

    if audit:
        lines.append("### Audit Findings\n")
        critical = []
        major = []
        for finding in audit:
            findings_list = finding.get("findings", [])
            for f in findings_list if isinstance(findings_list, list) else []:
                severity = f.get("severity", f.get("finding_severity", "info"))
                desc = f.get("description", f.get("finding", ""))
                if severity in ("critical",):
                    critical.append(f"- **[CRITICAL]** {desc}")
                elif severity in ("major",):
                    major.append(f"- **[MAJOR]** {desc}")

        if critical:
            lines.append("#### Critical\n")
            lines.extend(critical)
            lines.append("")
        if major:
            lines.append("#### Major\n")
            lines.extend(major)
            lines.append("")
        if not critical and not major:
            lines.append("_No critical or major findings reported._\n")

    lines.append(
        "### General Limitations\n"
        "- This report is based on data collected from publicly available sources.\n"
        "- Prices may vary by region, seller, and collection date.\n"
        "- Claim verification is limited to the evidence records reviewed.\n"
        "- The absence of a finding does not imply the absence of an issue.\n"
    )

    return "\n".join(lines)


def _render_conclusions(
    plan: Dict[str, Any],
    audit: Optional[List[Dict[str, Any]]],
) -> str:
    """Render section 11: Conclusions.

    The conclusions section synthesises the plan objectives against available
    data but does not generate new strategic judgments.

    Parameters
    ----------
    plan : dict
        Research plan.
    audit : list[dict] or None
        Audit findings.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Conclusions\n"]

    objectives = plan.get("research_objectives", plan.get("objectives", []))
    if objectives:
        lines.append("### Status Against Objectives\n")
        for obj in objectives:
            oid = obj.get("id", "") if isinstance(obj, dict) else ""
            desc = (
                obj.get("description", obj.get("title", ""))
                if isinstance(obj, dict)
                else obj
            )
            lines.append(f"- **{oid}** {desc}: _included in analysis_")
        lines.append("")

    if audit:
        lines.append("### Audit Conclusion\n")
        passed = any(
            f.get("pass_fail_decision") == "pass"
            for f in audit
        )
        minor = any(
            f.get("pass_fail_decision") == "pass_with_minor_revisions"
            for f in audit
        )
        failed = any(
            f.get("pass_fail_decision") == "fail_requires_major_revisions"
            for f in audit
        )
        if failed:
            lines.append(
                "> ⚠ **This report has unresolved critical audit findings. "
                "It should not be considered final.**\n"
            )
        elif minor:
            lines.append("_This report passed audit with minor revisions._\n")
        elif passed:
            lines.append("_This report passed audit._\n")
    else:
        lines.append(
            "_No audit was performed. Findings should be independently verified._\n"
        )

    return "\n".join(lines)


def _render_source_inventory(
    market: Optional[List[Dict[str, Any]]],
    evidence: Optional[List[Dict[str, Any]]],
    claims: Optional[List[Dict[str, Any]]],
) -> str:
    """Render section 12: Source Inventory.

    Parameters
    ----------
    market : list[dict] or None
        Market records.
    evidence : list[dict] or None
        Evidence records.
    claims : list[dict] or None
        Claim records.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Source Inventory\n"]

    # Collect all source IDs
    source_set: set = set()
    for dataset, label in [
        (market, "market"),
        (evidence, "evidence"),
        (claims, "claims"),
    ]:
        if dataset is None:
            continue
        for rec in dataset:
            sid = rec.get("source_id", "")
            if sid:
                source_set.add(sid)
            for s in rec.get("source_ids", []):
                if isinstance(s, str):
                    source_set.add(s)
            # Evidence cites
            citation = rec.get("citation", rec.get("source", {}))
            if isinstance(citation, dict):
                pmid = citation.get("pmid", "")
                doi = citation.get("doi", "")
                if pmid:
                    source_set.add(f"PMID:{pmid}")
                if doi:
                    source_set.add(f"DOI:{doi}")

    if source_set:
        lines.append("### Sources Referenced\n")
        for src in sorted(source_set):
            lines.append(f"- {src}")
    else:
        lines.append("_No sources recorded._")
    lines.append("")

    # Record counts
    lines.append("### Record Counts by Artifact\n")
    lines.append("| Artifact | Records |")
    lines.append("|----------|---------|")
    lines.append(f"| Market | {len(market) if market else 0} |")
    lines.append(f"| Evidence | {len(evidence) if evidence else 0} |")
    lines.append(f"| Claims | {len(claims) if claims else 0} |")
    lines.append("")

    return "\n".join(lines)


def _render_appendices(
    brief_text: str,
    plan: Dict[str, Any],
    market: Optional[List[Dict[str, Any]]],
    evidence: Optional[List[Dict[str, Any]]],
    competitors: Optional[List[Dict[str, Any]]],
    claims: Optional[List[Dict[str, Any]]],
    audit: Optional[List[Dict[str, Any]]],
) -> str:
    """Render section 13: Appendices.

    Parameters
    ----------
    brief_text : str
        Raw brief text (included in full).
    plan : dict
        Research plan.
    market : list[dict] or None
        Market records.
    evidence : list[dict] or None
        Evidence records.
    competitors : list[dict] or None
        Competitor records.
    claims : list[dict] or None
        Claim records.
    audit : list[dict] or None
        Audit records.

    Returns
    -------
    str
        Markdown section content.
    """
    lines = ["## Appendices\n"]

    # Appendix A: Artifact manifest
    lines.append("### Appendix A: Artifact Manifest\n")
    lines.append("| Artifact | Format | Records |")
    lines.append("|----------|--------|---------|")
    artifacts = [
        ("Brief", "markdown", "N/A"),
        ("Plan", "json", "N/A"),
        ("Market", "jsonl", str(len(market)) if market else "N/A"),
        ("Evidence", "jsonl", str(len(evidence)) if evidence else "N/A"),
        ("Competitors", "jsonl", str(len(competitors)) if competitors else "N/A"),
        ("Claims", "jsonl", str(len(claims)) if claims else "N/A"),
        ("Audit", "jsonl", str(len(audit)) if audit else "N/A"),
    ]
    for name, fmt, count in artifacts:
        lines.append(f"| {name} | {fmt} | {count} |")
    lines.append("")

    # Appendix B: Research Brief (full text)
    lines.append("### Appendix B: Research Brief\n")
    lines.append("<details>")
    lines.append("<summary>Click to expand the full research brief</summary>\n")
    lines.append(brief_text)
    lines.append("</details>\n")

    # Appendix C: Plan Summary
    lines.append("### Appendix C: Plan Summary\n")
    lines.append("```json")
    # Redact verbose fields for readability
    plan_summary = {
        k: v
        for k, v in plan.items()
        if k not in ("platform_tasks", "tasks", "raw_content")
    }
    lines.append(json.dumps(plan_summary, indent=2, ensure_ascii=False))
    lines.append("```\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main report assembly
# ---------------------------------------------------------------------------


def _generate_report(
    brief_text: str,
    plan: Dict[str, Any],
    market: Optional[List[Dict[str, Any]]],
    evidence: Optional[List[Dict[str, Any]]],
    competitors: Optional[List[Dict[str, Any]]],
    claims: Optional[List[Dict[str, Any]]],
    audit: Optional[List[Dict[str, Any]]],
) -> str:
    """Assemble the complete markdown report from all artifacts.

    Parameters
    ----------
    brief_text : str
        Raw content of the research brief.
    plan : dict
        Parsed research plan.
    market : list[dict] or None
        Market research records.
    evidence : list[dict] or None
        Evidence records.
    competitors : list[dict] or None
        Competitor records.
    claims : list[dict] or None
        Claim verification records.
    audit : list[dict] or None
        Audit finding records.

    Returns
    -------
    str
        Complete markdown report.
    """
    sections: List[str] = []

    sections.append(_render_title_metadata(brief_text, plan))
    sections.append("---\n")
    sections.append(_render_executive_summary(plan, market, audit))
    sections.append("---\n")
    sections.append(_render_research_questions(plan))
    sections.append("---\n")
    sections.append(_render_method(plan))
    sections.append("---\n")
    sections.append(_render_market_landscape(market))
    sections.append("---\n")
    sections.append(_render_competitor_analysis(competitors))
    sections.append("---\n")
    sections.append(_render_evidence_review(evidence))
    sections.append("---\n")
    sections.append(_render_claim_verification(claims))
    sections.append("---\n")
    sections.append(_render_regulatory_context(market, evidence))
    sections.append("---\n")
    sections.append(_render_limitations(audit))
    sections.append("---\n")
    sections.append(_render_conclusions(plan, audit))
    sections.append("---\n")
    sections.append(_render_source_inventory(market, evidence, claims))
    sections.append("---\n")
    sections.append(_render_appendices(brief_text, plan, market, evidence, competitors, claims, audit))

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments, load artifacts, generate report, and return exit code."""
    parser = argparse.ArgumentParser(
        description="Generate a project-level market research report from "
                    "cross-skill artifact files.",
    )
    parser.add_argument(
        "--brief",
        type=str,
        required=True,
        help="Path to research brief (brief.md)",
    )
    parser.add_argument(
        "--plan",
        type=str,
        required=True,
        help="Path to research plan (plan.json)",
    )
    parser.add_argument(
        "--market",
        type=str,
        default=None,
        help="Path to market research data (market.jsonl)",
    )
    parser.add_argument(
        "--evidence",
        type=str,
        default=None,
        help="Path to academic evidence data (evidence.jsonl)",
    )
    parser.add_argument(
        "--competitors",
        type=str,
        default=None,
        help="Path to competitor analysis data (competitors.jsonl)",
    )
    parser.add_argument(
        "--claims",
        type=str,
        default=None,
        help="Path to claim verification data (claims.jsonl)",
    )
    parser.add_argument(
        "--audit",
        type=str,
        default=None,
        help="Path to audit findings (audit.jsonl)",
    )
    parser.add_argument(
        "--out",
        type=str,
        required=True,
        help="Output markdown report path (report.md)",
    )
    args = parser.parse_args()

    # -- Load required artifacts --
    log_info("Loading required artifacts...")
    brief_text = _load_text(Path(args.brief))
    plan = _load_json(Path(args.plan))

    # -- Load optional artifacts --
    log_info("Loading optional artifacts...")
    market = _load_optional_jsonl(args.market)
    evidence = _load_optional_jsonl(args.evidence)
    competitors = _load_optional_jsonl(args.competitors)
    claims = _load_optional_jsonl(args.claims)
    audit = _load_optional_jsonl(args.audit)

    # -- Generate report --
    log_info("Generating report...")
    try:
        report = _generate_report(
            brief_text, plan, market, evidence, competitors, claims, audit
        )
    except Exception as exc:
        log_error(f"Report generation failed: {exc}")
        return 3

    # -- Write output --
    out_path = Path(args.out)
    try:
        out_path.write_text(report, encoding="utf-8")
    except OSError as exc:
        log_error(f"Failed to write report to {out_path}: {exc}")
        return 3

    log_info(f"Report written to {out_path} ({len(report)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
