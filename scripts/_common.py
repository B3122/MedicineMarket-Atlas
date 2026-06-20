"""
Shared utility module for cross-skill project-level scripts.

Stdlib-only helpers for JSONL I/O, uniform stderr logging, and JSON
Schema loading with automatic project-root resolution.

Target: Python 3.9+
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Union


# ---------------------------------------------------------------------------
# Project root resolution
# ---------------------------------------------------------------------------

#: Absolute path to the project root, determined by walking up from this
#: file's location until a ``schemas/`` directory or ``.git`` marker is found.
_PROJECT_ROOT: Path | None = None


def _find_project_root() -> Path:
    """Walk up from ``scripts/`` to locate the project root.

    Stops at the first ancestor that contains a ``schemas/`` directory or a
    ``.git`` directory (checked in that order).  Falls back to the parent of
    ``scripts/`` when neither marker is found.

    Returns
    -------
    Path
        Absolute path to the project root directory.
    """
    current = Path(__file__).resolve().parent  # scripts/
    for ancestor in [current] + list(current.parents):
        if (ancestor / "schemas").is_dir():
            return ancestor
        if (ancestor / ".git").is_dir():
            return ancestor
    # Fallback: parent of scripts/
    return current.parent


def get_project_root() -> Path:
    """Return the cached project root, discovering it on first call."""
    global _PROJECT_ROOT
    if _PROJECT_ROOT is None:
        _PROJECT_ROOT = _find_project_root()
    return _PROJECT_ROOT


# Ensure the project root is on ``sys.path`` so sibling modules (e.g.
# ``scripts._common``) are importable regardless of working directory.
_root = get_project_root()
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

_LOG = logging.getLogger("market-research")


def _setup_logging() -> None:
    """Configure stderr logging once."""
    if _LOG.handlers:
        return
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    _LOG.addHandler(handler)
    _LOG.setLevel(logging.INFO)


def log_info(msg: str) -> None:
    """Print an info-level message to stderr with uniform formatting.

    Parameters
    ----------
    msg : str
        The message to log.
    """
    _setup_logging()
    _LOG.info(msg)


def log_error(msg: str) -> None:
    """Print an error-level message to stderr with uniform formatting.

    Parameters
    ----------
    msg : str
        The error message to log.
    """
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


def write_jsonl(path: Union[str, Path], records: List[Dict]) -> None:
    """Write *records* as UTF-8 line-delimited JSON.

    Each dict is serialised on its own line.  The file is created or
    truncated on open.

    Parameters
    ----------
    path : str or Path
        Output file path.
    records : list[dict]
        Records to write.
    """
    with open(str(path), "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Schema loader
# ---------------------------------------------------------------------------


def load_schema(name: str) -> Dict:
    """Load a JSON Schema file from the project-level ``schemas/`` directory.

    Resolves the project root automatically, then reads
    ``schemas/<name>.schema.json``.  Raises ``FileNotFoundError`` if the
    schema file does not exist and ``json.JSONDecodeError`` if the file
    contains invalid JSON.

    Parameters
    ----------
    name : str
        Schema stem (e.g. ``"listing"`` loads ``schemas/listing.schema.json``).

    Returns
    -------
    dict
        The parsed JSON Schema as a Python dictionary.
    """
    schema_path = get_project_root() / "schemas" / f"{name}.schema.json"
    with open(str(schema_path), "r", encoding="utf-8") as fh:
        return json.load(fh)
