# product-market-research Skill — Maintainer Reference

**Purpose**: Domain knowledge pack for pharmaceutical and health-product market research. Provides SOPs, reference documents, data-processing scripts, JSON schemas, and QA fixtures.

## STRUCTURE

```
product-market-research/
├── SKILL.md                  # Skill entry point (71 lines)
├── AGENTS.md                 # This file — maintainer reference
├── references/               # 10 domain reference documents
│   ├── output-record-specification.md  # Canonical field definitions
│   ├── source-hierarchy.md             # Source type priority tiers
│   ├── platform-field-matrix.md        # Data fields per platform type
│   ├── product-identity-rules.md       # Product/SKU/version resolution
│   ├── pricing-normalization.md        # Price normalization methodology
│   ├── competitor-selection.md         # Competitor inclusion criteria
│   ├── claim-taxonomy.md               # Commercial/scientific claim classification
│   ├── consumer-content-rules.md       # Consumer-generated content handling
│   ├── regulatory-source-map.md        # Regulatory authorities by region
│   └── data-quality-scoring.md         # Data quality assessment methodology
├── scripts/                  # 8 Python CLI data-processing tools + 1 shared library
│   ├── _common.py            # Shared lib: JSONL I/O, unit parsing, currency formatting
│   ├── validate-listings.py            # Schema validation for listing records
│   ├── validate-source-inventory.py    # Source inventory validation + cross-ref checks
│   ├── normalize-units.py              # Unit normalization to base (mg/mL)
│   ├── normalize-prices.py             # Price normalization + currency validation
│   ├── calculate-daily-cost.py         # Daily cost from price + dose data
│   ├── detect-duplicate-products.py    # Rule-based duplicate product detection
│   ├── merge-platform-records.py       # Cross-platform record merging
│   └── build-competitor-matrix.py      # Competitor comparison export (CSV/XLSX)
├── schemas/                  # 6 JSON Schema Draft-07 files
│   ├── _defs.json            # Shared definitions: IDs, enums, units, types
│   ├── source.schema.json              # Source record structure (9 source types)
│   ├── product.schema.json             # Product record (15 required fields)
│   ├── listing.schema.json             # Listing record (26+ fields)
│   ├── price-observation.schema.json   # Price observation with normalization
│   └── competitor-matrix.schema.json   # Competitor metric export format
└── assets/                   # QA fixtures + reference examples
    ├── *.valid.jsonl         # Happy path test fixtures
    ├── *.invalid.jsonl       # Schema violation fixtures
    ├── *.corrupted.jsonl     # Malformed JSONL fixtures (parse error testing)
    ├── *.example.json/csv    # Reference example files
    └── pipeline/             # Integration test data
```

## WHERE TO LOOK

| Task | Location | Key Info |
|------|----------|----------|
| Understand skill workflow | `SKILL.md` | 8-step workflow, platform priorities, prohibitions |
| Find field definitions | `references/output-record-specification.md` | All record field specs |
| Understand source tiers | `references/source-hierarchy.md` | Evidence quality hierarchy |
| Map platform data fields | `references/platform-field-matrix.md` | Fields per official/ecom/social |
| Resolve product identity | `references/product-identity-rules.md` | SKU/version/regional rules |
| Normalize prices correctly | `references/pricing-normalization.md` | Forbidden calc rules |
| Classify commercial claims | `references/claim-taxonomy.md` | Claim type + evidence level matrix |
| Handle consumer content | `references/consumer-content-rules.md` | Privacy rules, theme analysis |
| Score data quality | `references/data-quality-scoring.md` | 8-dimension scoring, no collapse |
| Select competitors | `references/competitor-selection.md` | Inclusion/exclusion criteria |
| Find regulatory sources | `references/regulatory-source-map.md` | Authorities by jurisdiction |
| Find shared ID definitions | `schemas/_defs.json` | All shared types and enums |
| Validate listing data | Run `scripts/validate-listings.py input.jsonl` | Exit 0=pass, 1=errors |
| Validate source inventory | Run `scripts/validate-source-inventory.py sources.jsonl` | Cross-ref checking |
| Normalize units to base | Run `scripts/normalize-units.py input.jsonl --out output.jsonl` | mg, mL, count |
| Detect duplicates | Run `scripts/detect-duplicate-products.py input.jsonl --out dups.json` | Never auto-merges |
| Build competitor matrix | Run `scripts/build-competitor-matrix.py input.jsonl --out out.csv` | CSV or XLSX |
| Find test fixtures | `assets/*.jsonl` | Valid/invalid/corrupted/edge-case |

## CONVENTIONS

**All scripts**: Read-only on inputs. Exit codes: 0/1/2/3. JSONL in/out. Log to stderr via `_common.log_info()`/`log_error()`. Insert project root into `sys.path`.

**All schemas**: JSON Schema Draft-07 with `$ref` to `_defs.json`. IDs: `{type}-{platform}-{YYYYMMDD}-{seq}`. Never `null` — use `"unknown"` or `"not_applicable"`.

**All references**: Markdown with tables. Business rules use imperative mood. Critical prohibitions in **bold**.

**QA fixtures**: Named `{record-type}.{scenario}.jsonl`. Scenarios: valid, invalid, corrupted, duplicate, missing-field, edge-case-descriptive.

## ANTI-PATTERNS (skill-specific)

- **Never modify input files** — all 9 scripts are read-only on inputs
- **Never auto-merge duplicates** — `detect-duplicate-products.py` outputs candidates for human review only
- **Never infer daily dosage** — `calculate-daily-cost.py` returns exit code 1 for missing dose
- **Never collapse regional versions** — keep separate `product_version` records, link via `product_master_id`
- **Never guess currency** — use `"unknown"` when unconfirmed; never assume from platform
- **Never combine live-stream prices with retail** — separate price types, never average
- **Never merge based on similar names** — always check identifiers, manufacturer, formulation, dose

## DEPENDENCIES

- **Python stdlib**: `json`, `csv`, `sys`, `argparse`, `re`, `os`, `datetime`
- **jsonschema**: Schema validation in validate-*.py and build-competitor-matrix.py (`pip install jsonschema`)
- **openpyxl**: XLSX export in build-competitor-matrix.py, optional (`pip install openpyxl`)
