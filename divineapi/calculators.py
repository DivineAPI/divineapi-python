"""Calculator endpoints (astroapi-7)."""

from typing import Any, Dict

from .client import BaseClient

HOST = "astroapi-7"


class CalculatorApi:
    """Fun calculator endpoints (FLAMES, Love Calculator)."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    def flames(self, your_name: str, partner_name: str) -> Dict[str, Any]:
        """FLAMES Calculator."""
        return self._c.post(HOST, "/calculator/v1/flames-calculator", {
            "your_name": your_name, "partner_name": partner_name,
        })

    def love_calculator(
        self,
        your_name: str,
        partner_name: str,
        your_gender: str,
        partner_gender: str,
    ) -> Dict[str, Any]:
        """Love Calculator."""
        return self._c.post(HOST, "/calculator/v1/love-calculator", {
            "your_name": your_name, "partner_name": partner_name,
            "your_gender": your_gender, "partner_gender": partner_gender,
        })
