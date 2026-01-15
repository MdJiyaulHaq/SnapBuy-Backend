#!/bin/bash

# SnapBuy Backend - Development Setup Script

set -e

echo "🚀 SnapBuy Backend - Development Setup"
echo "======================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
else
    echo -e "${GREEN}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created. Please update it with your configuration.${NC}"
else
    echo -e "${GREEN}.env file already exists${NC}"
fi

# Create logs directory
mkdir -p logs

# Run migrations
echo -e "${BLUE}Running migrations...${NC}"
python manage.py migrate

# Create superuser
echo -e "${BLUE}Creating superuser...${NC}"
echo "Enter superuser details:"
python manage.py createsuperuser

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "To start development server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "To start Celery worker:"
echo "  celery -A config worker -l info"
echo ""
echo "To start Celery Beat:"
echo "  celery -A config beat -l info"
echo ""
echo "API Documentation:"
echo "  Swagger: http://localhost:8000/api/docs/swagger/"
echo "  ReDoc: http://localhost:8000/api/docs/redoc/"
