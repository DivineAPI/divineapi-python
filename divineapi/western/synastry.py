"""Western API - Synastry endpoints (astroapi-4)."""

from typing import Any, Dict

from ..client import BaseClient

HOST = "astroapi-4"


class SynastryApi:
    """Synastry (relationship compatibility) endpoints."""

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

    # ------------------------------------------------------------------ #
    # v1 synastry endpoints (8)
    # ------------------------------------------------------------------ #

    def planetary_positions(self, **kw: Any) -> Dict[str, Any]:
        """Synastry Planetary Positions."""
        return self._post("/western-api/v1/synastry/planetary-positions", **kw)

    def house_cusps(self, **kw: Any) -> Dict[str, Any]:
        """Synastry House Cusps."""
        return self._post("/western-api/v1/synastry/house-cusps", **kw)

    def natal_wheel_chart(self, **kw: Any) -> Dict[str, Any]:
        """Synastry Natal Wheel Chart."""
        return self._post("/western-api/v1/synastry/natal-wheel-chart", **kw)

    def aspect(self, **kw: Any) -> Dict[str, Any]:
        """Synastry Aspect."""
        return self._post("/western-api/v1/synastry/aspect", **kw)

    def harmonious_aspect_reading(self, **kw: Any) -> Dict[str, Any]:
        """Synastry Harmonious Aspect Reading."""
        return self._post("/western-api/v1/synastry/harmonious-aspect-reading", **kw)

    def conflicting_aspect_reading(self, **kw: Any) -> Dict[str, Any]:
        """Synastry Conflicting Aspect Reading."""
        return self._post("/western-api/v1/synastry/conflicting-aspect-reading", **kw)

    def contrasting_aspect_reading(self, **kw: Any) -> Dict[str, Any]:
        """Synastry Contrasting Aspect Reading."""
        return self._post("/western-api/v1/synastry/contrasting-aspect-reading", **kw)

    def intense_aspect_reading(self, **kw: Any) -> Dict[str, Any]:
        """Synastry Intense Aspect Reading."""
        return self._post("/western-api/v1/synastry/intense-aspect-reading", **kw)

    # ------------------------------------------------------------------ #
    # v2 compatibility endpoints (5)
    # ------------------------------------------------------------------ #

    def physical_compatibility(self, **kw: Any) -> Dict[str, Any]:
        """Physical Compatibility."""
        return self._post("/western-api/v2/synastry/physical-compatibility", **kw)

    def emotional_compatibility(self, **kw: Any) -> Dict[str, Any]:
        """Emotional Compatibility."""
        return self._post("/western-api/v2/synastry/emotional-compatibility", **kw)

    def sexual_compatibility(self, **kw: Any) -> Dict[str, Any]:
        """Sexual Compatibility."""
        return self._post("/western-api/v2/synastry/sexual-compatibility", **kw)

    def spiritual_compatibility(self, **kw: Any) -> Dict[str, Any]:
        """Spiritual Compatibility."""
        return self._post("/western-api/v2/synastry/spiritual-compatibility", **kw)

    def financial_compatibility(self, **kw: Any) -> Dict[str, Any]:
        """Financial Compatibility."""
        return self._post("/western-api/v2/synastry/financial-compatibility", **kw)
