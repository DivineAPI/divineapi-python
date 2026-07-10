"""DivineAPI Python SDK.

Usage::

    from divineapi import DivineApi

    client = DivineApi(api_key="your-api-key", auth_token="your-bearer-token")
    result = client.horoscope.daily(sign="aries", h_day="today", tzone=5.5)
    print(result)
"""

from typing import Any

from .calculators import CalculatorApi
from .client import BaseClient
from .exceptions import (
    AuthenticationError,
    DivineApiError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .horoscope import HoroscopeApi
from .indian import IndianApi
from .lifestyle import LifestyleApi
from .numerology import NumerologyApi
from .pdf import PdfReportApi
from .western import WesternApi

__version__ = "1.4.0"

__all__ = [
    "DivineApi",
    "DivineApiError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "NotFoundError",
    "ServerError",
    "NetworkError",
]


class DivineApi:
    """Top-level client for the Divine API.

    Args:
        api_key: Your Divine API key (sent as ``api_key`` in every request body).
        auth_token: Bearer token for the ``Authorization`` header.
        timeout: HTTP request timeout in seconds (default 30).
        max_retries: Number of retry attempts on transient failures (default 2).

    Example::

        client = DivineApi(api_key="...", auth_token="...")

        # Horoscope & Tarot
        client.horoscope.daily(sign="aries", h_day="today", tzone=5.5)

        # Indian Panchang
        client.indian.panchang.find_panchang(
            day=10, month=3, year=2024,
            place="Delhi", lat=28.6, lon=77.2, tzone=5.5,
        )

        # Indian Kundli
        client.indian.kundli.basic_astro_details(
            full_name="John", day=1, month=1, year=1990,
            hour=10, min=30, sec=0, gender="male",
            place="Mumbai", lat=19.07, lon=72.87, tzone=5.5,
        )

        # Indian Match Making
        client.indian.match_making.ashtakoot_milan(
            p1_full_name="A", p1_day=1, p1_month=1, p1_year=1990,
            p1_hour=10, p1_min=0, p1_sec=0, p1_gender="male",
            p1_place="Delhi", p1_lat=28.6, p1_lon=77.2, p1_tzone=5.5,
            p2_full_name="B", p2_day=5, p2_month=5, p2_year=1992,
            p2_hour=14, p2_min=0, p2_sec=0, p2_gender="female",
            p2_place="Mumbai", p2_lat=19.07, p2_lon=72.87, p2_tzone=5.5,
        )

        # Western Natal
        client.western.natal.planetary_positions(
            full_name="Jane", day=15, month=6, year=1995,
            hour=8, min=0, sec=0, gender="female",
            place="New York", lat=40.71, lon=-74.0, tzone=-5.0,
        )

        # Numerology
        client.numerology.core_numbers(
            full_name="John Doe", day=1, month=1, year=1990,
            gender="male", method="pythagorean",
        )

        # PDF Reports
        client.pdf.kundali_sampoorna(
            full_name="John", day=1, month=1, year=1990,
            hour=10, min=30, sec=0, gender="male",
            place="Mumbai", lat=19.07, lon=72.87, tzone=5.5,
            company_name="MyCompany", company_url="https://example.com",
            company_email="hello@example.com", company_bio="We do astrology.",
            logo_url="https://example.com/logo.png", footer_text="(c) MyCompany",
        )
    """

    def __init__(
        self,
        api_key: str,
        auth_token: str,
        timeout: int = 30,
        max_retries: int = 2,
    ) -> None:
        self._client = BaseClient(
            api_key=api_key,
            auth_token=auth_token,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.horoscope = HoroscopeApi(self._client)
        self.indian = IndianApi(self._client)
        self.western = WesternApi(self._client)
        self.pdf = PdfReportApi(self._client)
        self.numerology = NumerologyApi(self._client)
        self.lifestyle = LifestyleApi(self._client)
        self.calculators = CalculatorApi(self._client)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._client.close()

    def __enter__(self) -> "DivineApi":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
