#!/usr/bin/env python3
"""
USAC E-Rate Funding Balance API Query Tool

This script queries the USAC Open Data API to get the available funding balance 
for a Billed Entity Number (BEN).

Usage:
    python get_ben_funding_balance.py <BEN_NUMBER>
    
Example:
    python get_ben_funding_balance.py 16038543

Output: JSON response with funding balance details
"""

import requests
import json
import sys
from typing import Dict, List, Optional
from datetime import datetime


# USAC Open Data API Endpoints (Socrata)
DATASETS = {
    'form_471': 'srbr-2d59',           # Form 471 Applications (commitments)
    'form_472': 'jpiu-tj8h',           # Form 472 Invoices & Disbursements
    'ecf': 'i5j4-3rvr',                # Emergency Connectivity Fund
    'c2_budget': '6brt-5pbv',          # C2 Budget Tool (5-year Category 2 budget)
}

BASE_URL_TEMPLATE = "https://opendata.usac.org/resource/{dataset_id}.json"


def get_base_url(dataset: str) -> str:
    """Get the API URL for a specific dataset"""
    dataset_id = DATASETS.get(dataset)
    if not dataset_id:
        raise ValueError(f"Unknown dataset: {dataset}")
    return BASE_URL_TEMPLATE.format(dataset_id=dataset_id)


def fetch_data(dataset: str, filters: Dict, limit: int = 5000, order_by: Optional[str] = None) -> List[Dict]:
    """
    Fetch data from USAC Open Data API with filters
    
    Args:
        dataset: Dataset name ('form_471', 'form_472', 'ecf', 'c2_budget')
        filters: Dictionary of field:value pairs for filtering
        limit: Maximum records to fetch
        order_by: Optional ORDER BY clause (default: 'funding_year DESC' for most datasets)
    
    Returns:
        List of records as dictionaries
    """
    url = get_base_url(dataset)
    
    # Build WHERE clause
    where_clauses = []
    for field, value in filters.items():
        if isinstance(value, list):
            # OR conditions for multiple values
            or_conditions = [f"{field}='{v}'" for v in value]
            where_clauses.append(f"({' OR '.join(or_conditions)})")
        else:
            escaped_value = str(value).replace("'", "''")
            where_clauses.append(f"{field}='{escaped_value}'")
    
    params = {
        "$limit": limit,
    }
    
    # C2 Budget Tool doesn't have funding_year field, so use custom ordering
    if order_by:
        params["$order"] = order_by
    elif dataset != 'c2_budget':
        params["$order"] = "funding_year DESC"
    
    if where_clauses:
        params["$where"] = " AND ".join(where_clauses)
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return []


def get_funding_balance(ben: str, funding_year: Optional[int] = None) -> Dict:
    """
    Get the funding balance for a BEN (Billed Entity Number)
    
    Args:
        ben: Billed Entity Number
        funding_year: Optional - filter by specific funding year
    
    Returns:
        Dictionary with funding balance details in JSON format
    """
    result = {
        "ben": ben,
        "query_timestamp": datetime.utcnow().isoformat() + "Z",
        "funding_year_filter": funding_year,
        "entity_info": None,
        "e_rate_funding": {
            "total_committed": 0.0,
            "total_disbursed": 0.0,
            "remaining_balance": 0.0,
            "applications_count": 0,
            "by_year": {},
            "by_status": {},
        },
        "ecf_funding": {
            "total_committed": 0.0,
            "applications_count": 0,
        },
        "c2_budget_info": [],
        "applications": [],
        "errors": [],
    }
    
    # ========== STEP 1: Fetch Form 471 Applications for this BEN ==========
    print(f"🔍 Fetching Form 471 applications for BEN {ben}...", file=sys.stderr)
    
    filters_471 = {"ben": ben}
    if funding_year:
        filters_471["funding_year"] = str(funding_year)
    
    form_471_data = fetch_data("form_471", filters_471, limit=5000)
    
    if not form_471_data:
        result["errors"].append(f"No Form 471 applications found for BEN {ben}")
        return result
    
    # Get entity info from first record
    first_record = form_471_data[0]
    result["entity_info"] = {
        "organization_name": first_record.get("organization_name"),
        "state": first_record.get("state"),
        "entity_type": first_record.get("organization_entity_type_name"),
    }
    
    # Process Form 471 applications
    by_year = {}
    by_status = {}
    total_committed = 0.0
    funded_frns = []
    
    for app in form_471_data:
        # Get status
        status = app.get("form_471_frn_status_name", "Unknown")
        year = app.get("funding_year", "Unknown")
        frn = app.get("funding_request_number")
        
        # funding_commitment_request is the APPROVED/COMMITTED amount
        committed_amount = float(app.get("funding_commitment_request") or 0)
        
        # Track by status
        if status not in by_status:
            by_status[status] = {"count": 0, "amount": 0.0}
        by_status[status]["count"] += 1
        by_status[status]["amount"] += committed_amount
        
        # Track by year
        if year not in by_year:
            by_year[year] = {"count": 0, "committed": 0.0, "disbursed": 0.0}
        by_year[year]["count"] += 1
        by_year[year]["committed"] += committed_amount
        
        # Only count "Funded" applications for balance calculation
        if status == "Funded":
            total_committed += committed_amount
            if frn:
                funded_frns.append({
                    "frn": frn,
                    "year": year,
                    "committed": committed_amount,
                    "application_number": app.get("application_number"),
                    "service_type": app.get("form_471_service_type_name"),
                })
        
        # Add to applications list (simplified)
        result["applications"].append({
            "funding_request_number": frn,
            "application_number": app.get("application_number"),
            "funding_year": year,
            "status": status,
            "service_type": app.get("form_471_service_type_name"),
            "committed_amount": committed_amount,
            "total_pre_discount_costs": float(app.get("original_total_pre_discount_costs") or 0),
            "discount_rate": float(app.get("dis_pct") or 0),
        })
    
    result["e_rate_funding"]["applications_count"] = len(form_471_data)
    result["e_rate_funding"]["total_committed"] = round(total_committed, 2)
    result["e_rate_funding"]["by_year"] = by_year
    result["e_rate_funding"]["by_status"] = by_status
    
    # ========== STEP 2: Fetch Form 472 Disbursements ==========
    print(f"💰 Fetching Form 472 disbursements for BEN {ben}...", file=sys.stderr)
    
    filters_472 = {"billed_entity_number": ben}
    if funding_year:
        filters_472["funding_year"] = str(funding_year)
    
    form_472_data = fetch_data("form_472", filters_472, limit=5000)
    
    total_disbursed = 0.0
    disbursement_details = []
    
    if form_472_data:
        for invoice in form_472_data:
            # approved_inv_line_amt is the disbursed amount
            disbursed = float(invoice.get("approved_inv_line_amt") or 0)
            total_disbursed += disbursed
            
            year = invoice.get("funding_year", "Unknown")
            if year in by_year:
                by_year[year]["disbursed"] += disbursed
            
            disbursement_details.append({
                "frn": invoice.get("funding_request_number"),
                "year": year,
                "amount": disbursed,
                "invoice_number": invoice.get("form_472_number"),
            })
    else:
        print(f"ℹ️  No disbursement records found for BEN {ben}", file=sys.stderr)
    
    result["e_rate_funding"]["total_disbursed"] = round(total_disbursed, 2)
    result["e_rate_funding"]["remaining_balance"] = round(total_committed - total_disbursed, 2)
    
    # Update by_year with disbursement data
    for year_data in by_year.values():
        year_data["committed"] = round(year_data["committed"], 2)
        year_data["disbursed"] = round(year_data["disbursed"], 2)
        year_data["remaining"] = round(year_data["committed"] - year_data["disbursed"], 2)
    
    result["e_rate_funding"]["by_year"] = by_year
    
    # ========== STEP 3: Fetch ECF Funding (if any) ==========
    print(f"🌐 Checking ECF funding for BEN {ben}...", file=sys.stderr)
    
    ecf_data = fetch_data("ecf", {"billed_entity_number": ben}, limit=500)
    
    if ecf_data:
        ecf_committed = 0.0
        for ecf_app in ecf_data:
            ecf_amount = float(ecf_app.get("funding_commitment_request") or 
                              ecf_app.get("funding_commitment_amount") or 0)
            ecf_committed += ecf_amount
        
        result["ecf_funding"]["total_committed"] = round(ecf_committed, 2)
        result["ecf_funding"]["applications_count"] = len(ecf_data)
    
    # ========== STEP 4: Fetch C2 Budget Tool Data ==========
    print(f"📊 Fetching C2 Budget data for BEN {ben}...", file=sys.stderr)
    
    c2_data = fetch_data("c2_budget", {"ben": ben}, limit=100)
    
    if c2_data:
        for record in c2_data:
            c2_info = {
                "budget_cycle": record.get("c2_budget_cycle"),
                "total_c2_budget": round(float(record.get("c2_budget") or 0), 2),
                "funded_amount": round(float(record.get("funded_c2_budget_amount") or 0), 2),
                "pending_amount": round(float(record.get("pending_c2_budget_amount") or 0), 2),
                "available_amount": round(float(record.get("available_c2_budget_amount") or 0), 2),
                "budget_version": record.get("c2_budget_version"),
                "budget_algorithm": record.get("c2_budget_algorithm"),
                "full_time_students": record.get("full_time_students"),
                "student_multiplier": record.get("school_student_multiplier"),
                "consultant": record.get("consulting_firm_name_crn"),
            }
            result["c2_budget_info"].append(c2_info)
        print(f"✅ Found {len(c2_data)} C2 Budget cycle(s)", file=sys.stderr)
    else:
        print(f"ℹ️  No C2 Budget Tool records found for BEN {ben}", file=sys.stderr)
    
    print(f"✅ Query complete for BEN {ben}", file=sys.stderr)
    return result


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python get_ben_funding_balance.py <BEN_NUMBER> [FUNDING_YEAR]")
        print("\nExample:")
        print("  python get_ben_funding_balance.py 16038543")
        print("  python get_ben_funding_balance.py 16038543 2024")
        sys.exit(1)
    
    ben = sys.argv[1].strip()
    funding_year = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    # Get funding balance
    result = get_funding_balance(ben, funding_year)
    
    # Output as formatted JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
