"""Custom exceptions for the DivineAPI Python SDK."""


class DivineApiError(Exception):
    """Base exception for all DivineAPI errors."""

    def __init__(self, message: str, status_code: int = 0, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(DivineApiError):
    """Raised when authentication fails (401/403)."""
    pass


class RateLimitError(DivineApiError):
    """Raised when API rate limit is exceeded (429)."""
    pass


class ValidationError(DivineApiError):
    """Raised when request parameters are invalid (400/422)."""
    pass


class NotFoundError(DivineApiError):
    """Raised when the requested resource is not found (404)."""
    pass


class ServerError(DivineApiError):
    """Raised when the API server returns a 5xx error."""
    pass


class NetworkError(DivineApiError):
    """Raised when a network-level error occurs (timeout, connection refused, etc.)."""
    pass
