"""
Quick test of USAC API - funding balance query
"""
import requests
import json

BEN = "16038543"  # Sample BEN from sample_data.json

print(f"Testing USAC API for BEN: {BEN}")
print("=" * 50)

# Form 471 - Commitments
url_471 = "https://opendata.usac.org/resource/srbr-2d59.json"
params_471 = {
    "$where": f"ben='{BEN}'",
    "$limit": 20,
    "$order": "funding_year DESC"
}

print("\n1. Fetching Form 471 (Commitments)...")
resp = requests.get(url_471, params=params_471, timeout=30)
print(f"   Status: {resp.status_code}")

data_471 = resp.json()
print(f"   Records: {len(data_471)}")

total_committed = 0
funded_count = 0

if data_471:
    entity_name = data_471[0].get("organization_name", "Unknown")
    state = data_471[0].get("state", "Unknown")
    print(f"\n   Entity: {entity_name}")
    print(f"   State: {state}")
    print(f"\n   Applications by Status:")
    
    status_summary = {}
    for app in data_471:
        status = app.get("form_471_frn_status_name", "Unknown")
        year = app.get("funding_year", "Unknown")
        committed = float(app.get("funding_commitment_request") or 0)
        
        if status not in status_summary:
            status_summary[status] = {"count": 0, "amount": 0}
        status_summary[status]["count"] += 1
        status_summary[status]["amount"] += committed
        
        if status == "Funded":
            total_committed += committed
            funded_count += 1
    
    for status, info in status_summary.items():
        print(f"     - {status}: {info['count']} apps, ${info['amount']:,.2f}")

print(f"\n   Total FUNDED commitment: ${total_committed:,.2f}")

# Form 472 - Disbursements
url_472 = "https://opendata.usac.org/resource/jpiu-tj8h.json"
params_472 = {
    "$where": f"billed_entity_number='{BEN}'",
    "$limit": 100
}

print("\n2. Fetching Form 472 (Disbursements)...")
resp2 = requests.get(url_472, params=params_472, timeout=30)
print(f"   Status: {resp2.status_code}")

data_472 = resp2.json()
print(f"   Records: {len(data_472)}")

total_disbursed = 0
if data_472:
    for inv in data_472:
        disbursed = float(inv.get("approved_inv_line_amt") or 0)
        total_disbursed += disbursed

print(f"   Total Disbursed: ${total_disbursed:,.2f}")

# Calculate balance
remaining = total_committed - total_disbursed

print("\n" + "=" * 50)
print("FUNDING BALANCE SUMMARY")
print("=" * 50)
print(f"BEN: {BEN}")
print(f"Entity: {data_471[0].get('organization_name', 'Unknown') if data_471 else 'Unknown'}")
print(f"Total Funded/Committed: ${total_committed:,.2f}")
print(f"Total Disbursed:        ${total_disbursed:,.2f}")
print(f"REMAINING BALANCE:      ${remaining:,.2f}")
print("=" * 50)

# Output as JSON
output = {
    "ben": BEN,
    "entity_name": data_471[0].get("organization_name") if data_471 else None,
    "state": data_471[0].get("state") if data_471 else None,
    "total_committed": round(total_committed, 2),
    "total_disbursed": round(total_disbursed, 2),
    "remaining_balance": round(remaining, 2),
    "funded_applications_count": funded_count,
    "total_applications_count": len(data_471),
}

print("\nJSON Response:")
print(json.dumps(output, indent=2))
