---
name: evidence-appraisal
description: Retrieves, extracts, compares, and appraises clinical, pharmacological, safety, guideline, and regulatory evidence for drugs, health products, ingredients, interventions, and commercial claims. Use when evaluating efficacy, safety, dose relevance, evidence certainty, or whether published evidence supports a product claim.
compatibility: Requires access to supplied documents or web-research tools. Structured extraction scripts may require Python 3.11 or later.
---

# Evidence Appraisal

Use this skill for focused evidence reviews, claim substantiation,
clinical-evidence summaries, safety reviews, and ingredient-to-product
applicability assessments.

This skill does not convert a rapid narrative search into a formal systematic
review. Describe the method according to what was actually performed.

## Core principles

1. Define the question before searching.
2. Preserve the distinction between retrieval, extraction, appraisal,
   synthesis, and report writing.
3. Prefer primary and authoritative sources.
4. Include negative and inconclusive evidence when relevant.
5. Assess directness to the target product, dose, formulation, population,
   and outcome.
6. Avoid claim inflation.
7. Retain identifiers and source provenance.
8. Mark inaccessible or unverified material clearly.
9. Never invent missing data.
10. Separate scientific evidence from regulatory permission.

## Step 1: Define the question

Select the most suitable framework.

### PICO

Use for intervention efficacy or safety:

- Population
- Intervention
- Comparator
- Outcome

### PECO

Use for exposure or observational questions:

- Population
- Exposure
- Comparator
- Outcome

### Claim-substantiation framework

Use for a commercial claim:

- exact original claim;
- product or ingredient;
- target population;
- implied intervention;
- claimed outcome;
- claimed magnitude;
- claimed speed or duration;
- implied certainty;
- product dose and formulation;
- relevant jurisdiction.

Record unresolved ambiguities before searching.

## Step 2: Define eligibility

Document:

- population criteria;
- intervention or exposure;
- formulation;
- dose and route;
- comparator;
- outcomes;
- study designs;
- date limits;
- language limits;
- publication status;
- jurisdiction;
- exclusion criteria.

Do not silently broaden the question to obtain more positive evidence.

## Step 3: Select source types

Prioritize sources according to the question.

### Clinical efficacy and safety

1. current clinical guidelines;
2. regulatory assessments and official labels;
3. systematic reviews and meta-analyses;
4. randomized controlled trials;
5. prospective observational studies;
6. retrospective observational studies;
7. case-control studies;
8. case series and reports;
9. mechanistic human studies;
10. animal and in-vitro studies.

### Drug or product status

1. official regulator databases;
2. official product labels or package inserts;
3. government or public-health sources;
4. manufacturer regulatory documents;
5. commercial pages only as secondary evidence.

### Literature discovery

Prefer databases or indexes that provide stable identifiers and sufficient
metadata. Examples may include PubMed, Europe PMC, Crossref, trial registries,
official guideline repositories, and regulator websites.

Do not assume that every source returned by a general search engine has been
peer reviewed.

## Step 4: Build search concepts

Create concept blocks for:

- intervention, ingredient, drug, product, and synonyms;
- population or disease;
- outcome or claim;
- study design where appropriate;
- safety terms where appropriate.

Combine synonyms with OR and concept groups with AND.

Maintain a search log containing:

- source searched;
- exact query;
- date searched;
- filters;
- result count when available;
- changes made to the query;
- known access limitations.

For a rapid review, state that the search was focused rather than exhaustive.

## Step 5: Screen sources

Evaluate title and abstract relevance first, then inspect the full source when
the conclusion depends on details not available in the abstract.

Record at minimum:

- included;
- excluded;
- awaiting full text;
- duplicate;
- unusable because identity could not be confirmed.

For pivotal exclusions, record the reason.

Do not exclude a study merely because its result is negative.

## Step 6: Extract study data

For each included study extract:

- source ID;
- complete citation;
- DOI, PMID, trial registration, or official URL;
- publication year;
- country and setting;
- study design;
- eligibility criteria;
- population;
- sample size;
- baseline characteristics;
- intervention;
- formulation;
- dose;
- route;
- frequency;
- comparator;
- duration;
- outcome definitions;
- analysis population;
- effect estimate;
- confidence interval or uncertainty;
- p-value where relevant;
- absolute result where available;
- adverse events;
- attrition;
- funding;
- conflicts of interest;
- study limitations;
- extractor notes.

Use `references/evidence-extraction-fields.md` for the detailed field guide.

## Step 7: Assess internal validity

Assess risk of bias according to study design.

### Randomized trials

Consider:

- randomization;
- allocation concealment;
- blinding;
- missing outcome data;
- adherence;
- selective reporting;
- outcome measurement;
- analysis approach;
- early stopping;
- baseline imbalance.

### Observational studies

Consider:

- selection bias;
- exposure measurement;
- outcome measurement;
- confounding;
- immortal-time bias;
- reverse causation;
- missing data;
- selective reporting;
- model specification;
- generalizability.

### Systematic reviews

Consider:

- protocol or prespecification;
- search coverage;
- study selection;
- duplicate processes;
- risk-of-bias assessment;
- appropriateness of pooling;
- heterogeneity;
- publication bias;
- certainty assessment;
- recency.

### Case reports and mechanistic evidence

Treat as hypothesis-generating unless the question specifically concerns
signal detection, rare events, plausibility, or mechanism.

Do not produce a formal named-tool score unless the necessary information has
actually been assessed.

## Step 8: Assess applicability

Evaluate the following separately:

- population match;
- disease or health-state match;
- ingredient match;
- chemical form match;
- formulation match;
- dose match;
- route match;
- exposure duration match;
- comparator match;
- outcome match;
- product quality or bioavailability match;
- jurisdictional relevance.

Use the following applicability categories:

- direct;
- mostly direct;
- partially indirect;
- substantially indirect;
- not applicable;
- cannot determine.

An ingredient-level study is not automatically direct evidence for a
commercial product.

## Step 9: Assess certainty

Assess the body of evidence rather than relying on one positive study.

Consider:

- risk of bias;
- inconsistency;
- indirectness;
- imprecision;
- publication bias;
- magnitude;
- dose-response;
- residual confounding;
- replication;
- relevance of outcome.

Use one of the following verbal levels unless a formal framework was
prospectively applied:

- high confidence;
- moderate confidence;
- low confidence;
- very low confidence;
- insufficient evidence.

Explain the reasons.

Do not label an informal judgment as a formal GRADE assessment.

## Step 10: Evaluate commercial claims

Preserve the exact original wording.

For each claim examine:

1. Is the claimed population represented?
2. Is the same ingredient or intervention studied?
3. Is the formulation comparable?
4. Is the product dose comparable?
5. Is the route comparable?
6. Is the claimed outcome directly measured?
7. Is the claimed magnitude supported?
8. Is the claimed onset or duration supported?
9. Is the causal language justified?
10. Are safety qualifications omitted?
11. Is the claim compatible with applicable regulation?
12. Does the claim improperly imply treatment, prevention, or cure?

Classify support as:

- directly supported;
- partially supported;
- indirectly supported;
- unsupported;
- contradicted;
- cannot determine.

### Directly supported

Use only when population, intervention, formulation, dose, outcome, and
claim wording are sufficiently aligned and the evidence is credible.

### Partially supported

Use when the general direction is supported but the commercial wording,
population, magnitude, dose, speed, or certainty is broader than the evidence.

### Indirectly supported

Use when support is mechanistic, ingredient-level, based on a materially
different population or formulation, or otherwise not directly transferable.

### Unsupported

Use when relevant evidence does not substantiate the claim or the claim
depends on assumptions not demonstrated.

### Contradicted

Use when credible evidence materially conflicts with the claim.

### Cannot determine

Use when essential information or source access is missing.

## Step 11: Distinguish finding types

Label statements as one of:

- source-reported result;
- reviewer calculation;
- reviewer interpretation;
- regulatory statement;
- commercial claim;
- unresolved conflict.

Never merge these categories into a single apparent fact.

## Step 12: Write calibrated conclusions

Match language to certainty.

Prefer:

- “was associated with” for observational evidence;
- “the trial reported” for a single trial;
- “may improve” for limited or uncertain evidence;
- “evidence suggests” for a consistent but imperfect body of evidence;
- “evidence is insufficient” when conclusions cannot be supported;
- “has not been established” when product-level applicability is absent.

Avoid:

- “proves”;
- “guarantees”;
- “works” without qualification;
- “safe” without population and duration limits;
- “clinically effective” based only on statistical significance;
- “no risk” based on absence of reported events.

## Required outputs

A complete evidence artifact should contain:

1. review question;
2. method and search scope;
3. eligibility criteria;
4. search log;
5. source inventory;
6. evidence table;
7. risk-of-bias observations;
8. applicability assessment;
9. synthesis by outcome;
10. safety synthesis;
11. claim-support assessment where relevant;
12. certainty judgment;
13. limitations;
14. references;
15. unresolved questions.

## Quality checks

Before completion verify:

- every pivotal citation exists;
- identifiers match the cited title;
- quantitative values match the source;
- no abstract-only source is represented as full-text verified;
- negative evidence has not been omitted;
- study design has been classified correctly;
- population and dose differences are disclosed;
- ingredient evidence has not been overstated as product evidence;
- regulatory and scientific conclusions remain distinct;
- certainty wording is calibrated;
- limitations are explicit.

## Supporting references

Read as needed:

- `references/evidence-extraction-fields.md`
- `references/study-design-appraisal.md`
- `references/claim-support-rules.md`
- `references/evidence-language-guide.md`
- `references/search-log-template.md`

## Helper scripts

Use scripts only on copies or generated artifacts:

- `scripts/validate-evidence-records.py`
- `scripts/deduplicate-citations.py`
- `scripts/check-identifiers.py`
- `scripts/build-evidence-table.py`

Do not allow helper scripts to invent missing bibliographic or study data.
