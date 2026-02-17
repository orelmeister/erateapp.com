"""
USAC Open Data Fetcher
Handles fetching and filtering data from the USAC E-Rate Open Data API
"""
import requests
import json
from typing import List, Dict, Optional
import time


class USACDataFetcher:
    """Fetch and manage USAC E-Rate data"""
    
    BASE_URL = "https://opendata.usac.org/resource"
    DATASET_ID = "srbr-2d59"  # E-Rate Form 471 dataset
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        self.cache = {}
    
    def fetch_data(self, funding_year: str, limit: int = 1000, offset: int = 0) -> List[Dict]:
        """
        Fetch E-Rate data for a specific funding year
        
        Args:
            funding_year: The funding year to filter (e.g., "2024")
            limit: Maximum number of records to fetch
            offset: Offset for pagination
            
        Returns:
            List of records as dictionaries
        """
        cache_key = f"{funding_year}_{limit}_{offset}"
        if cache_key in self.cache:
            print(f"✓ Using cached data for {funding_year}")
            return self.cache[cache_key]
        
        url = f"{self.BASE_URL}/{self.DATASET_ID}.json"
        params = {
            "$where": f"funding_year = '{funding_year}'",
            "$limit": limit,
            "$offset": offset
        }
        
        try:
            print(f"⟳ Fetching data for funding year {funding_year}...")
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.cache[cache_key] = data
                print(f"✓ Fetched {len(data)} records for year {funding_year}")
                return data
            else:
                print(f"✗ Error {response.status_code}: {response.text}")
                return []
        except Exception as e:
            print(f"✗ Error fetching data: {e}")
            return []
    
    def fetch_all_years_data(self, funding_years: List[str], max_per_year: int = 5000) -> Dict[str, List[Dict]]:
        """
        Fetch data for multiple funding years
        
        Args:
            funding_years: List of funding years to fetch
            max_per_year: Maximum records per year
            
        Returns:
            Dictionary mapping year to records
        """
        all_data = {}
        for year in funding_years:
            data = self.fetch_data(year, limit=max_per_year)
            all_data[year] = data
            time.sleep(0.5)  # Be nice to the API
        return all_data
    
    def filter_by_status(self, data: List[Dict], status: str) -> List[Dict]:
        """Filter records by funding status"""
        return [record for record in data if record.get("form_471_frn_status_name", "").lower() == status.lower()]
    
    def filter_denied_or_unfunded(self, data: List[Dict]) -> List[Dict]:
        """Get records that were denied or not funded"""
        denied_statuses = ["denied", "not funded", "rejected", "cancelled"]
        return [
            record for record in data 
            if any(status in record.get("form_471_frn_status_name", "").lower() for status in denied_statuses)
        ]
    
    def get_by_organization(self, data: List[Dict], organization_name: str) -> List[Dict]:
        """Filter records by organization name (case-insensitive partial match)"""
        org_lower = organization_name.lower()
        return [
            record for record in data 
            if org_lower in record.get("organization_name", "").lower()
        ]
    
    def get_by_state(self, data: List[Dict], state_code: str) -> List[Dict]:
        """Filter records by state code"""
        return [record for record in data if record.get("state", "").upper() == state_code.upper()]
    
    def get_statistics(self, data: List[Dict]) -> Dict:
        """Get basic statistics about the data"""
        if not data:
            return {}
        
        total = len(data)
        funded = len([r for r in data if r.get("form_471_frn_status_name", "").lower() == "funded"])
        denied = len(self.filter_denied_or_unfunded(data))
        
        total_funding = sum(
            float(r.get("funding_commitment_request", 0) or 0) 
            for r in data 
            if r.get("funding_commitment_request")
        )
        
        states = set(r.get("state", "") for r in data if r.get("state"))
        organizations = set(r.get("organization_name", "") for r in data if r.get("organization_name"))
        
        return {
            "total_applications": total,
            "funded": funded,
            "denied_or_unfunded": denied,
            "total_funding_requested": f"${total_funding:,.2f}",
            "unique_states": len(states),
            "unique_organizations": len(organizations)
        }
