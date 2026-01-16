FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p logs media staticfiles

# Collect static files at build time
RUN python manage.py collectstatic --noinput --clear || true

# Expose port (Render uses $PORT env var)
EXPOSE 8000

# Run gunicorn - use $PORT for Render compatibility
CMD gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4
