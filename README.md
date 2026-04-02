# ApiCheck Python Client

Address validation, search, and verification for 18 European countries.

## Installation

```bash
pip install apicheck
```

## Quick Start

```python
from apicheck import ApiClient

client = ApiClient('your-api-key')
```

## Global Search (Recommended)

The **global search** endpoint is the most powerful way to find addresses. It searches across streets, cities, and postal codes in one query with powerful filtering options.

```python
from apicheck import ApiClient

client = ApiClient('your-api-key')

# Basic search - finds streets, cities, and postal codes
results = client.global_search('nl', 'Amsterdam', limit=10)

for result in results:
    print(f"{result['name']} ({result['type']})")
# Output:
# Amsterdam (city)
# Amsterdamsestraat (street)
# 1012LM (postalcode)

# Filter by city - only return results within a specific city
results = client.global_search('nl', 'Dam', city_id=2465, limit=10)

# Filter by street - only return results on a specific street  
results = client.global_search('nl', '1', street_id=12345, limit=10)

# Filter by postal code area
results = client.global_search('nl', 'A', postalcode_id=54321, limit=10)

# Belgium: filter by locality (deelgemeente)
results = client.global_search('be', 'Hoofd', locality_id=111, limit=10)

# Belgium: filter by municipality (gemeente)
results = client.global_search('be', 'Station', municipality_id=222, limit=10)

# Combine filters for precise results
results = client.global_search('nl', '1', city_id=2465, limit=10)
```

### Global Search Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `country` | str | Country code (nl, be, lu, de, fr, cz, fi, it, no, pl, pt, ro, es, ch, at, dk, gb, se) |
| `query` | str | Search term (street name, city name, or postal code) |
| `limit` | int | Maximum results (default: 10) |
| `city_id` | int | Filter results to a specific city |
| `street_id` | int | Filter results to a specific street |
| `postalcode_id` | int | Filter results to a specific postal code area |
| `locality_id` | int | Filter results to a specific locality (Belgium) |
| `municipality_id` | int | Filter results to a specific municipality (Belgium) |

### Result Types

Results include a `type` field indicating what was matched:

- `city` - City/municipality
- `street` - Street name
- `postalcode` - Postal code area

## Address Lookup (Netherlands & Luxembourg)

For exact address lookup by postal code and house number:

```python
# Basic lookup
address = client.lookup('nl', '1012LM', '1')
print(address['street'])  # Damrak
print(address['city'])    # Amsterdam

# With number addition (apartment/suite)
address = client.lookup('nl', '1012LM', '1', number_addition='A')

# Get available number additions for an address
additions = client.get_number_additions('nl', '1012LM', '1')
print(additions['numberAdditions'])  # ['A', 'B', '1-3']
```

## Individual Search Endpoints

For targeted searches when you know exactly what you're looking for:

```python
# Search cities
cities = client.search_city('nl', 'Amsterdam', limit=10)

# Search streets
streets = client.search_street('nl', 'Damrak', limit=10)
streets = client.search_street('nl', 'Dam', city_id=2465, limit=10)  # Filter by city

# Search postal codes
postalcodes = client.search_postalcode('nl', '1012', limit=10)

# Search localities (Belgium primarily)
localities = client.search_locality('be', 'Antwerpen', limit=10)

# Search municipalities (Belgium primarily)
municipalities = client.search_municipality('be', 'Antwerpen', limit=10)

# Resolve full address using IDs from other searches
addresses = client.search_address(
    'nl',
    city_id=2465,
    number='1',
    number_addition='A',
    limit=10
)
```

## Verification

```python
# Verify email
result = client.verify_email('test@example.com')
print(result['status'])         # valid, invalid, or unknown
print(result['disposable_email'])  # True if disposable email provider
print(result['greylisted'])     # True if greylisted

# Verify phone number
result = client.verify_phone('+31612345678')
print(result['valid'])          # True if valid number
print(result['country_code'])   # NL
```

## Supported Countries

### All Search Endpoints (18 countries)
`nl`, `be`, `lu`, `de`, `fr`, `cz`, `fi`, `it`, `no`, `pl`, `pt`, `ro`, `es`, `ch`, `at`, `dk`, `gb`, `se`

### Address Lookup (Netherlands & Luxembourg only)
`nl`, `lu`

## API Key

Get your API key at [app.apicheck.nl](https://app.apicheck.nl)

## Error Handling

```python
from apicheck import ApiClient, UnsupportedCountryError

client = ApiClient('your-api-key')

try:
    address = client.lookup('de', '10115', '1')  # Germany not supported for lookup
except UnsupportedCountryError as e:
    print(f"Country not supported: {e.country}")
```

## Options

```python
client = ApiClient(
    api_key='your-api-key',
    timeout=15,  # Request timeout in seconds (default: 10)
    referer='https://yoursite.com'  # Required if API key has "Allowed Hosts" enabled
)
```

## Tips

1. **Use Global Search first** - It's the most flexible and covers all use cases
2. **Filter for precision** - Use city_id, street_id, etc. to narrow down results
3. **Chain searches** - Use Search City to get a city_id, then use it in Global Search or Search Address
4. **Belgium addresses** - Use locality_id and municipality_id filters for precise results

## License

MIT
