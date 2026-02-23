#!/usr/bin/env python3
"""
USAC Full Data Scraper
=====================
Scrapes the entire USAC E-Rate Open Data to produce CSV files for:
  1. Entities (BEN) - All billed entities with contact info
  2. Consultants (CRN/ACRN) - All registered consultants  
  3. Vendors (SPIN) - All service providers

Uses USAC Open Data API (Socrata):
  - Consultants: https://opendata.usac.org/resource/x5px-esft.json
  - Vendors:     https://opendata.usac.org/resource/xcy2-bdid.json
  - Entities:    https://opendata.usac.org/resource/srbr-2d59.json
"""

import requests
import csv
import json
import time
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional, Set
from collections import OrderedDict


# ============================================================================
# Configuration
# ============================================================================

BASE_URL = "https://opendata.usac.org/resource"

DATASETS = {
    "consultants": "x5px-esft",    # Form 471 Consultant Registration
    "vendors": "xcy2-bdid",         # Service Providers (SPIN)
    "entities": "srbr-2d59",        # Form 471 FRN Status (has BEN data)
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SkyRate-DataScraper/1.0",
    "Accept": "application/json",
}

BATCH_SIZE = 5000       # Records per API request (Socrata max is 50,000)
RATE_LIMIT_DELAY = 0.2  # Seconds between requests
MAX_RETRIES = 3         # Retry count on failure
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scraped_data")


# ============================================================================
# API Helper
# ============================================================================

def fetch_paginated(dataset_id: str, params_base: dict = None, 
                    batch_size: int = BATCH_SIZE, max_records: int = 0,
                    description: str = "") -> List[Dict]:
    """
    Fetch all records from a USAC Socrata dataset with pagination.
    
    Args:
        dataset_id: Socrata dataset identifier (e.g., 'x5px-esft')
        params_base: Base query parameters ($select, $where, $group, etc.)
        batch_size: Number of records per request
        max_records: Maximum total records (0 = unlimited)
        description: Description for progress logging
        
    Returns:
        List of all fetched records
    """
    url = f"{BASE_URL}/{dataset_id}.json"
    all_records = []
    offset = 0
    
    if params_base is None:
        params_base = {}
    
    print(f"\n{'='*60}")
    print(f"  Fetching: {description}")
    print(f"  Dataset: {dataset_id}")
    print(f"  Batch size: {batch_size}")
    print(f"{'='*60}")
    
    while True:
        params = {**params_base, "$limit": batch_size, "$offset": offset}
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, params=params, headers=HEADERS, timeout=120)
                
                if response.status_code == 200:
                    data = response.json()
                    break
                elif response.status_code == 429:
                    wait = 2 ** (attempt + 1)
                    print(f"  ⚠ Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"  ✗ HTTP {response.status_code}: {response.text[:200]}")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(2)
                    else:
                        print(f"  ✗ Failed after {MAX_RETRIES} attempts at offset {offset}")
                        return all_records
            except requests.exceptions.Timeout:
                print(f"  ⚠ Timeout on attempt {attempt+1}. Retrying...")
                time.sleep(3)
            except Exception as e:
                print(f"  ✗ Error: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2)
                else:
                    return all_records
        else:
            break
        
        if not data:
            break
            
        all_records.extend(data)
        fetched = len(all_records)
        print(f"  ⟳ Fetched {fetched:,} records (batch at offset {offset})...")
        
        if len(data) < batch_size:
            break
            
        if max_records > 0 and fetched >= max_records:
            all_records = all_records[:max_records]
            break
            
        offset += batch_size
        time.sleep(RATE_LIMIT_DELAY)
    
    print(f"  ✓ Total: {len(all_records):,} records fetched")
    return all_records


# ============================================================================
# Consultant Scraper (CRN/ACRN)
# ============================================================================

def scrape_consultants() -> List[Dict]:
    """
    Scrape all unique E-Rate consultants from the USAC consultant dataset.
    Returns deduplicated list by CRN with the most recent info.
    
    Fields fetched:
      - cnslt_epc_organization_id (CRN)
      - cnslt_name
      - cnslt_email
      - cnslt_phone
      - cnslt_city, cnslt_state, cnslt_zipcode
      - cnct_email (contact email at entity)
    Also fetches: number of unique schools served, most recent funding year
    """
    print("\n" + "="*60)
    print("  PHASE 1: SCRAPING CONSULTANTS (CRN)")
    print("="*60)
    
    # Step 1: Get all unique consultant records using GROUP BY
    # This reduces 581K records to ~5K grouped rows
    params = {
        "$select": (
            "cnslt_epc_organization_id, cnslt_name, cnslt_email, "
            "cnslt_phone, cnslt_city, cnslt_state, cnslt_zipcode, "
            "count(*) as application_count, "
            "max(funding_year) as latest_funding_year"
        ),
        "$group": (
            "cnslt_epc_organization_id, cnslt_name, cnslt_email, "
            "cnslt_phone, cnslt_city, cnslt_state, cnslt_zipcode"
        ),
        "$order": "cnslt_epc_organization_id",
        "$where": "cnslt_epc_organization_id IS NOT NULL",
    }
    
    raw_records = fetch_paginated(
        DATASETS["consultants"], params, 
        batch_size=5000,
        description="Unique Consultant Records (grouped)"
    )
    
    # Step 2: Also get the count of unique schools per consultant
    print("\n  Getting school counts per consultant...")
    school_count_params = {
        "$select": "cnslt_epc_organization_id, count(distinct epc_organization_id) as school_count",
        "$group": "cnslt_epc_organization_id",
        "$where": "cnslt_epc_organization_id IS NOT NULL",
    }
    school_counts_raw = fetch_paginated(
        DATASETS["consultants"], school_count_params,
        batch_size=5000,
        description="School counts per consultant"
    )
    school_count_map = {
        r["cnslt_epc_organization_id"]: r.get("school_count", "0")
        for r in school_counts_raw
    }
    
    # Step 3: Deduplicate by CRN (keep the one with most applications / latest year)
    crn_map = {}
    for record in raw_records:
        crn = record.get("cnslt_epc_organization_id", "").strip()
        if not crn:
            continue
        
        existing = crn_map.get(crn)
        if existing is None:
            crn_map[crn] = record
        else:
            # Keep the one with the latest funding year, or more applications
            new_year = record.get("latest_funding_year", "0")
            old_year = existing.get("latest_funding_year", "0")
            if new_year > old_year:
                crn_map[crn] = record
            elif new_year == old_year:
                new_count = int(record.get("application_count", 0))
                old_count = int(existing.get("application_count", 0))
                if new_count > old_count:
                    crn_map[crn] = record
    
    # Step 4: Build final consultant list
    consultants = []
    for crn, record in sorted(crn_map.items()):
        consultants.append(OrderedDict([
            ("crn", crn),
            ("consultant_name", record.get("cnslt_name", "").strip()),
            ("email", record.get("cnslt_email", "").strip()),
            ("phone", record.get("cnslt_phone", "").strip()),
            ("city", record.get("cnslt_city", "").strip()),
            ("state", record.get("cnslt_state", "").strip()),
            ("zipcode", record.get("cnslt_zipcode", "").strip()),
            ("schools_served", school_count_map.get(crn, "0")),
            ("total_applications", record.get("application_count", "0")),
            ("latest_funding_year", record.get("latest_funding_year", "")),
        ]))
    
    print(f"\n  ✓ {len(consultants):,} unique consultants identified")
    return consultants


# ============================================================================
# Vendor/Service Provider Scraper (SPIN)
# ============================================================================

def scrape_vendors() -> List[Dict]:
    """
    Scrape all service providers (vendors) from the USAC vendor dataset.
    Each record is already unique per SPIN.
    
    Fields fetched:
      - spin (SPIN number)
      - service_provider_name
      - phone_number
      - mailing_address_1, mailing_city, mailing_state, mailing_zip_code
      - physical_address_1, physical_city, physical_state, physical_zip_code
      - status (Active/Inactive)
    """
    print("\n" + "="*60)
    print("  PHASE 2: SCRAPING VENDORS (SPIN)")
    print("="*60)
    
    params = {
        "$select": (
            "spin, service_provider_name, status, phone_number, "
            "mailing_address_1, mailing_city, mailing_state, mailing_zip_code, "
            "physical_address_1, physical_city, physical_state, physical_zip_code, "
            "fcc_form_498_last_approved_date, last_updated_time"
        ),
        "$order": "spin",
    }
    
    raw_records = fetch_paginated(
        DATASETS["vendors"], params,
        batch_size=5000,
        description="All Service Providers / Vendors"
    )
    
    # Build final vendor list (already unique per SPIN)
    vendors = []
    seen_spins = set()
    
    for record in raw_records:
        spin = record.get("spin", "").strip()
        if not spin or spin in seen_spins:
            continue
        seen_spins.add(spin)
        
        vendors.append(OrderedDict([
            ("spin", spin),
            ("company_name", record.get("service_provider_name", "").strip()),
            ("status", record.get("status", "").strip()),
            ("phone", record.get("phone_number", "").strip()),
            ("mailing_address", record.get("mailing_address_1", "").strip()),
            ("mailing_city", record.get("mailing_city", "").strip()),
            ("mailing_state", record.get("mailing_state", "").strip()),
            ("mailing_zip", record.get("mailing_zip_code", "").strip()),
            ("physical_address", record.get("physical_address_1", "").strip()),
            ("physical_city", record.get("physical_city", "").strip()),
            ("physical_state", record.get("physical_state", "").strip()),
            ("physical_zip", record.get("physical_zip_code", "").strip()),
            ("last_updated", record.get("last_updated_time", "").strip()),
        ]))
    
    print(f"\n  ✓ {len(vendors):,} unique vendors/service providers identified")
    return vendors


# ============================================================================
# Entity Scraper (BEN)
# ============================================================================

def scrape_entities() -> List[Dict]:
    """
    Scrape all unique billed entities from the USAC Form 471 dataset.
    Fetches raw records with minimal fields and deduplicates locally by BEN.
    
    Available fields in srbr-2d59:
      - ben, organization_name, organization_entity_type_name, state
      - cnct_name (contact person name), cnct_email (contact person email)
      NOTE: No city/zip_code/street in this dataset
    """
    print("\n" + "="*60)
    print("  PHASE 3: SCRAPING ENTITIES (BEN)")
    print("="*60)
    
    # Fetch raw records year by year to avoid GROUP BY performance issues
    # Just select minimal fields to reduce transfer size
    FUNDING_YEARS = [str(y) for y in range(2016, 2027)]
    
    ben_map = {}  # ben -> best record
    total_raw = 0
    
    for year in FUNDING_YEARS:
        params = {
            "$select": (
                "ben, organization_name, organization_entity_type_name, "
                "state, cnct_name, cnct_email, "
                "funding_year, funding_commitment_request"
            ),
            "$where": f"funding_year='{year}' AND ben IS NOT NULL",
            "$order": "ben",
        }
        
        year_records = fetch_paginated(
            DATASETS["entities"], params,
            batch_size=10000,
            description=f"Entities for funding year {year}"
        )
        total_raw += len(year_records)
        
        # Merge into ben_map, keeping best record per BEN
        for record in year_records:
            ben = record.get("ben", "").strip()
            if not ben:
                continue
            
            existing = ben_map.get(ben)
            if existing is None:
                # First time seeing this BEN - initialize aggregation
                ben_map[ben] = {
                    **record,
                    "_frn_count": 1,
                    "_total_funding": float(record.get("funding_commitment_request", 0) or 0),
                    "_latest_year": record.get("funding_year", "0"),
                }
            else:
                # Update: prefer records with contact info, latest year
                existing["_frn_count"] += 1
                existing["_total_funding"] += float(record.get("funding_commitment_request", 0) or 0)
                
                new_year = record.get("funding_year", "0")
                if new_year > existing["_latest_year"]:
                    existing["_latest_year"] = new_year
                
                # Upgrade record if this one has email and old one doesn't,
                # or if same and this one is newer
                new_has_email = bool(record.get("cnct_email", "").strip())
                old_has_email = bool(existing.get("cnct_email", "").strip())
                new_has_name = bool(record.get("cnct_name", "").strip())
                old_has_name = bool(existing.get("cnct_name", "").strip())
                
                if (new_has_email and not old_has_email) or \
                   (new_has_email == old_has_email and new_has_name and not old_has_name) or \
                   (new_has_email == old_has_email and new_has_name == old_has_name and new_year > existing.get("funding_year", "0")):
                    # Preserve aggregated fields
                    frn_count = existing["_frn_count"]
                    total_funding = existing["_total_funding"]
                    latest_year = existing["_latest_year"]
                    existing.update(record)
                    existing["_frn_count"] = frn_count
                    existing["_total_funding"] = total_funding
                    existing["_latest_year"] = latest_year
        
        print(f"    → Unique BENs so far: {len(ben_map):,}")
    
    print(f"\n  Raw records processed: {total_raw:,}")
    
    # Build final entity list
    entities = []
    for ben, record in sorted(ben_map.items()):
        try:
            total_funding_str = f"${record.get('_total_funding', 0):,.2f}"
        except (ValueError, TypeError):
            total_funding_str = "$0.00"
        
        entities.append(OrderedDict([
            ("ben", ben),
            ("organization_name", record.get("organization_name", "").strip()),
            ("entity_type", record.get("organization_entity_type_name", "").strip()),
            ("contact_name", record.get("cnct_name", "").strip()),
            ("contact_email", record.get("cnct_email", "").strip()),
            ("state", record.get("state", "").strip()),
            ("total_frns", str(record.get("_frn_count", 0))),
            ("total_funding_committed", total_funding_str),
            ("latest_funding_year", record.get("_latest_year", "")),
        ]))
    
    print(f"\n  ✓ {len(entities):,} unique entities identified")
    print(f"  ✓ {sum(1 for e in entities if e['contact_email']):,} entities have contact emails")
    print(f"  ✓ {sum(1 for e in entities if e['contact_name']):,} entities have contact names")
    return entities


# ============================================================================
# CSV Export
# ============================================================================

def export_to_csv(records: List[Dict], filename: str, description: str = "") -> str:
    """Export records to CSV file."""
    if not records:
        print(f"  ✗ No records to export for {description}")
        return ""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    fieldnames = list(records[0].keys())
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"\n  ✓ Exported {len(records):,} {description} to: {filepath}")
    return filepath


# ============================================================================
# Summary Statistics
# ============================================================================

def print_summary(consultants, vendors, entities):
    """Print summary statistics."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n" + "="*70)
    print(f"  USAC DATA SCRAPING COMPLETE - {timestamp}")
    print("="*70)
    
    print(f"\n  📋 CONSULTANTS (CRN/ACRN)")
    print(f"     Total unique consultants: {len(consultants):,}")
    if consultants:
        with_email = sum(1 for c in consultants if c.get("email"))
        with_phone = sum(1 for c in consultants if c.get("phone"))
        print(f"     With email: {with_email:,} ({100*with_email/len(consultants):.1f}%)")
        print(f"     With phone: {with_phone:,} ({100*with_phone/len(consultants):.1f}%)")
    
    print(f"\n  🏢 VENDORS / SERVICE PROVIDERS (SPIN)")
    print(f"     Total unique vendors: {len(vendors):,}")
    if vendors:
        active = sum(1 for v in vendors if v.get("status", "").lower() == "active")
        with_phone = sum(1 for v in vendors if v.get("phone"))
        print(f"     Active: {active:,} ({100*active/len(vendors):.1f}%)")
        print(f"     With phone: {with_phone:,} ({100*with_phone/len(vendors):.1f}%)")
    
    print(f"\n  🏫 ENTITIES (BEN)")
    print(f"     Total unique entities: {len(entities):,}")
    if entities:
        with_email = sum(1 for e in entities if e.get("contact_email"))
        print(f"     With contact email: {with_email:,} ({100*with_email/len(entities):.1f}%)")
    
    print(f"\n  📁 Output Directory: {OUTPUT_DIR}")
    print("="*70)


# ============================================================================
# Main
# ============================================================================

def main():
    """Main entry point - scrape all USAC data and export to CSV."""
    start_time = time.time()
    
    print("\n" + "★"*70)
    print("  USAC E-RATE FULL DATA SCRAPER")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("  Scraping: Consultants (CRN), Vendors (SPIN), Entities (BEN)")
    print("★"*70)
    
    # Allow running individual phases via command-line args
    phases = sys.argv[1:] if len(sys.argv) > 1 else ["consultants", "vendors", "entities"]
    
    consultants = []
    vendors = []
    entities = []
    
    # Phase 1: Consultants
    if "consultants" in phases:
        try:
            consultants = scrape_consultants()
            export_to_csv(consultants, "usac_consultants.csv", "consultants")
        except Exception as e:
            print(f"\n  ✗ ERROR scraping consultants: {e}")
            import traceback
            traceback.print_exc()
    
    # Phase 2: Vendors
    if "vendors" in phases:
        try:
            vendors = scrape_vendors()
            export_to_csv(vendors, "usac_vendors.csv", "vendors")
        except Exception as e:
            print(f"\n  ✗ ERROR scraping vendors: {e}")
            import traceback
            traceback.print_exc()
    
    # Phase 3: Entities
    if "entities" in phases:
        try:
            entities = scrape_entities()
            export_to_csv(entities, "usac_entities.csv", "entities")
        except Exception as e:
            print(f"\n  ✗ ERROR scraping entities: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    elapsed = time.time() - start_time
    print_summary(consultants, vendors, entities)
    print(f"\n  ⏱ Total elapsed time: {elapsed/60:.1f} minutes")
    
    # Also export a combined summary JSON
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    summary = {
        "scrape_timestamp": datetime.now().isoformat(),
        "elapsed_seconds": round(elapsed, 1),
        "consultants_count": len(consultants),
        "vendors_count": len(vendors),
        "entities_count": len(entities),
        "output_files": {
            "consultants": os.path.join(OUTPUT_DIR, "usac_consultants.csv"),
            "vendors": os.path.join(OUTPUT_DIR, "usac_vendors.csv"),
            "entities": os.path.join(OUTPUT_DIR, "usac_entities.csv"),
        }
    }
    summary_path = os.path.join(OUTPUT_DIR, "scrape_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"  📄 Summary saved to: {summary_path}\n")


if __name__ == "__main__":
    main()
