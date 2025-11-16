#!/bin/bash
# Setup script for askmyuni-supportsystems

set -e  # Exit on error

echo "===== askmyuni-supportsystems Setup ====="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment (optional)
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created"
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Setup environment file
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠ Please edit .env and add your GitHub token:"
    echo "  GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    echo ""
    echo "Edit with: nano .env"
else
    echo "✓ .env file already exists"
fi

# Verify GitHub token
echo ""
echo "Checking GitHub token..."
if grep -q "GITHUB_TOKEN=ghp_" .env 2>/dev/null; then
    echo "✓ GitHub token found in .env"
else
    echo "⚠ GitHub token not configured in .env"
    echo "  Please add your token before running import commands"
fi

# Show available commands
echo ""
echo "===== Setup Complete ====="
echo ""
echo "Available commands:"
echo ""
echo "  Validate CSV (dry-run):"
echo "    python src/cli.py validate --csv data/import.csv --dry-run"
echo ""
echo "  Preview import:"
echo "    python src/cli.py preview --csv data/import.csv"
echo ""
echo "  Import to GitHub:"
echo "    python src/cli.py import --csv data/import.csv"
echo ""
echo "See QUICKSTART.md for detailed instructions."
echo ""
