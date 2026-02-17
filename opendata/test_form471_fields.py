#!/usr/bin/env python
"""Check fields in form_471 dataset"""
import requests
import sys

# Main form_471 dataset
url = 'https://opendata.usac.org/resource/srbr-2d59.json'
params = {'$limit': 3}

print(f"Fetching from {url}...")
r = requests.get(url, params=params)
print(f"Status: {r.status_code}")

if r.status_code == 200:
    data = r.json()
    print(f"Found {len(data)} records")
    
    if data:
        rec = data[0]
        print("\n=== ALL FIELDS ===")
        for k in sorted(rec.keys()):
            print(f"  {k}: {rec.get(k, 'N/A')}")
else:
    print(f"Error: {r.text[:500]}")
