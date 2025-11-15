## About

This project builds an MCP server allowing CLAUDE desktop to query MSSQL database

## Configuration

Before running the server, configure your MSSQL database connection by creating a `.env` file in the project root with the following parameters:

```env
MSSQL_SERVER="your_server_address"
MSSQL_DATABASE="your_database_name"
MSSQL_USERNAME="your_username"
MSSQL_PASSWORD="your_password"
```

## How to run

The setup uses **lazy initialization** - the Docker container will be automatically pulled from GHCR and started the first time Claude Desktop uses it. No manual setup required!

**Step 1**: Make the invoke script executable and copy to a well-known location:

```bash
$ chmod +x invoke-mssql-query-mcp.sh && cp invoke-mssql-query-mcp.sh /usr/local/bin
```

**Step 2**: Configure Claude Desktop by locating `claude_desktop_config.json` (typically at: `C:\Users\{YOUR_USER}\AppData\Roaming\Claude`) and add the MCP server configuration:

```json
{
  "mcpServers": {
    "mssql-query-mcp": {
      "command": "wsl",
      "args": ["/usr/local/bin/invoke-mssql-query-mcp.sh"]
    }
  }
}
```

**Step 3**: Restart Claude Desktop. 

The first time you use the MCP server, the `invoke-mssql-query-mcp.sh` script will automatically:
- Pull the latest Docker image from GitHub Container Registry (ghcr.io/sajonaro/mcp-mssql-query:latest)
- If GHCR pull fails, it will build the image locally from the Dockerfile
- Start the container in detached mode with automatic restart policy
- Connect to your MSSQL database using the `.env` configuration

On subsequent uses, it will simply connect to the already-running container for instant response.
