# Calibrated Language

Rules for matching language to evidence certainty and distinguishing statement
types in pharmaceutical and health-product market research reports.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: evidence-appraisal SKILL.md Step 12 (calibrated conclusions,
certainty levels), evidence-appraisal references/evidence-language-guide.md
(certainty-to-language mapping), SKILL.md lines 254-285 (statement types),
quantitative-reporting-rules.md (calculation labeling).

---

## Table of Contents

1. [Certainty-to-language mapping](#1-certainty-to-language-mapping)
2. [Statement type labeling](#2-statement-type-labeling)
3. [Forbidden phrases](#3-forbidden-phrases)
4. [Causal language rules](#4-causal-language-rules)
5. [Safety language rules](#5-safety-language-rules)
6. [Scientific language rules](#6-scientific-language-rules)
7. [Commercial interpretation language](#7-commercial-interpretation-language)
8. [Cross-reporting consistency](#8-cross-reporting-consistency)

---

## 1. Certainty-to-language mapping

### 1.1 Evidence support levels

Match language to the claim-support classification from evidence appraisal.
Use the preferred phrasing for each level. Alternative phrasing is acceptable
only when it communicates the same degree of certainty.

| Evidence support level | Preferred phrasing | Alternative phrasing |
|------------------------|--------------------|----------------------|
| Directly supported | "was associated with" (observational) / "the trial reported" (RCT) / "reduced" (RCT, causal justified) | "demonstrated", "showed" |
| Partially supported | "may be associated with" / "may improve" | "suggests a possible effect", "preliminary evidence indicates" |
| Indirectly supported | "has been linked to in related populations" / "mechanistic evidence suggests" | "indirect evidence from [population/mechanism] indicates" |
| Unsupported | "no evidence was found to support" / "has not been established" | "evidence does not substantiate", "remains unsubstantiated" |
| Contradicted | "evidence contradicts the claim that" / "evidence does not support the claim that" | "the available evidence is inconsistent with", "findings conflict with" |
| Cannot determine | "evidence is insufficient to determine" / "available evidence does not permit a conclusion" | "further research is needed to determine" |

### 1.2 Confidence levels

For synthesis-level judgments about a body of evidence:

| Confidence level | Language guidance | Example |
|------------------|-------------------|---------|
| High confidence | Use direct, unhedged language | "The evidence consistently shows..." |
| Moderate confidence | Use "suggests", "indicates", "likely" | "The evidence suggests..." |
| Low confidence | Use "may", "might", "limited evidence" | "Limited evidence suggests a possible..." |
| Very low confidence | Use "very uncertain", "insufficient to conclude" | "The evidence is very uncertain regarding..." |
| Insufficient evidence | Use "no conclusion can be drawn" | "The available evidence does not permit a conclusion about..." |

### 1.3 Evidence type modifiers

Adjust phrasing based on study design:

| Study design | Appropriate verbs |
|--------------|-------------------|
| Randomized controlled trial | "reduced", "improved", "increased" (if statistically significant and clinically meaningful) |
| Observational study | "was associated with", "was linked to", "correlated with" |
| Systematic review / meta-analysis | "pooled results showed", "the body of evidence indicates" |
| Case series / report | "has been described in", "case reports have noted" |
| Mechanistic / in vitro | "provides a mechanistic basis for", "is consistent with the hypothesis that" |
| Animal study | "in animal models", "preclinical data indicate" |

### 1.4 Uncertainty qualifiers

**Never omit uncertainty qualifiers when they are warranted by the evidence.**
Every statement about efficacy, safety, or comparative advantage must include
the appropriate level of uncertainty based on the evidence body.

Required qualifiers by evidence strength:

- Single small trial: "in a single trial of [N] participants"
- Short duration: "over [X] weeks", "short-term data suggest"
- Surrogate outcome: "improved [surrogate marker], but the effect on [clinical outcome] is unknown"
- Narrow population: "in [specific population], but generalizability is uncertain"
- Indirect comparison: "no direct comparative evidence is available"

---

## 2. Statement type labeling

### 2.1 Statement type taxonomy

Every significant statement in the report body must be classified into one of
seven statement types. Use explicit language to distinguish them.

| Statement type | Label | Description | Example introductory phrase |
|----------------|-------|-------------|----------------------------|
| Verified fact | `[FACT]` | A fact confirmed by official sources (label, regulator) | "According to the official label..." |
| Platform observation | `[OBSERVATION]` | Data observed on a platform at a specific time | "At the time of collection, the listing displayed..." |
| Commercial claim | `[CLAIM]` | A claim made by the seller, manufacturer, or advertiser | "The seller stated that the product..." |
| Consumer narrative | `[NARRATIVE]` | Patterns observed in consumer-generated content | "Frequently observed user discussions concerned..." |
| Scientific finding | `[EVIDENCE]` | A finding from a published scientific study or guideline | "In a randomized trial of [N], the investigators reported..." |
| Regulatory finding | `[REGULATORY]` | A regulatory status, classification, or determination | "The authority classifies the product as..." |
| Analyst interpretation | `[INTERPRETATION]` | An inference, pattern recognition, or strategic reading | "This pattern may indicate..." |

### 2.2 Derived labels

In addition to the primary seven types, use these labels for reviewer-generated
content:

| Label | Meaning | Use when |
|-------|---------|----------|
| `[CALCULATION]` | Reviewer-derived numeric value | The value was computed from source data (daily cost, normalized price, percentage change) |
| `[OPINION]` | Reviewer judgment or recommendation | The statement expresses a strategic assessment, recommendation, or subjective evaluation not directly supported by a single source |
| `[LIMITATION]` | Acknowledged limitation | The statement identifies a constraint on the findings |

### 2.3 Label placement

Labels must be placed:

- In section headings for sections dedicated to a single type
- At the beginning of paragraphs where types are mixed
- In the margin or as a prefix for individual statements in evidence tables

### 2.4 Prohibition on type mixing

**Never collapse statement types into a single apparent fact.** A commercial
claim must not be presented as a scientific finding. An analyst interpretation
must not be presented as a verified fact. A consumer narrative must not be
presented as evidence.

If a paragraph contains statements of different types, each must be introduced
with the appropriate framing language. If this creates an awkward structure,
separate the statements into distinct paragraphs.

---

## 3. Forbidden phrases

### 3.1 Absolute prohibitions

The following words and phrases must never appear in a report unless
accompanied by the exact qualifying context that justifies them:

| Forbidden phrase | Why prohibited | Permitted only when |
|------------------|----------------|---------------------|
| **"proves"** | Implies certainty not available from any single study | Never — use "demonstrated", "showed", or "supports" |
| **"guarantees"** | Implies a warranty or unconditional outcome | Never — commercial guarantees are commercial claims, not evidence |
| **"works for everyone"** | Impossible to support for any product | Never |
| **"100% safe"** | No product is absolutely safe | Never — safety always requires population, dose, and duration limits |
| **"clinically proven"** | Implies a level of proof that requires specific context | Only when referencing a specific regulatory determination that uses this exact phrase; otherwise use "clinically studied" or "shown in clinical trials" |
| **"no side effects"** | Absence of reported events is not absence of risk | Only when a specific trial reported zero adverse events and the trial design, duration, and sample size are stated |
| **"cures"** | Implies disease eradication rarely supported | Only for products with regulatory approval as a curative treatment for the specific disease |
| **"prevents"** | Implies guaranteed prophylaxis | Only for products with regulatory approval for prevention of the specific condition, with stated efficacy |
| **"treats"** | Implies therapeutic efficacy | Only for products with regulatory approval for treatment of the specific condition |

### 3.2 Phrases requiring qualification

The following phrases may be used only when accompanied by the specified
qualification:

| Phrase | Required qualification |
|--------|----------------------|
| "effective" | State: effective for what outcome, in what population, at what dose, over what duration, based on what evidence |
| "safe" | State: safe in what population, at what dose, over what duration, based on what evidence; include known risks and adverse event rates |
| "superior to" | State: superiority in what outcome, compared to what specific comparator, based on what study, with what magnitude and confidence interval |
| "recommended by" | State: recommended by what specific body, in what guideline, at what strength of recommendation |
| "better than" | State: better in what dimension (efficacy, safety, cost, convenience), based on what evidence |

### 3.3 Promotional language prohibition

**Never use promotional language in a research report.** Replace any phrase
that reads like advertising copy:

| Promotional phrasing | Replace with |
|----------------------|--------------|
| "revolutionary" | Describe the mechanism or feature |
| "game-changing" | Quantify the difference from alternatives |
| "best-in-class" | State the specific comparative advantage with evidence |
| "all-natural" | State the specific ingredients and their sources |
| "breakthrough" | Describe the novelty and cite the supporting evidence |
| "trusted by millions" | Cite the sales data or market share, with source and date |
| "doctor-recommended" | Cite the specific recommendation, body, and evidence |

---

## 4. Causal language rules

### 4.1 Causal language hierarchy

The strength of causal language must match the strength of the evidence design:

| Evidence design | Maximum causal language |
|-----------------|------------------------|
| Multiple large RCTs with consistent results | "reduces", "improves", "increases" |
| Single RCT | "reduced" (past tense, limited to the studied population and dose) |
| Pooled analysis of RCTs | "reduces" (if homogeneous and consistent) |
| Prospective cohort | "was associated with a lower/higher rate of" |
| Case-control | "was associated with" |
| Cross-sectional | "was correlated with" |
| Ecological | "at the population level, [X] was associated with [Y]" |
| Mechanistic / in vitro | "provides a plausible mechanism by which [X] could affect [Y]" |
| Expert opinion | "experts have hypothesized that" |

### 4.2 RCT requirement for causal claims

**Never use causal language (reduces, improves, prevents, causes, leads to,
results in) without RCT evidence that directly studied the intervention, in the
same or comparable population, at a comparable dose, and measured the claimed
outcome.**

Correlation language ("associated with", "linked to", "correlated with") must
be used for all non-randomized evidence, regardless of the consistency or
strength of the association.

### 4.3 Mechanistic causal language

When evidence is mechanistic only:

- Use "may contribute to", "is consistent with a role in", "provides a
  mechanistic basis for the hypothesis that"
- **Never** use the mechanistic finding alone to imply clinical efficacy
- Always state that clinical studies of the finished product are needed

---

## 5. Safety language rules

### 5.1 Safety statement requirements

Every safety statement must include:

- The population in which safety was assessed
- The dose at which safety was assessed
- The duration of exposure
- The sample size (for study-derived safety data)
- The adverse event reporting method

### 5.2 Absence of events language

When no adverse events were reported:

- Use "no adverse events were reported" (not "no adverse events occurred")
- State the sample size, duration, and method of adverse event collection
- Add: "The study was not powered to detect rare adverse events" when
  sample size is under 1,000
- **Never** use "no risk", "risk-free", or "absolutely safe"

### 5.3 Risk comparison language

When comparing safety profiles:

- Use absolute risk differences, not relative risk alone
- State the baseline risk in the comparator group
- State the confidence interval for the risk difference
- Do not claim superior safety based on a non-significant difference

### 5.4 Long-term safety language

When long-term safety data are absent:

- State the maximum follow-up duration in the available evidence
- Add: "Long-term safety beyond [duration] has not been established"
- Do not extrapolate short-term safety to long-term use

---

## 6. Scientific language rules

### 6.1 Statistical significance

When reporting statistical results:

- Report the effect estimate with confidence interval, not just the p-value
- Distinguish statistical significance from clinical meaningfulness
- **Never** equate statistical significance with meaningful benefit: "The
  difference was statistically significant (p = 0.03) but the absolute
  difference was 0.5 percentage points"
- For non-significant results: "The difference did not reach statistical
  significance (p = 0.12), but the study may have been underpowered to detect
  a clinically meaningful effect" (if the confidence interval does not exclude
  a meaningful effect)

### 6.2 Ingredient vs product evidence

When evidence is for an ingredient rather than the finished product:

- State: "Evidence for [ingredient] includes..." (not "Evidence for [product]
  includes...")
- Add: "The applicability of ingredient-level evidence to [product] depends
  on formulation, dose, bioavailability, and manufacturing quality"
- **Never** imply that ingredient evidence is finished-product evidence
- Do not present ingredient studies in a table labeled "Product Evidence"

### 6.3 Population and duration limits

Every scientific statement must preserve population and duration limits from
the source:

- "In a 12-week trial of [population]" (not simply "the trial showed")
- "Among adults aged 18 to 65" (not "among adults")
- Do not generalize from a narrow population without explicit caveats

### 6.4 Negative and inconclusive evidence

- Include negative and inconclusive findings alongside positive ones
- Use neutral language: "the trial did not find a significant difference"
  (not "the trial failed to show")
- **Never** omit negative evidence from a section that summarizes evidence
  for a claim

---

## 7. Commercial interpretation language

### 7.1 Separation of layers

Commercial and strategic interpretation must be separated from factual
reporting. Use distinct language for each layer:

| Layer | Language | Example |
|-------|----------|---------|
| Observed pattern | Descriptive, factual | "Product A was priced 15% below the category median." |
| Interpretation | Inferential, cautious | "This pricing may reflect a market-entry strategy." |
| Business implication | Forward-looking, contingent | "If this pricing is sustained, it could pressure competitors to adjust." |
| Recommendation | Prescriptive, conditional | "Monitoring price movements monthly is recommended." |
| Uncertainty | Explicit, limiting | "This interpretation assumes the observed price is the sustained retail price, not a temporary promotion." |

### 7.2 Recommendation language

Recommendations must:

- Follow from documented findings, not from the report format expectation
- Include the evidence basis: "Based on the price gap of [X]% and [Y]
  competitor positioning..."
- Include the uncertainty: "This recommendation is limited by [specific
  limitation]"
- **Never** fabricate a market opportunity because the report template expects
  one

### 7.3 When evidence is weak

When evidence is insufficient for a firm recommendation:

- State: "Further verification is recommended before acting on this finding"
- Specify what verification is needed (additional data sources, longer
  observation period, confirmatory studies)
- **Never** generate false certainty to fill a gap in the report

---

## 8. Cross-reporting consistency

### 8.1 Language consistency across sections

The same evidence finding must use the same certainty language across all
sections of the report. A finding described as "suggests" in the results
section must not become "demonstrates" in the executive summary.

### 8.2 Consistency with source appraisal

The language used to describe a study or finding in the report must be
consistent with the appraisal in the evidence artifact. If the evidence
artifact classifies a finding as "partially supported," the report must not
describe it as "supported."

### 8.3 Consistency with claim review

When a claim review classifies a commercial claim as "unsupported," the report
must use language consistent with that classification. Do not present an
unsupported claim as "suggested by evidence" or "supported by research."
