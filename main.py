# type: ignore
from mcp.server.fastmcp import FastMCP
from typing import Optional, Any, List, Dict
import pyodbc
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the server
mcp = FastMCP("MSSQL_Query_Server")


def connect_to_db():
    """Connect to SQL Server database using SQL Server authentication"""
    server = os.getenv("MSSQL_SERVER")
    port = os.getenv("MSSQL_PORT", "1433")
    database = os.getenv("MSSQL_DATABASE")
    username = os.getenv("MSSQL_USERNAME")
    password = os.getenv("MSSQL_PASSWORD")

    # Validate required environment variables
    if not server:
        raise ValueError("MSSQL_SERVER environment variable is required")
    if not database:
        raise ValueError("MSSQL_DATABASE environment variable is required")
    if not username:
        raise ValueError("MSSQL_USERNAME environment variable is required")
    if not password:
        raise ValueError("MSSQL_PASSWORD environment variable is required")

    # Use FreeTDS driver with port and TDS protocol version
    conn_string = (
        f"DRIVER={{FreeTDS}};"
        f"SERVER={server};"
        f"PORT={port};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"TDS_Version=7.4;"
        f"TrustServerCertificate=yes;"
    )

    try:
        conn = pyodbc.connect(conn_string, timeout=30)
        return conn
    except pyodbc.Error as e:
        raise ConnectionError(f"Failed to connect to SQL Server: {str(e)}")


def is_select_query(query: str) -> bool:
    """Check if the query is a SELECT statement only - more robust validation"""
    # Remove comments and normalize whitespace
    cleaned_query = re.sub(r"--.*$", "", query, flags=re.MULTILINE)
    cleaned_query = re.sub(r"/\*.*?\*/", "", cleaned_query, flags=re.DOTALL)
    cleaned_query = re.sub(r"\s+", " ", cleaned_query.strip())

    if not cleaned_query:
        return False

    # Convert to uppercase for checking
    upper_query = cleaned_query.upper()

    # Must start with SELECT
    if not upper_query.startswith("SELECT"):
        return False

    # Check for forbidden keywords that indicate DML/DDL operations
    forbidden_patterns = [
        r"\bINSERT\b",
        r"\bUPDATE\b",
        r"\bDELETE\b",
        r"\bDROP\b",
        r"\bCREATE\b",
        r"\bALTER\b",
        r"\bTRUNCATE\b",
        r"\bEXEC\b",
        r"\bEXECUTE\b",
        r"\bSP_\w+\b",
        r"\bXP_\w+\b",
        r"\bBULK\b",
        r"\bMERGE\b",
        r"\bGRANT\b",
        r"\bREVOKE\b",
        r"\bDENY\b",
    ]

    for pattern in forbidden_patterns:
        if re.search(pattern, upper_query):
            return False

    # Additional check: ensure no semicolon followed by non-SELECT statements
    statements = [stmt.strip() for stmt in cleaned_query.split(";") if stmt.strip()]
    for stmt in statements:
        if stmt and not stmt.upper().startswith("SELECT"):
            return False

    return True


@mcp.tool()
async def execute_query(query: str) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query on the SQL Server database.
    Only SELECT statements are allowed - no INSERT, UPDATE, DELETE, or DDL operations.

    Parameters:
        query (str): The SELECT SQL query to execute

    Returns:
        List[Dict[str, Any]]: List of dictionaries representing the query results
    """

    if not is_select_query(query):
        raise ValueError(
            "Only SELECT queries are allowed. No DML or DDL operations permitted."
        )

    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        return results
    finally:
        cursor.close()
        conn.close()


@mcp.tool()
async def query_table(
    table_name: str,
    columns: Optional[str] = "*",
    where_clause: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Query a non-system table or view with optional filtering.

    Parameters:
        table_name (str): Name of the table or view to query
        columns (Optional[str]): Comma-separated list of columns to select (default: "*")
        where_clause (Optional[str]): WHERE clause conditions (without the WHERE keyword)
        limit (Optional[int]): Maximum number of rows to return

    Returns:
        List[Dict[str, Any]]: List of dictionaries representing the query results
    """

    # Build the query
    query = f"SELECT {columns} FROM {table_name}"

    if where_clause:
        query += f" WHERE {where_clause}"

    if limit:
        query += f" ORDER BY (SELECT NULL) OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY"

    return await execute_query(query)


@mcp.tool()
async def get_tables() -> List[Dict[str, Any]]:
    """
    Get the list of non-system tables in the current database.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing table information
    """

    query = """
    SELECT 
        TABLE_SCHEMA as schema_name,
        TABLE_NAME as table_name,
        TABLE_TYPE as table_type
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE'
    AND TABLE_SCHEMA NOT IN ('sys', 'information_schema')
    ORDER BY TABLE_SCHEMA, TABLE_NAME
    """

    return await execute_query(query)


@mcp.tool()
async def get_views() -> List[Dict[str, Any]]:
    """
    Get the list of non-system views in the current database.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing view information
    """

    query = """
    SELECT 
        TABLE_SCHEMA as schema_name,
        TABLE_NAME as view_name,
        VIEW_DEFINITION as definition
    FROM INFORMATION_SCHEMA.VIEWS 
    WHERE TABLE_SCHEMA NOT IN ('sys', 'information_schema')
    ORDER BY TABLE_SCHEMA, TABLE_NAME
    """

    return await execute_query(query)


if __name__ == "__main__":
    mcp.run(transport="stdio")
