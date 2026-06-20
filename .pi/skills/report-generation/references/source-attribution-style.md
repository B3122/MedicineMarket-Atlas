# Source Attribution Style

Citation format, source ID conventions, and traceability rules for every
externally verifiable statement in market-research reports.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: SKILL.md (lines 155-178 source attribution, lines
254-286 distinguish statement types), report-structure-guide.md (references
section format), output-record-specification.md (source record fields, source
ID format), schemas/_defs.json (ID pattern definitions),
data-quality-scoring.md (source quality dimensions).

---

## Table of Contents

1. [Source ID conventions](#1-source-id-conventions)
2. [Inline citation format](#2-inline-citation-format)
3. [Bibliography and reference format](#3-bibliography-and-reference-format)
4. [Traceability rules by statement type](#4-traceability-rules-by-statement-type)
5. [Source quality in attribution](#5-source-quality-in-attribution)
6. [Conflict attribution](#6-conflict-attribution)
7. [Multi-source attribution](#7-multi-source-attribution)
8. [Prohibited attribution practices](#8-prohibited-attribution-practices)
9. [Attribution checklist](#9-attribution-checklist)

---

## 1. Source ID conventions

### 1.1 Source ID format

Every source in a project source inventory carries a unique source ID with
the format:

```
{platform}-{YYYYMMDD}-{seq}
```

| Component | Description | Example |
|-----------|-------------|---------|
| `platform` | Lowercase platform code (see 1.2) | `jd`, `tmall`, `pubmed`, `nmpa` |
| `YYYYMMDD` | Collection or access date | `20260615` |
| `seq` | Zero-padded 3-digit sequence number, starting at `001` per platform per date | `001`, `002` |

Complete ID examples:

- `jd-20260615-001` — first JD.com listing collected on 15 June 2026.
- `tmall-20260616-003` — third Tmall listing collected on 16 June 2026.
- `pubmed-20260617-002` — second PubMed search result from 17 June 2026.
- `nmpa-20260614-001` — first NMPA regulatory record accessed on 14 June 2026.

### 1.2 Platform codes

Use these codes for the `platform` component:

| Platform | Code |
|----------|------|
| JD.com | `jd` |
| Tmall | `tmall` |
| Taobao | `taobao` |
| Suning | `suning` |
| Pinduoduo | `pdd` |
| Amazon | `amazon` |
| iHerb | `iherb` |
| Rakuten | `rakuten` |
| PubMed | `pubmed` |
| ClinicalTrials.gov | `clinicaltrials` |
| Cochrane Library | `cochrane` |
| NMPA (China) | `nmpa` |
| FDA (US) | `fda` |
| EMA (EU) | `ema` |
| PMDA (Japan) | `pmda` |
| MFDS (Korea) | `mfds` |
| Official brand website | `official` |
| Social / consumer platform | platform name lowercase (e.g., `xiaohongshu`, `weibo`) |

### 1.3 Source ID assignment rules

- Assign source IDs when the source is first recorded in the source inventory.
- Reuse the same source ID for all citations to the same source within a report.
- Do not reassign or reassign IDs across projects. Each project maintains its
  own source inventory with independent numbering.
- When a source yields multiple distinct records (e.g., multiple products from
  one platform page), assign separate IDs if the records are independent.

### 1.4 Source ID in reports

Every source cited in the body must appear exactly once in the references
section with its source ID, full citation, and access date.

---

## 2. Inline citation format

### 2.1 Primary format: source ID bracket

```
[source-id]
```

Example:

> The product was listed at CNY 129.00 for 30 tablets [jd-20260615-001].
>
> A randomized trial of 240 participants reported a 32% reduction in pain
> scores [pubmed-20260617-002].

### 2.2 When to place brackets

Place the source ID bracket immediately after the claim it supports, before
the sentence-ending punctuation.

For multi-sentence claims from the same source, cite at the end of the
relevant sentence or clause. Do not place a single citation at the end of a
paragraph that covers multiple distinct claims.

### 2.3 Citation placement rules

| Claim type | Citation placement |
|------------|--------------------|
| Single fact | Immediately after the fact, before the period. |
| Quantitative value | Immediately after the value and its unit. |
| Multiple facts from same source | At the end of each sentence containing a supported fact. |
| Entire paragraph from one source | Cite at the first supported statement; repeat at last if the paragraph is long. |

### 2.4 Derived and calculated values

When a value is calculated from a source, cite both the source and note the
derivation:

> The estimated daily cost is CNY 8.60 per day, calculated from the sale price
> of CNY 129.00 for 30 tablets at a labeled dose of 2 tablets per day
> [jd-20260615-001].

The formula and assumptions must be recorded in the appendices or calculation
notes.

---

## 3. Bibliography and reference format

### 3.1 Reference entry structure

Each reference entry includes:

```
[source-id] Citation text. URL. Accessed: date.
```

### 3.2 Format by source type

#### Marketplace listing

```
[jd-20260615-001] "Product Name" listing on JD.com (seller: [seller name]).
https://item.jd.com/XXXXXXXXX.html. Accessed: 2026-06-15.
```

#### Official product page

```
[official-20260616-001] "Product Name" product page, [Manufacturer Name]
official website. https://www.example.com/product. Accessed: 2026-06-16.
```

#### Academic article

```
[pubmed-20260617-001] Author A, Author B, Author C. "Title." Journal Name.
YYYY;Vol(Issue):Pages. DOI: 10.XXXX/XXXXX. PMID: XXXXXXXX.
```

#### Clinical trial registry

```
[clinicaltrials-20260617-001] "Study Title." ClinicalTrials.gov Identifier:
NCTXXXXXXXX. https://clinicaltrials.gov/study/NCTXXXXXXXX.
Accessed: 2026-06-17.
```

#### Regulatory record

```
[nmpa-20260614-001] National Medical Products Administration. "Drug
Registration Certificate." Registration No. XXXXXXXX. Date: YYYY-MM-DD.
https://www.nmpa.gov.cn/.... Accessed: 2026-06-14.
```

#### Guideline or recommendation

```
[pubmed-20260617-003] Organization Name. "Guideline Title." Guideline
publication date. URL. Accessed: YYYY-MM-DD.
```

#### Social or consumer content

```
[xiaohongshu-20260616-001] User-generated content on Xiaohongshu, collected
on 2026-06-16. Note: Consumer-generated content; not verified clinical
evidence.
```

### 3.3 URL requirement

Every source with a publicly accessible URL must include it. For sources
behind authentication (paywalls, login-required pages), note the access
restriction:

```
URL not publicly accessible — paywalled. Accessed via institutional access
on 2026-06-17.
```

### 3.4 Access date requirement

Every source entry must include the date the source was accessed or collected.
This is critical for price data, which changes over time.

---

## 4. Traceability rules by statement type

### 4.1 Statement type categories

Seven statement types are distinguished in reports (per SKILL.md lines
254-286). Each type has its own minimum attribution requirements.

### 4.2 Verified fact

A statement that can be confirmed against an official source.

> "According to the official label, the product contains 500 mg glucosamine
> sulfate per tablet."

**Attribution requirements**:
- Source ID of the official record, label, or regulatory filing.
- For product composition: regulatory record preferred over manufacturer page
  over marketplace listing.

### 4.3 Platform observation

A statement describing what was visible on a platform at the time of
collection.

> "At the time of collection, the listing displayed a sale price of
> CNY 129.00."

**Attribution requirements**:
- Source ID of the platform listing.
- Collection date (must match the date in the source ID).
- Price type (sale_price, coupon_price, member_price, etc.).

### 4.4 Commercial claim

A statement attributed to a seller, brand, or manufacturer that has not been
independently verified.

> "The seller stated that the product 'relieves joint pain within 7 days.'"

**Attribution requirements**:
- Source ID of the listing or page where the claim appeared.
- Explicit labeling as a commercial claim — never present as verified fact.
- Quotation marks or clear attribution language.

### 4.5 Consumer narrative

A statement describing themes or observations from consumer-generated content.

> "Frequently observed user discussions concerned the product's taste and
> ease of swallowing."

**Attribution requirements**:
- Source ID(s) of the consumer content collection.
- Platform and date range.
- Explicit note: "Consumer-generated content; not verified clinical evidence."

### 4.6 Scientific finding

A statement reporting research results from an academic or clinical study.

> "In a randomized trial of 240 participants, the investigators reported a
> 32% reduction in WOMAC pain scores at 12 weeks."

**Attribution requirements**:
- Source ID of the study.
- **DOI, PMID, or clinical trial registry identifier**.
- Study design descriptor (RCT, cohort, case-control, etc.).
- Sample size.
- Effect estimate with uncertainty interval.
- Duration.
- Must distinguish ingredient-level from finished-product evidence when
  applicable.

### 4.7 Regulatory finding

A statement about a product's regulatory status, classification, or
authorization.

> "The NMPA classifies the product as a health food (保健食品) with
> registration number 国食健字G20XXXXXX."

**Attribution requirements**:
- Source ID of the official regulatory record.
- **Official authority name and jurisdiction.**
- Registration or approval number, if available.
- Access date.

### 4.8 Analyst interpretation

A statement expressing the analyst's judgment, synthesis, or inference.

> "This pattern may indicate that the premium-priced products are
> concentrated on Tmall flagship stores rather than open marketplace
> listings."

**Attribution requirements**:
- No external source required, but the underlying observations that support
  the interpretation must be cited in the preceding text.
- Use cautious language (e.g., "may indicate", "suggests", "is consistent
  with") — never present as fact.

---

## 5. Source quality in attribution

### 5.1 Source tier annotation

When source quality materially affects the reliability of a claim, annotate
the source tier in the citation:

> The product was listed at CNY 129.00 [jd-20260615-001 — tier 3: marketplace].

Source tiers follow the hierarchy defined in source-hierarchy.md.

### 5.2 Low-quality source flag

When relying on a lower-tier source because a higher-tier source is
unavailable, state the limitation explicitly:

> The active ingredient dose could not be confirmed from an NMPA regulatory
> record. The dose stated here is from the manufacturer's Tmall flagship
> store listing [tmall-20260616-002] and has not been independently verified.

### 5.3 Data quality annotation

When a source has a data quality score below threshold, note the specific
deficiency:

> The package quantity was not explicitly stated on the listing. The value of
> 30 tablets is inferred from product images and may be incorrect
> [jd-20260615-003 — incomplete listing data].

---

## 6. Conflict attribution

### 6.1 When sources conflict

When two sources provide conflicting values, cite both:

> The manufacturer's official website lists the active ingredient as 1500 mg
> per tablet [official-20260616-001], while the JD.com listing states 750 mg
> [jd-20260615-001]. The official source is preferred per the product identity
> hierarchy.

### 6.2 Conflict resolution annotation

Always state which source is preferred and why. Use the conflict resolution
rules from source-hierarchy.md.

### 6.3 Unresolved conflicts

When a conflict cannot be resolved:

> Two marketplace listings report different package quantities for the same
> product: 30 tablets [jd-20260615-001] and 60 tablets [jd-20260615-004].
> This conflict could not be resolved from available sources. Both values are
> preserved in the product record.

---

## 7. Multi-source attribution

### 7.1 When to use multiple citations

Use multiple citations when:

- A claim synthesizes data from multiple sources.
- A comparative claim involves two or more products.
- A consumer theme is drawn from multiple consumer content items.

### 7.2 Format for multiple sources

```
[source-id-1] [source-id-2] [source-id-3]
```

Example:

> The product was available across three platforms: JD.com at CNY 129.00
> [jd-20260615-001], Tmall at CNY 125.00 [tmall-20260616-001], and Pinduoduo
> at CNY 118.00 [pdd-20260616-001].

### 7.3 Consumer theme attribution

When drawing a theme from multiple consumer comments, cite the collection
batch and the number of comments:

> Among 45 consumer comments collected from Xiaohongshu [xiaohongshu-20260616],
> the most frequent theme was gastrointestinal tolerability, mentioned in
> 18 comments.

---

## 8. Prohibited attribution practices

- **Never cite a source without a source ID.** Every citation in the body
  must correspond to a source ID in the references section.
- **Never use "personal communication" as a citation.** All sources must be
  publicly verifiable or documented in the source inventory with a collection
  record.
- **Never cite a source that does not support the associated statement.**
  Verify that the source contains the specific information being attributed to
  it.
- **Never cite a consumer review as evidence of efficacy or safety.**
  Consumer comments are consumer narratives, not clinical evidence.
- **Never cite a commercial claim as if it were a scientific finding.**
  Label commercial claims explicitly.
- **Never cite without an access date.** Every source must include the date
  it was accessed or collected.
- **Never fabricate a source ID or invent a citation.** If a source cannot be
  located, state that the information could not be confirmed rather than
  fabricating a reference.
- **Never cite a broken or unverifiable URL as if it were verified.** If a URL
  is no longer accessible, note the original access date and the current status.
- **Never omit the URL from a web source citation.**
- **Never use "anonymous source" or vague references** (e.g., "industry
  reports suggest", "experts say"). Every source must be specific and
  traceable.

---

## 9. Attribution checklist

Before finalizing a report, verify:

- Every factual claim in the body has a source ID bracket.
- Every source ID appears exactly once in the references section.
- Every source ID follows the `{platform}-{YYYYMMDD}-{seq}` format.
- Every web source citation includes a URL and access date.
- Every academic citation includes DOI, PMID, or registry ID.
- Every regulatory citation names the official authority and jurisdiction.
- Commercial claims are explicitly labeled, never presented as verified facts.
- Consumer comments are labeled as consumer-generated content, not clinical
  evidence.
- Analyst interpretations use cautious language and are grounded in cited
  observations.
- Conflicting values are attributed to both sources with a resolution
  statement.
- No fabricated source IDs, dates, or URLs are present.
- No "personal communication" citations are present.
