# Competitor Selection Rules

Defines how competitors are typed, included, excluded, counted, and approved
during product-market research.

**Version**: 1.0.0
**Last updated**: 2025-06-20
**Cross-references**: SYSTEM.md (product identity boundaries lines 148-165),
skill-builder.md lines 100-116, output-record-specification.md,
product-identity-rules.md

---

## Competitor Type Definitions

Six competitor types cover the competitive landscape of a pharmaceutical or
health product. Every candidate competitor must be assigned to at least one
type. A single product can belong to multiple types.

### Direct competitor

A product that targets the same indication, uses the same therapeutic
mechanism or ingredient class, and is marketed to the same consumer segment
in the same region.

**Definition**: Same indication, same mechanism class, same consumer segment,
same region.

**Examples**:
- Two omega-3 softgels both labeled "supports cardiovascular health,"
  sold in Germany, each taken 1 capsule daily.
- Two melatonin gummy brands both labeled "helps with occasional
  sleeplessness," sold in the US, each containing 5 mg melatonin per
  serving.

### Indirect competitor

A product that targets the same indication but uses a different mechanism
or ingredient class, or targets a related but not identical segment.

**Definition**: Same or overlapping indication, different mechanism or
ingredient class.

**Examples**:
- An L-theanine chewable for stress vs. a chamomile-based nighttime tea
  for relaxation. Same endpoint (stress relief), different mechanisms.
- A probiotic capsule for digestive regularity vs. a fiber powder for
  bowel movement support. Same general need, different active approach.

### Functional substitute

A product that meets the same consumer need or solves the same problem
without sharing ingredients or mechanisms. Functional substitutes compete
on outcome, not composition.

**Definition**: Same consumer need or problem, different composition or
mechanism entirely.

**Examples**:
- A caffeine-free herbal sleep tea substitute for a melatonin tablet.
  The consumer wants "fall asleep faster"; the compositions are unrelated.
- A topical lidocaine patch substitute for an oral NSAID for localized
  muscle pain. Same pain-relief need, different route and ingredient.

### Same-ingredient competitor

A product that shares the same active ingredient (or ingredient combination)
at any dose, in any formulation, from any manufacturer. Used for ingredient-
level cost and positioning analysis.

**Definition**: Same active ingredient or ingredient combination.

**Examples**:
- All vitamin D3 1000 IU softgels on a market, regardless of brand.
- Any magnesium glycinate powder or capsule, regardless of claim or brand.
- Any product listing "ashwagandha root extract" as the active ingredient,
  even if the target population differs.

### Same-target-population competitor

A product marketed to the same demographic, lifestyle, or health-condition
segment, regardless of ingredients or mechanism.

**Definition**: Overlapping target consumer profile (age, gender, life stage,
health concern, lifestyle).

**Examples**:
- Products labeled "for pregnant women" even if one is a multivitamin and
  another is a fish oil.
- Products labeled "for people with diabetes" including glucose support
  supplements, sugar-free protein bars, and diabetic foot creams.
- Products labeled "for athletes" including electrolyte powders, joint
  support supplements, and protein bars.

### Same-price-band competitor

A product occupying the same absolute or per-serving price band as the
subject product. Used to understand price positioning and price elasticity
expectations.

**Definition**: Price within the same band: absolute price within +- 20%
OR per-serving daily cost within +- 25% of the subject product.

**Examples**:
- A probiotic priced at CNY 199-299 per bottle when the subject product
  is CNY 249 per bottle.
- A daily-cost range of USD 1.00-1.80 per day when the subject product
  costs USD 1.40 per day.

---

## Inclusion Criteria

A competitor may be included if it meets ALL of these criteria:

1. **Market presence**: Available for purchase in the target market during
   the research period. Out-of-stock, discontinued, or pre-order products
   are excluded unless specifically required by the research brief.
2. **Identifiable product**: The product must have a name, brand, or
   identifier sufficient to distinguish it from other products. Commodities
   sold without a brand identifier (e.g., bulk powders without labeling)
   are excluded.
3. **Assignable type**: The product must fit at least one of the six
   competitor types defined above.
4. **Verifiable source**: At least one source record supports the
   product's identity, pricing, or claims used for comparison. Products
   known only from unchecked social-media mentions or unverifiable user
   testimonials are excluded.
5. **Minimum evidence**: At least one of price, daily cost, or a major
   commercial claim must be observable. Products for which none of these
   can be obtained are excluded.

---

## Exclusion Criteria

A product must be excluded if it meets ANY of these conditions:

1. **Wrong jurisdiction**: Not sold or authorized in the target market.
   Cross-border versions of the same core product are treated as separate
   products and included only if the research brief covers that region.
2. **Non-consumer product**: Products intended exclusively for
   professional or institutional use (e.g., hospital-only formulations,
   bulk clinical ingredients) unless the brief explicitly includes them.
3. **Identical to subject**: The same product as the subject of research
   under the product identity rules (SYSTEM.md lines 148-165). A product
   is identical when it matches on registration number, manufacturer,
   brand, dosage form, unit dose, and package configuration.
4. **Ambiguous identity**: Product identity cannot be resolved even after
   applying product-identity-rules.md matching criteria. These should be
   flagged for human review rather than forcibly included or excluded.
5. **No current data**: The only available source records are more than
   18 months old with no indication the product is still in market.

---

## Maximum Competitor Count

The total number of competitors in a single research batch must fall within
these bounds:

| Context                          | Minimum | Recommended | Maximum |
|----------------------------------|---------|-------------|---------|
| Narrow scope (single ingredient) | 4       | 8           | 12      |
| Broad scope (multi-category)     | 6       | 12          | 15      |
| Same-price-band only             | 4       | 8           | 12      |

**Rules**:
- No single competitor type may exceed 60% of the total competitor count
  unless explicitly justified in the research notes.
- When more candidates exist than the maximum, selection must prioritize
  diversity across types, mechanisms, price bands, and evidence quality.
- The maximum may be exceeded only with documented human approval.

---

## Platform Heat and Trending Data Rules

Platform heat, trending scores, popularity rankings, and engagement metrics
may not be used as the sole or primary basis for competitor inclusion.

### Permitted uses of heat data

- **Screening signal**: A product that appears in platform trend lists may
  be flagged as a candidate, but it must still pass all inclusion criteria.
- **Supplementary evidence**: Heat data may strengthen the case for including
  a borderline candidate when other criteria (price, ingredient match, target
  population) are already met.
- **Competitor metric field**: Platform heat may be recorded as a
  `platform_metric` observation within the competitor's record (see
  output-record-specification.md), but it must not be the deciding factor
  for inclusion.

### Prohibited uses of heat data

- **Sole inclusion criterion**: A product may not be included only because
  it is "trending," "viral," or "top selling" without meeting at least two
  of the competitor-type criteria.
- **Omitting non-trending competitors**: Competitors that do not appear in
  trending lists but satisfy inclusion criteria must still be considered and
  must be selected if they improve type coverage or evidence quality.
- **Skewing type distribution**: Heat-based selection must not result in a
  competitor set where one type dominates solely because that type has more
  trending products.

### Rationale

Platform heat reflects algorithmic amplification, paid promotion, and
short-term consumer attention, not market significance or product quality.
A product that has been steadily sold for years may be more relevant than
a viral newcomer. Competitor sets that rely on popularity alone introduce
systematic bias toward well-funded marketing campaigns and away from generic,
private-label, or niche products that may be equally important for
positioning analysis.

---

## Bias Avoidance Strategies

The following strategies are mandatory during competitor selection.

### Strategy 1: Type-balanced sampling

When the candidate pool exceeds the maximum count, select at least one
competitor from each applicable type before adding a second from any type.
This prevents any single type (typically direct competitors) from crowding
out other relevant types.

### Strategy 2: Multi-source candidate generation

Generate the candidate list from at least three independent source categories:

- Platform search and category browsing (ecommerce, pharmacy, social).
- Ingredient or registration database queries.
- Industry reports, market analyses, or researcher domain knowledge.

Relying on a single source category (e.g., only ecommerce search results)
introduces platform-specific coverage gaps.

### Strategy 3: Negative-case inclusion

Actively search for competitors that occupy different positions on price,
quality, or brand perception. Include at least one lower-priced and one
higher-priced competitor when available. This prevents the set from being
skewed toward premium brands or well-known names.

### Strategy 4: Evidence-quality weighting

When choosing between two candidates that fit the same type and are otherwise
comparable, prefer the one with higher-quality source records. Evidence
quality is assessed per data-quality-scoring.md on dimensions of source
authority, field completeness, page freshness, and direct observation.

### Strategy 5: Blinded initial screening

When feasible, screen candidate competitors on product identity and inclusion
criteria before reviewing their pricing, ratings, or popularity metrics.
This prevents awareness of "winners" from biasing the selection toward
products with favorable metrics.

### Strategy 6: Documented exclusion reasons

Every candidate that meets inclusion criteria but is excluded must have a
brief documented reason. The reason must reference a specific exclusion
criterion or a capacity limit. Examples:

- "Excluded: wrong jurisdiction (not sold in target market)."
- "Excluded: type quota filled; chose alternative with better evidence
  quality (scores 3.8 vs 2.5)."

---

## Human Approval Requirements

Human approval must be obtained before finalizing the competitor set under
any of the following conditions.

### Condition 1: Maximum exceeded

If the analysis requires more than 15 competitors, or more than 12 for a
narrow-scope batch, documented human approval is required. The request must
state the proposed count, the reason (e.g., "7 direct competitors needed
because each uses a distinct delivery system"), and the additional value.

### Condition 2: Type imbalance

If any single type exceeds 60% of the total count, and the imbalance cannot
be corrected by adding competitors of other types (e.g., because no other
type candidates exist), human approval is required.

### Condition 3: Competitor identity uncertain

If after applying product-identity-rules.md the researcher cannot determine
whether two records refer to the same product, or whether a product belongs
in the set, the uncertainty must be presented to a human with the available
evidence and a clear question. The human may decide to include, exclude, or
request additional data.

### Condition 4: Novel or ambiguous category

If the subject product belongs to a category not previously researched by
this system (no previous competitor set exists in the knowledge base), the
initial competitor list must be reviewed by a human before analysis proceeds.

### Condition 5: Regulatory or compliance sensitivity

If the competitor set includes any of the following, human approval is
required:

- Products under active regulatory scrutiny or safety warning.
- Products that make disease-treatment claims that may cross regulatory
  lines (drug-device boundary, drug-supplement boundary).
- Products in a category recently subject to regulatory guidance changes
  or enforcement actions.

### Approval process

1. The researcher prepares a candidate list with type assignments, inclusion
   justification, and the specific condition triggering the approval.
2. A human reviewer (product manager, regulatory lead, or domain expert)
   approves, rejects, or modifies the list.
3. The human's decision and rationale are recorded in the research output
   (see competitor-metric record in output-record-specification.md).
4. The competitor set is not used for downstream analysis until approval is
   recorded.

---

## Integration with Product Identity Boundaries

Competitor selection must respect the product identity rules defined in
SYSTEM.md (lines 148-165). The following table maps each identity
distinction to its competitor-selection implication:

| SYSTEM.md identity distinction          | Competitor selection implication                        |
|-----------------------------------------|--------------------------------------------------------|
| Same listing                            | Only one listing record is needed; duplicates removed. |
| Same SKU, different seller              | Seller is a field on the listing, not a separate       |
|                                         | competitor.                                            |
| Same core product, different package    | Same competitor; select the most common package size.  |
| Different active-ingredient dose        | Separate competitor if dose change is clinically       |
|                                         | meaningful (e.g., 5 mg vs 10 mg melatonin).            |
| Different formulation / dosage form     | Separate competitor if formulation affects use         |
|                                         | (tablet vs gummy vs powder).                           |
| Domestic vs cross-border version        | Separate competitor only if both are in-market.        |
| Old vs new packaging                    | Same competitor; prefer current packaging.             |
| Official product vs seller bundle       | Bundle is not a competitor; treat as a listing of the  |
|                                         | core product.                                          |
| Similar name, different manufacturer    | Separate competitor; verify registration identifier.   |
| Different registration or filing ID     | Separate competitor; registration ID is definitive.    |

When identity remains uncertain after applying these rules, follow Human
Approval Condition 3 above.
