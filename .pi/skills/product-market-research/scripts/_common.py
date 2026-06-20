"""
Shared utility module for product-market research scripts.

Stdlib-only helpers for JSONL I/O, unit parsing, currency formatting,
ISO date validation, and uniform CLI logging.

Target: Python 3.9+
"""

from __future__ import annotations

import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

_LOG = logging.getLogger("product-market-research")


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
# Unit parsing  (mass, volume, count)
# ---------------------------------------------------------------------------

#: Normalised name → canonical unit (lowercase)
_UNIT_ALIASES = {
    # mass
    "microgram": "μg",
    "micrograms": "μg",
    "mcg": "μg",
    "ug": "μg",
    # gram → mg is handled by conversion below
    "gram": "g",
    "grams": "g",
    "milligram": "mg",
    "milligrams": "mg",
    # volume
    "milliliter": "mL",
    "milliliters": "mL",
    "millilitre": "mL",
    "millilitres": "mL",
    "ml": "mL",
    "liter": "L",
    "liters": "L",
    "litre": "L",
    "litres": "L",
    "l": "L",
    # count
    "capsule": "caps",
    "capsules": "caps",
    "cap": "caps",
    "tablet": "tabs",
    "tablets": "tabs",
    "tab": "tabs",
    "bag": "bags",
    "bags": "bags",
    "each": "each",
    "unit": "each",
    "units": "each",
}

#: Category for each canonical unit.
_UNIT_CATEGORY = {
    # mass
    "μg": "mass",
    "mg": "mass",
    "g": "mass",
    # volume
    "mL": "volume",
    "L": "volume",
    # count
    "caps": "count",
    "tabs": "count",
    "bags": "count",
    "each": "count",
}

#: Conversion factor to the *base* unit for each category.
#: Mass  → mg ; Volume → mL ; Count → identity.
_TO_BASE = {
    "μg": 1.0 / 1000.0,
    "mg": 1.0,
    "g": 1000.0,
    "mL": 1.0,
    "L": 1000.0,
    "caps": 1.0,
    "tabs": 1.0,
    "bags": 1.0,
    "each": 1.0,
}

#: Canonical units recognised by ``parse_quantity``.
_CANONICAL = frozenset(_TO_BASE.keys())

#: Pattern used to decompose ``"<value> <unit>"`` strings.
_QUANTITY_RE = re.compile(
    r"^\s*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*"
    r"(μg|µg|mcg|ug|mg|g|mL|ml|milliliter|milliliters|millilitre|millilitres"
    r"|L|l|liter|liters|litre|litres"
    r"|caps|capsule|capsules|cap|tabs|tablet|tablets|tab|bags|bag|each|units?)\s*$",
    re.IGNORECASE,
)


def parse_quantity(
    value_str: str,
    target_unit: Optional[str] = None,
) -> Dict[str, Union[float, str]]:
    """Parse a human-readable quantity string.

    Supports mass (μg, mg, g), volume (mL, L), and count units (caps,
    tabs, bags, each).  By default values are normalised to the category's
    base unit (mg for mass, mL for volume, count preserved as-is).  Pass
    *target_unit* to request a specific canonical unit instead.

    Parameters
    ----------
    value_str : str
        String like ``"1.5 g"``, ``"500 μg"``, or ``"10 mL"``.
    target_unit : str or None
        Desired output unit (e.g. ``"mg"``, ``"mL"``).  Must belong to the
        same quantity category as the input.

    Returns
    -------
    dict
        ``{"value": <float>, "unit": "<canonical unit>"}``.

    Raises
    ------
    ValueError
        If the string cannot be parsed, if *target_unit* belongs to a
        different quantity category (e.g. mass vs volume), or if the unit
        is unknown.
    """
    match = _QUANTITY_RE.match(value_str)
    if not match:
        raise ValueError(
            "cannot parse quantity: {!r}".format(value_str)
        )

    raw_value = float(match.group(1))
    raw_unit = match.group(2).lower()

    # Resolve alias → canonical unit.
    canonical = _UNIT_ALIASES.get(raw_unit, raw_unit)
    if canonical not in _CANONICAL:
        raise ValueError(
            "unknown unit: {!r}".format(match.group(2))
        )

    category = _UNIT_CATEGORY[canonical]

    # Normalise to base unit for the category.
    base_value = raw_value * _TO_BASE[canonical]

    if target_unit is None:
        # Return in the category's base unit.
        if category == "mass":
            result_unit = "mg"
        elif category == "volume":
            result_unit = "mL"
        else:
            result_unit = canonical  # count units stay as-is
        result_value = base_value
    else:
        # Normalise target to canonical form.
        target_canon = _UNIT_ALIASES.get(target_unit.lower(), target_unit.lower())
        if target_canon not in _CANONICAL:
            raise ValueError(
                "unknown target unit: {!r}".format(target_unit)
            )
        target_cat = _UNIT_CATEGORY[target_canon]
        if target_cat != category:
            raise ValueError(
                "incompatible units: cannot convert {} ({}) to {} ({})".format(
                    canonical, category, target_canon, target_cat
                )
            )
        result_value = base_value / _TO_BASE[target_canon]
        result_unit = target_canon

    return {"value": result_value, "unit": result_unit}


# ---------------------------------------------------------------------------
# Currency formatting
# ---------------------------------------------------------------------------

#: Simple currency symbol map for display purposes.
_CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CNY": "¥",
    "CHF": "CHF",
    "CAD": "CA$",
    "AUD": "AU$",
    "KRW": "₩",
    "INR": "₹",
}


def format_currency(value: float, currency_code: str) -> str:
    """Format a numeric value as a human-readable currency string.

    Uses ``locale``-free formatting with two decimal places for most
    currencies (zero decimal places for JPY, KRW, etc.).

    Parameters
    ----------
    value : float
        Numeric amount.
    currency_code : str
        ISO 4217 three-letter currency code (e.g. ``"USD"``).

    Returns
    -------
    str
        Formatted string such as ``"$1,234.56"`` or ``"¥1,000"``.
    """
    code = currency_code.upper()

    # Zero-decimal currencies (typically)
    zero_dec = {"JPY", "KRW", "CLP", "COP", "IDR", "ISK", "PYG", "UGX",
                "VND", "XAF", "XOF", "XPF"}

    if code in zero_dec:
        formatted = "{:,.0f}".format(value)
    else:
        formatted = "{:,.2f}".format(value)

    symbol = _CURRENCY_SYMBOLS.get(code, code + " ")
    # If symbol is a prefix like "$", prepend; if a suffix-like code, append.
    if symbol.endswith(" "):
        return symbol + formatted
    if symbol in ("CHF",):
        return formatted + " " + symbol
    return symbol + formatted


# ---------------------------------------------------------------------------
# ISO 8601 date validation
# ---------------------------------------------------------------------------

_ISO_DATE_PATTERNS = [
    # YYYY
    re.compile(r"^\d{4}$"),
    # YYYY-MM
    re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$"),
    # YYYY-MM-DD
    re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$"),
]


def validate_iso_date(date_str: str) -> bool:
    """Check whether *date_str* is a valid ISO 8601 partial or full date.

    Accepts ``YYYY``, ``YYYY-MM``, and ``YYYY-MM-DD``.  Leading/trailing
    whitespace is not allowed.

    Parameters
    ----------
    date_str : str
        The date string to validate.

    Returns
    -------
    bool
        ``True`` if the string matches one of the recognised ISO 8601
        patterns, ``False`` otherwise.
    """
    if not isinstance(date_str, str):
        return False

    for pattern in _ISO_DATE_PATTERNS:
        if pattern.match(date_str):
            # For YYYY-MM-DD, verify it is a real calendar date.
            if len(date_str) == 10:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    return False
            return True
    return False
