#! /usr/bin/env bash

# Add logging to help debug connection issues
echo "WSL Bridge: Starting mssql-query-mcp MCP server connection..." >&2

# Load environment variables from .env file first
if [ ! -f .env ]; then
    echo "WSL Bridge: ERROR - .env file not found!" >&2
    exit 1
fi

# Export all variables from .env file
set -a
source .env
set +a
echo "WSL Bridge: Environment variables loaded from .env file" >&2

# Check if container exists and is running
if ! docker ps --format "table {{.Names}}" | grep -q "^mssql-query-mcp$"; then
    echo "WSL Bridge: Container not running. Starting it now..." >&2
    
    # Try to pull the latest image, fallback to local build
    echo "WSL Bridge: Attempting to pull latest image from GHCR..." >&2
    if docker pull ghcr.io/sajonaro/mcp-mssql-query:latest 2>&1 | grep -q "Downloaded\|up to date"; then
        echo "WSL Bridge: Using image from registry" >&2
        IMAGE_NAME="ghcr.io/sajonaro/mcp-mssql-query:latest"
    else
        echo "WSL Bridge: Failed to pull image. Building locally..." >&2
        docker build -t mssql-query-server . >&2
        IMAGE_NAME="mssql-query-server"
    fi
    
    # Stop and remove any existing stopped container with the same name
    docker rm mssql-query-mcp 2>/dev/null || true
    
    # Start the container in detached mode
    echo "WSL Bridge: Starting container with environment variables..." >&2
    docker run -d \
        --name mssql-query-mcp \
        -i \
        --restart unless-stopped \
        --env-file .env \
        "$IMAGE_NAME" >&2
    
    echo "WSL Bridge: Container started successfully" >&2
else
    echo "WSL Bridge: Container already running" >&2
fi

echo "WSL Bridge: Connecting to container..." >&2
echo "WSL Bridge: Environment variables:" >&2
echo "  MSSQL_SERVER=$MSSQL_SERVER" >&2
echo "  MSSQL_DATABASE=$MSSQL_DATABASE" >&2
echo "  MSSQL_USERNAME=$MSSQL_USERNAME" >&2

exec docker exec -i \
    -e MSSQL_SERVER="$MSSQL_SERVER" \
    -e MSSQL_DATABASE="$MSSQL_DATABASE" \
    -e MSSQL_USERNAME="$MSSQL_USERNAME" \
    -e MSSQL_PASSWORD="$MSSQL_PASSWORD" \
    mssql-query-mcp uv run main.py
