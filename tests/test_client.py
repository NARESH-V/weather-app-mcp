"""
Test suite for the MCP Client
"""

import pytest
from client.mcp_client import WeatherMCPClient


@pytest.fixture
def client():
    """Create a client instance for testing"""
    return WeatherMCPClient()


def test_client_initialization(client):
    """Test that the client initializes correctly"""
    assert client is not None
    assert client.session is None  # Not connected yet
    assert client.exit_stack is not None


def test_client_not_connected_errors(client):
    """Test that operations fail gracefully when not connected"""
    with pytest.raises(RuntimeError):
        # This should fail because we haven't connected to a server
        import asyncio
        asyncio.run(client.list_resources())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

