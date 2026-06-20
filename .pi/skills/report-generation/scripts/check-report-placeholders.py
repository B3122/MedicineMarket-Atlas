#!/usr/bin/env python3
"""Scan a report markdown file for unreplaced placeholder patterns.

Usage
-----
    python check-report-placeholders.py <report.md> [--out findings.json]

Exit codes
----------
    0   No placeholders found.
    1   One or more placeholders found.
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
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Ensure the skill root is on sys.path so ``scripts._common`` is importable
# when this script is run as ``python scripts/check-report-placeholders.py``.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts._common import log_info, log_error  # noqa: E402


# ---------------------------------------------------------------------------
# Placeholder patterns
# ---------------------------------------------------------------------------

#: Patterns that indicate unreplaced placeholders in prose.
#: Each entry is (label, compiled regex).
_PLACEHOLDER_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("[TODO]", re.compile(r"\[TODO\]", re.IGNORECASE)),
    ("[TK]", re.compile(r"\[TK\]", re.IGNORECASE)),
    ("{{...}}", re.compile(r"\{\{[^}]*\}\}")),
    ("[...]", re.compile(r"\[\.\.\.\]")),
]


def _is_inside_code_block(line: str, in_code_block: bool) -> bool:
    """Update and return whether *line* starts or ends a fenced code block.

    Parameters
    ----------
    line : str
        The current line.
    in_code_block : bool
        Current code-block state before this line.

    Returns
    -------
    bool
        Updated code-block state after processing this line.
    """
    stripped = line.strip()
    if stripped.startswith("```"):
        # Toggle code block state on fenced code block markers.
        return not in_code_block
    return in_code_block


def _scan_report(text: str) -> List[Dict[str, object]]:
    """Scan *text* for placeholder patterns, skipping fenced code blocks.

    Parameters
    ----------
    text : str
        Full report markdown content.

    Returns
    -------
    list[dict]
        Each entry has ``line`` (int, 1-indexed), ``pattern`` (str label),
        and ``match`` (str) with surrounding context.
    """
    findings: List[Dict[str, object]] = []
    lines = text.splitlines()
    in_code_block = False

    for line_num_0, raw_line in enumerate(lines):
        line_num = line_num_0 + 1
        in_code_block = _is_inside_code_block(raw_line, in_code_block)
        if in_code_block:
            continue
        for label, pattern in _PLACEHOLDER_PATTERNS:
            for match in pattern.finditer(raw_line):
                start = max(0, match.start() - 20)
                end = min(len(raw_line), match.end() + 20)
                context = raw_line[start:end].strip()
                findings.append(
                    {
                        "line": line_num,
                        "pattern": label,
                        "match": match.group(),
                        "context": context,
                    }
                )
    return findings


def _check_placeholders(path: Path, out_path: Optional[Path] = None) -> int:
    """Read the report, scan for placeholders, and report results.

    Parameters
    ----------
    path : Path
        Path to the report ``.md`` file.
    out_path : Path or None
        Optional path for a JSON findings report.

    Returns
    -------
    int
        Exit code: 0 (none found), 1 (placeholders found), 2 (bad file/args),
        or 3 (read error).
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

    # ---- Scan for placeholders ----------------------------------------------
    findings = _scan_report(text)

    # ---- Report results -----------------------------------------------------
    if findings:
        log_error(f"FAIL: {len(findings)} placeholder(s) found")
        for f in findings:
            log_error(
                f"  Line {f['line']}, pattern '{f['pattern']}': "
                f"\"{f['match']}\" in \"{f['context']}\""
            )
        if out_path:
            try:
                with open(out_path, "w", encoding="utf-8") as fh:
                    json.dump(
                        {
                            "input": str(path),
                            "passed": False,
                            "placeholder_count": len(findings),
                            "placeholders": findings,
                        },
                        fh,
                        indent=2,
                        ensure_ascii=False,
                    )
            except OSError:
                log_error(f"Failed to write report to {out_path}")
                return 3
        return 1

    log_info("PASS: no placeholders found")
    if out_path:
        try:
            with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(
                    {
                        "input": str(path),
                        "passed": True,
                        "placeholder_count": 0,
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
    """Parse arguments and run placeholder check."""
    parser = argparse.ArgumentParser(
        description="Scan report markdown for unreplaced placeholders",
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

    log_info(f"Scanning: {input_path}")
    exit_code = _check_placeholders(input_path, out_path)
    log_info(
        f"Done scanning {input_path}"
        + (f" | Report: {args.out}" if args.out else "")
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
