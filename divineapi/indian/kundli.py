"""Indian API - Kundli endpoints (astroapi-3)."""

from typing import Any, Dict, Optional

from ..client import BaseClient

HOST = "astroapi-3"


class KundliApi:
    """Kundli / birth-chart endpoints."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    # ------------------------------------------------------------------ #
    # Common birth-data payload builder
    # ------------------------------------------------------------------ #

    @staticmethod
    def _birth(
        full_name: str, day: int, month: int, year: int,
        hour: int, min: int, sec: int, gender: str,
        place: str, lat: float, lon: float, tzone: float,
        lan: str = "en", **extra: Any,
    ) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "full_name": full_name, "day": day, "month": month, "year": year,
            "hour": hour, "min": min, "sec": sec, "gender": gender,
            "place": place, "lat": lat, "lon": lon, "tzone": tzone,
            "lan": lan,
        }
        d.update(extra)
        return d

    # Shorthand so callers can pass **kwargs
    def _post_birth(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post(HOST, path, self._birth(**kw))

    # ------------------------------------------------------------------ #
    # Jaimini (4 endpoints)
    # ------------------------------------------------------------------ #

    def jaimini_planetary_positions(self, **kw: Any) -> Dict[str, Any]:
        """Jaimini Planetary Positions."""
        return self._post_birth("/indian-api/v1/jaimini-astrology/planetary-positions", **kw)

    def jaimini_padas(self, **kw: Any) -> Dict[str, Any]:
        """Jaimini Padas."""
        return self._post_birth("/indian-api/v2/jaimini-astrology/padas", **kw)

    def jaimini_karakamsha_lagna(self, **kw: Any) -> Dict[str, Any]:
        """Jaimini Karakamsha Lagna."""
        return self._post_birth("/indian-api/v1/jaimini-astrology/karakamsha-lagna", **kw)

    def jaimini_chara_dasha(self, **kw: Any) -> Dict[str, Any]:
        """Jaimini Chara Dasha."""
        return self._post_birth("/indian-api/v2/jaimini-astrology/chara-dasha", **kw)

    # ------------------------------------------------------------------ #
    # Sub Planets (2 endpoints)
    # ------------------------------------------------------------------ #

    def sub_planet_positions(self, **kw: Any) -> Dict[str, Any]:
        """Sub Planet Positions."""
        return self._post_birth("/indian-api/v1/sub-planet-positions", **kw)

    def sub_planet_chart(self, **kw: Any) -> Dict[str, Any]:
        """Sub Planet Chart (supports chart styling params via **kw)."""
        return self._post_birth("/indian-api/v2/sub-planet-chart", **kw)

    # ------------------------------------------------------------------ #
    # KP (5 endpoints)
    # ------------------------------------------------------------------ #

    def kp_planetary_positions(self, **kw: Any) -> Dict[str, Any]:
        """KP Planetary Positions."""
        return self._post_birth("/indian-api/v1/kp/planetary-positions", **kw)

    def kp_cuspal(self, **kw: Any) -> Dict[str, Any]:
        """KP Cuspal."""
        return self._post_birth("/indian-api/v2/kp/cuspal", **kw)

    def kp_planetary_sub(self, **kw: Any) -> Dict[str, Any]:
        """KP Planetary Sub."""
        return self._post_birth("/indian-api/v1/kp/planetary-sub", **kw)

    def kp_planetary_cuspal_significator_table(self, **kw: Any) -> Dict[str, Any]:
        """KP Planetary Cuspal Significator Table."""
        return self._post_birth("/indian-api/v2/kp/planetary-cuspal-significator-table", **kw)

    def kp_cuspal_sub(self, **kw: Any) -> Dict[str, Any]:
        """KP Cuspal Sub."""
        return self._post_birth("/indian-api/v1/kp/cuspal-sub", **kw)

    # ------------------------------------------------------------------ #
    # Kundali Transit (2 endpoints)
    # ------------------------------------------------------------------ #

    def kundli_transit_ascendant(self, **kw: Any) -> Dict[str, Any]:
        """Kundali Transit Ascendant (pass transit params + chart styling via **kw)."""
        return self._post_birth("/indian-api/v1/kundli-transit/ascendant", **kw)

    def kundli_transit_moon(self, **kw: Any) -> Dict[str, Any]:
        """Kundali Transit Moon (pass transit params + chart styling via **kw)."""
        return self._post_birth("/indian-api/v1/kundli-transit/moon", **kw)

    # ------------------------------------------------------------------ #
    # Bhinnashtakvarga (3 endpoints)
    # ------------------------------------------------------------------ #

    def bhinnashtakvarga_ashtakvarga(self, **kw: Any) -> Dict[str, Any]:
        """Bhinnashtakvarga Ashtakvarga."""
        return self._post_birth("/indian-api/v1/bhinnashtakvarga/ashtakvarga", **kw)

    def bhinnashtakvarga_sarvashtakavarga(self, chart: str, **kw: Any) -> Dict[str, Any]:
        """Bhinnashtakvarga Sarvashtakavarga for a given chart."""
        return self._post_birth(f"/indian-api/v1/bhinnashtakvarga/sarvashtakavarga/{chart}", **kw)

    def bhinnashtakvarga_prasthara_chakra(self, **kw: Any) -> Dict[str, Any]:
        """Bhinnashtakvarga Prasthara Chakra."""
        return self._post_birth("/indian-api/v1/bhinnashtakvarga/prasthara-chakra", **kw)

    # ------------------------------------------------------------------ #
    # Dasha Analysis (3 endpoints - different params, no birth data)
    # ------------------------------------------------------------------ #

    def maha_dasha_analysis(
        self, maha_dasha: str, lan: str = "en",
    ) -> Dict[str, Any]:
        """Maha Dasha Analysis."""
        return self._c.post(HOST, "/indian-api/v1/maha-dasha-analysis", {
            "maha_dasha": maha_dasha, "lan": lan,
        })

    def antar_dasha_analysis(
        self, maha_dasha: str, antar_dasha: str, lan: str = "en",
    ) -> Dict[str, Any]:
        """Antar Dasha Analysis."""
        return self._c.post(HOST, "/indian-api/v1/antar-dasha-analysis", {
            "maha_dasha": maha_dasha, "antar_dasha": antar_dasha, "lan": lan,
        })

    def pratyantar_dasha_analysis(
        self, maha_dasha: str, antar_dasha: str, pratyantar_dasha: str,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Pratyantar Dasha Analysis."""
        return self._c.post(HOST, "/indian-api/v1/pratyantar-dasha-analysis", {
            "maha_dasha": maha_dasha, "antar_dasha": antar_dasha,
            "pratyantar_dasha": pratyantar_dasha, "lan": lan,
        })

    # ------------------------------------------------------------------ #
    # General Kundli endpoints (birth-data based)
    # ------------------------------------------------------------------ #

    def basic_astro_details(self, **kw: Any) -> Dict[str, Any]:
        """Basic Astro Details."""
        return self._post_birth("/indian-api/v3/basic-astro-details", **kw)

    def planetary_positions(self, **kw: Any) -> Dict[str, Any]:
        """Planetary Positions."""
        return self._post_birth("/indian-api/v2/planetary-positions", **kw)

    def horoscope_chart(self, chart_id: str, **kw: Any) -> Dict[str, Any]:
        """Horoscope Chart (pass chart styling via **kw)."""
        return self._post_birth(f"/indian-api/v1/horoscope-chart/{chart_id}", **kw)

    def vimshottari_dasha(self, dasha_type: Optional[str] = None, **kw: Any) -> Dict[str, Any]:
        """Vimshottari Dasha."""
        if dasha_type is not None:
            kw["dasha_type"] = dasha_type
        return self._post_birth("/indian-api/v1/vimshottari-dasha", **kw)

    def kaal_sarpa_yoga(self, **kw: Any) -> Dict[str, Any]:
        """Kaal Sarpa Dosha."""
        return self._post_birth("/indian-api/v1/kaal-sarpa-yoga", **kw)

    def manglik_dosha(self, **kw: Any) -> Dict[str, Any]:
        """Manglik Dosha."""
        return self._post_birth("/indian-api/v2/manglik-dosha", **kw)

    def ascendant_report(self, **kw: Any) -> Dict[str, Any]:
        """Ascendant Report."""
        return self._post_birth("/indian-api/v2/ascendant-report", **kw)

    def composite_friendship(self, **kw: Any) -> Dict[str, Any]:
        """Composite Friendship."""
        return self._post_birth("/indian-api/v1/composite-friendship", **kw)

    def bhava_kundli(self, chart_id: str, **kw: Any) -> Dict[str, Any]:
        """Bhava Kundli (pass chart styling via **kw)."""
        return self._post_birth(f"/indian-api/v1/bhava-kundli/{chart_id}", **kw)

    def sadhe_sati(self, **kw: Any) -> Dict[str, Any]:
        """Sadhe Sati."""
        return self._post_birth("/indian-api/v3/sadhe-sati", **kw)

    def ghata_chakra(self, **kw: Any) -> Dict[str, Any]:
        """Ghata Chakra."""
        return self._post_birth("/indian-api/v1/ghata-chakra", **kw)

    def shadbala(self, **kw: Any) -> Dict[str, Any]:
        """Shadbala."""
        return self._post_birth("/indian-api/v2/shadbala", **kw)

    def gemstone_suggestion(self, **kw: Any) -> Dict[str, Any]:
        """Gemstone Suggestions."""
        return self._post_birth("/indian-api/v2/gemstone-suggestion", **kw)

    def yogini_dasha(self, **kw: Any) -> Dict[str, Any]:
        """Yogini Dasha."""
        return self._post_birth("/indian-api/v2/yogini-dasha", **kw)

    def kaal_chakra_dasha(self, **kw: Any) -> Dict[str, Any]:
        """Kaal Chakra Dasha."""
        return self._post_birth("/indian-api/v1/kaal-chakra-dasha", **kw)

    def yogas(self, **kw: Any) -> Dict[str, Any]:
        """Yogas."""
        return self._post_birth("/indian-api/v2/yogas", **kw)

    def pitra_dosha(self, **kw: Any) -> Dict[str, Any]:
        """Pitra Dosha."""
        return self._post_birth("/indian-api/v1/pitra-dosha", **kw)

    def planet_analysis(self, analysis_planet: str, **kw: Any) -> Dict[str, Any]:
        """Planet Analysis for a given planet."""
        kw["analysis_planet"] = analysis_planet
        return self._post_birth("/indian-api/v2/planet-analysis", **kw)

    def sudarshana_chakra(self, **kw: Any) -> Dict[str, Any]:
        """Sudarshana Chakra."""
        return self._post_birth("/indian-api/v1/sudarshana-chakra", **kw)

    # ------------------------------------------------------------------ #
    # Lal Kitab (16 endpoints)
    # ------------------------------------------------------------------ #

    def lal_kitab_planetary_positions(self, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Planetary Positions."""
        return self._post_birth("/indian-api/v1/lal-kitab/planetary-positions", **kw)

    def lal_kitab_horoscope_chart(self, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Horoscope Chart."""
        return self._post_birth("/indian-api/v1/lal-kitab/horoscope-chart", **kw)

    def lal_kitab_house_position(self, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab House Position."""
        return self._post_birth("/indian-api/v1/lal-kitab/house-position", **kw)

    def lal_kitab_conjunctions(self, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Conjunctions."""
        return self._post_birth("/indian-api/v1/lal-kitab/conjunctions", **kw)

    def lal_kitab_teva(self, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Teva."""
        return self._post_birth("/indian-api/v1/lal-kitab/teva", **kw)

    def lal_kitab_planet_analysis(self, analysis_planet: str, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Planet Analysis for a given planet.

        analysis_planet: sun, moon, mars, mercury, jupiter, venus, saturn,
        rahu or ketu.
        """
        kw["analysis_planet"] = analysis_planet
        return self._post_birth("/indian-api/v1/lal-kitab/planet-analysis", **kw)

    def lal_kitab_dasha(self, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Dasha."""
        return self._post_birth("/indian-api/v1/lal-kitab/dasha", **kw)

    def lal_kitab_planet_types(self, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Planet Types."""
        return self._post_birth("/indian-api/v1/lal-kitab/planet-types", **kw)

    def lal_kitab_mahadasha_content(
        self, maha_dasha: str, lan: str = "en",
    ) -> Dict[str, Any]:
        """Lal Kitab Mahadasha Content (no birth data needed)."""
        return self._c.post(HOST, "/indian-api/v1/lal-kitab/mahadasha-content", {
            "maha_dasha": maha_dasha, "lan": lan,
        })

    def lal_kitab_antardasha_content(
        self, maha_dasha: str, antar_dasha: str, lan: str = "en",
    ) -> Dict[str, Any]:
        """Lal Kitab Antardasha Content (no birth data needed).

        The antar_dasha must be valid for the chosen maha_dasha; the API
        lists the valid values on mismatch.
        """
        return self._c.post(HOST, "/indian-api/v1/lal-kitab/antardasha-content", {
            "maha_dasha": maha_dasha, "antar_dasha": antar_dasha, "lan": lan,
        })

    def lal_kitab_debts(self, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Debts."""
        return self._post_birth("/indian-api/v1/lal-kitab/debts", **kw)

    def lal_kitab_house_signification(self, house_no: int, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab House Signification for a given house (1-12)."""
        kw["house_no"] = house_no
        return self._post_birth("/indian-api/v1/lal-kitab/house-signification", **kw)

    def lal_kitab_varshphal_varsha_pravesh(self, varshphal_year: int, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Varshphal Varsha Pravesh for the given year."""
        kw["varshphal_year"] = varshphal_year
        return self._post_birth("/indian-api/v1/lal-kitab/varshphal/varsha-pravesh", **kw)

    def lal_kitab_varshphal_planetary_positions(self, varshphal_year: int, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Varshphal Planetary Positions for the given year."""
        kw["varshphal_year"] = varshphal_year
        return self._post_birth("/indian-api/v1/lal-kitab/varshphal/planetary-positions", **kw)

    def lal_kitab_varshphal_muntha(self, varshphal_year: int, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Varshphal Muntha for the given year."""
        kw["varshphal_year"] = varshphal_year
        return self._post_birth("/indian-api/v1/lal-kitab/varshphal/muntha", **kw)

    def lal_kitab_varshphal_chart(self, varshphal_year: int, **kw: Any) -> Dict[str, Any]:
        """Lal Kitab Varshphal Chart for the given year."""
        kw["varshphal_year"] = varshphal_year
        return self._post_birth("/indian-api/v1/lal-kitab/varshphal/chart", **kw)

    # ------------------------------------------------------------------ #
    # Additional Kundli Analysis (6 endpoints)
    # ------------------------------------------------------------------ #

    def vargottama_planets(self, **kw: Any) -> Dict[str, Any]:
        """Vargottama Planets."""
        return self._post_birth("/indian-api/v1/vargottama-planets", **kw)

    def bhav_bala(self, **kw: Any) -> Dict[str, Any]:
        """Bhav Bala."""
        return self._post_birth("/indian-api/v1/bhav-bala", **kw)

    def shani_ashtam_shani(self, **kw: Any) -> Dict[str, Any]:
        """Shani Ashtam Shani."""
        return self._post_birth("/indian-api/v1/shani-ashtam-shani", **kw)

    def bhava_analysis(self, **kw: Any) -> Dict[str, Any]:
        """Bhava Analysis."""
        return self._post_birth("/indian-api/v1/bhava-analysis", **kw)

    def bhava_group_predictions(self, **kw: Any) -> Dict[str, Any]:
        """Bhava Group Predictions."""
        return self._post_birth("/indian-api/v1/bhava-group-predictions", **kw)

    def planet_remedies(self, analysis_planet: str, **kw: Any) -> Dict[str, Any]:
        """Planet Remedies for a given planet.

        analysis_planet: sun, moon, mars, mercury, jupiter, venus, saturn,
        rahu or ketu.
        """
        kw["analysis_planet"] = analysis_planet
        return self._post_birth("/indian-api/v1/planet-remedies", **kw)

    def rudraksha_suggestion(self, **kw: Any) -> Dict[str, Any]:
        """Rudraksh Suggestion."""
        return self._post_birth("/indian-api/v1/rudraksha-suggestion", **kw)
