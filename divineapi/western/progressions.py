"""Western API - Progressions endpoints (astroapi-8)."""

from typing import Any, Dict, Optional

from ..client import BaseClient
from ._house_system import resolve_house_system

HOST = "astroapi-8"


class ProgressionsApi:
    """Progression endpoints (secondary progressions, arc directions, lunar events)."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    @staticmethod
    def _birth(
        full_name: str, day: int, month: int, year: int,
        hour: int, min: int, sec: int, gender: str,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", house_system: str = "placidus",
        **extra: Any,
    ) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "full_name": full_name, "day": day, "month": month, "year": year,
            "hour": hour, "min": min, "sec": sec, "gender": gender,
            "place": place, "lat": lat, "lon": lon, "tzone": tzone,
            "lan": lan, "house_system": resolve_house_system(house_system),
        }
        d.update(extra)
        return d

    def progressed_lunar_events(self, prenatal_type: str, **kw: Any) -> Dict[str, Any]:
        """Progressed Lunar Events."""
        kw["prenatal_type"] = prenatal_type
        return self._c.post(HOST, "/western-api/v1/progressed-lunar-events", self._birth(**kw))

    def planetary_arc_directions(
        self, planet: str,
        progressed_day: int, progressed_month: int, progressed_year: int,
        **kw: Any,
    ) -> Dict[str, Any]:
        """Planetary Arc Directions."""
        kw["planet"] = planet
        kw["progressed_day"] = progressed_day
        kw["progressed_month"] = progressed_month
        kw["progressed_year"] = progressed_year
        return self._c.post(HOST, "/western-api/v1/planetary-arc-directions", self._birth(**kw))

    def secondary_progressions(
        self,
        progressed_day: int, progressed_month: int, progressed_year: int,
        progressed_hour: int, progressed_min: int, progressed_sec: int,
        progressed_type: str,
        planet: Optional[str] = None,
        **kw: Any,
    ) -> Dict[str, Any]:
        """Secondary Progressions.

        ``progressed_day/month/year/hour/min/sec`` and ``progressed_type`` are
        required by the API; ``planet`` is optional.
        """
        kw["progressed_day"] = progressed_day
        kw["progressed_month"] = progressed_month
        kw["progressed_year"] = progressed_year
        kw["progressed_hour"] = progressed_hour
        kw["progressed_min"] = progressed_min
        kw["progressed_sec"] = progressed_sec
        kw["progressed_type"] = progressed_type
        if planet is not None:
            kw["planet"] = planet
        return self._c.post(HOST, "/western-api/v1/secondary-progressions", self._birth(**kw))
