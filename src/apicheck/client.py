import requests
from typing import Any, Optional

API_ENDPOINT = "https://api.apicheck.nl"

class ApiClient:
    def __init__(self, api_key: str, timeout: int = 10):
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/json",
            "X-API-KEY": api_key,
        })

    # Lookup API (NL, LU)
    def lookup(self, country: str, postalcode: str, number: str) -> dict:
        resp = self._session.get(
            f"{API_ENDPOINT}/lookup/v1/postalcode/{country.lower()}",
            params={"postalcode": postalcode, "number": number},
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    def get_number_additions(self, country: str, postalcode: str, number: str) -> dict:
        resp = self._session.get(
            f"{API_ENDPOINT}/lookup/v1/address/{country.lower()}",
            params={"postalcode": postalcode, "number": number, "fields": '["numberAdditions"]'},
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    # Search API
    def global_search(self, country: str, query: str, limit: int = 10) -> list:
        resp = self._session.get(
            f"{API_ENDPOINT}/search/v1/global/{country.lower()}",
            params={"query": query, "limit": limit},
            timeout=self.timeout
        )
        resp.raise_for_status()
        data = resp.json().get("data", {})
        results = []
        if "Results" in data:
            if data["Results"].get("Cities"):
                results.extend(data["Results"]["Cities"])
            if data["Results"].get("Streets"):
                results.extend(data["Results"]["Streets"])
        return results

    # Verify API
    def verify_email(self, email: str) -> dict:
        resp = self._session.get(
            f"{API_ENDPOINT}/verify/v1/email/",
            params={"email": email},
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json().get("data", resp.json())

    def verify_phone(self, number: str) -> dict:
        resp = self._session.get(
            f"{API_ENDPOINT}/verify/v1/phone/",
            params={"number": number},
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json().get("data", resp.json())
