"""Numerology endpoints (astroapi-7 and astroapi-4)."""

from typing import Any, Dict

from .client import BaseClient


class NumerologyApi:
    """Numerology endpoints (Chaldean, mobile number, core numbers)."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _name_dob(
        fname: str, lname: str,
        day: int, month: int, year: int,
        lan: str = "en", **extra: Any,
    ) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "fname": fname, "lname": lname,
            "day": day, "month": month, "year": year,
            "lan": lan,
        }
        d.update(extra)
        return d

    # ------------------------------------------------------------------ #
    # Mobile number endpoints (astroapi-7)
    # ------------------------------------------------------------------ #

    def new_mobile_number(
        self, fname: str, lname: str,
        day: int, month: int, year: int,
    ) -> Dict[str, Any]:
        """New Mobile Number suggestion."""
        return self._c.post("astroapi-7", "/numerology/v1/new-mobile-number", {
            "fname": fname, "lname": lname,
            "day": day, "month": month, "year": year,
        })

    def analyze_mobile_number(
        self, fname: str, lname: str,
        day: int, month: int, year: int,
        mobile_number: str,
    ) -> Dict[str, Any]:
        """Analyze Mobile Number."""
        return self._c.post("astroapi-7", "/numerology/v1/analyze-mobile-number", {
            "fname": fname, "lname": lname,
            "day": day, "month": month, "year": year,
            "mobile_number": mobile_number,
        })

    # ------------------------------------------------------------------ #
    # Chaldean numerology (astroapi-7) - 12 endpoints
    # ------------------------------------------------------------------ #

    def loshu_grid(self, **kw: Any) -> Dict[str, Any]:
        """Loshu Grid."""
        return self._c.post("astroapi-7", "/numerology/v1/loshu-grid", self._name_dob(**kw))

    def zodiac_planet_number(self, **kw: Any) -> Dict[str, Any]:
        """Zodiac Planet Number."""
        return self._c.post("astroapi-7", "/numerology/v1/zodiac-planet-number", self._name_dob(**kw))

    def luck_numerology(self, **kw: Any) -> Dict[str, Any]:
        """Luck Numerology."""
        return self._c.post("astroapi-7", "/numerology/v1/luck-numerology", self._name_dob(**kw))

    def name_number(self, **kw: Any) -> Dict[str, Any]:
        """Name Number."""
        return self._c.post("astroapi-7", "/numerology/v1/name-number", self._name_dob(**kw))

    def name_correction(
        self, full_name: str,
        day: int, month: int, year: int,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Name Correction: suggest better-aligned spellings of a full name.

        Note: this endpoint takes a single ``full_name`` (not fname/lname
        like its numerology siblings).
        """
        return self._c.post("astroapi-7", "/numerology/v1/name-correction", {
            "full_name": full_name,
            "day": day, "month": month, "year": year,
            "lan": lan,
        })

    def birthday_number(self, **kw: Any) -> Dict[str, Any]:
        """Birthday Number."""
        return self._c.post("astroapi-7", "/numerology/v1/birthday-number", self._name_dob(**kw))

    def missing_numbers(self, **kw: Any) -> Dict[str, Any]:
        """Missing Numbers."""
        return self._c.post("astroapi-7", "/numerology/v1/missing-numbers", self._name_dob(**kw))

    def driver_and_conductor_numbers(self, **kw: Any) -> Dict[str, Any]:
        """Driver and Conductor Numbers."""
        return self._c.post("astroapi-7", "/numerology/v1/driver-and-conductor-numbers", self._name_dob(**kw))

    def two_numbers_arrows(self, **kw: Any) -> Dict[str, Any]:
        """Two Numbers Arrows."""
        return self._c.post("astroapi-7", "/numerology/v1/two-numbers-arrows", self._name_dob(**kw))

    def three_numbers_arrows(self, **kw: Any) -> Dict[str, Any]:
        """Three Numbers Arrows."""
        return self._c.post("astroapi-7", "/numerology/v1/three-numbers-arrows", self._name_dob(**kw))

    def repeating_numbers(self, **kw: Any) -> Dict[str, Any]:
        """Repeating Numbers."""
        return self._c.post("astroapi-7", "/numerology/v1/repeating-numbers", self._name_dob(**kw))

    def yearly_prediction(self, **kw: Any) -> Dict[str, Any]:
        """Yearly Prediction."""
        return self._c.post("astroapi-7", "/numerology/v1/yearly-prediction", self._name_dob(**kw))

    def gemstones(self, **kw: Any) -> Dict[str, Any]:
        """Gemstones."""
        return self._c.post("astroapi-7", "/numerology/v1/gemstones", self._name_dob(**kw))

    # ------------------------------------------------------------------ #
    # Core numbers (astroapi-4)
    # ------------------------------------------------------------------ #

    def core_numbers(
        self, full_name: str,
        day: int, month: int, year: int,
        gender: str, method: str,
    ) -> Dict[str, Any]:
        """Core Numbers (Pythagorean / Chaldean)."""
        return self._c.post("astroapi-4", "/numerology/v1/core-numbers", {
            "full_name": full_name,
            "day": day, "month": month, "year": year,
            "gender": gender, "method": method,
        })
