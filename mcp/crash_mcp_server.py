"""
Urban Crash Safety Agent - MCP Server
Exposes crash risk scoring and safe route finding as MCP tools
so any MCP-compatible agent or client can use them via
standard protocol without custom integration.
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
)

# Import our existing tool functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.tools import score_crash_risk, find_safe_route

# ─── MCP Server Setup ───────

app = Server("urban-crash-safety-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Lists all tools available through this MCP server.
    Any MCP-compatible agent can discover and call these tools
    without knowing the underlying implementation.
    """
    return [
        Tool(
            name="score_crash_risk",
            description=(
                "Scores the crash risk at a given GPS coordinate in NYC. "
                "Uses a trained XGBoost model (F1: 0.848, AUC: 0.971) "
                "built on 500,000+ historical collision records. "
                "Returns risk score (0-1), risk level, and explanation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "GPS latitude of the location"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "GPS longitude of the location"
                    }
                },
                "required": ["latitude", "longitude"]
            }
        ),
        Tool(
            name="find_safe_route",
            description=(
                "Finds the safest driving route between two NYC locations. "
                "Scores crash risk at each waypoint and flags routes with "
                "average risk above 0.60 for human review before proceeding."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Starting location name or address in NYC"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Ending location name or address in NYC"
                    }
                },
                "required": ["origin", "destination"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handles tool calls from any MCP-compatible client.
    Routes the call to the appropriate function and returns
    the result as JSON-formatted text content.
    """
    try:
        if name == "score_crash_risk":
            result = score_crash_risk(
                latitude=arguments["latitude"],
                longitude=arguments["longitude"]
            )
        elif name == "find_safe_route":
            result = find_safe_route(
                origin=arguments["origin"],
                destination=arguments["destination"]
            )
        else:
            result = {"error": f"Unknown tool: {name}"}

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]


# ─── Entry Point 

async def main():
    """
    Runs the MCP server over stdio so Antigravity and other
    MCP-compatible clients can connect to it directly.
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())