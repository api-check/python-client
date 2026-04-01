import requests
from typing import Any, Optional, List

API_ENDPOINT = "https://api.apicheck.nl"

# All supported countries for search
COUNTRIES_ALL = ["nl", "be", "lu", "de", "fr", "cz", "fi", "it", "no", "pl", "pt", "ro", "es", "ch", "at", "dk", "gb", "se"]
# Countries that support lookup by postalcode (NL, LU only)
COUNTRIES_LOOKUP = ["nl", "lu"]


class ApiClient:
    def __init__(self, api_key: str, timeout: int = 10, referer: Optional[str] = None):
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/json",
            "X-API-KEY": api_key,
        })
        if referer:
            self._session.headers["Referer"] = referer

    def _extract_data(self, response: requests.Response) -> Any:
        """Extract data from API response."""
        response.raise_for_status()
        json_data = response.json()
        return json_data.get("data", json_data)

    # ============================================
    # Lookup API (Netherlands, Luxembourg only)
    # ============================================

    def lookup(self, country: str, postalcode: str, number: str, 
               number_addition: Optional[str] = None) -> dict:
        """
        Look up an address by postal code and house number.
        
        Args:
            country: Country code (nl, lu)
            postalcode: Postal code (e.g., "2513AA")
            number: House number (e.g., "1")
            number_addition: Optional number addition (e.g., "A", "B")
        """
        params = {"postalcode": postalcode, "number": number}
        if number_addition:
            params["numberAddition"] = number_addition
            
        resp = self._session.get(
            f"{API_ENDPOINT}/lookup/v1/postalcode/{country.lower()}",
            params=params,
            timeout=self.timeout
        )
        return self._extract_data(resp)

    def get_number_additions(self, country: str, postalcode: str, number: str) -> dict:
        """Get available number additions for a postal code and house number."""
        resp = self._session.get(
            f"{API_ENDPOINT}/lookup/v1/address/{country.lower()}",
            params={"postalcode": postalcode, "number": number, "fields": '["numberAdditions"]'},
            timeout=self.timeout
        )
        return self._extract_data(resp)

    # ============================================
    # Search API (18 European countries)
    # ============================================

    def global_search(self, country: str, query: str, limit: int = 10,
                      city_id: Optional[int] = None,
                      street_id: Optional[int] = None,
                      postalcode_id: Optional[int] = None,
                      locality_id: Optional[int] = None,
                      municipality_id: Optional[int] = None) -> list:
        """
        Global search for addresses, streets, cities, or postal codes.
        
        Args:
            country: Country code (nl, be, lu, de, fr, cz, fi, it, no, pl, pt, ro, es, ch, at, dk, gb, se)
            query: Search query
            limit: Maximum results (default 10)
            city_id: Filter by city
            street_id: Filter by street
            postalcode_id: Filter by postal code
            locality_id: Filter by locality (Belgium)
            municipality_id: Filter by municipality (Belgium)
        """
        params = {"query": query, "limit": limit}
        if city_id:
            params["city_id"] = city_id
        if street_id:
            params["street_id"] = street_id
        if postalcode_id:
            params["postalcode_id"] = postalcode_id
        if locality_id:
            params["locality_id"] = locality_id
        if municipality_id:
            params["municipality_id"] = municipality_id
            
        resp = self._session.get(
            f"{API_ENDPOINT}/search/v1/global/{country.lower()}",
            params=params,
            timeout=self.timeout
        )
        data = self._extract_data(resp)
        
        results = []
        if "Results" in data:
            for street in data["Results"].get("Streets", []):
                results.append({**street, "type": "street"})
            for city in data["Results"].get("Cities", []):
                results.append({**city, "type": "city"})
            for pc in data["Results"].get("Postalcodes", []):
                results.append({**pc, "type": "postalcode"})
                
        return results[:limit]

    def search_city(self, country: str, name: str, limit: int = 10) -> list:
        """Search for cities by name."""
        resp = self._session.get(
            f"{API_ENDPOINT}/search/v1/city/{country.lower()}",
            params={"name": name, "limit": limit},
            timeout=self.timeout
        )
        return self._extract_data(resp)

    def search_street(self, country: str, name: str, 
                      city_id: Optional[int] = None, 
                      limit: int = 10) -> list:
        """Search for streets by name."""
        params = {"name": name, "limit": limit}
        if city_id:
            params["city_id"] = city_id
            
        resp = self._session.get(
            f"{API_ENDPOINT}/search/v1/street/{country.lower()}",
            params=params,
            timeout=self.timeout
        )
        return self._extract_data(resp)

    def search_postalcode(self, country: str, name: str,
                          city_id: Optional[int] = None,
                          limit: int = 10) -> list:
        """Search for postal codes."""
        params = {"name": name, "limit": limit}
        if city_id:
            params["city_id"] = city_id
            
        resp = self._session.get(
            f"{API_ENDPOINT}/search/v1/postalcode/{country.lower()}",
            params=params,
            timeout=self.timeout
        )
        return self._extract_data(resp)

    def search_locality(self, country: str, name: str, limit: int = 10) -> list:
        """
        Search for localities (deelgemeenten) by name.
        Primarily relevant for Belgium.
        """
        resp = self._session.get(
            f"{API_ENDPOINT}/search/v1/locality/{country.lower()}",
            params={"name": name, "limit": limit},
            timeout=self.timeout
        )
        return self._extract_data(resp)

    def search_municipality(self, country: str, name: str, limit: int = 10) -> list:
        """
        Search for municipalities (gemeenten) by name.
        Primarily relevant for Belgium.
        """
        resp = self._session.get(
            f"{API_ENDPOINT}/search/v1/municipality/{country.lower()}",
            params={"name": name, "limit": limit},
            timeout=self.timeout
        )
        return self._extract_data(resp)

    def search_address(self, country: str,
                       street_id: Optional[int] = None,
                       city_id: Optional[int] = None,
                       postalcode_id: Optional[int] = None,
                       locality_id: Optional[int] = None,
                       municipality_id: Optional[int] = None,
                       number: Optional[str] = None,
                       number_addition: Optional[str] = None,
                       limit: int = 10) -> list:
        """
        Resolve a full address using IDs from other search results.
        
        Provide at least one ID parameter (street_id, city_id, postalcode_id, 
        locality_id, or municipality_id).
        """
        params = {"limit": limit}
        if street_id:
            params["street_id"] = street_id
        if city_id:
            params["city_id"] = city_id
        if postalcode_id:
            params["postalcode_id"] = postalcode_id
        if locality_id:
            params["locality_id"] = locality_id
        if municipality_id:
            params["municipality_id"] = municipality_id
        if number:
            params["number"] = number
        if number_addition:
            params["numberAddition"] = number_addition
            
        resp = self._session.get(
            f"{API_ENDPOINT}/search/v1/address/{country.lower()}",
            params=params,
            timeout=self.timeout
        )
        return self._extract_data(resp)

    # ============================================
    # Verify API
    # ============================================

    def verify_email(self, email: str) -> dict:
        """Verify an email address for validity, disposable status, and greylisting."""
        resp = self._session.get(
            f"{API_ENDPOINT}/verify/v1/email/",
            params={"email": email},
            timeout=self.timeout
        )
        return self._extract_data(resp)

    def verify_phone(self, number: str) -> dict:
        """Verify a phone number for validity and formatting."""
        resp = self._session.get(
            f"{API_ENDPOINT}/verify/v1/phone/",
            params={"number": number},
            timeout=self.timeout
        )
        return self._extract_data(resp)
