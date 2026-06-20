---
name: product-market-research
description: Researches pharmaceutical and health-product markets, product listings, competitors, pricing, positioning, claims, and platform differences.
---

# Workflow

1. Confirm market, time point, product category, and target use.
2. Identify the exact product version.
3. Record one page snapshot as one source record.
4. Preserve platform, seller, URL, and retrieval date.
5. Extract fields without filling missing values from assumptions.
6. Separate page claims from verified facts.
7. Flag conflicts for product normalization.
8. Save structured results to the assigned artifact path.

# Platform priorities

## Official website
Prioritize ingredients, dose, manufacturer, intended use, official claims,
warnings, product version, and official identifiers.

## Ecommerce platform
Prioritize current price, promotion type, package size, seller type,
sales proxy, review count, claims, bundles, and shipping region.

## Social platform
Prioritize usage scenarios, recurring pain points, message framing,
content engagement, commercial sponsorship, and consumer narratives.

# Prohibitions

- Do not use comments as proof of efficacy.
- Do not infer exact sales from popularity or review count.
- Do not combine live-stream price with ordinary retail price.
- Do not collapse regional versions into one product.

## References — Supporting Reference Files

| File | Description |
|---|---|
| `references/output-record-specification.md` | Canonical field definitions for all output record types |
| `references/source-hierarchy.md` | Preferred source types per research question and evidence tiering |
| `references/platform-field-matrix.md` | Available data fields mapped per platform type |
| `references/product-identity-rules.md` | Rules for identifying and disambiguating product versions |
| `references/pricing-normalization.md` | Methods for normalising price data across sources |
| `references/competitor-selection.md` | Criteria for selecting comparable competitor products |
| `references/claim-taxonomy.md` | Classification system for commercial and scientific claims |
| `references/consumer-content-rules.md` | Guidelines for handling consumer-generated content in research |
| `references/regulatory-source-map.md` | Regulatory authorities and official data sources by region |
| `references/data-quality-scoring.md` | Scoring methodology for assessing data quality and reliability |

## Scripts — Helper Scripts

| Script | Description |
|---|---|
| `scripts/_common.py` | Shared utilities for JSONL I/O, unit parsing, currency formatting, and CLI logging |
| `scripts/validate-listings.py` | Validates listing records against `listing.schema.json` and business rules |
| `scripts/validate-source-inventory.py` | Validates source inventory records for completeness and consistency |
| `scripts/normalize-units.py` | Normalises quantity and unit fields to standard representations |
| `scripts/normalize-prices.py` | Normalises price fields to standard currency and unit-price formats |
| `scripts/calculate-daily-cost.py` | Calculates daily treatment cost from price and dosage data |
| `scripts/detect-duplicate-products.py` | Detects potential duplicate product records using identity matching rules |
| `scripts/merge-platform-records.py` | Merges platform-specific records into unified product records |
| `scripts/build-competitor-matrix.py` | Builds a competitor comparison matrix from validated product records |

## Assets and Schemas

- **Example files** — `assets/listing-record.example.json`, `assets/product-record.example.json`, `assets/competitor-matrix.example.csv`, `assets/source-inventory.example.csv`
- **QA fixtures** — JSONL test cases under `assets/` covering valid, invalid, corrupted, duplicate, missing-field, and edge-case scenarios for every validator and normaliser
- **JSON Schemas** — `schemas/source.schema.json`, `schemas/product.schema.json`, `schemas/listing.schema.json`, `schemas/price-observation.schema.json`, `schemas/competitor-matrix.schema.json`, `schemas/_defs.json`
