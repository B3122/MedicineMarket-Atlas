# Study Design Appraisal

Risk-of-bias criteria, appraisal tool selection, and certainty
assessment rules per study design. This reference operationalizes
the internal validity assessment in SKILL.md Step 7 and the
certainty assessment in Step 9.

Use this reference after study data has been extracted (per
evidence-extraction-fields.md) and the study design has been
classified. The output is a risk-of-bias judgment that feeds into
the overall certainty of evidence rating.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: SKILL.md (Step 7 internal validity, Step 9
certainty assessment), evidence-extraction-fields.md (bias and
quality fields), claim-support-rules.md (downgrade criteria for
risk of bias).

---

## Table of Contents

1. [Appraisal principles](#1-appraisal-principles)
2. [Study design classification](#2-study-design-classification)
3. [Randomized controlled trials](#3-randomized-controlled-trials)
4. [Observational studies](#4-observational-studies)
5. [Systematic reviews and meta-analyses](#5-systematic-reviews-and-meta-analyses)
6. [Case reports and case series](#6-case-reports-and-case-series)
7. [Mechanistic and preclinical studies](#7-mechanistic-and-preclinical-studies)
8. [Clinical practice guidelines](#8-clinical-practice-guidelines)
9. [Appraisal tools and scoring](#9-appraisal-tools-and-scoring)
10. [Certainty of evidence](#10-certainty-of-evidence)
11. [Forbidden appraisal practices](#11-forbidden-appraisal-practices)

---

## 1. Appraisal principles

### 1.1 Assess what is reported, not what is assumed

Base the risk-of-bias judgment on information present in the source.
When a domain cannot be assessed because the source does not report
sufficient detail, record the domain as `"unclear"` or `"not_reported"`.
Do not assume adequate methods in the absence of reporting.

### 1.2 Rate per domain before rating overall

Assess each bias domain separately. The overall risk-of-bias judgment
derives from the domain-level assessments. A study with low risk of
bias in eight domains but high risk in one critical domain may still
warrant an overall judgment of high risk.

### 1.3 Use the appropriate tool for the design

Apply the appraisal tool designed for the study design. Using
Cochrane RoB 2 for an observational study or ROBINS-I for an RCT
produces invalid assessments. Tool selection is governed by the
design-tool mapping in section 9.

### 1.4 Separate risk of bias from precision

Risk of bias addresses systematic error (internal validity).
Imprecision addresses random error (width of confidence intervals).
Both contribute to certainty of evidence but are distinct domains.
Assess them separately before combining into a certainty rating.

### 1.5 Record the tool and version

Always record which appraisal tool was used and its version.
A judgment of "high risk of bias" without documenting the tool
and the domain-level reasoning is not reproducible.

---

## 2. Study design classification

### 2.1 Design hierarchy for appraisal

| Design | Appraisal tool | Key bias domains |
|--------|---------------|------------------|
| RCT (parallel, crossover, cluster, factorial) | Cochrane RoB 2 | Randomization, deviations, missing data, measurement, selective reporting |
| Observational cohort | ROBINS-I | Confounding, selection, classification, deviations, missing data, measurement, selective reporting |
| Observational case-control | ROBINS-I | Confounding, selection, classification, deviations, missing data, measurement, selective reporting |
| Observational cross-sectional | Adapted ROBINS-I or JBI checklist | Selection, measurement, confounding |
| Systematic review / meta-analysis | AMSTAR 2 or ROBIS | Protocol, search, selection, data extraction, bias assessment, synthesis |
| Case series / case report | JBI case report checklist | Selection, assessment, causality, reporting |
| Quasi-experimental | ROBINS-I or adapted RoB | Confounding, selection, time trends, measurement |
| Mechanistic / preclinical | SYRCLE or adapted assessment | Allocation, blinding, outcome assessment, reporting |
| Guideline | AGREE II | Scope, stakeholder, rigor, clarity, applicability, editorial independence |
| Regulatory assessment | Reviewer judgment | Source authority, completeness, recency |

### 2.2 Design confirmation rule

Confirm the study design from the methods section, not the title
or abstract. Some sources label themselves incorrectly (e.g., a
retrospective chart review labeled as a "clinical trial"). Record
the actual design per the methods and note any title-methods
discrepancy in the extraction.

---

## 3. Randomized controlled trials

### 3.1 Bias domains (Cochrane RoB 2 framework)

| Domain | Low risk criteria | High risk indicators |
|--------|-------------------|----------------------|
| Randomization process | Central, web-based, or pharmacy-controlled randomization with allocation concealment | Alternating assignment, date of birth, chart number, open allocation list |
| Deviations from intended interventions | Double-blind with identical placebo; analysis by ITT | Open-label with differential co-interventions; per-protocol analysis with substantial exclusions |
| Missing outcome data | Complete outcome data or reasons balanced across arms and unlikely related to outcome | Differential loss to follow-up; missingness likely related to true outcome |
| Measurement of the outcome | Blinded outcome assessors using objective measurement | Unblinded assessors for subjective outcomes; patient-reported unblinded outcomes |
| Selection of the reported result | Analysis follows prespecified plan; all prespecified outcomes reported | Selective reporting of favorable outcomes; outcome switching without explanation |

### 3.2 Overall risk-of-bias judgment (RoB 2 algorithm)

| Condition | Overall judgment |
|-----------|-----------------|
| All domains low risk | Low risk of bias |
| Some concerns in at least one domain, no high risk | Some concerns |
| High risk in at least one domain, or multiple domains with some concerns in a way that lowers confidence | High risk of bias |

### 3.3 Crossover trial considerations

For crossover trials, assess additionally:
- Carryover effects between periods.
- Period effects (time trends).
- Whether the washout period is adequate.
- Whether the analysis accounts for the paired design.

### 3.4 Cluster-randomized trial considerations

For cluster-randomized trials, assess additionally:
- Whether recruitment bias occurred (individuals recruited after
  cluster allocation known).
- Whether baseline imbalance between clusters was addressed.
- Whether the analysis accounts for clustering (intraclass
  correlation).

### 3.5 Equivalence and non-inferiority trials

For equivalence and non-inferiority trials, the direction of bias
assessment differs. In a non-inferiority trial, poor methodology
that biases toward the null (e.g., non-adherence analyzed as ITT)
is conservative for superiority but anti-conservative for
non-inferiority. Assess bias direction against the trial's stated
hypothesis.

---

## 4. Observational studies

### 4.1 Bias domains (ROBINS-I framework)

| Domain | Low risk criteria | High risk indicators |
|--------|-------------------|----------------------|
| Confounding | All known important confounders measured and controlled; appropriate analytic method | Key confounders unmeasured; confounding by indication not addressed |
| Selection of participants | All eligible participants included; start of follow-up and start of intervention coincide | Selection into study related to both intervention and outcome; immortal time bias present |
| Classification of interventions | Intervention status well-defined and based on information recorded at the time | Retrospective classification using recall; misclassification differential by outcome |
| Deviations from intended interventions | No deviations; any deviations reflect usual practice and were accounted for | Systematic deviations related to prognosis; time-varying confounding not addressed |
| Missing data | Complete data or appropriate multiple imputation; reasons for missingness independent of outcome | Substantial missing data with differential reasons by outcome |
| Measurement of outcomes | Objective outcomes; blinded assessment; validated instruments | Subjective outcomes with unblinded assessment; different measurement methods by group |
| Selection of reported result | Prespecified analysis plan; all measured outcomes reported | Selective reporting; outcome data dredging; post-hoc subgroup selection |

### 4.2 The target trial framework

When appraising an observational study that estimates a causal
effect, define the hypothetical target trial: the RCT that would
answer the same question. Each ROBINS-I domain asks whether the
observational study emulates the target trial adequately. A
well-conducted observational study explicitly designs itself as
an emulation of a target trial.

### 4.3 Confounding by indication

Confounding by indication is the single most important bias in
observational studies of treatment effects. People who receive
treatment differ systematically from those who do not. Record
how the study addressed this: propensity score matching, inverse
probability weighting, instrumental variable analysis, or
none. Studies without any adjustment for confounding by indication
start at critical risk of bias.

### 4.4 Immortal time bias

Immortal time bias occurs when the classification of exposure
depends on surviving to a future time point, but survival time
before exposure is misclassified as exposed time. Common in
cohort studies that define treatment groups based on whether
treatment was ever received. Studies that use a time-varying
exposure definition or landmark analysis mitigate this bias.

---

## 5. Systematic reviews and meta-analyses

### 5.1 Critical appraisal domains (AMSTAR 2 framework)

| Domain | Critical item |
|--------|--------------|
| Protocol registration | Was the review registered or a protocol published before conduct? |
| Literature search | Was the search comprehensive (at least 2 databases, search strategy provided)? |
| Study selection | Was study selection performed in duplicate? |
| Data extraction | Was data extraction performed in duplicate? |
| Excluded studies | Was a list of excluded studies with reasons provided? |
| Included studies | Are the included studies described in adequate detail? |
| Risk of bias | Was risk of bias assessed with an appropriate tool? |
| Funding of included studies | Was the funding source of included studies reported? |
| Meta-analysis methods | Were appropriate methods used for meta-analysis? |
| Risk of bias in synthesis | Was risk of bias accounted for in interpreting results? |
| Publication bias | Was publication bias assessed and discussed? |
| Conflicts of interest | Were review author conflicts of interest reported? |

### 5.2 Overall confidence rating (AMSTAR 2)

| Rating | Criteria |
|--------|----------|
| High | No or one non-critical weakness; the review provides an accurate and comprehensive summary |
| Moderate | More than one non-critical weakness; the review may provide an accurate summary |
| Low | One critical flaw with or without non-critical weaknesses; the review may not provide an accurate summary |
| Critically low | More than one critical flaw; the review should not be relied on |

### 5.3 Network meta-analysis considerations

For network meta-analyses, assess additionally:
- Whether the transitivity assumption is justified (are the studies
  sufficiently similar to support indirect comparisons?).
- Whether inconsistency between direct and indirect evidence was
  assessed (node-splitting, design-by-treatment interaction).
- Whether the network geometry is adequate (connected network,
  sufficient studies per comparison).
- Whether treatments were jointly randomizable.

### 5.4 Publication bias assessment

When a meta-analysis reports no publication bias assessment, note
this as a critical flaw. Funnel plot asymmetry tests (Egger's test,
Begg's test) require at least 10 studies. For smaller meta-analyses,
publication bias cannot be ruled out and must be discussed as a
limitation.

---

## 6. Case reports and case series

### 6.1 Appraisal domains (JBI checklist)

| Domain | Assessment question |
|--------|-------------------|
| Patient demographics | Are the patient's demographic characteristics clearly described? |
| Patient history | Is the patient's history clearly described and presented as a timeline? |
| Clinical condition | Is the current clinical condition of the patient clearly described? |
| Diagnostic assessment | Are diagnostic tests or methods and results clearly described? |
| Interventions | Are the interventions or treatments clearly described? |
| Post-intervention condition | Is the post-intervention clinical condition clearly described? |
| Adverse events | Are adverse events or unanticipated events identified and described? |
| Takeaway lessons | Does the case report provide takeaway lessons? |

### 6.2 Evidence weight

Case reports and case series provide the lowest weight of evidence
for efficacy claims. They are hypothesis-generating and useful for
signal detection (rare adverse events, unexpected effects) but do
not establish causality or generalizable efficacy.

**Never upgrade a case report or case series to support a claim of
effectiveness.** Use case reports only to identify safety signals or
generate hypotheses for further investigation. Record this limitation
in any synthesis that includes case-level evidence.

---

## 7. Mechanistic and preclinical studies

### 7.1 Appraisal domains

| Domain | Assessment question |
|--------|-------------------|
| Study question | Is the hypothesis clearly stated? |
| Experimental model | Is the model appropriate for the research question? |
| Sample size | Is the sample size justified (power calculation or convention)? |
| Allocation | Were animals or samples randomly allocated to groups? |
| Blinding | Was outcome assessment blinded to group allocation? |
| Dose relevance | Are the doses tested relevant to human exposure levels? |
| Outcome measurement | Are outcomes measured with validated methods? |
| Reporting completeness | Are all measured outcomes reported? |

### 7.2 Human relevance limitation

Mechanistic studies (in vitro, animal models, pharmacokinetic
simulations) cannot directly support human efficacy claims.
They provide plausibility and biological rationale. When cited
in support of a clinical claim, classify the evidence as
indirect at best. Record the model-to-human gap explicitly.

### 7.3 Dose translation

When a mechanistic study uses doses that differ substantially
from human exposure levels (e.g., in vitro concentrations orders
of magnitude above achievable plasma levels), note the translational
gap. Such evidence may be irrelevant to the clinical question.

---

## 8. Clinical practice guidelines

### 8.1 Appraisal domains (AGREE II framework)

| Domain | Key items |
|--------|----------|
| Scope and purpose | Objectives, health questions, target population explicitly described |
| Stakeholder involvement | Guideline development group includes relevant professionals; target population views sought |
| Rigor of development | Systematic evidence search; explicit link between evidence and recommendations; external review; updating procedure |
| Clarity of presentation | Recommendations are specific and unambiguous; different options clearly presented |
| Applicability | Facilitators and barriers to application; resource implications; monitoring criteria |
| Editorial independence | Funding body views not influential; competing interests recorded and addressed |

### 8.2 Recency assessment

Guidelines older than 5 years may not reflect current evidence.
When using an older guideline, verify that no major new evidence
has emerged since publication. Record the last search date stated
in the guideline. Guidelines without a stated search date receive
a downgrade on the rigor domain.

### 8.3 Jurisdictional relevance

A guideline developed for one health system may not apply to
another. Differences in available treatments, standard of care,
regulatory approvals, and population characteristics affect
applicability. Record jurisdictional mismatch in the applicability
assessment per evidence-extraction-fields.md section 4.3.

---

## 9. Appraisal tools and scoring

### 9.1 Tool selection matrix

| Study design | Primary tool | Alternative tool | Notes |
|-------------|-------------|------------------|-------|
| Parallel-group RCT | Cochrane RoB 2 | PEDro scale (physiotherapy) | RoB 2 preferred for drug and supplement trials |
| Crossover RCT | Cochrane RoB 2 (crossover variant) | none standard | Assess carryover and period effects additionally |
| Cluster RCT | Cochrane RoB 2 (cluster variant) | none standard | Assess recruitment bias and clustering additionally |
| Cohort study | ROBINS-I | Newcastle-Ottawa Scale (NOS) | ROBINS-I preferred; NOS is older and less rigorous |
| Case-control study | ROBINS-I | Newcastle-Ottawa Scale | Same preference as cohort |
| Cross-sectional study | Adapted ROBINS-I | JBI checklist for cross-sectional | State the adaptation |
| Systematic review of RCTs | AMSTAR 2 | ROBIS | AMSTAR 2 does not produce a single score |
| Systematic review of observational studies | AMSTAR 2 or ROBIS | none standard | Note the design of included studies |
| Case report | JBI case report checklist | CARE guidelines | JBI is an appraisal tool; CARE is a reporting guideline |
| Case series | Adapted JBI checklist | Institute of Health Economics checklist | Document the adaptation |
| Diagnostic accuracy | QUADAS-2 | none standard | Use only when the question concerns diagnostic accuracy |
| Prognostic studies | QUIPS | none standard | Use for prognostic factor or model studies |
| Preclinical animal | SYRCLE RoB tool | CAMARADES checklist | Animal studies only |
| Guideline | AGREE II | none standard | Score as percentage per domain |

### 9.2 Tool version recording

Always record the tool version used. Example entries:
- `"Cochrane RoB 2 (2019 version)"`
- `"AMSTAR 2 (2017)"`
- `"ROBINS-I (2016)"`
- `"JBI critical appraisal checklist for case reports (2020)"`

### 9.3 When a formal tool is not used

If a formal appraisal tool is not applied, explicitly state the
reason and describe the ad-hoc method. Do not present ad-hoc
assessments as formal tool-based judgments. Common valid reasons:
- Insufficient information reported in the source to apply the tool.
- Source type lacks a validated appraisal tool (some regulatory
  documents, expert consensus statements).
- The review scope is explicitly scoping or mapping rather than
  appraising.

---

## 10. Certainty of evidence

### 10.1 GRADE domains for downgrading

| Domain | Downgrade trigger | Downgrade level |
|--------|-------------------|-----------------|
| Risk of bias | Overall high risk of bias across most studies | -1 (serious) or -2 (very serious) |
| Inconsistency | Substantial unexplained heterogeneity (I² > 50% or non-overlapping CIs) | -1 (serious) or -2 (very serious) |
| Indirectness | Population, intervention, comparator, or outcome differs from the review question | -1 (serious) or -2 (very serious) |
| Imprecision | Wide confidence interval crossing decision threshold; small sample size; few events | -1 (serious) or -2 (very serious) |
| Publication bias | Evidence of small-study effects, funnel plot asymmetry, or known unpublished negative studies | -1 (strongly suspected) |

### 10.2 GRADE domains for upgrading (observational studies only)

| Domain | Upgrade trigger | Upgrade level |
|--------|-----------------|--------------|
| Large effect | RR > 2 or RR < 0.5 with no plausible confounding | +1 (large) or +2 (very large) |
| Dose-response gradient | A clear dose-response relationship is present | +1 |
| Residual confounding | All plausible confounding would reduce the demonstrated effect or suggest a spurious effect when results show no effect | +1 |

Upgrading applies only to observational studies that start at low
quality. RCTs start at high quality and can only be downgraded.
**Never upgrade based on a single study.** Multiple consistent
studies are required for upgrading.

### 10.3 Certainty levels and interpretation

| Certainty level | Interpretation | Implication for practice |
|----------------|---------------|--------------------------|
| High | Further research is very unlikely to change confidence in the estimate | Strong basis for decision-making |
| Moderate | Further research is likely to have an important impact and may change the estimate | Adequate basis, but may change |
| Low | Further research is very likely to have an important impact and is likely to change the estimate | Uncertain basis; use with caution |
| Very low | Any estimate of effect is very uncertain | Do not rely on for decisions |
| Insufficient evidence | No evidence or evidence too limited to form a judgment | No conclusion possible |

### 10.4 Informal vs formal GRADE

If a formal GRADE assessment was not conducted, use verbal labels
(high confidence, moderate confidence, low confidence, very low
confidence, insufficient evidence) without the GRADE terminology.
**Do not label an informal judgment as a formal GRADE assessment.**
GRADE requires a structured, domain-by-domain evaluation with
documented reasons for each downgrade or upgrade.

---

## 11. Forbidden appraisal practices

### 11.1 Funding source discrimination prohibition

**Never downgrade for funding source alone.** Industry funding is
a potential source of bias, but the risk-of-bias assessment must
be based on actual methodological features, not the funding source.
An industry-funded study with excellent methodology has low risk
of bias. Record the funding source in the extraction (per
evidence-extraction-fields.md section 10) and consider it as one
contextual factor, but do not use it as a surrogate for
methodological quality assessment.

### 11.2 Single-study upgrade prohibition

**Never upgrade evidence certainty based on a single study.**
GRADE upgrading criteria (large effect, dose-response, residual
confounding) require a body of consistent evidence. One positive
observational study with a large effect size does not warrant an
upgrade. Multiple studies showing the same large effect are required.

### 11.3 Tool misapplication prohibition

**Never apply an appraisal tool to a study design it was not
designed for.** Using ROBINS-I on an RCT, or Cochrane RoB 2 on
an observational study, produces invalid results. When the study
design classification is uncertain, use the most conservative
tool or document the assumption.

### 11.4 Selective domain reporting prohibition

**Never report only favorable bias domain assessments.** When a
study has high risk of bias in one domain and low risk in others,
report all domain assessments. Selective reporting of favorable
domains misrepresents the overall risk of bias.

### 11.5 Certainty inflation prohibition

**Never inflate the certainty rating to support a desired
conclusion.** The certainty assessment must reflect the actual
body of evidence, not the strength of the claim being evaluated.
A weakly supported claim remains weakly supported regardless of
how strongly it is worded by the claimant.

### 11.6 Equating absence of evidence with evidence of absence

**Never treat the absence of reported bias safeguards as evidence
of adequate methodology.** When a source does not describe its
randomization procedure, the domain is `"unclear"` or
`"not_reported"`, not `"low risk"`. The absence of reporting is
not evidence of proper conduct.

