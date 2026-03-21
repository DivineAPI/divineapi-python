"""Western API - Planet Returns endpoints (astroapi-8)."""

from typing import Any, Dict

from ..client import BaseClient

HOST = "astroapi-8"


class PlanetReturnsApi:
    """Planet return (solar return, lunar return, etc.) endpoints."""

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
            "lan": lan, "house_system": house_system,
        }
        d.update(extra)
        return d

    def planet_return_list(
        self, planet: str, return_year: int,
        return_lat: float, return_lon: float,
        return_tzone: float, return_place: str,
        **kw: Any,
    ) -> Dict[str, Any]:
        """Planet Return List."""
        kw["planet"] = planet
        kw["return_year"] = return_year
        kw["return_lat"] = return_lat
        kw["return_lon"] = return_lon
        kw["return_tzone"] = return_tzone
        kw["return_place"] = return_place
        return self._c.post(HOST, "/western-api/v1/planet-returns-list", self._birth(**kw))

    def planet_return_details(
        self, planet: str, return_key: str,
        return_lat: float, return_lon: float,
        return_tzone: float, return_place: str,
        **kw: Any,
    ) -> Dict[str, Any]:
        """Planet Return Details."""
        kw["planet"] = planet
        kw["return_key"] = return_key
        kw["return_lat"] = return_lat
        kw["return_lon"] = return_lon
        kw["return_tzone"] = return_tzone
        kw["return_place"] = return_place
        return self._c.post(HOST, "/western-api/v1/planet-return-details", self._birth(**kw))
