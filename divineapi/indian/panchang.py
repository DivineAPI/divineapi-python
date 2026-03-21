"""Indian API - Panchang endpoints (various hosts)."""

from typing import Any, Dict, Optional

from ..client import BaseClient


class PanchangApi:
    """Panchang, calendar, and transit endpoints."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    # ------------------------------------------------------------------ #
    # Helper to build common location/date payload
    # ------------------------------------------------------------------ #

    @staticmethod
    def _loc(
        day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", **extra: Any,
    ) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "day": day, "month": month, "year": year,
            "place": place, "lat": lat, "lon": lon,
            "tzone": tzone, "lan": lan,
        }
        d.update(extra)
        return d

    @staticmethod
    def _month_loc(
        month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", **extra: Any,
    ) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "month": month, "year": year,
            "place": place, "lat": lat, "lon": lon,
            "tzone": tzone, "lan": lan,
        }
        d.update(extra)
        return d

    # ------------------------------------------------------------------ #
    # Endpoints
    # ------------------------------------------------------------------ #

    def find_sun_and_moon(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Find Sun And Moon."""
        return self._c.post("astroapi-2", "/indian-api/v2/find-sun-and-moon",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def find_panchang(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", sanskrit_sign: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Find Panchang."""
        data = self._loc(day, month, year, place, lat, lon, tzone, lan)
        if sanskrit_sign is not None:
            data["sanskrit_sign"] = sanskrit_sign
        return self._c.post("astroapi-1", "/indian-api/v2/find-panchang", data)

    def find_chandramasa(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", month_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Find Chandramasa."""
        data = self._loc(day, month, year, place, lat, lon, tzone, lan)
        if month_type is not None:
            data["month_type"] = month_type
        return self._c.post("astroapi-3", "/indian-api/v2/chandramasa", data)

    def find_samvat(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Find Samvat."""
        return self._c.post("astroapi-2", "/indian-api/v1/find-samvat",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def find_nakshatra(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Find Nakshatra."""
        return self._c.post("astroapi-1", "/indian-api/v2/find-nakshatra",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def find_surya_nakshatra(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Find Surya Nakshatra."""
        return self._c.post("astroapi-1", "/indian-api/v2/find-surya-nakshatra",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def find_tithi(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Find Tithi."""
        return self._c.post("astroapi-1", "/indian-api/v1/find-tithi",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def find_yoga(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Find Yoga."""
        return self._c.post("astroapi-1", "/indian-api/v2/find-yoga",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def find_karana(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Find Karana."""
        return self._c.post("astroapi-1", "/indian-api/v1/find-karana",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def find_ritu_and_anaya(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", sanskrit_sign: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Find Ritu And Anaya."""
        data = self._loc(day, month, year, place, lat, lon, tzone, lan)
        if sanskrit_sign is not None:
            data["sanskrit_sign"] = sanskrit_sign
        return self._c.post("astroapi-2", "/indian-api/v1/find-ritu-and-anaya", data)

    def auspicious_timings(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Auspicious Timings."""
        return self._c.post("astroapi-3", "/indian-api/v1/auspicious-timings",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def inauspicious_timings(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Inauspicious Timings."""
        return self._c.post("astroapi-3", "/indian-api/v1/inauspicious-timings",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def find_nivas_and_shool(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Find Nivas And Shool."""
        return self._c.post("astroapi-2", "/indian-api/v1/find-nivas-and-shool",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def other_calendars(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Other Calendars."""
        return self._c.post("astroapi-2", "/indian-api/v2/find-other-calendars-and-epoch",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def chandrashtama(
        self, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", sanskrit_sign: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Chandrashtama."""
        data = self._month_loc(month, year, place, lat, lon, tzone, lan)
        if sanskrit_sign is not None:
            data["sanskrit_sign"] = sanskrit_sign
        return self._c.post("astroapi-3", "/indian-api/v2/chandrashtama", data)

    def grah_gochar(
        self, planet: str, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", sanskrit_sign: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Grah Gochar for a given planet."""
        data = self._month_loc(month, year, place, lat, lon, tzone, lan)
        if sanskrit_sign is not None:
            data["sanskrit_sign"] = sanskrit_sign
        return self._c.post("astroapi-3", f"/indian-api/v2/grah-gochar/{planet}", data)

    def planet_nakshatra_transit(
        self, planet: str, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", pada_transit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Planet Nakshatra Transit."""
        data = self._month_loc(month, year, place, lat, lon, tzone, lan)
        if pada_transit is not None:
            data["pada_transit"] = pada_transit
        return self._c.post("astroapi-3", f"/indian-api/v2/planet-nakshatra-transit/{planet}", data)

    def planet_retrograde_transit(
        self, planet: str, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Planet Retrograde Transit."""
        return self._c.post("astroapi-3", f"/indian-api/v2/planet-retrograde-transit/{planet}",
                            self._month_loc(month, year, place, lat, lon, tzone, lan))

    def planet_combustion_transit(
        self, planet: str, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Planet Combustion Transit."""
        return self._c.post("astroapi-3", f"/indian-api/v2/planet-combustion-transit/{planet}",
                            self._month_loc(month, year, place, lat, lon, tzone, lan))

    def chandrabalam_and_tarabalam(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", sanskrit_sign: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Chandrabalam And Tarabalam."""
        data = self._loc(day, month, year, place, lat, lon, tzone, lan)
        if sanskrit_sign is not None:
            data["sanskrit_sign"] = sanskrit_sign
        return self._c.post("astroapi-2", "/indian-api/v2/find-chandrabalam-and-tarabalam", data)

    def panchak_rahita(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Panchak Rahita."""
        return self._c.post("astroapi-3", "/indian-api/v1/panchak-rahita",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def uday_lagna(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", sanskrit_sign: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Uday Lagna."""
        data = self._loc(day, month, year, place, lat, lon, tzone, lan)
        if sanskrit_sign is not None:
            data["sanskrit_sign"] = sanskrit_sign
        return self._c.post("astroapi-3", "/indian-api/v2/uday-lagna", data)

    def find_choghadiya(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Find Choghadiya."""
        return self._c.post("astroapi-2", "/indian-api/v1/find-choghadiya",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))

    def month_sunrise_sunset(
        self, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Month Sunrise-Sunset list."""
        return self._c.post("astroapi-8", "/indian-api/v1/month-sunrise-sunset-list", {
            "month": month, "year": year, "place": place,
            "lat": lat, "lon": lon, "tzone": tzone,
        })

    def month_nakshatra(
        self, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Month Nakshatra list."""
        return self._c.post("astroapi-8", "/indian-api/v1/month-nakshatra-list", {
            "month": month, "year": year, "place": place,
            "lat": lat, "lon": lon, "tzone": tzone,
        })

    def month_tithi(
        self, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Month Tithi list."""
        return self._c.post("astroapi-8", "/indian-api/v1/month-tithi-list", {
            "month": month, "year": year, "place": place,
            "lat": lat, "lon": lon, "tzone": tzone,
        })

    def month_surya_nakshatra(
        self, day: int, month: int, year: int,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Month Surya Nakshatra list."""
        return self._c.post("astroapi-8", "/indian-api/v1/month-surya-nakshatra-list",
                            self._loc(day, month, year, place, lat, lon, tzone, lan))
