import pytest
from unittest.mock import Mock, patch
from apicheck import ApiClient

class TestApiClient:
    def test_init(self):
        client = ApiClient("test-key")
        assert client.api_key == "test-key"
    
    @patch("apicheck.client.requests.Session")
    def test_lookup_unsupported_country(self, mock_session):
        client = ApiClient("test-key")
        from apicheck.exceptions import UnsupportedCountryError
        with pytest.raises(UnsupportedCountryError):
            client.lookup("us", "12345", "1")
