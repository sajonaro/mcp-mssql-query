#! /usr/bin/env bash

echo "Building mssql-query MCP server Docker image..."
docker build -t mssql-query-server .

echo "Stopping any existing mssql-query-mcp container..."
docker stop mssql-query-mcp 2>/dev/null || true
docker rm mssql-query-mcp 2>/dev/null || true

echo "Starting mssql-query-mcp container..."
docker run -d --name mssql-query-mcp -i --restart unless-stopped mssql-query-server

echo "Checking container status..."
docker ps | grep mssql-query-mcp

echo "mssql-query MCP server container started successfully!"
echo "Container logs can be viewed with: docker logs mssql-query-mcp"