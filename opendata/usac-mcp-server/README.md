# USAC E-Rate Open Data MCP Server

An MCP (Model Context Protocol) server that provides AI assistants with direct access to USAC E-Rate program data.

## Features

### Available Tools

1. **query_erate_data** - Query E-Rate data with flexible filtering
   - Filter by year, status, entity type, state, service category
   - Returns up to 10,000 records with pagination
   - Includes funding amounts and application details

2. **get_field_values** - Discover available values for any field
   - Get all unique states, statuses, entity types, etc.
   - Optionally filter by year
   - Useful for building dynamic queries

3. **search_entities** - Find specific schools or libraries
   - Search by organization name (partial match)
   - Filter by entity type and year
   - Returns entity details and application history

4. **get_statistics** - Aggregate statistics and analysis
   - Group by status, entity type, state, or year
   - Calculate totals, averages, and distributions
   - Summary funding statistics

5. **analyze_denials** - Analyze denied applications
   - Patterns in denial rates
   - Geographic and entity type breakdown
   - Total denied funding amounts

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. Install the MCP server package:

```bash
cd usac-mcp-server
pip install -e .
```

2. Configure in Claude Desktop (or other MCP client):

Edit your MCP settings file:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "usac-erate": {
      "command": "python",
      "args": [
        "C:\\Users\\orelm\\OneDrive\\Documents\\GitHub\\erateapp.com\\opendata\\usac-mcp-server\\server.py"
      ]
    }
  }
}
```

3. Restart Claude Desktop

## Usage Examples

Once installed, you can ask your AI assistant natural language questions like:

### Basic Queries
- "Show me all denied schools in 2025"
- "How many libraries got funded in California last year?"
- "What are the available application statuses?"

### Statistical Analysis
- "Give me statistics on E-Rate applications by state for 2024"
- "Analyze denial patterns for schools in Texas"
- "What's the total funding amount for all funded applications this year?"

### Entity Search
- "Find all applications for 'Lincoln High School'"
- "Search for library systems in New York"

### Advanced Analysis
- "Compare funding rates between schools and libraries"
- "Which states have the highest denial rates?"
- "What service categories receive the most funding?"

## Data Source

Data is fetched in real-time from the USAC Open Data API:
https://opendata.usac.org/resource/srbr-2d59.json

### Available Fields
- **funding_year**: 2016-2025
- **application_status**: Funded, Denied, Cancelled, Unfunded
- **entity_type**: School, Library, School District, Library System, Consortium
- **state**: Two-letter state codes
- **category_of_service**: Internet Access, Voice, etc.
- **amount_of_commitment_request**: Funding amount requested
- **applicant_name**: Organization name

### API Limitations
- Maximum 200 records per API call (automatically paginated)
- Default tool limit: 1,000 records (adjustable up to 10,000)
- Rate limiting may apply for large queries

## Troubleshooting

### MCP Server Not Appearing
1. Check that Python path in config is correct
2. Verify all dependencies are installed: `pip list | grep mcp`
3. Check Claude Desktop logs for errors

### No Data Returned
1. Verify internet connection
2. Check USAC API is accessible: https://opendata.usac.org
3. Try broader query criteria (remove filters)

### Performance Issues
1. Reduce the `limit` parameter for faster queries
2. Add more specific filters to narrow results
3. Use pagination for large datasets

## Development

### Running Locally
```bash
python server.py
```

### Testing Tools
Use the MCP Inspector:
```bash
npx @modelcontextprotocol/inspector python server.py
```

### Adding New Tools
1. Add tool definition in `list_tools()`
2. Add handler logic in `call_tool()`
3. Update this README with usage examples

## License

MIT License - Feel free to use and modify

## Support

For issues or questions:
- Check USAC Open Data documentation: https://opendata.usac.org
- Review MCP protocol documentation: https://modelcontextprotocol.io
