#!/usr/bin/env python3
"""
BEN Enricher - Fetches entity information from USAC APIs for BEN numbers
Uses robust retry logic and saves progress incrementally.
"""

import requests
import csv
import json
import time
import sys
import os
from typing import Dict, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_URL = "https://opendata.usac.org/resource/srbr-2d59.json"
PROGRESS_FILE = "ben_enricher_progress.json"


def create_session() -> requests.Session:
    """Create a robust session with retry logic"""
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[408, 429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=5, pool_maxsize=5)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({'User-Agent': 'Mozilla/5.0 SkyRate/1.0'})
    return session


def fetch_ben_data(session: requests.Session, ben: str) -> Dict:
    """Fetch entity data for a single BEN"""
    result = {
        "Entity Name": "",
        "Type": "",
        "Address": "",
        "BEN Number": ben,
        "FRN Number": "",
        "DUB Number": "",
        "SAM ID": "",
        "Contract Number": "",
        "Students Over 3": "",
        "Students with Lunch": "",
        "CEP Score": "",
        "Physical Size": "",
        "District Percentage": "",
        "State": "",
        "City": "",
        "Zip": "",
        "Total Funding Committed": "",
        "Funding Years Active": "",
    }
    
    params = {"ben": ben, "$limit": 50, "$order": "funding_year DESC"}
    
    for attempt in range(3):
        try:
            response = session.get(BASE_URL, params=params, timeout=45)
            if response.status_code == 200:
                data = response.json()
                if data:
                    rec = data[0]
                    result["Entity Name"] = rec.get("organization_name", "")
                    result["Type"] = rec.get("organization_entity_type_name", "")
                    result["State"] = rec.get("state", "")
                    result["City"] = rec.get("city", "")
                    result["Zip"] = rec.get("zip_code", "")
                    
                    # Address
                    addr = [rec.get("street", ""), rec.get("city", ""), 
                            rec.get("state", ""), rec.get("zip_code", "")]
                    result["Address"] = ", ".join(filter(None, addr))
                    
                    # Aggregate
                    frns, years, total = set(), set(), 0.0
                    for r in data:
                        if r.get("funding_request_number"):
                            frns.add(str(r.get("funding_request_number")))
                        if r.get("funding_year"):
                            years.add(str(r.get("funding_year")))
                        try:
                            total += float(r.get("funding_commitment_request", 0) or 0)
                        except: pass
                    
                    if frns: result["FRN Number"] = sorted(frns)[-1]
                    if total > 0: result["Total Funding Committed"] = f"${total:,.2f}"
                    if years: result["Funding Years Active"] = ", ".join(sorted(years, reverse=True)[:5])
                return result
            elif response.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            else:
                break
        except requests.exceptions.Timeout:
            time.sleep(3)
            continue
        except Exception as e:
            time.sleep(2)
            continue
    
    return result


def read_ben_list(filepath: str) -> List[str]:
    """Read BEN numbers from CSV file"""
    bens = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        for line in f:
            ben = line.strip()
            if ben and ben.upper() != 'BEN' and ben.isdigit():
                bens.append(ben)
    return bens


def load_progress() -> Dict:
    """Load saved progress"""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"processed": {}, "completed": []}


def save_progress(progress: Dict):
    """Save progress to file"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def main():
    input_file = "BEN.csv"
    output_file = "BEN_enriched.csv"
    
    print("=" * 60)
    print("BEN Enricher - USAC API Data Fetcher")
    print("=" * 60)
    
    # Read BENs
    print(f"\n📄 Reading BEN numbers from {input_file}...")
    bens = read_ben_list(input_file)
    print(f"   Found {len(bens)} BEN numbers")
    
    if not bens:
        print("❌ No valid BEN numbers found!")
        return
    
    # Load previous progress
    progress = load_progress()
    completed = set(progress.get("completed", []))
    all_data = progress.get("processed", {})
    
    if completed:
        print(f"   Resuming... {len(completed)} already processed")
    
    # Create session
    session = create_session()
    
    # Process BENs
    print(f"\n🔍 Fetching entity data from USAC APIs...")
    
    for i, ben in enumerate(bens):
        if ben in completed:
            continue
        
        pct = (i + 1) * 100 // len(bens)
        sys.stdout.write(f"\r   [{i+1}/{len(bens)}] ({pct}%) BEN {ben}...")
        sys.stdout.flush()
        
        data = fetch_ben_data(session, ben)
        all_data[ben] = data
        completed.add(ben)
        
        # Save progress every 10 records
        if len(completed) % 10 == 0:
            progress["processed"] = all_data
            progress["completed"] = list(completed)
            save_progress(progress)
        
        # Rate limiting
        time.sleep(0.5)
    
    # Final save
    progress["processed"] = all_data
    progress["completed"] = list(completed)
    save_progress(progress)
    
    # Write CSV
    print(f"\n\n📝 Writing enriched data to {output_file}...")
    columns = [
        "Entity Name", "Type", "Address", "BEN Number", "FRN Number",
        "DUB Number", "SAM ID", "Contract Number", "Students Over 3",
        "Students with Lunch", "CEP Score", "Physical Size", "District Percentage",
        "State", "City", "Zip", "Total Funding Committed", "Funding Years Active"
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for ben in bens:
            if ben in all_data:
                writer.writerow({k: v for k, v in all_data[ben].items() if k in columns})
    
    # Summary
    found = sum(1 for b in bens if all_data.get(b, {}).get("Entity Name"))
    print(f"\n✅ Done!")
    print(f"📊 Found: {found}/{len(bens)} entities")
    print(f"📁 Output: {output_file}")
    
    # Clean up progress file
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    
    print("=" * 60)


if __name__ == "__main__":
    main()
