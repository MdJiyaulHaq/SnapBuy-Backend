# SnapBuy Backend

A clean, production-ready Django REST Framework backend for an e-commerce platform built with clean architecture principles.

## Features

- ✅ Clean Architecture with modular apps structure
- ✅ Django REST Framework API with Swagger documentation
- ✅ JWT Authentication (SimpleJWT + Djoser)
- ✅ Celery for async tasks with Redis
- ✅ PostgreSQL database (SQLite for development)
- ✅ Unified Docker Compose for all environments
- ✅ Development and production ready

## Tech Stack

- **Framework**: Django 5.0.4, Django REST Framework 3.15.2
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL 13+ (SQLite for dev)
- **Cache/Queue**: Redis 6+ with Celery 5.4.0
- **Documentation**: Swagger/OpenAPI (drf-yasg)
- **Admin**: Django Admin
- **Containerization**: Docker & Docker Compose

## Project Structure

```
config/                      # Django settings & configuration
├── settings.py            # Settings (env-driven)
├── urls.py                # Root URL routing
├── wsgi.py, asgi.py       # Application servers
└── celery.py              # Celery configuration

apps/                        # Modular Django applications
├── core/                  # User/auth models & views
├── store/                 # Products, orders, carts
├── tags/                  # Tag management
├── likes/                 # User likes
└── playground/            # Testing utilities

docker-compose.yml          # Production Docker Compose
docker-compose.local.yml    # Local dev overrides
.env.example               # Local dev env template
.env.prod.example          # Production env template
```

## Prerequisites

- **For Docker** (Recommended): Docker & Docker Compose only
- **For Local Dev**: Python 3.10+, PostgreSQL 13+, Redis 6+ (optional)

## Quick Start

### 🚀 Option 1: Docker Development (Recommended)

**Same environment for dev and production - fastest setup.**

```bash
# 1. Setup environment
cp .env.example .env

# 2. Start all services (uses docker-compose.override.yml automatically)
docker-compose up -d

# 3. Run migrations
docker-compose exec web python manage.py migrate

# 4. Create superuser
docker-compose exec web python manage.py createsuperuser
```

**Access the application:**
- API Documentation: http://localhost:8000/api/docs/
- Admin Panel: http://localhost:8000/admin/
- API Base: http://localhost:8000/api/v1/

**Services running:**
- Django API (port 8000)
- PostgreSQL (port 5432)
- Redis (port 6379)
- Celery Worker
- Celery Beat (scheduled tasks)

**Useful commands:**
```bash
docker-compose logs -f web          # Watch Django logs
docker-compose logs -f celery       # Watch Celery logs
docker-compose ps                   # Show running containers
docker-compose down                 # Stop all services
docker-compose down -v              # Stop and delete volumes
```

### 🔒 Option 2: Production Deployment (Self-Hosted)

**Deploy with Nginx, security hardening, and persistent data.**

```bash
# 1. Create and configure production environment
cp .env.example .env
# Edit .env with your production values:
# - SECRET_KEY: Generate a strong one
# - POSTGRES_PASSWORD: Use a strong password
# - ALLOWED_HOSTS: Your domain
# - CORS_ALLOWED_ORIGINS: Your frontend domain

# 2. Start production services
docker-compose up -d

# 3. Run migrations
docker-compose exec web python manage.py migrate

# 4. Create superuser
docker-compose exec web python manage.py createsuperuser
```

### ☁️ Option 2b: Deploy to Render

**Deploy using Render's managed infrastructure.**

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New" → "Blueprint"
4. Connect your repository
5. Render will auto-detect `render.yaml` and create:
   - Web service (Django API)
   - Worker services (Celery)
   - PostgreSQL database
   - Redis cache
6. Update environment variables in Render dashboard:
   - `ALLOWED_HOSTS`: `your-app.onrender.com`
   - `CORS_ALLOWED_ORIGINS`: Your frontend URL

**Production includes:**
- Nginx reverse proxy (port 80/443)
- Gunicorn with 4 workers
- PostgreSQL with persistent volumes
- Redis for caching and tasks
- Celery workers
- Auto-restart and health checks

### 💻 Option 3: Local Development (Without Docker)

**For development without Docker containers.**

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements-dev.txt

# 3. Configure environment
cp .env.example .env

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver
```

Access at: http://localhost:8000/api/docs/

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/docs/schema/

### Key Endpoints

```
Authentication:
  POST   /api/v1/auth/token/         - Get JWT token
  POST   /api/v1/auth/token/refresh/ - Refresh token
  POST   /api/v1/auth/users/         - Register

Store:
  GET    /api/v1/store/products/     - List products
  POST   /api/v1/store/orders/       - Create order
  GET    /api/v1/store/carts/        - Get cart

Admin:
  GET    /admin/                      - Django admin panel
```

## Development

### Running Tests

```bash
pytest                      # All tests
pytest apps/store/tests/    # Specific app
pytest --cov=apps          # With coverage
```

### Code Quality

```bash
black .          # Format code
flake8 .         # Lint
isort .          # Sort imports
```

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations --empty core --name migration_name  # Create empty
```

### Create Superuser

```bash
python manage.py createsuperuser
# Or in Docker:
docker-compose exec web python manage.py createsuperuser
```

## Environment Variables

### Local Development (.env)
```
DEBUG=True
SECRET_KEY=dev-key-not-secure
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
POSTGRES_DB=snapbuy_dev
POSTGRES_PASSWORD=snapbuy_dev
```

### Production (.env)
```
DEBUG=False
SECRET_KEY=<generate-a-strong-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
POSTGRES_PASSWORD=<strong-password>
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

See `.env.example` and `.env.prod.example` for all available options.

## Troubleshooting

### Port Already in Use
```bash
# Change port in .env
WEB_PORT=8001
docker-compose up -d
```

### Database Migration Errors
```bash
docker-compose exec web python manage.py migrate --run-syncdb
```

### Permission Denied in Admin
```bash
# Make sure user is superuser
docker-compose exec web python manage.py shell
# In shell:
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='your_username')
user.is_staff = True
user.is_superuser = True
user.save()
```

### Clear Everything and Restart
```bash
docker-compose down -v
docker-compose up -d
```

## Architecture

**Clean Architecture Layers:**
- **Config**: Central Django settings and URL routing
- **Apps**: Self-contained modules (core, store, tags, likes, playground)
- **Infrastructure**: Database, cache, message queue

**Each app contains:**
- `models.py` - Data models
- `views.py` - API viewsets
- `serializers.py` - Data serialization
- `urls.py` - URL routing
- `admin.py` - Django admin
- `migrations/` - Database changes

## Deployment Checklist

- [ ] Update `.env` with production values
- [ ] Generate strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure Redis/cache
- [ ] Set up email service
- [ ] Configure CORS for frontend
- [ ] Set up SSL certificates
- [ ] Run migrations
- [ ] Create superuser
- [ ] Test API endpoints
- [ ] Monitor logs

## Common Commands

```bash
# Development
docker-compose up -d              # Start development
docker-compose down               # Stop services
docker-compose logs -f web        # Watch logs
docker-compose exec web bash      # Access container shell

# Production
docker-compose up -d
docker-compose down
docker-compose logs -f web

# Management
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

## License

MIT License
