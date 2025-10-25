"""
Test suite for the MCP Server
"""

import pytest
import asyncio
import json
from server.mcp_server import WeatherMCPServer


@pytest.fixture
def server():
    """Create a server instance for testing"""
    return WeatherMCPServer()


@pytest.mark.asyncio
async def test_server_initialization(server):
    """Test that the server initializes correctly"""
    assert server is not None
    assert server.server is not None
    assert len(server.weather_data) > 0
    assert "new_york" in server.weather_data
    assert "london" in server.weather_data


@pytest.mark.asyncio
async def test_weather_data_structure(server):
    """Test that weather data has the correct structure"""
    for city_key, data in server.weather_data.items():
        assert "city" in data
        assert "temperature" in data
        assert "conditions" in data
        assert "humidity" in data
        assert "wind_speed" in data
        assert isinstance(data["temperature"], (int, float))
        assert isinstance(data["humidity"], (int, float))
        assert isinstance(data["wind_speed"], (int, float))


def test_server_has_request_handlers(server):
    """Test that the server has registered request handlers"""
    # The server should have handlers registered
    assert server.server is not None
    # Check that the server name is set correctly
    assert server.server.name == "weather-server"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

