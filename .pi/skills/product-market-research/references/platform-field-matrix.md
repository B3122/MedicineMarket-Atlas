# Platform Field Matrix

Canonical field requirements, limitations, and collection notes for each
platform type used in product-market research.

**Version**: 1.0.0
**Last updated**: 2025-06-20
**Cross-references**: SYSTEM.md (platform interpretation rules lines 166-197,
source hierarchy lines 96-124, evidence discipline lines 126-143),
skill-builder.md (platform list lines 43-68),
output-record-specification.md (record type definitions)

---

## How to read this document

Each platform section defines:

- **Supported information**: What claims and facts this platform type can
  reasonably establish, per SYSTEM.md lines 166-197.
- **Unsupported information**: What this platform type cannot independently
  establish. Collecting these claims is allowed, but the source limitation
  must be preserved in the record.
- **Required fields**: Fields that MUST be collected whenever they are visible
  on the page. If a required field is not displayed, record `null` and note
  the absence.
- **Optional fields**: Fields that SHOULD be collected when present but whose
  absence does not block record creation.
- **Common misjudgments**: Frequent errors in interpreting data from this
  platform type, with the correction.
- **Collection frequency**: How often data from this platform type should be
  refreshed.
- **Screenshot needed**: Whether a visual capture is required as evidence.
- **Login required**: Whether the collector needs an authenticated session.

---

## Official Brand Site

### Supported information

- Official product positioning and brand messaging.
- Declared ingredients, dose, and formulation as listed by the manufacturer.
- Manufacturer identity and country of origin.
- Official usage instructions and recommended dosage.
- Official commercial claims approved by the brand.
- Authorized retailer or distributor lists (when published).
- Product registration or certification numbers when displayed
  (e.g., FDA NDC, CFDA filing number).

Per SYSTEM.md lines 171-177, official brand sites are the preferred source for
positioning, ingredient, dose, manufacturer, and official claims.

### Unsupported information

- Actual transaction prices. List price may be shown, but observed selling
  price requires e-commerce data.
- Consumer satisfaction or real-world outcomes.
- Comparative efficacy against competing products unless independently
  sourced.
- Market share, sales volume, or revenue.
- Third-party reviews or ratings.
- Stock or availability at retail.

### Required fields

- `source_type`: Always `"official_brand_site"`.
- `brand_name`: As displayed on the site.
- `manufacturer_name`: Legal manufacturer or brand owner.
- `product_name`: Full product name as listed.
- `url`: Full URL of the product page.
- `collection_date`: ISO 8601 date of access.
- `screenshot_path` or `archive_path`: Reference to the saved page capture.

### Optional fields

- `declared_ingredients`: Ingredient list with amounts if shown.
- `dosage_form`: Tablet, capsule, powder, liquid, etc.
- `unit_dose`: Strength per unit (e.g., "500 mg").
- `package_size`: Count or volume per package.
- `serving_size`: Per the usage instructions.
- `list_price`: Manufacturer's suggested retail or list price if displayed.
- `registration_number`: Any regulatory identifier displayed.
- `official_claims`: Commercial claims extracted from the page, each tagged
  as `commercial_claim` in the output record.
- `usage_instructions`: Directions for use as published.
- `target_audience`: Intended user group if specified.

### Common misjudgments

| Misjudgment | Correction |
|---|---|
| Treating list price as market price. | List price is the manufacturer's suggested price. Actual price at retail may differ. Record as `list_price` with a distinct `price_type`. |
| Assuming all displayed claims are evidence-based. | Official claims on brand sites are commercial assertions. They describe what the brand wants consumers to believe, not what has been proven. Each claim must be recorded as a `commercial_claim` and verified against independent sources. |
| Treating absence of an ingredient as confirmation it is not present. | Brand sites may omit inactive ingredients or excipients. Absence is not proof of non-inclusion. |
| Confusing brand-operated sites with authorized distributor sites. | Verify domain ownership. A site that looks like a brand site may be run by a distributor. Check WHOIS or the site's legal notice. |

### Collection frequency

- At project start and once per major product update cycle.
- Revisit only if the brand launches a new version or if a claim dispute arises.

### Screenshot needed

Yes. Full-page screenshot or PDF archive is required. The dynamic nature of
modern brand sites (pop-ups, region redirects) means the page may not render
identically on a later visit.

### Login required

No. Brand sites are generally publicly accessible. If the site requires
registration or a healthcare-professional credential, treat this as a
restricted-access variant and note the access level.

---

## E-commerce Platform

### Supported information

- Observed listing price with promotion context.
- Promotion type (coupon, flash sale, bundle, subscription discount).
- Package configuration (count, volume, bundle contents).
- Seller identity and seller tier (official store, authorized reseller,
  third-party seller).
- Displayed review count, rating score, and sales volume proxies.
- Platform-specific sales language (title, bullet points, A+ content).
- Shipping and fulfillment information.

Per SYSTEM.md lines 179-186, e-commerce platforms are the primary source for
price, promotion, package, seller, and review or transaction proxies.

### Unsupported information

- Clinical efficacy or safety. Reviews and ratings are consumer opinions,
  not scientific evidence.
- Verified ingredient accuracy. Ingredient lists on e-commerce pages are
  copied from the brand or uploaded by sellers and may be outdated or wrong.
- Manufacturer claims unless the page is the brand's official storefront on
  that platform.
- Actual sales volume. What platforms display (e.g., "10,000+ sold") is often
  a cumulative or fuzzy count, not a precise figure. Record the displayed
  value as a `platform_metric` with the platform's label for it.
- Price history or trend. The page shows only the current price unless a
  historical price feature is explicitly available.

### Required fields

- `source_type`: Always `"ecommerce"`.
- `platform_name`: Specific platform (e.g., "Tmall Global", "Amazon US",
  "JD.com").
- `product_title`: Listing title as displayed.
- `current_price`: Numeric value of the displayed selling price.
- `currency`: ISO 4217 code.
- `seller_name`: Store or seller name.
- `seller_type`: One of `official_brand`, `authorized_reseller`,
  `third_party`, `unknown`.
- `url`: Full URL of the listing page.
- `collection_date`: ISO 8601 date of access.
- `price_type`: `list_price`, `sale_price`, `member_price`, `promotional_price`,
  or `subscription_price`.

### Optional fields

- `original_price`: Crossed-out or MSRP reference price if shown.
- `promotion_details`: Coupon value, flash sale timing, minimum purchase, etc.
- `package_count`: Number of units per purchase (single, twin pack, etc.).
- `unit_dose`: If the listing specifies strength per unit.
- `dosage_form`: If stated in the listing.
- `review_count`: Displayed number of reviews.
- `rating`: Displayed average rating (0.0-5.0 scale or platform equivalent).
- `sales_metric`: Any displayed sales volume proxy, tagged with the
  platform's label.
- `shipping_cost`: Shipping fee if separately displayed.
- `fulfillment_type`: "Fulfilled by platform", "Fulfilled by seller", etc.
- `variants`: Available options (flavor, size, pack count) if shown.
- `seller_location`: Country or region of the seller, if displayed.

### Common misjudgments

| Misjudgment | Correction |
|---|---|
| Treating display price as the final transaction price. | Coupons, member discounts, and flash sales can reduce the actual price. The price observed on the listing page is the starting point, not necessarily what consumers pay. Record coupon or promotion information separately when visible, and always tag `price_type`. |
| Interpreting review counts as a reliable proxy for quality. | Reviews on e-commerce platforms are subject to selection bias, incentivized reviews, and fake reviews. They support consumer sentiment analysis but do not independently establish product quality or efficacy. |
| Treating sales volume displays as precise transaction counts. | Platforms vary: some show "10,000+ sold" as a lifetime cumulative, others show monthly figures. Record the exact displayed string and the platform's label verbatim. |
| Assuming the seller is always the brand. | On marketplace-style platforms, many listings come from third-party resellers. Always record `seller_name` and `seller_type`. A third-party seller does not have authority to make binding claims about the product. |
| Equating "out of stock" with "discontinued." | Stock status is a snapshot. A product may be out of stock temporarily. Do not mark as discontinued based on a single observation of stock absence. |

### Collection frequency

- At project start and once per week during active research for price tracking.
- Revisit during major shopping events (Singles Day, Black Friday, Prime Day)
  if price volatility is relevant.
- Revisit only if the listing changes for a static snapshot project.

### Screenshot needed

Yes. E-commerce pages change frequently. A screenshot or PDF archive is
required to preserve the observed price, promotion, and listing content at the
time of collection. Capture the full page including price, seller info, and
shopping cart button.

### Login required

Sometimes. Many e-commerce platforms allow browsing product pages without
login. Member-only prices, coupons, and order history require login.
For standard listing data, anonymous access is generally sufficient. Note
whether the session was authenticated.

---

## Pharmacy Platform

### Supported information

- Authorized dispensing information.
- Registered dosage and administration (for prescription products).
- Regulatory classification (OTC vs. prescription).
- Pharmacy-specific pricing, which may differ from general e-commerce.
- Availability status at pharmacy level.
- Pharmacy-level substitution or generic alternatives.

Pharmacy platforms occupy a middle ground between official regulatory sources
and commercial e-commerce. Their ingredient and dosage information is
generally more reliable than general e-commerce because it must support
dispensing decisions. However, pricing and availability are still
point-in-time observations.

### Unsupported information

- Clinical efficacy or safety. Pharmacy platforms present what is approved
  for dispensing, not what has been proven in the specific context.
- Manufacturer's official positioning. Pharmacy content may paraphrase or
  abbreviate official prescribing information.
- Consumer satisfaction or outcomes.
- Market-wide pricing. Pharmacy pricing is chain-specific and regional.
- Off-label usage or unapproved indications.

### Required fields

- `source_type`: Always `"pharmacy"`.
- `pharmacy_name`: Name of the pharmacy chain or platform.
- `product_name`: As listed on the pharmacy site.
- `current_price`: Numeric price displayed.
- `currency`: ISO 4217 code.
- `regulatory_classification`: `prescription`, `OTC`, `behind_the_counter`,
  or `unknown`.
- `url`: Full URL of the product page.
- `collection_date`: ISO 8601 date of access.

### Optional fields

- `dosage_form`: As displayed on the pharmacy listing.
- `unit_dose`: Strength per unit.
- `package_size`: Count or volume.
- `generic_equivalent`: Name of any listed generic alternative.
- `insurance_coverage_note`: Any displayed insurance or reimbursement info.
- `substitution_info`: Note on mandatory or optional substitution policy.
- `prescription_required`: Boolean, if explicitly stated.
- `availability_status`: In stock, out of stock, limited supply.
- `storage_requirements`: If listed (e.g., refrigerated).
- `patient_restrictions`: Age limits, ID requirements, etc.

### Common misjudgments

| Misjudgment | Correction |
|---|---|
| Treating pharmacy-stated dosage as a clinical recommendation. | Pharmacy listings typically reproduce regulatory-approved prescribing information. The dosage shown is the approved range, not a recommendation for a specific patient. |
| Assuming pharmacy price represents the market. | Pharmacy pricing varies by chain, region, insurance contract, and membership program. A single pharmacy observation is not a market-wide price. |
| Confusing pharmacy platform content with medical advice. | Pharmacy platforms provide dispensing information, not personalized medical guidance. Do not characterize pharmacy text as professional medical advice. |
| Treating availability at one pharmacy as universal availability. | Stock and distribution vary by chain and region. Record pharmacy name and location alongside availability. |

### Collection frequency

- At project start and once per week during active price research.
- Revisit if regulatory classification changes are suspected.

### Screenshot needed

Yes. Pharmacy pages contain regulated information and should be preserved.
Full-page screenshot including price, regulatory classification, and dosage
information.

### Login required

Sometimes. Some pharmacy platforms require age verification or account login
to view product details. Checkout and member pricing always require login.
For standard listing data, anonymous access is acceptable if available.

---

## Short-video and Live-streaming Platform

### Supported information

- Marketing framing and sales pitch content.
- Promotional offers and flash-sale pricing.
- Influencer or host claims about the product.
- Consumer engagement metrics (views, likes, shares, comments count).
- Real-time or time-limited pricing and bundling.
- Sponsored-content patterns (paid promotion tags, affiliate links).
- Usage scenarios demonstrated or described by hosts.

Per SYSTEM.md lines 188-196, social and content platforms support consumer
narratives, usage scenarios, marketing framing, and influencer patterns.
They do not independently establish clinical efficacy.

### Unsupported information

- Clinical efficacy, safety, or therapeutic value. Host claims and consumer
  testimonials on these platforms are not scientific evidence regardless of
  presentation style.
- Verified ingredient or dosage accuracy. Hosts may misstate or exaggerate
  product composition.
- Independent product reviews. Many videos are sponsored, and the boundary
  between organic and paid content is often opaque.
- Long-term price. Flash sales, limited-time offers, and live-stream
  pricing are event-specific and may not reflect regular pricing.
- Objective comparison between products. Influencer comparisons are
  marketing content, not systematic evaluations.

### Required fields

- `source_type`: Always `"short_video_live"`.
- `platform_name`: Specific platform (e.g., "Douyin", "Kuaishou",
  "TikTok Shop", "Taobao Live").
- `creator_or_host_name`: Account name of the video creator or live host.
- `content_type`: `short_video` or `live_stream`.
- `content_url`: Direct URL to the video or stream recording.
- `collection_date`: ISO 8601 date of access.
- `sponsored_status`: `sponsored`, `not_sponsored`, or `unclear`.
  If unclear, record the indicators that led to uncertainty.

### Optional fields

- `product_mentioned`: Product name(s) as mentioned by the host.
- `promotional_price`: Price stated during the stream or in the video
  description.
- `offer_details`: Time limit, stock limit, bundle contents, discount code.
- `claims_made`: Claims by the host or creator, each recorded as a
  `commercial_claim` with `channel: "short_video_live"`.
- `engagement_metrics`: View count, like count, share count, comment count
  as displayed at collection time.
- `comment_sample`: Representative consumer comments (preserve as
  `consumer_narrative` records, not as proof of efficacy).
- `affiliate_link`: Listed affiliate or commission link if visible.
- `live_duration`: Length of the live stream if available.
- `viewer_peak`: Peak concurrent viewers for live streams if displayed.

### Common misjudgments

| Misjudgment | Correction |
|---|---|
| Treating host claims as expert endorsements. | A host claiming to be a doctor, nutritionist, or expert does not make their claims clinical evidence. The claim is still a commercial assertion. Verify credentials independently. |
| Treating high engagement as product quality. | High view counts or likes reflect content virality, not product effectiveness. A video can be widely viewed because it is entertaining or controversial. |
| Assuming "influencer says it works" is consumer evidence. | Sponsored content is advertising. Distinguish paid promotion from organic consumer reporting. If the video carries a paid-partnership tag, it is advertising. |
| Taking flash-sale prices as regular market prices. | Live-stream prices are often the lowest available for a limited window. Record the price with full context of the promotion. Do not use live-stream prices for market-average calculations. |
| Treating the absence of a sponsored-content tag as proof of organic content. | Not all paid content is tagged. Use additional signals (excessive praise, discount codes, #ad in description) to assess sponsorship. |

### Collection frequency

- At project start and once during each major campaign or shopping event.
- Ongoing monitoring is generally not needed unless the research question
  involves real-time marketing dynamics.

### Screenshot needed

Yes. Video content is ephemeral; live streams may not be archived. Capture
the video page (title, creator, engagement metrics, description) and a
representative video frame if possible. For live streams, a contemporaneous
recording or screenshot of the pricing and offer details.

### Login required

Yes for full engagement metrics. Anonymous browsing typically shows view
counts but may not show comments, creator analytics, or purchase links.
Login may be required to access product detail pages linked from videos.

---

## Content Community

### Supported information

- Consumer narratives and real-world usage descriptions.
- Recurring themes in consumer experience (likes, dislikes, side effects).
- Comparison discussions among consumers.
- Usage scenarios and routines.
- Common concerns, questions, and misconceptions.
- Influencer and organic content patterns.
- Product mentions in broader lifestyle or health discussions.

Per SYSTEM.md lines 188-196, content communities are a primary source for
consumer narratives, usage scenarios, and recurring themes. The same platform
rule applies: they do not independently establish clinical efficacy.

### Unsupported information

- Clinical efficacy or safety. A popular post claiming a product "works" is
  a consumer opinion, not evidence of efficacy.
- Verified ingredient or dosage information. User-generated posts may
  contain incorrect product details.
- Representative satisfaction rates. Community content is subject to
  self-selection bias. People who post are not representative of all users.
- Objective product comparisons. Comparison posts reflect individual
  preferences and experiences.
- Aggregate market data. Community discussions do not yield statistically
  reliable metrics.
- Authenticity of product claims made by users. A user reporting an outcome
  may be mistaken, exaggerating, or fabricating.

### Required fields

- `source_type`: Always `"content_community"`.
- `platform_name`: Specific platform (e.g., "Xiaohongshu", "Zhihu",
  "Reddit", "Douban", "Bilibili").
- `post_url`: Direct URL to the post or thread.
- `author_identifier`: Username or handle. Do NOT collect real names.
- `collection_date`: ISO 8601 date of access.
- `content_type`: `post`, `comment`, `thread`, `review`, or `article`.

### Optional fields

- `post_title`: Title or subject line.
- `author_follower_count`: If displayed and relevant to authority assessment.
- `sponsored_status`: `sponsored`, `not_sponsored`, or `unclear`.
- `product_mentioned`: Product name(s) mentioned in the post.
- `narrative_theme`: Theme code from the consumer narrative taxonomy
  (see output-record-specification.md).
- `sentiment`: Positive, negative, mixed, or neutral toward the product.
- `engagement_metrics`: Likes, comments, shares, saves as displayed.
- `comment_sample`: Representative replies that add context.
- `crosspost_links`: Links to the same content on other platforms.

### Common misjudgments

| Misjudgment | Correction |
|---|---|
| Treating frequently mentioned benefits as proven efficacy. | Frequency of mention reflects what consumers talk about, not what is clinically true. Common themes can arise from marketing campaigns, social trends, or placebo effects. |
| Treating community content as demographically representative. | Community users skew younger, more urban, and more engaged. Do not extrapolate community sentiment to the general population. |
| Treating detailed personal stories as reliable evidence. | A vivid narrative is not more reliable than a brief one. Detail does not equal accuracy. Personal stories are self-reported and unverified. |
| Confusing paid seeding with organic buzz. | Brands often seed products to community influencers. Look for patterns: multiple posts with similar language, sudden spikes in mentions, or content that links to the same affiliate landing page. |
| Assuming "no negative posts" means high satisfaction. | Negative posts may be deleted by moderators, removed by the platform, or suppressed by brand legal requests. Absence of negative content is not evidence of absence of negative experiences. |

### Collection frequency

- At project start and once midway through the research cycle.
- Ongoing monitoring only if the research question involves tracking
  sentiment trends over time.

### Screenshot needed

Conditional. If the post is likely to be deleted or edited (controversial
topic, negative review, competitor mention), take a screenshot. For stable
content or platform-archived discussions, the URL may be sufficient with a
note of the collection date.

### Login required

Sometimes. Most content communities are publicly readable. Login may be
required to view NSFW/age-restricted content, full comment threads, or
user profiles. Do not use login to access private user data.

---

## Regulatory Database

### Supported information

- Official product registration or listing status.
- Regulatory classification and approval category.
- Approved indications, ingredients, and dosage.
- Manufacturer and establishment registration.
- Safety warnings, recalls, and adverse event data.
- Marketing authorization holder and history.
- Label or prescribing information as approved by the regulator.

Regulatory databases are the highest-authority source for registration,
approval status, and safety information. They take precedence over all
commercial and consumer sources.

### Unsupported information

- Current market price or commercial availability. Regulatory databases
  do not track pricing.
- Consumer satisfaction or real-world usage patterns.
- Market share or competitive landscape.
- Unofficial, off-label, or emerging usage not yet reviewed by the
  regulator.
- Product quality or efficacy relative to competitors.
- Post-market observational data unless the database specifically includes
  such surveillance (e.g., FAERS for adverse events).

### Required fields

- `source_type`: Always `"regulatory_database"`.
- `regulatory_authority`: Name of the issuing authority
  (e.g., "FDA", "NMPA", "EMA", "PMDA", "TGA").
- `database_name`: Specific database or portal name.
- `product_name`: Name as registered.
- `registration_or_approval_number`: Unique identifier assigned by the
  authority.
- `registration_status`: `active`, `suspended`, `withdrawn`, `expired`,
  or `unknown`.
- `url`: Direct URL to the registration record or query result.
- `collection_date`: ISO 8601 date of access.

### Optional fields

- `manufacturer_name`: As registered with the authority.
- `marketing_authorization_holder`: If different from manufacturer.
- `approved_indications`: Listed therapeutic indications.
- `active_ingredients`: Approved ingredient list with strengths.
- `dosage_form`: As registered.
- `approval_date`: Date of initial or most recent approval.
- `expiration_date`: Registration validity end date if applicable.
- `classification`: OTC, prescription, traditional medicine, medical device,
  food supplement, etc.
- `safety_warnings`: Boxed warnings, contraindications, known adverse
  reactions as listed.
- `recall_information`: If the product is subject to a current recall.
- `label_url`: Link to the official label or prescribing information PDF.
- `approval_history`: List of approval events with dates.
- `regulatory_action`: Any noted regulatory action (warning letter,
  import alert, etc.).

### Common misjudgments

| Misjudgment | Correction |
|---|---|
| Treating registration as proof of efficacy. | Registration confirms the regulator found the product acceptably safe and effective for its approved indication based on the data submitted. It is not an independent endorsement and does not guarantee effectiveness in all populations. |
| Assuming the regulatory database is complete for all products. | Not all products are registered in publicly queryable databases. Supplements, foods, and cosmetics often have different or less transparent registration requirements. |
| Confusing product registration with establishment registration. | A registered facility does not mean all products from that facility are registered. Verify product-level registration separately. |
| Treating absence of safety warnings as proof of safety. | Safety warnings are issued when problems are identified and reported. Absence of a warning means no signal has been confirmed, not that no signal exists. |
| Assuming all countries use the same product identifier. | Cross-border products may have different registration numbers in each jurisdiction. Do not assume a single ID applies globally. |

### Collection frequency

- At project start and once before the final report.
- Revisit only if a regulatory action (recall, warning, label change) is
  publicly announced during the research period.

### Screenshot needed

Conditional. Regulatory database pages are generally stable and authoritative.
A screenshot is recommended for the specific registration record to preserve
the exact registration number, status, and date. Search result pages do not
need to be screenshotted unless the result page is the only evidence of
registration.

### Login required

Mostly no. Major regulatory databases (FDA, EMA, NMPA public portal, TGA)
are publicly searchable. Some advanced features (bulk download, API access,
full adverse event reports) may require registration or an account.

---

## Industry Report

### Supported information

- Market size, growth rate, and segmentation estimates.
- Competitive landscape analysis and market share rankings.
- Distribution channel analysis.
- Consumer demographic and behavior profiles.
- Pricing benchmarks and average selling prices.
- Regulatory environment summaries.
- Technology and innovation trends.
- Forecasts and projections (with methodology noted).

Industry reports synthesize data from multiple sources and are useful for
market-level context that cannot be observed from individual platforms.

### Unsupported information

- Specific product-level pricing or sales data for individual SKUs
  (unless the report is a dedicated product teardown).
- Clinically validated efficacy or safety conclusions. Industry reports
  summarize market data, not clinical evidence.
- Real-time data. Reports reflect the market at the time of research, which
  is typically 6-18 months before publication.
- Independent verification of underlying data. Report authors rely on
  proprietary models, surveys, and interviews that cannot be independently
  checked.
- Granular regional or demographic data unless the report's methodology
  explicitly covers that breakdown.

### Required fields

- `source_type`: Always `"industry_report"`.
- `report_title`: Full title as published.
- `publisher`: Research firm or publisher name
  (e.g., "Euromonitor", "IQVIA", "Mintel", "Grand View Research").
- `publication_date`: Date or year of publication.
- `url_or_doi`: Link to the report or a permanent identifier.
- `collection_date`: ISO 8601 date of access.

### Optional fields

- `report_type`: Market sizing, competitive landscape, consumer survey,
  trend analysis, pricing study, etc.
- `geography_covered`: Region or countries covered.
- `segments_covered`: Product categories or market segments analyzed.
- `methodology_summary`: Brief description of how the data was collected
  and analyzed.
- `page_reference`: Specific page or section number for each data point
  extracted.
- `data_points`: Key numerical findings (market size, growth rate, share
  percentages), each with the exact page reference.
- `limitations_notes`: Any limitations the report itself acknowledges.
- `raw_data_availability`: Whether underlying data tables are accessible.

### Common misjudgments

| Misjudgment | Correction |
|---|---|
| Treating industry report figures as primary data. | Industry reports are secondary sources. Their figures are synthesized from surveys, interviews, and proprietary models. Always note the publisher and methodology. |
| Assuming forecasts are predictions. | Forecasts are modeled projections based on current trends and assumptions. They are not guarantees of future outcomes. Record the underlying assumptions when available. |
| Treating paid/subscription reports as authoritative. | Commercial research firms have reputational incentives for accuracy but also have commercial interests. A paid report is not inherently more accurate than a free one. Evaluate methodology, not price. |
| Confusing "market size" definitions across reports. | "Market size" can mean retail sales, wholesale sales, manufacturer revenue, or consumer spending. Different reports use different definitions. Always record the definition used. |
| Mixing data from reports with different base years. | Market data from different years cannot be directly compared without adjusting for inflation, category growth, and methodology changes. Note the base year and currency year. |

### Collection frequency

- At project start. Industry reports are published on an annual or quarterly
  cycle.
- Revisit only if a newer edition is published during the research period
  and the difference is material.

### Screenshot needed

Conditional. For freely available reports and executive summaries, a
screenshot of the relevant page with the data point and source attribution
is recommended. For paid reports, record the exact page number, figure/table
number, and the publisher. Do not screenshot behind a paywall without
authorization.

### Login required

Sometimes. Many industry report publishers require registration for PDF
downloads (free with registration) or a paid subscription. Executive
summaries and press releases are typically publicly accessible.

---

## Academic Database

### Supported information

- Peer-reviewed study results, including methodology and statistical
  findings.
- Systematic reviews and meta-analyses synthesizing multiple studies.
- Clinical trial registrations with protocol details.
- Evidence-based clinical guidelines.
- Mechanistic studies (in vitro, in vivo, ex vivo).
- Observational studies and real-world evidence analyses.

Academic databases are the primary source for establishing clinical efficacy
and safety. Per SYSTEM.md, every important study must be recorded with DOI,
PMID, trial identifier, or official source URL.

### Unsupported information

- Current market pricing or commercial availability. Academic studies do
  not track market conditions.
- Consumer sentiment or user experience outside of controlled studies.
- Regulatory status or approval. A study may investigate an unapproved
  use or a product not yet submitted for regulatory review.
- Brand market share or competitive positioning.
- Product availability in specific regions or channels.
- Real-world usage patterns not captured in the study design.

### Required fields

- `source_type`: Always `"academic_database"`.
- `database_name`: Specific database
  (e.g., "PubMed", "ClinicalTrials.gov", "Cochrane Library", "Scopus",
  "Web of Science", "CNKI", "Google Scholar").
- `citation_title`: Full article title.
- `authors`: At least first author last name and initials.
- `journal_or_source`: Journal name, preprint server, or conference.
- `publication_year`: Year of publication or posting.
- `doi_or_pmid`: At least one persistent identifier
  (DOI, PMID, or registry ID).
- `url`: Link to the record.
- `collection_date`: ISO 8601 date of access.

### Optional fields

- `study_design`: RCT, cohort, case-control, cross-sectional, systematic
  review, meta-analysis, in vitro, etc.
- `population`: Study population description, including sample size.
- `intervention`: Product, dose, duration as studied.
- `comparator`: Control or comparison condition.
- `primary_outcome`: The main outcome measure.
- `key_findings`: Summary of results relevant to the research question.
- `funding_source`: As declared in the publication.
- `conflicts_of_interest`: Declared conflicts of the authors.
- `registry_id`: Clinical trial registry number (e.g., NCT number,
  ChiCTR number).
- `ethics_approval`: Statement of ethics committee approval.
- `limitations`: Limitations acknowledged by the authors.
- `mesh_terms`: MeSH or keyword terms for search recall.
- `study_status`: For trials: not yet recruiting, recruiting, active,
  completed, terminated, withdrawn.

### Common misjudgments

| Misjudgment | Correction |
|---|---|
| Treating a single study as conclusive. | A single study, regardless of design, is one piece of evidence. Systematic effects require replication across studies, populations, and settings. |
| Equating statistical significance with clinical significance. | A statistically significant result may have a small effect size that is not clinically meaningful. Record effect size and confidence intervals. |
| Treating an abstract as the full study. | Conference abstracts and preprint titles may not reflect the final peer-reviewed publication. Do not cite an abstract as equivalent to a published paper. |
| Assuming "published in a peer-reviewed journal" guarantees validity. | Peer review reduces error but does not guarantee correctness. Retractions, corrections, and replication failures occur even in high-impact journals. Check retraction and correction status. |
| Overgeneralizing study populations. | Results from a study in one population (e.g., healthy adults, specific age group, single country) may not apply to other populations. Note the demographic scope. |
| Treating observational studies as establishing causation. | Observational studies can identify associations but cannot establish causation unless they use causal inference methods. Distinguish association from causation in the evidence record. |

### Collection frequency

- At project start and once before the final report.
- Revisit if the research question involves rapidly evolving evidence
  (e.g., COVID-19 treatments) or if a key study is pre-publication.

### Screenshot needed

No. Academic database records are stable and permanently citable via DOI or
PMID. A screenshot of the abstract page is optional for convenience but not
required. Do screenshot if the study is behind a paywall and only the
abstract is accessible.

### Login required

Mostly no. PubMed, ClinicalTrials.gov, Cochrane Library abstracts, and Google
Scholar are publicly accessible. Full-text access may require institutional
subscription or individual payment. An API key (e.g., NCBI API key) is
recommended but not required for basic searching.

---

## Revision history

| Date | Change |
|---|---|
| 2025-06-20 | Initial version. All 8 platform types defined per skill-builder.md. |
