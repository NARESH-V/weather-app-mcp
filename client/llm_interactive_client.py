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
    
    This client can work with OpenAI, Anthropic Claude, or AWS Bedrock.
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
        elif self.provider == "bedrock":
            try:
                import boto3
                
                # Get configuration
                region = ConfigManager.get_config("AWS_REGION") or "us-east-1"
                role_arn = ConfigManager.get_config("AWS_ROLE_ARN")
                external_id = ConfigManager.get_config("AWS_EXTERNAL_ID")
                
                # Check if we should assume a role
                if role_arn:
                    # Assume role with optional external ID
                    print(f"🔐 Assuming role: {role_arn}")
                    if external_id:
                        print(f"   Using external ID: {external_id}")
                    
                    credentials = self._assume_role_with_external_id(
                        role_arn=role_arn,
                        external_id=external_id,
                        region=region
                    )
                    
                    self.llm_client = boto3.client(
                        service_name='bedrock-runtime',
                        region_name=region,
                        aws_access_key_id=credentials['AccessKeyId'],
                        aws_secret_access_key=credentials['SecretAccessKey'],
                        aws_session_token=credentials['SessionToken']
                    )
                else:
                    # Use direct credentials or default credential chain
                    access_key = os.getenv("AWS_ACCESS_KEY_ID")
                    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
                    session_token = os.getenv("AWS_SESSION_TOKEN")
                    
                    # Initialize Bedrock client
                    # If access_key is provided, use explicit credentials
                    # Otherwise, use default credential chain (handles SSO, profiles, etc.)
                    if access_key and secret_key:
                        self.llm_client = boto3.client(
                            service_name='bedrock-runtime',
                            region_name=region,
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key,
                            aws_session_token=session_token
                        )
                    else:
                        # Use default credential chain (recommended)
                        # This will automatically use ~/.aws/credentials or AWS SSO
                        self.llm_client = boto3.client(
                            service_name='bedrock-runtime',
                            region_name=region
                        )
                
                # Default to Claude 3.5 Sonnet on Bedrock
                self.model = ConfigManager.get_config("BEDROCK_MODEL_ID") or "anthropic.claude-3-5-sonnet-20241022-v2:0"
                
                print(f"✓ Using AWS Bedrock in region: {region}")
                print(f"✓ Model: {self.model}")
                
            except ImportError:
                print("Error: boto3 package not installed. Run: pip install boto3")
                sys.exit(1)
            except Exception as e:
                print(f"Error initializing AWS Bedrock: {e}")
                print("\nTroubleshooting:")
                print("1. Refresh your AWS credentials if using temporary credentials")
                print("2. Run: aws configure (or gimme-aws-creds if using Okta)")
                print("3. Check your credentials: aws sts get-caller-identity")
                print("4. Ensure Bedrock is available in your region")
                sys.exit(1)
        else:
            print(f"Error: Unknown provider '{provider}'. Use 'openai', 'anthropic', or 'bedrock'")
            sys.exit(1)
    
    def _assume_role_with_external_id(
        self, 
        role_arn: str, 
        external_id: Optional[str] = None,
        region: str = "us-east-1"
    ) -> Dict[str, str]:
        """
        Assume an IAM role with optional external ID.
        
        Args:
            role_arn: The ARN of the role to assume
            external_id: Optional external ID for cross-account access
            region: AWS region
            
        Returns:
            Dictionary containing temporary credentials
        """
        import boto3
        
        # Create STS client using current credentials or default chain
        sts_client = boto3.client('sts', region_name=region)
        
        # Get session name from config or use default
        session_name = ConfigManager.get_config("AWS_ROLE_SESSION_NAME") or "weather-app-session"
        
        # Prepare assume role parameters
        assume_role_params = {
            'RoleArn': role_arn,
            'RoleSessionName': session_name,
            'DurationSeconds': 3600  # 1 hour
        }
        
        # Add external ID if provided
        if external_id:
            assume_role_params['ExternalId'] = external_id
        
        try:
            # Assume the role
            response = sts_client.assume_role(**assume_role_params)
            
            print(f"✓ Successfully assumed role")
            print(f"   Session: {session_name}")
            print(f"   Expiry: {response['Credentials']['Expiration']}")
            
            return response['Credentials']
        
        except Exception as e:
            print(f"❌ Failed to assume role: {e}")
            print("\nPossible issues:")
            print("1. Role ARN is incorrect")
            print("2. External ID doesn't match role's trust policy")
            print("3. Current credentials lack sts:AssumeRole permission")
            print("4. Role trust policy doesn't allow your identity")
            raise
    
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
    
    async def _call_bedrock(self, messages: List[Dict[str, str]]) -> str:
        """Call AWS Bedrock with Claude model and tool support"""
        import json
        
        tools = self._format_tools_for_claude()  # Use same format as Anthropic
        
        # Extract system message if present
        system_message = None
        if messages and messages[0]["role"] == "system":
            system_message = messages[0]["content"]
            messages = messages[1:]
        
        # Prepare request for Bedrock
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "system": system_message if system_message else "You are a helpful weather assistant.",
            "messages": messages,
            "tools": tools
        }
        
        # Call Bedrock
        response = self.llm_client.invoke_model(
            modelId=self.model,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        
        # Check if Claude wants to use a tool
        if response_body.get('stop_reason') == "tool_use":
            tool_use = next(block for block in response_body['content'] if block.get('type') == "tool_use")
            tool_name = tool_use['name']
            tool_args = tool_use['input']
            
            print(f"\n🤖 Calling tool: {tool_name} with args: {tool_args}\n")
            
            # Execute the MCP tool
            result = await self.client.call_tool(tool_name, tool_args)
            
            # Continue conversation with tool result
            messages.append({
                "role": "assistant",
                "content": response_body['content']
            })
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use['id'],
                        "content": result
                    }
                ]
            })
            
            # Get final response
            final_request = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "system": system_message if system_message else "You are a helpful weather assistant.",
                "messages": messages,
                "tools": tools
            }
            
            final_response = self.llm_client.invoke_model(
                modelId=self.model,
                body=json.dumps(final_request)
            )
            
            final_body = json.loads(final_response['body'].read())
            return final_body['content'][0]['text']
        
        return response_body['content'][0]['text']
    
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
            elif self.provider == "anthropic":
                response = await self._call_claude(conversation_history)
            else:  # bedrock
                response = await self._call_bedrock(conversation_history)
            
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
    
    if provider not in ["openai", "anthropic", "bedrock"]:
        print(f"Invalid LLM_PROVIDER: {provider}. Using 'openai' as default.")
        provider = "openai"
    
    # Check for API key/credentials
    if provider == "openai" and not ConfigManager.get_config("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    if provider == "anthropic" and not ConfigManager.get_config("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    if provider == "bedrock":
        # Check if credentials are available
        # boto3 will use default credential chain if explicit credentials not provided
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        
        if not access_key and not secret_key:
            # Will use default AWS credential chain
            print("Using default AWS credential chain (recommended)")
            print("Credentials will be loaded from ~/.aws/credentials or AWS SSO")
            print("If you get authentication errors, run: gimme-aws-creds (or aws configure)")
        else:
            print("Using explicitly provided AWS credentials")
            if not access_key or not secret_key:
                print("Error: Both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")
                print("Or leave both unset to use default credential chain")
                sys.exit(1)
    
    client = LLMInteractiveClient(provider=provider)
    await client.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)

