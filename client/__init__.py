"""
MCP Client Module

This module implements a Model Context Protocol (MCP) client that can connect
to MCP servers and interact with their resources, tools, and prompts.
"""

from .mcp_client import WeatherMCPClient

__all__ = ['WeatherMCPClient']

