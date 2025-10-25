#!/usr/bin/env python3
"""
Example script showing how to use the MCP client
"""

import sys
import os

# Add parent directory to path to import client module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.mcp_client import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())

