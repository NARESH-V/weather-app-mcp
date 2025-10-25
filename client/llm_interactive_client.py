"""
LLM-Powered Interactive MCP Client

This client uses an LLM (OpenAI GPT or Anthropic Claude) to process natural
language queries and automatically select and execute the appropriate MCP tools.
"""

import asyncio
import logging
import os
import sys
import json
from typing import Optional, List, Dict, Any

from mcp_client import WeatherMCPClient
from config_manger import ConfigManager

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)


class LLMInteractiveClient:
    """
    Interactive client that uses an LLM to understand queries and call MCP tools.
    
    This client can work with either OpenAI or Anthropic Claude.
    """
    
    def __init__(self, provider: str = "openai"):
        self.client = WeatherMCPClient()
        self.provider = provider.lower()
        self.tools_info = []
        self.resources_info = []
        
        # Initialize LLM client
        if self.provider == "openai":
            try:
                import openai
                self.llm_client = openai.OpenAI(api_key=ConfigManager.get_config("OPENAI_API_KEY"))
                self.model = "gpt-4o-mini"
            except ImportError:
                print("Error: openai package not installed. Run: pip install openai")
                sys.exit(1)
        elif self.provider == "anthropic":
            try:
                import anthropic
                self.llm_client = anthropic.Anthropic(api_key=ConfigManager.get_config("ANTHROPIC_API_KEY"))
                self.model = "claude-3-5-sonnet-20241022"
            except ImportError:
                print("Error: anthropic package not installed. Run: pip install anthropic")
                sys.exit(1)
        else:
            print(f"Error: Unknown provider '{provider}'. Use 'openai' or 'anthropic'")
            sys.exit(1)
    
    async def connect(self, server_path: str = "server/mcp_server.py"):
        """Connect to the MCP server and load tool information"""
        await self.client.connect_to_server(server_path)
        
        # Load available tools
        self.tools_info = await self.client.list_tools()
        self.resources_info = await self.client.list_resources()
        
        print(f"✓ Connected to weather MCP server")
        print(f"✓ Loaded {len(self.tools_info)} tools and {len(self.resources_info)} resources")
        print(f"✓ Using {self.provider.upper()} ({self.model})\n")
    
    async def disconnect(self):
        """Disconnect from the server"""
        await self.client.disconnect()
    
    def _format_tools_for_openai(self) -> List[Dict[str, Any]]:
        """Format MCP tools for OpenAI function calling"""
        formatted_tools = []
        
        for tool in self.tools_info:
            formatted_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["inputSchema"]
                }
            })
        
        return formatted_tools
    
    def _format_tools_for_claude(self) -> List[Dict[str, Any]]:
        """Format MCP tools for Claude tool use"""
        formatted_tools = []
        
        for tool in self.tools_info:
            formatted_tools.append({
                "name": tool["name"],
                "description": tool["description"],
                "input_schema": tool["inputSchema"]
            })
        
        return formatted_tools
    
    async def _call_openai(self, messages: List[Dict[str, str]]) -> str:
        """Call OpenAI API with tool support"""
        tools = self._format_tools_for_openai()
        
        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        # Check if the model wants to call a tool
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            print(f"\n🤖 Calling tool: {tool_name} with args: {tool_args}\n")
            
            # Execute the MCP tool
            result = await self.client.call_tool(tool_name, tool_args)
            
            # Add tool result to conversation
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [tool_call]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
            
            # Get final response
            final_response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            return final_response.choices[0].message.content
        
        return message.content
    
    async def _call_claude(self, messages: List[Dict[str, str]]) -> str:
        """Call Claude API with tool support"""
        tools = self._format_tools_for_claude()
        
        # Extract system message if present
        system_message = None
        if messages and messages[0]["role"] == "system":
            system_message = messages[0]["content"]
            messages = messages[1:]
        
        response = self.llm_client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_message if system_message else "You are a helpful weather assistant.",
            messages=messages,
            tools=tools
        )
        
        # Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            tool_use = next(block for block in response.content if block.type == "tool_use")
            tool_name = tool_use.name
            tool_args = tool_use.input
            
            print(f"\n🤖 Calling tool: {tool_name} with args: {tool_args}\n")
            
            # Execute the MCP tool
            result = await self.client.call_tool(tool_name, tool_args)
            
            # Continue conversation with tool result
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": result
                    }
                ]
            })
            
            # Get final response
            final_response = self.llm_client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_message if system_message else "You are a helpful weather assistant.",
                messages=messages,
                tools=tools
            )
            
            return final_response.content[0].text
        
        return response.content[0].text
    
    async def process_query(self, query: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Process a user query using the LLM.
        
        Args:
            query: User's natural language query
            conversation_history: Previous messages in the conversation
        
        Returns:
            LLM's response
        """
        # Add user query to conversation
        conversation_history.append({
            "role": "user",
            "content": query
        })
        
        try:
            # Call appropriate LLM
            if self.provider == "openai":
                response = await self._call_openai(conversation_history)
            else:  # anthropic
                response = await self._call_claude(conversation_history)
            
            # Add assistant response to history
            conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return response
        
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    async def run(self):
        """Run the interactive LLM-powered client"""
        try:
            await self.connect()
            
            print("="*60)
            print(f"WEATHER MCP CLIENT - LLM POWERED ({self.provider.upper()})")
            print("="*60)
            print("\nAsk me anything about the weather in natural language!")
            print("Type 'quit' to exit\n")
            
            # Initialize conversation with system message
            conversation_history = [{
                "role": "system",
                "content": (
                    "You are a helpful weather assistant. You have access to weather "
                    "tools that can provide current weather information for New York, "
                    "London, Tokyo, and Paris. Use the tools to answer user questions "
                    "about weather. Be concise and friendly."
                )
            }]
            
            while True:
                try:
                    # Get user input
                    query = input("You: ").strip()
                    
                    if not query:
                        continue
                    
                    if query.lower() in ["quit", "exit", "q"]:
                        print("\nGoodbye! 👋")
                        break
                    
                    # Process with LLM
                    print("\n🤔 Thinking...\n")
                    response = await self.process_query(query, conversation_history)
                    
                    # Display response
                    print(f"Assistant: {response}\n")
                
                except KeyboardInterrupt:
                    print("\n\nInterrupted. Type 'quit' to exit.")
                    continue
                except EOFError:
                    print("\n\nGoodbye! 👋")
                    break
        
        finally:
            await self.disconnect()


async def main():
    """Main entry point"""
    # Check which provider to use
    provider = ConfigManager.get_config("LLM_PROVIDER").lower()
    
    if provider not in ["openai", "anthropic"]:
        print(f"Invalid LLM_PROVIDER: {provider}. Using 'openai' as default.")
        provider = "openai"
    
    # Check for API key
    if provider == "openai" and not ConfigManager.get_config("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    if provider == "anthropic" and not ConfigManager.get_config("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    client = LLMInteractiveClient(provider=provider)
    await client.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)

