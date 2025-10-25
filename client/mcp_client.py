"""
Weather MCP Client Implementation

This client connects to MCP servers and demonstrates how to:
- List and read resources
- Call tools
- Use prompts
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import (
    TextContent,
    TextResourceContents,
    BlobResourceContents
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherMCPClient:
    """
    A Model Context Protocol client for interacting with weather servers.
    
    This client can:
    - Connect to MCP servers
    - List available resources
    - Read resource content
    - Call tools with arguments
    - Use prompt templates
    """
    
    def __init__(self):
        """Initialize the Weather MCP Client"""
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        logger.info("Weather MCP Client initialized")
    
    async def connect_to_server(self, server_script_path: str):
        """
        Connect to an MCP server.
        
        Args:
            server_script_path: Path to the server script to run
        """
        try:
            logger.info(f"Connecting to MCP server: {server_script_path}")
            
            # Configure server parameters
            server_params = StdioServerParameters(
                command="python",
                args=[server_script_path],
                env=None
            )
            
            # Create stdio client connection
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            read_stream, write_stream = stdio_transport
            
            # Initialize client session
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )
            
            # Initialize the session
            await self.session.initialize()
            
            logger.info("Successfully connected to MCP server")
            
        except Exception as e:
            logger.error(f"Failed to connect to server: {e}")
            raise
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """
        List all available resources from the server.
        
        Returns:
            List of resource dictionaries
        """
        if not self.session:
            raise RuntimeError("Not connected to a server. Call connect_to_server first.")
        
        try:
            logger.info("Listing resources...")
            response = await self.session.list_resources()
            
            resources = []
            for resource in response.resources:
                resource_dict = {
                    "uri": str(resource.uri),
                    "name": resource.name,
                    "description": resource.description,
                    "mimeType": resource.mimeType,
                }
                resources.append(resource_dict)
                logger.info(f"  - {resource.name}: {resource.uri}")
            
            return resources
            
        except Exception as e:
            logger.error(f"Failed to list resources: {e}")
            raise
    
    async def read_resource(self, uri: str) -> str:
        """
        Read a specific resource from the server.
        
        Args:
            uri: The URI of the resource to read
        
        Returns:
            The resource content as a string
        """
        if not self.session:
            raise RuntimeError("Not connected to a server. Call connect_to_server first.")
        
        try:
            logger.info(f"Reading resource: {uri}")
            response = await self.session.read_resource(uri)
            
            # Extract text content from the response
            content = ""
            for item in response.contents:
                if isinstance(item, TextResourceContents):
                    content += item.text
                elif hasattr(item, 'text'):
                    content += item.text
            
            return content
            
        except Exception as e:
            logger.error(f"Failed to read resource: {e}")
            raise
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools from the server.
        
        Returns:
            List of tool dictionaries
        """
        if not self.session:
            raise RuntimeError("Not connected to a server. Call connect_to_server first.")
        
        try:
            logger.info("Listing tools...")
            response = await self.session.list_tools()
            
            tools = []
            for tool in response.tools:
                tool_dict = {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema,
                }
                tools.append(tool_dict)
                logger.info(f"  - {tool.name}: {tool.description}")
            
            return tools
            
        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            raise
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Call a tool on the server.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Dictionary of arguments for the tool
        
        Returns:
            The tool result as a string
        """
        if not self.session:
            raise RuntimeError("Not connected to a server. Call connect_to_server first.")
        
        try:
            logger.info(f"Calling tool '{tool_name}' with arguments: {arguments}")
            response = await self.session.call_tool(tool_name, arguments)
            
            # Extract text content from the response
            result = ""
            for item in response.content:
                if isinstance(item, TextContent):
                    result += item.text
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to call tool: {e}")
            raise
    
    async def list_prompts(self) -> List[Dict[str, Any]]:
        """
        List all available prompts from the server.
        
        Returns:
            List of prompt dictionaries
        """
        if not self.session:
            raise RuntimeError("Not connected to a server. Call connect_to_server first.")
        
        try:
            logger.info("Listing prompts...")
            response = await self.session.list_prompts()
            
            prompts = []
            for prompt in response.prompts:
                prompt_dict = {
                    "name": prompt.name,
                    "description": prompt.description,
                    "arguments": [
                        {
                            "name": arg.name,
                            "description": arg.description,
                            "required": arg.required
                        }
                        for arg in (prompt.arguments or [])
                    ]
                }
                prompts.append(prompt_dict)
                logger.info(f"  - {prompt.name}: {prompt.description}")
            
            return prompts
            
        except Exception as e:
            logger.error(f"Failed to list prompts: {e}")
            raise
    
    async def get_prompt(self, prompt_name: str, arguments: Dict[str, str]) -> Dict[str, Any]:
        """
        Get a prompt from the server.
        
        Args:
            prompt_name: Name of the prompt to get
            arguments: Dictionary of argument values for the prompt
        
        Returns:
            Dictionary containing prompt information and messages
        """
        if not self.session:
            raise RuntimeError("Not connected to a server. Call connect_to_server first.")
        
        try:
            logger.info(f"Getting prompt '{prompt_name}' with arguments: {arguments}")
            response = await self.session.get_prompt(prompt_name, arguments)
            
            messages = []
            for message in response.messages:
                msg_dict = {
                    "role": message.role,
                    "content": {}
                }
                
                if isinstance(message.content, TextContent):
                    msg_dict["content"] = {
                        "type": "text",
                        "text": message.content.text
                    }
                
                messages.append(msg_dict)
            
            return {
                "description": response.description,
                "messages": messages
            }
            
        except Exception as e:
            logger.error(f"Failed to get prompt: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from the server"""
        try:
            logger.info("Disconnecting from server...")
            await self.exit_stack.aclose()
            self.session = None
            logger.info("Disconnected successfully")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
            raise


async def main():
    """
    Main demonstration function showing how to use the MCP client.
    """
    client = WeatherMCPClient()
    
    try:
        # Connect to the server
        await client.connect_to_server("server/mcp_server.py")
        
        print("\n" + "="*60)
        print("WEATHER MCP CLIENT DEMONSTRATION")
        print("="*60)
        
        # 1. List and display all resources
        print("\n1. LISTING RESOURCES:")
        print("-" * 60)
        resources = await client.list_resources()
        for resource in resources:
            print(f"\nName: {resource['name']}")
            print(f"URI: {resource['uri']}")
            print(f"Description: {resource['description']}")
        
        # 2. Read a specific resource
        print("\n\n2. READING A RESOURCE (New York):")
        print("-" * 60)
        weather_data = await client.read_resource("weather://new_york")
        print(weather_data)
        
        # 3. List all tools
        print("\n\n3. LISTING TOOLS:")
        print("-" * 60)
        tools = await client.list_tools()
        for tool in tools:
            print(f"\nTool: {tool['name']}")
            print(f"Description: {tool['description']}")
        
        # 4. Call a tool to get current weather
        print("\n\n4. CALLING TOOL: get_current_weather")
        print("-" * 60)
        result = await client.call_tool("get_current_weather", {"city": "london"})
        print(result)
        
        # 5. Call tool to compare weather
        print("\n\n5. CALLING TOOL: compare_weather")
        print("-" * 60)
        result = await client.call_tool("compare_weather", {
            "city1": "new_york",
            "city2": "tokyo"
        })
        print(result)
        
        # 6. Call tool to get temperature summary
        print("\n\n6. CALLING TOOL: get_temperature_summary")
        print("-" * 60)
        result = await client.call_tool("get_temperature_summary", {})
        print(result)
        
        # 7. List all prompts
        print("\n\n7. LISTING PROMPTS:")
        print("-" * 60)
        prompts = await client.list_prompts()
        for prompt in prompts:
            print(f"\nPrompt: {prompt['name']}")
            print(f"Description: {prompt['description']}")
            print("Arguments:")
            for arg in prompt['arguments']:
                print(f"  - {arg['name']}: {arg['description']} (required: {arg['required']})")
        
        # 8. Get a prompt
        print("\n\n8. GETTING PROMPT: weather_report")
        print("-" * 60)
        prompt_result = await client.get_prompt("weather_report", {"city": "paris"})
        print(f"Description: {prompt_result['description']}")
        print(f"Messages: {prompt_result['messages']}")
        
        print("\n" + "="*60)
        print("DEMONSTRATION COMPLETE")
        print("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Error in demonstration: {e}")
        raise
    
    finally:
        # Always disconnect
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

