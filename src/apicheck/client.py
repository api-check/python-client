"""ApiCheck Python Client."""
import requests
from typing import Any, Optional
from .types import LookupResponse, NumberAdditionsResponse, GlobalSearchResponse, EmailVerificationResponse, PhoneVerificationResponse
from .types import Country, Coordinates, SearchResult
from .exceptions import ApiCheckError, UnsupportedCountryError

API_ENDPOINT = "https://api.apicheck.nl"
LOOKUP_COUNTRIES = {"nl", "lu"}
SEARCH_COUNTRIES = {"nl", "be", "lu", "fr", "de", "cz", "fi", "it", "no", "pl", "pt", "ro", "es", "ch", "at", "dk", "gb", "se"}

class ApiClient:
    def __init__(self, api_key: str, timeout: int = 10):
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"Accept": "application/json", "X-API-KEY": api_key})

    def lookup(self, country: str, postalcode: str, number: str | int) -> LookupResponse:
        country = country.lower()
        if country not in LOOKUP_COUNTRIES:
            raise UnsupportedCountryError(f"Country '{country}' not supported for lookup", country)
        response = self._session.get(f"{API_ENDPOINT}/lookup/v1/address/", params={"country": country, "postalcode": postalcode, "number": number}, timeout=self.timeout)
        self._check_response(response)
        return self._parse_lookup(response.json())

    def get_number_additions(self, country: str, postalcode: str, number: str | int) -> NumberAdditionsResponse:
        country = country.lower()
        if country not in LOOKUP_COUNTRIES:
            raise UnsupportedCountryError(f"Country '{country}' not supported", country)
        response = self._session.get(f"{API_ENDPOINT}/lookup/v1/numberadditions/", params={"country": country, "postalcode": postalcode, "number": number}, timeout=self.timeout)
        self._check_response(response)
        data = response.json()
        return NumberAdditionsResponse(number=str(data.get("number", number)), number_additions=data.get("numberAdditions", []))

    def global_search(self, country: str, query: str, limit: int | None = None) -> GlobalSearchResponse:
        country = country.lower()
        if country not in SEARCH_COUNTRIES:
            raise UnsupportedCountryError(f"Country '{country}' not supported", country)
        params = {"country": country, "query": query}
        if limit: params["limit"] = limit
        response = self._session.get(f"{API_ENDPOINT}/search/v1/global/", params=params, timeout=self.timeout)
        self._check_response(response)
        return self._parse_search(response.json())

    def verify_email(self, email: str) -> EmailVerificationResponse:
        response = self._session.get(f"{API_ENDPOINT}/verify/v1/email/", params={"email": email}, timeout=self.timeout)
        self._check_response(response)
        data = response.json()
        return EmailVerificationResponse(email=data["email"], status=data["status"], disposable_email=data.get("disposable_email", False), greylisted=data.get("greylisted", False))

    def verify_phone(self, number: str) -> PhoneVerificationResponse:
        response = self._session.get(f"{API_ENDPOINT}/verify/v1/phone/", params={"number": number}, timeout=self.timeout)
        self._check_response(response)
        data = response.json()
        return PhoneVerificationResponse(number=data["number"], valid=data.get("valid", False), country_code=data.get("country_code"), carrier=data.get("carrier"))

    def _check_response(self, response: requests.Response) -> None:
        if response.status_code == 401:
            from .exceptions import AuthenticationError
            raise AuthenticationError()
        if response.status_code >= 400:
            raise ApiCheckError(f"API error: {response.status_code}", response.status_code)

    def _parse_lookup(self, data: dict[str, Any]) -> LookupResponse:
        return LookupResponse(
            street=data.get("street", ""), number=data.get("number", ""), postalcode=data.get("postalcode", ""), city=data.get("city", ""),
            country=Country(name=data.get("country", {}).get("name", ""), code=data.get("country", {}).get("code", "")),
            coordinates=Coordinates(latitude=data.get("coordinates", {}).get("latitude", 0), longitude=data.get("coordinates", {}).get("longitude", 0)),
        )

    def _parse_search(self, data: dict[str, Any]) -> GlobalSearchResponse:
        results = [SearchResult(id=r.get("id", 0), name=r.get("name", ""), result_type=r.get("type")) for r in data.get("results", [])]
        return GlobalSearchResponse(results=results, count=data.get("count", len(results)))
