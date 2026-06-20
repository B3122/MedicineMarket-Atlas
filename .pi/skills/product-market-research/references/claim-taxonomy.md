# Claim Taxonomy

> **Core principle**: Commercial claims are marketing assertions, not verified facts. Every claim must be classified, extracted with its exact source wording, and independently verified before it can be used as evidence. See [Claim Support Classifications](#claim-support-classifications) below.

## Overview

This taxonomy classifies health product commercial claims into 14 categories. Use it during claim extraction (see `commercial_claim` record in `output-record-specification.md`) to ensure consistent categorization and to determine what evidence is needed to support or refute each claim.

---

## 1. Ingredient Fact

**Definition**: A factual statement about the presence, quantity, source, or form of an ingredient. Does not assert a health outcome. Often appears in ingredient lists, Supplement Facts panels, or product descriptions.

**Examples**:
- CN: "每粒含 500mg 维生素 C"
- EN: "Contains 2000 IU vitamin D3 per serving"

**Extraction method**: Extract verbatim from product page, label, or listing. Record the ingredient name, stated quantity/unit, and any claims about ingredient form (e.g., "buffered", "liposomal", "methylated").

**Risk points**:
- Quantity may refer to proprietary blend total rather than individual ingredient.
- "Proprietary blend" masking can make individual ingredient quantities unknown.
- Ingredient source claims ("from Icelandic kelp") may be unverifiable.
- Unit errors or label discrepancies between regions.

**Required supporting evidence**:
- Label image or official product page screenshot.
- Third-party lab analysis (if verifying quantity).
- Direct evidence from manufacturer or regulatory filing for ingredient source claims.

---

## 2. Efficacy

**Definition**: A claim that the product produces a specific beneficial effect on a body function, structure, or state of well-being. Distinct from disease treatment (Category 3) — efficacy claims stay within structure-function or general wellness territory.

**Examples**:
- CN: "增强免疫力，改善睡眠质量"
- EN: "Supports joint health and flexibility"

**Extraction method**: Capture the exact wording of the benefit statement. Note whether it uses qualifying language ("may", "supports", "helps") or definitive language ("boosts", "strengthens", "improves").

**Risk points**:
- Structure-function claims for dietary supplements require FDA disclaimer in the US: "This statement has not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease."
- Efficacy claims without clinical evidence are marketing assertions only.
- "May help" versus "guarantees" — degree of certainty in claim wording.
- Different regulators treat claims differently (FDA, EFSA, CFDA/NMPA, TGA).

**Required supporting evidence**:
- At minimum: a plausible mechanism of action based on established science.
- Strong evidence: randomized controlled trial (RCT) using the specific product.
- Acceptable: systematic reviews, meta-analyses, or authoritative monographs (e.g., WHO, EMA, USP).
- Strength of evidence must be classified: direct, partial, indirect, unsupported, or contradicted (see classifications below).

---

## 3. Disease Treatment or Prevention Implication

**Definition**: A claim that explicitly or implicitly states the product can treat, cure, prevent, mitigate, or diagnose a specific disease or medical condition. This is the most regulated claim category.

**Examples**:
- CN: "辅助降血糖，糖尿病患者适用"
- EN: "Clinically shown to reduce LDL cholesterol by 15%"

**Extraction method**: Identify disease terminology (diabetes, hypertension, cancer, arthritis, cholesterol, etc.). Capture both explicit statements and implied connections (e.g., "supports healthy blood sugar levels already in the normal range" — implied diabetes claim). Note images of medical symbols (stethoscopes, crosses, ECG lines) as implied disease claims.

**Risk points**:
- **REGULATORY VIOLATION**: Disease treatment claims on dietary supplements are illegal in the US (FDA), EU (EFSA), China (NMPA/SAMR), and most major markets. Products making such claims are misbranded and subject to enforcement.
- Implied claims (using medical symbols, patient testimonials mentioning disease names) carry the same regulatory risk.
- Even structure-function language that explicitly names a disease crosses the line.
- In some jurisdictions, a single disease claim on a marketplace page is enough for removal or penalty.
- Some platforms (Amazon, Tmall) have their own stricter policies beyond local regulation.

**Required supporting evidence**:
- For a pharmaceutical: approved label/package insert from the relevant regulator (FDA, EMA, NMPA).
- For a supplement: disease claims are not legally permissible, so no amount of supporting evidence makes the claim compliant. Flag as regulatory violation regardless of scientific support.
- If evidence of disease effect exists from clinical studies, record it in the academic evidence track but mark the commercial claim itself as noncompliant.

---

## 4. Safety

**Definition**: A claim about the product's safety profile — absence of side effects, suitability for long-term use, lack of interactions, or specific safety certifications ("non-GMO", "no artificial preservatives", "hypoallergenic").

**Examples**:
- CN: "无副作用，适合长期服用"
- EN: "Non-drowsy formula, safe for daily use"

**Extraction method**: Capture the exact safety assertion. Note whether it is an absolute claim ("no side effects" — highest risk) or a qualified claim ("generally well tolerated"). Also flag safety certifications (NSF, USP, GMP, organic, non-GMO verified).

**Risk points**:
- Absolute safety claims ("no side effects", "completely safe") are nearly impossible to substantiate and are regulatory red flags.
- "Natural does not mean safe" — natural positioning (Category 10) may imply safety without evidence.
- Safety data from clinical trials may not reflect real-world use (e.g., long-term, polypharmacy).
- Lack of reported side effects is not the same as evidence of safety.
- Claims about specific safety certifications must be verified with the certifying body.

**Required supporting evidence**:
- Clinical trial adverse event data (at minimum for the active ingredient).
- Post-market surveillance data.
- Regulatory approval history.
- For absolute safety claims: near-impossible to fully substantiate. Flag as high-risk.
- For safety certifications: third-party certification documentation.

---

## 5. Onset Speed

**Definition**: A claim about how quickly the product takes effect. May be explicit ("works in 30 minutes") or implicit ("fast-acting relief").

**Examples**:
- CN: "5 分钟快速缓解酸痛"
- EN: "Noticeable results in as little as 2 weeks"

**Extraction method**: Extract the time frame and the specific effect expected within that time. Note whether the timing applies to everyone or is qualified ("in as little as", "up to", "within").

**Risk points**:
- Onset varies by individual; unqualified timing claims overpromise.
- "Fast-acting" without specific timing is vague but still implies a speed benefit that must be supported.
- Rapid onset claims for dietary supplements are often unsupported.
- Confusion between subjective perception (feeling) and objective onset (measurable biomarker change).
- Comparison to competitor onset speed invites comparative claim scrutiny (Category 13).

**Required supporting evidence**:
- Pharmacokinetic or pharmacodynamic data for the specific formulation.
- Clinical studies reporting time-to-effect for the specific product.
- At minimum: published data on the active ingredient's absorption kinetics.
- Unsupported timing claims should be classified as unsupported.

---

## 6. Effect Magnitude

**Definition**: A claim about the size, degree, or extent of the product's effect. Often uses numbers, percentages, or comparative language.

**Examples**:
- CN: "吸收率提高 3 倍"
- EN: "85% of users reported improved energy within 4 weeks"

**Extraction method**: Extract the numerical value and the comparator. "3x more X than Y" — record numerator (3x), metric (absorption rate), comparator (Y). For survey/study claims, record the percentage and the population.

**Risk points**:
- Numbers can be cherry-picked (best-case subgroup, not the overall population).
- "Up to X%" means the typical result may be far lower.
- Multiple comparison framing (better than what? Placebo? Competitor? Baseline?).
- Small absolute differences can be reported as large relative differences.
- In-vitro results presented as in-vivo magnitude.
- Survey results from non-representative samples.

**Required supporting evidence**:
- Full study results, not just the highlighted number.
- Effect size with confidence intervals.
- Clinical relevance (statistical significance is not the same as clinical significance).
- Context for comparator (placebo-controlled? baseline-controlled?).

---

## 7. Target Population

**Definition**: A claim that the product is specifically designed for, or particularly suitable for, a defined group of people. Based on demographic, physiologic, or lifestyle characteristics.

**Examples**:
- CN: "专为 50 岁以上中老年人设计"
- EN: "Formulated for pregnant and nursing women"

**Extraction method**: Extract the target population definition and the basis for the targeting. Note whether adapted (e.g., "smaller pill for seniors") or claimed as exclusive benefit.

**Risk points**:
- Population-specific claims need population-specific evidence.
- Pediatric claims require pediatric clinical data.
- Claims targeting vulnerable populations (elderly, pregnant women, children) face heightened regulatory scrutiny.
- Exclusivity claims ("only formula for X") require proof of uniqueness.
- Cultural note: "middle-aged and elderly" (中老年) is a common Chinese market segment but has varying definitions.

**Required supporting evidence**:
- Clinical data from the specific population group.
- For pregnancy: established safety data in pregnancy (often limited).
- For age-specific: age-stratified efficacy or safety data.
- Formulation rationale (different dose, different delivery system, different ingredients).

---

## 8. Expert Endorsement

**Definition**: A claim that a medical professional, scientist, institution, or organization recommends, endorses, or developed the product. Includes doctor-recommended claims, professional association seals, and "developed by" statements.

**Examples**:
- CN: "三甲医院皮肤科医生推荐"
- EN: "Recommended by 9 out of 10 dentists"

**Extraction method**: Identify the endorser, their qualification or institution, and the endorsement statement. Distinguish between paid endorsement, independent recommendation, and institutional approval.

**Risk points**:
- "Doctor recommended" surveys often use small, non-representative samples.
- Endorsement by a single doctor is not endorsement by the medical profession.
- Paid endorsements may not be disclosed (FTC endorsement guidelines).
- Institutional logos (hospital crests, university seals) imply institutional endorsement, which may not exist.
- Fake or misleading credentials ("Dr." for someone without an MD).
- Endorsement may be historical and no longer current.

**Required supporting evidence**:
- Documentation of the endorsement (signed statement, contract, video).
- For surveys: full methodology and sample size.
- For institutional endorsement: official letter or agreement.
- Verification of endorser credentials against professional registries.
- Currency check (is the endorsement still active?).

---

## 9. Technology or Process

**Definition**: A claim about a proprietary technology, manufacturing process, delivery system, or scientific approach used in the product. Often positions the product as more advanced or innovative.

**Examples**:
- CN: "采用微胶囊包埋技术，确保活性成分直达肠道"
- EN: "Patented liposomal delivery system for maximum bioavailability"

**Extraction method**: Extract the technology name, the claimed benefit of the technology, and any patent or trademark references. Distinguish between genuine proprietary technology and commonly available processes branded with trade names.

**Risk points**:
- "Patented" does not mean clinically superior — a patent covers novelty, not efficacy.
- Technology names may be marketing inventions (a trademark, not a technology).
- Common processes (liposomes, microencapsulation) branded as unique.
- Vague "scientific process" claims without specifics.
- Process claims need process validation data, not just ingredient data.

**Required supporting evidence**:
- Patent number (and confirmation the patent covers the specific product).
- Comparative bioavailability or stability data for the technology vs. standard.
- Published research on the specific delivery system.
- Manufacturing documentation (if available).
- For unpatented proprietary processes: independent validation of the claimed benefit.

---

## 10. Natural or Pure

**Definition**: A claim that the product is natural, organic, pure, clean, free from synthetic ingredients, or otherwise positioned as closer to nature. Includes "no artificial" claims and "organic" certifications.

**Examples**:
- CN: "100% 天然成分，无添加"
- EN: "Pure, organic, non-GMO, and free from artificial colors or preservatives"

**Extraction method**: Extract all purity and naturalness descriptors. Record whether the claim covers all ingredients or only some. Note certification logos (USDA Organic, EU Organic Leaf, Chinese Green Food, Non-GMO Project).

**Risk points**:
- "Natural" is not legally defined in many markets — widely abused.
- "Chemical-free" is scientifically meaningless (everything is a chemical).
- Natural ≠ effective (Category 2 risk).
- Natural ≠ safe (Category 4 risk).
- Partial natural claims ("made with natural ingredients") may coexist with significant synthetic content.
- Certification claims without certification numbers.

**Required supporting evidence**:
- Third-party certification documentation (certificate, license number).
- Ingredient sourcing documentation.
- For organic: organic certificate from an accredited certifier.
- For "no artificial": complete ingredient list showing no synthetic additives.
- Pure/clean claims are almost impossible to fully substantiate in absolute terms.

---

## 11. Clinical-Study Backing

**Definition**: A claim that the product (or its ingredients) is supported by clinical research, studies, or trials. Often phrased as "clinically proven", "backed by science", or references to specific studies.

**Examples**:
- CN: "经临床试验证明，28 天显著改善皮肤弹性"
- EN: "Clinically proven to reduce hair thinning in 12 weeks"

**Extraction method**: Capture the clinical claim and any study identifiers (NCT number, publication reference, institution name). Distinguish between:
- Product-specific clinical studies.
- Ingredient-level clinical studies (often presented as product-level).
- In vitro or animal studies presented as human clinical evidence.
- Preprint/unpublished studies.

**Risk points**:
- "Clinically proven" is often a claim about ingredient-level research, not the specific formulation.
- Studies may be small, short-term, or uncontrolled.
- Publication in a predatory journal is not valid clinical evidence.
- Results of one study do not equal "scientifically proven."
- Selective reporting — highlighting positive outcomes, burying negative or null results.
- Studies may have been funded by the manufacturer (not inherently invalid, but must be disclosed).

**Required supporting evidence**:
- Full study protocol and results (not just abstract or press release).
- Verification of study registration (ClinicalTrials.gov, ChiCTR, etc.).
- Peer-reviewed publication in a legitimate journal.
- Study design assessment: RCT > controlled trial > open-label > before-after.
- Distinguish: direct (product tested), partial (ingredient tested), indirect (mechanism tested), unsupported (no study found), contradicted (study shows no effect).

---

## 12. Ranking or Sales

**Definition**: A claim about the product's market position, popularity, sales volume, or ranking. Includes "bestseller", "#1 rated", "market leader", and specific sales figures.

**Examples**:
- CN: "天猫销量第一*
- EN: "#1 doctor-recommended brand for joint health"

**Extraction method**: Capture the exact ranking or sales statement, the claimed scope, the source, and any qualifiers (asterisks, footnotes, time period). The asterisk and footnote must be extracted and investigated.

**Risk points**:
- "#1" is often qualified by very narrow scope (#1 in a specific micro-category on a specific platform in a specific month).
- Sales claims from third-party platforms may not be independently verifiable.
- Historical rankings presented as current.
- Paid rankings or "editor's choice" that are actually advertisements.
- Self-reported sales data without audit.
- Category definition manipulation (narrow category to claim #1).
- Platform-specific rankings may be based on unspecified criteria.

**Required supporting evidence**:
- Platform-provided ranking data (if available).
- Third-party market research (Nielsen, Mintel, iResearch, etc.).
- Seller claims of sales volume require audited financial statements.
- For "doctor recommended": the full survey methodology (sample size, question wording, population).
- If no external verification is possible, classify as unsupported.

---

## 13. Comparative Claim

**Definition**: A claim that directly compares the product to another product, brand, category, or baseline. Includes both superiority claims ("better than") and parity claims ("as good as").

**Examples**:
- CN: "效果比普通维生素 C 高 50%"
- EN: "Works better than the leading competitor brand"

**Extraction method**: Identify the comparison target (named brand, unnamed "leading brand", previous version, baseline), comparison metric (efficacy, price, absorption, taste), and direction of comparison (superior, equivalent, inferior). Distinguish between explicit and implied comparisons.

**Risk points**:
- Comparative claims require head-to-head clinical data, not separate studies.
- Unnamed comparators ("better than the leading brand") are unverifiable.
- Price comparisons may use non-comparable formats (per unit vs. per serving, different package sizes).
- Regulatory scrutiny is higher for comparative claims (FTC, ASA, SAT).
- "New and improved" claims imply a prior inferior version.
- Comparative claims can trigger competitor legal action.
- EU comparative advertising directive requires objective, verifiable comparisons.

**Required supporting evidence**:
- Head-to-head clinical trial (for efficacy comparisons).
- Identical methodology applied to both products.
- For equivalence claims: statistical non-inferiority test.
- For price comparisons: same-unit, same-time comparison with methodology.
- For market comparisons: third-party market data.

---

## 14. User Testimonial

**Definition**: A claim presented as a personal experience, review, or endorsement from a consumer who has used the product. Includes before-and-after photos, star ratings, written reviews, and video testimonials.

**Examples**:
- CN: "用了两周，血糖明显下降，感觉好多了" — 用户张先生
- EN: "I lost 15 pounds in one month with this product!" — verified buyer

**Extraction method**: Extract the testimonial text, the author identifier (name, username, "verified buyer" badge), date, and any supporting media (photos, videos). Note whether the testimonial is from a platform review or a curated marketing testimonial.

**Risk points**:
- **Testimonials are NOT evidence of efficacy.** Individual results are not generalizable.
- Anecdotal reports cannot replace controlled clinical data.
- Before-and-after photos may be staged, edited, or from different people.
- "Results may vary" disclaimers do not protect against misleading claims.
- Paid testimonials must be disclosed (FTC endorsement guidelines).
- Fake or incentivized reviews are common on ecommerce platforms.
- Extreme results in testimonials (rapid weight loss, dramatic cures) are red flags for regulatory violation.
- Testimonials mentioning disease treatment cross into Category 3.

**Required supporting evidence**:
- Testimonials alone support nothing beyond narrative analysis. See consumer-content-rules.md.
- For marketing testimonials: documentation that the experience is genuine and representative.
- For platform reviews: aggregate patterns (not individual stories) can inform consumer narrative analysis.
- Never use a testimonial as proof of efficacy or safety.
- If a testimonial claims disease treatment, flag as regulatory violation regardless of how compelling the story is.

---

## Claim Support Classifications

Every claim, once paired with evidence, must be classified using the following five-tier system:

| Classification | Meaning | What is required |
|---|---|---|
| **Direct** | The specific product was tested in a study that supports the claim | RCT or controlled trial using the commercial product exactly as sold |
| **Partial** | A similar formulation, the active ingredient, or a related product was tested | Ingredient-level study, or different dose/form used in research |
| **Indirect** | The claim is supported by established mechanism or related research, but not the product itself | Mechanistic studies, biomarker rationale, epidemiological data |
| **Unsupported** | No credible evidence was found that supports the claim | After systematic search, no relevant study exists |
| **Contradicted** | Existing evidence directly refutes the claim | Negative RCT, meta-analysis showing no effect, regulatory warning |

### Classification rules

- Default classification is **unsupported** — the burden is on establishing support.
- A single positive study does not override a body of contradictory evidence. When conflicts exist, preserve both in the `conflict` record (see `output-record-specification.md`).
- Commercial claims are separate from evidence; a well-supported claim can still fail regulatory compliance (e.g., a disease treatment claim on a supplement is illegal even with strong evidence).
- Reclassify when new evidence becomes available. Claim support is not static.

---

## Quick Reference: Mapping Claims to Evidence Types

| Category | Minimum Evidence | Strong Evidence | Typical Classification |
|---|---|---|---|
| Ingredient Fact | Label/label image | 3rd-party lab analysis | Direct (if label matches) |
| Efficacy | Plausible mechanism | Product-specific RCT | Partial to Direct |
| Disease Treatment/Prevention | N/A (regulatory violation for supplements) | Approved label (for pharma) | Unsupported or Contradicted for supplements |
| Safety | Published safety data | Clinical AE data + post-market surveillance | Partial to Direct |
| Onset Speed | PK/PD data on ingredient | Product-specific time-to-effect study | Unsupported to Partial |
| Effect Magnitude | Ingredient-level effect size | Product-specific RCT with CI | Partial to Direct |
| Target Population | Population rationale | Population-stratified RCT | Unsupported to Direct |
| Expert Endorsement | Endorsement contract | Independent institutional endorsement | Unsupported to Direct |
| Technology/Process | Patent or trademark | Comparative bioavailability data | Unsupported to Partial |
| Natural/Pure | Ingredient list | Certification documents | Unsupported to Direct |
| Clinical-Study Backing | Study identifier | Full published RCT | Check actual study: Direct to Contradicted |
| Ranking/Sales | Platform ranking | 3rd-party market report | Unsupported to Direct |
| Comparative Claim | Ingredient-level comparison | Head-to-head RCT | Unsupported to Partial |
| User Testimonial | Individual review | Representative survey with controls | Unsupported (never claim-level evidence) |

---

## Taxonomy Use in the Research Workflow

1. **Extraction phase**: Classify each extracted claim into one or more categories. A single statement may span multiple categories (e.g., "clinically proven to reduce LDL by 15% in 8 weeks" spans Categories 3, 5, 6, and 11).

2. **Evidence phase**: For each categorized claim, search for supporting evidence. Use the classification tier (Direct/Partial/Indirect/Unsupported/Contradicted) to assign a support level.

3. **Verification phase**: Separate commercial claims from verified facts. A claim with Direct support can become a verified fact; a claim with Unsupported or Contradicted status remains an unverified assertion.

4. **Report phase**: Present claims alongside their support level. Never present an unsubstantiated commercial claim as fact.

---

## Regulatory Framework Quick Reference

| Market | Key Regulator | Relevant Rules |
|---|---|---|
| US | FDA, FTC | DSHEA 1994, FDCA §403(r)(6), FTC substantiation doctrine |
| EU | EFSA, National agencies | Nutrition and Health Claims Regulation (EC) No 1924/2006 |
| UK | MHRA, ASA | TCHR 2005, CAP Code |
| China | NMPA, SAMR | Food Safety Law, Advertising Law, GB 28050, GB 7718 |
| Japan | MHLW, CAA | FOSHU system, Health Promotion Act, Pharmaceutical and Medical Device Act |
| Australia | TGA | Therapeutic Goods Advertising Code |
| Canada | Health Canada | Natural Health Products Regulations, Food and Drugs Act |

---

*This taxonomy is part of the product-market-research skill. Last updated: 2025-06-20.*
