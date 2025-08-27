#!/usr/bin/env python3

import sys
import socket


def test_basic_connection():
    """Test basic TCP connection to SQL Server port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(("20.157.206.39", 1433))
        sock.close()

        if result == 0:
            print("✓ TCP connection to 20.157.206.39:1433 successful")
            return True
        else:
            print("✗ TCP connection failed")
            return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False


def test_sql_connection():
    """Test SQL Server connection with credentials"""
    try:
        import pyodbc

        # Connection string for SQL Server with Microsoft ODBC Driver 17
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=20.157.206.39;"
            "DATABASE=poc_db_aggregated;"
            "UID=zed;"
            "PWD=TempSA_Password123!;"
            "TrustServerCertificate=yes;"
        )

        print("Attempting SQL Server connection...")
        conn = pyodbc.connect(connection_string, timeout=10)

        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]

        print("✓ SQL Server connection successful!")
        print(f"✓ SQL Server version: {version[:50]}...")

        # Test database access
        cursor.execute("SELECT DB_NAME()")
        db_name = cursor.fetchone()[0]
        print(f"✓ Connected to database: {db_name}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"✗ SQL Server connection failed: {e}")
        return False


if __name__ == "__main__":
    print("=== SQL Server Connection Test ===")
    print("Target: 20.157.206.39:1433")
    print("Instance: MSSQLSERVER01")
    print("Database: poc_db")
    print()

    # Test basic TCP connection
    print("1. Testing TCP connection...")
    tcp_ok = test_basic_connection()

    if tcp_ok:
        print("\n2. Testing SQL Server authentication...")
        test_sql_connection()
    else:
        print("\n✗ Cannot proceed with SQL test - TCP connection failed")
        sys.exit(1)
