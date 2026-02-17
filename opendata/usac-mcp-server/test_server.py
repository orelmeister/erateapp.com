"""
Test script for USAC MCP Server
Run this to verify the server works before connecting to Claude Desktop
"""

import json
import sys
sys.path.insert(0, '.')

# Test the client functionality
from server import USACDataClient

print("=" * 60)
print("USAC MCP Server - Functionality Test")
print("=" * 60)

client = USACDataClient(max_records=50)

# Test 1: Basic query
print("\n✓ Test 1: Query denied schools in 2025")
print("-" * 60)
df = client.fetch_data(year=2025, filters={'application_status': 'Denied', 'entity_type': 'School'}, limit=50)
print(f"Records fetched: {len(df)}")
if len(df) > 0:
    print(f"Sample record: {df.iloc[0]['applicant_name']}")
    print("✓ PASSED")
else:
    print("✗ FAILED: No records returned")

# Test 2: Get field values
print("\n✓ Test 2: Get available states")
print("-" * 60)
states = client.get_field_values('state', year=2024)
print(f"Found {len(states)} states")
print(f"Sample: {states[:5]}")
if len(states) > 0:
    print("✓ PASSED")
else:
    print("✗ FAILED: No states returned")

# Test 3: Pagination
print("\n✓ Test 3: Test pagination (fetching 250 records)")
print("-" * 60)
df = client.fetch_data(year=2024, limit=250)
print(f"Records fetched: {len(df)}")
if len(df) >= 200:
    print("✓ PASSED: Pagination working (fetched more than 200)")
else:
    print(f"✗ WARNING: Only fetched {len(df)} records")

# Test 4: Filtering
print("\n✓ Test 4: Filter by multiple criteria")
print("-" * 60)
df = client.fetch_data(
    year=2024, 
    filters={'application_status': 'Funded', 'entity_type': 'Library', 'state': 'CA'},
    limit=20
)
print(f"Funded libraries in CA (2024): {len(df)}")
if 'application_status' in df.columns:
    print(f"Status values: {df['application_status'].unique()}")
    print("✓ PASSED")
else:
    print("✗ FAILED: Missing expected columns")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
print("\nNext steps:")
print("1. Install in Claude Desktop using the config in README.md")
print("2. Restart Claude Desktop")
print("3. Start asking questions about E-Rate data!")
