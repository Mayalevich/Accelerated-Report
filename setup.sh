#!/bin/bash

# Accelerated Report App - Setup Script
# This script helps you set up the project quickly

echo "🚀 Accelerated Report App - Setup"
echo "=================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found: Python $python_version"

# Navigate to backend
echo ""
echo "📦 Setting up backend..."
cd backend || exit

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv .venv
else
    echo "   Virtual environment already exists"
fi

# Activate virtual environment
echo "   Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "   Installing dependencies..."
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "   Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit backend/.env and add your Sentry DSN"
    echo "   Get your DSN from: https://sentry.io"
else
    echo "   .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit backend/.env and add your Sentry DSN"
echo "   2. Start backend: cd backend && source .venv/bin/activate && uvicorn main:app --reload"
echo "   3. Open frontend/index.html in your browser"
echo "   4. Read QUICKSTART.md for detailed instructions"
echo ""
echo "🎯 Test Sentry: Visit http://localhost:8000/boom after starting the backend"
echo ""
