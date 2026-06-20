# Table Specifications

Column definitions, data types, formatting rules, and sentinels for the two
primary structured tables in market-research reports: the competitor
comparison table and the evidence table.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: SKILL.md (lines 218-253 table specifications, lines
193-215 quantitative reporting), report-structure-guide.md (comparative and
evidence analysis sections), source-attribution-style.md (source ID format,
inline citation rules), output-record-specification.md (product and price
field definitions), product-identity-rules.md (product normalization),
pricing-normalization.md (price type hierarchy, daily cost calculation),
schemas/competitor-matrix.schema.json (competitor matrix export schema).

---

## Table of Contents

1. [Competitor comparison table](#1-competitor-comparison-table)
2. [Evidence table](#2-evidence-table)
3. [Data type conventions](#3-data-type-conventions)
4. [Sentinel values](#4-sentinel-values)
5. [Formatting rules (both table types)](#5-formatting-rules-both-table-types)
6. [Prohibited table practices](#6-prohibited-table-practices)
7. [Table quality checklist](#7-table-quality-checklist)

---

## 1. Competitor comparison table

### 1.1 Purpose

Present a structured, row-by-row comparison of the target product and its
competitors on price, dose, cost, channel, and positioning. Every row
represents one distinct product or product version observed on one platform
from one seller.

### 1.2 Column definitions

| # | Column | Data type | Required | Description |
|---|--------|-----------|----------|-------------|
| 1 | `product_name` | String | Yes | Normalized product name per product-identity-rules.md. Includes brand, ingredient, dose, and form. Example: "Move Free Glucosamine 1500 mg tablets". |
| 2 | `brand` | String | Yes | Brand or manufacturer name. Use the registered brand, not the seller's store name. |
| 3 | `formulation` | String | Yes | Dosage form. One of: `tablet`, `capsule`, `softgel`, `oral_liquid`, `powder`, `granule`, `topical_cream`, `topical_ointment`, `injectable`, `patch`, `device`, `other`. |
| 4 | `per_unit_dose` | Number | Yes | Amount of active ingredient per single dosage unit. Include the unit. Example: `1500 mg`. |
| 5 | `active_ingredient` | String | Yes | Name of the primary active ingredient(s). For combination products, list all separated by semicolons. |
| 6 | `package_size` | Number | Yes | Total number of dosage units in the package. Example: `30` for 30 tablets. |
| 7 | `observed_price` | Number | Yes | The observed price in the transaction currency. Must specify price type in `price_type` column. |
| 8 | `price_currency` | String (ISO 4217) | Yes | Three-letter currency code. Example: `CNY`. Use `"unknown"` only when the currency cannot be determined. |
| 9 | `price_type` | Enum | Yes | One of: `sale_price`, `coupon_price`, `member_price`, `list_price`, `subscription_price`, `bundle_price`. Per pricing-normalization.md section 3. |
| 10 | `includes_tax` | Boolean | Yes | Whether the observed price includes applicable taxes. `true`, `false`, or `null` when unknown. |
| 11 | `unit_price` | Number | Yes | Price per single dosage unit, calculated as `observed_price / package_size`. 4 decimal places. |
| 12 | `unit_price_currency` | String (ISO 4217) | Yes | Currency of the unit price. Matches `price_currency`. |
| 13 | `daily_dose_units` | Number | Conditional | Number of dosage units per day per the labeled or official dose. Required when available. |
| 14 | `daily_dose_source` | Enum | Conditional | Source of the daily dose. One of: `label`, `official_site`, `clinical_guideline`, `regulatory_filing`, `assumption`. Required when `daily_dose_units` is present. |
| 15 | `daily_cost` | Number | Conditional | Estimated daily cost, calculated as `unit_price * daily_dose_units`. 2 decimal places. `null` when daily dose is unavailable. |
| 16 | `daily_cost_currency` | String (ISO 4217) | Conditional | Currency of the daily cost. Matches `price_currency`. Required when `daily_cost` is present. |
| 17 | `ai_normalized_price` | Number | Optional | Price per mg (or per base unit) of active ingredient. 6 decimal places. Per pricing-normalization.md section 5. |
| 18 | `platform` | String | Yes | Platform where the listing was observed. Use platform code per source-attribution-style.md section 1.2. Example: `jd`. |
| 19 | `seller_type` | Enum | Yes | One of: `official_flagship`, `authorized_retailer`, `marketplace_seller`, `cross_border`, `pharmacy`, `unknown`. |
| 20 | `seller_name` | String | Optional | Name of the seller or store, as displayed on the platform. |
| 21 | `principal_claims` | String | Optional | Primary commercial claims made on the listing, summarized in one sentence. Prefixed with `[Commercial claim]` label. |
| 22 | `collection_date` | String (ISO 8601 date) | Yes | Date the listing was collected. Format: `YYYY-MM-DD`. Must match the date component of the source ID. |
| 23 | `source_id` | String | Yes | Source identifier per source-attribution-style.md. Example: `jd-20260615-001`. |
| 24 | `key_caveat` | String | Conditional | Important qualification. Required when: price type is not `sale_price`, daily dose is assumed, product identity is unconfirmed, or tax status is unknown. |

### 1.3 Column ordering

Columns must appear in the order listed in 1.2. The grouping is:

1. Product identity (columns 1-5)
2. Package and price (columns 6-12)
3. Dose and daily cost (columns 13-17)
4. Channel and seller (columns 18-20)
5. Claims and metadata (columns 21-24)

### 1.4 Row ordering

Order rows by:

1. Target product first (if the report has a primary product).
2. Direct competitors (same active ingredient, same dose form) next.
3. Indirect competitors (different dose form, same ingredient) next.
4. Adjacent competitors (different ingredient, same indication) last.

Within each category, order by unit price ascending.

### 1.5 Conditional columns

| Condition | Columns required |
|-----------|-----------------|
| Daily dose available from label, official site, guideline, or regulatory filing | `daily_dose_units`, `daily_dose_source`, `daily_cost`, `daily_cost_currency` |
| Daily dose unavailable from any valid source | Set `daily_cost` to `null`; omit `daily_dose_units` and `daily_dose_source`; `key_caveat` must note "daily dose not confirmed" |
| Per-unit dose confirmed from regulatory or official source | `ai_normalized_price` may be calculated |
| Per-unit dose unconfirmed | `ai_normalized_price` must be `null` |
| Price type is not `sale_price` | `key_caveat` must note the price type used and any conditions (e.g., "member price — requires JD PLUS membership") |

---

## 2. Evidence table

### 2.1 Purpose

Present a structured, row-by-row summary of clinical or scientific evidence
relevant to the research question. Every row represents one distinct study,
systematic review, guideline, or regulatory assessment.

### 2.2 Column definitions

| # | Column | Data type | Required | Description |
|---|--------|-----------|----------|-------------|
| 1 | `study_id` | String | Yes | Short identifier for the study. Format: `[FirstAuthor][Year]`. Example: `Smith2023`. For guidelines: `[Organization][Year]`. |
| 2 | `full_citation` | String | Optional | Full bibliographic citation. Can be abbreviated when space-constrained; full citation must appear in the references section. |
| 3 | `design` | String | Yes | Study design. One of: `SR/MA` (systematic review/meta-analysis), `RCT`, `cohort_prospective`, `cohort_retrospective`, `case_control`, `case_series`, `cross_sectional`, `guideline`, `regulatory_assessment`, `PK/PD`, `animal`, `in_vitro`, `other`. |
| 4 | `population` | String | Yes | Brief description of the study population: condition, key inclusion criteria, age range, and sample size. Example: "Adults with knee OA, age 50-75, N = 240". |
| 5 | `intervention` | String | Yes | Intervention details: product name (if available), active ingredient, dose, frequency, route. Example: "Glucosamine sulfate 1500 mg once daily, oral". |
| 6 | `comparator` | String | Conditional | Comparator details. Required for controlled studies. Use `placebo`, active comparator name, or `no treatment`. |
| 7 | `duration` | String | Yes | Duration of treatment and follow-up. Example: "12 weeks treatment, 24 weeks total". Use `NR` if not reported. |
| 8 | `primary_outcome` | String | Yes | The primary endpoint as defined in the study, with measurement instrument. Example: "WOMAC pain subscale (0-20)". |
| 9 | `outcome_measure` | String | Yes | The specific measure reported in this row. May be primary or secondary. |
| 10 | `effect_estimate` | String | Yes | The effect estimate with uncertainty interval and statistical test result. Example: "MD -1.8 (95% CI -2.9 to -0.7), p = 0.001". |
| 11 | `effect_direction` | Enum | Yes | Direction of effect. One of: `favors_intervention`, `favors_comparator`, `no_difference`, `unclear`. |
| 12 | `certainty` | String | Yes | Certainty or quality of evidence assessment. Use GRADE ratings when available: `high`, `moderate`, `low`, `very_low`. Otherwise, state the assessment method. Use `not_assessed` when no formal assessment was performed. |
| 13 | `limitations` | String | Yes | Key study limitations: risk of bias, imprecision, indirectness, inconsistency, publication bias, or other concerns. Be specific. Example: "Open-label design; single center; industry-funded". |
| 14 | `applicability` | String | Yes | Assessment of whether the study applies to the research question. Consider population, intervention, dose, formulation, and outcome match. Use: `direct`, `partial` (with explanation), or `indirect` (with explanation). |
| 15 | `evidence_level` | Enum | Yes | The specific type of evidence this row represents for the research question. One of: `finished_product_RCT`, `finished_product_observational`, `ingredient_RCT`, `ingredient_observational`, `mechanistic`, `guideline_recommendation`, `regulatory_assessment`, `other`. |
| 16 | `doi_pmid` | String | Yes | DOI, PMID, or registry identifier. At least one must be provided. Format: `DOI: 10.XXXX/XXXXX` or `PMID: XXXXXXXX` or `NCTXXXXXXXX`. Use `not_available` only when genuinely unavailable. |
| 17 | `source_id` | String | Yes | Source identifier per source-attribution-style.md. |
| 18 | `key_caveat` | String | Conditional | Important qualification. Required when: evidence is ingredient-level (not finished product), applicability is partial or indirect, certainty is low or very low, or study is not peer-reviewed. |

### 2.3 Column ordering

Columns must appear in the order listed in 2.2. The grouping is:

1. Study identity (columns 1-2)
2. Methods (columns 3-7)
3. Outcomes (columns 8-11)
4. Assessment (columns 12-15)
5. Attribution (columns 16-18)

### 2.4 Row ordering

Order rows by evidence level per the clinical evidence hierarchy (source-hierarchy.md):

1. Guidelines and regulatory assessments.
2. Systematic reviews and meta-analyses.
3. Randomized controlled trials.
4. Observational studies (prospective, then retrospective).
5. PK/PD and mechanistic studies.
6. Animal studies.
7. In-vitro studies.

Within each level, order by publication date (most recent first).

### 2.5 Conditional columns

| Condition | Columns required |
|-----------|-----------------|
| Controlled study (RCT, cohort, case-control) | `comparator` |
| Uncontrolled study (case series, cross-sectional) | `comparator` may be `not_applicable` |
| GRADE assessment available | `certainty`: use GRADE rating |
| No formal certainty assessment | `certainty`: use `not_assessed` |
| Ingredient-level evidence | `key_caveat` must note "ingredient-level evidence; not confirmed in finished product" |
| Partial or indirect applicability | `key_caveat` must explain the mismatch |
| Finished-product RCT | `evidence_level`: use `finished_product_RCT` |
| Guideline recommendation | `evidence_level`: use `guideline_recommendation` |

---

## 3. Data type conventions

### 3.1 String fields

- Use sentence case for descriptions (e.g., "Glucosamine sulfate 1500 mg
  tablets").
- Do not use ALL CAPS unless the source itself uses them in a proper name.
- Truncate to 200 characters maximum in table cells. Longer content must go
  to footnotes or the body text.
- For `principal_claims`: always prefix with `[Commercial claim]` or
  `[Seller claim]` to distinguish from verified product information.

### 3.2 Number fields

- Do not include currency symbols or unit abbreviations in the number field.
  Use the companion unit/currency column.
- Apply the rounding rules from pricing-normalization.md section 12.
- Preserve intermediate values at full precision; round only the final
  displayed value.
- Negative values are prohibited for prices, costs, and doses. Use `0` only
  for free items, with a `key_caveat` explaining the reason.

### 3.3 Enum fields

- Use the exact values listed in the column definitions.
- Do not abbreviate or create ad-hoc values.
- When no enum value matches, use `other` and explain in `key_caveat`.

### 3.4 Date fields

- Use ISO 8601 format: `YYYY-MM-DD`.
- The `collection_date` must match the date component of the `source_id`.

### 3.5 Boolean fields

- Use lowercase `true` and `false`.
- Use `null` (not the string `"null"`, not `"unknown"`) when the value cannot
  be determined.

---

## 4. Sentinel values

### 4.1 Defined sentinels

| Sentinel | Meaning | When to use |
|----------|---------|-------------|
| `null` | Value is absent or cannot be determined | Daily cost when dose is missing; tax status when unknown. |
| `"unknown"` | The value exists conceptually but could not be identified from sources | Currency, seller type, or platform when unidentifiable. |
| `"not_applicable"` | The concept does not apply to this row | Comparator for uncontrolled studies; daily dose for non-consumable products. |
| `"not_available"` | The value should exist but the source does not provide it | DOI/PMID for a study that lacks an identifier. |
| `"not_assessed"` | A formal assessment was not performed | Certainty when no GRADE or equivalent assessment was done. |
| `"NR"` | The source did not report this value | Duration when not stated in the study. |

### 4.2 Sentinel selection rules

- Prefer `null` over `"unknown"` for fields with a defined Boolean or numeric
  type.
- Prefer `"unknown"` over `"not_applicable"` when the value might apply but
  cannot be confirmed.
- Prefer `"not_applicable"` over `"unknown"` when the concept genuinely does
  not apply.
- Never use `null` in a string-typed field. Use `"unknown"` or
  `"not_applicable"` instead.
- Never use `0` as a sentinel for missing numeric data. Use `null` instead.
  `0` means "zero", not "missing".

### 4.3 Sentinel in daily cost

- `daily_cost`: `null` means the daily dose could not be confirmed. This is
  the correct behavior per pricing-normalization.md section 11.
- `daily_cost`: `0.00` means the product is free. This requires a `key_caveat`
  explaining why.

---

## 5. Formatting rules (both table types)

### 5.1 Column width

- Adjust column widths so that no cell wraps more than 3 lines.
- The `key_caveat` column may be wider than other columns.
- If a column consistently contains short values (e.g., currency codes), use
  a narrow column width.

### 5.2 Text alignment

| Data type | Alignment |
|-----------|-----------|
| String (names, descriptions) | Left |
| Number (prices, costs, doses) | Right |
| Enum (price type, design) | Center |
| Date (ISO 8601) | Center |
| Boolean | Center |

### 5.3 Number formatting

| Value | Format | Example |
|-------|--------|---------|
| Observed price | 2 decimal places | `129.00` |
| Unit price | 4 decimal places | `4.3000` |
| Daily cost | 2 decimal places | `8.60` |
| AI-normalized price | 6 decimal places | `0.008600` |
| Package size | Integer | `30` |
| Daily dose units | 1 decimal place | `2.0` |
| Sample size | Integer with comma separators for >999 | `1,240` |

### 5.4 Cell merging

Cell merging is permitted only for:

- Grouping header rows (e.g., a "Product Identity" header spanning multiple
  columns).
- The `product_name` column when the same product appears in multiple rows
  with different price observations (different sellers, platforms, or dates).

**Never merge cells that would hide differences in data values.** Two rows
with different prices must never have their price cells merged. Two rows with
different doses must never have their dose cells merged.

### 5.5 Footnote markers

Use superscript numbers for footnotes: ¹, ², ³.

Footnotes appear below the table, not in a separate section.

Each footnote must be self-contained. The reader should not need to consult
another section to understand the footnote.

### 5.6 Empty cells

- Do not leave a cell visually empty. Always include the sentinel value
  (`null`, `"unknown"`, `"NR"`, `"not_applicable"`) or a dash (`—`) for
  genuinely inapplicable cells.
- A missing numeric value is `null`, not a blank cell.
- A missing string value is `"unknown"`, not a blank cell.

---

## 6. Prohibited table practices

- **Never merge cells that hide data differences.** Two products with different
  unit prices must never appear to share a unit price through cell merging.
- **Never omit uncertainty intervals from effect estimates** in the evidence
  table. Every effect estimate must include the 95% confidence interval,
  credible interval, standard error, or equivalent measure of uncertainty.
  Point estimates without uncertainty are not acceptable.
- **Never compare products on incompatible bases** — all rows must use the
  same price type, same currency (or explicitly converted), and comparable
  collection dates.
- **Never present a point estimate from a small study as if it were precise**
  — if the confidence interval is wide, the `key_caveat` must note the
  imprecision.
- **Never omit the `key_caveat` column when it is conditional** — if any
  condition listed in sections 1.5 or 2.5 is met, the column must be present
  and populated.
- **Never use `0` as a sentinel for missing numeric data.**
- **Never present live-stream prices (`live_price`) in a competitor comparison
  table alongside retail prices.** If a live-stream price must be referenced,
  report it in a separate row or table with an explicit label.
- **Never calculate daily cost when the daily dose is missing** from all
  valid sources. Set `daily_cost` to `null` and add a `key_caveat`.
- **Never omit the `limitations` column from an evidence table.**
- **Never present ingredient-level evidence as if it were finished-product
  evidence** without clearly labeling the `evidence_level` and adding a
  `key_caveat`.
- **Never present statistical significance without the corresponding effect
  estimate and uncertainty interval.**

---

## 7. Table quality checklist

Before finalizing a table, verify:

### Competitor table

- All products are identified with normalized names.
- All prices include currency and price type.
- All unit prices use 4 decimal places.
- Daily costs are present only when the daily dose is confirmed from a valid
  source.
- Daily dose source is recorded for every row with a daily cost.
- No live-stream prices are mixed with retail prices in the same comparison.
- Price types are consistent across compared rows (or discrepancies are noted).
- Every row has a `source_id` and `collection_date`.
- Every conditional `key_caveat` is present and specific.
- No cells are merged across rows with different data values.

### Evidence table

- Every study has a DOI, PMID, or registry identifier (or `not_available` with
  an explanation).
- Every effect estimate includes an uncertainty interval.
- Certainty is assessed for every row (or `not_assessed` is stated).
- `evidence_level` correctly distinguishes finished-product from ingredient
  evidence.
- `applicability` is explicitly stated for every row.
- Limitations are specific to each study, not generic.
- Ingredient-level evidence is flagged with a `key_caveat`.
- Studies are ordered by evidence hierarchy level.
- No raw consumer comments appear in the evidence table.
