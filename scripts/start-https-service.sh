#!/bin/bash
set -e

echo "=== MCP MSSQL Query Service - HTTPS Deployment ==="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your MSSQL configuration."
    exit 1
fi

# Check if SSL certificates exist
if [ ! -f certs/cert.pem ] || [ ! -f certs/key.pem ]; then
    echo "⚠️  SSL certificates not found. Generating self-signed certificates..."
    chmod +x scripts/generate-ssl-certs.sh
    ./scripts/generate-ssl-certs.sh
    echo ""
fi

echo "Starting HTTPS service with docker-compose..."
echo ""

# Build and start services
docker-compose -f docker-compose.https.yml up --build -d

echo ""
echo "✓ Services started successfully!"
echo ""
echo "Access your MCP service at:"
echo "  - HTTPS: https://localhost/sse"
echo "  - HTTP (redirects to HTTPS): http://localhost/sse"
echo ""
echo "To view logs:"
echo "  docker-compose -f docker-compose.https.yml logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose -f docker-compose.https.yml down"
echo ""
echo "Note: Browser may show security warning due to self-signed certificate."
echo "For production, replace certificates in ./certs/ with trusted certificates."
