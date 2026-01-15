#!/bin/bash

# SnapBuy Backend - Docker Development Script

echo "🚀 SnapBuy Backend - Docker Setup"
echo "=================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env created. Please update database credentials.${NC}"
fi

# Build and start containers
echo -e "${BLUE}Building and starting containers...${NC}"
docker-compose up -d

# Wait for database to be ready
echo -e "${BLUE}Waiting for database to be ready...${NC}"
sleep 10

# Run migrations
echo -e "${BLUE}Running migrations...${NC}"
docker-compose exec -T web python manage.py migrate

# Create superuser
echo -e "${BLUE}Creating superuser...${NC}"
docker-compose exec web python manage.py createsuperuser

# Collect static files
echo -e "${BLUE}Collecting static files...${NC}"
docker-compose exec -T web python manage.py collectstatic --noinput

echo ""
echo -e "${GREEN}✅ Docker setup complete!${NC}"
echo ""
echo "Services are running:"
echo "  🌐 API: http://localhost:8000"
echo "  🔐 Admin: http://localhost:8000/admin/"
echo "  📚 Swagger: http://localhost:8000/api/docs/swagger/"
echo "  📖 ReDoc: http://localhost:8000/api/docs/redoc/"
echo "  📊 Flower (Celery): http://localhost:5555 (if enabled)"
echo ""
echo "Common commands:"
echo "  docker-compose logs -f web       # View web logs"
echo "  docker-compose logs -f celery    # View Celery logs"
echo "  docker-compose exec web bash     # Access container shell"
echo "  docker-compose down              # Stop all containers"
