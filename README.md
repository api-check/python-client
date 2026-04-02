# ApiCheck Python Client

Address validation, search, and verification for 18 European countries.

## Installation

pip install apicheck

## Quick Start

from apicheck import ApiClient

client = ApiClient('your-api-key')

## Global Search (Recommended)

The global search endpoint is the most powerful way to find addresses. It searches across streets, cities, and postal codes in one query with powerful filtering options.

results = client.global_search('nl', 'Amsterdam', limit=10)

for result in results:
    print(f"{result['name']} ({result['type']})")

# Filter by city
results = client.global_search('nl', 'Dam', city_id=2465, limit=10)

# Filter by street
results = client.global_search('nl', '1', street_id=12345, limit=10)

# Filter by postal code
results = client.global_search('nl', 'A', postalcode_id=54321, limit=10)

# Belgium: filter by locality
results = client.global_search('be', 'Hoofd', locality_id=111, limit=10)

# Belgium: filter by municipality
results = client.global_search('be', 'Station', municipality_id=222, limit=10)

### Global Search Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| country | string | Country code (nl, be, lu, de, fr, cz, fi, it, no, pl, pt, ro, es, ch, at, dk, gb, se) |
| query | string | Search term (street, city, or postal code) |
| limit | int | Maximum results (default: 10) |
| city_id | int | Filter to a specific city |
| street_id | int | Filter to a specific street |
| postalcode_id | int | Filter to a postal code area |
| locality_id | int | Filter to a locality (Belgium) |
| municipality_id | int | Filter to a municipality (Belgium) |

### Result Types

- city - City/municipality
- street - Street name
- postalcode - Postal code area

## Address Lookup (Netherlands & Luxembourg)

address = client.lookup('nl', '1012LM', '1')
print(address['street'])  # Damrak
print(address['city'])    # Amsterdam

# With number addition
address = client.lookup('nl', '1012LM', '1', number_addition='A')

# Get available additions
additions = client.get_number_additions('nl', '1012LM', '1')

## Individual Search Endpoints
cities = client.search_city('nl', 'Amsterdam', limit=10)
streets = client.search_street('nl', 'Damrak', limit=10)
streets = client.search_street('nl', 'Dam', city_id=2465, limit=10)
postalcodes = client.search_postalcode('nl', '1012', limit=10)
localities = client.search_locality('be', 'Antwerpen', limit=10)
municipalities = client.search_municipality('be', 'Antwerpen', limit=10)

## Verification
email = client.verify_email('test@example.com')
print(email['status'])  # valid, invalid, unknown

phone = client.verify_phone('+31612345678')
print(phone['valid'])  # True/False

## Supported Countries

All endpoints: nl, be, lu, de, fr, cz, fi, it, no, pl, pt, ro, es, ch, at, dk, gb, se
Lookup only: nl, lu

## API Key
Get your key at app.apicheck.nl
