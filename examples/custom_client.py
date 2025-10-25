#!/usr/bin/env python3
"""
Advanced example: Custom client usage showing specific interactions
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.mcp_client import WeatherMCPClient


async def custom_demo():
    """Custom demonstration of MCP client capabilities"""
    client = WeatherMCPClient()
    
    try:
        # Connect to server
        server_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "server",
            "mcp_server.py"
        )
        await client.connect_to_server(server_path)
        
        print("\n🌤️  Custom Weather MCP Client Demo\n")
        
        # Example 1: Get weather for multiple cities
        print("="*60)
        print("Example 1: Checking weather in multiple cities")
        print("="*60)
        cities = ["new_york", "london", "tokyo", "paris"]
        for city in cities:
            result = await client.call_tool("get_current_weather", {"city": city})
            print(f"\n{result}")
        
        # Example 2: Compare all cities pairwise
        print("\n\n" + "="*60)
        print("Example 2: Comparing weather between cities")
        print("="*60)
        comparisons = [
            ("new_york", "london"),
            ("tokyo", "paris"),
        ]
        for city1, city2 in comparisons:
            result = await client.call_tool("compare_weather", {
                "city1": city1,
                "city2": city2
            })
            print(f"\n{result}")
        
        # Example 3: Read raw resource data
        print("\n\n" + "="*60)
        print("Example 3: Reading raw resource data")
        print("="*60)
        for city in ["new_york", "tokyo"]:
            data = await client.read_resource(f"weather://{city}")
            print(f"\nRaw data for {city}:")
            print(data)
        
        # Example 4: Use prompt templates
        print("\n\n" + "="*60)
        print("Example 4: Using prompt templates")
        print("="*60)
        prompt = await client.get_prompt("travel_weather_advice", {
            "origin": "new_york",
            "destination": "london"
        })
        print(f"\nPrompt description: {prompt['description']}")
        for msg in prompt['messages']:
            print(f"\nRole: {msg['role']}")
            print(f"Content: {msg['content']['text']}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(custom_demo())

