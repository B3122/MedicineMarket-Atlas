# Source Hierarchy Reference

Defines preferred source types per research question, evidence tiering,
conflict resolution order, and source-access recording conventions.

**Version**: 1.0.0
**Last updated**: 2025-06-20
**Cross-references**: SYSTEM.md lines 96-143 (source hierarchy, evidence
discipline), output-record-specification.md (source record fields,
`data_category`, `access_notes`, `snapshot_path`, `collection_date`)

---

## Overview

Every research question maps to a different source priority ladder. A price
question and a clinical efficacy question require different evidence types,
rated on different scales. This document defines those ladders and the rules
for using them.

The system uses four broad tiers, ranked by trustworthiness:

1. **Official** — regulatory filings, approved labels, guidelines, clinical
   registries, manufacturer-controlled pages.
2. **Authorized** — licensed distributors, authorized retailers, certified
   resellers, pharmacy listings.
3. **Marketplace** — third-party platform pages, unverified sellers, user-
   generated listings, aggregator sites.
4. **Social** — social media posts, forum threads, consumer reviews, comments,
   influencer content.

A source from a higher tier overrides a source from a lower tier when they
conflict. Within the same tier, prefer the most specific and most recent
source.

---

## Product Identity and Composition Hierarchy

Use when identifying a product, its ingredients, dosage form, strength,
manufacturer, brand, or package configuration.

| Priority | Source Type | Example |
|----------|-------------|---------|
| 1 (highest) | Official regulatory record | NMPA registration, FDA NDC directory, EMA public assessment report |
| 2 | Approved label or package insert | FDA label, Chinese-registered说明书, PIL |
| 3 | Manufacturer or brand official page | Product page on pfizer.com.cn, official Tmall flagship store |
| 4 | Authorized retailer or pharmacy page | Licensed online pharmacy (e.g., 健客网, 1mg), hospital formulary |
| 5 | Third-party marketplace listing | Unverified seller on Taobao, Amazon third-party listing |
| 6 (lowest) | Social post or consumer comment | Xiaohongshu post, douban review, Reddit thread |

**Concrete example**: To confirm the active ingredient dose of a product:

- If the NMPA registration record lists `500 mg`, accept it over all others.
- If no regulatory record is available, use the manufacturer's official page.
- If the manufacturer page conflicts with a marketplace listing, the
  manufacturer page wins.
- Never use a social post to establish ingredient, dose, or manufacturer.

**Cross-reference**: SYSTEM.md lines 100-107.

---

## Clinical Efficacy and Safety Hierarchy

Use when evaluating therapeutic effect, safety profile, adverse events,
contraindications, or drug interactions. This hierarchy follows the standard
evidence pyramid for clinical questions.

| Priority | Source Type | Example |
|----------|-------------|---------|
| 1 (highest) | Official guideline or regulatory assessment | NMPA clinical guideline, FDA label review, WHO essential medicines list, NICE guideline |
| 2 | Systematic review or meta-analysis | Cochrane review, BMJ Clinical Evidence |
| 3 | Randomized controlled trial | Phase III RCT published in a peer-reviewed journal |
| 4 | Prospective observational study | Cohort study, registry study with prospective design |
| 5 | Retrospective observational study | Case-control study, retrospective chart review |
| 6 | Case series or case report | Single-center case series, n-of-1 report |
| 7 | Pharmacokinetic or mechanistic human study | PK/PD study, bioavailability study in healthy volunteers |
| 8 | Animal study | Mouse model, rat model of disease |
| 9 (lowest) | In-vitro study | Cell-line assay, receptor-binding study |

**Boundary rules**:

- A manufacturer claim about efficacy is **not** clinical evidence. It is a
  commercial claim (see `commercial_claim` record type) and must be
  distinguished from independent clinical research.
- Animal and in-vitro findings must not be represented as demonstrated human
  clinical effects. Reports must explicitly note the species or model system.
- Consumer reviews are not proof of efficacy or safety. They belong in the
  consumer narrative record type, not in the clinical evidence table.
- Ingredient-level research does not automatically apply to a finished product.
  Formulation, dose, route, population, duration, and outcome differences
  must be assessed and documented before extrapolating.

**Cross-reference**: SYSTEM.md lines 109-119 and lines 127-143 (evidence
discipline).

---

## Price, Promotion, Channel, and Listing Hierarchy

Use when collecting current price, discount, promotion, channel availability,
stock status, or listing information. Price is time-sensitive; the source page
itself is the best evidence.

| Priority | Source Type | Example |
|----------|-------------|---------|
| 1 (highest) | The page where the price was observed | Live product page on JD.com, Amazon listing page |
| 2 | Screenshot or archived snapshot of the same page | Saved PDF, Playwright screenshot with timestamp |
| 3 | Official brand price list | Manufacturer MSRP page, official WeChat mini-program |
| 4 | Authorized retailer published price | Licensed pharmacy price list |
| 5 | Price aggregator or comparison site | Kangai.cn, GoodRx, DrugsUpdate |
| 6 | Consumer-reported price | Social post mentioning purchase price |

**Key rules**:

- The page itself is the primary authority. If the live page shows
  `¥89.00`, that is the price. No higher authority overrides it for the
  observation date.
- Always retain the collection date alongside the price. A price without a
  collection date is not a valid observation.
- Promotions (coupons, flash sales, bundled discounts) must be recorded
  separately from the list price. Use `original_price` and `price` fields as
  defined in output-record-specification.md.
- If a price changed between two collection dates, record both observations
  as separate price_observation records. Do not average them.

**Cross-reference**: SYSTEM.md lines 121-123.

---

## Conflict Resolution Order

When two or more sources provide conflicting values for the same fact, apply
this resolution order:

1. **Tier** — the source in a higher evidence tier (official > authorized >
   marketplace > social) wins. A regulatory record overrides an authorized
   retailer page.
2. **Recency** — within the same tier, the more recent source wins unless
   there is reason to suspect the older source is more authoritative (e.g.,
   an approved label supersedes a corrected draft).
3. **Specificity** — within the same tier and same recency, the source
   that addresses the specific product, dose, package, and region wins over
   a general or aggregate source.
4. **Proximity** — within the same tier, recency, and specificity, the source
   closest to the primary data (direct observation over a secondary report)
   wins.

**When conflicts are not resolvable**:

- Record both values in a `conflict` record (see output-record-specification.md
  `conflict` record type).
- Do not silently pick one value. Preserve conflicting source values and
  document the conflict in the report.
- Flag the conflict for human review if it affects a critical finding.

**Cross-reference**: SYSTEM.md lines 137-138 (do not silently select one value
when credible sources conflict).

---

## Search-Summary Limitations

Search-result snippets (the excerpt shown on a search engine results page,
platform search listings, or API search results) have inherent limitations
that affect their use as evidence.

### What search snippets are not

- A snippet is **not** a source. It is a preview of a source.
- A snippet does **not** replace visiting the page, capturing its content,
  and saving a snapshot.
- A snippet may be truncated, out of date, drawn from a non-authoritative
  section of the page, or algorithmically generated.

### When snippets may be used

Snippets may be noted as leads or starting points, but only if the source
page was inaccessible and all reasonable access methods were exhausted.
In that case, the snippet is recorded as a source with
`access_notes: "page_not_found"` and the limitation is noted in the report.

### Rule

> Search-result snippets are not evidence. Every fact must trace back to a
> source that was opened, inspected, and saved.

**Cross-reference**: SYSTEM.md lines 131-132 (do not treat search-result
snippets as sufficient evidence when the source can be opened and inspected).

---

## Snapshot and Collection-Date Requirements

Every source must be captured and timestamped so the evidence can be
independently verified.

### Snapshot requirements

| Content type | Snapshot requirement |
|--------------|---------------------|
| Static web page (HTML) | Save as PDF via browser print, or archive via single-file HTML save |
| Dynamic web page (JS-rendered) | Take a full-page screenshot via Playwright, or save as PDF with rendered content |
| Social media post | Take a screenshot showing the full post, timestamp, and username |
| PDF or document | Save the original file; note the retrieval date and URL |
| API response | Save the raw JSON or XML response; note the endpoint and parameters |
| Price observation | Always take a screenshot showing the price, currency, product identifier, and page URL |

### Snapshot path convention

Use relative paths under the project's `sources/` directory:

```
sources/{platform}/{YYYYMMDD}/{source_id}.{ext}
```

Example: `sources/tmall/20250620/tmall-20250620-001.pdf`

Record the path in the source record's `snapshot_path` field. Use
`"not_applicable"` if no snapshot was saved (e.g., an API response stored
as a JSON source file rather than a screenshot).

### Collection-date requirements

| Field | Requirement |
|-------|-------------|
| `collection_date` | Required on every source record. Format: `YYYY-MM-DD`. |
| `collection_datetime` | Optional but recommended for time-sensitive data (prices, flash promotions, limited-time listings). Format: `YYYY-MM-DDThh:mm:ss±hh:mm`. |
| Timezone | Use the local timezone of the collection point, or UTC for cross-region research. Document which was used in the project config. |

A price observation without a collection date is invalid. A clinical evidence
source does not require a datetime but must have at least the collection date
so the report reader knows when the source was accessed.

**Cross-reference**: SYSTEM.md lines 121-123 (collection date for price),
output-record-specification.md lines 124-127 (`collection_date`,
`snapshot_path`).

---

## Inaccessible-Page Marking

When a source page cannot be accessed, the reason must be recorded so the
report reader and future researchers understand the gap.

### Marking convention

Use the `access_notes` field on the source record. Standard values:

| `access_notes` value | Meaning | When to use |
|----------------------|---------|-------------|
| `"page_not_found"` | URL returned HTTP 404 or equivalent | Link is dead, product delisted |
| `"paywall"` | Page requires payment to view | Journal article behind fee, paid database |
| `"login_required"` | Page requires authentication | Members-only area, gated content |
| `"captcha_blocked"` | Automated access blocked by CAPTCHA | Bot detection prevented collection |
| `"redirected"` | URL redirected to an unrelated page | Domain changed, product moved |
| `"timeout"` | Page did not load within a reasonable time | Server error, network issue |
| `"partial_content"` | Page loaded but key sections were missing | Dynamic content failed to render, truncated view |
| `"removed_by_platform"` | Page existed but was taken down | Removed listing, deleted post |
| `"region_blocked"` | Content not available from the collector's region | Geo-restricted content |
| `"not_found_no_404"` | Page appeared reachable but the content referenced no longer exists | Soft 404, empty search results |

### What to do when a page is inaccessible

1. Record the URL, attempted access date, and method in a source record with
   the appropriate `access_notes` value.
2. Set `snapshot_path` to `"not_applicable"` (no snapshot could be taken).
3. If a search snippet or cached version is available and relevant, note it
   as a lead but mark the source as `access_notes: "page_not_found"` and
   include a caveat in the report.
4. Do not fabricate the content of the inaccessible page.
5. If the page later becomes accessible, create a new source record with the
   new collection date and update any facts derived from it.

### What inaccessible-page marking is not

- It is not permission to guess the page content.
- It is not permission to substitute a different product's page.
- It is not a substitute for attempting reasonable recovery (checking
  Internet Archive, trying a different network, searching for a cached copy).

**Cross-reference**: output-record-specification.md line 128 (`access_notes`
field), SYSTEM.md lines 127-130 (never invent a URL or fact).

---

## Examples by Tier

### Tier 1: Official source

```json
{
  "source_id": "nmpa-20250620-001",
  "source_type": "database_record",
  "platform": "nmpa",
  "title": "NMPA Drug Registration - Guoyao Zhunzi J20190001",
  "url": "https://www.nmpa.gov.cn/datasearch/...",
  "collection_date": "2025-06-20",
  "collection_method": "manual_browse",
  "snapshot_path": "sources/nmpa/20250620/nmpa-20250620-001.pdf",
  "access_notes": "unknown",
  "data_category": "product_identity",
  "extraction_confidence": "high"
}
```

### Tier 2: Authorized source

```json
{
  "source_id": "official-20250620-002",
  "source_type": "web_page",
  "platform": "official",
  "title": "Product page - Brand X Official Store",
  "url": "https://official-brand.example.com/products/x",
  "collection_date": "2025-06-20",
  "collection_method": "playwright",
  "snapshot_path": "sources/official/20250620/official-20250620-002.pdf",
  "access_notes": "unknown",
  "data_category": "pricing",
  "extraction_confidence": "high"
}
```

### Tier 3: Marketplace source

```json
{
  "source_id": "tmall-20250620-003",
  "source_type": "web_page",
  "platform": "tmall",
  "title": "Listing - Product X on Tmall Marketplace",
  "url": "https://detail.tmall.com/item.htm?id=...",
  "collection_date": "2025-06-20",
  "collection_method": "playwright",
  "snapshot_path": "sources/tmall/20250620/tmall-20250620-003.pdf",
  "access_notes": "unknown",
  "data_category": "pricing",
  "extraction_confidence": "medium"
}
```

### Tier 4: Social source

```json
{
  "source_id": "xhs-20250620-004",
  "source_type": "social_post",
  "platform": "xhs",
  "title": "User review - Product X experience post",
  "url": "https://www.xiaohongshu.com/explore/...",
  "collection_date": "2025-06-20",
  "collection_method": "manual_browse",
  "snapshot_path": "sources/xhs/20250620/xhs-20250620-004.png",
  "access_notes": "unknown",
  "data_category": "consumer_narrative",
  "extraction_confidence": "low"
}
```

### Inaccessible page

```json
{
  "source_id": "jd-20250620-005",
  "source_type": "web_page",
  "platform": "jd",
  "title": "Listing - Product X on JD.com (page not found)",
  "url": "https://item.jd.com/123456.html",
  "collection_date": "2025-06-20",
  "collection_method": "playwright",
  "snapshot_path": "not_applicable",
  "access_notes": "page_not_found",
  "data_category": "pricing",
  "extraction_confidence": "unknown"
}
```

---

## Quick Reference Card

| Question type | Tier 1 source | Tier 2 source | Tier 3 source | Tier 4 source |
|---------------|---------------|---------------|---------------|---------------|
| Product identity / composition | Regulatory record | Approved label | Manufacturer page | Marketplace listing |
| Clinical efficacy / safety | Guideline / regulatory assessment | Systematic review / meta-analysis | RCT | Observational study |
| Price / channel / listing | The page itself | Screenshot of page | Official price list | Consumer report |

**Cross-reference**: SYSTEM.md lines 96-143 for the complete source hierarchy
and evidence discipline rules.
