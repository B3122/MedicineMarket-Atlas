# Consumer Content Rules

Rules for handling consumer-generated content (reviews, comments, social
posts) in product market research. This document governs what consumer
content can and cannot support, how to classify it, how to detect bad
data, and how to protect privacy.

**Version**: 1.0.0
**Last updated**: 2025-06-20
**Cross-references**: SYSTEM.md (evidence discipline lines 136-140),
output-record-specification.md (consumer narrative record),
claim-taxonomy.md (user testimonial claim type),
regulatory-source-map.md (advertising claim rules)

---

## Core Prohibition

**Consumer comments are NOT evidence of clinical efficacy.**

No consumer-generated content, regardless of volume, sentiment, or
apparent consistency, can establish that a product works, is safe, or
produces a specific health outcome. This prohibition applies to all
forms of consumer content:

- E-commerce product reviews
- Social media posts and comments
- Video testimonials
- Forum discussions
- Private group messages
- Survey responses from non-controlled populations
- Any other unsolicited or solicited consumer utterance

The only acceptable uses of consumer content are:

1. **Narrative pattern analysis**: identifying recurring themes, usage
   scenarios, pain points, and sentiment patterns.
2. **Market positioning insight**: understanding how consumers frame
   and compare products in their own language.
3. **Hypothesis generation**: surfacing questions that can be tested
   against clinical or regulatory evidence.
4. **Engagement context**: documenting platform-level engagement signals
   (volume, sentiment distribution) as market context, not proof.

A recurring consumer claim (e.g., "many users say it works overnight")
is a **narrative observation**, not corroboration. It must never be
presented alongside clinical evidence as if it carries equivalent
weight.

### What consumer content CAN support

| Use case | Example | Output record type |
|----------|---------|-------------------|
| Recurring usage scenarios | "Most mentions involve post-meal use" | consumer_narrative |
| Sentiment distribution | "70% of reviews are positive" | consumer_narrative |
| Common complaints | "Bitter taste is the top negative theme" | consumer_narrative |
| Purchase motivation | "Price is the main reason for switching" | consumer_narrative |
| Language for positioning | "Users say 'gentle' not 'mild'" | consumer_narrative |

### What consumer content CANNOT support

| Incorrect use | Why it is wrong |
|---------------|-----------------|
| "80% of reviewers saw results" as efficacy evidence | No control group, no blinding, no verified outcome measurement |
| "Users report no side effects" as safety evidence | No systematic adverse event collection, no medical confirmation |
| "Viral post says product cured condition X" as treatment claim | Anecdotal, unverifiable, may be fabricated |
| Review count as sales or market share | Review counts are engagement proxies, not transaction records |

---

## Influencer vs Ordinary User Content

### Definitions

**Ordinary user**: A person who purchased or used the product and shared
their experience without commercial arrangement with the brand. Their
content reflects unprompted consumer experience, though it still carries
no clinical evidentiary weight.

**Key Opinion Consumer (KOC)**: A content creator with moderate
following who receives free products or samples but may not have a
formal paid agreement. Often identifiable by "gifted" or "free sample"
disclosures. Treat as potentially influenced content.

**Key Opinion Leader (KOL) / Influencer**: A content creator with a
commercial relationship with the brand. Their content is paid
promotion, even when framed as personal experience. Must be flagged as
sponsored content.

**Professional KOL**: A licensed practitioner (doctor, pharmacist,
nutritionist) who posts product content. Their professional credentials
do not convert the post into clinical evidence. The post remains a
commercial endorsement unless it links to peer-reviewed research or
regulatory determinations.

**Brand / Media account**: An account operated by or on behalf of the
product's manufacturer, distributor, or paid agency. Not consumer
content at all. Exclude from consumer narrative analysis.

### Classification rules

1. **Default to ordinary user** unless one of the signals below is
   present. Do not assume commercial relationship without evidence.
2. **When in doubt, classify as `unknown`** rather than guessing.
3. **Record the `content_author_type`** in the consumer narrative
   record using the values: `ordinary_user`, `key_opinion_consumer`,
   `professional_kol`, `media_account`, `brand_account`,
   `verified_practitioner`, `unknown`.
4. **Do not collapse categories**: influencer content and ordinary user
   content should be analyzed separately. Mixing them distorts
   sentiment and theme frequencies.
5. **Follower count is descriptive, not dispositive**: a user with
   100,000 followers who has no disclosed commercial relationship is
   still an ordinary user for classification purposes. Conversely, a
   user with 500 followers who discloses a sponsored post is an
   influencer.

### Cross-reference

The `is_sponsored` and `content_author_type` fields in the consumer
narrative record capture these distinctions. See
output-record-specification.md lines 353-380.

---

## Commercial Cooperation Identification

### Why this matters

Content posted under commercial arrangements systematically differs from
organic content in sentiment, claims, and emphasis. Treating sponsored
content as independent consumer experience inflates positive sentiment
and creates misleading market intelligence.

### Detection signals

| Signal | Where it appears | Reliability |
|--------|------------------|-------------|
| `#ad`, `#sponsored`, `#合作`, `#推广` tags | Post body, caption, or comment | High when explicit |
| Platform cooperation label (e.g., Xiaohongshu "赞助" badge, Douyin "商业合作" badge, Weibo "推广" label) | Platform UI adjacent to post | High |
| "Received free product" / "gifted" disclosure | Post body | High |
| Brand account tagging the creator | Post or comment | Medium |
| Affiliate link or discount code | Post body, bio, link-in-bio | Medium |
| Product seeding program participation | Creator platform profile | Medium |
| Consistently positive posts across different products by the same creator | Cross-post pattern | Low (suggestive only) |
| Identical phrasing across multiple creators' posts | Cross-creator text match | Medium (may indicate campaign brief) |

### Handling

1. **Flag `is_sponsored = true`** when any high-reliability signal is
   present or when two or more medium-reliability signals coincide.
2. **Do not exclude sponsored content from analysis automatically**.
   Sponsored content can still provide narrative themes (usage
   scenarios, common phrasings). But it must be analyzed separately
   from organic content, or at minimum tagged so the report can
   distinguish the two.
3. **Report the sponsorship rate**: when presenting consumer narrative
   findings, state what fraction of the analyzed content was sponsored.
   Example: "Of 200 posts analyzed, 45 (22.5%) carried commercial
   cooperation markings."
4. **Do not guess**: if no cooperation signal is present but the
   content looks promotional, classify as `ordinary_user` with
   `is_sponsored = false` and add a note if suspicion exists. Do not
   mark content as sponsored based on tone alone.

---

## Template and Repeated Review Detection

### What template reviews look like

Template reviews share identical or near-identical text across different
user accounts, products, or listings. They indicate coordinated inauthentic
behavior, often from:

- Paid review farms
- Automated review generation scripts
- Incentivized review campaigns that supply boilerplate text
- Cross-posting the same review across multiple SKUs or platforms

### Detection methods

1. **Exact text deduplication**: hash review body text and flag exact
   matches posted by different user IDs or on different dates.
2. **Near-duplicate detection**: apply text similarity (e.g., edit
   distance, Jaccard similarity on word n-grams) and flag pairs or
   clusters above a threshold. A reasonable threshold is Jaccard
   similarity > 0.80 on character-level 3-grams.
3. **Same-text-different-product**: a review that is identical across
   two or more unrelated products from the same brand or different
   brands.
4. **Timestamp clustering**: reviews posted in a burst (e.g., 20
   reviews within 5 minutes) with similar text structure.
5. **Rating-template correlation**: five-star reviews that all follow
   the same sentence template (e.g., "Great product! Fast shipping!
   [Ingredient] works well! Recommend!").
6. **Cross-platform matching**: the same review text found on two
   different platforms for the same product.

### Handling

1. **Exclude from theme frequency counts**: template reviews inflate
   the apparent prevalence of a theme. Remove deduplicated clusters
   before computing frequencies.
2. **Log the detection**: record how many reviews were identified
   as template content, and which detection method flagged them.
3. **Do not automatically delete**: preserve flagged reviews in the
   raw data store with a `quality_flag` field so the exclusion
   decision can be audited.
4. **Report the template rate**: "Of 500 reviews analyzed, 60 (12%)
   were identified as template content and excluded from theme
   frequency analysis."

---

## Fake Review Detection

### What this document cannot do

This is a process rule, not a detection system. Automated fake review
detection is a specialized field (NLP, behavioral analysis, network
graph analysis) beyond the scope of this skill. What follows are
minimum handling rules for cases where fake content is suspected or
obvious.

### Obvious signals

- Reviews mentioning products, ingredients, or effects that do not
  match the listing (e.g., a review of a dietary supplement that
  describes a skincare product).
- Reviews with the same text posted across multiple accounts on the
  same date (covered under template detection above).
- Reviews with nonsensical or randomized text.
- Reviewer account created on the same day as the review with no
  other activity.
- Review rating contradicts the body text (e.g., 1-star rating with
  effusive praise).

### Language for unverifiable content

When fake review status is suspected but cannot be confirmed, use the
following language in research outputs:

> "[N] reviews could not be verified as authentic. These reviews are
> included in narrative theme counts but are flagged as
> unverifiable. Their inclusion does not imply endorsement of their
> claims."

Do not state or imply that unverified reviews are definitely fake.
Use "unverifiable", "cannot be confirmed as authentic", or
"insufficient verification signals" rather than "fake", "fraudulent",
or "suspicious".

### Handling

1. **Flag unverifiable reviews** with a `quality_flag` value of
   `"unverifiable_authenticity"` in the raw data store.
2. **Sensitivity analysis**: when presenting theme frequencies, state
   whether excluding unverifiable reviews would change the result.
   If possible, provide both-included and excluded figures.
3. **Do not rely on consumer reports of fakery**: a user comment
   claiming another review is fake is itself consumer content and
   carries no verification authority.

---

## High-Frequency Theme Statistics

### Principles

1. **Count unique authors, not total reviews**: if one user posts 10
   reviews mentioning the same theme, count it as 1 author, not 10.
   Exception: repeat-purchase mentions from the same author across
   different time periods may be counted separately with annotation.
2. **Separate organic and sponsored**: compute theme frequencies
   separately for organic and sponsored content. If the ratio is
   within 10 percentage points, they can be reported as combined with
   a note. If the gap exceeds 10 points, report separately.
3. **State the denominator**: every frequency claim must include the
   base. Example: "Bitter taste was mentioned in 34 of 200 organic
   reviews (17%)." Not: "Bitter taste was mentioned by 17% of
   reviewers."
4. **Remove template duplicates before counting**: see template
   detection above.
5. **Do not extrapolate**: theme frequency in collected reviews does
   not predict frequency in the broader population of all purchasers.
   State this limitation. Example: "Among the 200 reviews analyzed,
   34 mention bitter taste. This reflects the reviewed sample, not
   the general purchaser population."
6. **Minimum sample threshold**: do not report theme frequencies for
   samples smaller than 30 distinct consumer content items. Below
   this threshold, report only qualitative theme lists without
   percentages.
7. **Multiple themes per item**: one review may express multiple
   themes. The sum of theme percentages may exceed 100%. State this
   explicitly.

### Reporting template

> Consumer narrative analysis is based on [N] pieces of consumer
> content ([N_organic] organic, [N_sponsored] sponsored) collected
> from [platform list] on [date(s)]. Template duplicates ([N_template]
> items) were removed before frequency computation. The sample reflects
> the collected content only and does not represent the general
> purchaser population.
>
> | Theme | Frequency (organic) | Frequency (sponsored) |
> |-------|--------------------|-----------------------|
> | Theme A | N (%) | N (%) |
> | Theme B | N (%) | N (%) |

---

## Privacy and Personal Data

### Core rule

**Do not collect unnecessary user identity data.**

Consumer content analysis requires the text of the review or post and
platform-level metadata (date, engagement metrics). It does not require
the identity of the reviewer.

### What NOT to collect

- **Usernames, display names, or handles**: unless required for
  template duplicate detection (and then must be hashed or discarded
  after deduplication).
- **Profile URLs**: do not store links to user profiles.
- **Profile photos or avatars**: do not download or store.
- **Email addresses**: never. Even if visible on a platform.
- **Phone numbers**: never. Even if visible on a platform.
- **Real names**: never. Even if the user posts under their real name.
- **Location data**: do not collect unless the research question
  specifically requires geographic analysis and the data is aggregated
  (city or region level, not precise coordinates). State the
  geographic purpose explicitly in the research plan.
- **Device or browser fingerprints**: do not collect. Consumer content
  is collected from platform pages, not via tracking scripts.

### What MAY be collected

| Data | Purpose | Retention |
|------|---------|-----------|
| Review or post body text | Narrative theme analysis | Until project completion, then anonymized |
| Date of post | Temporal trend analysis | Retained |
| Platform user ID (internal platform identifier, not username) | Template duplicate detection only | Hashed after deduplication; store only the hash |
| Follower count at time of collection | Author type classification | Retained as integer |
| Engagement metrics (likes, shares, comments) | Engagement context | Retained |
| Verified badge or platform certification flag | Author type classification | Retained as boolean |

### Anonymization procedure

1. **Replace usernames with a sequential ID** in the analysis dataset
   (e.g., `user_001`, `user_002`). Keep the mapping in a separate,
   access-controlled file if re-identification is needed for
   deduplication. Delete the mapping after deduplication.
2. **Strip profile URLs** from any exported data. If a URL was
   collected as part of source recording (e.g., the post URL), the
   post URL is permissible because it identifies the content, not a
   person. Profile URLs are not permissible.
3. **Quotes in reports**: when including example quotes in research
   outputs, remove any identifying information (names, usernames,
   profile references) from the quote. Use "[user]" or "a reviewer"
   instead.
4. **No re-identification**: do not attempt to re-identify anonymous
   reviewers by cross-referencing platforms or datasets.

### Jurisdiction-specific rules

Where applicable regulations (GDPR, China PIPL, CCPA) impose stricter
requirements, the stricter rule applies. In case of doubt, consult
the project's privacy or legal advisor before collecting consumer
content data.

---

## QA Checklist

Use this checklist to verify compliance before including consumer
content analysis in a report:

- [ ] Consumer comments explicitly labeled as narrative analysis,
      not efficacy evidence.
- [ ] Sponsored content identified and separated or tagged.
- [ ] Template/repeated reviews detected and excluded from
      frequency counts.
- [ ] Template rate and detection method documented.
- [ ] Unverifiable reviews flagged with appropriate language
      ("unverifiable", not "fake").
- [ ] Theme frequencies report the denominator and state the
      sample limitation.
- [ ] No usernames, profile URLs, or personal identifiers in the
      research output.
- [ ] Influencer and ordinary user content analyzed separately or
      with clear tagging.
- [ ] Minimum sample threshold (30) respected for frequency
      reporting.
- [ ] Anonymization procedure applied to any example quotes.
