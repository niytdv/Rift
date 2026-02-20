#!/bin/bash
set -e

echo "=== Starting Build Process ==="

echo "Step 1: Installing Python dependencies..."
mkdir -p .python_packages
python3 -m pip install --upgrade pip
python3 -m pip install --target=.python_packages pandas networkx python-dateutil

echo "Step 2: Installing Node.js dependencies..."
npm ci

echo "Step 3: Building Next.js application..."
npm run build

echo "Step 4: Verifying build..."
ls -la .next/ || echo "Warning: .next directory not found"

echo "=== Build Complete ==="
