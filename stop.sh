#!/bin/bash

# Accelerated Report App - Stop Script
# This script stops both backend and frontend servers

echo "🛑 Stopping Accelerated Report App..."
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Kill processes on ports 8000 and 3000
echo "Stopping backend (port 8000)..."
lsof -ti :8000 | xargs kill -9 2>/dev/null && echo -e "${GREEN}✅ Backend stopped${NC}" || echo -e "${RED}❌ No backend process found${NC}"

echo "Stopping frontend (port 3000)..."
lsof -ti :3000 | xargs kill -9 2>/dev/null && echo -e "${GREEN}✅ Frontend stopped${NC}" || echo -e "${RED}❌ No frontend process found${NC}"

echo ""
echo "======================================"
echo -e "${GREEN}✅ All services stopped${NC}"
echo "======================================"
