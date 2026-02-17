# E-Rate Data Query Tool

A Python script to query and analyze E-Rate funding data from USAC's Open Data API.

## Features

- Fetch data from USAC E-Rate Open Data API
- Filter by state, funding year, organization, status, and service type
- Complex multi-criteria searches
- Statistics and data summaries
- Export results to JSON
- Display results in readable format

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script to see example queries:
```bash
python query_erate_data.py
```

### Custom Queries

```python
from query_erate_data import ERateDataQuery

# Initialize and fetch data
query = ERateDataQuery()
query.fetch_data(limit=1000)  # Fetch up to 1000 records

# Filter by state
ny_schools = query.filter_by_state('NY')
query.display_records(ny_schools)

# Filter by funding year
records_2025 = query.filter_by_funding_year('2025')

# Search by organization name
libraries = query.filter_by_organization('Library')

# Filter by status
funded = query.filter_by_status('Funded')
cancelled = query.filter_by_status('Cancelled')

# Complex search with multiple criteria
results = query.search(
    state='CA',
    funding_year='2025',
    status='Funded',
    service_type='Internet Access'
)

# Get statistics
stats = query.get_statistics()
print(stats)

# Export results
query.export_to_json(results, 'my_results.json')
```

## Available Fields

The API returns records with the following key fields:

- `funding_year` - The funding year
- `organization_name` - Name of the organization
- `organization_entity_type_name` - Type (School, Library, School District, etc.)
- `state` - State abbreviation
- `application_number` - Application number
- `funding_request_number` - FRN number
- `form_471_frn_status_name` - Status (Funded, Cancelled, Denied, etc.)
- `form_471_service_type_name` - Service type
- `dis_pct` - Discount percentage
- `dis_pct_band` - Discount band
- `spin_name` - Service provider name
- `fcdl_letter_date` - Funding commitment letter date
- `wave_sequence_number` - Wave number

## API Endpoint

Data source: https://opendata.usac.org/resource/bd9t-w7tr.json

## Examples

### Example 1: Find all schools in Texas
```python
query = ERateDataQuery()
query.fetch_data(limit=2000)
tx_schools = query.filter_by_state('TX')
query.display_records(tx_schools, max_records=20)
```

### Example 2: Find funded projects in 2025
```python
funded_2025 = query.search(funding_year='2025', status='Funded')
print(f"Found {len(funded_2025)} funded projects in 2025")
```

### Example 3: Analyze by service type
```python
internet = query.filter_by_service_type('Internet Access')
internal = query.filter_by_service_type('Internal Connections')
print(f"Internet Access requests: {len(internet)}")
print(f"Internal Connections requests: {len(internal)}")
```

## License

This tool is provided as-is for querying public E-Rate data from USAC.
