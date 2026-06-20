# Claim Support Rules

Rules for classifying whether published evidence substantiates a
commercial or scientific claim about a health product. This reference
extends the claim-substantiation framework in SKILL.md Step 10 and
Step 11, and the claim taxonomy in product-market-research/references/
claim-taxonomy.md.

Use this reference after evidence has been extracted and appraised.
The output is a support classification that appears in the claim-support
assessment section of the evidence artifact.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: SKILL.md (Step 10 evaluate commercial claims,
Step 11 distinguish finding types, Step 12 calibrated conclusions),
evidence-extraction-fields.md (outcome and population fields),
study-design-appraisal.md (certainty ratings), claim-taxonomy.md
(14 claim categories, support classifications).

---

## Table of Contents

1. [Classification principles](#1-classification-principles)
2. [Support level definitions](#2-support-level-definitions)
3. [Directness assessment](#3-directness-assessment)
4. [Evidence-to-claim matching](#4-evidence-to-claim-matching)
5. [Upgrade and downgrade rules](#5-upgrade-and-downgrade-rules)
6. [Claim element decomposition](#6-claim-element-decomposition)
7. [Cross-category claim analysis](#7-cross-category-claim-analysis)
8. [Regulatory context overlay](#8-regulatory-context-overlay)
9. [Edge cases and special rules](#9-edge-cases-and-special-rules)
10. [Forbidden claim practices](#10-forbidden-claim-practices)

---

## 1. Classification principles

### 1.1 The default is unsupported

A claim begins as **unsupported** until evidence of support is
found, extracted, and appraised. The burden rests on establishing
support, not on disproving the claim. Absent relevant evidence,
the classification remains unsupported regardless of how plausible
the claim appears.

### 1.2 Match claim element to evidence element

A claim often contains multiple elements: a population, an
intervention, an outcome, a magnitude, a timeframe, and a causal
assertion. Each element must be matched to the evidence. A claim
can be partially supported when some elements match and others do not.

### 1.3 Evidence quality constrains classification

The support classification ceiling is set by the certainty of the
underlying evidence. Low-certainty evidence cannot support a
"directly supported" classification, even when the study population,
intervention, and outcome match the claim exactly. A single RCT
at high risk of bias may be "partially supported" at best.

### 1.4 Preserve conflicts

When evidence conflicts, classify each evidence source separately.
Do not select one source as authoritative and discard the rest.
If one study supports the claim and another contradicts it, the
classification is "contradicted" with both sources cited. The
existence of supporting evidence does not cancel contradictory
evidence.

### 1.5 Separate scientific from regulatory

A claim can be scientifically supported and still violate
regulatory requirements. A disease treatment claim on a dietary
supplement may be factually accurate based on clinical evidence
but remains a regulatory violation that must be flagged. The
support classification addresses scientific validity only.
Regulatory compliance is a separate axis assessed in the
regulatory context overlay (section 8).

---

## 2. Support level definitions

### 2.1 Classification table

| Classification | Definition | Evidence required | Typical source |
|---------------|------------|-------------------|----------------|
| Directly supported | The specific product (same formulation, same dose, same population, same outcome) was tested and the evidence is credible | Product-specific RCT or controlled trial with low-to-moderate risk of bias; the study measured the claimed outcome, in the claimed population, at a comparable dose, within a comparable timeframe | Published clinical trial on the commercial product |
| Partially supported | The general direction of the claim is supported, but at least one element differs materially: ingredient tested but not the product, different dose or formulation, different population, or broader claim wording than evidence allows | Ingredient-level study, or same product but different dose/formulation, or same ingredient/population with weaker study design | Ingredient-level RCT, product study with different dose |
| Indirectly supported | Support comes from mechanistic rationale, biomarker data, epidemiological associations, animal studies, or studies in materially different populations with only inferential connection to the claim | Mechanistic studies, in vitro data, animal models, observational studies with surrogate outcomes, or population-level epidemiological data | Pharmacological rationale, animal efficacy, biomarker study |
| Unsupported | Relevant evidence was sought but none was found that substantiates the claim; OR the evidence found does not support the claim's direction, magnitude, or certainty | Systematic search completed with no relevant evidence; OR evidence exists but is neutral or null | Negative or null studies, or absence of evidence after search |
| Contradicted | Credible evidence directly conflicts with the claim; a body of evidence shows no effect, harm, or an effect in the opposite direction | At least one moderate-to-high certainty study showing null or opposite effect; OR a systematic review concluding no benefit; OR a regulatory finding against the claim | Negative RCT, meta-analysis showing no effect, FDA warning letter |
| Cannot determine | Essential information for classification is missing: study access blocked, critical methodological detail absent, source unverifiable, or claim wording ambiguous beyond resolution | Gaps in evidence access or quality that prevent any of the above classifications | Paywalled study with uninformative abstract, ambiguous claim wording |

### 2.2 Classification decision tree

For each claim, assess in this order:

1. **Is the claim worded clearly enough to assess?**
   - No: cannot determine.
   - Yes: proceed.

2. **Is there any relevant evidence?**
   - No, after systematic search: unsupported.
   - Yes: proceed.

3. **Does the evidence address each claim element (population, intervention, outcome, magnitude, timeframe)?**
   - Yes, all elements match, and evidence certainty is moderate or higher: directly supported.
   - Most elements match, but at least one differs materially: partially supported.
   - Evidence is mechanistic, biomarker-level, or from a materially different population or product: indirectly supported.

4. **Does the evidence conflict with the claim?**
   - Yes, credible contradictory evidence exists: contradicted.

5. **Is there a conflict between supporting and contradictory evidence?**
   - Yes: contradicted (preserve both sources).

### 2.3 Claim timing and evidence staleness

A claim supported by a single study from 15 years ago may be
reclassified if more recent evidence contradicts it or if the
product formulation has changed. Reclassify when new evidence
appears. Claim support is not static. Re-evaluate when:
- New clinical trials are published.
- Systematic reviews update the evidence base.
- Regulatory actions modify the status.
- Product reformulation occurs.

---

## 3. Directness assessment

### 3.1 Directness dimensions

| Dimension | Direct match | Partial match | Indirect | Not applicable |
|-----------|-------------|---------------|----------|----------------|
| Ingredient | Same active ingredient, same chemical form | Same ingredient, different salt or form | Related ingredient class or metabolite | Different ingredient entirely |
| Formulation | Same dosage form, same excipients, same release mechanism | Same dosage form, different excipients | Different dosage form with same ingredient | Cannot determine |
| Dose | Same per-unit dose, same daily dose | Dose within therapeutic range but different from product | Dose materially different from product | Dose not reported |
| Route | Same route of administration | Same route category (e.g., oral) | Different route with systemic absorption | Route not reported |
| Population | Same demographic, disease state, severity, and inclusion criteria | Same disease state, different severity or demographic mix | Different condition with overlapping pathophysiology | Population not described |
| Outcome | Same outcome, same measurement method, same time point | Same outcome domain, different measurement tool or time point | Surrogate outcome or related biomarker | Outcome not defined |
| Magnitude | Study effect size matches or exceeds claimed magnitude | Study effect size is directionally consistent but smaller | Study reports a different metric | Magnitude not quantified |
| Timeframe | Study duration matches claimed onset or duration | Study duration in same range but shorter or longer | Different exposure duration | Timeframe not specified |
| Comparator | Study comparator matches implied comparison (placebo vs placebo, active vs active) | Study uses a different comparator than implied | No comparator or inappropriate comparator | Comparator irrelevant to claim |

### 3.2 Directness scoring

Count the dimensions that are direct matches, partial matches,
indirect, or not applicable. The overall directness classification:

| Directness rating | Criteria |
|------------------|----------|
| Direct | All applicable dimensions match directly |
| Mostly direct | At least one dimension is a partial match; no dimension is indirect or not applicable |
| Partially indirect | One or two dimensions are indirect or the population or intervention differs materially |
| Substantially indirect | Three or more dimensions are indirect, or the key dimensions (ingredient, population, outcome) are indirect |
| Not applicable | Evidence cannot be applied to the claim (e.g., different condition, different mechanism) |
| Cannot determine | Insufficient information to assess one or more critical dimensions |

### 3.3 Ingredient-to-product bridge

An ingredient-level study is not automatically direct evidence for
a commercial product. The bridge from ingredient to product requires:
- Same ingredient in the same chemical form.
- Comparable dose (within the same therapeutic range).
- Comparable bioavailability (formulation and excipients do not
  materially alter absorption).
- Comparable quality (the product meets pharmacopeial standards).

If any of these conditions is not demonstrated, the evidence is
indirect at best. Use `indirectly_supported` and note which bridge
elements are missing.

---

## 4. Evidence-to-claim matching

### 4.1 The claim-element evidence matrix

For each claim element, record the match status in a matrix:

| Claim element (from claim extraction) | Evidence finding (from evidence extraction) | Match status |
|---------------------------------------|---------------------------------------------|-------------|
| Population: [text] | Study population: [text] | Direct / Partial / Indirect / No match |
| Intervention: [text] | Study intervention: [text] | Direct / Partial / Indirect / No match |
| Outcome: [text] | Study outcome: [text] | Direct / Partial / Indirect / No match |
| Magnitude: [text] | Study effect size: [text] | Direct / Partial / Indirect / No match |
| Timeframe: [text] | Study duration: [text] | Direct / Partial / Indirect / No match |
| Causal assertion: [text] | Study design: [text] | Supported / Unsupported by design |

### 4.2 Causal language calibration

Match the strength of causal language in the claim to the study
design:

| Claim language | Minimum study design required |
|---------------|------------------------------|
| "Proven to", "guaranteed to", "will" | RCT with low risk of bias AND replication in at least one confirmatory trial |
| "Shown to", "demonstrated to" | RCT with moderate risk of bias |
| "Clinically studied", "supported by research" | At least one controlled study (RCT or well-controlled observational) |
| "May", "helps", "supports" | Mechanistic rationale or preliminary evidence |
| "Has been associated with" | Observational study |
| "Traditionally used for" | Historical or ethnobotanical record |

A claim using causal language that exceeds the study design
warrants a downgrade in the support classification. For example,
a claim that an ingredient "has been proven to reduce cholesterol"
based on a single observational study is partially supported at
best, even if the observational study found an association.

### 4.3 Magnitude matching

When the claim specifies a magnitude (e.g., "reduces X by 30%"),
the evidence must show an effect of comparable size:
- Direct match: the study's point estimate falls within a
  clinically reasonable range of the claimed magnitude.
- Partial match: the direction matches but the magnitude differs
  substantially.
- No match: the study shows a smaller or null effect.

When the claim uses vague magnitude language ("significantly",
"dramatically"), interpret the wording in the context of the
claim's regulatory category and the product type. A "significant"
effect in a dietary supplement claim may refer to statistical
significance or clinical significance; extract the exact wording
and assess both.

---

## 5. Upgrade and downgrade rules

### 5.1 Downgrade criteria

A support classification is downgraded when:

| Downgrade trigger | From | To | Example |
|------------------|------|-----|---------|
| Evidence certainty is low or very low | Directly supported | Partially supported | Single small RCT at high risk of bias |
| Key claim element is a partial match | Directly supported | Partially supported | Same ingredient, different dose |
| Key claim element is indirect | Directly supported | Indirectly supported | Different population, same intervention |
| Causal language exceeds study design | Partially supported | Indirectly supported | "Proven" based on mechanistic study |
| Evidence is from a single unreplicated study | Directly supported | Partially supported | One positive trial, no confirmatory studies |
| Abstract-only source without full text verification | Partially supported | Indirectly supported | Abstract suggests support but methods are inaccessible |
| Study predates the product formulation | Directly supported | Partially supported | Ingredient study from 2010; product launched 2025 with different formulation |
| Conflict of interest with no independent replication | Partially supported | Indirectly supported | Only manufacturer-funded study exists |

### 5.2 Upgrade criteria (rare)

A support classification is upgraded only when:

| Upgrade trigger | From | To | Condition |
|----------------|------|-----|-----------|
| Consistent evidence from multiple independent sources | Partially supported | Directly supported | At least 2 independent RCTs with consistent results |
| Evidence certainty increases upon re-assessment | Partially supported | Directly supported | New evidence or re-analysis raises certainty to moderate or high |
| A meta-analysis confirms the effect with narrow CIs | Partially supported | Directly supported | Meta-analysis of at least 3 studies, I² < 30%, narrow confidence interval |

Upgrades are uncommon. Most evidence does not become stronger over
time without new studies. **Never upgrade based on reinterpretation
alone.** Reinterpreting existing evidence cannot increase the
underlying certainty.

### 5.3 Direction of effect in downgrading

When evidence conflicts, the classification resolves to the lowest
level that is supported. A claim with one directly supporting study
and one contradicting study is "contradicted", not "directly supported".
A claim with direct support from one study, partial support from
another, and no contradicting evidence is "partially supported"
pending replication.

---

## 6. Claim element decomposition

### 6.1 Decompose before classifying

Every claim must be decomposed into its constituent elements
before classification. A claim like "Clinically proven to reduce
LDL cholesterol by 15% in 8 weeks for adults over 50" contains:

| Element | Value |
|---------|-------|
| Intervention claim | The product (implicit) |
| Outcome | LDL cholesterol reduction |
| Magnitude | 15% |
| Timeframe | 8 weeks |
| Population | Adults over 50 |
| Causal assertion | Clinically proven |
| Evidence type implied | Clinical study |

Each element must be compared against the evidence. A study that
measured total cholesterol (not LDL) in adults of all ages (not
just over 50) over 12 weeks (not 8) shows a partial match on outcome,
partial match on population, and partial match on timeframe. The
best classification is "partially supported."

### 6.2 Implicit claims

Some claims are implicit rather than explicit. A product named
"Sleep Aid Formula" implies a sleep efficacy claim even if no
explicit claim appears. An image of a heart implies a cardiovascular
benefit claim. Extract implicit claims and treat them the same as
explicit claims for classification purposes. Record the basis for
the implication in the claim extraction.

### 6.3 Qualified vs unqualified language

A claim using qualified language ("may help support") requires
less evidence to reach "directly supported" than an unqualified
claim ("reduces"). However, the qualified language itself must
match the evidence. If the evidence shows clear, consistent benefit
and the claim says "may help", the classification is "directly
supported" because the evidence exceeds the claim. If the evidence
is weak and the claim is unqualified, the classification is
"unsupported" or "partially supported" at best.

---

## 7. Cross-category claim analysis

### 7.1 Multi-category claims

A single claim statement can span multiple categories in the
claim-taxonomy.md classification. For example, "Clinically proven
to reduce LDL by 15% in 8 weeks" spans:
- Category 3: Disease treatment implication (LDL cholesterol).
- Category 5: Onset speed (8 weeks).
- Category 6: Effect magnitude (15%).
- Category 11: Clinical-study backing.

Each category element receives its own support classification.
The overall claim classification is the lowest (least supportive)
of the individual classifications.

### 7.2 Composite claim classification

When a claim spans multiple categories, produce a composite
classification matrix:

| Category | Element | Support level | Evidence source |
|----------|---------|---------------|-----------------|
| Clinical-study backing | Existence of clinical study | Directly supported | Study NCT12345678 |
| Effect magnitude | 15% LDL reduction | Partially supported | Study showed 12.3% not 15% |
| Onset speed | Within 8 weeks | Directly supported | Outcome measured at week 8 |
| Disease implication | LDL cholesterol treatment | Contradicted | Meta-analysis shows 3-5% reduction, not 15% |

Overall classification: **Partially supported** (lowest non-contradicted level is partial for magnitude, and the disease implication claim is contradicted by the broader evidence base).

### 7.3 Claim dependency analysis

Some claims depend on other claims. A technology claim ("patented
liposomal delivery for maximum absorption") may underpin an efficacy
claim ("better absorption means better results"). If the technology
claim is unsupported, any claim that depends on it is downgraded
to unsupported, regardless of the efficacy evidence. Assess
dependency chains explicitly.

---

## 8. Regulatory context overlay

### 8.1 Regulatory compliance vs scientific support

| Scenario | Scientific support | Regulatory status | Classification in report |
|----------|-------------------|-------------------|------------------------|
| Pharma with approved indication | Directly supported | Compliant | Directly supported; regulatory compliant |
| Supplement with disease claim | Directly supported (by ingredient study) | Noncompliant (illegal claim type) | Partially supported (ingredient evidence); flagged as regulatory violation |
| Supplement with structure-function claim | Directly supported | Compliant | Directly supported |
| Supplement with efficacy claim, no evidence | Unsupported | May be compliant (if qualified) or noncompliant (if unqualified) | Unsupported; regulatory status noted separately |
| Any product with safety claim | Contradicted (evidence of risk) | Noncompliant | Contradicted; flagged for safety concern |

### 8.2 Jurisdictional variation

A claim may be scientifically supported and regulatory compliant
in one jurisdiction but noncompliant in another. For example, a
health claim authorized by Japan's FOSHU system may not be permitted
under EU Regulation 1924/2006. Record the jurisdictional context
of the assessment. When evaluating for multiple jurisdictions,
produce separate regulatory assessments.

### 8.3 Required disclaimers

When a claim requires a regulatory disclaimer (e.g., the FDA
disclaimer for dietary supplement structure-function claims),
verify whether the disclaimer is present in the source. A missing
required disclaimer is a regulatory finding, not a scientific one,
but must be recorded in the claim assessment.

---

## 9. Edge cases and special rules

### 9.1 Proprietary blends with undisclosed quantities

When a product uses a proprietary blend and the individual
ingredient quantities are not disclosed, any ingredient-level
efficacy evidence is "cannot determine" for dose matching.
Without knowing the dose in the product, the evidence-to-product
bridge is incomplete. Classify as "indirectly supported" at best.

### 9.2 Multi-ingredient products

When a product contains multiple active ingredients and the claim
attributes benefit to a single ingredient, assess support for that
ingredient alone. When the claim attributes benefit to the
combination, the evidence must involve the same combination at
comparable doses. Ingredient-level evidence for each component
individually is "partially supported" for a combination claim.

### 9.3 Reformulated products

When a product has been reformulated since the evidence was
generated, the existing evidence may not apply. A study on version 1
does not directly support a claim about version 2 if the
formulation, dose, or delivery system has changed. Classify as
"partially supported" and note the reformulation gap.

### 9.4 Historical or traditional use claims

Claims based on traditional use (e.g., "used for centuries in
Ayurvedic medicine") are classified differently from efficacy
claims. Traditional use claims require evidence of historical use,
not clinical evidence of efficacy. Classify traditional use claims as:
- **Directly supported** if documented in an authoritative
  pharmacopeia or traditional medicine monograph.
- **Partially supported** if documented in secondary historical
  sources.
- **Unsupported** if no documentation of traditional use exists.

A traditional use claim must not be confused with an efficacy
claim. When a product makes both types of claims, classify each
separately.

### 9.5 Homeopathic products

Homeopathic products at high dilutions present a special case.
Evidence rules apply normally: if no credible evidence of efficacy
exists above placebo, the claim is unsupported. The dilution
principle does not create an exception to evidence requirements.
Regulatory status (homeopathic registration) is separate from
scientific support.

---

## 10. Forbidden claim practices

### 10.1 Correlation as causation prohibition

**Never treat correlation as causation.** Observational evidence
shows association, not causation. An observational study reporting
that people who take supplement X have lower levels of biomarker Y
establishes an association. It does not establish that supplement X
causes the reduction. Causal language in a claim requires causal
evidence (RCT or strong quasi-experimental design). When the
evidence is observational, classify the claim as "indirectly
supported" at best, even if the association is strong.

### 10.2 Consumer review prohibition

**Never use consumer reviews as evidence.** Consumer reviews,
testimonials, ratings, and user comments are not evidence of
efficacy, safety, or product quality. They may inform narrative
analysis or signal detection for adverse events, but they cannot
support any claim classification above "unsupported." A product
with thousands of positive reviews and no clinical evidence is
"unsupported" for any efficacy claim.

### 10.3 In vitro to in vivo leap prohibition

**Never present in vitro evidence as in vivo efficacy evidence.**
A study showing that an ingredient inhibits an enzyme in a petri
dish does not mean the product inhibits that enzyme in humans.
The gap between in vitro concentration, bioavailability,
metabolism, and clinical effect is too large to bridge without
human studies. In vitro evidence is "indirectly supported" at best
for any human efficacy claim.

### 10.4 Animal to human extrapolation prohibition

**Never present animal study evidence as human efficacy evidence.**
Animal models provide mechanistic plausibility but do not establish
human efficacy. Species differences in metabolism, disease etiology,
and treatment response are well documented. Animal evidence is
"indirectly supported" at best for human efficacy claims.

### 10.5 Evidence fabrication prohibition

**Never invent evidence to support a claim.** When no relevant
evidence is found after systematic search, classify as "unsupported."
Do not fabricate study names, journal references, effect sizes,
confidence intervals, or any other evidential detail to fill the gap.

### 10.6 Evidence overstatement prohibition

**Never overstate the strength of evidence to match the strength
of the claim.** A claim may use strong language ("guaranteed results")
while the evidence is weak. The classification reflects the evidence,
not the claim's wording. Do not upgrade a classification because
the claimant would prefer a higher rating. A weak claim with weak
evidence is still "unsupported" or "partially supported", not
"directly supported."

### 10.7 Selective citation prohibition

**Never cite only supporting evidence when contradictory evidence
exists.** When the evidence base is mixed, classify as "contradicted"
and report both the supporting and the contradictory sources. The
existence of one positive study does not cancel three negative
studies. The reader must see the full evidence picture.

### 10.8 Abstract-only overstatement prohibition

**Never present an abstract-only source as full-text verified
evidence.** An abstract that states positive results without
reporting methods detail, dropout rates, or adverse events is
insufficient for a support classification above "cannot determine."
If the investigator cannot access the full text, the evidence
gap must be recorded.

