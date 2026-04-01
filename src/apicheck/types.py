"""Type definitions for ApiCheck Python Client."""

from dataclasses import dataclass
from typing import Optional, Literal, List, Any


@dataclass
class Coordinates:
    latitude: float
    longitude: float


@dataclass
class Country:
    name: str
    code: str


@dataclass
class LookupResponse:
    street: str
    number: str
    postalcode: str
    city: str
    country: Country
    coordinates: Coordinates
    street_short: Optional[str] = None
    number_addition: Optional[str] = None
    city_short: Optional[str] = None
    municipality: Optional[str] = None
    province: Optional[str] = None


@dataclass
class NumberAdditionsResponse:
    number: str
    number_additions: List[str]


@dataclass
class SearchResult:
    id: int
    name: str
    result_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    postalcode: Optional[str] = None


@dataclass
class GlobalSearchResponse:
    results: List[SearchResult]
    count: int
    limit: Optional[int] = None


@dataclass
class EmailVerificationResponse:
    email: str
    status: Literal["valid", "invalid", "unknown"]
    disposable_email: bool
    greylisted: bool


@dataclass
class PhoneVerificationResponse:
    number: str
    valid: bool
    country_code: Optional[str] = None
    area_code: Optional[str] = None
    international_formatted: Optional[str] = None
    national_formatted: Optional[str] = None
    number_type: Optional[str] = None
    carrier: Optional[str] = None


@dataclass
class LookupOptions:
    number_addition: Optional[str] = None
    fields: Optional[List[str]] = None
    aliases: Optional[bool] = None
    shortening: Optional[bool] = None


@dataclass
class GlobalSearchOptions:
    limit: Optional[int] = None
    city_id: Optional[int] = None
    street_id: Optional[int] = None
    postalcode_id: Optional[int] = None
    locality_id: Optional[int] = None
    municipality_id: Optional[int] = None


@dataclass
class SearchOptions:
    limit: Optional[int] = None
    city_id: Optional[int] = None


@dataclass
class AddressSearchOptions:
    limit: Optional[int] = None
    street_id: Optional[int] = None
    city_id: Optional[int] = None
    postalcode_id: Optional[int] = None
    locality_id: Optional[int] = None
    municipality_id: Optional[int] = None
    number: Optional[str] = None
    number_addition: Optional[str] = None
