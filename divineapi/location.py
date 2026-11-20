"""Location API (geolocation.divineapi.com): place search, the timezone offset on a date, and the service health."""

from typing import Any, Dict, Optional

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
        in a zone with summer time it can differ by an hour, so get the
        offset for the birth date with :meth:`timezone` before using it as
        ``tzone``.
        """
        return self._c.post(HOST, "/location", {"place": place})

    def timezone(
        self,
        place_id: Optional[int] = None,
        *,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        timezone: Optional[str] = None,
        day: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        hour: Optional[int] = None,
        min: Optional[int] = None,
        sec: Optional[int] = None,
    ) -> Dict[str, Any]:
        """The UTC offset that applied at a place on a local date and time.

        It accounts for summer time (DST) and historical changes, so its
        ``timezone_value`` is the ``tzone`` to send for a birth date.

        The place is one of:

        - ``place_id`` from :meth:`search` (the documented input);
        - ``lat`` and ``lon``: the nearest known place is used;
        - ``timezone``: an IANA name such as ``"America/New_York"``.

        Giving none or several raises ``ValueError``; with several, the API
        would silently use ``place_id``.

        The local date and time: ``day``, ``month``, ``year``, ``hour`` and
        ``min`` together (``sec`` defaults to 0), or none of them for the
        current time.

        ``data`` holds ``place`` (``None`` for a timezone name), ``timezone``,
        ``local_datetime``, ``utc_datetime``, ``timezone_value`` (decimal
        hours, e.g. 5.5 or -4), ``utc_offset`` (e.g. ``"+05:30"``),
        ``is_dst`` and ``ambiguous``.

        - ``ambiguous`` is true when the local time happened twice because
          the clocks went back. The first of the two is used.
        - A local time skipped when the clocks went forward raises
          ``ValidationError`` (HTTP 422).
        - An unknown ``place_id`` raises ``NotFoundError`` (HTTP 404).
        """
        given = [
            name for name, present in (
                ("place_id", place_id is not None),
                ("lat/lon", lat is not None or lon is not None),
                ("timezone", bool(timezone and str(timezone).strip())),
            ) if present
        ]
        if len(given) != 1:
            raise ValueError(
                "Give exactly one of place_id, lat and lon, or timezone"
                + (f" (got {' and '.join(given)})" if given else "")
            )
        fields = {
            "place_id": place_id, "lat": lat, "lon": lon,
            "timezone": timezone.strip() if isinstance(timezone, str) else timezone,
            "day": day, "month": month, "year": year,
            "hour": hour, "min": min, "sec": sec,
        }
        return self._c.post(HOST, "/timezone", {k: v for k, v in fields.items() if v is not None})

    def health(self) -> Dict[str, Any]:
        """Check that the Location API service is up (``GET /health``).

        Needs no credentials and uses no credits. When healthy it returns
        ``{"status": "success", ..., "data": {"service": "location-api",
        "status": "ok"}}``. When the service is down it raises
        ``ServerError`` or ``NetworkError``.
        """
        return self._c.get(HOST, "/health")
