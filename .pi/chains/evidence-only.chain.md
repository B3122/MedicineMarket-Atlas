---
name: evidence-only
description: Conduct a focused clinical, pharmacological, safety, or commercial-claim evidence review without a full market analysis.
---

## task-planner
phase: Planning
label: Define evidence-review question
as: plan
output: 01-evidence-plan.md
outputMode: file-only
skills: evidence-appraisal
progress: true

Read {task} and the relevant project brief.

Transform the request into a focused evidence-review plan.

Define:

- exact question;
- target product, ingredient, intervention, or claim;
- target population;
- intervention, formulation, dose, and route;
- comparator where relevant;
- target outcomes;
- safety outcomes;
- eligible study designs;
- jurisdiction where regulatory evidence is relevant;
- date and language limits;
- inclusion and exclusion criteria;
- required databases or official sources;
- expected output structure;
- unresolved scope questions.

Use PICO, PECO, or another appropriate framework.

If the request concerns a commercial product, explicitly separate:

1. evidence for the ingredient or intervention;
2. evidence for the tested formulation and dose;
3. evidence directly applicable to the finished commercial product.

Do not retrieve evidence in this step.

## academic-researcher
phase: Evidence retrieval
label: Retrieve and appraise academic evidence
as: academic
reads: 01-evidence-plan.md
output: 02-academic-evidence.md
outputMode: file-only
skills: evidence-appraisal
progress: true

Execute the academic portion of 01-evidence-plan.md.

Prioritize the highest available level of evidence while preserving relevant
negative, neutral, and conflicting findings.

For each included source extract:

- complete citation;
- DOI, PMID, trial identifier, or official URL;
- publication type and study design;
- country and setting;
- population and sample size;
- intervention, formulation, dose, and route;
- comparator;
- duration;
- outcome definitions;
- quantitative results and uncertainty;
- adverse events;
- funding and conflicts where reported;
- risk-of-bias concerns;
- important limitations;
- directness to the target question;
- reason for inclusion.

Maintain a list of excluded or unusable pivotal sources and explain why they
could not support the review.

Do not cite a search snippet as though the source itself was inspected.
Do not invent unavailable quantitative results.

## regulatory-researcher
phase: Regulatory evidence
label: Retrieve official regulatory and guideline information
as: regulatory
reads: 01-evidence-plan.md
output: 03-regulatory-and-guideline-evidence.md
outputMode: file-only
progress: true

Retrieve relevant official regulatory, labeling, guideline, or public-health
information for the jurisdiction defined in 01-evidence-plan.md.

Document:

- issuing authority or organization;
- document title;
- publication or update date;
- jurisdiction;
- product category or indication;
- permitted, approved, or recommended wording;
- contraindications, warnings, and restrictions;
- source URL;
- retrieval date;
- applicability and limitations.

Prioritize official primary sources.

Do not infer that absence of an approved claim proves biological inefficacy.
Do not treat a professional guideline recommendation as equivalent to product
authorization.

## claim-verifier
phase: Synthesis
label: Determine support for the target claim or question
as: assessment
reads: 01-evidence-plan.md+02-academic-evidence.md+03-regulatory-and-guideline-evidence.md
output: 04-evidence-assessment.md
outputMode: file-only
skills: evidence-appraisal
progress: true

Synthesize the academic, guideline, and regulatory evidence.

For each target claim or conclusion assess:

- population match;
- intervention and ingredient match;
- formulation match;
- dose match;
- route match;
- duration match;
- outcome match;
- effect magnitude;
- consistency;
- risk of bias;
- directness;
- precision;
- publication-bias concerns;
- regulatory compatibility.

Classify support as:

- directly supported;
- partially supported;
- indirectly supported;
- unsupported;
- contradicted;
- cannot determine.

State whether the available evidence permits:

- a causal conclusion;
- an ingredient-level conclusion only;
- extrapolation to the finished product;
- extrapolation to the requested population;
- a quantitative efficacy statement;
- a safety conclusion.

Provide a concise evidence-certainty judgment and the reasons for it.

## report-writer
phase: Reporting
label: Draft evidence-review report
as: report
reads: 01-evidence-plan.md+02-academic-evidence.md+03-regulatory-and-guideline-evidence.md+04-evidence-assessment.md
output: 05-evidence-review.md
outputMode: file-only
skills: evidence-appraisal+report-generation
progress: true

Write a focused evidence-review report using only the supplied artifacts.

Required sections:

1. Review question
2. Methods and source scope
3. Evidence map
4. Findings by outcome
5. Safety findings
6. Applicability to the target product or claim
7. Regulatory and guideline context
8. Certainty and limitations
9. Conclusions
10. References

Do not present the review as a formal systematic review unless its search,
screening, extraction, and risk-of-bias methods meet that standard.

Use calibrated language corresponding to evidence strength.

## report-auditor
phase: Audit
label: Audit evidence interpretation and citations
as: audit
reads: 01-evidence-plan.md+02-academic-evidence.md+03-regulatory-and-guideline-evidence.md+04-evidence-assessment.md+05-evidence-review.md
output: 06-evidence-review-audit.md
outputMode: file-only
skills: evidence-appraisal+report-generation
progress: true

Audit 05-evidence-review.md against all evidence artifacts.

Check:

- citation existence and identity;
- whether cited sources support the associated statements;
- population, dose, formulation, route, and outcome matching;
- causal overstatement;
- ingredient-to-product extrapolation;
- animal-to-human or in-vitro-to-clinical extrapolation;
- effect-size accuracy;
- selective omission of negative evidence;
- confusion between statistical and clinical significance;
- certainty-language calibration;
- regulatory overstatement;
- missing safety qualifications;
- whether the methods are mislabeled as systematic.

Classify findings as critical, major, or minor.

Return an explicit PASS, PASS WITH CORRECTIONS, or FAIL decision.
