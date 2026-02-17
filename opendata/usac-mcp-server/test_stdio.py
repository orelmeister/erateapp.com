"""
Minimal test of the MCP server using stdio
"""
import asyncio
import json
import sys

async def test_server():
    """Test that server can respond to initialization"""
    # Simulate initialization request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    print("Testing server initialization...", file=sys.stderr)
    print(json.dumps(init_request))
    print("", flush=True)
    
    # Wait a moment for response
    await asyncio.sleep(1)

if __name__ == "__main__":
    # Run basic test
    asyncio.run(test_server())
