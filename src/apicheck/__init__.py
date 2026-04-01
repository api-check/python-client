"""ApiCheck Python Client - address validation, search, and verification."""

from .client import ApiClient, COUNTRIES_ALL, COUNTRIES_LOOKUP
from .types import (
    LookupResponse,
    NumberAdditionsResponse,
    GlobalSearchResponse,
    EmailVerificationResponse,
    PhoneVerificationResponse,
    SearchResult,
    LookupOptions,
    GlobalSearchOptions,
    SearchOptions,
    AddressSearchOptions,
)
from .exceptions import (
    ApiCheckError,
    UnsupportedCountryError,
    AuthenticationError,
    RateLimitError,
)

__version__ = "2.1.0"
__all__ = [
    "ApiClient",
    "COUNTRIES_ALL",
    "COUNTRIES_LOOKUP",
    "LookupResponse",
    "NumberAdditionsResponse",
    "GlobalSearchResponse",
    "EmailVerificationResponse",
    "PhoneVerificationResponse",
    "SearchResult",
    "LookupOptions",
    "GlobalSearchOptions",
    "SearchOptions",
    "AddressSearchOptions",
    "ApiCheckError",
    "UnsupportedCountryError",
    "AuthenticationError",
    "RateLimitError",
]
