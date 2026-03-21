"""Indian API - Match Making endpoints (astroapi-3)."""

from typing import Any, Dict

from ..client import BaseClient

HOST = "astroapi-3"


class MatchMakingApi:
    """Match-making / compatibility endpoints using couple birth data."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    # ------------------------------------------------------------------ #
    # Couple payload builder
    # ------------------------------------------------------------------ #

    @staticmethod
    def _couple(
        p1_full_name: str, p1_day: int, p1_month: int, p1_year: int,
        p1_hour: int, p1_min: int, p1_sec: int, p1_gender: str,
        p1_place: str, p1_lat: float, p1_lon: float, p1_tzone: float,
        p2_full_name: str, p2_day: int, p2_month: int, p2_year: int,
        p2_hour: int, p2_min: int, p2_sec: int, p2_gender: str,
        p2_place: str, p2_lat: float, p2_lon: float, p2_tzone: float,
        lan: str = "en", **extra: Any,
    ) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "p1_full_name": p1_full_name, "p1_day": p1_day, "p1_month": p1_month,
            "p1_year": p1_year, "p1_hour": p1_hour, "p1_min": p1_min,
            "p1_sec": p1_sec, "p1_gender": p1_gender, "p1_place": p1_place,
            "p1_lat": p1_lat, "p1_lon": p1_lon, "p1_tzone": p1_tzone,
            "p2_full_name": p2_full_name, "p2_day": p2_day, "p2_month": p2_month,
            "p2_year": p2_year, "p2_hour": p2_hour, "p2_min": p2_min,
            "p2_sec": p2_sec, "p2_gender": p2_gender, "p2_place": p2_place,
            "p2_lat": p2_lat, "p2_lon": p2_lon, "p2_tzone": p2_tzone,
            "lan": lan,
        }
        d.update(extra)
        return d

    def _post_couple(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post(HOST, path, self._couple(**kw))

    # ------------------------------------------------------------------ #
    # Endpoints
    # ------------------------------------------------------------------ #

    def ashtakoot_milan(self, **kw: Any) -> Dict[str, Any]:
        """Ashtakoot Milan."""
        return self._post_couple("/indian-api/v2/ashtakoot-milan", **kw)

    def dashakoot_milan(self, **kw: Any) -> Dict[str, Any]:
        """Dashakoot Milan."""
        return self._post_couple("/indian-api/v2/dashakoot-milan", **kw)

    def nav_pancham_yoga(self, **kw: Any) -> Dict[str, Any]:
        """Nav Pancham Yoga."""
        return self._post_couple("/indian-api/v1/nav-pancham-yoga", **kw)

    def basic_astro_details(self, **kw: Any) -> Dict[str, Any]:
        """Matching Basic Astro Details."""
        return self._post_couple("/indian-api/v3/matching/basic-astro-details", **kw)

    def planetary_positions(self, **kw: Any) -> Dict[str, Any]:
        """Matching Planetary Positions."""
        return self._post_couple("/indian-api/v2/matching/planetary-positions", **kw)

    def vimshottari_dasha(self, **kw: Any) -> Dict[str, Any]:
        """Matching Vimshottari Dasha."""
        return self._post_couple("/indian-api/v1/matching/vimshottari-dasha", **kw)

    def manglik_dosha(self, **kw: Any) -> Dict[str, Any]:
        """Matching Manglik Dosha."""
        return self._post_couple("/indian-api/v2/matching/manglik-dosha", **kw)

    def horoscope_chart(self, chart_id: str, **kw: Any) -> Dict[str, Any]:
        """Matching Horoscope Chart."""
        return self._post_couple(f"/indian-api/v1/matching/horoscope-chart/{chart_id}", **kw)
