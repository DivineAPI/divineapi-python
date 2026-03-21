"""Western API - Transit endpoints (astroapi-4 and astroapi-8)."""

from typing import Any, Dict

from ..client import BaseClient


class TransitApi:
    """Transit endpoints for Western astrology."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    # ------------------------------------------------------------------ #
    # Birth-data helper
    # ------------------------------------------------------------------ #

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

    def _post4(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post("astroapi-4", path, self._birth(**kw))

    def _post8(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post("astroapi-8", path, self._birth(**kw))

    # ------------------------------------------------------------------ #
    # astroapi-4 transit endpoints
    # ------------------------------------------------------------------ #

    def basic(self, **kw: Any) -> Dict[str, Any]:
        """Transit Basic (pass transit_day/month/year/hour/min/sec via **kw)."""
        return self._post4("/western-api/v1/transit/basic", **kw)

    def daily(self, **kw: Any) -> Dict[str, Any]:
        """Transit Daily."""
        return self._post4("/western-api/v1/transit/daily", **kw)

    def weekly(self, transit_planet: str, **kw: Any) -> Dict[str, Any]:
        """Transit Weekly."""
        kw["transit_planet"] = transit_planet
        return self._post4("/western-api/v1/transit/weekly", **kw)

    def house(self, **kw: Any) -> Dict[str, Any]:
        """Transit House (pass full transit params via **kw)."""
        return self._post4("/western-api/v1/transit/house", **kw)

    # ------------------------------------------------------------------ #
    # astroapi-8 transit endpoints
    # ------------------------------------------------------------------ #

    def monthly(self, **kw: Any) -> Dict[str, Any]:
        """Transit Monthly (pass extensive transit params via **kw)."""
        return self._post8("/western-api/v1/transit/monthly", **kw)

    def full(self, **kw: Any) -> Dict[str, Any]:
        """Full Transit (pass extensive transit params via **kw)."""
        return self._post8("/western-api/v1/full-transit", **kw)

    def planet_retrograde(
        self, planet: str, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Planet Retrograde Transit."""
        return self._c.post("astroapi-8", "/western-api/v1/planet-retrograde-transit", {
            "planet": planet, "month": month, "year": year,
            "place": place, "lat": lat, "lon": lon, "tzone": tzone,
        })

    def planet_combustion(
        self, planet: str, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Planet Combustion Transit."""
        return self._c.post("astroapi-8", "/western-api/v1/planet-combustion-transit", {
            "planet": planet, "month": month, "year": year,
            "place": place, "lat": lat, "lon": lon, "tzone": tzone,
        })
