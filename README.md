# apicheck

Python client for ApiCheck - address validation, search, and verification.

## Installation

```bash
pip install apicheck
```

## Usage

```python
from apicheck import ApiClient

client = ApiClient("your-api-key")

# Lookup address (NL, LU)
address = client.lookup("nl", "1012LM", "1")
print(address.street)  # Damrak
print(address.city)    # Amsterdam

# Global search (18 countries)
results = client.global_search("nl", "amsterdam")

# Verify email
email = client.verify_email("test@example.com")
print(email.status)  # valid, invalid, unknown

# Verify phone
phone = client.verify_phone("+31612345678")
print(phone.valid)  # True/False
```

## API

### `lookup(country, postalcode, number)`
Address lookup for NL and LU.

### `global_search(country, query, limit?)`
Search across 18 European countries.

### `verify_email(email)`
Validate email address.

### `verify_phone(number)`
Validate phone number.

## License

MIT
