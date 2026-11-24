"""Horoscope & Tarot endpoints (astroapi-5)."""

from typing import Any, Dict, Optional

from .client import BaseClient

HOST = "astroapi-5"


def _special_info(enabled: bool) -> Optional[int]:
    """The Chinese endpoints add ``special`` only for ``special_info=1``.

    ``True`` would be sent as "True", which the API ignores. ``None`` is left
    out of the form, so the default request is unchanged.
    """
    return 1 if enabled else None


class HoroscopeApi:
    """33 endpoints covering horoscopes, tarot, and miscellaneous readings."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    # ------------------------------------------------------------------ #
    # Horoscopes
    # ------------------------------------------------------------------ #

    def daily(
        self,
        sign: str,
        h_day: str,
        tzone: float,
        lan: str = "en",
        day: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Daily Horoscope.

        The reading is selected with ``h_day`` ('today', 'tomorrow', or
        'yesterday'). ``day``/``month``/``year`` are deprecated: the API
        ignores them and they are accepted only for backward compatibility.
        """
        return self._c.post(HOST, "/api/v5/daily-horoscope", {
            "sign": sign, "h_day": h_day, "tzone": tzone, "lan": lan,
        })

    def weekly(
        self,
        sign: str,
        week: str,
        tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Weekly Horoscope.

        ``week`` is a selector: 'current', 'prev', or 'next' (not a date).
        """
        return self._c.post(HOST, "/api/v5/weekly-horoscope", {
            "sign": sign, "week": week, "tzone": tzone, "lan": lan,
        })

    def monthly(
        self,
        sign: str,
        month: str,
        tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Monthly Horoscope.

        ``month`` is a selector: 'current', 'prev', or 'next' (not a calendar
        month number).
        """
        return self._c.post(HOST, "/api/v5/monthly-horoscope", {
            "sign": sign, "month": month, "tzone": tzone, "lan": lan,
        })

    def yearly(
        self,
        sign: str,
        year: str,
        tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Yearly Horoscope.

        ``year`` is a selector: 'current', 'prev', or 'next' (not a calendar
        year number).
        """
        return self._c.post(HOST, "/api/v5/yearly-horoscope", {
            "sign": sign, "year": year, "tzone": tzone, "lan": lan,
        })

    def chinese(
        self,
        sign: str,
        h_day: str,
        tzone: float,
        lan: str = "en",
        special_info: bool = False,
    ) -> Dict[str, Any]:
        """Chinese Horoscope (daily: ``h_day`` is 'today', 'tomorrow' or 'yesterday').

        ``data`` has ``sign``, ``date`` and ``prediction`` (growth, health,
        wealth, career, love, family, fortune). ``special_info=True`` adds
        ``data["special"]``; see :meth:`chinese_weekly`.
        """
        return self._c.post(HOST, "/api/v3/chinese-horoscope", {
            "sign": sign, "h_day": h_day, "tzone": tzone, "lan": lan,
            "special_info": _special_info(special_info),
        })

    def chinese_weekly(
        self,
        sign: str,
        week: str,
        tzone: float,
        lan: str = "en",
        special_info: bool = False,
    ) -> Dict[str, Any]:
        """Weekly Chinese Horoscope.

        ``sign`` is a Chinese animal sign (rat, ox, tiger, rabbit, dragon, snake,
        horse, goat, monkey, rooster, dog, pig). ``week`` is a selector:
        'current', 'prev', or 'next' (not a date). ``data`` has ``sign``,
        ``week`` (e.g. "08 Nov 2026 to 14 Nov 2026") and ``prediction``
        (growth, health, wealth, career, love, family, fortune).

        ``special_info=True`` adds ``data["special"]``: ``lucky_colors`` (two
        colours, each ``{"name", "hex"}``), ``horoscope_percentage`` (0-100 for
        growth, health, wealth, career, love, family and luck) and ``summary``
        (a short overview). The default leaves the response unchanged.
        """
        return self._c.post(HOST, "/api/v3/chinese-horoscope-weekly", {
            "sign": sign, "week": week, "tzone": tzone, "lan": lan,
            "special_info": _special_info(special_info),
        })

    def chinese_monthly(
        self,
        sign: str,
        month: str,
        tzone: float,
        lan: str = "en",
        special_info: bool = False,
    ) -> Dict[str, Any]:
        """Monthly Chinese Horoscope.

        ``month`` is a selector: 'current', 'prev', or 'next' (not a month
        number). ``data`` has ``sign``, ``month`` (e.g. "November 2026") and
        ``prediction``, shaped like :meth:`chinese_weekly`, as is
        ``special_info``.
        """
        return self._c.post(HOST, "/api/v3/chinese-horoscope-monthly", {
            "sign": sign, "month": month, "tzone": tzone, "lan": lan,
            "special_info": _special_info(special_info),
        })

    def chinese_yearly(
        self,
        sign: str,
        year: str,
        tzone: float,
        lan: str = "en",
        special_info: bool = False,
    ) -> Dict[str, Any]:
        """Yearly Chinese Horoscope.

        ``year`` is a selector: 'current', 'prev', or 'next' (not a calendar
        year). ``data`` has ``sign``, ``year`` and ``prediction``, shaped like
        :meth:`chinese_weekly`, as is ``special_info``.
        """
        return self._c.post(HOST, "/api/v3/chinese-horoscope-yearly", {
            "sign": sign, "year": year, "tzone": tzone, "lan": lan,
            "special_info": _special_info(special_info),
        })

    def chinese_yearly_top_signs(
        self,
        year: str,
        tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Top 3 Chinese signs of the year in each life area.

        There is no sign: the answer ranks all twelve animals. ``year`` is a
        selector: 'current', 'prev', or 'next' (not a calendar year).
        ``data`` has ``year`` (e.g. "2026") and ``areas``, a dict keyed by area
        (career, health, love, wealth) whose values are three
        ``{"rank", "sign", "reason"}`` entries sorted by rank (1 = best).
        A year without a ranking answers ``success`` 0, "Data not found.".
        """
        return self._c.post(HOST, "/api/v3/chinese-yearly-top-signs", {
            "year": year, "tzone": tzone, "lan": lan,
        })

    def numerology(
        self,
        number: int,
        day: int,
        month: int,
        year: int,
        tzone: float,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Numerology Horoscope."""
        return self._c.post(HOST, "/api/v2/numerology-horoscope", {
            "number": number, "day": day, "month": month, "year": year,
            "tzone": tzone, "lan": lan,
        })

    # ------------------------------------------------------------------ #
    # Tarot & Readings
    # ------------------------------------------------------------------ #

    def yes_or_no_tarot(self, lan: str = "en") -> Dict[str, Any]:
        """Yes or No Tarot."""
        return self._c.post(HOST, "/api/v2/yes-or-no-tarot", {"lan": lan})

    def daily_tarot(self, lan: str = "en") -> Dict[str, Any]:
        """Daily Tarot."""
        return self._c.post(HOST, "/api/v2/daily-tarot", {"lan": lan})

    def fortune_cookie(self, lan: str = "en") -> Dict[str, Any]:
        """Fortune Cookie."""
        return self._c.post(HOST, "/api/v2/fortune-cookie", {"lan": lan})

    def coffee_cup_reading(self, lan: str = "en") -> Dict[str, Any]:
        """Coffee Cup Reading."""
        return self._c.post(HOST, "/api/v2/coffee-cup-reading", {"lan": lan})

    def career_daily_reading(self, lan: str = "en") -> Dict[str, Any]:
        """Career Daily Reading."""
        return self._c.post(HOST, "/api/v3/career-daily-reading", {"lan": lan})

    def divine_angel_reading(self, lan: str = "en") -> Dict[str, Any]:
        """Divine Angel Reading."""
        return self._c.post(HOST, "/api/v3/divine-angel-reading", {"lan": lan})

    def divine_magic_reading(
        self, card_image: str, lan: str = "en"
    ) -> Dict[str, Any]:
        """Divine Magic Reading."""
        return self._c.post(HOST, "/api/v2/divine-magic-reading", {
            "card_image": card_image, "lan": lan,
        })

    def dream_come_true_reading(self, lan: str = "en") -> Dict[str, Any]:
        """Dream Come True Reading."""
        return self._c.post(HOST, "/api/v3/dream-come-true-reading", {"lan": lan})

    def egyptian_prediction(self, lan: str = "en") -> Dict[str, Any]:
        """Egyptian Prediction."""
        return self._c.post(HOST, "/api/v3/egyptian-prediction", {"lan": lan})

    def erotic_love_reading(self, lan: str = "en") -> Dict[str, Any]:
        """Erotic Love Reading."""
        return self._c.post(HOST, "/api/v3/erotic-love-reading", {"lan": lan})

    def ex_flame_reading(self, lan: str = "en") -> Dict[str, Any]:
        """Ex-Flame Reading."""
        return self._c.post(HOST, "/api/v3/ex-flame-reading", {"lan": lan})

    def flirt_love_reading(self, lan: str = "en") -> Dict[str, Any]:
        """Flirt Love Reading."""
        return self._c.post(HOST, "/api/v3/flirt-love-reading", {"lan": lan})

    def heartbreak_reading(
        self, card_image: str, lan: str = "en"
    ) -> Dict[str, Any]:
        """Heartbreak Reading."""
        return self._c.post(HOST, "/api/v2/heartbreak-reading", {
            "card_image": card_image, "lan": lan,
        })

    def in_depth_love_reading(self, lan: str = "en") -> Dict[str, Any]:
        """In-Depth Love Reading."""
        return self._c.post(HOST, "/api/v3/in-depth-love-reading", {"lan": lan})

    def know_your_friend_reading(self, lan: str = "en") -> Dict[str, Any]:
        """Know Your Friend Reading."""
        return self._c.post(HOST, "/api/v3/know-your-friend-reading", {"lan": lan})

    def love_compatibility(
        self, sign_1: str, sign_2: str, lan: str = "en"
    ) -> Dict[str, Any]:
        """Love Compatibility."""
        return self._c.post(HOST, "/api/v2/love-compatibility", {
            "sign_1": sign_1, "sign_2": sign_2, "lan": lan,
        })

    def love_triangle_reading(
        self, card_image: str, lan: str = "en"
    ) -> Dict[str, Any]:
        """Love Triangle Reading."""
        return self._c.post(HOST, "/api/v2/love-triangle-reading", {
            "card_image": card_image, "lan": lan,
        })

    def made_for_each_other(self, lan: str = "en") -> Dict[str, Any]:
        """Made For Each Other Reading."""
        return self._c.post(HOST, "/api/v3/made-for-each-other-or-not-reading", {"lan": lan})

    def power_life_reading(self, lan: str = "en") -> Dict[str, Any]:
        """Power Life Reading."""
        return self._c.post(HOST, "/api/v3/power-life-reading", {"lan": lan})

    def past_lives_connection(self, lan: str = "en") -> Dict[str, Any]:
        """Past Lives Connection Reading."""
        return self._c.post(HOST, "/api/v3/past-lives-connection-reading", {"lan": lan})

    def past_present_future(
        self, card_image: str, lan: str = "en"
    ) -> Dict[str, Any]:
        """Past-Present-Future Reading."""
        return self._c.post(HOST, "/api/v3/past-present-future-reading", {
            "card_image": card_image, "lan": lan,
        })

    def which_animal_are_you(
        self,
        full_name: str,
        day: int,
        month: int,
        year: int,
        lan: str = "en",
    ) -> Dict[str, Any]:
        """Which Animal Are You Reading."""
        return self._c.post(HOST, "/api/v2/which-animal-are-you-reading", {
            "full_name": full_name, "day": day, "month": month,
            "year": year, "lan": lan,
        })

    def wisdom_reading(
        self, card_image: str, lan: str = "en"
    ) -> Dict[str, Any]:
        """Wisdom Reading."""
        return self._c.post(HOST, "/api/v2/wisdom-reading", {
            "card_image": card_image, "lan": lan,
        })
