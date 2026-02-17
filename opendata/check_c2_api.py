#!/usr/bin/env python3
import requests
import json

# Check C2 Budget API structure
print("Fetching C2 Budget API sample...")
r = requests.get('https://opendata.usac.org/resource/6brt-5pbv.json?$limit=5')
data = r.json()

if data:
    print(f"\nFound {len(data)} records\n")
    print("Available fields:")
    print("-" * 80)
    for key in sorted(data[0].keys()):
        print(f"  {key}")
    
    print("\n" + "=" * 80)
    print("Sample record:")
    print("=" * 80)
    print(json.dumps(data[0], indent=2))
else:
    print("No data returned")
