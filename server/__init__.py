"""
MCP Server Module

This module implements a Model Context Protocol (MCP) server that exposes
resources, tools, and prompts to MCP clients.
"""

from .mcp_server import WeatherMCPServer

__all__ = ['WeatherMCPServer']

