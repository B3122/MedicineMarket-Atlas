# Quantitative Reporting Rules

Rules for documenting, rounding, and presenting reviewer-derived quantitative
values in pharmaceutical and health-product market research reports.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: pricing-normalization.md (formula derivations, rounding
method, price type hierarchy), output-record-specification.md (field definitions
for calculated values), SKILL.md (quantitative reporting section lines 193-216).

---

## Table of Contents

1. [Formula documentation](#1-formula-documentation)
2. [Daily cost](#2-daily-cost)
3. [Price per unit](#3-price-per-unit)
4. [Dose normalization](#4-dose-normalization)
5. [Rounding rules](#5-rounding-rules)
6. [Price type distinctions](#6-price-type-distinctions)
7. [Unit normalization](#7-unit-normalization)
8. [Quantitative statements in reports](#8-quantitative-statements-in-reports)
9. [Forbidden operations](#9-forbidden-operations)

---

## 1. Formula documentation

### 1.1 Requirement

Every reviewer-derived numeric value in a report must be accompanied by its
formula. State the formula explicitly in the report text or in an adjacent
calculation note.

A formula statement must include:

- Formula expression
- Numerator and its source
- Denominator and its source
- Unit of the result
- Currency (if applicable)
- Collection date of input values
- Price type (if applicable)
- Assumptions applied
- Rounding rule used

### 1.2 Formula recording format

Use the following format in report calculation notes:

```
formula: (numerator) / (denominator) = result
numerator: <value> <unit> (source: <source ID>, date: <YYYY-MM-DD>)
denominator: <value> <unit> (source: <source ID>)
result: <value> <unit>
rounding: <rule>
assumptions: <list>
```

### 1.3 Traceability

Every calculated value must be independently traceable to its source inputs
without reconstructing the research session. An auditor must be able to
reproduce the calculation using only the formula statement and the source
inventory.

---

## 2. Daily cost

### 2.1 Formula

```
daily_cost = price / package_quantity * daily_dose_units
```

Where:

- `price` = total observed price of the package (in the observation currency)
- `package_quantity` = total number of dosage units in the package
- `daily_dose_units` = number of dosage units consumed per day

### 2.2 Alternate expression

```
daily_cost = unit_price * daily_dose_units
```

Where `unit_price = price / package_quantity`.

### 2.3 Step-by-step derivation

For a product with price `P`, package quantity `Q`, and daily dose `D`:

1. **Unit price**: `U = P / Q` (cost per single dosage unit)
2. **Daily cost**: `C = U * D` (cost per day at the labeled dose)

### 2.4 Required inputs

Both `price` and `package_quantity` must be known from the source observation.
The `daily_dose_units` value must come from one of the accepted daily dose
sources defined in pricing-normalization.md section 6.5.

### 2.5 Dose source attribution

In the report, state the source of the daily dose explicitly:

- "per product label" for label-derived doses
- "per official website" for website-derived doses
- "per [guideline name]" for clinical guideline doses
- "per regulatory filing [ID]" for regulatory doses
- "assumed [value] based on [rationale]" for assumed doses

### 2.6 Dose range handling

When a product label specifies a dosage range (e.g., "1 to 2 tablets per day"):

- Report both a low-end daily cost and a high-end daily cost
- Label as `daily_cost_range_low` and `daily_cost_range_high`
- Do not report the midpoint as a single daily cost unless separately labeled
  as an approximation with documented assumptions

### 2.7 Non-daily dosing conversion

For products dosed on a non-daily schedule, normalize to daily cost:

| Dosing schedule | Daily multiplier |
|-----------------|------------------|
| Once weekly | dose / 7 |
| Every other day | dose / 2 |
| Every 8 hours | dose * 3 |
| Every 12 hours | dose * 2 |
| Twice daily | dose * 2 |
| Three times daily | dose * 3 |

Document the conversion factor in the assumptions.

### 2.8 Prohibition

**Never calculate daily cost when the daily dosage is unavailable from an
accepted source.** If no label, official, guideline, or regulatory daily dose
can be identified, report `daily_cost` as "cannot be calculated" with the
reason. Do not infer, guess, or assume a daily dosage from consumer reviews,
seller recommendations, or category norms.

---

## 3. Price per unit

### 3.1 Formula

```
unit_price = price / package_quantity
```

Where:

- `price` = total observed price of the package
- `package_quantity` = total number of dosage units in the package

### 3.2 Unit selection

The unit price unit depends on the dosage form:

| Dosage form | Unit price unit |
|-------------|-----------------|
| Tablet, capsule, softgel | per tablet / per capsule |
| Oral liquid | per mL |
| Topical cream, ointment | per g |
| Injectable | per mL or per vial |
| Powder, granule | per g or per sachet |
| Patch | per patch |
| Device | per piece |

### 3.3 Multi-pack handling

When a product is sold as a multi-pack, first calculate total units across all
containers:

```
total_units = units_per_container * container_count
unit_price = price / total_units
```

Document the multi-pack configuration in the report when it affects the unit
price interpretation.

### 3.4 When price per unit cannot be calculated

Price per unit cannot be calculated when:

- `package_quantity` is missing or unknown
- The dosage unit definition is ambiguous (e.g., "serving" without
  specification)

In these cases, report the price per unit as "cannot be calculated" with the
specific missing field identified.

---

## 4. Dose normalization

### 4.1 Definition

Dose normalization converts product quantities to a common base unit for
comparison. The primary function is `parse_quantity()` from `_common.py`,
which extracts numeric values and units from product quantity strings.

### 4.2 Normalization process

1. Extract the raw quantity string from the product listing (e.g., "500 mg",
   "10 mL").
2. Parse into numeric value and unit using `parse_quantity()`.
3. Convert to base unit:
   - Mass: convert to mg (milligrams)
   - Volume: convert to mL (milliliters)
   - Count: convert to count (integer)

### 4.3 Active ingredient normalized price

For comparing products with different per-unit doses:

```
ai_normalized_price = unit_price / per_unit_dose
```

Where `per_unit_dose` is the amount of active ingredient per dosage unit in
the base unit (mg, mL).

### 4.4 Common conversions

| From | To | Factor |
|------|----|--------|
| g | mg | * 1000 |
| µg, mcg | mg | / 1000 |
| L | mL | * 1000 |
| µg/mL | mg/mL | / 1000 |
| IU | varies | conversion factor must be sourced |

For IU (International Units), the conversion to mg is substance-specific.
Do not convert IU to mg without a verified conversion factor for the specific
substance. Document the factor and its source.

### 4.5 Normalization in reports

When reporting dose-normalized comparisons:

- State the original unit and the normalized unit
- State the conversion factor used
- Do not mix products normalized to different base units in the same comparison
- Label all normalized values with `[CALCULATION]` in the report

---

## 5. Rounding rules

### 5.1 Rounding table

| Quantity type | Round to | Example |
|---------------|----------|---------|
| Price (currency) | 2 decimal places | `129.00` not `129` |
| Unit price (currency per unit) | 4 decimal places | `4.3000` CNY/tablet |
| AI-normalized price (currency per mg) | 6 decimal places | `0.008600` USD/mg |
| Daily cost (currency per day) | 2 decimal places | `8.60` CNY/d |
| Exchange rate | 6 decimal places | `7.246500` |
| Package quantity | Integer (floor) | `30` tablets |
| Dosage units per day | 1 decimal place | `2.5` tablets/d |
| Percentage (prices, margins) | 2 decimal places | `15.50%` |
| Percentage (clinical outcomes) | 1 decimal place | `12.3%` |
| Risk ratio, odds ratio, hazard ratio | 2 decimal places | `1.45` |
| p-value | 3 decimal places (or "<0.001") | `p = 0.032` |
| Confidence interval bounds | same as point estimate | `1.45 (95% CI 1.12 to 1.89)` |

### 5.2 Rounding method

Use **half-up rounding** (round half away from zero):

- `4.3250` rounds to `4.33`
- `4.3249` rounds to `4.32`
- `4.3350` rounds to `4.34`

### 5.3 Significant figures for clinical values

For clinical measurements (laboratory values, biomarker concentrations,
physiological parameters), use significant figure conventions rather than fixed
decimal places:

- Match the measurement precision of the source
- Do not add precision not present in the original measurement
- For aggregate values (means, medians), use one additional significant figure
  beyond the individual measurement precision

### 5.4 Intermediate precision

Preserve intermediate values at full precision before applying rounding. Round
only the final displayed value. Chained rounding (applying intermediate rounding
at each step of a multi-step calculation) is prohibited.

Example for daily cost:

1. `unit_price = 129.00 / 30 = 4.300000...` (store at full precision)
2. `daily_cost = 4.300000... * 2 = 8.600000...` (store at full precision)
3. Display as `8.60 CNY/d` (round to 2 decimal places)

### 5.5 Rounding in tables

Within a single table, all values of the same type must use the same rounding
rule. Do not mix 2-decimal and 4-decimal unit prices in the same column. State
the rounding rule in the table caption or footnote.

---

## 6. Price type distinctions

### 6.1 Price type definitions

| Price type | Definition | Do not mix with |
|------------|------------|-----------------|
| `list_price` | Manufacturer's suggested or official shelf price | `sale_price`, `coupon_price` |
| `sale_price` | Standard everyday platform price after routine markdown | `list_price`, `member_price` |
| `coupon_price` | Price after platform or store coupon deduction | `sale_price` |
| `member_price` | Price available only to platform members or subscribers | `sale_price` |
| `live_price` | Time-limited live-stream price | Any retail price type |
| `subscription_price` | Recurring price under subscription commitment | `sale_price` |
| `bundle_price` | Combined offer of multiple products or units | Single-unit prices |

### 6.2 Same-type comparison rule

**Never compare or average prices of different types.** When building a
competitor price comparison, use the same price type for all entries. If a
uniform price type is not available across all products, select the most
comparable available type and note the discrepancies.

### 6.3 Live price exclusion

**Never include live-stream prices in any retail price comparison, average,
or trend calculation.** Live-stream prices are time-limited, platform-subsidized,
and not representative of standard market price. If live prices are referenced
in the report, present them in a separate, clearly labeled section.

### 6.4 Price type labeling in reports

Every price stated in a report must include its price type. Do not present a
price value without specifying what kind of price it is. Examples:

- "The sale price was CNY 129.00 (per product listing, 2026-06-15)."
- "The member price was CNY 119.00 (JD PLUS member, 2026-06-15)."

### 6.5 Price type in calculation formulas

When a price is used in a calculation, the formula documentation must include
the price type. The same price type must be used across all products in a
comparative calculation.

### 6.6 Prohibition

**Never average different price types to produce a single "representative"
price.** Each price type carries different assumptions about availability,
eligibility, and duration. Averaging across types obscures these distinctions
and produces a meaningless figure.

---

## 7. Unit normalization

### 7.1 Requirement

All quantity values used in price comparisons, dose comparisons, or daily cost
calculations must be normalized to a common base unit before calculation.

### 7.2 Base units

| Dimension | Base unit |
|-----------|-----------|
| Mass | mg (milligrams) |
| Volume | mL (milliliters) |
| Count | count (integer) |
| Concentration | mg/mL |

### 7.3 Normalization in reports

When reporting a value derived from normalized units:

1. State the original quantity and unit
2. State the normalized quantity and unit
3. State the conversion factor
4. Label the result with `[CALCULATION]`

### 7.4 Cross-product consistency

When comparing products, verify that all quantities are normalized to the same
base unit. Do not compare a price per 500 mg tablet with a price per 200 mg
capsule without normalizing both to a common unit (e.g., price per mg).

### 7.5 Volume-weight equivalences

Do not convert between volume and mass units without a verified density or
concentration value. For liquid products, use the labeled concentration
(e.g., mg/mL) rather than assuming a density of 1 g/mL.

### 7.6 Product labeling parsing

When a product label uses non-standard units (e.g., "one scoop", "one dropper",
"one serving"):

- Do not convert to a base unit without the manufacturer's quantitative
  specification
- Record the original unit in the report
- Note that normalization was not possible and why

---

## 8. Quantitative statements in reports

### 8.1 Labeling

All reviewer-derived numeric statements must be labeled with `[CALCULATION]`
in the report body to distinguish them from source-reported values.

### 8.2 Relative comparisons

When reporting relative differences:

- State the absolute values being compared
- State the formula: `((value_a - value_b) / value_b) * 100`
- State which value is the reference
- Use percentage points for differences of percentages (not relative percent
  change)

### 8.3 Directional language

When reporting numeric findings:

- "higher than" / "lower than" — for directionally clear comparisons
- "approximately" — when rounding or estimation is applied
- "ranged from X to Y" — for ranges, not single values
- "median" / "mean" — specify the measure of central tendency used

### 8.4 Missing data handling

When a calculated value cannot be produced:

- State "cannot be calculated" rather than omitting the field
- Provide the specific reason (e.g., "daily dose not available from any
  accepted source")
- Do not substitute a category average, similar-product value, or other proxy

---

## 9. Forbidden operations

### 9.1 Absolute prohibitions

The following operations are never permitted in a report:

- **Never calculate daily cost without confirmed dosage from an accepted
  source**
- **Never average different price types to produce a single figure**
- **Never include live-stream prices in retail price comparisons**
- **Never compare prices normalized to different base units**
- **Never chained-round intermediate calculation steps**
- **Never convert IU to mg without a substance-specific verified factor**
- **Never guess a price type from context**

### 9.2 Conditional prohibitions

The following operations require explicit documentation of assumptions and are
prohibited when assumptions cannot be documented:

- Converting between volume and mass without verified concentration data
- Using a dosage range midpoint as a single daily cost value
- Applying a non-standard rounding rule without justification
- Using a member price in a comparison that includes non-member prices

### 9.3 Reporting violations

If a quantitative value in the report was produced through a forbidden
operation, the audit must flag it as a critical finding. The correction
procedure is to recalculate using only permitted operations and accepted source
data. If recalculation is impossible, the value must be replaced with "cannot
be calculated" and the reason documented.
