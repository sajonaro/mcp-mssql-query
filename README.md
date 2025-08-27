## About

This project builds an MCP server allowing CLAUDE desktop to query MSSQL database

## How to run

**step 1** : 
```bash
# build & run docker image with server
$ ./start.sh
```

**step 2** : 
```bash
# create a command to execute our mcp server 
# or just use existing wsl-bridge-mssql-query-mcp.sh:
# we may simply put it into well known location e.g.:
$ chown +x wsl-bridge-mssql-query-mcp.sh && cp wsl-bridge-mssql-query-mcp.sh /usr/local/bin
```

**step 3** : 

```json
locate claude_desktop_config ( typically at: C:\Users\{YOUR_USER}\AppData\Roaming\Claude), and update it with new mcp service record
// e.g.
{
  "mcpServers": {
        "mssql-query-mcp": {
          "command": "wsl",
          "args": ["/usr/local/bin/wsl-bridge-mssql-query-mcp.sh"]
        }
  }
}

```