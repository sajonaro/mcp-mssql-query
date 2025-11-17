#!/usr/bin/env python3
"""
SSE transport wrapper for the MCP MSSQL Query Server.
This allows the server to be accessed over HTTP/HTTPS while keeping
the original stdio transport available for Claude Desktop.
"""

# type: ignore
from mcp.server.fastmcp import FastMCP
from mcp_common import execute_query, query_table, get_tables, get_views

# Initialize the server with SSE configuration
mcp = FastMCP(
    "MSSQL_Query_Server",
    host="0.0.0.0",  # Bind to all interfaces for Docker
    port=8000,
    sse_path="/sse",
)


# Register tools - simply delegate to common implementations
mcp.tool()(execute_query)
mcp.tool()(query_table)
mcp.tool()(get_tables)
mcp.tool()(get_views)


if __name__ == "__main__":
    # Use SSE transport for HTTP/HTTPS access
    mcp.run(transport="sse")
