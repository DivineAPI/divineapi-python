"""Indian API - Festival endpoints (astroapi-3)."""

from typing import Any, Dict, Optional

from ..client import BaseClient

HOST = "astroapi-3"

# Hindu months with their URL slugs
_HINDU_MONTHS = [
    "margashirsh", "ashvina", "magha", "phalguna", "chaitra",
    "vaishakha", "jyeshtha", "ashada", "shraavana", "bhadrapada",
    "kartika", "pausha",
]


class FestivalApi:
    """Festival endpoints (Hindu month festivals, English calendar, date-specific, festival-specific)."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    # ------------------------------------------------------------------ #
    # Helper
    # ------------------------------------------------------------------ #

    def _festival_loc(
        self, year: int, place: str, lat: float, lon: float, tzone: float,
        **extra: Any,
    ) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "year": year, "place": place,
            "lat": lat, "lon": lon, "tzone": tzone,
        }
        d.update(extra)
        return d

    # ------------------------------------------------------------------ #
    # Hindu month festivals (12 endpoints)
    # ------------------------------------------------------------------ #

    def _hindu_month(
        self, month_slug: str,
        year: int, place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        return self._c.post(HOST, f"/indian-api/v2/{month_slug}-festivals",
                            self._festival_loc(year, place, lat, lon, tzone))

    def margashirsh_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("margashirsh", year, place, lat, lon, tzone)

    def ashvina_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("ashvina", year, place, lat, lon, tzone)

    def magha_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("magha", year, place, lat, lon, tzone)

    def phalguna_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("phalguna", year, place, lat, lon, tzone)

    def chaitra_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("chaitra", year, place, lat, lon, tzone)

    def vaishakha_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("vaishakha", year, place, lat, lon, tzone)

    def jyeshtha_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("jyeshtha", year, place, lat, lon, tzone)

    def ashada_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("ashada", year, place, lat, lon, tzone)

    def shraavana_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("shraavana", year, place, lat, lon, tzone)

    def bhadrapada_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("bhadrapada", year, place, lat, lon, tzone)

    def kartika_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("kartika", year, place, lat, lon, tzone)

    def pausha_festivals(self, year: int, place: str, lat: float, lon: float, tzone: float) -> Dict[str, Any]:
        return self._hindu_month("pausha", year, place, lat, lon, tzone)

    # ------------------------------------------------------------------ #
    # Other festival endpoints
    # ------------------------------------------------------------------ #

    def english_calendar(
        self, year: int, month: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """English Calendar Festivals."""
        data = self._festival_loc(year, place, lat, lon, tzone)
        data["month"] = month
        return self._c.post(HOST, "/indian-api/v1/english-calendar-festivals", data)

    def date_specific(
        self, year: int, month: int, day: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Date Specific Festivals."""
        data = self._festival_loc(year, place, lat, lon, tzone)
        data["month"] = month
        data["day"] = day
        return self._c.post(HOST, "/indian-api/v1/date-specific-festivals", data)

    def find_festival(
        self, festival: str, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Festival Specific lookup."""
        data = self._festival_loc(year, place, lat, lon, tzone)
        data["festival"] = festival
        return self._c.post(HOST, "/indian-api/v1/find-festival", data)

    def malayalam_festivals(
        self, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Malayalam (Kerala) Festivals for a year."""
        return self._c.post(HOST, "/indian-api/v1/malayalam-festivals",
                            self._festival_loc(year, place, lat, lon, tzone))

    def tamil_festivals(
        self, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Tamil Festivals for a year."""
        return self._c.post(HOST, "/indian-api/v1/tamil-festivals",
                            self._festival_loc(year, place, lat, lon, tzone))

    def sankranti_festivals(
        self, year: int,
        place: str, lat: float, lon: float, tzone: float,
    ) -> Dict[str, Any]:
        """Sankranti Festivals for a year."""
        return self._c.post(HOST, "/indian-api/v1/sankranti-festivals",
                            self._festival_loc(year, place, lat, lon, tzone))
