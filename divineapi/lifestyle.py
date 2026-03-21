"""Lifestyle endpoints (astroapi-7)."""

from typing import Any, Dict

from .client import BaseClient

HOST = "astroapi-7"


class LifestyleApi:
    """Lifestyle endpoints (gift guru, beauty, fashion)."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    def _post(
        self, path: str,
        sign: str, h_day: str, tzone: float, lan: str = "en",
    ) -> Dict[str, Any]:
        return self._c.post(HOST, path, {
            "sign": sign, "h_day": h_day, "tzone": tzone, "lan": lan,
        })

    def zodiac_gift_guru(
        self, sign: str, h_day: str, tzone: float, lan: str = "en",
    ) -> Dict[str, Any]:
        """Zodiac Gift Guru."""
        return self._post("/api/v1/zodiac-gift-guru", sign, h_day, tzone, lan)

    def beauty_by_the_stars(
        self, sign: str, h_day: str, tzone: float, lan: str = "en",
    ) -> Dict[str, Any]:
        """Beauty By The Stars."""
        return self._post("/api/v1/beauty-by-the-stars", sign, h_day, tzone, lan)

    def astro_chic_picks(
        self, sign: str, h_day: str, tzone: float, lan: str = "en",
    ) -> Dict[str, Any]:
        """Astro Chic Picks."""
        return self._post("/api/v1/astro-chic-picks", sign, h_day, tzone, lan)
