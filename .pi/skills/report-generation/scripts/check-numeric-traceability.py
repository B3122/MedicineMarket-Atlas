#!/usr/bin/env python3
"""Trace numbers in a report back to source attributions.

Usage
-----
    python check-numeric-traceability.py <report.md> [--out findings.json]

Exit codes
----------
    0   All extracted numbers are traceable to a source.
    1   One or more numbers flagged as untraceable.
    2   File not found or missing arguments.
    3   Read error (e.g. encoding issue).

The input file is never modified.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Ensure the skill root is on sys.path so ``scripts._common`` is importable
# when this script is run as ``python scripts/check-numeric-traceability.py``.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import log_info, log_error  # noqa: E402


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

#: Numbers that are likely report data (not dates, years alone, or section nums).
#: Matches integers and decimals, optionally with comma separators, %
#: Sign, and scientific notation.  Captures the number for extraction.
_NUMBER_RE = re.compile(
    r"(?<![a-zA-Z0-9])"  # not preceded by alphanumeric
    r"([+-]?"             # optional sign
    r"(?:\d{1,3}(?:,\d{3})+"  # comma-separated thousands, or
    r"|\d+)"                    # plain digits
    r"(?:\.\d+)?"               # optional decimal
    r"(?:[eE][+-]?\d+)?"        # optional exponent
    r")\s*%?"                    # optional trailing percent
    r"(?![a-zA-Z0-9])",         # not followed by alphanumeric
)

#: Fenced code block marker.
_CODE_FENCE_RE = re.compile(r"^\s*```")

#: Markdown table row (contains | pipe separators).
_TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")

#: Table separator row (like ``|---|---|``).
_TABLE_SEP_RE = re.compile(r"^\s*\|[\s\-:]+\|")

#: Source ID pattern (e.g. ``jd-20250620-001``).
_SOURCE_ID_RE = re.compile(r"\b[a-z][a-z0-9]*-\d{8}-\d{3}\b")

#: Citation reference pattern like ``[1]``, ``[2,3]``, ``[4-6]``.
_CITATION_REF_RE = re.compile(r"\[(?:\d+(?:[,\-]\d+)*)\]")

#: Parenthetical citation like ``(Smith et al., 2023)``.
_PAREN_CITE_RE = re.compile(r"\([^)]*\d{4}[^)]*\)")

#: Attribution phrases that introduce sourced information.
_ATTRIBUTION_PHRASES: List[str] = [
    "according to",
    "per the",
    "reported by",
    "as noted in",
    "as cited in",
    "as stated in",
    "as shown in",
    "as described in",
    "data from",
    "based on",
    "sourced from",
    "referenced in",
    "as documented in",
    "the source indicates",
    "the study found",
    "the trial reported",
    "the label states",
    "the manufacturer lists",
    "the seller displays",
    "the platform shows",
    "the authority classifies",
    "the guideline recommends",
    "the database records",
    "the inventory shows",
]

#: Compiled attribution phrase pattern (case-insensitive).
_ATTRIBUTION_PATTERN = re.compile(
    r"\b(?:" + "|".join(re.escape(phrase) for phrase in _ATTRIBUTION_PHRASES) + r")\b",
    re.IGNORECASE,
)


def _is_source_attribution_marker(text: str) -> bool:
    """Check whether *text* contains any source attribution marker.

    Detects source ID citations, numbered references, parenthetical
    citations, and attribution phrases.

    Parameters
    ----------
    text : str
        A sentence or span of text to check.

    Returns
    -------
    bool
        ``True`` if the text contains at least one attribution marker.
    """
    if _SOURCE_ID_RE.search(text):
        return True
    if _CITATION_REF_RE.search(text):
        return True
    if _PAREN_CITE_RE.search(text):
        return True
    if _ATTRIBUTION_PATTERN.search(text):
        return True
    return False


def _split_sentences(text: str) -> List[str]:
    """Split *text* into sentences using period, exclamation, and question marks.

    Handles common abbreviations like ``e.g.``, ``i.e.``, ``etc.``, ``vs.``
    to avoid splitting mid-abbreviation.

    Parameters
    ----------
    text : str
        Input paragraph or multi-sentence text.

    Returns
    -------
    list[str]
        List of sentence strings (stripped).
    """
    # Split on sentence-ending punctuation followed by whitespace.
    raw = re.split(r"(?<=[.!?])\s+", text)
    # Rejoin fragments split on abbreviations.
    merged: List[str] = []
    abbrev = re.compile(
        r"\b(?:e\.g|i\.e|etc|vs|dr|mr|mrs|ms|prof|dept|approx|fig|eq|vol|p|pp"
        r"|et\s+al|ca|approx|esp|incl|no|nos|ref|refs|ed|eds|viz|al)$"
    )
    for sentence in raw:
        stripped = sentence.strip()
        if not stripped:
            continue
        if merged and abbrev.search(merged[-1]):
            merged[-1] += " " + stripped
        else:
            merged.append(stripped)
    return merged


def _process_report(text: str) -> Tuple[List[Dict[str, object]], int]:
    """Extract and assess traceability of numbers in report text.

    Parameters
    ----------
    text : str
        Full report markdown content.

    Returns
    -------
    tuple[list[dict], int]
        ``(findings, total_numbers_extracted)``.  Findings are entries with
        ``line``, ``number``, ``sentence``, and ``traceable`` (bool).
    """
    findings: List[Dict[str, object]] = []
    total_numbers = 0
    in_code_block = False

    lines = text.splitlines()

    # ---- First pass: mark which lines are in code blocks or tables ----------
    skip_line: Set[int] = set()
    for i, line in enumerate(lines):
        if _CODE_FENCE_RE.match(line):
            in_code_block = not in_code_block
            skip_line.add(i)
            continue
        if in_code_block:
            skip_line.add(i)
            continue
        if _TABLE_ROW_RE.match(line) or _TABLE_SEP_RE.match(line):
            skip_line.add(i)

    # ---- Second pass: extract numbers and assess traceability ----------------
    sentence_buffer: List[Tuple[int, str]] = []  # (line_num, text)
    sentences: List[Tuple[int, str]] = []  # (line_num, sentence_text)

    # Collect non-skipped lines into a paragraph buffer, then split.
    for i, line in enumerate(lines):
        if i in skip_line:
            # Flush buffer on context break.
            if sentence_buffer:
                para_text = " ".join(t for _, t in sentence_buffer)
                sents = _split_sentences(para_text)
                # Approximate line for each sentence: use first line of buffer.
                first_line = sentence_buffer[0][0]
                for s in sents:
                    sentences.append((first_line, s))
                sentence_buffer = []
            continue

        stripped = line.strip()
        if not stripped:
            # Empty line: flush buffer.
            if sentence_buffer:
                para_text = " ".join(t for _, t in sentence_buffer)
                sents = _split_sentences(para_text)
                first_line = sentence_buffer[0][0]
                for s in sents:
                    sentences.append((first_line, s))
                sentence_buffer = []
            continue

        sentence_buffer.append((i + 1, stripped))

    # Flush remaining buffer.
    if sentence_buffer:
        para_text = " ".join(t for _, t in sentence_buffer)
        sents = _split_sentences(para_text)
        first_line = sentence_buffer[0][0]
        for s in sents:
            sentences.append((first_line, s))

    # ---- Assess traceability per number -------------------------------------
    total_sentences = len(sentences)

    for idx, (sline, sentence) in enumerate(sentences):
        # Extract all numbers in this sentence.
        numbers_found = [
            m.group(0).replace(",", "")  # remove comma separators for display
            for m in _NUMBER_RE.finditer(sentence)
        ]
        if not numbers_found:
            continue

        # Build the surrounding context window: prev, current, next sentences.
        context_parts = [sentence]
        if idx > 0:
            context_parts.insert(0, sentences[idx - 1][1])
        if idx < total_sentences - 1:
            context_parts.append(sentences[idx + 1][1])

        context_text = " ".join(context_parts)

        # Determine if this context has source attribution.
        traceable = _is_source_attribution_marker(context_text)

        for num in numbers_found:
            total_numbers += 1
            if not traceable:
                findings.append(
                    {
                        "line": sline,
                        "number": num,
                        "sentence": sentence,
                        "traceable": False,
                    }
                )

    return findings, total_numbers


def _check_numeric_traceability(
    path: Path,
    out_path: Optional[Path] = None,
) -> int:
    """Read the report, extract numbers, assess traceability, report results.

    Parameters
    ----------
    path : Path
        Path to the report ``.md`` file.
    out_path : Path or None
        Optional path for a JSON findings report.

    Returns
    -------
    int
        Exit code: 0 (all traceable), 1 (untraceable numbers found),
        2 (bad file/args), or 3 (read error).
    """
    # ---- Read report --------------------------------------------------------
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        log_error(f"File not found: {path}")
        return 2
    except (OSError, UnicodeDecodeError) as exc:
        log_error(f"Failed to read {path}: {exc}")
        return 3

    # ---- Extract and assess -------------------------------------------------
    findings, total_numbers = _process_report(text)
    untraceable = [f for f in findings if not f["traceable"]]
    untraceable_count = len(untraceable)

    # ---- Report results -----------------------------------------------------
    if untraceable:
        log_error(
            f"FAIL: {untraceable_count} of {total_numbers} numeric value(s) "
            f"lack source attribution within 2-sentence window"
        )
        for f in untraceable[:20]:  # Limit stderr output.
            log_error(
                f"  Line {f['line']}, number '{f['number']}': "
                f"\"{f['sentence'][:80]}...\""
            )
        if len(untraceable) > 20:
            log_error(f"  ... and {len(untraceable) - 20} more")

        if out_path:
            try:
                with open(out_path, "w", encoding="utf-8") as fh:
                    json.dump(
                        {
                            "input": str(path),
                            "passed": False,
                            "total_numbers": total_numbers,
                            "untraceable_count": untraceable_count,
                            "traceable_count": total_numbers - untraceable_count,
                            "findings": untraceable,
                        },
                        fh,
                        indent=2,
                        ensure_ascii=False,
                    )
            except OSError:
                log_error(f"Failed to write report to {out_path}")
                return 3
        return 1

    log_info(
        f"PASS: all {total_numbers} numeric value(s) traceable to source attribution"
    )
    if out_path:
        try:
            with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(
                    {
                        "input": str(path),
                        "passed": True,
                        "total_numbers": total_numbers,
                        "untraceable_count": 0,
                        "findings": [],
                    },
                    fh,
                    indent=2,
                    ensure_ascii=False,
                )
        except OSError:
            log_error(f"Failed to write report to {out_path}")
            return 3
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments and run numeric traceability check."""
    parser = argparse.ArgumentParser(
        description="Trace report numbers back to source attributions",
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to the report .md file",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Optional path to write a JSON findings report",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out) if args.out else None

    log_info(f"Tracing numbers in: {input_path}")
    exit_code = _check_numeric_traceability(input_path, out_path)
    log_info(
        f"Done tracing {input_path}"
        + (f" | Report: {args.out}" if args.out else "")
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
