"""Western API - Prenatal endpoints (astroapi-8)."""

from typing import Any, Dict

from ..client import BaseClient

HOST = "astroapi-8"


class PrenatalApi:
    """Prenatal (pre-birth) chart endpoints."""

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

    def prenatal_list(self, prenatal_type: str, **kw: Any) -> Dict[str, Any]:
        """Prenatal List."""
        kw["prenatal_type"] = prenatal_type
        return self._c.post(HOST, "/western-api/v1/prenatal-list", self._birth(**kw))

    def prenatal_details(self, prenatal_key: str, **kw: Any) -> Dict[str, Any]:
        """Prenatal Details."""
        kw["prenatal_key"] = prenatal_key
        return self._c.post(HOST, "/western-api/v1/prenatal-details", self._birth(**kw))
