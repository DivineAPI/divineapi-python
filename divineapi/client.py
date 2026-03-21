"""Base HTTP client for the DivineAPI SDK."""

from typing import Any, Dict, Optional

import requests

from .exceptions import (
    AuthenticationError,
    DivineApiError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)

# Host mapping
HOSTS = {
    "astroapi-1": "https://astroapi-1.divineapi.com",
    "astroapi-2": "https://astroapi-2.divineapi.com",
    "astroapi-3": "https://astroapi-3.divineapi.com",
    "astroapi-4": "https://astroapi-4.divineapi.com",
    "astroapi-5": "https://astroapi-5.divineapi.com",
    "astroapi-7": "https://astroapi-7.divineapi.com",
    "astroapi-8": "https://astroapi-8.divineapi.com",
    "pdf": "https://pdf.divineapi.com",
}


class BaseClient:
    """Low-level HTTP client that handles auth, requests, and error mapping."""

    def __init__(
        self,
        api_key: str,
        auth_token: str,
        timeout: int = 30,
        max_retries: int = 2,
    ) -> None:
        self.api_key = api_key
        self.auth_token = auth_token
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = requests.Session()
        self._session.headers.update(
            {"Authorization": f"Bearer {auth_token}"}
        )

    # --------------------------------------------------------------------- #
    # Public helpers
    # --------------------------------------------------------------------- #

    def post(
        self,
        host: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Send a POST request with form-data body.

        Args:
            host: Key from ``HOSTS`` (e.g. ``"astroapi-5"``).
            path: API path (e.g. ``"/api/v5/daily-horoscope"``).
            data: Extra form fields. ``api_key`` is injected automatically.

        Returns:
            Parsed JSON response as a dict.

        Raises:
            DivineApiError (or subclass) on failure.
        """
        url = f"{HOSTS[host]}{path}"
        payload = dict(data or {})
        payload["api_key"] = self.api_key

        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self._session.post(
                    url, data=payload, timeout=self.timeout
                )
                return self._handle_response(resp)
            except NetworkError:
                raise
            except requests.RequestException as exc:
                last_exc = exc
                if attempt == self.max_retries:
                    raise NetworkError(
                        f"Request to {url} failed after {self.max_retries} attempts: {exc}"
                    ) from exc
        # Should never reach here, but just in case:
        raise NetworkError(str(last_exc))  # pragma: no cover

    # --------------------------------------------------------------------- #
    # Internal
    # --------------------------------------------------------------------- #

    @staticmethod
    def _handle_response(resp: requests.Response) -> Dict[str, Any]:
        """Map HTTP status codes to SDK exceptions."""
        try:
            body = resp.json()
        except ValueError:
            body = {"raw": resp.text}

        if resp.status_code in (200, 201):
            return body

        msg = body.get("message") or body.get("error") or resp.text
        kwargs = {"message": msg, "status_code": resp.status_code, "response": body}

        if resp.status_code in (401, 403):
            raise AuthenticationError(**kwargs)
        if resp.status_code == 404:
            raise NotFoundError(**kwargs)
        if resp.status_code == 429:
            raise RateLimitError(**kwargs)
        if resp.status_code in (400, 422):
            raise ValidationError(**kwargs)
        if 500 <= resp.status_code < 600:
            raise ServerError(**kwargs)

        raise DivineApiError(**kwargs)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> "BaseClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
