#!/usr/bin/env python
"""Debug script to check USAC API field names directly"""
import requests
import json

def main():
    # Query USAC Open Data API directly - Form 471 dataset
    url = "https://opendata.usac.org/resource/avi8-svp9.json"
    
    # Use $where clause with 2025 filter
    params = {
        "$where": "billed_entity_number='142576' AND funding_year=2025",
        "$limit": 20
    }
    
    print(f"Fetching from {url}...")
    print(f"Params: {params}")
    r = requests.get(url, params=params)
    print(f"Status: {r.status_code}")
    
    data = r.json()
    
    if isinstance(data, list) and data:
        print(f"Found {len(data)} records for 2025")
        print("\n=== KEY FIELDS IN RECORDS ===")
        c2_total = 0
        for i, rec in enumerate(data):
            cat = rec.get('chosen_category_of_service', '')
            amt = float(rec.get('post_discount_extended_eligible_line_item_costs', 0) or 0)
            status = rec.get('form_471_frn_status_name', '')
            print(f"  {i+1}. Cat: {cat}, Status: {status}, Amount: ${amt:,.2f}")
            if 'category2' in cat.lower().replace(' ', ''):
                c2_total += amt
        print(f"\nTotal C2 funding: ${c2_total:,.2f}")
    else:
        print(f"Response: {data}")

if __name__ == "__main__":
    main()
