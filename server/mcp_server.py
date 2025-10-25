"""
Weather MCP Server Implementation

This server provides weather-related resources, tools, and prompts
following the Model Context Protocol specification.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Prompt,
    PromptArgument,
    PromptMessage,
    GetPromptResult,
)
from pydantic import AnyUrl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherMCPServer:
    """
    A Model Context Protocol server for weather information.
    
    This server provides:
    - Resources: Weather data for different cities
    - Tools: Functions to get current weather, forecasts, etc.
    - Prompts: Templates for weather-related queries
    """
    
    def __init__(self):
        """Initialize the Weather MCP Server"""
        self.server = Server("weather-server")
        
        # Sample weather data (in production, this would come from a real API)
        self.weather_data = {
            "new_york": {
                "city": "New York",
                "temperature": 72,
                "conditions": "Partly Cloudy",
                "humidity": 65,
                "wind_speed": 12
            },
            "london": {
                "city": "London",
                "temperature": 58,
                "conditions": "Rainy",
                "humidity": 80,
                "wind_speed": 15
            },
            "tokyo": {
                "city": "Tokyo",
                "temperature": 68,
                "conditions": "Clear",
                "humidity": 55,
                "wind_speed": 8
            },
            "paris": {
                "city": "Paris",
                "temperature": 62,
                "conditions": "Cloudy",
                "humidity": 70,
                "wind_speed": 10
            }
        }
        
        self._setup_request_handlers()
        logger.info("Weather MCP Server initialized")
    
    def _setup_request_handlers(self):
        """Set up handlers for MCP protocol requests"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """
            List all available weather resources.
            
            Returns:
                List of Resource objects representing weather data for different cities
            """
            logger.info("Listing available resources")
            resources = []
            
            for city_key, data in self.weather_data.items():
                resources.append(
                    Resource(
                        uri=AnyUrl(f"weather://{city_key}"),
                        name=f"Weather for {data['city']}",
                        description=f"Current weather conditions in {data['city']}",
                        mimeType="application/json",
                    )
                )
            
            return resources
        
        @self.server.read_resource()
        async def handle_read_resource(uri: AnyUrl) -> str:
            """
            Read a specific weather resource.
            
            Args:
                uri: The URI of the resource (e.g., weather://new_york)
            
            Returns:
                JSON string containing weather data
            """
            city_key = str(uri).replace("weather://", "")
            logger.info(f"Reading resource for city: {city_key}")
            
            if city_key not in self.weather_data:
                raise ValueError(f"Unknown city: {city_key}")
            
            weather_info = self.weather_data[city_key].copy()
            weather_info["timestamp"] = datetime.now().isoformat()
            
            return json.dumps(weather_info, indent=2)
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """
            List all available tools.
            
            Returns:
                List of Tool objects that can be invoked by clients
            """
            logger.info("Listing available tools")
            return [
                Tool(
                    name="get_current_weather",
                    description="Get the current weather for a specific city",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The city name (e.g., new_york, london, tokyo, paris)",
                            }
                        },
                        "required": ["city"],
                    },
                ),
                Tool(
                    name="compare_weather",
                    description="Compare weather conditions between two cities",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "city1": {
                                "type": "string",
                                "description": "First city name",
                            },
                            "city2": {
                                "type": "string",
                                "description": "Second city name",
                            }
                        },
                        "required": ["city1", "city2"],
                    },
                ),
                Tool(
                    name="get_temperature_summary",
                    description="Get a summary of temperatures across all cities",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """
            Execute a tool with given arguments.
            
            Args:
                name: The name of the tool to execute
                arguments: Dictionary of arguments for the tool
            
            Returns:
                List containing the tool execution result
            """
            logger.info(f"Calling tool: {name} with arguments: {arguments}")
            
            if name == "get_current_weather":
                city = arguments.get("city", "").lower()
                
                if city not in self.weather_data:
                    return [TextContent(
                        type="text",
                        text=f"Error: Unknown city '{city}'. Available cities: {', '.join(self.weather_data.keys())}"
                    )]
                
                weather = self.weather_data[city]
                result = (
                    f"Current weather in {weather['city']}:\n"
                    f"Temperature: {weather['temperature']}°F\n"
                    f"Conditions: {weather['conditions']}\n"
                    f"Humidity: {weather['humidity']}%\n"
                    f"Wind Speed: {weather['wind_speed']} mph"
                )
                
                return [TextContent(type="text", text=result)]
            
            elif name == "compare_weather":
                city1 = arguments.get("city1", "").lower()
                city2 = arguments.get("city2", "").lower()
                
                if city1 not in self.weather_data or city2 not in self.weather_data:
                    return [TextContent(
                        type="text",
                        text=f"Error: One or both cities not found. Available cities: {', '.join(self.weather_data.keys())}"
                    )]
                
                w1 = self.weather_data[city1]
                w2 = self.weather_data[city2]
                
                temp_diff = w1['temperature'] - w2['temperature']
                result = (
                    f"Weather Comparison:\n\n"
                    f"{w1['city']}: {w1['temperature']}°F, {w1['conditions']}\n"
                    f"{w2['city']}: {w2['temperature']}°F, {w2['conditions']}\n\n"
                    f"Temperature difference: {abs(temp_diff)}°F "
                    f"({w1['city']} is {'warmer' if temp_diff > 0 else 'cooler' if temp_diff < 0 else 'the same temperature'})"
                )
                
                return [TextContent(type="text", text=result)]
            
            elif name == "get_temperature_summary":
                temps = [data['temperature'] for data in self.weather_data.values()]
                avg_temp = sum(temps) / len(temps)
                max_temp = max(temps)
                min_temp = min(temps)
                
                hottest_city = [city['city'] for city in self.weather_data.values() if city['temperature'] == max_temp][0]
                coldest_city = [city['city'] for city in self.weather_data.values() if city['temperature'] == min_temp][0]
                
                result = (
                    f"Temperature Summary Across All Cities:\n\n"
                    f"Average Temperature: {avg_temp:.1f}°F\n"
                    f"Hottest: {hottest_city} at {max_temp}°F\n"
                    f"Coldest: {coldest_city} at {min_temp}°F\n"
                    f"Range: {max_temp - min_temp}°F"
                )
                
                return [TextContent(type="text", text=result)]
            
            else:
                return [TextContent(
                    type="text",
                    text=f"Error: Unknown tool '{name}'"
                )]
        
        @self.server.list_prompts()
        async def handle_list_prompts() -> List[Prompt]:
            """
            List all available prompts.
            
            Returns:
                List of Prompt templates
            """
            logger.info("Listing available prompts")
            return [
                Prompt(
                    name="weather_report",
                    description="Generate a weather report for a specific city",
                    arguments=[
                        PromptArgument(
                            name="city",
                            description="The city to get weather for",
                            required=True,
                        )
                    ],
                ),
                Prompt(
                    name="travel_weather_advice",
                    description="Get travel advice based on weather in two cities",
                    arguments=[
                        PromptArgument(
                            name="origin",
                            description="City you're traveling from",
                            required=True,
                        ),
                        PromptArgument(
                            name="destination",
                            description="City you're traveling to",
                            required=True,
                        )
                    ],
                ),
            ]
        
        @self.server.get_prompt()
        async def handle_get_prompt(name: str, arguments: Dict[str, str]) -> GetPromptResult:
            """
            Get a specific prompt with arguments filled in.
            
            Args:
                name: The name of the prompt
                arguments: Dictionary of argument values
            
            Returns:
                GetPromptResult with the prompt messages
            """
            logger.info(f"Getting prompt: {name} with arguments: {arguments}")
            
            if name == "weather_report":
                city = arguments.get("city", "").lower()
                
                if city not in self.weather_data:
                    weather_text = f"Error: Unknown city '{city}'"
                else:
                    weather = self.weather_data[city]
                    weather_text = f"The weather in {weather['city']}"
                
                return GetPromptResult(
                    description=f"Weather report for {city}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"Please provide a detailed weather report for {city}. Include temperature, conditions, humidity, and any relevant advice."
                            ),
                        )
                    ],
                )
            
            elif name == "travel_weather_advice":
                origin = arguments.get("origin", "").lower()
                destination = arguments.get("destination", "").lower()
                
                return GetPromptResult(
                    description=f"Travel advice from {origin} to {destination}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"I'm traveling from {origin} to {destination}. Compare the weather in both cities and give me advice on what to pack and what to expect."
                            ),
                        )
                    ],
                )
            
            else:
                raise ValueError(f"Unknown prompt: {name}")
    
    async def run(self):
        """Run the MCP server using stdio transport"""
        logger.info("Starting Weather MCP Server...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="weather-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


async def main():
    """Main entry point for the server"""
    server = WeatherMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())

