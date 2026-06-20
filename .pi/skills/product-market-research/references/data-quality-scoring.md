# Data Quality Scoring

Guidance for scoring each piece of collected data across 8 quality
dimensions. The product record's `data_quality_score` field
(output-record-specification.md line 174) represents the overall quality
category after dimension-level assessment. That overall category is a
summary, not a replacement for per-dimension scores.

## Scoring Principles

- Every sourced fact gets scored on each of the 8 dimensions below.
- Each dimension uses 3 levels: `high` (green), `medium` (yellow), `low` (red).
- A dimension score is always accompanied by a short rationale explaining why.
- Do not collapse the 8 scores into a single opaque total. The overall
  `data_quality_score` is derived from the pattern of dimension scores but
  the per-dimension detail must remain visible in research notes or audit
  artifacts.
- When a dimension is not applicable (e.g., Direct Observation does not
  apply to a regulatory database entry), use `not_applicable` with a one-line
  explanation.

## Dimension 1: Source Authority

How authoritative is the source of this information?

| Level  | Criteria |
|--------|----------|
| high   | Official regulatory authority (NMPA, FDA, EMA, PMDA), official manufacturer product page, peer-reviewed journal via PubMed, government database, clinical trial registry. |
| medium | Authorized distributor page, platform-owned listing (Tmall Self-Owned, JD Self-Owned), established industry report (IQVIA, Mintel), recognized medical database (Drugs@FDA, WHO ATC/DDD). |
| low    | Third-party marketplace listing, consumer review, social media post, forum discussion, unverified blog, content farm, affiliate site, user-generated price tracker. Unauthenticated API response. |

**Rationale should cite**: who published the information and why they are or
are not an authoritative source for this specific data point.

## Dimension 2: Product Identity Certainty

How certain are we that the data refers to the exact product we are tracking?

| Level  | Criteria |
|--------|----------|
| high   | Official product identifier present and matched: NMPA approval number, FDA NDC, registration ID, batch number. Product identity confirmed at master and version level. |
| medium | Brand and product name match, dosage form and dose match, but no official registration ID was available for cross-check. Identity is probable but not confirmed. |
| low    | Only partial identity signals: generic name without brand, brand without variant information, ambiguous listing title, product name inferred from consumer description. Identity is possible or uncertain. |

**Rationale should cite**: which identity signals were matched (or absent),
whether a registration ID was cross-checked, and the certainty level per
product-identity-rules.md.

## Dimension 3: Field Completeness

What proportion of the required and expected fields are populated for this
record type?

| Level  | Criteria |
|--------|----------|
| high   | All required fields populated. Most optional fields relevant to the record type are also present. No critical gaps. |
| medium | All required fields populated. Several optional fields are missing but the record is usable for its primary purpose. |
| low    | One or more required fields are missing or set to `"unknown"`. The record has significant gaps that affect reliability. |

**Rationale should cite**: which expected fields are missing, whether those
gaps affect downstream analysis, and the record type being assessed.

## Dimension 4: Page Timeliness

How recent is the source page or observation relative to the analysis date?

| Level  | Criteria |
|--------|----------|
| high   | Collected within the last 30 days for dynamic sources (pricing, listings, platform metrics) or within 1 year for stable sources (regulatory filings, product labels that rarely change). |
| medium | Collected 30-90 days ago for dynamic sources, or 1-2 years ago for stable sources. Information likely still current but worth flagging. |
| low    | Collected more than 90 days ago for dynamic sources, or more than 2 years ago for stable sources. High risk of being outdated. |

**Rationale should cite**: the collection date, the source type (dynamic vs.
stable), and what may have changed since collection (price updates, formula
changes, regulatory status changes).

## Dimension 5: Original Evidence Saved

Was the original source content preserved as a snapshot, screenshot, PDF, or
archival copy?

| Level  | Criteria |
|--------|----------|
| high   | Full-page screenshot, PDF, or HTML archive saved. Snapshot is verifiable and includes all content relevant to the extracted data. |
| medium | Partial snapshot saved (e.g., screenshot of top portion only, or auto-saved HTML without rendered dynamic content). Snapshot exists but may not capture every element. |
| low    | No snapshot saved. URL only, or snapshot is a corrupt/unreadable file. The data cannot be independently verified against the original source. |

**Rationale should cite**: what type of evidence was saved (screenshot, PDF,
archived HTML, API response JSON), the file path, and any limitations of the
snapshot (dynamic content not captured, paywall, partial page).

## Dimension 6: Source Conflict

Are there conflicts between this source and other sources for the same data
point?

| Level  | Criteria |
|--------|----------|
| high   | No known conflicts. All sources that address this data point agree. Or this is the only available source and its authority is high. |
| medium | Minor conflicts exist but do not materially affect conclusions (e.g., slight price differences between platforms on the same day). Conflicts are resolved or resolvable. |
| low    | Material conflicts exist and are unresolved. Conflicting sources disagree on core facts (identity, price by >20%, contradictory regulatory status). Human review required. |

**Rationale should cite**: whether conflict records exist for this data point,
the number and severity of conflicting values, and the current resolution
status.

## Dimension 7: Direct Observation

Was the value directly observed on the source page, or was it inferred,
calculated, or copied from another context?

| Level  | Criteria |
|--------|----------|
| high   | Value directly visible on the source page and extracted verbatim. Price displayed on listing page. Ingredient listed on product label. Registration number displayed on regulatory filing. |
| medium | Value was calculated from directly observed data (e.g., unit price derived from package price and quantity). Value was extracted from a screenshot of a dynamic element. Value was transcribed from an image via OCR. |
| low    | Value was inferred or estimated without direct observation (e.g., "assumed 30-day month" for daily cost, price estimated from a range, dose assumed from standard regimen). Value copied from a secondary source that itself did not directly observe it. |

**Rationale should cite**: whether the value was seen on the page, any
inference or calculation performed, the formula used for derived values,
and the confidence in the extraction method.

## Dimension 8: Human Review

Has a human reviewed this data point for accuracy and consistency?

| Level  | Criteria |
|--------|----------|
| high   | Human reviewed and confirmed the extracted value against the source. Any corrections were applied and documented. |
| medium | Human glanced at the extraction but did not systematically verify every field. Spot-checked. Or human reviewed an automated extraction but only for obvious errors. |
| low    | No human review. Fully automated extraction with no human verification. Data passed through without any manual quality gate. |

**Rationale should cite**: who or what process performed the review, what
proportion of fields were checked, whether corrections were made, and the
date of review.

## Example: Scored Product Record

Below is an example showing how a product called "BrandX Vitamin C 500mg
Tablets" collected from a Tmall listing would look when scored across all 8
dimensions. This is illustrative only; actual scores depend on real source
conditions.

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Source Authority | medium | Tmall is a major e-commerce platform but not an official manufacturer site. Listing is from an authorized distributor storefront (Tmall Self-Owned). |
| Product Identity Certainty | medium | Brand and product name match the expected product. Dosage form (tablet) and dose (500 mg) match. No NMPA registration ID was available on the listing page for cross-check. |
| Field Completeness | medium | All 7 required product record fields populated. Optional fields missing: registration_id, identity_certainty. No critical gaps for a pricing comparison. |
| Page Timeliness | high | Collected 2025-06-20, within 30 days of analysis date. Price and listing details are current. |
| Original Evidence Saved | high | Full-page screenshot saved to `screenshots/tmall-20250620-001.png`. HTML archive also saved. Snapshot includes the price, product name, and seller information. |
| Source Conflict | high | No conflicting sources for this specific listing observation. Single listing record, no other Tmall listing for the same product collected on the same date. |
| Direct Observation | high | Price ("99.00") directly visible on listing page and extracted verbatim. Product name and dosage form read directly from the page title and description. |
| Human Review | low | Fully automated extraction via Playwright. No human verified the extracted values against the source screenshot. |

### Determining the Overall `data_quality_score`

The product record's `data_quality_score` field (see
output-record-specification.md line 174) is set based on the pattern of
dimension scores:

- **high**: 6 or more dimensions scored `high`, none scored `low`.
- **medium**: 4 or more dimensions scored `medium` or better, at most 1 or 2
  dimensions scored `low`.
- **low**: 3 or more dimensions scored `low`, or any single dimension scored
  `low` AND that dimension is material to the record's purpose (e.g., low
  Source Authority for a regulatory claim).
- **unknown**: Insufficient information to assess quality, or scoring was not
  performed.

The per-dimension scores must always accompany the overall score in research
notes. The overall score alone is never sufficient for audit or
reproducibility purposes.

## Usage in Research Workflow

1. After extracting data from a source, score each relevant dimension.
2. Record the per-dimension scores and rationales in the research notes or
   within the source record's `access_notes` or `data_quality_notes` fields.
3. When creating a product record, use the dimension pattern to determine the
   overall `data_quality_score` value.
4. If any dimension scores `low`, flag the product record for potential human
   review before using it in final analysis.
5. When two sources conflict on the same data point, compare their dimension
   scores to decide which to trust by default (but preserve both values per
   conflict resolution rules).
