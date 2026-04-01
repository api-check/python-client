"""ApiCheck Python Client - address validation, search, and verification."""

from .client import ApiClient, AsyncApiClient
from .types import (
    LookupResponse,
    NumberAdditionsResponse,
    GlobalSearchResponse,
    EmailVerificationResponse,
    PhoneVerificationResponse,
    SearchOptions,
    LookupOptions,
)
from .exceptions import (
    ApiCheckError,
    ValidationError,
    UnsupportedCountryError,
    NotFoundError,
    AuthenticationError,
    RateLimitError,
)

__version__ = "2.0.0"
__all__ = [
    "ApiClient",
    "AsyncApiClient",
    "LookupResponse",
    "NumberAdditionsResponse",
    "GlobalSearchResponse",
    "EmailVerificationResponse",
    "PhoneVerificationResponse",
    "SearchOptions",
    "LookupOptions",
    "ApiCheckError",
    "ValidationError",
    "UnsupportedCountryError",
    "NotFoundError",
    "AuthenticationError",
    "RateLimitError",
]
