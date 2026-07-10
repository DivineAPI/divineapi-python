"""Western API - Transit endpoints (astroapi-4 and astroapi-8)."""

from typing import Any, Dict

from ..client import BaseClient
from ._house_system import resolve_house_system


class TransitApi:
    """Transit endpoints for Western astrology."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    # ------------------------------------------------------------------ #
    # Payload helpers
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
            "lan": lan, "house_system": resolve_house_system(house_system),
        }
        d.update(extra)
        return d

    @staticmethod
    def _transit_dt(
        transit_day: int, transit_month: int, transit_year: int,
        transit_hour: int = 0, transit_min: int = 0, transit_sec: int = 0,
    ) -> Dict[str, Any]:
        return {
            "transit_day": transit_day, "transit_month": transit_month,
            "transit_year": transit_year, "transit_hour": transit_hour,
            "transit_min": transit_min, "transit_sec": transit_sec,
        }

    @staticmethod
    def _transit_loc(
        transit_lat: float, transit_lon: float,
        transit_tzone: float, transit_place: str,
    ) -> Dict[str, Any]:
        return {
            "transit_lat": transit_lat, "transit_lon": transit_lon,
            "transit_tzone": transit_tzone, "transit_place": transit_place,
        }

    def _post4(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post("astroapi-4", path, self._birth(**kw))

    def _post8(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post("astroapi-8", path, self._birth(**kw))

    # ------------------------------------------------------------------ #
    # astroapi-4 transit endpoints
    # ------------------------------------------------------------------ #

    def basic(
        self,
        transit_day: int, transit_month: int, transit_year: int,
        transit_hour: int = 0, transit_min: int = 0, transit_sec: int = 0,
        **kw: Any,
    ) -> Dict[str, Any]:
        """Transit Basic. Requires the transit date; time defaults to 00:00:00."""
        payload = self._birth(**kw)
        payload.update(self._transit_dt(
            transit_day, transit_month, transit_year,
            transit_hour, transit_min, transit_sec,
        ))
        return self._c.post("astroapi-4", "/western-api/v1/transit/basic", payload)

    def daily(self, **kw: Any) -> Dict[str, Any]:
        """Transit Daily."""
        return self._post4("/western-api/v1/transit/daily", **kw)

    def weekly(self, transit_planet: str, **kw: Any) -> Dict[str, Any]:
        """Transit Weekly. Requires the transiting planet (e.g. 'moon')."""
        kw["transit_planet"] = transit_planet
        return self._post4("/western-api/v1/transit/weekly", **kw)

    def house(
        self,
        transit_day: int, transit_month: int, transit_year: int,
        transit_lat: float, transit_lon: float,
        transit_tzone: float, transit_place: str,
        transit_hour: int = 0, transit_min: int = 0, transit_sec: int = 0,
        **kw: Any,
    ) -> Dict[str, Any]:
        """Transit House. Requires transit date + location; time defaults to 00:00:00."""
        payload = self._birth(**kw)
        payload.update(self._transit_dt(
            transit_day, transit_month, transit_year,
            transit_hour, transit_min, transit_sec,
        ))
        payload.update(self._transit_loc(
            transit_lat, transit_lon, transit_tzone, transit_place,
        ))
        return self._c.post("astroapi-4", "/western-api/v1/transit/house", payload)

    # ------------------------------------------------------------------ #
    # astroapi-8 transit endpoints
    # ------------------------------------------------------------------ #

    def monthly(
        self,
        transit_planet: str, transit_month: int, transit_year: int,
        transit_lat: float, transit_lon: float,
        transit_tzone: float, transit_place: str,
        **kw: Any,
    ) -> Dict[str, Any]:
        """Transit Monthly. Requires the transiting planet, month, year and location."""
        payload = self._birth(**kw)
        payload.update({
            "transit_planet": transit_planet,
            "transit_month": transit_month, "transit_year": transit_year,
        })
        payload.update(self._transit_loc(
            transit_lat, transit_lon, transit_tzone, transit_place,
        ))
        return self._c.post("astroapi-8", "/western-api/v2/transit/monthly", payload)

    def full(
        self,
        transit_planet: str,
        transit_day: int, transit_month: int, transit_year: int,
        transit_lat: float, transit_lon: float,
        transit_tzone: float, transit_place: str,
        transit_hour: int = 0, transit_min: int = 0, transit_sec: int = 0,
        **kw: Any,
    ) -> Dict[str, Any]:
        """Full Transit. Requires the transiting planet, transit date and location."""
        payload = self._birth(**kw)
        payload["transit_planet"] = transit_planet
        payload.update(self._transit_dt(
            transit_day, transit_month, transit_year,
            transit_hour, transit_min, transit_sec,
        ))
        payload.update(self._transit_loc(
            transit_lat, transit_lon, transit_tzone, transit_place,
        ))
        return self._c.post("astroapi-8", "/western-api/v1/full-transit", payload)

    def planet_retrograde(
        self, planet: str, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Planet Retrograde Transit."""
        return self._c.post("astroapi-8", "/western-api/v1/planet-retrograde-transit", {
            "planet": planet, "month": month, "year": year,
            "place": place, "lat": lat, "lon": lon, "tzone": tzone,
        })

    def planetary_ingress(
        self, planet: str, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Planetary Ingress."""
        return self._c.post("astroapi-8", "/western-api/v1/planetary-ingress", {
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

    def wheel_chart(
        self,
        transit_day: int, transit_month: int, transit_year: int,
        transit_lat: float, transit_lon: float,
        transit_tzone: float, transit_place: str,
        transit_hour: int = 0, transit_min: int = 0, transit_sec: int = 0,
        **kw: Any,
    ) -> Dict[str, Any]:
        """Transit Wheel Chart. Requires transit date + location."""
        payload = self._birth(**kw)
        payload.update(self._transit_dt(
            transit_day, transit_month, transit_year,
            transit_hour, transit_min, transit_sec,
        ))
        payload.update(self._transit_loc(
            transit_lat, transit_lon, transit_tzone, transit_place,
        ))
        return self._c.post("astroapi-8", "/western-api/v1/transit/wheel-chart", payload)

    def planetary_positions(
        self,
        transit_day: int, transit_month: int, transit_year: int,
        transit_lat: float, transit_lon: float,
        transit_tzone: float, transit_place: str,
        transit_hour: int = 0, transit_min: int = 0, transit_sec: int = 0,
        **kw: Any,
    ) -> Dict[str, Any]:
        """Transit Planetary Positions. Requires transit date + location."""
        payload = self._birth(**kw)
        payload.update(self._transit_dt(
            transit_day, transit_month, transit_year,
            transit_hour, transit_min, transit_sec,
        ))
        payload.update(self._transit_loc(
            transit_lat, transit_lon, transit_tzone, transit_place,
        ))
        return self._c.post("astroapi-8", "/western-api/v1/transit/planetary-positions", payload)
