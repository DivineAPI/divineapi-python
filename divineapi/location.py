"""Location API (geolocation.divineapi.com): place name -> coordinates and timezone."""

from typing import Any, Dict

from .client import BaseClient

HOST = "geolocation"


class LocationApi:
    """Location endpoints."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    def search(self, place: str) -> Dict[str, Any]:
        """Search for a place by name (at least 3 characters).

        Returns up to 10 matches, largest population first, under
        ``data["results"]``: each has ``place_id``, ``name``, ``full_name``,
        ``country``, ``admin1``, ``latitude``, ``longitude``, ``timezone``
        (IANA name), ``timezone_value`` and ``population``. The response
        also carries the GeoNames ``attribution`` (CC BY 4.0).

        ``timezone_value`` is the zone's UTC offset today. For a birth date
        in a zone with summer time it can differ by an hour, so compute the
        offset for the birth date from ``timezone`` before using it as
        ``tzone``.
        """
        return self._c.post(HOST, "/location", {"place": place})
