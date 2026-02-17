"""
E-Rate Data Query Script
This script fetches and queries E-Rate funding data from USAC's Open Data API
"""

import requests
import json
import argparse
import sys
from typing import List, Dict, Any, Optional
from collections import Counter


class ERateDataQuery:
    """Class to query E-Rate funding data"""
    
    def __init__(self, base_url: str = "https://opendata.usac.org/resource/bd9t-w7tr.json"):
        """
        Initialize the query object
        
        Args:
            base_url: The API endpoint URL
        """
        self.base_url = base_url
        self.data: List[Dict[str, Any]] = []
    
    def fetch_data(self, limit: int = 1000, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Fetch data from the API
        
        Args:
            limit: Maximum number of records to fetch (default 1000)
            offset: Number of records to skip (for pagination)
            
        Returns:
            List of records
        """
        try:
            params = {
                '$limit': limit,
                '$offset': offset
            }
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            self.data = response.json()
            print(f"✓ Successfully fetched {len(self.data)} records")
            return self.data
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching data: {e}")
            return []
    
    def filter_by_state(self, state: str) -> List[Dict[str, Any]]:
        """Filter records by state"""
        return [record for record in self.data if record.get('state', '').upper() == state.upper()]
    
    def filter_by_funding_year(self, year: str) -> List[Dict[str, Any]]:
        """Filter records by funding year"""
        return [record for record in self.data if record.get('funding_year') == str(year)]
    
    def filter_by_organization(self, org_name: str) -> List[Dict[str, Any]]:
        """Filter records by organization name (case-insensitive partial match)"""
        org_name_lower = org_name.lower()
        return [record for record in self.data 
                if org_name_lower in record.get('organization_name', '').lower()]
    
    def filter_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Filter records by FRN status"""
        return [record for record in self.data 
                if record.get('form_471_frn_status_name', '').lower() == status.lower()]
    
    def filter_by_service_type(self, service_type: str) -> List[Dict[str, Any]]:
        """Filter records by service type (partial match)"""
        service_type_lower = service_type.lower()
        return [record for record in self.data 
                if service_type_lower in record.get('form_471_service_type_name', '').lower()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get summary statistics of the data"""
        if not self.data:
            return {"error": "No data loaded"}
        
        states = [record.get('state', 'Unknown') for record in self.data]
        years = [record.get('funding_year', 'Unknown') for record in self.data]
        statuses = [record.get('form_471_frn_status_name', 'Unknown') for record in self.data]
        entity_types = [record.get('organization_entity_type_name', 'Unknown') for record in self.data]
        
        return {
            "total_records": len(self.data),
            "states": dict(Counter(states).most_common(10)),
            "funding_years": dict(Counter(years)),
            "statuses": dict(Counter(statuses)),
            "entity_types": dict(Counter(entity_types).most_common(10))
        }
    
    def search(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Search records with multiple filters
        
        Args:
            **kwargs: Filters to apply (e.g., state='NY', funding_year='2025', status='Funded')
            
        Returns:
            Filtered list of records
        """
        results = self.data
        
        if 'state' in kwargs:
            results = [r for r in results if r.get('state', '').upper() == kwargs['state'].upper()]
        
        if 'funding_year' in kwargs:
            results = [r for r in results if r.get('funding_year') == str(kwargs['funding_year'])]
        
        if 'status' in kwargs:
            status_lower = kwargs['status'].lower()
            results = [r for r in results if status_lower in r.get('form_471_frn_status_name', '').lower()]
        
        if 'organization' in kwargs:
            org_lower = kwargs['organization'].lower()
            results = [r for r in results if org_lower in r.get('organization_name', '').lower()]
        
        if 'service_type' in kwargs:
            service_lower = kwargs['service_type'].lower()
            results = [r for r in results if service_lower in r.get('form_471_service_type_name', '').lower()]
        
        return results
    
    def display_records(self, records: List[Dict[str, Any]], max_records: int = 10):
        """Display records in a readable format"""
        if not records:
            print("\n✗ No records found")
            return
        
        print(f"\n✓ Found {len(records)} record(s)")
        print("=" * 100)
        
        for i, record in enumerate(records[:max_records], 1):
            print(f"\nRecord {i}:")
            print(f"  Organization: {record.get('organization_name', 'N/A')}")
            print(f"  State: {record.get('state', 'N/A')}")
            print(f"  Funding Year: {record.get('funding_year', 'N/A')}")
            print(f"  Status: {record.get('form_471_frn_status_name', 'N/A')}")
            print(f"  Service Type: {record.get('form_471_service_type_name', 'N/A')}")
            print(f"  Discount: {record.get('dis_pct_band', 'N/A')}")
            print(f"  Application #: {record.get('application_number', 'N/A')}")
            print("-" * 100)
        
        if len(records) > max_records:
            print(f"\n... and {len(records) - max_records} more record(s)")
    
    def export_to_json(self, records: List[Dict[str, Any]], filename: str):
        """Export records to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            print(f"✓ Exported {len(records)} records to {filename}")
        except Exception as e:
            print(f"✗ Error exporting data: {e}")


def run_cli_query(args):
    """Run query based on command-line arguments"""
    print("=" * 100)
    print("E-RATE DATA QUERY TOOL")
    print("=" * 100)
    
    # Initialize the query object
    query = ERateDataQuery()
    
    # Fetch data
    print(f"\nFetching data from API (limit: {args.limit})...")
    query.fetch_data(limit=args.limit, offset=args.offset)
    
    if not query.data:
        print("✗ No data fetched. Exiting.")
        return
    
    # If stats flag is set, show statistics
    if args.stats:
        print("\n" + "=" * 100)
        print("DATA STATISTICS")
        print("=" * 100)
        stats = query.get_statistics()
        print(f"\nTotal Records: {stats['total_records']}")
        
        print("\nTop 10 States:")
        for state, count in stats['states'].items():
            print(f"  {state}: {count}")
        
        print("\nFunding Years:")
        for year, count in stats['funding_years'].items():
            print(f"  {year}: {count}")
        
        print("\nStatuses:")
        for status, count in stats['statuses'].items():
            print(f"  {status}: {count}")
        
        print("\nTop 10 Entity Types:")
        for entity_type, count in stats['entity_types'].items():
            print(f"  {entity_type}: {count}")
        return
    
    # Build search criteria
    search_criteria = {}
    if args.state:
        search_criteria['state'] = args.state
    if args.year:
        search_criteria['funding_year'] = args.year
    if args.status:
        search_criteria['status'] = args.status
    if args.organization:
        search_criteria['organization'] = args.organization
    if args.service_type:
        search_criteria['service_type'] = args.service_type
    
    # Execute search
    if search_criteria:
        print("\n" + "=" * 100)
        print("SEARCH CRITERIA")
        print("=" * 100)
        for key, value in search_criteria.items():
            print(f"  {key}: {value}")
        
        results = query.search(**search_criteria)
    else:
        results = query.data
    
    # Display results
    query.display_records(results, max_records=args.max_display)
    
    # Export if filename provided
    if args.export:
        query.export_to_json(results, args.export)


def interactive_mode():
    """Run interactive mode"""
    print("=" * 100)
    print("E-RATE DATA QUERY TOOL - INTERACTIVE MODE")
    print("=" * 100)
    
    query = ERateDataQuery()
    
    # Fetch data
    while True:
        try:
            limit = input("\nEnter number of records to fetch (default 1000): ").strip()
            limit = int(limit) if limit else 1000
            break
        except ValueError:
            print("Please enter a valid number")
    
    print(f"\nFetching {limit} records...")
    query.fetch_data(limit=limit)
    
    if not query.data:
        print("✗ No data fetched. Exiting.")
        return
    
    while True:
        print("\n" + "=" * 100)
        print("QUERY OPTIONS")
        print("=" * 100)
        print("1. Filter by State")
        print("2. Filter by Funding Year")
        print("3. Filter by Organization Name")
        print("4. Filter by Status")
        print("5. Filter by Service Type")
        print("6. Complex Search (multiple criteria)")
        print("7. Show Statistics")
        print("8. Export Results")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            state = input("Enter state code (e.g., NY, CA): ").strip()
            results = query.filter_by_state(state)
            query.display_records(results, max_records=10)
            
        elif choice == '2':
            year = input("Enter funding year (e.g., 2025): ").strip()
            results = query.filter_by_funding_year(year)
            query.display_records(results, max_records=10)
            
        elif choice == '3':
            org_name = input("Enter organization name (partial match): ").strip()
            results = query.filter_by_organization(org_name)
            query.display_records(results, max_records=10)
            
        elif choice == '4':
            status = input("Enter status (e.g., Funded, Cancelled, Denied): ").strip()
            results = query.filter_by_status(status)
            query.display_records(results, max_records=10)
            
        elif choice == '5':
            service = input("Enter service type (e.g., Internet Access): ").strip()
            results = query.filter_by_service_type(service)
            query.display_records(results, max_records=10)
            
        elif choice == '6':
            criteria = {}
            state = input("State (leave blank to skip): ").strip()
            if state:
                criteria['state'] = state
            year = input("Funding Year (leave blank to skip): ").strip()
            if year:
                criteria['funding_year'] = year
            status = input("Status (leave blank to skip): ").strip()
            if status:
                criteria['status'] = status
            org = input("Organization (leave blank to skip): ").strip()
            if org:
                criteria['organization'] = org
            service = input("Service Type (leave blank to skip): ").strip()
            if service:
                criteria['service_type'] = service
            
            if criteria:
                results = query.search(**criteria)
                query.display_records(results, max_records=10)
                
                export_choice = input("\nExport results? (y/n): ").strip().lower()
                if export_choice == 'y':
                    filename = input("Enter filename (e.g., results.json): ").strip()
                    if filename:
                        query.export_to_json(results, filename)
            else:
                print("No criteria entered")
                
        elif choice == '7':
            stats = query.get_statistics()
            print("\n" + "=" * 100)
            print("STATISTICS")
            print("=" * 100)
            print(f"\nTotal Records: {stats['total_records']}")
            
            print("\nTop 10 States:")
            for state, count in stats['states'].items():
                print(f"  {state}: {count}")
            
            print("\nFunding Years:")
            for year, count in stats['funding_years'].items():
                print(f"  {year}: {count}")
            
            print("\nStatuses:")
            for status, count in stats['statuses'].items():
                print(f"  {status}: {count}")
                
        elif choice == '8':
            filename = input("Enter filename to export all data (e.g., results.json): ").strip()
            if filename:
                query.export_to_json(query.data, filename)
                
        elif choice == '9':
            print("\nGoodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1-9.")


def main():
    """Main function with CLI argument parsing"""
    parser = argparse.ArgumentParser(
        description='Query E-Rate funding data from USAC Open Data API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python query_erate_data.py -i
  
  # Show statistics
  python query_erate_data.py --stats
  
  # Search by state
  python query_erate_data.py --state NY --max-display 20
  
  # Search by multiple criteria
  python query_erate_data.py --state CA --year 2025 --status Funded
  
  # Export results
  python query_erate_data.py --state TX --export texas_results.json
  
  # Complex query with export
  python query_erate_data.py --state NY --year 2025 --service-type "Internet Access" --export ny_internet_2025.json
        """
    )
    
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Run in interactive mode')
    parser.add_argument('--stats', action='store_true',
                        help='Show data statistics only')
    parser.add_argument('--state', type=str,
                        help='Filter by state code (e.g., NY, CA)')
    parser.add_argument('--year', type=str,
                        help='Filter by funding year (e.g., 2025)')
    parser.add_argument('--status', type=str,
                        help='Filter by status (e.g., Funded, Cancelled, Denied)')
    parser.add_argument('--organization', type=str,
                        help='Filter by organization name (partial match)')
    parser.add_argument('--service-type', type=str,
                        help='Filter by service type (e.g., "Internet Access")')
    parser.add_argument('--limit', type=int, default=1000,
                        help='Maximum number of records to fetch (default: 1000)')
    parser.add_argument('--offset', type=int, default=0,
                        help='Number of records to skip (for pagination, default: 0)')
    parser.add_argument('--max-display', type=int, default=10,
                        help='Maximum number of records to display (default: 10)')
    parser.add_argument('--export', type=str,
                        help='Export results to JSON file')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n" + "=" * 100)
        print("TIP: Use -i or --interactive for interactive mode")
        print("=" * 100)
        return
    
    # Run interactive mode if requested
    if args.interactive:
        interactive_mode()
    else:
        run_cli_query(args)


if __name__ == "__main__":
    main()
