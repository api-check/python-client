"""ApiCheck Python Client - address validation, search, and verification."""

from .client import ApiClient
from .types import (
    LookupResponse,
    NumberAdditionsResponse,
    GlobalSearchResponse,
    EmailVerificationResponse,
    PhoneVerificationResponse,
)
from .exceptions import (
    ApiCheckError,
    UnsupportedCountryError,
    AuthenticationError,
    RateLimitError,
)

__version__ = "2.0.0"
__all__ = [
    "ApiClient",
    "LookupResponse",
    "NumberAdditionsResponse",
    "GlobalSearchResponse",
    "EmailVerificationResponse",
    "PhoneVerificationResponse",
    "ApiCheckError",
    "UnsupportedCountryError",
    "AuthenticationError",
    "RateLimitError",
]
