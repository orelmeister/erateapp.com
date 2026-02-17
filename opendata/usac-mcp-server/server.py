#!/usr/bin/env python3
"""
USAC E-Rate Open Data MCP Server

This MCP server provides tools to query and analyze E-Rate program data from USAC.
Compatible with Claude Desktop and other MCP clients.
"""

import json
import sys
import asyncio
from typing import Any, Dict, List, Optional
import requests
import pandas as pd
from datetime import datetime

# MCP Protocol imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Field name mapping from friendly names to API field names
FIELD_NAME_MAPPING = {
    'entity_type': 'organization_entity_type_name',
    'application_status': 'form_471_frn_status_name',
    'applicant_name': 'organization_name',
    'category_of_service': 'form_471_service_type_name',
    'amount_of_commitment_request': 'funding_commitment_request',
    'state': 'state'  # Correct field name
}


def map_field_name(field: str) -> str:
    """Convert friendly field name to actual API field name"""
    return FIELD_NAME_MAPPING.get(field, field)


class USACDataClient:
    """Client for fetching E-Rate data from USAC Open Data API"""
    
    BASE_URL = "https://opendata.usac.org/resource/srbr-2d59.json"
    MAX_BATCH_SIZE = 200  # API returns max 200 records per request
    
    def __init__(self, max_records: int = 1000):
        self.max_records = max_records
        
    def fetch_data(self, year: Optional[int] = None, filters: Optional[Dict] = None, limit: int = None) -> pd.DataFrame:
        """
        Fetch data from USAC API with optional filters and pagination
        
        Args:
            year: Funding year to filter by
            filters: Dictionary of field:value pairs to filter by
            limit: Maximum number of records to fetch (uses max_records if not specified)
        
        Returns:
            pandas DataFrame with the fetched data
        """
        limit = limit or self.max_records
        all_data = []
        offset = 0
        
        while len(all_data) < limit:
            batch_size = min(self.MAX_BATCH_SIZE, limit - len(all_data))
            
            params = {
                "$limit": batch_size,
                "$offset": offset,
                "$order": "funding_year DESC, funding_commitment_request DESC"
            }
            
            # Build WHERE clause for better compatibility
            where_clauses = []
            if year:
                where_clauses.append(f"funding_year='{year}'")
            
            if filters:
                for field, value in filters.items():
                    api_field = map_field_name(field)
                    # Handle list values (multiple states, etc.)
                    if isinstance(value, list):
                        if len(value) == 1:
                            where_clauses.append(f"{api_field}='{value[0]}'")
                        elif len(value) > 1:
                            or_conditions = [f"{api_field}='{v}'" for v in value]
                            where_clauses.append(f"({' OR '.join(or_conditions)})")
                    elif isinstance(value, str):
                        where_clauses.append(f"{api_field}='{value}'")
                    else:
                        where_clauses.append(f"{api_field}='{value}'")
            
            if where_clauses:
                params["$where"] = " AND ".join(where_clauses)
            
            try:
                response = requests.get(self.BASE_URL, params=params, timeout=30)
                response.raise_for_status()
                
                batch_data = response.json()
                if not batch_data:
                    break  # No more data available
                
                all_data.extend(batch_data)
                offset += len(batch_data)
                
                # If we got less than requested, we've reached the end
                if len(batch_data) < batch_size:
                    break
                    
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data: {str(e)}", file=sys.stderr)
                break
        
        if not all_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(all_data)
        
        # Rename API field names to friendly names
        reverse_mapping = {v: k for k, v in FIELD_NAME_MAPPING.items()}
        df = df.rename(columns=reverse_mapping)
        
        # Convert numeric columns
        numeric_columns = [
            'funding_year', 
            'amount_of_commitment_request',
            'funding_commitment_request',
            'total_authorized_disbursement',
            'dis_pct'
        ]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def get_field_values(self, field: str, year: Optional[int] = None) -> List[str]:
        """Get unique values for a specific field"""
        api_field = map_field_name(field)
        
        params = {
            "$select": f"DISTINCT {api_field}",
            "$limit": 1000
        }
        
        if year:
            params["$where"] = f"funding_year='{year}'"
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return sorted([item[api_field] for item in data if api_field in item and item[api_field]])
        except:
            return []


# Initialize MCP server and client
app = Server("usac-erate-data")
client = USACDataClient(max_records=1000)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools for USAC E-Rate data access"""
    return [
        Tool(
            name="query_erate_data",
            description="""Query USAC E-Rate program data with flexible filtering options.
            
            This tool provides access to comprehensive E-Rate funding data including:
            - Application status (Funded, Denied, Cancelled, Unfunded)
            - Entity information (Schools, Libraries, Consortiums)
            - Funding amounts and commitments
            - Service types and categories
            - Geographic data (state, city)
            - Temporal data (funding years from 2016-2025)
            
            Returns up to 1000 records by default, with pagination support.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "Funding year (e.g., 2024, 2025). Leave empty for all years.",
                        "minimum": 2016,
                        "maximum": 2025
                    },
                    "application_status": {
                        "type": "string",
                        "description": "Filter by application status",
                        "enum": ["Funded", "Denied", "Cancelled", "Unfunded"]
                    },
                    "entity_type": {
                        "type": "string",
                        "description": "Filter by organization type",
                        "enum": ["School", "Library", "School District", "Library System", "Consortium"]
                    },
                    "state": {
                        "type": "string",
                        "description": "Two-letter state code (e.g., CA, NY, TX)"
                    },
                    "category_of_service": {
                        "type": "string",
                        "description": "Service category filter"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of records to return (default: 1000)",
                        "default": 1000,
                        "minimum": 1,
                        "maximum": 10000
                    }
                }
            }
        ),
        Tool(
            name="get_field_values",
            description="""Get all unique values for a specific field in the E-Rate dataset.
            
            Useful for discovering available options before querying, such as:
            - Available states
            - Service categories
            - Entity types
            - Application statuses
            
            Can be filtered by year to see values for a specific funding year.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "field": {
                        "type": "string",
                        "description": "Field name to get values for",
                        "enum": [
                            "application_status",
                            "entity_type",
                            "state",
                            "category_of_service",
                            "form_471_service_type_name"
                        ]
                    },
                    "year": {
                        "type": "integer",
                        "description": "Optional: Filter values by funding year",
                        "minimum": 2016,
                        "maximum": 2025
                    }
                },
                "required": ["field"]
            }
        ),
        Tool(
            name="search_entities",
            description="""Search for specific schools, libraries, or other organizations by name.
            
            Returns detailed funding information for matching entities, including:
            - Organization details
            - Funding history
            - Application statuses
            - Service categories""",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_name": {
                        "type": "string",
                        "description": "Name or partial name of the organization to search for"
                    },
                    "year": {
                        "type": "integer",
                        "description": "Optional: Filter by funding year",
                        "minimum": 2016,
                        "maximum": 2025
                    },
                    "state": {
                        "type": "string",
                        "description": "Optional: Filter by state (two-letter code)"
                    }
                },
                "required": ["entity_name"]
            }
        ),
        Tool(
            name="get_statistics",
            description="""Get aggregate statistics for E-Rate program data for a specific year.
            
            Provides insights including:
            - Total funding requested and committed
            - Number of applicants
            - Breakdown by entity type
            - Breakdown by application status
            - Top funded states""",
            inputSchema={
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "Funding year to get statistics for",
                        "minimum": 2016,
                        "maximum": 2025
                    }
                },
                "required": ["year"]
            }
        ),
        Tool(
            name="analyze_denials",
            description="""Analyze denied E-Rate applications to identify patterns and trends.
            
            Provides insights on:
            - Common denial reasons
            - Geographic patterns
            - Entity types most affected
            - Funding amounts involved""",
            inputSchema={
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "Optional: Focus on a specific funding year",
                        "minimum": 2016,
                        "maximum": 2025
                    }
                },
                "required": ["year"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls from MCP clients"""
    
    try:
        if name == "query_erate_data":
            # Extract filter parameters
            year = arguments.get("year")
            limit = arguments.get("limit", 1000)
            
            filters = {}
            for key in ["application_status", "entity_type", "state", "category_of_service"]:
                if key in arguments and arguments[key]:
                    filters[key] = arguments[key]
            
            # Fetch data
            df = client.fetch_data(year=year, filters=filters, limit=limit)
            
            if df.empty:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "success",
                        "count": 0,
                        "message": "No records found matching the criteria",
                        "data": []
                    }, indent=2)
                )]
            
            # Convert to JSON-friendly format
            records = df.to_dict('records')
            
            # Create summary
            summary = {
                "status": "success",
                "count": len(records),
                "years": sorted(df['funding_year'].dropna().unique().tolist()) if 'funding_year' in df.columns else [],
                "total_funding_requested": float(df['amount_of_commitment_request'].sum()) if 'amount_of_commitment_request' in df.columns else 0,
                "data": records[:100]  # Limit to first 100 for display
            }
            
            if len(records) > 100:
                summary["note"] = f"Showing first 100 of {len(records)} records"
            
            return [TextContent(
                type="text",
                text=json.dumps(summary, indent=2, default=str)
            )]
        
        elif name == "get_field_values":
            field = arguments["field"]
            year = arguments.get("year")
            
            values = client.get_field_values(field, year)
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "field": field,
                    "year": year,
                    "count": len(values),
                    "values": values
                }, indent=2)
            )]
        
        elif name == "search_entities":
            entity_name = arguments["entity_name"]
            year = arguments.get("year")
            state = arguments.get("state")
            
            # Build filter
            filters = {}
            if state:
                filters["state"] = state
            
            # Fetch data
            df = client.fetch_data(year=year, filters=filters, limit=1000)
            
            if df.empty:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "success",
                        "count": 0,
                        "message": "No entities found",
                        "data": []
                    }, indent=2)
                )]
            
            # Filter by name (case-insensitive partial match)
            name_col = 'applicant_name' if 'applicant_name' in df.columns else 'organization_name'
            if name_col in df.columns:
                mask = df[name_col].str.contains(entity_name, case=False, na=False)
                df = df[mask]
            
            records = df.to_dict('records')
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "search_term": entity_name,
                    "count": len(records),
                    "data": records[:50]  # Limit to first 50
                }, indent=2, default=str)
            )]
        
        elif name == "get_statistics":
            year = arguments["year"]
            
            # Fetch data for the year
            df = client.fetch_data(year=year, limit=10000)
            
            if df.empty:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "success",
                        "year": year,
                        "message": "No data found for this year",
                        "statistics": {}
                    }, indent=2)
                )]
            
            # Calculate statistics
            stats = {
                "year": year,
                "total_applications": len(df),
                "total_funding_requested": float(df['amount_of_commitment_request'].sum()) if 'amount_of_commitment_request' in df.columns else 0,
                "unique_applicants": int(df['applicant_name'].nunique()) if 'applicant_name' in df.columns else 0,
            }
            
            # Breakdown by status
            if 'application_status' in df.columns:
                stats["by_status"] = df['application_status'].value_counts().to_dict()
            
            # Breakdown by entity type
            if 'entity_type' in df.columns:
                stats["by_entity_type"] = df['entity_type'].value_counts().to_dict()
            
            # Top states
            if 'state' in df.columns:
                stats["top_states"] = df['state'].value_counts().head(10).to_dict()
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "statistics": stats
                }, indent=2, default=str)
            )]
        
        elif name == "analyze_denials":
            year = arguments.get("year")
            
            # Fetch denied applications
            filters = {"application_status": "Denied"}
            df = client.fetch_data(year=year, filters=filters, limit=5000)
            
            if df.empty:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "success",
                        "year": year,
                        "message": "No denied applications found",
                        "analysis": {}
                    }, indent=2)
                )]
            
            # Analyze denials
            analysis = {
                "year": year,
                "total_denials": len(df),
                "total_denied_amount": float(df['amount_of_commitment_request'].sum()) if 'amount_of_commitment_request' in df.columns else 0,
            }
            
            # By entity type
            if 'entity_type' in df.columns:
                analysis["by_entity_type"] = df['entity_type'].value_counts().to_dict()
            
            # By state
            if 'state' in df.columns:
                analysis["by_state"] = df['state'].value_counts().head(10).to_dict()
            
            # By service category
            if 'category_of_service' in df.columns:
                analysis["by_service_category"] = df['category_of_service'].value_counts().head(10).to_dict()
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "analysis": analysis,
                    "sample_denials": df.head(20).to_dict('records')
                }, indent=2, default=str)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "error",
                    "message": f"Unknown tool: {name}"
                })
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "error",
                "message": str(e)
            })
        )]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
