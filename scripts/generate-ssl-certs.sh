#!/bin/bash
set -e

CERTS_DIR="./certs"

echo "Generating self-signed SSL certificates..."

# Create certs directory if it doesn't exist
mkdir -p "$CERTS_DIR"

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$CERTS_DIR/key.pem" \
    -out "$CERTS_DIR/cert.pem" \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

chmod 600 "$CERTS_DIR/key.pem"
chmod 644 "$CERTS_DIR/cert.pem"

echo "✓ SSL certificates generated successfully in $CERTS_DIR/"
echo "  - Certificate: $CERTS_DIR/cert.pem"
echo "  - Private Key: $CERTS_DIR/key.pem"
echo ""
echo "Note: These are self-signed certificates for development/testing."
echo "For production, use proper SSL certificates from a trusted CA or Let's Encrypt."
