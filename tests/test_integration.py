"""
Integration tests for MCP server and client
"""

import pytest
import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.mcp_client import WeatherMCPClient


@pytest.mark.asyncio
async def test_full_integration():
    """Test full integration between client and server"""
    client = WeatherMCPClient()
    
    try:
        # Get the path to the server
        server_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "server",
            "mcp_server.py"
        )
        
        # Connect to server
        await client.connect_to_server(server_path)
        
        # Test listing resources
        resources = await client.list_resources()
        assert len(resources) > 0
        assert any("new_york" in r["uri"] for r in resources)
        
        # Test reading a resource
        weather_data = await client.read_resource("weather://new_york")
        assert "New York" in weather_data
        assert "temperature" in weather_data.lower()
        
        # Test listing tools
        tools = await client.list_tools()
        assert len(tools) > 0
        tool_names = [t["name"] for t in tools]
        assert "get_current_weather" in tool_names
        
        # Test calling a tool
        result = await client.call_tool("get_current_weather", {"city": "london"})
        assert "London" in result
        assert "temperature" in result.lower()
        
        # Test listing prompts
        prompts = await client.list_prompts()
        assert len(prompts) > 0
        
    finally:
        await client.disconnect()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

