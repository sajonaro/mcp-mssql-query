#! /usr/bin/env bash

# Add logging to help debug connection issues
echo "WSL Bridge: Starting mssql-query-mcp MCP server connection..." >&2
echo "WSL Bridge: Attempting to connect to container 'mssql-query-mcp'..." >&2

# Check if container exists and is running
if ! docker ps --format "table {{.Names}}" | grep -q "^mssql-query-mcp$"; then
    echo "WSL Bridge: ERROR - Container 'mssql-query-mcp' is not running!" >&2
    exit 1
fi

echo "WSL Bridge: Container found, executing main.py..." >&2

# Set environment variables for SQL Server connection
export MSSQL_SERVER="20.157.206.39"
export MSSQL_DATABASE="poc_db_aggregated"
export MSSQL_USERNAME="zed"
export MSSQL_PASSWORD="TempSA_Password123!"

echo "WSL Bridge: Environment variables set:" >&2
echo "  MSSQL_SERVER=$MSSQL_SERVER" >&2
echo "  MSSQL_DATABASE=$MSSQL_DATABASE" >&2
echo "  MSSQL_USERNAME=$MSSQL_USERNAME" >&2

exec docker exec -i \
    -e MSSQL_SERVER="$MSSQL_SERVER" \
    -e MSSQL_DATABASE="$MSSQL_DATABASE" \
    -e MSSQL_USERNAME="$MSSQL_USERNAME" \
    -e MSSQL_PASSWORD="$MSSQL_PASSWORD" \
    mssql-query-mcp uv run main.py
