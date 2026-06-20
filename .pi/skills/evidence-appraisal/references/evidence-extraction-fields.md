# Evidence Extraction Fields

Detailed field guide for extracting study data from included sources
during systematic evidence retrieval. Defines required versus optional
fields, field formats, sentinel values, and extraction rules for each
category of study information.

This reference extends the extraction checklist in SKILL.md Step 6
(Extract study data). Use it during extraction to ensure completeness
and consistency. Do not treat this guide as a substitute for reading
the full source.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: SKILL.md (Step 6 extraction checklist, Step 8
applicability assessment), study-design-appraisal.md (risk-of-bias
fields), claim-support-rules.md (directness dimensions), schemas/_defs.json
(sentinel value conventions).

---

## Table of Contents

1. [Extraction principles](#1-extraction-principles)
2. [Source identification fields](#2-source-identification-fields)
3. [Study design and setting fields](#3-study-design-and-setting-fields)
4. [Population and sample fields](#4-population-and-sample-fields)
5. [Intervention and exposure fields](#5-intervention-and-exposure-fields)
6. [Comparator fields](#6-comparator-fields)
7. [Outcome fields](#7-outcome-fields)
8. [Effect estimate fields](#8-effect-estimate-fields)
9. [Safety and adverse event fields](#9-safety-and-adverse-event-fields)
10. [Bias and quality fields](#10-bias-and-quality-fields)
11. [Extractor and provenance fields](#11-extractor-and-provenance-fields)
12. [Field format rules](#12-field-format-rules)
13. [Sentinel value rules](#13-sentinel-value-rules)
14. [Forbidden extractions](#14-forbidden-extractions)

---

## 1. Extraction principles

### 1.1 Source-first extraction

Extract exactly what the source reports. Do not reinterpret, summarize,
or paraphrase during extraction. The extraction record is a faithful
transcription of the source content into structured fields.

### 1.2 Distinguish reported from calculated

Separate values reported by the source from values calculated by the
reviewer. A risk ratio stated in the abstract is a source-reported value.
A risk ratio recalculated from raw event counts is a reviewer calculation.
Label each accordingly.

### 1.3 Extract negative and null results

Extract all prespecified outcomes, including those where the source
reports no statistically significant difference or a null result. Do
not extract only positive findings.

### 1.4 Preserve uncertainty

When the source reports a range, extract the range. When the source
reports a confidence interval, extract the interval bounds. Do not
collapse uncertainty into a point estimate unless both the point
estimate and its range or interval are preserved.

### 1.5 Record what is missing

When a field value exists but the source does not report it, record
the absence explicitly with a sentinel value. The absence of
information is itself an extraction finding.

---

## 2. Source identification fields

### 2.1 Required fields

| Field | Type | Description | Sentinel if missing |
|-------|------|-------------|---------------------|
| `source_id` | string | Unique source identifier per `source_id` format in _defs.json | Must not be missing |
| `citation` | string | Complete bibliographic citation in author-format style | `"unknown"` |
| `doi` | string or `null` | Digital Object Identifier, no URL prefix | `null` |
| `pmid` | string or `null` | PubMed ID as numeric string | `null` |
| `trial_registration` | string or `null` | Trial registry ID (NCT, ChiCTR, EUCTR, etc.) | `null` |
| `url` | string or `null` | Direct URL to the source | `null` |
| `publication_year` | integer or `null` | Four-digit publication year | `null` |
| `publication_type` | string | Journal article, preprint, guideline, regulatory document, etc. | `"unknown"` |

### 2.2 Optional fields

| Field | Type | Description |
|-------|------|-------------|
| `journal` | string | Journal name as it appears on the article |
| `volume` | string | Volume number |
| `issue` | string | Issue number |
| `pages` | string | Page range |
| `publisher` | string | Publisher name |
| `language` | string | ISO 639-1 two-letter language code |
| `access_status` | string | `"open_access"`, `"subscription"`, `"abstract_only"`, `"unknown"` |

### 2.3 Access status rule

Set `access_status` to `"abstract_only"` when extraction relies on the
abstract alone. Do not represent an abstract-only source as a full-text
verified source in any downstream synthesis.

---

## 3. Study design and setting fields

### 3.1 Required fields

| Field | Type | Description | Sentinel if missing |
|-------|------|-------------|---------------------|
| `study_design` | string | Study design classification | `"unknown"` |
| `study_design_detail` | string | Specific design subtype | `"unknown"` |
| `country` | string or array | ISO 3166-1 alpha-2 country code(s) | `"unknown"` |
| `setting` | string | Clinical setting: inpatient, outpatient, community, etc. | `"unknown"` |
| `multicenter` | boolean or `null` | Whether the study involved multiple sites | `null` |
| `number_of_sites` | integer or `null` | Number of sites if reported | `null` |

### 3.2 Study design classification values

| Value | Design | Examples |
|-------|--------|----------|
| `"rct"` | Randomized controlled trial | Parallel-group, crossover, cluster-randomized, factorial |
| `"observational_cohort"` | Cohort study | Prospective cohort, retrospective cohort |
| `"observational_case_control"` | Case-control study | Nested case-control, population-based |
| `"observational_cross_sectional"` | Cross-sectional study | Survey, prevalence study |
| `"systematic_review"` | Systematic review or meta-analysis | Pairwise meta-analysis, network meta-analysis |
| `"case_series"` | Case series or case report | Single case, small series |
| `"quasi_experimental"` | Quasi-experimental | Before-after, interrupted time series |
| `"mechanistic"` | Mechanistic or laboratory | In vitro, in vivo animal, pharmacokinetic |
| `"guideline"` | Clinical practice guideline | National guideline, consensus statement |
| `"regulatory"` | Regulatory assessment | FDA review, EMA assessment report, NMPA filing |
| `"unknown"` | Design cannot be determined | Use only when the source provides no design information |

### 3.3 Refine with `study_design_detail`

Use `study_design_detail` to record the specific design subtype:
`"double-blind_parallel_rct"`, `"prospective_cohort"`,
`"network_meta_analysis"`, `"nested_case_control"`, etc. This field
enables precise risk-of-bias assessment per study-design-appraisal.md.

---

## 4. Population and sample fields

### 4.1 Required fields

| Field | Type | Description | Sentinel if missing |
|-------|------|-------------|---------------------|
| `population_description` | string | Source text describing the study population | `"unknown"` |
| `eligibility_criteria` | string | Inclusion and exclusion criteria as stated | `"unknown"` |
| `sample_size_total` | integer or `null` | Total number of participants analyzed | `null` |
| `sample_size_per_arm` | object or `null` | Participants per arm/group: `{"arm_name": N, ...}` | `null` |
| `age_mean` | number or `null` | Mean age in years | `null` |
| `age_sd` | number or `null` | Standard deviation of age | `null` |
| `age_range` | string or `null` | Age range as reported | `null` |
| `sex_female_percent` | number or `null` | Percentage female | `null` |
| `baseline_characteristics` | string | Narrative description of baseline features | `"unknown"` |

### 4.2 Optional population fields

| Field | Type | Description |
|-------|------|-------------|
| `race_ethnicity` | string | Race or ethnicity breakdown as reported |
| `comorbidities` | string | Pre-existing conditions in the population |
| `disease_severity` | string | Disease stage or severity at baseline |
| `prior_treatment` | string | Previous treatments received |
| `geographic_region` | string | More specific location than country |

### 4.3 Population match for applicability

The population fields feed directly into the applicability assessment
in SKILL.md Step 8. When the study population differs materially from
the target population of the review question, record the difference
in `extractor_notes` and flag for applicability downgrade.

---

## 5. Intervention and exposure fields

### 5.1 Required fields

| Field | Type | Description | Sentinel if missing |
|-------|------|-------------|---------------------|
| `intervention_name` | string | Name of the intervention product or ingredient | `"unknown"` |
| `intervention_type` | string | Drug, supplement, device, behavioral, etc. | `"unknown"` |
| `active_ingredient` | string | Active pharmaceutical or supplement ingredient | `"unknown"` |
| `formulation` | string | Dosage form: tablet, capsule, liquid, injection, etc. | `"unknown"` |
| `dose_per_unit` | string | Dose per dosage unit with unit (e.g., "500 mg") | `"unknown"` |
| `dose_per_unit_value` | number or `null` | Numeric dose per unit | `null` |
| `dose_per_unit_unit` | string | Unit of dose per unit (mg, g, IU, CFU, etc.) | `"unknown"` |
| `route` | string | Route of administration | `"unknown"` |
| `frequency` | string | Dosing frequency (e.g., "2 times daily") | `"unknown"` |
| `daily_dose` | string | Total daily dose with unit (e.g., "1000 mg/day") | `"unknown"` |
| `duration` | string | Duration of intervention exposure | `"unknown"` |
| `duration_days` | number or `null` | Duration in days (for comparison) | `null` |

### 5.2 Dose extraction rules

Extract the dose exactly as stated. Record the numeric value and the
unit separately to enable normalization.

**Never infer dose from product name.** A product named "Vitamin C 1000"
may or may not contain 1000 mg per dose. The name is a marketing label,
not a dose declaration. Only extract dose from the study methods section,
product label, or official SmPC.

### 5.3 Formulation detail

When the source provides formulation details beyond the dosage form
( release mechanism, excipients, coating, salt form ), record them in
`intervention_detail`. Match chemical form for applicability: a study
on magnesium oxide does not automatically apply to magnesium citrate.

### 5.4 Multi-ingredient interventions

When the intervention contains multiple active ingredients, extract
each ingredient's dose separately. Do not sum doses across ingredients.
Create separate extraction entries for each ingredient when the review
question concerns ingredient-level effects.

---

## 6. Comparator fields

### 6.1 Required fields

| Field | Type | Description | Sentinel if missing |
|-------|------|-------------|---------------------|
| `comparator_name` | string | Name of the comparator | `"unknown"` or `"not_applicable"` |
| `comparator_type` | string | Placebo, active comparator, no treatment, etc. | `"unknown"` |
| `comparator_dose` | string | Comparator dose if active | `"not_applicable"` for placebo |
| `comparator_description` | string | Description of the comparator condition | `"unknown"` |

### 6.2 Comparator type values

| Value | Description |
|-------|-------------|
| `"placebo"` | Inert placebo indistinguishable from intervention |
| `"active"` | Another active intervention or standard of care |
| `"no_treatment"` | No treatment or observation only |
| `"sham"` | Sham procedure or sham device |
| `"waitlist"` | Waitlist control |
| `"usual_care"` | Treatment as usual or standard care |
| `"not_applicable"` | Single-arm study with no comparator |

### 6.3 Comparator for claim assessment

When assessing a commercial claim, the study comparator must match
the implied comparison in the claim. A claim of "better than leading
brand" requires a head-to-head study against the named brand. A
placebo-controlled trial does not support a comparative efficacy
claim against another active product.

---

## 7. Outcome fields

### 7.1 Required fields

| Field | Type | Description | Sentinel if missing |
|-------|------|-------------|---------------------|
| `outcome_name` | string | Name of the outcome as reported | Must not be missing |
| `outcome_domain` | string | Efficacy, safety, quality of life, biomarker, etc. | `"unknown"` |
| `outcome_type` | string | Primary, secondary, exploratory, safety, post-hoc | `"unknown"` |
| `outcome_definition` | string | How the outcome was defined or measured | `"unknown"` |
| `outcome_timepoint` | string | Timing of assessment (e.g., "12 weeks") | `"unknown"` |
| `outcome_measurement_tool` | string | Instrument or scale used | `"unknown"` |

### 7.2 Outcome type classification

| Value | Description |
|-------|-------------|
| `"primary"` | Prespecified primary outcome |
| `"secondary"` | Prespecified secondary outcome |
| `"exploratory"` | Additional outcome not in primary/secondary hierarchy |
| `"safety"` | Safety or adverse event outcome |
| `"post_hoc"` | Outcome defined after data collection |
| `"unknown"` | Hierarchy cannot be determined from source |

### 7.3 Outcome match for applicability

The extracted outcome must match the claimed outcome. A study measuring
serum biomarker levels does not directly support a claim about symptom
improvement unless the source demonstrates the biomarker-surrogate
relationship. Record outcome mismatch in `extractor_notes`.

---

## 8. Effect estimate fields

### 8.1 Required fields

| Field | Type | Description | Sentinel if missing |
|-------|------|-------------|---------------------|
| `effect_estimate_type` | string | Type of estimate: risk ratio, mean difference, OR, HR, etc. | `"unknown"` |
| `effect_estimate_value` | number or `null` | Point estimate | `null` |
| `ci_lower` | number or `null` | Lower bound of 95% confidence interval | `null` |
| `ci_upper` | number or `null` | Upper bound of 95% confidence interval | `null` |
| `ci_level` | number | Confidence level (default 95) | `95` |
| `p_value` | number or `null` | Reported p-value | `null` |
| `absolute_effect` | string or `null` | Absolute effect when reported (e.g., "ARR 3.2%") | `null` |
| `analysis_population` | string | ITT, per-protocol, modified ITT, as-treated | `"unknown"` |
| `statistical_method` | string | Statistical test or model used | `"unknown"` |

### 8.2 Effect estimate type values

| Value | Full name | Common context |
|-------|-----------|----------------|
| `"risk_ratio"` | Risk ratio or relative risk | Binary outcomes |
| `"odds_ratio"` | Odds ratio | Case-control, logistic regression |
| `"hazard_ratio"` | Hazard ratio | Time-to-event outcomes |
| `"mean_difference"` | Mean difference | Continuous outcomes |
| `"standardized_mean_difference"` | SMD (Cohen's d, Hedges' g) | Different scales |
| `"rate_ratio"` | Rate ratio | Count data |
| `"risk_difference"` | Absolute risk difference | Binary outcomes |
| `"correlation"` | Correlation coefficient | Association studies |
| `"unknown"` | Cannot be classified | Incomplete reporting |

### 8.3 Statistical significance vs clinical significance

Record the p-value but do not equate statistical significance with
clinical importance. A small but statistically significant effect may
be clinically irrelevant. Record the minimal clinically important
difference (MCID) for the outcome when known, in `extractor_notes`.

### 8.4 Absolute effect requirement

When the source reports only a relative effect, calculate the absolute
effect from the reported event rates if available. Label the calculated
value as `"reviewer_calculation"` in the `effect_estimate_source` field.
If event rates are not available, record `absolute_effect` as `null`
and note the limitation.

---

## 9. Safety and adverse event fields

### 9.1 Required fields

| Field | Type | Description | Sentinel if missing |
|-------|------|-------------|---------------------|
| `adverse_events_reported` | boolean or `null` | Whether the source reports safety data | `null` |
| `total_ae_count` | integer or `null` | Total adverse events reported | `null` |
| `serious_ae_count` | integer or `null` | Serious adverse events | `null` |
| `ae_leading_to_discontinuation` | integer or `null` | AEs causing treatment discontinuation | `null` |
| `death_count` | integer or `null` | Deaths during the study | `null` |
| `ae_summary_text` | string | Narrative summary of adverse events | `"unknown"` |
| `safety_conclusion` | string | Source's own safety conclusion | `"unknown"` |

### 9.2 Absence of reported events

**The absence of reported adverse events is not evidence of safety.**
When a source does not report safety data, set `adverse_events_reported`
to `false` and note the absence. Do not write "no safety concerns" or
"well tolerated" unless those are the source's own reported words.

### 9.3 Common terminology

Record adverse events using the source's own terminology. Optionally
map to MedDRA preferred terms in a separate field (`ae_meddra_term`)
but preserve the original wording.

---

## 10. Bias and quality fields

### 10.1 Required fields

| Field | Type | Description | Sentinel if missing |
|-------|------|-------------|---------------------|
| `risk_of_bias_judgment` | string | Overall risk-of-bias assessment | `"unknown"` |
| `risk_of_bias_tool` | string | Tool used for assessment | `"not_assessed"` |
| `funding_source` | string | Stated funding source | `"unknown"` |
| `funding_type` | string | Industry, government, non-profit, none, mixed | `"unknown"` |
| `conflicts_of_interest` | string | Author COI declarations | `"unknown"` |
| `study_limitations` | string | Limitations stated by the authors | `"unknown"` |
| `reviewer_limitations` | string | Additional limitations identified by the reviewer | `""` |

### 10.2 Reference to study-design-appraisal.md

For detailed risk-of-bias criteria and appraisal tools by study design,
see study-design-appraisal.md. This section records the resulting
judgments. The appraisal methodology is defined in that reference.

### 10.3 Funding and COI recording

Record the funding source and conflicts of interest exactly as stated.
Do not infer COI from the absence of a disclosure statement. When no
COI statement exists, record `"not_stated"` for `conflicts_of_interest`.

---

## 11. Extractor and provenance fields

### 11.1 Required fields

| Field | Type | Description |
|-------|------|-------------|
| `extraction_date` | string | ISO 8601 date of extraction |
| `extractor_id` | string | Identifier for the person or process performing extraction |
| `extraction_method` | string | How the extraction was performed: manual, automated, mixed |
| `extraction_source_type` | string | Full text, abstract only, summary, second-hand citation |
| `extractor_notes` | string | Free-text notes by the extractor |

### 11.2 Extraction source type rule

When `extraction_source_type` is `"abstract_only"`, the extraction
inherits all limitations of abstract-only evidence. Do not present
abstract-only extractions alongside full-text extractions without
explicitly flagging the source of each value.

### 11.3 Second-hand citations

A second-hand citation occurs when the review cites a study based on
another review or meta-analysis rather than reading the original
publication. Record the intermediate source in `secondary_source_id`.
Second-hand citations carry additional uncertainty and must be flagged
in any synthesis.

---

## 12. Field format rules

### 12.1 Numeric precision

| Quantity | Precision | Example |
|----------|-----------|---------|
| Effect estimates (RR, OR, HR) | 2 decimal places | `1.45` |
| Confidence interval bounds | 2 decimal places | `0.92` |
| P-values | 3 decimal places or exact | `0.042` or `<0.001` |
| Sample sizes | Integer | `318` |
| Percentages | 1 decimal place | `62.3` |
| Mean age | 1 decimal place | `58.4` |
| Dose values | 2 decimal places | `500.00` |

### 12.2 String conventions

Preserve the source language for extracted text fields. Use UTF-8.
Do not translate extracted text during extraction. Translation belongs
in the synthesis phase, not the extraction phase.

### 12.3 Date format

All dates use ISO 8601: `YYYY-MM-DD`. Partial dates (`"2024"` or
`"2024-06"`) are permitted when the source does not provide the full
date.

---

## 13. Sentinel value rules

### 13.1 Sentinel definitions

| Sentinel | Meaning | When to use |
|----------|---------|-------------|
| `"unknown"` | Value exists but is not reported in the source | The source should have this information but does not provide it |
| `"not_applicable"` | The field does not apply to this study or context | The study design or scope makes this field irrelevant |
| `"not_stated"` | The source is silent on this point | Use for declarations that should be present but are absent (e.g., COI) |
| `"not_assessed"` | The reviewer has not yet assessed this field | Use when appraisal is deferred or pending |
| `null` | No value is expected or the field is empty | Use only for truly optional fields where absence is meaningful |

### 13.2 Never use `null` where a sentinel applies

The schema convention for this skill's schemas uses `"unknown"` and
`"not_applicable"` as string sentinels. Numeric fields use `null` for
missing values when the numeric type cannot hold a string sentinel.

### 13.3 Distinguish `unknown` from `not_stated`

- `"unknown"`: the source reports on the topic but the specific
  value cannot be determined (e.g., a dose range is given but the
  exact dose per arm is unclear).
- `"not_stated"`: the source is entirely silent on the topic
  (e.g., no COI disclosure exists anywhere in the publication).

---

## 14. Forbidden extractions

### 14.1 Missing data prohibition

**Never invent missing data.** When a field value is not present in
the source, record the appropriate sentinel. Do not estimate, infer,
or back-calculate missing values unless the calculation is derived
from other values in the same source and the derivation is documented.

### 14.2 Dose inference prohibition

**Never infer dose from product name, brand name, or product
category.** A product named "500 mg Formula" in a study does not
guarantee the dose tested was 500 mg. Extract the dose only from
the study methods section or official product documentation cited
by the study.

### 14.3 Study design reclassification prohibition

**Never reclassify a study design based on the reviewer's
interpretation.** If the source labels a study as a "randomized
trial" but describes no randomization procedure, extract the source's
label and record the discrepancy in `extractor_notes`. Do not silently
reclassify.

### 14.4 Outcome redefinition prohibition

**Never redefine an outcome to better match the review question.**
The extraction must record the outcome as defined and measured in the
source. A mismatch between source outcome and review question outcome
is an applicability finding, not an extraction error.

### 14.5 P-value fabrication prohibition

**Never estimate or fabricate a p-value.** If the source does not
report a p-value, set `p_value` to `null`. Do not calculate a p-value
from the confidence interval, event counts, or other data unless the
calculation is explicitly labeled as a reviewer calculation and the
method is documented.

### 14.6 Abstract-only misrepresentation prohibition

**Never represent an abstract-only extraction as a full-text
verified source.** Set `extraction_source_type` to `"abstract_only"`
and flag the record in any downstream synthesis. Abstracts omit
methods detail, full results, and limitations that may alter the
conclusion.

