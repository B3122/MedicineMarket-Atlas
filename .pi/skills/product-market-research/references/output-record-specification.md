# Output Record Specification

Canonical field definitions for all record types produced by the
product-market-research skill.

**Version**: 1.0.0
**Last updated**: 2025-06-20
**Cross-references**: SYSTEM.md (source hierarchy lines 96-124, evidence
discipline lines 126-143, product identity rules lines 148-165, platform
interpretation rules lines 166-197)

---

## Format Conventions

### Date format

All dates use ISO 8601: `YYYY-MM-DD`. No time component is stored unless
explicitly specified (e.g., `collection_datetime`). Partial dates (year-only
or year-month) are permitted only when the day is genuinely unknown and are
stored as `YYYY` or `YYYY-MM`.

### Currency format

Currencies use ISO 4217 three-letter codes: `USD`, `EUR`, `CNY`, `JPY`, etc.
Always uppercase. A `currency` field without a corresponding `price` field is
not valid. When currency is unknown, use `"unknown"` not `"not_applicable"`.

### Unit format

Physical quantities use SI base units or commonly accepted medical units:

| Quantity        | Preferred unit                                  |
|-----------------|-------------------------------------------------|
| Mass            | mg, g, kg (not mcg; use ug or mcg documented)   |
| Volume          | mL, L                                           |
| Count           | capsule, tablet, sachet, patch, piece, dose     |
| Concentration   | mg/mL, ug/mL, % (w/w), % (w/v)                  |
| Daily cost      | currency per day (e.g., USD/d)                  |
| Unit price      | currency per base unit (e.g., CNY/g)            |
| Time            | d (day), h (hour), wk (week), mo (month)        |

Do not convert between non-comparable dimensions (e.g., mg to mL without
density). Always preserve the original unit string alongside any normalized
value.

### Null value convention

Two distinct null expressions exist:

- `"unknown"` — the value exists in reality but was not observed or could not
  be determined from available sources. Example: `manufacturer: "unknown"`
  when the product page does not list the manufacturer.
- `"not_applicable"` — the field does not apply to this record type or
  context. Example: `dosage_form: "not_applicable"` for a competitor metric
  record that aggregates multiple products.

A field with `"unknown"` should be filled if better data becomes available.
A field with `"not_applicable"` should never be filled.

### Original vs normalized values

Every field that undergoes transformation retains two versions:

- `original_<field>` — the verbatim value as observed on the source page.
- `<field>` or `normalized_<field>` — the standardized value after conversion.

Examples:
- `original_price`: `"¥129.00"`, `price`: `129.00`, `currency`: `"CNY"`
- `original_unit`: `"mcg"`, `unit`: `"ug"`
- `original_daily_dose`: `"2粒"`, `daily_dose`: `2`, `daily_dose_unit`: `"capsule"`

When no transformation is applied, both fields carry the same value.

### Source ID naming convention

Every source record receives a unique source ID in the format:

    {platform}-{YYYYMMDD}-{sequential}

- `{platform}`: a short, lowercase platform code (e.g., `tmall`, `jd`,
  `official`, `xhs`, `dy`, `amazon`, `pubmed`, `nmpa`, `fda`).
- `{YYYYMMDD}`: the collection date.
- `{sequential}`: a three-digit zero-padded sequence number starting at
  `001`, reset daily per platform.

Examples:
- `tmall-20250620-001`
- `official-20250620-003`
- `pubmed-20250619-001`

### Record versioning

Each record may carry an optional `record_version` field (integer) and
`record_version_note` (string). The initial version is always `1`.

Increment the version when a record is materially updated (new fields added,
incorrect values corrected, new source IDs linked). Do not increment for
cosmetic changes or re-serialization.

Previous versions are not stored inline. When versioning matters, keep a
separate audit log or archive of prior versions.

---

## source record (source)

A source record represents one page, document, or database entry that was
accessed, inspected, and saved as raw evidence. Every fact in the system
traces back to exactly one source record.

**File format**: one JSON object per line (JSONL), one object per file
(single-record JSON), or CSV for inventory listing.

### Fields

| Field                    | Type    | Required | Description |
|--------------------------|---------|----------|-------------|
| `source_id`              | string  | required | Unique identifier: `{platform}-{YYYYMMDD}-{sequential}`. |
| `source_type`            | string  | required | Category of source: `web_page`, `pdf`, `api_response`, `screenshot`, `database_record`, `regulatory_filing`, `academic_article`, `industry_report`, `social_post`. |
| `platform`               | string  | required | Platform code where the source was collected (e.g., `tmall`, `jd`, `official`, `xhs`, `pubmed`, `nmpa`). Must match a known platform key. |
| `title`                  | string  | required | Page title, document title, or descriptive label assigned during collection. |
| `url`                    | string  | required | Full URL of the source page. Use `"not_applicable"` for offline documents. |
| `collection_date`        | string  | required | ISO 8601 date when the source was accessed and saved. |
| `collection_datetime`    | string  | optional | ISO 8601 datetime with timezone when the source was accessed. |
| `collection_method`      | string  | optional | How the source was collected: `manual_browse`, `playwright`, `api`, `mcp_tool`, `file_import`, `user_provided`. |
| `snapshot_path`          | string  | optional | Relative path to a saved screenshot, PDF, or archival copy of the source. Use `"not_applicable"` if no snapshot was saved. |
| `access_notes`           | string  | optional | Free-text notes about access conditions: login required, CAPTCHA, paywall, partial content, dynamic content, page not found. Use `"unknown"` when access status is not determined. |
| `language`               | string  | optional | Primary language of the source content (ISO 639-1 code, e.g., `zh`, `en`, `ja`). |
| `region`                 | string  | optional | Geographic region or market the source pertains to, using ISO 3166-1 alpha-2 where applicable (e.g., `CN`, `US`, `JP`, `EU`). |
| `data_category`          | string  | optional | What kind of information this source primarily supports: `product_identity`, `pricing`, `claims`, `clinical_evidence`, `regulatory_status`, `consumer_narrative`, `market_metric`. Maps to the prioritization rules in SYSTEM.md source hierarchy. |
| `extraction_confidence`  | string  | optional | Confidence in the extraction quality: `high`, `medium`, `low`, `unknown`. Low confidence when auto-extraction was used on dynamic content or a screenshot. |
| `record_version`         | integer | optional | Version number of this source record. Starts at 1. |
| `record_version_note`    | string  | optional | Reason for the latest version change. |

### Source hierarchy cross-reference

The `data_category` field determines which source priority ladder applies
(SYSTEM.md lines 96-124):

- `product_identity` sources are prioritized per lines 100-107.
- `clinical_evidence` sources are prioritized per lines 109-119.
- `pricing` sources retain the page itself as the authority (lines 121-123).

---

## product record (product)

A product record describes an identified product at the master level and,
optionally, at the version level. One product record exists per distinct
product identity after normalization.

**File format**: JSONL. One product record per line.

### Fields

| Field                          | Type    | Required | Description |
|--------------------------------|---------|----------|-------------|
| `product_master_id`            | string  | required | Stable identifier for the core product across versions. Format: `pm-{platform_prefix}-{sequential}`. |
| `product_version_id`           | string  | optional | Identifier for a specific version/dose/package variant. Format: `pv-{platform_prefix}-{sequential}`. Use `"not_applicable"` when no versioning is needed. |
| `brand`                        | string  | required | Brand name as it appears on the official product or label. Use `"unknown"` when the brand cannot be identified. |
| `manufacturer`                 | string  | required | Manufacturer or distributor name. Use `"unknown"` when not found on the source. |
| `standard_name`                | string  | optional | Standardized product name following a naming convention (brand + generic + form + dose). Derived during normalization. |
| `generic_name`                 | string  | optional | Active ingredient or generic name (INN or local equivalent). |
| `dosage_form`                  | string  | required | Pharmaceutical dosage form (e.g., `tablet`, `capsule`, `cream`, `injection`, `oral_solution`, `powder`, `patch`). Use `"unknown"` for non-pharmaceutical products. |
| `active_ingredients`           | array   | required | List of active ingredients. Each entry: `{ "name": string, "per_unit_dose": string, "per_unit_dose_unit": string, "original_per_unit_dose": string }`. Empty array `[]` if no active ingredient (e.g., medical device). |
| `package_quantity`             | string  | optional | Number of dosage units per package (e.g., `"30"`, `"10x3"` for multi-pack). Use `"unknown"` when not found. |
| `package_description`          | string  | optional | Free-text description of the package configuration (e.g., `"30 tablets per bottle, 2 bottles per box"`). |
| `region`                       | string  | required | Market region using ISO 3166-1 alpha-2. Use `"unknown"` when regional identity could not be determined. |
| `registration_id`              | string  | optional | Regulatory registration, filing, or approval number (e.g., NMPA Guo Yao Zhun Zi, FDA NDC, EU CE mark number). Maps to SYSTEM.md lines 148-165 priority rules. |
| `registration_jurisdiction`    | string  | optional | Jurisdiction that issued the registration (e.g., `CN`, `US`, `EU`). Required if `registration_id` is present. |
| `registration_type`            | string  | optional | Type of registration: `drug_approval`, `device_registration`, `cosmetics_filing`, `health_food_filing`, `otc_monograph`, `unknown`. |
| `source_ids`                   | array   | required | List of source IDs that contributed to this product record. At least one source required. |
| `data_quality_score`           | string  | optional | Overall data quality category: `high`, `medium`, `low`, `unknown`. See data-quality-scoring.md for scoring dimensions. |
| `identity_certainty`           | string  | optional | How certain the product identity match is: `confirmed`, `probable`, `possible`, `uncertain`. Use `"uncertain"` when human review is needed. Maps to SYSTEM.md line 163 human-review gate. |
| `record_version`               | integer | optional | Version number of this product record. |
| `record_version_note`          | string  | optional | Reason for the latest version change. |

### Product identity rules cross-reference

The distinction between master, version, SKU, listing, and bundle is governed
by product-identity-rules.md and SYSTEM.md lines 148-165. When identity
remains uncertain, set `identity_certainty` to `"uncertain"` and preserve
separate records.

---

## listing record (listing)

A listing record represents one offer or product page observed on a specific
platform at a specific time. Multiple listings may refer to the same product.

**File format**: JSONL. One listing record per line.

### Fields

| Field                    | Type    | Required | Description |
|--------------------------|---------|----------|-------------|
| `listing_id`             | string  | required | Unique identifier for this listing observation. Format: `ls-{platform}-{YYYYMMDD}-{sequential}`. |
| `source_id`              | string  | required | The source record ID from which this listing was extracted. |
| `product_master_id`      | string  | optional | Link to the normalized product master record, if identified. Use `"unknown"` when the product identity has not been resolved. |
| `product_version_id`     | string  | optional | Link to the specific product version, if applicable. |
| `title`                  | string  | required | The listing title as displayed on the platform page. |
| `price`                  | number  | required | Observed price as a numeric value. Use a negative sentinel (e.g., `-1`) only if price is genuinely not displayed; otherwise `"unknown"` maps to null. |
| `currency`               | string  | required | ISO 4217 currency code. Use `"unknown"` when currency cannot be determined. |
| `original_price`         | string  | optional | The raw price string as displayed (e.g., `"¥129"`, `"$19.99"`). |
| `price_type`             | string  | required | Type of price observed: `list_price`, `sale_price`, `member_price`, `live_price`, `coupon_price`, `subscription_price`, `bundle_price`, `unknown`. See pricing-normalization.md for definitions. |
| `price_condition`        | string  | optional | Conditions tied to this price (e.g., `"first_order_only"`, `"min_purchase_2"`, `"subscription_required"`, `"flash_sale"`). |
| `package_size`           | string  | optional | Package size as displayed (e.g., `"30 tablets"`, `"100 mL"`, `"2-pack"`). |
| `package_quantity`       | number  | optional | Number of dosage units in the package as a numeric value (e.g., `30`). |
| `seller_type`            | string  | required | Type of seller: `official_brand`, `authorized_distributor`, `platform_self`, `third_party`, `individual`, `unknown`. |
| `seller_name`            | string  | optional | Displayed seller or store name. |
| `seller_region`          | string  | optional | Region of the seller, ISO 3166-1 alpha-2. |
| `platform_metrics`       | array   | optional | List of platform metric IDs (see platform metric record) observed on this listing. |
| `in_stock`               | boolean | optional | Whether the listing shows the item as in stock. `true`, `false`, or omitted if unknown. |
| `shipping_region`        | string  | optional | Region to which the seller ships this product. |
| `shipping_cost`          | number  | optional | Shipping cost if displayed separately. Use `0` for free shipping, omit if unknown. |
| `shipping_currency`      | string  | optional | Currency of the shipping cost. |
| `collection_date`        | string  | required | ISO 8601 date when the listing was observed. |
| `collection_datetime`    | string  | optional | ISO 8601 datetime with timezone of the observation. |
| `page_position`          | string  | optional | Where on the page this listing appeared: `search_result_N`, `category_page_N`, `promotion_banner`, `featured`. |
| `data_quality_notes`     | string  | optional | Notes about data quality concerns (dynamic pricing, login-gated price, etc.). |
| `record_version`         | integer | optional | Version number of this listing record. |

---

## price observation (price_observation)

A price observation is a single measured price point for a product, listing,
or combination. Multiple price observations can be derived from one listing
record when different price types, quantities, or promotions apply.

**File format**: JSONL. One price observation per line.

### Fields

| Field                       | Type    | Required | Description |
|-----------------------------|---------|----------|-------------|
| `observation_id`            | string  | required | Unique identifier. Format: `po-{platform}-{YYYYMMDD}-{sequential}`. |
| `source_id`                 | string  | required | Source record ID from which this observation was extracted. |
| `listing_id`                | string  | optional | Listing record ID if this observation was derived from a listing. |
| `product_master_id`         | string  | optional | Product master record ID, if identified. |
| `product_version_id`        | string  | optional | Product version record ID, if applicable. |
| `price`                     | number  | required | Numeric price value in the observation currency. |
| `currency`                  | string  | required | ISO 4217 currency code. |
| `original_price`            | string  | optional | Raw price string as observed. |
| `price_type`                | string  | required | Type of price: `list_price`, `sale_price`, `member_price`, `live_price`, `coupon_price`, `subscription_price`, `bundle_price`, `unit_price`, `daily_cost`, `unknown`. |
| `package_quantity`          | number  | optional | Number of dosage units this price covers. |
| `unit_price`                | number  | optional | Normalized price per single dosage unit. `null` when package_quantity is missing. |
| `unit_price_currency`       | string  | optional | Currency of the unit price (same as `currency` in most cases). |
| `unit_price_unit`           | string  | optional | Unit for the unit price (e.g., `"per_tablet"`, `"per_mL"`, `"per_g"`). |
| `daily_cost`                | number  | optional | Normalized cost per day based on the labeled or declared daily dose. `null` when dose is unknown. |
| `daily_cost_currency`       | string  | optional | Currency of the daily cost. |
| `daily_cost_source`         | string  | optional | Source of the daily dose used in calculation: `label`, `official_site`, `clinical_guideline`, `assumption`. |
| `daily_dose_used`           | number  | optional | Numeric daily dose value used in the daily cost calculation. |
| `daily_dose_unit`           | string  | optional | Unit of the daily dose (e.g., `"mg"`, `"mL"`, `"capsule"`). |
| `formula`                   | string  | optional | Human-readable formula used for calculations (e.g., `"129.00 / 30 = 4.30 per tablet"`, `"4.30 * 2 tablets/day = 8.60 USD/d"`). |
| `assumptions`               | array   | optional | List of assumptions made during normalization (e.g., `"assumed 30-day month"`, `"assumed 2 capsules per day per label"`). |
| `includes_shipping`         | boolean | optional | Whether the observed price includes shipping. `true`, `false`, or omitted. |
| `includes_tax`              | boolean | optional | Whether the observed price includes tax. `true`, `false`, or omitted. |
| `promotion_details`         | string  | optional | Description of promotions applied (e.g., `"buy 2 get 1 free"`, `"10% off first order"`). |
| `gift_or_bonus`             | string  | optional | Description of any gift or bonus items included with this price (e.g., `"free travel-size"`). |
| `exchange_rate`             | number  | optional | Exchange rate used if currency conversion was applied. |
| `exchange_rate_date`        | string  | optional | Date of the exchange rate, ISO 8601. |
| `exchange_rate_source`      | string  | optional | Source of the exchange rate (e.g., `"ECB"`, `"PBOC"`, `"XE"`). |
| `data_quality_notes`        | string  | optional | Quality concerns specific to this price observation. |
| `record_version`            | integer | optional | Version number. |

---

## commercial claim (commercial_claim)

A commercial claim is a factual assertion, promotional statement, or health
claim made on a product page, advertisement, or other commercial source.
Claims are recorded verbatim and classified for later verification against
academic and regulatory evidence.

**File format**: JSONL. One claim per line.

### Fields

| Field                    | Type    | Required | Description |
|--------------------------|---------|----------|-------------|
| `claim_id`               | string  | required | Unique identifier. Format: `cc-{platform}-{YYYYMMDD}-{sequential}`. |
| `source_id`              | string  | required | Source record ID where this claim was observed. |
| `listing_id`             | string  | optional | Listing record ID if the claim was extracted from a listing. |
| `product_master_id`      | string  | optional | Product master record ID, if the product is identified. |
| `product_version_id`     | string  | optional | Product version record ID, if applicable. |
| `claim_text`             | string  | required | Verbatim text of the claim as it appeared on the source. Include surrounding context when the meaning depends on it. |
| `claim_type`             | string  | required | Classification of the claim per claim-taxonomy.md. One of: `ingredient_fact`, `efficacy_claim`, `disease_treatment`, `safety_claim`, `speed_claim`, `magnitude_claim`, `population_claim`, `expert_endorsement`, `technology_claim`, `natural_claim`, `clinical_backing`, `ranking_claim`, `comparative_claim`, `user_testimonial`, `other`. |
| `claim_language`         | string  | optional | Language of the claim text (ISO 639-1). |
| `claim_context`          | string  | optional | Where on the page the claim appeared: `title`, `subtitle`, `description`, `bullet_point`, `ad_copy`, `video_overlay`, `review_response`, `faq`, `banner`, `package_image`. |
| `claim_confidence`       | string  | optional | Confidence that the extracted text is an actual commercial claim: `high`, `medium`, `low`, `unknown`. Low for ambiguous statements. |
| `support_status`         | string  | optional | Result after evidence appraisal (see evidence-appraisal SKILL.md lines 316-371). One of: `direct_support`, `partial_support`, `indirect_support`, `insufficient_evidence`, `contradicted`, `not_assessed`. |
| `support_status_note`    | string  | optional | Explanation of the support status, including which evidence sources were used. |
| `evidence_source_ids`    | array   | optional | Source IDs of academic or regulatory evidence records used in support assessment. |
| `verification_date`      | string  | optional | ISO 8601 date when the support assessment was performed. |
| `is_sponsored`           | boolean | optional | Whether the claim appears in sponsored or paid content. |
| `record_version`         | integer | optional | Version number. |

### Evidence discipline cross-reference

Per SYSTEM.md lines 126-143: manufacturer claims are not independent
scientific evidence. Do not treat the `claim_text` itself as proof. The
`support_status` field must be set by an evidence appraisal process, not by
the claim extractor.

---

## platform metric (platform_metric)

A platform metric is a quantitative indicator observed on a platform page
that relates to product popularity, engagement, or transaction activity.
These are proxies, not verified sales or clinical data.

**File format**: JSONL. One metric observation per line.

### Fields

| Field                    | Type    | Required | Description |
|--------------------------|---------|----------|-------------|
| `metric_id`              | string  | required | Unique identifier. Format: `pm-{platform}-{YYYYMMDD}-{sequential}`. |
| `source_id`              | string  | required | Source record ID where this metric was observed. |
| `listing_id`             | string  | optional | Listing record ID the metric is associated with. |
| `product_master_id`      | string  | optional | Product master record ID, if identified. |
| `metric_type`            | string  | required | Type of platform metric. One of: `review_count`, `rating`, `sales_volume_displayed`, `monthly_sales`, `total_sales`, `review_volume`, `favorite_count`, `like_count`, `share_count`, `view_count`, `comment_count`, `watchlist_count`, `question_count`, `popularity_label`, `ranking`, `badge`, `other`. |
| `metric_name`            | string  | required | The platform-specific label for this metric (e.g., `"月销"`, `"已售"`, `"评分"`, `"收藏"`). |
| `metric_value`           | string  | required | The observed value as displayed on the page. Stored as string to preserve formatting (e.g., `"1万+"`, `"4.8"`, `"TOP 3"`). |
| `metric_value_numeric`   | number  | optional | Numeric interpretation of the metric value, if derivable (e.g., `10000` for `"1万+"`). `null` when numeric conversion is unreliable. |
| `metric_unit`            | string  | optional | Unit of the metric value: `count`, `percent`, `score`, `rank`, `label`. |
| `metric_qualifier`       | string  | optional | Qualifier text that accompanies the metric (e.g., `"this month"`, `"last 30 days"`, `"all time"`). |
| `is_inferred`            | boolean | optional | `true` if the numeric value was inferred or estimated (e.g., from a vague label). Defaults to `false`. |
| `metric_confidence`      | string  | optional | Confidence in the accuracy of the metric extraction: `high`, `medium`, `low`, `unknown`. |
| `collection_date`        | string  | required | ISO 8601 date when the metric was observed. |
| `data_quality_notes`     | string  | optional | Notes about limitations of this metric. Per SYSTEM.md lines 135-136, sales must not be inferred from review counts, rankings, or popularity labels. |
| `record_version`         | integer | optional | Version number. |

### Platform interpretation cross-reference

Per SYSTEM.md lines 166-197, platform metrics from e-commerce platforms may
support observed listing price and displayed review proxies but cannot
independently establish clinical efficacy. Metrics from social platforms may
support content engagement patterns.

Per SYSTEM.md lines 135-136: exact sales must not be inferred from review
counts, rankings, popularity labels, or unspecified platform indicators.
When `is_inferred` is `true`, state the inference method in
`data_quality_notes`.

---

## consumer narrative (consumer_narrative)

A consumer narrative record captures a recurring theme, sentiment, or
reported experience from consumer-generated content. It does not constitute
evidence of clinical efficacy.

**File format**: JSONL. One narrative observation per line.

### Fields

| Field                    | Type    | Required | Description |
|--------------------------|---------|----------|-------------|
| `narrative_id`           | string  | required | Unique identifier. Format: `cn-{platform}-{YYYYMMDD}-{sequential}`. |
| `source_id`              | string  | required | Source record ID where this narrative was observed. |
| `product_master_id`      | string  | optional | Product master record ID, if the product is identified. |
| `narrative_type`         | string  | required | Category of narrative. One of: `usage_scenario`, `efficacy_experience`, `side_effect`, `convenience`, `taste_palatability`, `value_perception`, `purchase_motivation`, `comparison`, `repeat_purchase`, `switching_reason`, `safety_concern`, `other`. |
| `narrative_theme`        | string  | required | A concise label summarizing the recurring theme (e.g., `"tastes bitter"`, `"works overnight"`, `"expensive for quantity"`). |
| `narrative_summary`      | string  | required | Descriptive summary of the narrative pattern, supported by examples from the source. |
| `narrative_sentiment`    | string  | required | Dominant sentiment: `positive`, `neutral`, `negative`, `mixed`, `unknown`. |
| `frequency_estimate`     | string  | optional | Qualitative frequency of this theme among relevant content: `dominant`, `common`, `occasional`, `rare`, `unknown`. |
| `frequency_estimate_note`| string  | optional | Explanation of how the frequency was estimated (e.g., `"12 of 50 reviews"`, `"based on top 100 comments"`). |
| `example_quote`          | string  | optional | An illustrative verbatim quote from a single piece of content. |
| `example_quote_source_id`| string  | optional | Source ID for the specific example quote. |
| `is_sponsored`           | boolean | optional | Whether the content is marked as sponsored or paid promotion. |
| `content_author_type`    | string  | optional | Type of content author: `ordinary_user`, `key_opinion_consumer`, `professional_kol`, `media_account`, `brand_account`, `verified_practitioner`, `unknown`. |
| `follower_count`         | integer | optional | Follower count of the author at the time of collection, if displayed. |
| `collection_date`        | string  | required | ISO 8601 date when the narrative source was collected. |
| `record_version`         | integer | optional | Version number. |

### Consumer content rules cross-reference

Per consumer-content-rules.md and SYSTEM.md lines 136-140:

- Consumer narratives support consumer narrative analysis only, not causal
  efficacy claims.
- Consumer reviews must not be treated as proof of efficacy or safety.
- Distinguish between sponsored and organic content using `is_sponsored`.
- Distinguish between KOL and ordinary user content using
  `content_author_type`.

---

## conflict record (conflict)

A conflict record documents a disagreement between two sources, two
observations, or between a claim and evidence. Conflicts are preserved so
that report readers can assess uncertainty.

**File format**: JSONL. One conflict per line.

### Fields

| Field                    | Type    | Required | Description |
|--------------------------|---------|----------|-------------|
| `conflict_id`            | string  | required | Unique identifier. Format: `cf-{platform}-{YYYYMMDD}-{sequential}`. |
| `conflict_type`          | string  | required | Category of conflict. One of: `source_vs_source`, `platform_vs_platform`, `claim_vs_evidence`, `listing_vs_product`, `price_discrepancy`, `identity_mismatch`, `regulatory_vs_claim`, `timeline_change`, `other`. |
| `subject_type`           | string  | required | What kind of record the conflict is about: `product`, `listing`, `price`, `claim`, `metric`, `regulatory_status`, `identity`. |
| `subject_ids`            | array   | required | Record IDs involved in the conflict (source IDs, product IDs, listing IDs, claim IDs, etc.). At least two entries. |
| `field_in_conflict`      | string  | required | The specific field or attribute that differs (e.g., `"price"`, `"manufacturer"`, `"dosage"`, `"support_status"`). |
| `value_a`                | string  | required | The value from the first source/record. |
| `value_b`                | string  | required | The value from the second source/record. |
| `source_a_id`            | string  | required | Source ID supporting value_a. |
| `source_b_id`            | string  | required | Source ID supporting value_b. |
| `resolution_status`      | string  | required | Current resolution status: `unresolved`, `resolved_in_favor_of_a`, `resolved_in_favor_of_b`, `merged`, `both_retained`, `requires_human_review`. |
| `resolution_note`        | string  | optional | Explanation of how the conflict was resolved or why it remains unresolved. |
| `resolution_date`        | string  | optional | ISO 8601 date when the resolution was made. |
| `detection_date`         | string  | required | ISO 8601 date when the conflict was detected. |
| `detection_method`       | string  | optional | How the conflict was found: `automated_comparison`, `manual_review`, `normalization_check`, `claim_verification`, `cross_platform_compare`. |
| `severity`               | string  | optional | How materially the conflict affects conclusions: `critical`, `major`, `minor`, `informational`. Defaults to `minor`. |
| `record_version`         | integer | optional | Version number. |

### Conflict handling cross-reference

Per SYSTEM.md lines 138, 163-164, and 293:

- Do not silently select one value when credible sources conflict. Preserve
  the conflict record.
- When identity remains uncertain after conflicting evidence, preserve
  separate records and create a human-review question.
- If official and commercial sources materially conflict, request human
  clarification.

---

## competitor metric (competitor_metric)

A competitor metric is a derived record that places one product in a
competitive context alongside other products. It is calculated from
underlying product records, listing records, price observations, and claims.

**File format**: JSONL for intermediate storage; CSV or XLSX for final
report output per build-competitor-matrix.py conventions.

### Fields

| Field                        | Type    | Required | Description |
|------------------------------|---------|----------|-------------|
| `competitor_metric_id`       | string  | required | Unique identifier. Format: `cm-{project}-{sequential}`. |
| `product_master_id`          | string  | required | Product master record ID for this competitor entry. |
| `product_version_id`         | string  | optional | Specific version record ID, if the comparison is version-specific. |
| `competitor_group`           | string  | required | Which competitive group this product belongs to: `direct_competitor`, `indirect_competitor`, `functional_alternative`, `same_ingredient`, `same_target_population`, `same_price_band`. See competitor-selection.md. |
| `product_name`               | string  | required | Display name for the competitor (brand + product name). |
| `brand`                      | string  | required | Brand name. |
| `version`                    | string  | optional | Version descriptor (e.g., `"2024 formulation"`, `"new packaging"`). |
| `dosage_form`                | string  | required | Dosage form. Use `"not_applicable"` for non-pharmaceutical competitors or aggregated entries. |
| `active_ingredient`          | string  | optional | Primary active ingredient name. |
| `dose`                       | string  | optional | Dose per unit (e.g., `"500 mg"`, `"10 mg/mL"`). Use `"unknown"` when dose is not identified. |
| `package_size`               | string  | optional | Package description (e.g., `"30 tablets"`, `"100 mL"`). |
| `price`                      | number  | optional | The most representative price for comparison. |
| `currency`                   | string  | optional | ISO 4217 currency of the price. |
| `price_type`                 | string  | optional | Type of price selected: `list_price`, `sale_price`, `unit_price`, `daily_cost`, `range_low`, `range_high`, `unknown`. |
| `normalized_unit_price`      | number  | optional | Price normalized to a standard unit (e.g., per-g, per-mL, per-tablet). |
| `normalized_unit_price_unit` | string  | optional | Unit of the normalized price. |
| `daily_cost`                 | number  | optional | Estimated daily cost based on labeled or guideline-recommended dose. |
| `daily_cost_currency`        | string  | optional | Currency of the daily cost. |
| `daily_cost_assumptions`     | array   | optional | List of assumptions used in daily cost calculation. |
| `claims_summary`             | string  | optional | Concise summary of key commercial claims for this product, or a link to the relevant commercial claim records. |
| `claim_support_level`        | string  | optional | Overall evidence support for major claims: `direct`, `partial`, `indirect`, `insufficient`, `contradicted`, `not_assessed`. |
| `channels`                   | array   | optional | List of platform/channel codes where this product was observed (e.g., `["tmall", "jd", "official"]`). |
| `platform_count`             | integer | optional | Number of distinct platforms where the product was found. |
| `listing_count`              | integer | optional | Number of listings collected for this product. |
| `date_of_data`               | string  | optional | ISO 8601 date representing the most recent data used for this competitor entry. |
| `data_quality`               | string  | optional | Overall data quality for this entry: `high`, `medium`, `low`, `unknown`. |
| `main_limitations`           | text    | optional | Free-text description of important limitations affecting this competitor entry (e.g., `"price from single listing only"`, `"dose assumed from product label"`). |
| `source_ids`                 | array   | required | List of source IDs that contributed to this competitor metric. |
| `record_version`             | integer | optional | Version number. |

### Competitor selection cross-reference

Competitor inclusion follows competitor-selection.md rules. The
`competitor_group` field documents which inclusion criterion was met. When
the product list requires human approval, preserve both the automated
candidate list and the final approved list as separate artifacts.

### Report generation cross-reference

Per report-generation SKILL.md lines 219-250, competitor tables in reports
must include: product, brand, version, dosage form, dose, spec, price,
price type, normalized price, daily cost, claims, channel, data date,
data quality, and main limitations. These correspond directly to the fields
above.
