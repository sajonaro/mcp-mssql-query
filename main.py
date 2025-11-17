# type: ignore
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
from mcp_common import execute_query, query_table, get_tables, get_views

# Initialize the server
mcp = FastMCP("MSSQL_Query_Server")


# Register tools - simply delegate to common implementations
mcp.tool()(execute_query)
mcp.tool()(query_table)
mcp.tool()(get_tables)
mcp.tool()(get_views)


if __name__ == "__main__":
    mcp.run(transport="stdio")
