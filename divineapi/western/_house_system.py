"""House-system name resolution for the Western API.

The live Western API accepts ONLY single-letter Swiss Ephemeris house-system
codes. Word values like ``placidus`` are rejected on astroapi-4 and silently
ignored on astroapi-8, so every payload must send the letter code. This mirrors
the mapping used by the Divine Western MCP server.
"""

from typing import Optional

# Friendly house-system names mapped to the single-letter API codes.
HOUSE_SYSTEM_MAP = {
    "placidus": "P",
    "koch": "K",
    "porphyry": "O",
    "regiomontanus": "R",
    "campanus": "C",
    "equal": "E",
    "whole-sign": "W",
    "whole_sign": "W",
    "wholesign": "W",
    "morinus": "M",
    "alcabitius": "B",
}
VALID_HOUSE_SYSTEM_LETTERS = set(HOUSE_SYSTEM_MAP.values())
HOUSE_SYSTEM_FRIENDLY_NAMES = (
    "placidus, koch, porphyry, regiomontanus, campanus, equal, "
    "whole-sign, morinus, alcabitius"
)


def resolve_house_system(value: Optional[str]) -> str:
    """Map a friendly house-system name to its single-letter API code.

    Accepts friendly names case-insensitively (e.g. ``placidus``, ``Whole-Sign``)
    and already-valid single letters (passed through unchanged, upper-cased).
    An empty value defaults to ``P`` (Placidus). Raises ``ValueError`` for
    anything else.
    """
    hs = (value or "").strip()
    if not hs:
        return "P"
    if hs.upper() in VALID_HOUSE_SYSTEM_LETTERS:
        return hs.upper()
    mapped = HOUSE_SYSTEM_MAP.get(hs.lower())
    if mapped:
        return mapped
    raise ValueError(
        f"Invalid house_system '{value}'. Must be one of: "
        f"{HOUSE_SYSTEM_FRIENDLY_NAMES} (or a single-letter code: "
        f"{', '.join(sorted(VALID_HOUSE_SYSTEM_LETTERS))})"
    )
