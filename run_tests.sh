#!/bin/bash

# Complete test script for Bajaj AMC Factsheet RAG Chatbot
# Installs dependencies and runs tests

set -e  # Exit on error

echo "============================================================"
echo "🚀 Bajaj AMC Factsheet RAG - Setup & Test"
echo "============================================================"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated"

    if [ -d ".venv" ]; then
        echo "📦 Activating existing virtual environment..."
        source .venv/bin/activate
    else
        echo "❌ No virtual environment found!"
        echo "Please run: python3 -m venv .venv && source .venv/bin/activate"
        exit 1
    fi
else
    echo "✅ Virtual environment active: $VIRTUAL_ENV"
fi

echo ""
echo "============================================================"
echo "📦 Installing Dependencies (CPU-only)"
echo "============================================================"

# Install PyTorch CPU-only first
echo "Installing PyTorch (CPU-only)..."
pip install torch --index-url https://download.pytorch.org/whl/cpu --quiet

# Install other dependencies
echo "Installing other dependencies..."
pip install -e . --quiet

echo "✅ Dependencies installed"

echo ""
echo "============================================================"
echo "🧪 Running System Tests"
echo "============================================================"

# Run test script
python test_setup.py

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
