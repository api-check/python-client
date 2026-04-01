"""ApiCheck Python Client - address validation, search, and verification."""

from .client import ApiClient, COUNTRIES_ALL, COUNTRIES_LOOKUP
from .exceptions import (
    ApiCheckError,
    UnsupportedCountryError,
    AuthenticationError,
    RateLimitError,
)

__version__ = "2.1.1"

__all__ = [
    "ApiClient",
    "COUNTRIES_ALL",
    "COUNTRIES_LOOKUP",
    "ApiCheckError",
    "UnsupportedCountryError",
    "AuthenticationError",
    "RateLimitError",
]
