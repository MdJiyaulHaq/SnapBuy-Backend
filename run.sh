#!/bin/bash

# SnapBuy Backend - Simple Startup Script

echo "🚀 SnapBuy Backend - Starting..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p media
mkdir -p staticfiles

# Ensure .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "✅ Starting development server on http://localhost:8000"
python manage.py runserver
