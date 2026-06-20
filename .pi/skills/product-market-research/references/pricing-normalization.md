# Pricing Normalization

Canonical rules for collecting, normalizing, and comparing prices across
platforms, regions, and product configurations.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: output-record-specification.md (listing record price
fields, price observation record), schemas/price-observation.schema.json,
skill-builder.md (lines 84-99 pricing requirements), SKILL.md (prohibition on
live-stream/retail price mixing).

---

## Table of Contents

1. [Currency](#1-currency)
2. [Tax treatment](#2-tax-treatment)
3. [Price types](#3-price-types)
4. [Unit price](#4-unit-price)
5. [Active ingredient normalized price](#5-active-ingredient-normalized-price)
6. [Daily cost](#6-daily-cost)
7. [Gift handling](#7-gift-handling)
8. [Multi-bottle and multi-pack handling](#8-multi-bottle-and-multi-pack-handling)
9. [Shipping handling](#9-shipping-handling)
10. [FX date and exchange rates](#10-fx-date-and-exchange-rates)
11. [Forbidden calculations when dose is missing](#11-forbidden-calculations-when-dose-is-missing)
12. [Formulas and rounding rules](#12-formulas-and-rounding-rules)
13. [Price type hierarchy for comparison](#13-price-type-hierarchy-for-comparison)

---

## 1. Currency

### 1.1 Currency code

All currency values use ISO 4217 three-letter codes. Always uppercase.

| Code | Currency |
|------|----------|
| `USD` | US Dollar |
| `EUR` | Euro |
| `CNY` | Chinese Yuan |
| `JPY` | Japanese Yen |
| `GBP` | British Pound |
| `KRW` | South Korean Won |
| `TWD` | New Taiwan Dollar |
| `HKD` | Hong Kong Dollar |

Use `"unknown"` when the currency cannot be determined from the source. Do not
infer currency from region alone.

### 1.2 Currency field rule

A `currency` field without a corresponding `price` field is not valid. Every
price value must be accompanied by an explicit currency code.

### 1.3 Original and normalized currency

When a price is converted from one currency to another, preserve:

- `original_price` - the verbatim price string from the source.
- `original_currency` - the original currency code.
- `price` - the numeric value (in original currency, unless converted).
- `currency` - the currency of `price` (same as original unless converted).

---

## 2. Tax treatment

### 2.1 Tax inclusion flag

Every price observation must indicate whether tax is included:

- `includes_tax: true` - the displayed price includes applicable taxes
  (VAT, sales tax, GST, consumption tax, etc.).
- `includes_tax: false` - the displayed price excludes tax; tax is added at
  checkout.
- Omit or set `null` when the tax status cannot be determined from the source.

### 2.2 Regional defaults

When tax status is not explicitly stated, apply these regional conventions:

| Region | Default tax status | Notes |
|--------|--------------------|-------|
| CN | Included | Chinese e-commerce platforms typically show prices with VAT included. |
| JP | Included | Japanese retail prices generally include consumption tax. |
| EU | Varies | EU member states vary. B2C prices often include VAT by law. |
| US | Excluded | US shelf prices typically exclude sales tax. |
| KR | Included | Korean retail prices typically include VAT. |

Document the assumption in `data_quality_notes` when inferring tax status from
region. If uncertain, set `includes_tax` to `null`.

### 2.3 Tax-only price comparisons

When comparing prices across regions with different tax regimes, note the tax
status difference but do not silently add or remove tax. Report each price
with its actual observed tax inclusion flag. If a tax-adjusted comparison is
needed, store the adjusted value separately and document the assumed tax rate.

---

## 3. Price types

Every price observation carries a `price_type` field that classifies the kind
of price observed. Seven distinct types are defined.

### 3.1 Price type definitions

| Price type | Field value | Definition |
|------------|-------------|------------|
| List price | `list_price` | The manufacturer's suggested or official shelf price. No promotions applied. Often labeled as "原价", "市场价", or "建议零售价". |
| Sale price | `sale_price` | The standard everyday price on the platform after routine markdown but before any coupon, membership, or flash promotion. Often labeled as "日常价", "活动价", or "现价". |
| Coupon price | `coupon_price` | Price after applying a platform or store coupon. Requires coupon redemption or automatic deduction at checkout. Often labeled as "券后价". |
| Member price | `member_price` | Price available only to platform members, subscribers, or loyalty program participants. Often labeled as "会员价" or "PLUS价". |
| Live price | `live_price` | Time-limited price offered during a live-streaming session. Available only while the stream is active. Often labeled as "直播价". |
| Subscription price | `subscription_price` | Recurring price under a subscription or auto-delivery plan. Applies only when the buyer commits to repeat purchases. Often labeled as "订阅价" or "周期购价". |
| Bundle price | `bundle_price` | Price for a combined offer of multiple products or multiple units of the same product sold as a set. Often labeled as "组合价", "套装价". |

### 3.2 Live-stream price restriction

Do not combine live-stream prices with ordinary retail prices in any
calculation or comparison. Live-stream prices are:

- Time-limited and available only during the broadcast session.
- Often subsidized by the platform or the streamer.
- Not representative of the standard market price.

A live-stream price observation must be stored with `price_type: "live_price"`
and must not be averaged with or substituted for `sale_price`, `list_price`,
or any other retail price type.

### 3.3 Subscription price note

Subscription prices represent a recurring commitment. When recording a
subscription price, include the billing period in `price_condition`
(e.g., `"subscription_required"`, `"monthly_recurring"`,
`"quarterly_recurring"`). Do not treat a single subscription payment as
equivalent to a one-time purchase price.

### 3.4 Unknown price type

When the price type cannot be determined from the source, use
`"unknown"`. Do not guess the price type.

---

## 4. Unit price

### 4.1 Definition

Unit price is the total price divided by the number of dosage units in the
package. It represents the cost of one individual unit (tablet, capsule,
sachet, mL, g, etc.).

### 4.2 Formula

```
unit_price = price / package_quantity
```

### 4.3 When to calculate

Unit price can be calculated only when both `price` and `package_quantity` are
known. If `package_quantity` is missing or unknown, unit price must be `null`.

### 4.4 Unit selection

Use the base consumption unit for the product's dosage form:

| Dosage form | Unit price unit |
|-------------|-----------------|
| Tablet, capsule, softgel | per tablet / per capsule |
| Oral liquid | per mL |
| Topical cream, ointment | per g |
| Injectable | per mL or per vial |
| Powder, granule | per g or per sachet |
| Patch | per patch |
| Device | per piece |

Preserve the original unit string alongside any normalized value.

### 4.5 Multi-pack unit price

When a product is sold as a multi-pack (e.g., 2 bottles of 30 tablets each),
first determine the total number of units across all containers:

```
total_units = units_per_container * number_of_containers
unit_price = price / total_units
```

Document the multi-pack configuration in `promotion_details` or
`data_quality_notes`.

---

## 5. Active ingredient normalized price

### 5.1 Definition

Active ingredient normalized price (also called dose-standardized price)
expresses the cost per standard unit of the active ingredient (e.g., per mg
of the active pharmaceutical ingredient). This enables price comparison across
products with different per-unit doses.

### 5.2 Formula

```
ai_normalized_price = unit_price / per_unit_dose
```

Where:

- `unit_price` = price per dosage unit (tablet, mL, etc.).
- `per_unit_dose` = amount of active ingredient per dosage unit (e.g., 500 mg
  per tablet).

### 5.3 Units

The unit of the active-ingredient-normalized price combines the currency unit,
dosage unit, and ingredient mass/volume unit:

```
USD / (tablet * mg)  →  USD/mg  (after simplification using the per-tablet dose)
```

Examples:

- A 500 mg tablet priced at USD 0.50 per tablet:
  `0.50 USD/tablet / 500 mg/tablet = 0.001 USD/mg`.
- A 10 mg/mL oral solution at USD 0.80 per mL:
  `0.80 USD/mL / 10 mg/mL = 0.08 USD/mg`.

### 5.4 Multiple active ingredients

When a product contains multiple active ingredients, calculate the
ingredient-normalized price for each active ingredient separately. Document
which ingredient the calculation applies to. Do not sum ingredient doses or
prices across different active ingredients to derive a combined normalized
price.

### 5.5 When to skip

Active ingredient normalized price cannot be calculated when:

- The per-unit dose of the active ingredient is unknown.
- The product has no identified active ingredient
  (e.g., medical devices, certain cosmetics).
- The product uses a non-standardized formulation (e.g., proprietary blend
  without mass disclosure).

In these cases, set the normalized price to `null` and document the reason.

---

## 6. Daily cost

### 6.1 Definition

Daily cost is the estimated cost of using the product for one day at the
labeled or clinically recommended daily dosage. It is the primary metric for
comparing the affordability of competing products.

### 6.2 Formula

```
daily_cost = (price / package_quantity) * daily_dose_units
```

Where:

- `price` = total price of the package (in the observation currency).
- `package_quantity` = total number of dosage units in the package.
- `daily_dose_units` = number of dosage units consumed per day (e.g.,
  2 tablets/day, 15 mL/day).

### 6.3 Step-by-step derivation

For a product with price `P`, package quantity `Q`, and daily dose `D`:

1. **Unit price**: `U = P / Q` (cost per single dosage unit).
2. **Daily cost**: `C = U * D` (cost per day at the labeled dose).

### 6.4 Example

Product: 30 tablets per bottle, priced at CNY 129.00.
Labeled dose: 2 tablets per day.

```
unit_price = 129.00 / 30 = 4.30 CNY per tablet
daily_cost = 4.30 * 2 = 8.60 CNY per day
```

### 6.5 Daily dose source

Every daily cost calculation must record the source of the daily dose used:

| Source | `daily_cost_source` value | Description |
|--------|--------------------------|-------------|
| Product label | `label` | Dose printed on the package or official label. |
| Official website | `official_site` | Dose stated on the brand's official website. |
| Clinical guideline | `clinical_guideline` | Dose from a published clinical guideline or standard of care. |
| Regulatory filing | `regulatory_filing` | Dose from an approved prescribing information or SmPC. |
| Assumption | `assumption` | Dose estimated or inferred; must document the reasoning. |

Prefer `label` over `clinical_guideline` over `assumption`. When the source is
`assumption`, include a detailed explanation in `daily_cost_assumptions`.

### 6.6 Missing dosage prohibition

**Do not calculate daily cost when daily dosage is missing from all
available sources.**

If the daily dose cannot be determined from the product label, official
website, clinical guidelines, or regulatory filings, set `daily_cost` to
`null`. Do not infer, guess, or assume a daily dosage. The absence of a
labeled dosage means the daily cost cannot be meaningfully calculated.

This rule applies regardless of whether the product is a pharmaceutical,
health supplement, or non-pharmaceutical product.

### 6.7 Variable dosage

When a product has a dosage range (e.g., "1 to 2 tablets per day"), record:

- `daily_cost_range_low` - daily cost at the minimum recommended dose.
- `daily_cost_range_high` - daily cost at the maximum recommended dose.

Do not use the midpoint of the range as a single daily cost value unless
documented as an assumption.

### 6.8 Non-daily dosing

For products dosed on a non-daily schedule (e.g., "once weekly", "every 8
hours"), normalize to a daily cost:

- "Once weekly" = dose / 7 days.
- "Every 8 hours" = dose * 3 per day.

Document the conversion in `daily_cost_assumptions`.

---

## 7. Gift handling

### 7.1 Definition

Gifts (also called bonuses, freebies, or samples) are additional items
included with a purchase at no extra cost. They affect the effective unit
price because the buyer receives more product for the same total price.

### 7.2 Gift types

| Gift type | Description | Handling |
|-----------|-------------|----------|
| Same product bonus | Extra units of the same product (e.g., "buy 1 get 1 free", "+50% extra free"). | Adjust package quantity for unit price and daily cost calculations. |
| Different product sample | Free sample of a different product (e.g., "free travel-size moisturizer"). | Do not adjust package quantity. Record gift separately in `gift_or_bonus`. |
| Accessory or tool | Non-consumable item (e.g., measuring spoon, carrying case). | Do not adjust package quantity. Record in `gift_or_bonus`. |
| Coupon or credit | Future discount voucher or store credit. | Do not adjust price. Record in `promotion_details`. |

### 7.3 Same-product bonus adjustment

When the gift consists of additional units of the same product, adjust the
effective package quantity:

```
effective_quantity = paid_quantity + bonus_quantity
effective_unit_price = price / effective_quantity
```

Example: "Buy 2, get 1 free" for a product sold as 30 tablets per bottle:

```
paid_quantity = 60 tablets (2 bottles)
bonus_quantity = 30 tablets (1 free bottle)
effective_quantity = 90 tablets
effective_unit_price = price / 90
```

Document the gift in `gift_or_bonus` and note the quantity adjustment in
`data_quality_notes`.

### 7.4 Different-product gift

When the gift is a different product (not the same SKU), do not adjust the
price or package quantity of the purchased product. Record the gift
description in `gift_or_bonus` for informational purposes only.

---

## 8. Multi-bottle and multi-pack handling

### 8.1 Definition

Multi-bottle or multi-pack offers sell multiple containers of the same product
together. The price may be lower per unit than a single-container purchase.

### 8.2 Normalization

When recording a multi-bundle offer:

1. Record the total price of the bundle.
2. Determine total dosage units across all containers:
   `total_units = units_per_container * container_count`.
3. Calculate unit price using total units:
   `unit_price = bundle_price / total_units`.
4. Calculate daily cost using total units:
   `daily_cost = unit_price * daily_dose_units`.

### 8.3 Single-container baseline

Always also record the single-container price for the same product when
available, so that the per-unit savings of the multi-pack can be quantified.

### 8.4 Example

Product: 30 tablets per bottle.
Offer: 3 bottles for CNY 299.00. Single bottle: CNY 129.00.

Single-container:
```
unit_price = 129.00 / 30 = 4.30 CNY per tablet
```

Multi-pack:
```
total_units = 30 * 3 = 90 tablets
unit_price = 299.00 / 90 = 3.32 CNY per tablet
```

---

## 9. Shipping handling

### 9.1 Shipping cost recording

Record shipping cost separately from the product price whenever possible:

- `shipping_cost` - numeric shipping cost (use `0` for free shipping).
- `shipping_currency` - currency of the shipping cost.
- `includes_shipping` - whether the product price already includes shipping.

### 9.2 Free shipping threshold

When free shipping is conditional (e.g., "free shipping on orders over
CNY 99"), record the condition in `price_condition` or `data_quality_notes`.
Do not adjust the price to account for shipping unless the threshold is
definitively met for the observed purchase.

### 9.3 Shipping in total cost of treatment

For daily cost and total cost of treatment calculations, use the product price
alone. Shipping cost should be reported separately and noted in the report
when it materially affects the total price (e.g., shipping cost exceeds 10%
of the product price).

### 9.4 Regional shipping notes

| Region | Common pattern |
|--------|----------------|
| CN | Free shipping common above low thresholds (e.g., CNY 29-99). |
| JP | Shipping often free above JPY 3,000-5,000. |
| US | Shipping varies widely; free with Amazon Prime or above thresholds. |
| EU | Cross-border shipping within EU often free above EUR 50-100. |

Document the shipping policy as observed, not assumed.

---

## 10. FX date and exchange rates

### 10.1 When to convert

Currency conversion is performed only when prices must be compared across
currencies in a single report. Store prices in their original currency whenever
possible; convert only at the reporting stage.

### 10.2 Exchange rate date

Every currency conversion must record:

- `exchange_rate` - the numeric exchange rate used.
- `exchange_rate_date` - the ISO 8601 date of the exchange rate.
- `exchange_rate_source` - the source of the rate.

### 10.3 Preferred rate sources

Use official or widely recognized sources in this order of preference:

1. Central bank reference rates (PBOC, ECB, Fed, Bank of Japan, etc.).
2. Major financial data providers (Bloomberg, Reuters, XE, OANDA).
3. Platform-displayed conversion rates (only when the platform itself
   performs the conversion for checkout).

Avoid using historical averages or arbitrary date ranges. The exchange rate
date should match the price collection date as closely as possible.

### 10.4 No live rates

This document does not provide live exchange rates. Rates must be obtained
from external sources at the time of analysis and recorded with their source
and date.

---

## 11. Forbidden calculations when dose is missing

### 11.1 Absolute prohibition

**Do not calculate daily cost when the daily dosage is unavailable.**

This applies to:

- `daily_cost` must be `null` when no labeled, official, guideline, or
  regulatory daily dose can be identified.
- `daily_cost` must be `null` when the daily dose is ambiguously stated
  and cannot be confidently quantified (e.g., "take as needed", "apply
  sparingly").
- `daily_cost` must be `null` when only a dosage range exists and neither the
  low nor high end of the range can be selected without an explicit
  assumption. (If assumptions are documented, the range-low and range-high
  may be calculated per section 6.7.)

### 11.2 What is not a valid dose source

The following are **not** valid sources for daily dosage:

- Consumer reviews or comments (e.g., "I take 3 a day").
- Seller recommendations not backed by the label.
- Assumptions based on product category norms.
- General population averages without product-specific labeling.

### 11.3 Derived fields blocked by missing dose

When daily dosage is missing, the following fields must remain `null`:

- `daily_cost`
- `daily_cost_currency`
- `daily_cost_source`
- `daily_dose_used`
- `daily_dose_unit`

The `unit_price` and `ai_normalized_price` can still be calculated from
available `price` and `package_quantity` data, as they do not depend on daily
dosage.

### 11.4 Multi-ingredient and combination products

For combination products where each ingredient has a different recommended
daily dose, calculate daily cost only if a single combined dosing regimen is
specified on the label. If each ingredient is dosed independently, treat the
daily cost as missing unless a composite daily dose is explicitly stated.

---

## 12. Formulas and rounding rules

### 12.1 Summary of formulas

| Metric | Formula | Depends on |
|--------|---------|------------|
| Unit price | `price / package_quantity` | price, package_quantity |
| AI-normalized price | `unit_price / per_unit_dose` | unit_price, per_unit_dose |
| Daily cost | `(price / package_quantity) * daily_dose_units` | price, package_quantity, daily_dose_units |
| Effective quantity (with gift) | `paid_quantity + bonus_quantity` | paid_quantity, bonus_quantity |
| Multi-pack total units | `units_per_container * container_count` | both values known |

### 12.2 Rounding rules

| Quantity | Round to | Example |
|----------|----------|---------|
| Price (original currency) | 2 decimal places | `129.00` not `129` |
| Unit price (currency per unit) | 4 decimal places | `4.3000` CNY/tablet |
| AI-normalized price | 6 decimal places | `0.008600` USD/mg |
| Daily cost (currency per day) | 2 decimal places | `8.60` CNY/d |
| Exchange rate | 6 decimal places | `7.246500` |
| Package quantity | Integer (round down) | `30` tablets |
| Dosage units per day | 1 decimal place | `2.5` tablets/d |
| Percentage | 2 decimal places | `15.50%` |

### 12.3 Rounding method

Use **half-up rounding** (round half away from zero):

- `4.3250` rounds to `4.33`
- `4.3249` rounds to `4.32`
- `4.3350` rounds to `4.34`

### 12.4 Intermediate values

Preserve intermediate values at full precision before applying rounding. Round
only the final display value. For example, when calculating daily cost:

1. `unit_price = 129.00 / 30 = 4.300000...` (store at full precision).
2. `daily_cost = 4.300000... * 2 = 8.600000...` (store at full precision).
3. Display daily cost as `8.60` (round to 2 decimal places).

### 12.5 Formula recording

When a price observation includes calculated fields (`unit_price`,
`daily_cost`, `ai_normalized_price`), record the formula used in the
`formula` field for auditability:

```
"formula": "(129.00 / 30) * 2 = 8.60 CNY/d"
"formula": "129.00 / 30 = 4.30 per tablet"
```

### 12.6 Assumptions documentation

Every calculation that relies on an assumption (inferred daily dose, assumed
tax status, estimated shipping, regional default for tax) must list each
assumption in the `assumptions` array field:

```
"assumptions": [
  "assumed 2 capsules per day per label",
  "assumed price includes VAT per CN convention"
]
```

---

## 13. Price type hierarchy for comparison

### 13.1 Selection priority

When selecting a single representative price for comparison across products
(e.g., in a competitor matrix), use the following priority order:

1. **Sale price** (`sale_price`) - standard everyday price; most comparable
   across products.
2. **Coupon price** (`coupon_price`) - use when sale price is unavailable;
   note the coupon condition.
3. **Member price** (`member_price`) - use only when all products being
   compared have equivalent membership conditions.
4. **List price** (`list_price`) - use only when no promotional price is
   available; note that it may overstate actual transaction price.
5. **Subscription price** (`subscription_price`) - use only in
   subscription-specific comparisons; note the commitment period.
6. **Bundle price** (`bundle_price`) - use only for bundle-to-bundle
   comparisons; do not mix with single-unit prices.

### 13.2 Live price exclusion

Live-stream prices (`live_price`) are excluded from the standard price
comparison hierarchy. If a live price must be referenced, report it separately
and clearly label it as a live-stream promotion.

### 13.3 Cross-platform comparison

When comparing prices across platforms, use the same price type for all
products. For example, compare all `sale_price` values rather than mixing
`sale_price` for product A with `member_price` for product B. If the same
price type is not available for all products, note the discrepancy in the
report.

### 13.4 Price type in competitor matrix

In the competitor matrix, the `price_type` field must indicate which price
type was used for each entry. When the selected price type differs between
entries due to data availability, add a note explaining the difference.
