"""
Shared utility module for report-generation scripts.

Stdlib-only helpers for JSONL I/O and uniform CLI logging.

Target: Python 3.9+
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Union


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

_LOG = logging.getLogger("report-generation")


def _setup_logging() -> None:
    """Configure stderr logging once."""
    if _LOG.handlers:
        return
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    _LOG.addHandler(handler)
    _LOG.setLevel(logging.INFO)


def log_info(msg: str) -> None:
    """Print an info-level message to stderr with uniform formatting."""
    _setup_logging()
    _LOG.info(msg)


def log_error(msg: str) -> None:
    """Print an error-level message to stderr with uniform formatting."""
    _setup_logging()
    _LOG.error(msg)


# ---------------------------------------------------------------------------
# JSONL I/O
# ---------------------------------------------------------------------------


def read_jsonl(path: Union[str, Path]) -> List[Dict]:
    """Read a UTF-8 line-delimited JSON file.

    Empty lines are silently skipped.  Each non-empty line must contain
    exactly one JSON object (a dict).  Raises ``FileNotFoundError`` when
    *path* does not exist and ``json.JSONDecodeError`` on malformed lines.

    Parameters
    ----------
    path : str or Path
        Path to the ``.jsonl`` file.

    Returns
    -------
    list[dict]
        Decoded records in file order.
    """
    records: List[Dict] = []
    with open(str(path), "r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if not stripped:
                continue
            records.append(json.loads(stripped))
    return records
