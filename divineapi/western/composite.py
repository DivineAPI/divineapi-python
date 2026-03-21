"""Western API - Composite endpoints (astroapi-8)."""

from typing import Any, Dict

from ..client import BaseClient

HOST = "astroapi-8"


class CompositeApi:
    """Composite chart endpoints."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    @staticmethod
    def _couple(
        p1_full_name: str, p1_day: int, p1_month: int, p1_year: int,
        p1_hour: int, p1_min: int, p1_sec: int, p1_gender: str,
        p1_place: str, p1_lat: float, p1_lon: float, p1_tzone: float,
        p2_full_name: str, p2_day: int, p2_month: int, p2_year: int,
        p2_hour: int, p2_min: int, p2_sec: int, p2_gender: str,
        p2_place: str, p2_lat: float, p2_lon: float, p2_tzone: float,
        lan: str = "en", house_system: str = "placidus",
        **extra: Any,
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
            "lan": lan, "house_system": house_system,
        }
        d.update(extra)
        return d

    def _post(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post(HOST, path, self._couple(**kw))

    def planetary_positions(self, **kw: Any) -> Dict[str, Any]:
        """Composite Planetary Positions."""
        return self._post("/western-api/v1/composite/planetary-positions", **kw)

    def house_cusps(self, **kw: Any) -> Dict[str, Any]:
        """Composite House Cusps."""
        return self._post("/western-api/v1/composite/house-cusps", **kw)

    def aspect_table(self, **kw: Any) -> Dict[str, Any]:
        """Composite Aspect Table."""
        return self._post("/western-api/v1/composite/aspect-table", **kw)

    def natal_wheel_chart(self, **kw: Any) -> Dict[str, Any]:
        """Composite Natal Wheel Chart."""
        return self._post("/western-api/v1/composite/natal-wheel-chart", **kw)
