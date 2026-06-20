# Report Structure Guide

Section-by-section guide for the four standard report modes: quick competitor
review, full market review, evidence review, and claim-substantiation report.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: SKILL.md (lines 44-99 report modes, lines 101-118
architecture, lines 121-134 executive summary, lines 136-153 methods, lines
318-336 limitations), table-specifications.md (competitor and evidence table
column specs), source-attribution-style.md (citation format and traceability),
quantitative-reporting-rules.md (formula and derivation requirements),
calibrated-language.md (cautious wording conventions).

---

## Table of Contents

1. [Report modes and section matrix](#1-report-modes-and-section-matrix)
2. [Title](#2-title)
3. [Executive summary](#3-executive-summary)
4. [Research question and scope](#4-research-question-and-scope)
5. [Methods](#5-methods)
6. [Product or intervention definition](#6-product-or-intervention-definition)
7. [Main findings](#7-main-findings)
8. [Comparative or evidence analysis](#8-comparative-or-evidence-analysis)
9. [Regulatory and safety considerations](#9-regulatory-and-safety-considerations)
10. [Interpretation](#10-interpretation)
11. [Limitations](#11-limitations)
12. [Conclusions](#12-conclusions)
13. [References](#13-references)
14. [Appendices or source inventory](#14-appendices-or-source-inventory)
15. [Section ordering rules](#15-section-ordering-rules)
16. [Mode-specific templates](#16-mode-specific-templates)

---

## 1. Report modes and section matrix

Four standard report modes are defined. Use the section matrix to determine
which sections are required, optional, or prohibited for each mode.

### 1.1 Mode definitions

| Mode | ID | Purpose |
|------|----|---------|
| Quick competitor review | `quick-competitor` | Target product vs. competitors on price, dose, channel, and positioning. Light evidence context. |
| Full market review | `full-market` | Comprehensive landscape: products, platforms, pricing, competitors, consumers, evidence, and regulatory context. |
| Evidence review | `evidence-review` | Systematic or focused appraisal of clinical or scientific evidence for a defined question. |
| Claim-substantiation report | `claim-substantiation` | Assessment of whether a specific commercial or scientific claim is supported by available evidence. |

### 1.2 Section requirement matrix

| Section | Quick competitor | Full market | Evidence review | Claim-substantiation |
|---------|:-:|:-:|:-:|:-:|
| Title | R | R | R | R |
| Executive summary | R | R | R | R |
| Research question and scope | R | R | R | R |
| Methods | R | R | R | R |
| Product or intervention definition | R | R | R | R |
| Main findings | R | R | R | R |
| Comparative or evidence analysis | R | R | R | R |
| Regulatory and safety considerations | O | R | R | O |
| Interpretation | O | R | R | R |
| Limitations | R | R | R | R |
| Conclusions | R | R | R | R |
| References | R | R | R | R |
| Appendices or source inventory | O | R | O | O |

**Key**: R = Required, O = Optional, P = Prohibited. Blank cells default to Optional.

### 1.3 Prohibited sections by mode

| Section | Quick competitor | Full market | Evidence review | Claim-substantiation |
|---------|:-:|:-:|:-:|:-:|
| Unsupported market opportunity statements | P | P | P | P |
| Promotional or marketing language | P | P | P | P |
| Fabricated data, dates, or citations | P | P | P | P |
| Consumer reviews presented as efficacy evidence | P | P | P | P |
| Ingredient-level evidence presented as finished-product evidence | P | P | P | P |

---

## 2. Title

### 2.1 Required content

- Report mode descriptor (e.g., "Quick Competitor Review", "Full Market Review",
  "Evidence Review", "Claim-Substantiation Report").
- Primary product, intervention, or claim in scope.
- Date of report or version identifier.

### 2.2 Format

```
[Mode]: [Product or Topic] — [Date or Version]
```

Example:

```
Full Market Review: Glucosamine Sulfate 1500 mg — 2026-06-20
```

### 2.3 Optional content

- Geographic scope indicator (e.g., "China Market", "APAC").
- Subtitle with project identifier.

### 2.4 Prohibited content

- **Never include promotional language or unsupported superlatives.**
- **Never fabricate a market descriptor** (e.g., do not call a product
  "market-leading" without documented market-share data).
- **Never omit the date or version.**

---

## 3. Executive summary

### 3.1 Required content

State, in a self-contained paragraph or structured bullet format:

- What was reviewed — the product, intervention, or claim.
- Market and time scope — platforms, date range, geography.
- Main findings — the top 3 to 5 conclusions supported by the body.
- Most important evidence limitations.
- Practical conclusion — the actionable takeaway.
- Unresolved critical issue, if any.

### 3.2 Template

```
This [mode] examined [product/intervention/claim] in [scope/market]
during [date range]. Sources included [platforms/databases].

Key findings:
- [Finding 1 — supported by body section X]
- [Finding 2 — supported by body section Y]
- [Finding 3 — supported by body section Z]

Limitations include [primary limitation 1] and [primary limitation 2].
[Practical conclusion]. [Unresolved issue if present].
```

### 3.3 Prohibited content

- **Never introduce information absent from the body.**
- **Never use promotional language** (e.g., "best-in-class", "revolutionary",
  "game-changing").
- **Never present interpretation as fact** without the hedging language used in
  the body.
- **Never include unsupported numerical claims** — every number in the summary
  must appear in the body with its source.

### 3.4 Optional content

- A single sentence on recommended next steps, if grounded in the body.
- A note that the full report should be read for detailed evidence and
  limitations.

---

## 4. Research question and scope

### 4.1 Required content

- The exact research question as stated in the project brief or refined during
  planning.
- Geographic scope — country, region, or market.
- Time scope — collection date range or search date range.
- Platform or database scope — which platforms, databases, or registries were
  included and why.

### 4.2 Format

State the research question verbatim, followed by scope parameters.

### 4.3 Prohibited content

- **Never modify the research question** after the research is complete to match
  the findings.
- **Never omit the time scope** — every report must state when data were collected.

### 4.4 Optional content

- Sub-questions or secondary objectives.
- Explicit exclusion criteria.

---

## 5. Methods

### 5.1 Required content

Describe what was actually done. Include as applicable:

- Platforms or databases searched.
- Collection or search dates.
- Geographic scope confirmation.
- Competitor inclusion and exclusion criteria (for market reviews).
- Product normalization rules applied.
- Price normalization basis (price type, tax handling, currency).
- Evidence eligibility criteria (for evidence reviews and claim-substantiation).
- Regulatory jurisdictions checked.
- Major access limitations (e.g., paywalls, login requirements, geo-blocking).
- Whether the work was rapid, focused, narrative, or systematic.

### 5.2 Template

```
## Methods

### Data collection
Platforms searched: [list]
Date range: [start] to [end]
Geographic scope: [region]

### Product selection
[Competitor/product inclusion criteria]
[Normalization rules applied]

### Price analysis
Price type used: [sale_price / coupon_price / etc.]
Tax handling: [included / excluded / unknown]
Currency: [ISO 4217 code]

### Evidence assessment
[Search strategy]
[Eligibility criteria]
[Certainty assessment method]

### Limitations of method
[Access limitations, temporal constraints, language restrictions]
```

### 5.3 Prohibited content

- **Never call a review "systematic" merely because it uses several databases.**
  A systematic review requires a pre-registered protocol, comprehensive search,
  dual screening, and risk-of-bias assessment.
- **Never claim a method was applied when it was not** — describe what was
  actually done, not what would have been ideal.
- **Never omit the date range.**

### 5.4 Optional content

- Deviations from the planned method with rationale.
- Software or tools used.

---

## 6. Product or intervention definition

### 6.1 Required content

For each product or intervention reviewed:

- Normalized product name.
- Brand name(s).
- Manufacturer.
- Active ingredient(s) and per-unit dose.
- Dosage form and route.
- Package size(s) observed.
- Product version or regional variant, if applicable.
- Source of the product definition (regulatory record, label, official page).

### 6.2 Format

Use a structured table or bullet list. Include the product-master identifier
when available.

### 6.3 Prohibited content

- **Never merge products based on similar names alone** — always verify
  manufacturer, formulation, dose, and version.
- **Never present a marketplace listing's description as the official product
  definition** — distinguish seller-created content.
- **Never omit the source of the product definition.**

### 6.4 Optional content

- Regulatory registration numbers.
- Photograph or screenshot reference.
- Comparison to reference or innovator product.

---

## 7. Main findings

### 7.1 Required content

Present the core research output organized by theme or question.
Structure depends on the report mode:

| Mode | Main findings structure |
|------|------------------------|
| Quick competitor review | Competitor landscape, price and dose comparison, channel analysis, positioning summary. |
| Full market review | Product landscape, platform differences, competitor segmentation, price/dose/channel analysis, consumer narratives, evidence context. |
| Evidence review | Evidence map, outcome findings by endpoint, safety findings, certainty assessment, guideline context. |
| Claim-substantiation report | Exact claim restatement, evidence mapping, population/formulation/dose/outcome match analysis, support classification. |

### 7.2 Required for all modes

- Every finding must cite its source using a source ID or reference.
- Quantitative findings must state the formula, inputs, and rounding rule.
- Conflicting values from different sources must be disclosed, not silently
  resolved.

### 7.3 Prohibited content

- **Never present commercial claims as scientific findings.**
- **Never present consumer reviews as proof of efficacy or safety.**
- **Never fabricate data, prices, sales figures, or dates.**
- **Never infer sales from review counts or popularity metrics.**
- **Never calculate daily cost without a confirmed daily dosage.**

### 7.4 Optional content

- Sub-headings for thematic grouping.
- Visual summaries (charts, figures) with source attribution.

---

## 8. Comparative or evidence analysis

### 8.1 Required content

For market reviews: a competitor comparison table per
table-specifications.md.

For evidence reviews and claim-substantiation: an evidence table per
table-specifications.md.

### 8.2 Format

Use the table specifications defined in table-specifications.md. Do not
substitute narrative description for structured comparison when comparison is
the purpose.

### 8.3 Prohibited content

- **Never merge competitor table cells that hide data differences.**
- **Never omit uncertainty intervals** from evidence table effect estimates.
- **Never compare products on incompatible bases** — always use the same
  price type, same dose normalization, and same collection period.
- **Never present ingredient-level evidence as finished-product evidence**
  without documenting the extrapolation and its limitations.

### 8.4 Optional content

- Heatmap or visual comparison supplementing the table.
- Stratified analysis by platform, seller type, or region.

---

## 9. Regulatory and safety considerations

### 9.1 Required content

When relevant to the research question:

- Regulatory classification of the product (drug, medical device, health
  supplement, cosmetic, food) per the relevant jurisdiction.
- Registration or approval status.
- Known safety signals, adverse events, contraindications, or warnings from
  official sources.
- Guideline recommendations, if applicable.

### 9.2 Required sections by mode

| Mode | Regulatory required? |
|------|:-:|
| Quick competitor review | Optional |
| Full market review | Required |
| Evidence review | Required |
| Claim-substantiation report | Optional (required if claim touches regulatory status) |

### 9.3 Prohibited content

- **Never present a regulatory classification from a different jurisdiction
  without stating the jurisdiction.**
- **Never imply absence of risk from absence of reported events.**
- **Never cite a non-authoritative source for regulatory status** — use
  official regulatory databases or official manufacturer filings.

### 9.4 Optional content

- Comparison of regulatory status across jurisdictions.
- Pending applications or recent regulatory actions.

---

## 10. Interpretation

### 10.1 Required content

Synthesize the findings into a coherent narrative that addresses the research
question. Distinguish:

- Observed market pattern.
- Interpretation of the pattern.
- Business or strategic implication.
- Recommendation (if the brief requested one).
- Remaining uncertainty.

### 10.2 Required for full market reviews and evidence reviews

- Discussion of how findings compare to existing published data.
- Identification of evidence gaps.
- Assessment of generalizability.

### 10.3 Prohibited content

- **Never fabricate a market opportunity because the report format expects one.**
- **Never imply causality from observational data.**
- **Never imply clinical efficacy from mechanistic or ingredient data alone.**
- **Never equate statistical significance with clinical meaningfulness.**
- **Never present interpretation as fact** — use calibrated language per
  calibrated-language.md.

### 10.4 Optional content

- Scenario analysis or sensitivity analysis.
- Comparison to prior market reports (with source).

---

## 11. Limitations

### 11.1 Required content

A dedicated Limitations section. Address, as applicable:

- Dynamic prices and promotions — prices may have changed since collection.
- Inaccessible pages or paywalled content.
- Platform login or geo-blocking requirements.
- Nontransparent sales metrics — review counts do not equal sales.
- Incomplete product identity — missing regulatory records, unverified
  manufacturers.
- Seller-generated descriptions — may not match official product information.
- Temporal mismatch — different products collected on different dates.
- Regional version differences — products may differ across markets.
- Publication access — paywalled journal articles.
- Incomplete literature coverage — databases searched may not capture all
  relevant studies.
- Language restrictions — only [language(s)] sources were reviewed.
- Lack of direct finished-product evidence — ingredient evidence extrapolated.
- Absence of independent market-volume data — sales estimates not confirmed.
- Automated extraction errors — web scraping or API parsing limitations.

### 11.2 Template

```
## Limitations

This review is subject to the following limitations:

- **Price data**: [Specific statement about price volatility, collection
  window, and platform scope.]
- **Evidence coverage**: [Databases searched, languages, publication types,
  and known gaps.]
- **Product identity**: [Unverified or incomplete product information.]
- **Consumer data**: [Consumer comments reflect self-reported experience and
  are not verified clinical outcomes.]
- **Temporal**: [Data collected during a specific window; market conditions
  may have changed.]
- **Access**: [Platforms, articles, or registries that could not be accessed.]

These limitations should be considered when interpreting the conclusions.
```

### 11.3 Prohibited content

- **Never omit the limitations section** — every report mode requires it.
- **Never use a generic limitations paragraph** that does not address the
  specific limitations of this research.
- **Never minimize limitations to make conclusions appear stronger.**

### 11.4 Optional content

- Mitigation steps taken for each limitation.
- Recommendations for addressing limitations in future work.

---

## 12. Conclusions

### 12.1 Required content

- Direct answer to the research question.
- Summary of only the supported findings — do not introduce new information.
- Statement of the strength of evidence supporting each conclusion.
- Distinction between market attractiveness and clinical substantiation.
- Identification of unresolved issues.
- No new facts, sources, or data.

### 12.2 Prohibited content

- **Never introduce new facts, sources, or data.**
- **Never overstate the certainty of conclusions** — use evidence-calibrated
  language per calibrated-language.md.
- **Never present a commercial claim as a conclusion** unless it has been
  independently substantiated in the body.

### 12.3 Optional content

- Recommendations for further research or data collection.
- Decision-relevant framing for the intended audience.

---

## 13. References

### 13.1 Required content

Every source cited in the body must appear in the references section with:

- Source ID (per source-attribution-style.md).
- Full bibliographic or platform citation.
- URL (with access date for web sources).
- For academic sources: DOI, PMID, or registry identifier.
- For regulatory sources: authority, document title, date.

### 13.2 Format

Use the citation format defined in source-attribution-style.md.

### 13.3 Prohibited content

- **Never omit the references section.**
- **Never cite a source without a source ID.**
- **Never cite a source that does not support the associated statement.**

---

## 14. Appendices or source inventory

### 14.1 Required content

When included:

- Source inventory table listing all sources used, with platform, URL,
  collection date, and data category.
- Calculation notes for reviewer-derived values (formulas, inputs, assumptions).
- Unresolved conflict records.

### 14.2 Required sections by mode

| Mode | Appendices required? |
|------|:-:|
| Quick competitor review | Optional |
| Full market review | Required |
| Evidence review | Optional |
| Claim-substantiation report | Optional |

### 14.3 Prohibited content

- **Never include raw consumer data that contains PII** (names, emails, phone
  numbers, real names of individual reviewers).
- **Never include fabricated source records.**

---

## 15. Section ordering rules

### 15.1 Standard order (all modes)

1. Title
2. Executive summary
3. Research question and scope
4. Methods
5. Product or intervention definition
6. Main findings
7. Comparative or evidence analysis
8. Regulatory and safety considerations
9. Interpretation
10. Limitations
11. Conclusions
12. References
13. Appendices or source inventory

### 15.2 Mode-specific variations

**Quick competitor review**: Sections 9 (Interpretation) and 14 (Appendices)
are optional. Section 8 (Regulatory) is optional unless safety-relevant.

**Full market review**: Use the full standard order. Appendices are required.

**Evidence review**: Move section 5 (Product definition) to follow section 4
(Methods) if the product is the intervention. Section 8 (Regulatory) is
required.

**Claim-substantiation report**: The claim must be restated verbatim in both
section 3 (scope) and section 6 (main findings). Section 9 (Interpretation)
should include alternative wording recommendations when the claim is not fully
supported.

### 15.3 Prohibited ordering

- **Never place the limitations section before the main findings** — readers
  must see the evidence before the caveats.
- **Never place the conclusions before the limitations.**
- **Never bury critical limitations in an appendix.**

---

## 16. Mode-specific templates

### 16.1 Quick competitor review template

```
# Quick Competitor Review: [Product Name] — [Date]

## Executive summary
[Template per section 3.2]

## Research question and scope
[Question from brief]

## Methods
[Platforms, dates, selection criteria, normalization rules]

## Product definition: [Target Product]
[Name, brand, manufacturer, ingredient, dose, form, package, source]

## Competitor landscape
[Competitor comparison table per table-specifications.md]

## Price and dose analysis
[Normalized comparison with formulas and sources]

## Channel and positioning
[Platform distribution, seller types, commercial claims]

## Regulatory and safety context (optional)
[Registration status, known warnings]

## Limitations
[Template per section 11.2]

## Conclusions
[Answer to research question, evidence strength]

## References
[Source IDs and citations]

## Appendices (optional)
[Source inventory, calculation notes]
```

### 16.2 Full market review template

```
# Full Market Review: [Product or Market] — [Date]

## Executive summary
[Template per section 3.2]

## Research question and scope
[Question from brief]

## Methods
[Template per section 5.2]

## Product landscape
[Product definitions, market segmentation, platform distribution]

## Competitor analysis
[Competitor matrix, segmentation, positioning map]

## Price, dose, and channel analysis
[Normalized price comparison, daily cost analysis, channel mix]

## Consumer narratives
[Thematic summary of consumer-generated content, with platform and date]

## Evidence context
[Evidence table per table-specifications.md]

## Regulatory context
[Jurisdiction-specific regulatory classification and status]

## Interpretation
[Observed patterns, interpretation, implications, recommendations,
uncertainty]

## Limitations
[Template per section 11.2]

## Conclusions
[Answer to research question, evidence strength, unresolved issues]

## References
[Source IDs and citations]

## Appendices
[Source inventory, calculation notes, conflict records]
```

### 16.3 Evidence review template

```
# Evidence Review: [Question or Intervention] — [Date]

## Executive summary
[Template per section 3.2]

## Research question and scope
[PICO or equivalent structured question]

## Methods
[Search strategy, databases, eligibility criteria, certainty assessment]

## Intervention definition
[Product, dose, formulation, route, comparator]

## Evidence map
[PRISMA-style flow or structured summary of included studies]

## Outcome findings
[Evidence table per table-specifications.md, organized by outcome]

## Safety findings
[Adverse events, contraindications, warnings]

## Regulatory and guideline context
[Guideline recommendations, regulatory assessments]

## Interpretation
[Certainty assessment, generalizability, evidence gaps]

## Limitations
[Template per section 11.2, plus evidence-specific limitations]

## Conclusions
[Answer to research question, evidence strength]

## References
[Source IDs and citations, with DOIs and PMIDs]

## Appendices (optional)
[Search strings, excluded studies with reasons, source inventory]
```

### 16.4 Claim-substantiation report template

```
# Claim-Substantiation Report: [Exact Claim] — [Date]

## Executive summary
[Template per section 3.2, with support classification]

## Research question and scope
[Exact claim verbatim, product specification, assessment scope]

## Methods
[Evidence search, eligibility criteria, match analysis framework]

## Product specification
[Product identity, formulation, dose, target population, intended use]

## Claim analysis
[Claim restatement, claim type classification per claim-taxonomy.md]

## Evidence mapping
[Evidence table per table-specifications.md, organized by claim element]

## Population, formulation, dose, and outcome match
[Match analysis: direct, partial, indirect, or absent per claim element]

## Claim-support classification
[directly-supported | partially-supported | indirectly-supported |
unsupported | contradicted | cannot-determine]

## Alternative wording (if not fully supported)
[Qualified, supportable alternative phrasing]

## Regulatory risk
[Regulatory classification of the claim, jurisdiction-specific risks]

## Limitations
[Template per section 11.2, plus evidence extrapolation limitations]

## Conclusions
[Support classification and reasoning]

## References
[Source IDs and citations]

## Appendices (optional)
[Full evidence table, excluded evidence with reasons]
```

---

## General prohibitions

The following prohibitions apply to all report modes and sections:

- **Never include fabricated data, prices, doses, sales figures, citations,
  dates, or URLs.**
- **Never treat a commercial claim as scientific evidence.**
- **Never present consumer reviews as proof of efficacy or safety.**
- **Never omit the limitations section.**
- **Never present ingredient-level evidence as finished-product evidence**
  without documenting the extrapolation and its limitations.
- **Never calculate daily cost without a confirmed daily dosage.**
- **Never infer sales from review counts or popularity metrics.**
- **Never merge products based solely on similar names.**
- **Never use promotional language in any section.**
- **Never mark a report as complete with unresolved critical audit findings.**
