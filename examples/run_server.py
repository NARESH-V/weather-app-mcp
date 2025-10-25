#!/usr/bin/env python3
"""
Example script showing how to run the MCP server standalone
"""

import sys
import os

# Add parent directory to path to import server module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.mcp_server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())

