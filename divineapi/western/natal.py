"""Western API - Natal endpoints (astroapi-4 and astroapi-8)."""

from typing import Any, Dict

from ..client import BaseClient
from ._house_system import resolve_house_system


class NatalApi:
    """Natal (birth chart) endpoints for Western astrology."""

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
            "lan": lan, "house_system": resolve_house_system(house_system),
        }
        d.update(extra)
        return d

    def _post4(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post("astroapi-4", path, self._birth(**kw))

    def _post8(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post("astroapi-8", path, self._birth(**kw))

    # ------------------------------------------------------------------ #
    # astroapi-4 endpoints (10)
    # ------------------------------------------------------------------ #

    def planetary_positions(self, **kw: Any) -> Dict[str, Any]:
        """Natal Planetary Positions."""
        return self._post4("/western-api/v1/planetary-positions", **kw)

    def house_cusps(self, **kw: Any) -> Dict[str, Any]:
        """Natal House Cusps."""
        return self._post4("/western-api/v1/house-cusps", **kw)

    def aspect_table(self, **kw: Any) -> Dict[str, Any]:
        """Natal Aspect Table."""
        return self._post4("/western-api/v2/aspect-table", **kw)

    def natal_wheel_chart(self, **kw: Any) -> Dict[str, Any]:
        """Natal Wheel Chart (pass chart styling via **kw)."""
        return self._post8("/western-api/v2/natal-wheel-chart", **kw)

    def general_sign_report(self, planet: str, **kw: Any) -> Dict[str, Any]:
        """General Sign Report for a planet."""
        return self._post4(f"/western-api/v1/general-sign-report/{planet}", **kw)

    def general_house_report(self, planet: str, **kw: Any) -> Dict[str, Any]:
        """General House Report for a planet."""
        return self._post4(f"/western-api/v1/general-house-report/{planet}", **kw)

    def moon_phases(self, **kw: Any) -> Dict[str, Any]:
        """Moon Phases."""
        return self._post4("/western-api/v1/moon-phases", **kw)

    def ascendant_report(self, **kw: Any) -> Dict[str, Any]:
        """Ascendant Report."""
        return self._post4("/western-api/v2/ascendant-report", **kw)

    def moon_phase_calendar(self, **kw: Any) -> Dict[str, Any]:
        """Moon Phase Calendar."""
        return self._post4("/western-api/v1/moon-phase-calendar", **kw)

    def natal_insights(self, **kw: Any) -> Dict[str, Any]:
        """Natal Insights."""
        return self._post4("/western-api/v1/natal-insights", **kw)

    # ------------------------------------------------------------------ #
    # astroapi-8 endpoints (11)
    # ------------------------------------------------------------------ #

    def arabic_lots(self, **kw: Any) -> Dict[str, Any]:
        """Arabic Lots."""
        return self._post8("/western-api/v1/arabic-lots", **kw)

    def asteroid_positions(self, **kw: Any) -> Dict[str, Any]:
        """Asteroid Positions."""
        return self._post8("/western-api/v1/asteroid-positions", **kw)

    def fixed_stars_list(self) -> Dict[str, Any]:
        """Fixed Stars List (api_key only)."""
        return self._c.post("astroapi-8", "/western-api/v1/fixed-stars-list", {})

    def fixed_stars_details(self, star_list: str, **kw: Any) -> Dict[str, Any]:
        """Fixed Stars Details."""
        kw["star_list"] = star_list
        return self._post8("/western-api/v1/fixed-stars-details", **kw)

    def planetary_midpoints(self, **kw: Any) -> Dict[str, Any]:
        """Planetary Midpoints."""
        return self._post8("/western-api/v1/planetary-midpoints", **kw)

    def eclipse(self, **kw: Any) -> Dict[str, Any]:
        """Eclipse data."""
        return self._post8("/western-api/v1/eclipse", **kw)

    def declinations_parallels(self, **kw: Any) -> Dict[str, Any]:
        """Declinations Parallels."""
        return self._post8("/western-api/v1/declinations-parallels", **kw)

    def aspect_patterns(self, **kw: Any) -> Dict[str, Any]:
        """Aspect Patterns."""
        return self._post8("/western-api/v1/aspect-patterns", **kw)

    def chart_shape(self, **kw: Any) -> Dict[str, Any]:
        """Chart Shape."""
        return self._post8("/western-api/v1/chart-shape", **kw)

    def other_minor_bodies(self, **kw: Any) -> Dict[str, Any]:
        """Other Minor Bodies."""
        return self._post8("/western-api/v1/other-minor-bodies", **kw)

    def dominants(self, method: str, **kw: Any) -> Dict[str, Any]:
        """Dominants with method."""
        kw["method"] = method
        return self._post8("/western-api/v1/dominants", **kw)

    def persona_chart(self, persona_planet: str, **kw: Any) -> Dict[str, Any]:
        """Persona Chart for a chosen natal planet.

        Casts the full chart for the exact moment - within the first year of
        life - that the transiting Sun reaches the natal degree of
        ``persona_planet`` (sun, moon, mercury, venus, mars, jupiter, saturn,
        uranus, neptune or pluto; case-insensitive).

        Returns ``persona_planet``, ``persona_datetime``,
        ``planetary_positions``, ``house_cusps``, ``aspect_table`` and
        ``persona_natal_aspect``.

        Optional keyword arguments are passed straight through, including
        ``node_type`` (meannode | truenode), ``output_include``, the
        chart-appearance options (``graphic_layout``, ``filter_effect``,
        ``element_color`` and friends) and the aspect options
        (``aspects_type``, ``aspect_orbs_type``, ``aspect_orbs_value``).

        ``output_include`` controls response size and defaults to ``raw_data``
        server-side (~21 KB, data only). Image tokens are large - roughly
        0.5 MB per SVG, and ``all`` returns around 4.3 MB.

        Note ``persona_planet="sun"`` is accepted but reduces to a
        one-year-later Solar Return chart.
        """
        kw["persona_planet"] = persona_planet
        return self._post8("/western-api/v1/persona-chart", **kw)
