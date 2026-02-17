# Configuration for Claude Desktop

## Windows Configuration Path
`%APPDATA%\Claude\claude_desktop_config.json`

Full path example:
`C:\Users\YourUsername\AppData\Roaming\Claude\claude_desktop_config.json`

## Configuration Content

Add this to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "usac-erate": {
      "command": "python",
      "args": [
        "C:\\Users\\orelm\\OneDrive\\Documents\\GitHub\\erateapp.com\\opendata\\usac-mcp-server\\server.py"
      ],
      "env": {}
    }
  }
}
```

## If you have existing MCP servers

If you already have other MCP servers configured, add the `usac-erate` entry to your existing `mcpServers` object:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": ["..."]
    },
    "usac-erate": {
      "command": "python",
      "args": [
        "C:\\Users\\orelm\\OneDrive\\Documents\\GitHub\\erateapp.com\\opendata\\usac-mcp-server\\server.py"
      ],
      "env": {}
    }
  }
}
```

## Verification Steps

1. Save the configuration file
2. Close Claude Desktop completely (check Task Manager to ensure it's not running)
3. Restart Claude Desktop
4. Look for the MCP tools icon in Claude Desktop
5. You should see "usac-erate" server listed with 5 tools:
   - query_erate_data
   - get_field_values
   - search_entities
   - get_statistics
   - analyze_denials

## Testing

Try asking Claude:
- "What tools do you have available for E-Rate data?"
- "Show me denied schools in 2025"
- "Get statistics for funded applications in California"

## Troubleshooting

### Server doesn't appear
- Verify Python path: Run `where python` in PowerShell
- Check the full path in the config matches your file location
- Look for errors in Claude Desktop logs

### Python path issues
If `python` command doesn't work, use the full path:
```json
"command": "C:\\Users\\orelm\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
```

### Import errors
Make sure dependencies are installed:
```bash
pip install mcp requests pandas
```

### Check server works standalone
```bash
cd usac-mcp-server
python test_server.py
```
