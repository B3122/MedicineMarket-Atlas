---
name: quick-competitor-review
description: Rapidly compare a target pharmaceutical or health product with a small, explicitly defined competitor set using available market sources, normalized product identities, and an independently audited concise report.
---

## task-planner
phase: Planning
label: Define rapid competitor-review scope
as: plan
output: 01-quick-review-plan.md
outputMode: file-only
skills: product-market-research
progress: true

Read {task} together with the relevant project brief and configuration.

Create a focused competitor-review plan suitable for completion without a
full systematic evidence review.

The plan must define:

- target product and product version;
- target market and jurisdiction;
- competitor inclusion and exclusion criteria;
- maximum number of competitors;
- platforms or supplied source files to inspect;
- fields required for comparison;
- price normalization basis;
- report structure;
- missing information;
- human decisions required before research.

Default to no more than five competitors unless the project brief explicitly
requests more.

Do not perform market research in this step.
Do not silently resolve material ambiguity.

## market-researcher
phase: Research
label: Collect target and competitor market information
as: market
reads: 01-quick-review-plan.md
output: 02-quick-market-findings.md
outputMode: file-only
skills: product-market-research
progress: true

Execute the approved rapid review plan in 01-quick-review-plan.md.

Collect only the market information required for the focused comparison.

For every source retain:

- platform or publisher;
- seller where applicable;
- page title;
- URL or local source path;
- collection date;
- exact product version;
- original displayed value;
- normalized interpretation;
- uncertainty or access limitation.

Do not treat review counts or popularity labels as exact sales.
Do not merge package sizes, formulations, doses, or regional versions.

Separate verified product facts, seller claims, platform metrics, promotions,
consumer narratives, and analyst interpretation.

## product-normalizer
phase: Normalization
label: Resolve products, versions, packages, and duplicate listings
as: normalized
reads: 01-quick-review-plan.md+02-quick-market-findings.md
output: 03-quick-normalized-products.md
outputMode: file-only
progress: true

Normalize all target and competitor records.

For every pair of potentially related records classify the relationship as:

- same listing;
- same SKU from another seller;
- same core product with a different package quantity;
- different dose;
- different formulation;
- different regional version;
- seller-created bundle;
- possible duplicate requiring human confirmation;
- distinct product.

Document the evidence and confidence supporting each decision.

Do not combine uncertain records.

## competitor-analyst
phase: Analysis
label: Compare competitors using normalized units
as: analysis
reads: 01-quick-review-plan.md+02-quick-market-findings.md+03-quick-normalized-products.md
output: 04-quick-competitor-analysis.md
outputMode: file-only
skills: product-market-research
progress: true

Build the focused competitor comparison using only normalized records.

Where data permit, calculate:

- current observed price;
- price per package unit;
- price per gram or milligram of relevant active ingredient;
- estimated daily cost under the declared usage directions;
- dose and formulation differences;
- channel coverage;
- principal commercial claims;
- intended user group;
- positioning and differentiation.

State every calculation formula and assumption.

Do not compare promotional, membership, livestream, and ordinary retail prices
as though they are the same price type.

Identify:

- direct competitors;
- premium and budget positions;
- apparent product differentiation;
- important data gaps;
- comparisons that cannot be made reliably.

## report-writer
phase: Reporting
label: Draft concise competitor-review report
as: report
reads: 01-quick-review-plan.md+02-quick-market-findings.md+03-quick-normalized-products.md+04-quick-competitor-analysis.md
output: 05-quick-competitor-review.md
outputMode: file-only
skills: report-generation
progress: true

Write a concise, decision-oriented competitor-review report.

Use only the supplied artifacts.

Required sections:

1. Executive summary
2. Scope and method
3. Target product definition
4. Competitor selection
5. Normalized comparison table
6. Pricing and dose comparison
7. Positioning, claims, and channel differences
8. Opportunities and limitations
9. Source inventory

Clearly distinguish facts, commercial claims, consumer narratives, and
analyst interpretation.

Do not introduce new research or unsupported recommendations.

## report-auditor
phase: Audit
label: Audit competitor report
as: audit
reads: 02-quick-market-findings.md+03-quick-normalized-products.md+04-quick-competitor-analysis.md+05-quick-competitor-review.md
output: 06-quick-review-audit.md
outputMode: file-only
skills: evidence-appraisal+report-generation
progress: true

Audit 05-quick-competitor-review.md against the underlying artifacts.

Check:

- product and SKU identity;
- price type and collection date;
- dose and package values;
- calculation accuracy;
- claim attribution;
- unsupported sales statements;
- inappropriate comparison of nonequivalent products;
- missing conflicts;
- unsupported recommendations;
- missing limitations.

Classify findings as critical, major, or minor.

Return an explicit PASS, PASS WITH CORRECTIONS, or FAIL decision.
A report with unresolved product-identity or material numerical errors must fail.
