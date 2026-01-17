#!/bin/bash

# Accelerated Report App - Quick Start Script
# This script starts both backend and frontend servers

set -e

echo "🚀 Starting Accelerated Report App..."
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if backend setup is needed
if [ ! -d "backend/.venv" ]; then
    echo -e "${YELLOW}⚙️  Setting up backend (first time only)...${NC}"
    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -q -r requirements.txt
    
    # Create .env if it doesn't exist
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Remember to add your Sentry DSN to backend/.env${NC}"
    fi
    cd ..
    echo -e "${GREEN}✅ Backend setup complete!${NC}"
    echo ""
fi

# Kill any existing processes on ports 8000 and 3000
echo -e "${BLUE}🧹 Cleaning up existing processes...${NC}"
lsof -ti :8000 | xargs kill -9 2>/dev/null || true
lsof -ti :3000 | xargs kill -9 2>/dev/null || true
sleep 1

# Start backend
echo -e "${BLUE}🔧 Starting backend server...${NC}"
cd backend
nohup .venv/bin/uvicorn main:app --reload --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
echo -e "${GREEN}✅ Backend running on http://localhost:8000 (PID: $BACKEND_PID)${NC}"

# Wait for backend to start
sleep 2

# Start frontend
echo -e "${BLUE}🎨 Starting frontend server...${NC}"
cd frontend
nohup python3 -m http.server 3000 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo -e "${GREEN}✅ Frontend running on http://localhost:3000 (PID: $FRONTEND_PID)${NC}"

# Wait for frontend to start
sleep 1

# Test backend
echo ""
echo -e "${BLUE}🧪 Testing backend...${NC}"
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend is healthy!${NC}"
else
    echo -e "${YELLOW}⚠️  Backend health check failed. Check backend.log for errors.${NC}"
fi

# Print summary
echo ""
echo "======================================"
echo -e "${GREEN}🎉 All services started successfully!${NC}"
echo "======================================"
echo ""
echo "📍 URLs:"
echo "   • Frontend:       http://localhost:3000"
echo "   • API:            http://localhost:8000"
echo "   • API Docs:       http://localhost:8000/docs"
echo "   • Dashboard:      http://localhost:3000/dashboard.html"
echo ""
echo "📊 Process IDs:"
echo "   • Backend:  $BACKEND_PID"
echo "   • Frontend: $FRONTEND_PID"
echo ""
echo "📝 Logs:"
echo "   • Backend:  tail -f backend.log"
echo "   • Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop all services:"
echo "   ./stop.sh"
echo ""
echo -e "${YELLOW}💡 Tip: Make sure to add your Sentry DSN to backend/.env${NC}"
echo ""

# Open browser (optional)
if command -v open &> /dev/null; then
    echo "🌐 Opening browser..."
    sleep 2
    open http://localhost:3000
fi
