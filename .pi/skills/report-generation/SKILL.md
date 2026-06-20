---
name: report-generation
description: Converts validated pharmaceutical or health-product market, competitor, evidence, regulatory, and claim-assessment artifacts into traceable professional reports. Use when drafting, revising, structuring, or auditing research reports from saved project evidence.
compatibility: Works with Markdown artifacts. Optional export scripts may require Python 3.11 or later and document-generation packages.
---

# Report Generation

Use this skill only after the relevant research and normalization artifacts
exist.

The report writer must not silently replace missing research with model
knowledge.

## Inputs

Identify and read the available project artifacts:

- project brief;
- research plan;
- source inventory;
- normalized product records;
- market findings;
- competitor analysis;
- evidence tables;
- regulatory findings;
- claim assessments;
- unresolved conflicts;
- reviewer calculations;
- audit requirements;
- report template.

Before writing, create an input inventory identifying:

- artifact path;
- artifact role;
- status;
- date;
- known limitations;
- whether it is approved for reporting.

Do not use superseded or unapproved artifacts unless explicitly instructed.

## Reporting modes

Select the mode requested by the project.

### Quick competitor review

Emphasize:

- target product definition;
- competitor inclusion logic;
- normalized comparison;
- price and dose;
- channel and positioning;
- main differentiators;
- limitations.

### Full market review

Emphasize:

- method;
- market scope;
- product landscape;
- platform differences;
- competitor segmentation;
- price, dose, and channel analysis;
- consumer narratives;
- evidence and regulatory context;
- strategic interpretation;
- limitations.

### Evidence review

Emphasize:

- question;
- search and eligibility;
- evidence map;
- outcome findings;
- safety;
- applicability;
- certainty;
- regulatory or guideline context;
- limitations.

### Claim-substantiation report

Emphasize:

- exact claim;
- product specification;
- evidence mapping;
- population, formulation, dose, and outcome match;
- claim-support classification;
- regulatory risks;
- qualified alternative wording.

## Report architecture

Unless a project template overrides it, use:

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

Use sections only when relevant.

## Executive summary

The executive summary should state:

- what was reviewed;
- market and time scope;
- main findings;
- most important evidence limitations;
- practical conclusion;
- unresolved critical issue, if any.

Do not introduce information absent from the body.

Do not use promotional language.

## Methods

Describe what was actually done.

Include as applicable:

- platforms or databases;
- collection or search dates;
- geographic scope;
- competitor inclusion criteria;
- product normalization rules;
- price normalization basis;
- evidence eligibility criteria;
- regulatory jurisdictions;
- major access limitations;
- whether the work was rapid, focused, narrative, or systematic.

Do not call a review systematic merely because it uses several databases.

## Source attribution

Every externally verifiable statement should be traceable.

At minimum, cite or identify the source for:

- product composition;
- dose;
- formulation;
- package quantity;
- price;
- promotion;
- sales or review metrics;
- regulatory status;
- study design;
- sample size;
- effect estimate;
- safety result;
- guideline recommendation;
- commercial claim.

Use source IDs consistently where the project uses a source inventory.

Do not cite a source that does not support the associated statement.

## Handling platform differences

When sources differ:

1. verify whether records describe the same product version;
2. compare collection dates;
3. compare seller and market;
4. distinguish label price, ordinary price, promotion price, membership price,
   livestream price, and bundle price;
5. distinguish official product information from seller-created wording;
6. preserve both values when the conflict cannot be resolved;
7. explain the likely reason without presenting speculation as fact.

## Quantitative reporting

For every reviewer-derived value state:

- formula;
- numerator;
- denominator;
- unit;
- currency;
- collection date;
- price type;
- assumptions;
- rounding rule.

Examples include:

- price per capsule;
- price per gram;
- price per 100 mg active ingredient;
- estimated daily cost;
- relative price difference;
- dose-normalized comparison.

Never calculate with incompatible package or dose definitions.

## Tables

Use tables for structured comparison, not dense narrative.

A competitor table should normally include:

- normalized product name;
- brand;
- formulation;
- per-unit dose;
- package size;
- observed price and price type;
- normalized price;
- declared daily use;
- estimated daily cost;
- principal claims;
- channel;
- source date;
- key caveat.

An evidence table should normally include:

- source;
- design;
- population;
- intervention and dose;
- comparator;
- duration;
- outcome;
- result;
- limitations;
- applicability.

Keep raw source quotations outside summary tables unless wording itself is
being evaluated.

## Distinguish statement types

Use explicit language to distinguish:

### Verified fact

“According to the official label...”

### Platform observation

“At the time of collection, the listing displayed...”

### Commercial claim

“The seller stated that the product...”

### Consumer narrative

“Frequently observed user discussions concerned...”

### Scientific finding

“In a randomized trial of..., the investigators reported...”

### Regulatory finding

“The authority classifies the product as...”

### Analyst interpretation

“This pattern may indicate...”

Do not collapse these categories.

## Scientific language

Use cautious wording consistent with evidence certainty.

Do not:

- imply causality from observational data;
- imply clinical efficacy from mechanistic data alone;
- imply finished-product efficacy from ingredient evidence alone;
- imply absence of risk from absence of reported events;
- equate statistical significance with meaningful benefit;
- omit relevant population and duration limits.

## Commercial and strategic interpretation

Recommendations must follow from documented findings.

Separate:

- observed market pattern;
- interpretation;
- business implication;
- recommendation;
- uncertainty.

Do not fabricate a market opportunity because the report format expects one.

When evidence is weak, recommend further verification rather than generating
false certainty.

## Limitations

Consider:

- dynamic prices and promotions;
- inaccessible pages;
- platform login requirements;
- nontransparent sales metrics;
- incomplete product identity;
- seller-generated descriptions;
- temporal mismatch;
- regional version differences;
- publication access;
- incomplete literature coverage;
- language restrictions;
- lack of direct finished-product evidence;
- absence of independent market-volume data;
- automated extraction errors.

Limitations should affect the strength of conclusions, not merely appear as a
generic final paragraph.

## Conclusion

The conclusion must:

- answer the research question;
- summarize only supported findings;
- identify the strength of evidence;
- distinguish market attractiveness from clinical substantiation;
- identify unresolved issues;
- avoid introducing new facts.

## Final self-check

Before saving the report verify:

- all required sections are present;
- every number is traceable;
- every table uses consistent units;
- sources are not misattributed;
- product versions are not mixed;
- commercial claims are clearly labeled;
- consumer comments are not presented as evidence;
- ingredient and finished-product evidence are distinguished;
- regulatory jurisdiction is identified;
- conflicting values are disclosed;
- conclusions match evidence strength;
- methods match actual execution;
- limitations are specific;
- no placeholder remains.

## Audit preparation

Create a report that an independent auditor can verify without reconstructing
the entire project from chat history.

Retain:

- source IDs;
- artifact filenames;
- calculation notes;
- unresolved conflict IDs;
- collection dates;
- version information.

## Supporting references

Read as needed:

- `references/report-structure-guide.md`
- `references/source-attribution-style.md`
- `references/table-specifications.md`
- `references/quantitative-reporting-rules.md`
- `references/calibrated-language.md`
- `references/audit-checklist.md`

## Helper scripts

Optional scripts may include:

- `scripts/check-report-placeholders.py`
- `scripts/check-source-ids.py`
- `scripts/check-numeric-traceability.py`
- `scripts/render-report.py`
- `scripts/export-docx.py`

Scripts may validate or render content, but must not create unsupported facts.
