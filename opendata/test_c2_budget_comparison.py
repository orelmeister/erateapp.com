#!/usr/bin/env python3
"""
Compare C2 Budget Tool API vs Form 471/472 APIs for BEN funding balance

This script tests both approaches to see which provides better data.
"""

import requests
import json
import sys
from typing import Dict, List


def fetch_c2_budget_data(ben: str) -> List[Dict]:
    """Fetch C2 Budget Tool data for a BEN"""
    url = "https://opendata.usac.org/resource/6brt-5pbv.json"
    
    params = {
        "$limit": 1000,
        "$where": f"ben='{ben}'",
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching C2 Budget data: {e}")
        return []


def fetch_form_471_data(ben: str) -> List[Dict]:
    """Fetch Form 471 data for a BEN"""
    url = "https://opendata.usac.org/resource/srbr-2d59.json"
    
    params = {
        "$limit": 5000,
        "$where": f"ben='{ben}'",
        "$order": "funding_year DESC",
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Form 471 data: {e}")
        return []


def fetch_form_472_data(ben: str) -> List[Dict]:
    """Fetch Form 472 disbursement data for a BEN"""
    url = "https://opendata.usac.org/resource/jpiu-tj8h.json"
    
    params = {
        "$limit": 5000,
        "$where": f"billed_entity_number='{ben}'",
        "$order": "funding_year DESC",
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Form 472 data: {e}")
        return []


def compare_apis(ben: str):
    """Compare both API approaches"""
    print(f"\n{'='*80}")
    print(f"API COMPARISON FOR BEN: {ben}")
    print(f"{'='*80}\n")
    
    # ========== METHOD 1: C2 Budget Tool API ==========
    print("📊 METHOD 1: C2 Budget Tool API (6brt-5pbv)")
    print("-" * 80)
    
    c2_data = fetch_c2_budget_data(ben)
    
    if c2_data:
        print(f"✅ Found {len(c2_data)} C2 Budget records\n")
        
        for record in c2_data:
            print(f"Entity: {record.get('billed_entity_name')}")
            print(f"C2 Budget Cycle: {record.get('c2_budget_cycle')}")
            print(f"Applicant Type: {record.get('applicant_type')}")
            print(f"Students: {record.get('full_time_students')}")
            print(f"C2 Budget Algorithm: {record.get('c2_budget_algorithm')}")
            print(f"\n💰 C2 Budget Breakdown:")
            
            c2_budget = float(record.get("c2_budget") or 0)
            funded = float(record.get("funded_c2_budget_amount") or 0)
            pending = float(record.get("pending_c2_budget_amount") or 0)
            available = float(record.get("available_c2_budget_amount") or 0)
            
            print(f"  Total C2 Budget (5-year): ${c2_budget:,.2f}")
            print(f"  Funded Amount: ${funded:,.2f}")
            print(f"  Pending Amount: ${pending:,.2f}")
            print(f"  Available Amount: ${available:,.2f}")
            print(f"  Budget Version: {record.get('c2_budget_version')}")
            
            if record.get('consulting_firm_name_crn'):
                print(f"  Consultant: {record.get('consulting_firm_name_crn')}")
    else:
        print("❌ No C2 Budget Tool records found")
    
    # ========== METHOD 2: Form 471 + 472 APIs ==========
    print(f"\n{'='*80}")
    print("📊 METHOD 2: Form 471 + Form 472 APIs (Current Method)")
    print("-" * 80)
    
    form_471_data = fetch_form_471_data(ben)
    form_472_data = fetch_form_472_data(ben)
    
    if form_471_data:
        print(f"✅ Found {len(form_471_data)} Form 471 applications")
        print(f"✅ Found {len(form_472_data)} Form 472 disbursements\n")
        
        # Calculate totals
        print("📈 Form 471/472 Summary:")
        by_year = {}
        
        # Process commitments
        for app in form_471_data:
            status = app.get("form_471_frn_status_name", "Unknown")
            year = app.get("funding_year", "Unknown")
            
            if year not in by_year:
                by_year[year] = {"committed": 0.0, "disbursed": 0.0}
            
            if status == "Funded":
                committed = float(app.get("funding_commitment_request") or 0)
                by_year[year]["committed"] += committed
        
        # Process disbursements
        for invoice in form_472_data:
            year = invoice.get("funding_year", "Unknown")
            if year in by_year:
                disbursed = float(invoice.get("approved_inv_line_amt") or 0)
                by_year[year]["disbursed"] += disbursed
        
        # Show results
        for year, data in sorted(by_year.items(), reverse=True):
            remaining = data["committed"] - data["disbursed"]
            print(f"  FY {year}:")
            print(f"    Committed: ${data['committed']:,.2f}")
            print(f"    Disbursed: ${data['disbursed']:,.2f}")
            print(f"    Remaining: ${remaining:,.2f}")
    else:
        print("❌ No Form 471/472 records found")
    
    # ========== COMPARISON ==========
    print(f"\n{'='*80}")
    print("🔍 COMPARISON & RECOMMENDATION")
    print("=" * 80)
    print("\n📋 C2 Budget Tool (6brt-5pbv):")
    print("  ✅ Shows 5-year C2 budget allocation")
    print("  ✅ Tracks Internal Connections (C2) spending limits")
    print("  ✅ Pre-calculated remaining budgets")
    print("  ⚠️  Only covers Category 2 (Internal Connections)")
    print("  ⚠️  May not show invoice-level detail")
    
    print("\n📋 Form 471 + 472 APIs:")
    print("  ✅ Shows ALL E-Rate categories (C1 & C2)")
    print("  ✅ Detailed application & invoice data")
    print("  ✅ Shows exact disbursement history")
    print("  ✅ Tracks remaining balance per FRN")
    print("  ⚠️  Requires calculation (committed - disbursed)")
    
    print("\n💡 RECOMMENDATION:")
    print("  Use BOTH APIs together:")
    print("  • Form 471/472 = Complete funding balance (all categories)")
    print("  • C2 Budget Tool = 5-year C2 budget tracking")
    print("\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_c2_budget_comparison.py <BEN_NUMBER>")
        print("\nExample:")
        print("  python test_c2_budget_comparison.py 16069179")
        sys.exit(1)
    
    ben = sys.argv[1].strip()
    compare_apis(ben)
