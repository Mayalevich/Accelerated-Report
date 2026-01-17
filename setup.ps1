# Accelerated Report App - Setup Script (Windows)
# This script helps you set up the project quickly

Write-Host "🚀 Accelerated Report App - Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "📋 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "   Found: $pythonVersion" -ForegroundColor Green

# Navigate to backend
Write-Host ""
Write-Host "📦 Setting up backend..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "   Creating virtual environment..." -ForegroundColor Gray
    python -m venv .venv
} else {
    Write-Host "   Virtual environment already exists" -ForegroundColor Gray
}

# Activate virtual environment
Write-Host "   Activating virtual environment..." -ForegroundColor Gray
.\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "   Installing dependencies..." -ForegroundColor Gray
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "   Creating .env file..." -ForegroundColor Gray
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit backend\.env and add your Sentry DSN" -ForegroundColor Yellow
    Write-Host "   Get your DSN from: https://sentry.io" -ForegroundColor Yellow
} else {
    Write-Host "   .env file already exists" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Edit backend\.env and add your Sentry DSN"
Write-Host "   2. Start backend: cd backend && .\.venv\Scripts\activate && uvicorn main:app --reload"
Write-Host "   3. Open frontend\index.html in your browser"
Write-Host "   4. Read QUICKSTART.md for detailed instructions"
Write-Host ""
Write-Host "🎯 Test Sentry: Visit http://localhost:8000/boom after starting the backend" -ForegroundColor Yellow
Write-Host ""
