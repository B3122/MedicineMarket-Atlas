# Search Log Template

Template and field specification for the evidence-appraisal search log.
Every evidence search conducted during an appraisal must produce one entry
in this log.

**Version**: 1.0.0
**Last updated**: 2026-06-20
**Cross-references**: SKILL.md (Step 4 search log requirements, lines 135-144),
output-record-specification.md (product-market-research skill, source record
fields), source-hierarchy.md (source priority tiers).

---

## Table of Contents

1. [Field specification](#1-field-specification)
2. [Example entry](#2-example-entry)
3. [Instructions for maintaining the log](#3-instructions-for-maintaining-the-log)
4. [Query change recording convention](#4-query-change-recording-convention)
5. [Access limitation categories](#5-access-limitation-categories)

---

## 1. Field specification

Every search log entry contains the following fields. Required fields must
be populated for every entry. Optional fields are populated when the
information is available.

| Field | Type | Required | Description |
|---|---|---|---|
| `source` | string | Yes | The database, platform, index, or website searched. Use the full name (e.g., "PubMed", "Cochrane Library", "ClinicalTrials.gov", "EMA website"). Do not abbreviate on first use. |
| `query` | string | Yes | The exact search query as executed. Include Boolean operators, field tags, MeSH terms, truncation, and phrase quoting. Copy verbatim; do not prettify or summarize. |
| `date` | string (ISO 8601) | Yes | The date the search was executed, in `YYYY-MM-DD` format. Use the date the query was run, not the date the log entry was written. |
| `filters` | string or array | Yes | All active filters applied to the search. Include date ranges, language limits, study type filters, publication status filters, and any other restrictions. Format as a comma-separated list or structured array. |
| `result_count` | integer | No | The number of results returned by the search at the time of execution. Record when the platform reports a count. Omit or set to `null` when the count is not available. |
| `query_changes` | string | No | Any changes made to the query during the search session. Record the original query, the reason for the change, and the revised query. Leave empty for searches executed in a single attempt. |
| `access_limitations` | string or array | No | Known limitations on access to the search results. Include paywalls, institutional access requirements, regional blocks, language barriers, or API restrictions. Leave empty when full access was available. |

### 1.1 Field conventions

- The `source` field uses the official name of the database or platform. When
  the source is part of a larger platform, specify both (e.g., "Europe PMC
  (PubMed Central mirror)").
- The `query` field preserves exact syntax. If the query contains
  line breaks or special characters, preserve them. Use a code block for
  multi-line queries.
- The `date` field uses the date of execution, not the date of log entry.
  If a search is re-run, create a new entry with the new date.
- The `filters` field includes both explicit filters selected in the
  interface and implicit limits built into the query syntax.
- The `result_count` field records the count returned by the platform. If
  the platform does not report a count (e.g., some regulatory websites),
  note "not reported" in the field description rather than inventing a
  number.

---

## 2. Example entry

The following entry uses placeholder data to illustrate the format. It
does not reference real studies, real products, or real bibliographic data.

### 2.1 Markdown log format

```
### Search 001

- **Source**: PubMed
- **Query**: (("Dietary Supplements"[Mesh]) AND ("Blood Glucose"[Mesh])) AND
  ("randomized controlled trial"[Publication Type]) AND
  ("2015/01/01"[Date - Publication] : "2025/12/31"[Date - Publication])
- **Date**: 2026-06-15
- **Filters**: English language, Humans, Randomized Controlled Trial,
  Publication date 2015-2025
- **Result count**: 127
- **Query changes**: Initial query without publication type filter returned
  843 results (too many to screen). Added "randomized controlled trial"
  filter to narrow to controlled evidence.
- **Access limitations**: None. Full access via institutional subscription.
  Two of 127 results were available as abstracts only (no full text in PMC).
```

### 2.2 JSON log format

```json
{
  "search_id": "search-001",
  "source": "PubMed",
  "query": "((\"Dietary Supplements\"[Mesh]) AND (\"Blood Glucose\"[Mesh])) AND (\"randomized controlled trial\"[Publication Type]) AND (\"2015/01/01\"[Date - Publication] : \"2025/12/31\"[Date - Publication])",
  "date": "2026-06-15",
  "filters": [
    "English language",
    "Humans",
    "Randomized Controlled Trial",
    "Publication date 2015-2025"
  ],
  "result_count": 127,
  "query_changes": "Initial query without publication type filter returned 843 results. Added \"randomized controlled trial\" filter to narrow to controlled evidence.",
  "access_limitations": [
    "Two results available as abstracts only (no full text in PMC)"
  ]
}
```

### 2.3 Note on the example

The MeSH terms, date ranges, and result counts in this example are
placeholder values. They do not correspond to any actual search. Replace
with real data when populating the log.

---

## 3. Instructions for maintaining the log

### 3.1 When to create an entry

Create a new search log entry for every distinct search executed during an
evidence appraisal. A search is distinct when any of the following differ
from a previous search:

- The source platform or database.
- The query string.
- The filters applied.
- The date of execution (for searches re-run on different dates).

### 3.2 One entry per search session

If you run the same query multiple times in one session to verify results,
record it once. If you modify the query mid-session, record the original
query, the reason for modification, and the final query in the
`query_changes` field of a single entry.

### 3.3 Entry numbering

Number entries sequentially within each appraisal project:

- `search-001`, `search-002`, `search-003`, etc.

Use the same numbering in the evidence artifact to cross-reference searches
with their results.

### 3.4 Record before screening

Create or complete the search log entry before beginning title and abstract
screening. The result count must reflect what the platform reported at the
time of the search, not what remained after screening.

### 3.5 Multi-database searches

When the same or similar query is run across multiple databases, create a
separate entry for each database. Do not combine results from different
sources into one entry.

### 3.6 Regulatory and grey literature searches

For searches of regulatory websites, guideline repositories, and other
sources that do not provide structured search interfaces:

- Record the URL or navigation path in the `source` field.
- Record the search terms or browse path in the `query` field.
- Record all filters (document type, date, status) even if applied through
  navigation rather than a query interface.
- Set `result_count` to `null` and note that the platform does not report
  a count.

### 3.7 Update, do not overwrite

When a search is re-run on a later date, create a new entry with a new
`search_id` and `date`. Do not overwrite the previous entry. This preserves
the audit trail of when each search was performed.

---

## 4. Query change recording convention

### 4.1 What to record

When a query is modified during a search session, record in the
`query_changes` field:

1. The original query or the change that prompted modification.
2. The reason for the change (e.g., "too many results", "too few results",
   "irrelevant results", "missed key term").
3. The revised query or the specific modification made.

### 4.2 Format

Use plain language. Examples:

- "Initial query returned 2,300 results. Added date filter (2015-2025) to
  limit to recent evidence. Revised query reduced results to 430."
- "Initial query missed the brand name variant. Added 'OR BrandName' to the
  intervention concept block."
- "Removed 'NOT animal' filter because it excluded relevant human studies
  that mentioned animal models in the background section."

### 4.3 When the query does not change

If the query is executed exactly as planned and returns an acceptable result
set, leave `query_changes` empty. Do not write "none" or "no changes".

---

## 5. Access limitation categories

Use the following categories to describe access limitations consistently:

| Category | Description | Example |
|---|---|---|
| Paywall | Full text behind a publisher paywall. Abstract accessible. | "Full text requires subscription to [Journal Name]." |
| Institutional access | Access requires institutional affiliation or library subscription. | "Accessible only through institutional login." |
| Regional block | Source blocked or restricted in certain jurisdictions. | "Access restricted to [Country] IP addresses." |
| Language barrier | Full text in a language the reviewer cannot read. | "Full text available in [Language] only. English abstract reviewed." |
| API restriction | Programmatic access limited by rate, quota, or authentication. | "API limited to 100 requests per day without authentication." |
| Missing full text | No full text available through any accessible channel. | "Abstract only. Full text not located through institutional access, interlibrary loan, or author contact." |
| Registration required | Free access but requires account registration. | "Requires free account registration to view results." |

Record all that apply. If no limitations exist, leave `access_limitations`
empty. **Do not write "none" or "no limitations"** — an empty field means no
known limitations.

---

## Rules summary

1. Create one entry per distinct search per database.
2. Record the exact query as executed. **Do not edit, correct, or prettify
   the query string after the fact.**
3. Record the date of search execution, not the date of log entry.
4. Record the result count as reported by the platform. **Do not estimate or
   approximate the count.**
5. Create a new entry when a search is re-run on a different date. **Do not
   overwrite previous entries.**
6. Complete the log entry before beginning screening.
7. Leave optional fields empty when information is not available. **Do not
   write "none", "N/A", or "no limitations" in optional fields.**
