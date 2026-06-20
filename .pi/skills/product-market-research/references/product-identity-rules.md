# Product Identity Rules

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: SYSTEM.md (product identity rules lines 148-165),
output-record-specification.md (product record, identity_certainty field),
detect-duplicate-products.py (weighted matching algorithm)

---

## Identity Levels

Every item encountered during research belongs to one of five identity
levels. These levels form a hierarchy: one product can have many versions,
one version can appear across many SKUs, one SKU can appear in many listings,
and one listing may be a bundle of multiple products.

### Product (core product)

The fundamental therapeutic or consumer product, identified by its active
ingredient(s), intended use, and manufacturer. The product persists across
packaging changes, dose variations, and regional formulations. Examples:

- Ibuprofen 200 mg tablets manufactured by Pfizer
- Centrum Silver multivitamin manufactured by Haleon
- Panadol Extra paracetamol 500 mg + caffeine 65 mg manufactured by Haleon

The product level carries the `product_master_id` field. Two items with the
same `product_master_id` are considered the same core product regardless of
packaging or regional variation, provided the manufacturer and active
ingredient identity match.

### Version (product version)

A specific formulation, dose, delivery form, or release variant of a product.
Versions differ from the core product in quantifiable, label-level attributes
such as:

- Dose per unit (e.g., 200 mg vs 400 mg ibuprofen)
- Dosage form (e.g., tablet vs capsule vs oral suspension)
- Release mechanism (e.g., immediate release vs extended release)
- Formulation variant (e.g., sugar-free, gluten-free, pediatric)
- Flavor variant (e.g., mint vs citrus antacid)

One product may have many versions. Each version carries a
`product_version_id`. Items at the same product master but different versions
are NOT interchangeable for pricing or efficacy comparisons.

### SKU (stock keeping unit)

A unique identifier assigned by the manufacturer or distributor to a specific
package configuration of a product version. The SKU encodes:

- Package quantity (e.g., 30 tablets vs 100 tablets)
- Package type (e.g., bottle vs blister pack vs single-dose sachet)
- Regional packaging variant (e.g., CN-market box vs US-market bottle)

A SKU is manufacturer-assigned and stable across listings. Different SKUs may
refer to the same product version at different package sizes. SKUs are not
always visible on e-commerce listings and may be stored in backend data or
barcodes (UPC, EAN, GTIN).

### Listing (platform listing)

An offer or product page observed on a specific platform at a specific time.
Multiple listings can refer to the same SKU (different sellers), or one
listing may represent a different seller's offer of the same product. The
listing is the level at which price, seller, and platform metrics are
observed.

Two listings can share the same product version and SKU but differ in:

- Seller (official store vs third-party distributor)
- Price and promotions
- Shipping region and cost
- Platform metrics (review count, rating, sales volume display)

The listing is the unit of observation in e-commerce research. Listings are
never merged; they are linked to a product record via `product_master_id`.

### Bundle (seller-created combination)

A grouping of multiple products sold together as a single offer, typically
assembled by the seller rather than the manufacturer. Bundles include:

- Multi-pack: same product, multiple units (e.g., "buy 2 get 10% off")
- Variety pack: different flavors or variants of the same brand
- Cross-product bundle: different products sold together (e.g., shampoo +
  conditioner)
- Promotional bundle: product + gift item (e.g., supplement + branded shaker)
- Trial or sample bundle: multiple small sizes for testing

Bundles are recorded as listing records with `price_type: "bundle_price"` and
must link to each component product's `product_master_id`. Bundle pricing is
not used for per-unit or daily-cost calculations of individual component
products unless the bundle includes sufficient labeling to determine
individual product contributions.

---

## Registration Number Priority

When a product carries a regulatory registration or filing number, that
number is the single most authoritative identity signal. Matching by
registration number takes precedence over all other fields.

### Priority order

1. **Registration or filing number** (highest)
2. **Manufacturer or distributor name**
3. **Brand name**
4. **Standard product name** (generic + brand + form + dose)
5. **Dosage form**
6. **Unit dose / strength**
7. **Package quantity and description**
8. **Market region** (tiebreaker only)

### Jurisdiction-specific registration types

| Jurisdiction | Registration type      | Example format                           |
|--------------|------------------------|------------------------------------------|
| China (NMPA) | Guo Yao Zhun Zi        | 国药准字H10960100                        |
| China (NMPA) | Guo Yao Shu Zi         | 国药准字S20230001                        |
| China (NMPA) | Bei An Hao (备案号)     | 国妆备进字J202312345                     |
| China (CFDA) | Health food (卫食健字)  | 国食健字G20230001                        |
| US (FDA)     | NDC (National Drug Code) | 12345-678-90 (labeler-product-package) |
| US (FDA)     | OTC Monograph          | M012 (monograph identifier)              |
| EU           | CE marking number      | CE 0123 (notified body + certificate)    |
| EU           | MA number              | EU/1/23/1234                             |
| JP (PMDA)    | Approval number        | 21800AMZ00012000                         |
| KR (MFDS)    | Item number            | 201800001 (품목허가번호)                 |

### Rules

- A matching registration number between two records means they refer to the
  same approved product, regardless of packaging, listing title, or seller
  differences.
- When one record has a registration number and another does not, the record
  with the number is the authoritative reference. Do not assume the unlabeled
  record matches without additional evidence.
- When two records have different registration numbers, they are different
  products at the regulatory level, even if names are identical. Create a
  conflict record with `conflict_type: "identity_mismatch"`.
- Registration numbers from different jurisdictions are not comparable. A
  China Guo Yao Zhun Zi number does not match a US NDC, even for the same
  active ingredient.
- Registration jurisdiction must be recorded alongside the number in
  `registration_jurisdiction` and `registration_type`.

---

## Matching Rules

### Brand matching

Brand names are compared after case normalization and removal of leading or
trailing whitespace. Common brand suffixes and prefixes that are non-essential
(e.g., "(R)" registered mark, "(TM)", "brand") are stripped before matching.

Tolerated differences (do not break identity):

- Abbreviation: "Johnson & Johnson" vs "J&J"
- Localized translation: "Swisse" vs "Swisse (斯维诗)"
- Common transliteration: "Centrum" vs "善存"
- Missing legal entity suffix: "Pfizer" vs "Pfizer Inc."

Non-tolerated differences (break identity):

- Different sub-brands: "Centrum Silver" vs "Centrum Kids" (different
  versions, same parent brand)
- Different brand families from the same manufacturer: "Tylenol" vs "Motrin"
  (both McNeil/Johnson & Johnson, but different brands)

### Manufacturer matching

Manufacturer names are compared after normalization to a canonical form.
Maintain a manufacturer alias table for known equivalences:

- "Pfizer Inc." matched to "Pfizer", "Pfizer Pharmaceuticals Ltd."
- "Haleon" matched to "Haleon plc", "GSK Consumer Healthcare" (former name)

When the manufacturer name differs and cannot be resolved through aliases,
treat as different products even if all other fields match. Generic drug
manufacturers produce bioequivalent but distinct products with different
registration numbers and different NDCs.

### Dosage form matching

Dosage forms use a controlled vocabulary from output-record-specification.md:
tablet, capsule, cream, injection, oral_solution, powder, patch, etc.

Two items with different dosage forms are different versions at minimum, and
different products in most cases. Exceptions where different forms are
considered the same product:

- A product with both tablet and capsule versions of the same dose (same
  registration family, e.g., some OTC analgesics). These are different
  VERSIONS under the same product master.
- A product with an oral solution and oral suspension variant (different
  versions, same product master if same manufacturer and ingredient).

### Dose / strength matching

Unit dose is compared after normalization to base units (mg, g, mL, ug).

- Different doses = different versions (e.g., 200 mg vs 400 mg ibuprofen).
- Same dose expressed in different units normalizes before comparison (e.g.,
  0.5 g and 500 mg are the same dose).
- Fixed-dose combinations must match ALL active ingredient doses. A product
  containing amlodipine 5 mg + atorvastatin 10 mg is not the same version as
  amlodipine 5 mg + atorvastatin 20 mg.

### Package quantity matching

Package quantity differences alone do NOT change product identity:

- 30-tablet bottle vs 100-tablet bottle = same product, same version,
  different SKU
- 10 mL single-use vial vs 50 mL multi-dose vial = same product, different
  SKU (and potentially different version if preservative content differs)

Package quantity is stored as part of the SKU/listing, not the product master.

### Region matching

Region is encoded as ISO 3166-1 alpha-2. Products in different regions may
be:

- **Same product**: identical formulation, manufacturer, and registration
  (e.g., a globally standardized supplement sold in CN and JP with the same
  registration family).
- **Different version same product**: same brand and manufacturer but
  different dose or excipients per regional regulation (e.g., vitamin D
  dose may differ between US and EU versions of the same brand).
- **Different product**: different registration number, different
  manufacturer, or different formulation entirely (e.g., a product sold
  under the same brand name in two countries but manufactured by different
  local subsidiaries).

Never collapse regional versions into one product without explicit evidence
that formulations, doses, and manufacturing are identical (prohibited per
SYSTEM.md line 165).

---

## Same Core, Different Package

When the same product is sold in different package configurations:

### Acceptable configurations of the same core product

- Bottle vs blister pack of the same tablets (same dose, same count)
- Single bottle vs multi-pack bundle (core product is identical)
- Retail packaging vs hospital dispensing packaging (different labeling, same
  product)
- Sample size vs full size (different SKU, same product version)

### Rules

- The product master record captures the core identity once. Different
  packages are captured as separate listing records linked to the same
  `product_master_id` and `product_version_id`, with their own
  `package_quantity` and `package_description`.
- Do not create separate product records for different package types of the
  same product version.
- Flag the relationship in `package_description` (e.g., "original retail
  packaging" vs "hospital bulk pack").

---

## Old vs New Packaging

When a manufacturer updates product packaging but the formulation, dose, and
registration number remain unchanged:

### Identity handling

- The product master identity, version identity, and registration number are
  unchanged. The product record remains the same.
- The listing record should note the packaging variant in `data_quality_notes`
  (e.g., "new packaging observed June 2025").
- If both old and new packaging appear concurrently in the market, preserve
  both listing records and link them to the same product record.
- If the old packaging listing is known to be discontinued, add a note in
  the listing record but do not remove it from analysis. Historical prices
  from old packaging remain valid observations.

### When packaging change indicates a formulation change

If the packaging update coincides with a change to the registration number,
ingredient list, dose, or dosage form, treat as a new product version or,
if the changes are substantial, a new product. Create a conflict record.

---

## Cross-Border Versions

Products sold in multiple regions under the same brand may differ in:

- Dose (regional regulatory limits, e.g., EU max vitamin D 1000 IU vs US 2000 IU)
- Excipients (allowed additives differ by jurisdiction)
- Labeling language and required warnings
- Manufacturer (local subsidiary or contract manufacturer)
- Registration number (each jurisdiction issues its own)

### Identity handling

- A cross-border version with the same brand and manufacturer but a different
  registration number is a different product version (different
  `product_version_id`) under the same product master. Example: Centrum in
  the US vs Centrum in China, both manufactured by Haleon but with different
  NMPA filing number vs US NDC.
- A cross-border version with the same brand but a different manufacturer
  (e.g., a brand licensed to different companies in different regions) is a
  different product entirely. Example: a supplement brand manufactured by
  Company A in the US and by Company B under license in China.
- When assembling a product record for a cross-border version, set the
  `region` field to the market where the listing was observed. Do not
  inherit the region from the parent brand's origin country.
- Cross-border versions must not be averaged together in pricing analysis
  unless all formulation attributes are confirmed identical.

---

## Seller-Created Bundles

Bundles created by a seller (not the manufacturer) require special handling:

### Identification

A bundle is suspected when the listing title mentions multiple products, a
quantity larger than any standard package, or terms like "组合装", "套装",
"超值装", "value pack", "variety pack", "gift set". Bundles often include
items from different product lines or brands.

### Identity handling

- A bundle listing is recorded as a listing record with its own
  `listing_id` and `product_master_id` set to `"unknown"` or a designated
  bundle placeholder.
- Each component product in the bundle is recorded separately as a product
  record if it can be individually identified.
- The listing record's `package_description` describes the bundle contents.
- Bundle-level price observations carry `price_type: "bundle_price"`.
- Bundle prices are NOT used for per-unit or daily-cost calculations of
  component products unless the bundle components are individually labeled
  with their prices or the bundle contains identical units of a single
  product (e.g., a 3-pack of the same item). In that case, divide the
  bundle price by the number of units to derive a per-unit price, and
  document the assumption in `daily_cost_assumptions`.
- Cross-product bundles (e.g., shampoo + conditioner) must not be used to
  derive pricing for either component product individually.

---

## Fuzzy-Match Confidence

When registration numbers are not available and matching relies on field
comparison, assign a confidence level using the `identity_certainty` field
from output-record-specification.md:

| Confidence  | Definition                                                  | When to use                                                  |
|-------------|-------------------------------------------------------------|--------------------------------------------------------------|
| confirmed   | Identity is certain. Registration number matches, or all    | Manufacturer + brand + name + form + dose all match.         |
|             | identity-critical fields match without conflict.            | Registration number available and matches.                   |
| probable    | Strong match but minor field missing or unverifiable.       | All fields match but registration number is missing.         |
|             |                                                             | Brand, manufacturer, form, and dose match but region is     |
|             |                                                             | uncertain.                                                   |
| possible    | Moderate match with some differences or missing data.       | Brand and name match but manufacturer is unknown.            |
|             |                                                             | Same name and dose but different form.                       |
|             |                                                             | Same name but source does not specify manufacturer.          |
| uncertain   | Cannot determine identity with available evidence. Human    | Only name matches, no other fields verifiable.              |
|             | review required.                                            | Conflicting registration numbers or manufacturers.           |
|             |                                                             | Listing title is generic and product cannot be resolved.    |

### Mandatory human review conditions

Set `identity_certainty` to `"uncertain"` and escalate for human review when:

1. Two records agree on name and brand but disagree on manufacturer or
   registration number.
2. Only the product name is available and no manufacturer, registration
   number, or dose can be verified.
3. A listing's registration number is partially visible and cannot be fully
   read (e.g., blurred in an image).
4. A product appears under the same brand and name in two regions, but
   differences in formulation or manufacturer cannot be confirmed or ruled
   out with available evidence.
5. A registration number from one jurisdiction is presented as equivalent to
   another jurisdiction's registration without official cross-recognition
   documentation.
6. A seller claims a product is "the same as" a branded product but the
   registration number and manufacturer differ.
7. A bundle listing mixes products from different brands or manufacturers,
   making component identity ambiguous.
8. A product has been reformulated or repackaged, and it is unclear whether
   the current listing reflects the old or new version.

When human review is triggered, preserve all conflicting records and do not
merge any records until a human resolves the identity.

---

## Examples

### Positive examples (correctly matched as same product)

**Example 1: Same product, different listings, different sellers**

Listing A: "Centrum Silver Adults 50+ Multivitamin 120 Tablets"
  - Seller: Seller X (third-party)
  - Price: CNY 159
  - NMPA filing: not shown

Listing B: "Centrum Silver 50+ Multivitamin 120 Tablets Official"
  - Seller: Haleon Official Store
  - Price: CNY 179
  - NMPA filing: 国食健字G2023XXXX

Result: **Same product**. Manufacturer (Haleon), brand (Centrum Silver), form
(tablet), dose, and package quantity (120) match. The official listing provides
the registration number. The third-party listing links to the same product
master despite the price difference and missing registration number on the
listing page. `identity_certainty: "confirmed"` after the official listing
is identified. The two listings remain separate listing records.

**Example 2: Same product, different packaging (old vs new)**

Listing A: "Vitamin D3 1000 IU 90 Softgels (White Bottle)"
Listing B: "Vitamin D3 1000 IU 90 Softgels (New Amber Bottle Design)"

Result: **Same product**. Manufacturer, brand, form, dose, and quantity are
identical. The packaging change is cosmetic. Both listings map to the same
product master and version. Note the packaging difference in
`data_quality_notes`.

**Example 3: Same product, different package quantity (different SKU)**

Listing A: "Tylenol Extra Strength 500 mg 100 Caplets Bottle"
Listing B: "Tylenol Extra Strength 500 mg 200 Caplets Value Size Bottle"

Result: **Same product and version, different SKU**. Dose, form, brand, and
manufacturer all match. Quantity differs (100 vs 200). The product master
record has one entry. The two SKUs have separate listing records linked to
the same product master. Per-unit price comparison between the two is valid.

### Negative examples (incorrect to match as same product)

**Example 4: Same name, different registration number**

Listing A: "Ibuprofen 200 mg Tablets 100 count, Brand A"
  - Registration: NDC 12345-678-90
  - Manufacturer: Manufacturer X

Listing B: "Ibuprofen 200 mg Tablets 100 count, Brand A"
  - Registration: NDC 98765-432-10
  - Manufacturer: Manufacturer Y

Result: **Different products**. Same name and same dose, but different
registration numbers indicate different approved products (different
manufacturers or different approved applications). Do not merge.
`identity_certainty: "uncertain"` if attempted automated match; escalate
for human review. This is a case where "never merge based solely on similar
names" applies.

**Example 5: Same brand, different region, different registration**

Listing A: "Swisse Women's Multivitamin 60 Tablets (Australia)"
  - Registration: Australian ARTG 123456
  - Manufacturer: Swisse Wellness Pty Ltd

Listing B: "Swisse Women's Multivitamin 60 Tablets (China)"
  - Registration: 国食健字J2023XXXX
  - Manufacturer: Same parent company, different manufacturing entity

Result: **Different versions**. The products share a brand and name but have
different registration numbers from different jurisdictions. Formulation may
differ per local regulations. They map to the same product master but
different product versions. Do not collapse into one record.

**Example 6: Different dose, same brand and name otherwise**

Listing A: "Centrum Silver 50+ Multivitamin, 200 mg Calcium"
Listing B: "Centrum Silver 50+ Multivitamin, 500 mg Calcium"

Result: **Different versions**. Brand and name match. Dose is different.
These are two versions of the same product master. They must have separate
product version records. Pricing and efficacy comparisons between them must
account for the dose difference.

---

## Prohibitions

### Never merge based solely on similar names

This is the most important rule in product identity resolution. Do not merge
two records into the same product based on name similarity alone. A similar
or identical product name is never sufficient evidence of identity because:

- Different manufacturers produce the same generic drug under the same name.
- Different registration numbers distinguish different approved products even
  when names, doses, and forms are identical.
- Counterfeit or look-alike products may use identical or near-identical names.
- Cross-border versions share brand names but differ in registration and
  formulation.
- Listing titles are written by sellers and may be inaccurate, exaggerated, or
  deliberately misleading.

If only the name matches and no other identity field can be verified, set
`identity_certainty` to `"uncertain"` and require human review.

### Other prohibitions

- Do not collapse regional versions into one product (SYSTEM.md line 165).
- Do not treat a seller-created bundle as a manufacturer product record.
- Do not assume two listings with the same barcode (UPC/EAN/GTIN) are the
  same product without confirming manufacturer and registration number.
  Barcodes can be reused or assigned to distributor-specific packages.
- Do not use listing title alone to determine dosage form or dose. Verify
  against the product label, official site, or regulatory database.
- Do not merge records with conflicting manufacturer names unless a verified
  alias relationship exists in the alias table.
- Do not infer equivalence between two registration numbers from different
  jurisdictions without official cross-recognition documentation.

---

## Summary Decision Table

| Scenario                                                          | Identity level        | Identity_certainty  | Action                       |
|-------------------------------------------------------------------|-----------------------|---------------------|------------------------------|
| Registration number matches                                       | Same product          | confirmed           | Merge to one product record  |
| Registration differs, everything else matches                     | Different products    | uncertain           | Preserve separate, human     |
| Same brand, form, dose, different package quantity                | Same product, diff SKU| confirmed           | Same product master, diff    |
|                                                                   |                       |                     | listing                      |
| Same brand and name, different manufacturer                       | Different products    | uncertain           | Preserve separate, human     |
| Same product, old vs new packaging                                | Same product          | confirmed           | Same product master, note    |
|                                                                   |                       |                     | packaging                     |
| Cross-border, same brand and manufacturer, diff registration      | Same master, diff ver | probable            | Same master, diff version    |
| Cross-border, same brand, different manufacturer                  | Different products    | uncertain           | Preserve separate, human     |
| Bundle with multiple different products                           | Bundle (composite)    | confirmed (bundle)  | Listing record only, link    |
|                                                                   |                       |                     | components                    |
| Only name matches, no other fields                                | Cannot determine      | uncertain           | Human review required        |
| Different dose, everything else matches                           | Same master, diff ver | confirmed           | Separate version records     |
| Different formulation (tablet vs liquid), same brand and dose     | Same master, diff ver | confirmed           | Separate version records     |
