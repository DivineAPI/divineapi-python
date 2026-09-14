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
    "equal-asc": "A",
    "equal_asc": "A",
    "equal-mc": "D",
    "equal_mc": "D",
    "vehlow": "V",
    "vehlow-equal": "V",
    "whole-sign": "W",
    "whole_sign": "W",
    "wholesign": "W",
    "meridian": "X",
    "axial-rotation": "X",
    "morinus": "M",
    "sripati": "S",
    "topocentric": "T",
    "polich-page": "T",
    "alcabitius": "B",
    "whole-sign-aries": "N",
    "whole_sign_aries": "N",
}
# The full Swiss Ephemeris code set the API accepts. Deliberately NOT derived
# from HOUSE_SYSTEM_MAP.values(): "A" and "E" are both Equal, so a value-derived
# set silently omitted A, D, V, X, S, T and N and raised ValueError for them
# even though the API accepts all sixteen. Verified 2026-09-14 against
# astroapi-4 /planetary-positions and astroapi-8 /persona-chart.
VALID_HOUSE_SYSTEM_LETTERS = {
    "P", "K", "O", "R", "C", "A", "E", "D",
    "V", "W", "X", "M", "S", "T", "B", "N",
}
HOUSE_SYSTEM_FRIENDLY_NAMES = (
    "placidus, koch, porphyry, regiomontanus, campanus, equal, equal-asc, "
    "equal-mc, vehlow, whole-sign, meridian, morinus, sripati, topocentric, "
    "alcabitius, whole-sign-aries"
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
