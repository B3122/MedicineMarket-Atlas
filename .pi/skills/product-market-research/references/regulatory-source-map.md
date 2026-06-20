# Regulatory Source Map

> Map of regulatory information sources for product-market research.
> Covers China (Mainland) and United States only.
> All URLs were accessed or verified on the dates indicated.
> Source URLs may change; see [URL Maintenance](#url-maintenance) for handling.

## Contents

- [China (Mainland)](#china-mainland)
- [United States](#united-states)
- [URL Maintenance](#url-maintenance)

---

## China (Mainland)

### Regulators

| Agency | Role | URL | Verified |
|--------|------|-----|----------|
| National Medical Products Administration (NMPA, 国家药品监督管理局) | Primary regulator for drugs, medical devices, cosmetics | https://www.nmpa.gov.cn/ | 2026-06-20 |
| State Administration for Market Regulation (SAMR, 国家市场监督管理总局) | Market supervision, advertising regulation, food safety, anti-unfair competition | https://www.samr.gov.cn/ | 2026-06-20 |
| National Health Commission (NHC, 国家卫生健康委员会) | Food safety standards, national essential drug list | https://www.nhc.gov.cn/ | 2026-06-20 |

**Notes:**
- NMPA was formerly the China Food and Drug Administration (CFDA). It was renamed in 2018 during a State Council restructuring.
- SAMR was established in 2018, merging the former State Administration for Industry and Commerce (SAIC), the General Administration of Quality Supervision, Inspection and Quarantine (AQSIQ), and portions of the former CFDA's food safety functions.
- For drug advertising review, the review function resides in NMPA's provincial offices, but SAMR enforces the Advertising Law overall.

### Official Product Query Portals

| Portal | Scope | URL | Query Fields | Verified |
|--------|-------|-----|-------------|----------|
| NMPA Data Search (国家药品监督管理局数据查询) | Drugs, medical devices, cosmetics, health food | https://www.nmpa.gov.cn/datasearch/home-index.html | Product name, approval number, company name, NMPA registration number, category | 2026-06-20 |
| NMPA Drug Registration (药品注册信息) | Domestic and imported drugs | https://www.nmpa.gov.cn/datasearch/home-index.html?category=yp | Drug name, approval number, manufacturer, ingredient, approval date | 2026-06-20 |
| NMPA Medical Device Registration (医疗器械注册信息) | Medical devices (Class I/II/III) | https://www.nmpa.gov.cn/datasearch/home-index.html?category=ylqx | Device name, registration number, manufacturer, classification | 2026-06-20 |
| NMPA Cosmetics (化妆品查询) | Cosmetics registration and filing | https://www.nmpa.gov.cn/datasearch/home-index.html?category=hzp | Product name, company, registration number | 2026-06-20 |
| SAMR Special Food Query Platform (特殊食品信息查询平台) | Health food (保健食品), infant formula, foods for special medical purposes | https://tsspxx.gsxt.gov.cn/ | Product name, approval number, manufacturer | 2026-06-20 |
| SAMR National Enterprise Credit Info System (国家企业信用信息公示系统) | Enterprise registration, licensing, penalty records | https://www.gsxt.gov.cn/ | Enterprise name, unified social credit code, legal representative | 2026-06-20 |
| China Drug Code (药品本位码) Query | Domestic drug product coding | https://code.nmpa.gov.cn/ | Product name, drug code number, manufacturer | 2026-06-20 |

**Accessibility note:** NMPA and SAMR websites frequently use CAPTCHA, IP-rate-limiting, and WAF protections (HTTP 412/429/403). Automated scraping requires careful handling, including respectful crawl delays, user-agent rotation, and handling of the CAPTCHA challenges. Manual verification via a browser is the most reliable approach for high-value lookups.

### Advertising and Health Claim Rules

| Source | Description | URL | Verified |
|--------|-------------|-----|----------|
| Advertising Law of the PRC (中华人民共和国广告法) | Primary law governing all advertising, including health and medical claims | https://www.samr.gov.cn/ (search "广告法") or https://flk.npc.gov.cn/ | 2026-06-20 |
| SAMR Advertising Regulation Department (广告监督管理司) | Enforcement of advertising rules, publishes regulatory guidance | https://www.samr.gov.cn/ggjgs/ | 2026-06-20 |
| Interim Measures for Drug, Medical Device, Health Food, and Formula Food for Special Medical Purposes Advertising Review (药品、医疗器械、保健食品、特殊医学用途配方食品广告审查管理暂行办法) | Specific review requirements for health-related advertising; issued by SAMR and NMPA | Referenced at https://www.samr.gov.cn/ and https://www.nmpa.gov.cn/ | 2026-06-20 |
| SAMR Regulations on Internet Advertising (互联网广告管理办法) | Specific rules for online advertisements, including KOL endorsements and health claims | https://www.samr.gov.cn/ (search "互联网广告管理办法") | 2026-06-20 |
| NMPA Drug Advertising Approval Database (药品广告审批数据) | Search approved drug advertising filings | https://www.nmpa.gov.cn/datasearch/home-index.html?category=ggcx | 2026-06-20 |

**Key restrictions (verified 2026-06-20):**
- Health food (保健食品) advertising must include the warning "本品不能代替药物" (This product cannot replace medication).
- Drug advertising cannot guarantee efficacy, use absolute language, or feature medical professionals or patient testimonials.
- Medical device advertising must cite the registration approval number.
- Cosmetics cannot claim curative effects (i.e., cannot claim to "treat" or "cure" conditions).
- These rules are documented here as research reference. Always verify current legal text for compliance.

### Label / Package Insert Sources

| Source | Description | URL | Verified |
|--------|-------------|-----|----------|
| NMPA Drug Instruction Database (药品说明书查询) | Official package inserts for approved drugs | https://www.nmpa.gov.cn/datasearch/home-index.html?category=yp (search by drug name, view "说明书") | 2026-06-20 |
| NMPA Medical Device Label Database (医疗器械说明书/标签查询) | Labels and instructions for registered medical devices | https://www.nmpa.gov.cn/datasearch/home-index.html?category=ylqx | 2026-06-20 |
| Yaozh.com (药智网) | Third-party aggregator of NMPA drug labels; useful cross-reference | https://db.yaozh.com/ | 2026-06-20 |
| Dingxiangyuan (丁香园) Drug Database | Physician-facing drug label reference | https://drugs.dxy.cn/ | 2026-06-20 |

**Note:** NMPA's official database is the authoritative source. Third-party sites like Yaozh and Dingxiangyuan repackage NMPA data and may have delays or transcription errors. Always cross-reference with NMPA for critical label claims.

### Safety Warning Sources

| Source | Description | URL | Verified |
|--------|-------------|-----|----------|
| NMPA Adverse Drug Reaction Bulletin (国家药品不良反应监测年度报告) | Annual ADR reports; published by NMPA Center for ADR Monitoring | https://www.nmpa.gov.cn/ (search "不良反应") or https://www.cdr-adr.org.cn/ | 2026-06-20 |
| NMPA Drug Safety Alerts (药品安全警示) | Urgent safety communications, recalls, and market withdrawals | https://www.nmpa.gov.cn/ (section "药品"/"医疗器械"/"化妆品" -> "安全警示") | 2026-06-20 |
| SAMR Recall Notices (产品召回) | Product recall announcements across drugs, devices, food, and consumer goods | https://www.samr.gov.cn/ (section "召回") | 2026-06-20 |
| National ADR Monitoring Center (国家药品不良反应监测中心) | Dedicated ADR monitoring and database | https://www.cdr-adr.org.cn/ | 2026-06-20 |
| SAMR National 12315 Platform (全国12315平台) | Consumer complaint and violation reporting platform; can surface product safety issues | https://www.12315.cn/ | 2026-06-20 |

### Common Product Categories

Categories as classified by Chinese regulatory authorities:

| Category (Chinese) | Category (English) | Primary Regulator | Class/Type |
|--------------------|--------------------|-------------------|------------|
| 化学药 | Chemical drug | NMPA | Rx / OTC |
| 中药 (中成药、中药材、中药饮片) | Traditional Chinese medicine (patent, raw, prepared slices) | NMPA | Rx / OTC |
| 生物制品 | Biological product (vaccines, blood products, live biologics) | NMPA | Rx |
| 医疗器械 (I/II/III类) | Medical device (Class I/II/III) | NMPA | Based on risk class |
| 化妆品 (特殊/普通) | Cosmetics (special use / general) | NMPA | Special use requires registration |
| 保健食品 | Health food (functional food, dietary supplement in Chinese framework) | SAMR (approval) / NMPA (GMP) | "Blue Hat" (蓝帽子) certification |
| 特殊医学用途配方食品 | Food for special medical purposes (FSMP) | SAMR / NMPA | Requires product registration |
| 婴幼儿配方食品 | Infant formula | SAMR | Requires product registration |

### Update Notes

- **NMPA data:** The data search portal is updated daily for new approvals. Drug registration data has a few days' lag between approval publication and database entry.
- **SAMR data:** The enterprise credit system is updated continuously as regulators enter data. Special food approvals may take 1-2 weeks to appear post-publication.
- **Frequency of law/regulation amendments:** Major advertising law amendments occur every 2-5 years. Implementing rules (办法) are updated more frequently. Check the issuing agency's site for the current version.
- **Data reliability:** NMPA and SAMR databases are primary sources. However, third-party aggregators may be 1-3 months behind.

### URL Maintenance

See [URL Maintenance](#url-maintenance) section below.

---

## United States

### Regulators

| Agency | Role | URL | Verified |
|--------|------|-----|----------|
| Food and Drug Administration (FDA) | Regulates drugs, biologics, medical devices, cosmetics, food, tobacco, and radiation-emitting products | https://www.fda.gov/ | 2026-06-20 |
| Federal Trade Commission (FTC) | Regulates advertising (including health claims), unfair/deceptive practices, endorsements | https://www.ftc.gov/ | 2026-06-20 |
| Centers for Medicare & Medicaid Services (CMS) | Pricing, reimbursement data; not a product regulator but a key pricing source | https://www.cms.gov/ | 2026-06-20 |
| Drug Enforcement Administration (DEA) | Controlled substance scheduling and regulation | https://www.dea.gov/ | 2026-06-20 |
| Environmental Protection Agency (EPA) | Pesticides and antimicrobial products (regulated as "pesticide devices" under FIFRA) | https://www.epa.gov/ | 2026-06-20 |

**Notes:**
- FDA is an agency of the Department of Health and Human Services (HHS).
- FTC and FDA share jurisdiction over advertising: FDA oversees prescription drug and restricted device advertising; FTC oversees OTC drug, device, cosmetic, food, and dietary supplement advertising.
- The FDA website underwent migration in 2021-2022; many old URLs redirect to new paths under `https://www.fda.gov/`. The migration status is expected to stay stable.

### Official Product Query Portals

| Portal | Scope | URL | Query Fields | Verified |
|--------|-------|-----|-------------|----------|
| NDC Directory (National Drug Code) | Finished and unfinished drugs, OTC and Rx | https://www.accessdata.fda.gov/scripts/cder/ndc/ | Proprietary name, nonproprietary name, NDC code, application number, labeler | 2026-06-20 |
| FDA Orange Book (Approved Drug Products) | Approved prescription drugs with TE ratings | https://www.accessdata.fda.gov/scripts/cder/ob/ | Active ingredient, proprietary name, application number | 2026-06-20 |
| FDA Drugs@FDA | FDA-approved drug labels, approval history, reviews | https://www.accessdata.fda.gov/scripts/cder/daf/ | Drug name, active ingredient, application number | 2026-06-20 |
| FDA Establishment Registration & Device Listing | Medical device manufacturer registrations and product listings | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfRL/rl.cfm | Owner/operator, registration number, device name, product code | 2026-06-20 |
| FDA PMA / 510(k) Databases | Pre-market approval and 510(k) clearance for medical devices | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMA/pma.cfm (PMA) / https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm (510k) | Applicant, device name, product code, decision date | 2026-06-20 |
| FDA National Drug Code (NDC) Directory - SPL Data Files | Downloadable bulk NDC data in SPL format | https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory | (Bulk download, not query) | 2026-06-20 |
| FDA Voluntary Cosmetic Registration Program (VCRP) | Cosmetic product ingredient and facility registration | https://www.fda.gov/cosmetics/voluntary-cosmetic-registration-program | (Voluntary, not comprehensive) | 2026-06-20 |
| Dietary Supplement Label Database (DSLD) | Dietary supplement label information; managed by NIH Office of Dietary Supplements | https://www.dsld.nlm.nih.gov/dsld/ | Product name, ingredient, manufacturer | 2026-06-20 |
| ClinicalTrials.gov | Clinical trial registry; primary evidence source for drug/device claims | https://clinicaltrials.gov/ | Condition, drug, sponsor, NCT number | 2026-06-20 |

**Note:** The NDC Directory is updated daily. Inclusion does not denote FDA approval. The Orange Book only lists approved prescription drugs and some OTC drugs that have NDA/ANDA approval.

### Advertising and Health Claim Rules

| Source | Description | URL | Verified |
|--------|-------------|-----|----------|
| FDA Prescription Drug Advertising (21 CFR Part 202) | Regulations for prescription drug advertising and promotion | https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-202 | 2026-06-20 |
| FDA OTC Drug Labeling (21 CFR Part 201) | Labeling requirements for OTC drugs, including Drug Facts format | https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-201 | 2026-06-20 |
| FDA Advertising and Promotional Labeling Guidance | Guidance documents for drug/device promotion | https://www.fda.gov/drugs/guidance-compliance-regulatory-information/prescription-drug-advertising-and-promotional-labeling-guidances | 2026-06-20 |
| FTC Truth in Advertising Act | Basis for FTC authority over false/deceptive advertising | https://www.ftc.gov/legal-library/browse/statutes/federal-trade-commission-act | 2026-06-20 |
| FTC Dietary Supplement Advertising Guidance | Specific guidance for health claims in dietary supplement advertising | https://www.ftc.gov/tips-advice/business-center/guidance/dietary-supplement-advertising-guide-industry | 2026-06-20 |
| FTC Endorsement Guides (Guides Concerning Use of Endorsements and Testimonials in Advertising) | Rules for influencer/celebrity endorsements and testimonials | https://www.ftc.gov/legal-library/browse/guides-concerning-use-endorsements-testimonials-advertising | 2026-06-20 |
| FDA Food Labeling: Nutrition Labeling & Claims (21 CFR Part 101) | Nutrient content claims, health claims, qualified health claims for foods and dietary supplements | https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-101 | 2026-06-20 |
| FDA Food and Dietary Supplement Health Claims (FD&C Act §403(r)) | Statutory framework for authorized and qualified health claims | https://www.fda.gov/food/food-labeling-nutrition/health-claims-notification | 2026-06-20 |

**Key distinctions (verified 2026-06-20):**
- FDA regulates prescription drug ads (must include approved labeling, fair balance).
- FTC regulates OTC drug, dietary supplement, food, and cosmetic advertising.
- Dietary supplements cannot claim to "diagnose, treat, cure, or prevent" disease (must have a structure/function claim disclaimer).
- Qualified health claims are permitted for foods and supplements under FDAMA and FDA's enforcement discretion.
- These rules are documented here as research reference. Always verify current legal text for compliance.

### Label / Package Insert Sources

| Source | Description | URL | Verified |
|--------|-------------|-----|----------|
| Drugs@FDA | Official FDA-approved prescription drug labels (Prescribing Information/package insert) with approval history | https://www.accessdata.fda.gov/scripts/cder/daf/ | 2026-06-20 |
| DailyMed (NLM) | Structured product labels (SPL) for marketed drugs, including Rx and OTC | https://dailymed.nlm.nih.gov/dailymed/ | 2026-06-20 |
| FDA OTC Monograph Drug Products | OTC drugs marketed under OTC monographs (not individual NDAs) | https://www.fda.gov/drugs/otc-drugs/otc-drug-monographs | 2026-06-20 |
| FDA Device Labeling | Labels and instructions for medical devices | https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/device-labeling | 2026-06-20 |
| FDA National Drug Code (NDC) Directory | Downstream of SPL data; includes labeling information at the package level | https://www.accessdata.fda.gov/scripts/cder/ndc/ | 2026-06-20 |
| FDA Cosmetics Labeling | Cosmetic label requirements and ingredient labeling | https://www.fda.gov/cosmetics/cosmetics-labeling | 2026-06-20 |

**Note:** DailyMed is maintained by the National Library of Medicine (NLM) and is generally the most accessible source for structured product labels. Drugs@FDA is the authoritative source for FDA-approved labels. For unapproved products not marketed in the US, DailyMed may not have an entry.

### Safety Warning Sources

| Source | Description | URL | Verified |
|--------|-------------|-----|----------|
| FDA Recalls, Market Withdrawals, and Safety Alerts | Official recall and safety alert announcements | https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts | 2026-06-20 |
| FDA MedWatch | Safety information for medical products, adverse event reporting, and safety alerts | https://www.fda.gov/safety/medwatch-fda-safety-information-and-adverse-event-reporting-program | 2026-06-20 |
| FDA Warning Letters Database | Letters to companies for regulatory violations regarding claims, GMP, and advertising | https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters | 2026-06-20 |
| FDA Adverse Event Reporting System (FAERS) | Adverse event reports for drugs and biologics; downloadable quarterly | https://www.fda.gov/drugs/questions-and-answers-fdas-adverse-event-reporting-system-faers | 2026-06-20 |
| FDA MAUDE Database | Adverse event reports for medical devices | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfMAUDE/search.CFM | 2026-06-20 |
| FTC Consumer Alerts and Complaints | FTC actions on false advertising and consumer fraud | https://www.ftc.gov/news-events/consumer-alerts | 2026-06-20 |
| CDC Health Alerts Network (HAN) | Public health alerts, including drug safety issues, from Centers for Disease Control | https://emergency.cdc.gov/han/ | 2026-06-20 |
| NIH LiverTox | Drug-induced liver injury information, with causality assessments for drugs | https://www.ncbi.nlm.nih.gov/books/NBK547852/ | 2026-06-20 |

### Common Product Categories

Categories as classified by US regulatory authorities:

| Category | Primary Regulator | Classification Basis |
|----------|-------------------|---------------------|
| Prescription drugs (Rx) | FDA (CDER/CBER) | New Drug Application (NDA), Abbreviated NDA (ANDA), Biologics License Application (BLA) |
| Over-the-counter (OTC) drugs | FDA (CDER), FTC (advertising) | OTC monograph or NDA; Drug Facts label format |
| Biologics (including biosimilars) | FDA (CBER) | BLA, licensed under PHS Act |
| Medical devices (Class I/II/III) | FDA (CDRH) | 510(k) clearance, PMA approval, De Novo classification, or exempt |
| Combination products | FDA (OCP) | Product containing drug + device, drug + biologic, etc.; primary mode of action determines lead center |
| Dietary supplements | FDA (CFSAN), FTC (advertising) | Structure/function claims only; cannot claim disease treatment |
| Cosmetics | FDA (CFSAN), FTC (advertising) | Cannot make curative claims; color additive approval for some products |
| Food (including functional foods) | FDA (CFSAN), USDA (some) | Health claims require FDA authorization or qualified health claim notification |
| Vaccines | FDA (CBER) | BLA; licensed after clinical trials |
| Blood and blood products | FDA (CBER) | BLA; donor screening and facility registration |
| Tobacco products | FDA (CTP) | Pre-market tobacco product application (PMTA), substantial equivalence (SE) |

### Update Notes

- **NDC Directory:** Updated daily, reflecting new product listings from labelers. Historical data is not maintained within the directory; snapshot downloads are provided weekly.
- **Orange Book:** Updated monthly (usually first business day). Includes patent and exclusivity information for approved drugs.
- **DailyMed:** Updated within 24-48 hours of SPL submission to FDA. Covers both FDA-approved and marketed unapproved drugs.
- **FAERS:** Quarterly data releases with a 3-6 month lag from report receipt.
- **Warning Letters:** Posted to FDA's website as issued. FDA maintains a searchable database but letters from before 2015 may have limited searchability.
- **eCFR (Code of Federal Regulations):** Updated incrementally as final rules are published. The official CFR is updated once per calendar year on the Government Publishing Office site (https://www.govinfo.gov/).
- **FDA Guidance Documents:** Not binding but represent the agency's current thinking. Guidance documents are periodically revised.

### URL Maintenance

See [URL Maintenance](#url-maintenance) section below.

---

## URL Maintenance

### Problem Statement

Agencies restructure websites, migrate content between domains, or retire old portals. URLs documented here may break over time. The following method ensures continued access.

### Strategy

**Step 1: Check for redirects.**
Many agencies implement HTTP 301/302 redirects. Before updating the source map, test the documented URL. If it redirects, the destination is typically the new home for that content.

- Example: `https://www.accessdata.fda.gov/scripts/cder/ndc/` has been stable for years. If broken, the NDC directory likely moved to a new `accessdata.fda.gov` path or consolidated under `fda.gov/drugs/`.
- Example: Chinese government sites may return HTTP 412 (WAF block) even when functional. If 412 is received, test via a real browser session before declaring the URL dead.

**Step 2: Search the agency root.**
If the URL is truly dead (HTTP 404/410), navigate to the agency root and search for the content name.

| Agency | Root URL | Search Strategy |
|--------|----------|-----------------|
| NMPA | https://www.nmpa.gov.cn/ | Use site search box; search for "数据查询" or "药品查询" or the specific database name |
| SAMR | https://www.samr.gov.cn/ | Site search or navigate "服务" -> "查询平台" |
| FDA | https://www.fda.gov/ | Use site search or Google `site:fda.gov <topic>` |
| FTC | https://www.ftc.gov/ | Use site search or Google `site:ftc.gov <topic>` |
| eCFR | https://www.ecfr.gov/ | Search by title and part number (e.g., "21 CFR 202") |

**Step 3: Check Web Archive.**
If the URL is dead and cannot be found on the current site, check the Wayback Machine at `https://web.archive.org/`. Paste the old URL and find the most recent capture. This is especially useful for content that has been removed from the current website (e.g., old guidance documents, expired NMPA approvals).

**Step 4: Download bulk data whenever possible.**
For research reproducibility, periodically download bulk data:

| Dataset | Download Source | Format |
|---------|----------------|--------|
| NDC Directory (US) | https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory | SPL, ZIP, Excel |
| FAERS (US) | https://www.fda.gov/drugs/questions-and-answers-fdas-adverse-event-reporting-system-faers | ASCII, XML |
| Orange Book (US) | https://www.fda.gov/drugs/drug-approvals-and-databases/approved-drug-products-th%65rap%65utic-equivalence-evaluations | Excel |
| DailyMed (US) | https://dailymed.nlm.nih.gov/dailymed/download-labels.cfm | SPL, XML |
| NMPA Drug Data (CN) | Via third-party aggregators (yaozh.com, etc.) or NMPA data portal | Web only (no direct download) |

**Step 5: Update this file.**
When a URL changes:
1. Find the new URL using Steps 1-3 above.
2. Test it resolves to the correct content.
3. Update the entry in this file.
4. Change the "Verified" date to the date of the update.
5. If the content moved to a completely different platform, note the old URL in a comment or footnote.

### Dead URL Indicators

| Status | Likely Meaning | Action |
|--------|---------------|--------|
| HTTP 200 | Working | No action needed |
| HTTP 301/302 | Moved | Follow redirect, update URL |
| HTTP 403 | Blocked (often for NMPA/SAMR) | Try from a browser; may be temporary |
| HTTP 404 | Not found | Likely moved or removed; search |
| HTTP 412 | Precondition Failed (common for NMPA/SAMR) | May be WAF; test from browser |
| HTTP 429 | Rate limited | Retry with delay or from a different IP |
| DNS failure | Domain may be retired | Check for domain migration |
| Timeout | Site may be temporarily unreachable | Retry after 24h; check status |

### Maintenance Schedule

- **Frequency:** Review URLs at the start of each new research project (not per query).
- **Trigger:** If a documented URL returns HTTP 4xx/5xx during active use, verify and update immediately.
- **Entropy:** Based on historical patterns, expect 2-5 US federal URLs to change per year. Chinese government URLs change less frequently but can break without redirect when sites are redesigned.
