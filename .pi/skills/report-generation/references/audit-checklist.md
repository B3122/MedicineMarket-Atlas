# Audit Checklist

Comprehensive verification checklist for pharmaceutical and health-product
market research reports. Use this checklist after report generation and before
delivery. An independent auditor must be able to apply every check item using
only the report, its cited artifacts, and the source inventory.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: SKILL.md lines 353-368 (final self-check), SKILL.md lines
370-383 (audit preparation), schemas/audit.schema.json (audit finding record
structure), calibrated-language.md (language rules), quantitative-reporting-rules.md
(calculation verification), evidence-appraisal SKILL.md Step 12 (certainty).

---

## Table of Contents

1. [Numbers match sources](#1-numbers-match-sources)
2. [Citations exist in source inventory](#2-citations-exist-in-source-inventory)
3. [Product identity is consistent](#3-product-identity-is-consistent)
4. [Claims are properly classified](#4-claims-are-properly-classified)
5. [Calculations are correct](#5-calculations-are-correct)
6. [Conflicts of interest are disclosed](#6-conflicts-of-interest-are-disclosed)
7. [Limitations are stated](#7-limitations-are-stated)
8. [Regulatory conclusions are supported](#8-regulatory-conclusions-are-supported)
9. [Price data is current](#9-price-data-is-current)
10. [Dose information is verified](#10-dose-information-is-verified)
11. [Competitor selection is justified](#11-competitor-selection-is-justified)
12. [Report scope matches brief](#12-report-scope-matches-brief)
13. [Audit decision and severity classification](#13-audit-decision-and-severity-classification)
14. [Audit rules and prohibitions](#14-audit-rules-and-prohibitions)

---

## Severity classification

Every audit finding is assigned one of four severity levels. Use these
definitions consistently across all categories:

| Severity | Definition | Audit outcome effect |
|----------|------------|---------------------|
| **Critical** | The finding materially affects a conclusion, recommendation, or compliance determination. A reader relying on the report would be misled. | Blocks report delivery. Must be corrected before any further use of the report. |
| **Major** | The finding affects the accuracy or completeness of a substantive section but does not independently change a conclusion. | Must be corrected before final delivery. Report may proceed internally with the finding flagged. |
| **Minor** | The finding affects presentation quality, formatting, or minor data points but not substantive content. | Should be corrected. May be delivered with the finding documented if time-constrained. |
| **Info** | The finding identifies a potential improvement or documents a limitation that does not constitute an error. | No correction required. Record for continuous improvement. |

---

## 1. Numbers match sources

### 1.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 1.1 | Every numeric value in the report body matches its cited source within rounding tolerance. | For each numeric statement with a source citation, retrieve the source value from the source inventory. Verify equality within the rounding tolerance stated in quantitative-reporting-rules.md section 5. |
| 1.2 | Every table cell containing a numeric value is traceable to a source or formula statement. | Inspect every table. For each numeric cell, verify that a source citation or formula statement is present in the same row, column header, or table footnote. |
| 1.3 | No numeric value is presented without units. | Scan the report for bare numbers. Every number representing a quantity, price, dose, percentage, ratio, or rate must have an associated unit. |
| 1.4 | Currency values include the ISO 4217 currency code. | Verify that every price or cost value includes or is immediately adjacent to a three-letter ISO 4217 currency code. |
| 1.5 | Percentage values distinguish absolute percentages from relative percentage changes. | For each percentage, verify whether it represents an absolute proportion or a relative change. The report must make this distinction explicit. |
| 1.6 | Confidence intervals, standard deviations, and standard errors are correctly labeled. | Verify that every interval or error value specifies whether it is a CI, SD, or SE. Verify that the CI level is stated (e.g., 95% CI). |

### 1.2 Severity if failed

- 1.1, 1.2, 1.3: **Critical** — the report presents unverifiable or erroneous data
- 1.4: **Major** — currency ambiguity can lead to misinterpretation
- 1.5, 1.6: **Minor** — labeling ambiguity does not necessarily mislead but impairs auditability

### 1.3 Correction procedure

For each numeric mismatch:

1. Identify the correct value from the source
2. Replace the erroneous value in the report
3. Verify that all dependent calculations (other cells, derived metrics, comparisons) are recalculated with the corrected value
4. Re-run the full numeric traceability check for all values derived from the corrected source

---

## 2. Citations exist in source inventory

### 2.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 2.1 | Every source cited in the report has a corresponding entry in the project source inventory. | Extract all source references from the report. Cross-reference each against the source inventory. Flag any cited source that has no inventory entry. |
| 2.2 | Every source inventory entry cited in the report is complete: source ID, type, URL or identifier, collection date, and access date. | For each cited source, verify that the inventory entry contains all required fields per output-record-specification.md. |
| 2.3 | No source is cited for a statement it does not support. | For each citation, verify that the cited source actually contains the information attributed to it. This is a spot-check: sample 10% of citations, minimum 5. If any fail, expand to 100%. |
| 2.4 | Every table has source attribution for its data. | Verify that each data table includes a footnote or caption identifying the source(s) of the data. |
| 2.5 | No abstract-only source is represented as full-text verified. | For each cited study, verify the access level recorded in the source inventory. If the inventory indicates "abstract only," verify that the report does not cite detailed methods or results that only appear in the full text. |

### 2.2 Severity if failed

- 2.1, 2.3: **Critical** — unsupported attribution or missing sources undermine report credibility
- 2.2, 2.5: **Major** — incomplete source records impair auditability; abstract-only misrepresentation misleads
- 2.4: **Minor** — missing table attribution impairs traceability

### 2.3 Correction procedure

For each missing or incorrect citation:

1. Locate the correct source in the inventory or add it if missing
2. Verify that the source supports the attributed statement
3. Update the citation in the report
4. If the source does not support the statement, either remove the statement or replace it with a statement that the source does support

---

## 3. Product identity is consistent

### 3.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 3.1 | The target product identity (brand, name, formulation, dose, package size) is consistent across all sections. | Search the report for all instances of the product name. Verify that the formulation, dose, and package size are identical in every mention. |
| 3.2 | Product versions or regional variants are not conflated. | If the project involves multiple product versions or regional variants, verify that each is identified separately and that comparisons do not mix their attributes. |
| 3.3 | Competitor products are identified with the same level of detail as the target product. | Verify that each competitor entry includes brand, name, formulation, dose, and package size. Flag any entry with missing fields. |
| 3.4 | Product names used in tables match product names used in narrative text. | Cross-check product names between tables and narrative. Flag any inconsistency. |
| 3.5 | Products with similar names are not merged or confused. | For any pair of products with similar names, verify that they have distinct source records and that the report distinguishes them correctly. |

### 3.2 Severity if failed

- 3.1, 3.2, 3.5: **Critical** — mixing product versions or identities can invalidate all comparisons and conclusions
- 3.3: **Major** — incomplete competitor identity impairs comparison validity
- 3.4: **Minor** — naming inconsistency is a presentation defect

### 3.3 Correction procedure

1. Reconcile product identities against the normalized product records
2. Update all inconsistent references to use the canonical identification
3. If a product version mismatch is found, recalculate all comparisons involving that product
4. If two products were improperly merged, separate them and re-run the competitor analysis

---

## 4. Claims are properly classified

### 4.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 4.1 | Every commercial claim in the report is explicitly labeled as a claim from the seller or manufacturer. | Scan the report for statements that describe product benefits, effects, or qualities. Verify that each claim attributed to a commercial source is labeled as `[CLAIM]` or introduced with "The seller stated," "The manufacturer claims," or equivalent. |
| 4.2 | No commercial claim is presented as scientific evidence. | Verify that no `[CLAIM]` is used as the basis for a conclusion about efficacy, safety, or comparative superiority. |
| 4.3 | Consumer narratives are labeled as `[NARRATIVE]` and are not used to support efficacy claims. | Scan for statements about consumer experiences or reviews. Verify labeling and ensure they are presented as consumer perspectives, not as evidence of product performance. |
| 4.4 | Scientific findings are labeled as `[EVIDENCE]` and include study design, population, and limitations. | For each scientific finding, verify that it includes the study design, population, and relevant limitations. |
| 4.5 | Analyst interpretations are labeled as `[INTERPRETATION]` and are not presented as facts. | Scan for interpretive language ("may indicate," "could suggest," "this pattern"). Verify labeling. |
| 4.6 | Ingredient evidence and finished-product evidence are distinguished. | Verify that evidence for an ingredient is not presented as evidence for the finished product. Check section headings, table labels, and narrative framing. |

### 4.2 Severity if failed

- 4.1, 4.2, 4.3: **Critical** — misclassifying claims as evidence misleads readers about product substantiation
- 4.4, 4.6: **Major** — incomplete labeling or ingredient/product conflation weakens evidence quality assessment
- 4.5: **Minor** — unlabeled interpretation is a presentation defect if the interpretive nature is otherwise clear

### 4.3 Correction procedure

1. For each misclassified statement, apply the correct label from calibrated-language.md section 2
2. Rewrite framing language to match the statement type
3. If a commercial claim was used as evidence, remove the evidence-based conclusion and replace with "the seller claims [X]; independent verification of this claim was not found"
4. If consumer narratives were used as evidence, demote them to consumer perspectives and strengthen the limitation about consumer-generated content

---

## 5. Calculations are correct

### 5.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 5.1 | Daily cost values are correct given the stated price, package quantity, and daily dose. | For each daily cost in the report, recompute using the stated inputs. Verify within 2-decimal rounding tolerance. |
| 5.2 | Price per unit values are correct given the stated price and package quantity. | For each unit price, recompute. Verify within 4-decimal rounding tolerance. |
| 5.3 | AI-normalized prices use correct base units and conversion factors. | For each normalized price, verify that the per-unit dose is correctly converted to the base unit (mg, mL) and that the division is correct. |
| 5.4 | Percentage changes use the correct base value. | For each percentage difference, verify the formula: `((new - old) / old) * 100`. Verify that the denominator is the reference value stated in the report. |
| 5.5 | Rounding follows the rules in quantitative-reporting-rules.md section 5. | Verify each calculated value against its prescribed rounding rule. Flag any deviation. |
| 5.6 | Chained rounding has not been applied. | For multi-step calculations, verify that intermediate values were preserved at full precision and only the final value was rounded. |
| 5.7 | Calculations do not use incompatible price types. | For each calculation involving prices, verify that all price inputs use the same price type. Flag any mixing of list, sale, member, or live prices. |
| 5.8 | Daily cost calculations use accepted dose sources only. | Verify that the daily dose used in each daily cost calculation comes from a label, official website, clinical guideline, or regulatory filing. Reject calculations based on consumer reviews, seller recommendations, or assumptions unless explicitly documented and flagged. |

### 5.2 Severity if failed

- 5.1, 5.2, 5.7, 5.8: **Critical** — incorrect or improperly sourced daily cost or unit price invalidates cost comparisons
- 5.3, 5.4: **Major** — normalization or percentage errors affect comparative analysis
- 5.5, 5.6: **Minor** — rounding deviations affect presentation precision but rarely change conclusions

### 5.3 Correction procedure

1. Recalculate the value using the correct formula, inputs, and rounding rules
2. Replace the erroneous value in the report
3. Recompute all dependent values (comparisons, rankings, tables)
4. Document the correction in the audit findings record
5. Re-run calculation verification for all corrected values

---

## 6. Conflicts of interest are disclosed

### 6.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 6.1 | Study funding sources are disclosed for every cited study. | For each study cited as evidence, verify that the funding source is stated (from the study disclosure or conflict-of-interest statement). Flag any study where funding is not disclosed. |
| 6.2 | Studies funded by the product manufacturer are identified. | For each cited study, check whether the funder is the manufacturer of the product under review or a competitor. Flag any manufacturer-funded study that is not explicitly identified as such. |
| 6.3 | Author conflicts of interest from the original publications are noted. | For key studies (those supporting primary conclusions), verify that author COI declarations are captured. Flag any undisclosed relevant COI. |
| 6.4 | The report itself includes a conflict-of-interest statement for the research team. | Verify that the report includes a statement about the research team's relationship to any of the products or companies reviewed. |
| 6.5 | Commercial sources (manufacturer websites, seller pages) are distinguished from independent sources. | Verify that commercial sources are labeled as such in the source inventory and that the report does not treat them as independent verification. |

### 6.2 Severity if failed

- 6.1, 6.2: **Major** — undisclosed funding impairs evidence credibility assessment
- 6.3, 6.5: **Minor** — undisclosed COI or source type impairs transparency
- 6.4: **Info** — absence of a research team COI statement is a transparency gap

### 6.3 Correction procedure

1. Retrieve funding and COI information from the original publication or trial registry
2. Add the disclosure to the evidence table or source inventory
3. Add a note in the report where manufacturer-funded evidence is cited: "[Note: this study was funded by the manufacturer.]"
4. Add or complete the research team COI statement

---

## 7. Limitations are stated

### 7.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 7.1 | A dedicated Limitations section exists and is not a generic single paragraph. | Verify that the report includes a Limitations section that addresses at least 5 distinct limitations relevant to the specific research. |
| 7.2 | Limitations address the specific research methods used, not generic research constraints. | Review the limitations against the methods section. Each limitation must reference a specific methodological constraint of this project. Generic limitations ("all research has limitations") do not satisfy this check. |
| 7.3 | At minimum, the following categories are considered (mark as addressed or missing): dynamic prices, inaccessible pages, incomplete product identity, seller-generated content, temporal mismatch, regional version differences, publication access, incomplete literature coverage, language restrictions, lack of direct product evidence, absence of independent market data, automated extraction errors. | Review the limitations section against this list from SKILL.md section on Limitations. Flag each category that is applicable but not addressed. |
| 7.4 | Limitations affect the strength of conclusions. | For each major conclusion, verify that the relevant limitation is acknowledged and that the conclusion is appropriately qualified. Flag any unqualified conclusion that depends on limited data. |
| 7.5 | Limitations are reflected in the executive summary. | Verify that the executive summary mentions the most important limitations, not just the positive findings. |

### 7.2 Severity if failed

- 7.1: **Critical** — absence of a limitations section is a fundamental report integrity defect
- 7.4, 7.5: **Major** — unqualified conclusions or executive summaries misrepresent the report's certainty
- 7.2, 7.3: **Minor** — incomplete limitation coverage impairs transparency but may not mislead

### 7.3 Correction procedure

1. For each missing limitation, draft a specific limitation statement that references the actual project constraint
2. Insert into the Limitations section
3. For each affected conclusion, add the appropriate qualification
4. Update the executive summary to reflect the most important limitations
5. Re-verify that no conclusion overstates certainty after the qualifications are added

---

## 8. Regulatory conclusions are supported

### 8.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 8.1 | Every regulatory status claim cites a specific regulatory authority and a verifiable source. | For each statement about regulatory status (approved, registered, not approved, classified as), verify that the specific authority name and source are cited. |
| 8.2 | The regulatory jurisdiction is stated for every regulatory claim. | Verify that the country or region of the regulatory authority is explicitly stated. Flag any "approved" claim without jurisdiction. |
| 8.3 | Regulatory status is distinguished from scientific evidence. | Verify that regulatory approval is not presented as scientific proof of efficacy. A product can be registered as a supplement without efficacy evidence. |
| 8.4 | Regulatory classifications use official authority terminology. | Verify that terms like "drug," "medical device," "health supplement," "cosmetic" match the official classification used by the cited authority, not the seller's description. |
| 8.5 | Regulatory findings are dated. | Verify that every regulatory status statement includes the date of the determination or the date the regulatory database was checked. A regulatory status can change. |
| 8.6 | Claims about what a product "can" or "cannot" do legally are supported by the relevant regulation. | For any statement about legal permissibility (e.g., "cannot claim to treat disease"), verify it is supported by a cited regulation or regulatory guidance. |

### 8.2 Severity if failed

- 8.1, 8.2, 8.4: **Critical** — unsupported or jurisdiction-ambiguous regulatory claims can create legal risk for report users
- 8.3: **Major** — conflating registration with efficacy evidence misleads about product substantiation
- 8.5, 8.6: **Minor** — missing date or incomplete legal reference impairs precision

### 8.3 Correction procedure

1. Retrieve the correct regulatory status from the regulatory source map or official database
2. Update the report with the specific authority, jurisdiction, classification, and date
3. Remove any efficacy implication drawn from regulatory status alone
4. If a regulatory status cannot be verified, state "regulatory status in [jurisdiction] could not be confirmed" rather than omitting the information

---

## 9. Price data is current

### 9.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 9.1 | Every price in the report includes a collection date. | Scan the report for price values. Verify each is accompanied by a collection date (YYYY-MM-DD). |
| 9.2 | The collection date is within the freshness window defined in the project brief or config. | Compare collection dates to the freshness requirement. Flag any price older than the maximum age specified in the project configuration. If the project does not specify, flag prices older than 30 days. |
| 9.3 | Price types are consistent across comparisons. | Verify that all prices in a comparison table use the same price type. Flag any mixing. |
| 9.4 | Live-stream prices are excluded from standard price comparisons. | Verify that no live-stream price appears in a standard price comparison table. If live prices are present, verify they are in a separate, labeled section. |
| 9.5 | Promotion conditions are documented for promotional prices. | For coupon, member, bundle, and subscription prices, verify that the condition (e.g., "PLUS member," "buy 3 get 1") is documented. |

### 9.2 Severity if failed

- 9.1, 9.3: **Critical** — undated or mixed-type prices invalidate price comparisons
- 9.2, 9.4: **Major** — stale prices or live-price contamination can mislead market assessment
- 9.5: **Minor** — undocumented promotion conditions impair reproducibility

### 9.3 Correction procedure

1. For missing dates, retrieve the collection date from the source inventory
2. For stale prices, either recollect the price or add a prominent note: "Price data collected on [date] may not reflect current pricing"
3. For mixed price types, select a consistent price type across all compared products per the hierarchy in pricing-normalization.md section 13
4. Remove live prices from standard comparisons and relocate to a dedicated section

---

## 10. Dose information is verified

### 10.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 10.1 | The per-unit dose of the active ingredient is stated for every product where dose-based comparison is performed. | Verify that each product in a dose-normalized comparison has a stated per-unit dose (e.g., "500 mg per tablet"). |
| 10.2 | The source of the dose information is identified (label, official website, regulatory filing). | Verify that the dose source is stated. Flag any dose without a source. |
| 10.3 | Daily dose used in daily cost calculations comes from an accepted source. | Verify against the accepted dose source hierarchy in quantitative-reporting-rules.md section 2.5. |
| 10.4 | Consumer reviews or seller recommendations are not used as dose sources. | Scan dose attributions. Flag any dose attributed to consumer reviews or non-label seller statements. |
| 10.5 | Dose ranges are reported as ranges, not collapsed to midpoints. | For products with a dosage range, verify that both low and high values are reported. Flag any midpoint presented as a single value without explicit documentation. |
| 10.6 | Dose units are normalized to base units (mg, mL, count) for comparison. | Verify that dose comparisons use a common base unit. Flag comparisons that mix mg and g, or mL and L, without conversion. |

### 10.2 Severity if failed

- 10.1, 10.3, 10.4: **Critical** — missing, unverified, or consumer-sourced dose information undermines daily cost and any dose-dependent conclusion
- 10.2, 10.5, 10.6: **Major** — unsourced or improperly handled dose data impairs comparison validity

### 10.3 Correction procedure

1. Retrieve the correct dose from the highest-priority available source: label > official website > clinical guideline > regulatory filing
2. If no accepted source is available, remove the dose-dependent calculation and replace with "daily dose not available from accepted source"
3. Update all dependent calculations (daily cost, AI-normalized price)
4. Add the dose source to the product record and report

---

## 11. Competitor selection is justified

### 11.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 11.1 | Competitor inclusion criteria are stated in the methods section. | Verify that the report states the criteria used to select competitors (e.g., same active ingredient, same indication, same price tier, same channel). |
| 11.2 | Each included competitor meets the stated inclusion criteria. | Cross-check each competitor against the inclusion criteria. Flag any that do not meet the stated criteria. |
| 11.3 | Notable products that meet the inclusion criteria but were excluded are acknowledged. | Review the competitor analysis methods. If the search was constrained (e.g., only top-N results, only one platform), verify that this is stated. Flag any known competitor that meets criteria but is absent without explanation. |
| 11.4 | Competitors are not selected to produce a favorable comparison. | Review the competitor set for selection bias. If all competitors are higher-priced, weaker-formulated, or lower-rated, investigate whether the selection method was biased. |
| 11.5 | The number of competitors is sufficient for the report type. | For a quick competitor review: minimum 3. For a full market review: minimum 5, or an explanation of why fewer exist. |

### 11.2 Severity if failed

- 11.1, 11.4: **Critical** — unstated or biased selection criteria invalidate the competitor analysis
- 11.2, 11.3: **Major** — criterion violations or unexplained exclusions impair the analysis scope
- 11.5: **Minor** — small competitor sets are acceptable if justified

### 11.3 Correction procedure

1. If criteria are not stated, document the actual criteria used and add them to the methods section
2. Remove any competitor that does not meet the criteria, or expand the criteria if justified
3. Add acknowledgment of excluded notable products with reasons
4. If selection bias is suspected, expand the competitor search and re-run the analysis
5. If the competitor set is too small, document the reason and flag it as a limitation

---

## 12. Report scope matches brief

### 12.1 Check items

| ID | Check | Method |
|----|-------|--------|
| 12.1 | The report answers the research question stated in the project brief. | Read the brief's research question. Verify that the report's conclusion section directly addresses it. Flag any mismatch. |
| 12.2 | The report scope (geographic, temporal, product category) matches the brief. | Compare the scope stated in the report methods to the scope in the brief. Flag any deviation. |
| 12.3 | The reporting mode (quick, full, evidence, claim-substantiation) matches the mode requested. | Verify that the report architecture and emphasis match the requested mode as defined in SKILL.md section on Reporting modes. |
| 12.4 | All deliverables specified in the brief are present. | Cross-check the brief's deliverable list against the report output. Flag any missing deliverable. |
| 12.5 | The report does not introduce scope not requested in the brief without justification. | Verify that additional analysis, products, or markets beyond the brief scope are either explicitly requested in the brief or justified in the report. |
| 12.6 | The report does not contain placeholder text (e.g., "TODO," "[insert]," "TBD"). | Scan the report for placeholder markers. Flag any found. |

### 12.2 Severity if failed

- 12.1, 12.2, 12.4: **Critical** — a report that does not answer the research question or deliver requested content fails its primary purpose
- 12.3, 12.6: **Major** — wrong mode or placeholder content impairs usability
- 12.5: **Minor** — scope expansion may be acceptable if justified and noted

### 12.3 Correction procedure

1. Map the brief requirements to report sections and identify any missing content
2. Draft missing sections using available project artifacts
3. Remove content outside the brief scope or add explicit justification for its inclusion
4. Replace all placeholder text with actual content or remove the section
5. Re-run the scope match check after correction

---

## 13. Audit decision and severity classification

### 13.1 Pass/fail criteria

The audit result is determined by the highest-severity unresolved finding:

| Highest unresolved finding | Audit decision |
|---------------------------|----------------|
| No findings, or only Info findings | **Pass** |
| Minor findings only | **Pass with minor revisions** — corrections recommended but not blocking |
| One or more Major findings | **Pass with major revisions** — corrections required before final delivery |
| One or more Critical findings | **Fail — requires major revision** — report must not be delivered until all critical findings are resolved |

### 13.2 Audit report format

The audit report must include:

1. Audit date and auditor identification
2. Summary of findings by severity (count of Critical, Major, Minor, Info)
3. Detailed findings list: each finding with category, check ID, severity, description, and correction procedure
4. Pass/fail decision with justification
5. List of resolved findings (if re-auditing after corrections)
6. List of unresolved findings with blocking status

### 13.3 Re-audit requirement

If the initial audit results in a Fail or Pass with major revisions, a re-audit
is required after corrections are applied. The re-audit must verify:

- All critical findings are resolved
- All major findings are resolved
- Corrections did not introduce new errors
- No finding was suppressed rather than corrected

---

## 14. Audit rules and prohibitions

### 14.1 Audit integrity rules

1. The auditor must be independent of the report writer. When a separate auditor
   agent is not available, the report writer may perform the self-check in
   SKILL.md lines 353-368 but must not represent it as an independent audit.

2. The auditor must have access to the source inventory, all cited artifacts,
   and the project brief. Without these, a full audit cannot be performed and
   the limitations must be documented.

3. The auditor must verify facts against sources, not against memory or
   expectations. A value that "looks right" is not verified.

4. Sampling is permitted for repetitive checks (e.g., numeric verification of
   large tables) but must be documented: state the sample size and selection
   method. If any sampled item fails, the entire category must be checked at
   100%.

### 14.2 Absolute prohibitions

- **Never pass an audit with unresolved critical findings.** A report with one
  or more critical findings must not be delivered to any recipient. The findings
  must be corrected and the audit re-run.

- **Never suppress negative findings.** An audit finding that identifies an
  error, omission, or weakness must be recorded and reported, regardless of
  whether the correction is straightforward or difficult. Suppressing a finding
  to achieve a pass is an audit integrity violation.

- **Never downgrade a finding severity to achieve a pass.** Severity is
  determined by the impact on report reliability, not by convenience. A finding
  that could mislead a reader is critical regardless of how easy it is to fix.

- **Never skip a check category because the data is unavailable.** If a check
  cannot be performed (e.g., source inventory is missing), record it as an
  unresolved finding at the severity level appropriate to the missing
  information.

- **Never conduct a re-audit without verifying all corrected findings.** A
  re-audit that only spot-checks corrections is not valid. Every corrected
  finding must be individually verified.

### 14.3 Audit documentation requirements

Every audit must produce:

- An audit findings record conforming to `schemas/audit.schema.json`
- A written audit summary suitable for inclusion in the report appendix or as
  a standalone deliverable
- A source trace: which sources were consulted during the audit, with access
  dates

The audit documentation must be stored alongside the report and referenced in
the project artifact inventory.
