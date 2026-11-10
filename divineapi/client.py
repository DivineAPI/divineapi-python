"""Base HTTP client for the DivineAPI SDK."""

import json
from typing import Any, Dict, Iterator, Optional

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
    "geolocation": "https://geolocation.divineapi.com",
    "ask": "https://ask.divineapi.com",
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

    def post_json(
        self,
        host: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        retry: bool = True,
    ) -> Dict[str, Any]:
        """Send a POST request with a JSON body and the API key in an ``x-api-key`` header.

        Used by Reports V2 (``/api/v1/reports/generate`` and
        ``/api/v1/western/reports/generate``), which rejects form-encoded
        requests with 401 "x-api-key header required", and by the Astro
        Chatbot (``ask.divineapi.com``).

        ``retry=False`` sends the request once. Use it for calls that charge
        or change something, where a retry after a timeout could repeat them.
        """
        url = f"{HOSTS[host]}{path}"
        attempts = self.max_retries if retry else 1
        last_exc: Optional[Exception] = None
        for attempt in range(1, attempts + 1):
            try:
                resp = self._session.post(
                    url, json=dict(data or {}), headers={"x-api-key": self.api_key},
                    timeout=self.timeout,
                )
                return self._handle_response(resp)
            except NetworkError:
                raise
            except requests.RequestException as exc:
                last_exc = exc
                if attempt == attempts:
                    raise NetworkError(
                        f"Request to {url} failed after {attempts} attempts: {exc}"
                    ) from exc
        raise NetworkError(str(last_exc))  # pragma: no cover

    def post_json_stream(
        self,
        host: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Iterator[Dict[str, Any]]:
        """POST a JSON body like :meth:`post_json` and read a Server-Sent Events reply.

        The request is sent, once, before this returns, so an HTTP error
        raises here. The returned iterator yields each event's JSON ``data``
        payload as it arrives. A reply that is plain JSON instead of a stream
        is yielded as a single event.
        """
        url = f"{HOSTS[host]}{path}"
        try:
            resp = self._session.post(
                url, json=dict(data or {}),
                headers={"x-api-key": self.api_key, "Accept": "text/event-stream"},
                timeout=self.timeout, stream=True,
            )
        except requests.RequestException as exc:
            raise NetworkError(f"Request to {url} failed: {exc}") from exc
        if resp.status_code not in (200, 201) or "text/event-stream" not in resp.headers.get(
            "Content-Type", ""
        ):
            try:
                body = self._handle_response(resp)
            finally:
                resp.close()
            return iter([body])
        return self._iter_events(resp, url)

    # --------------------------------------------------------------------- #
    # Internal
    # --------------------------------------------------------------------- #

    @staticmethod
    def _iter_events(resp: requests.Response, url: str) -> Iterator[Dict[str, Any]]:
        """Parse a Server-Sent Events body into the JSON payloads of its ``data`` lines."""
        try:
            data_lines = []
            # Split the raw bytes and decode each line afterwards: the stream is
            # UTF-8, and splitting decoded text would also break on U+2028.
            for raw in resp.iter_lines():
                line = raw.decode("utf-8")
                if line.startswith("data:"):
                    data_lines.append(line[5:][1:] if line[5:6] == " " else line[5:])
                elif not line and data_lines:
                    yield BaseClient._parse_event(data_lines, url)
                    data_lines = []
            if data_lines:
                yield BaseClient._parse_event(data_lines, url)
        except requests.RequestException as exc:
            raise NetworkError(f"Stream from {url} broke off: {exc}") from exc
        finally:
            resp.close()

    @staticmethod
    def _parse_event(data_lines: list, url: str) -> Dict[str, Any]:
        data = "\n".join(data_lines)
        try:
            return json.loads(data)
        except ValueError as exc:
            raise DivineApiError(f"Unreadable event in the stream from {url}: {data[:200]}") from exc

    @staticmethod
    def _detail_message(detail: Any) -> str:
        """Text of a FastAPI ``detail`` (ask.divineapi.com errors): a string, or
        a list of field errors such as ``[{"loc": ["body", "user_id"], "msg": "Field required"}]``."""
        if isinstance(detail, str):
            return detail
        if isinstance(detail, list):
            parts = []
            for item in detail:
                if isinstance(item, dict):
                    loc = item.get("loc") or []
                    field = str(loc[-1]) if loc else ""
                    msg = str(item.get("msg", ""))
                    parts.append(f"{field}: {msg}" if field else msg)
                else:
                    parts.append(str(item))
            return "; ".join(p for p in parts if p)
        return ""

    @staticmethod
    def _handle_response(resp: requests.Response) -> Dict[str, Any]:
        """Map HTTP status codes to SDK exceptions."""
        try:
            body = resp.json()
        except ValueError:
            body = {"raw": resp.text}

        if resp.status_code in (200, 201):
            return body

        msg = (body.get("message") or body.get("error")
               or BaseClient._detail_message(body.get("detail")) or resp.text)
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
