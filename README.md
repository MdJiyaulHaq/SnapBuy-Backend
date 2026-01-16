# SnapBuy Backend

Please use the credentials responsibly, expecting professionalism.

https://snapbuy-backend-c28m.onrender.com/admin/
https://snapbuy-backend-c28m.onrender.com/

user: test
password: newuser@123

Production-ready Django REST Framework e-commerce backend with clean architecture.

## Tech Stack

Django 5.0.4 • DRF • PostgreSQL • Redis • Celery • Unfold Admin • WhiteNoise

## Quick Start

**Development with Docker (Recommended):**
```bash
cp .env.example .env
docker-compose -f docker-compose.local.yml up -d --build
docker-compose -f docker-compose.local.yml exec web python manage.py createsuperuser
# Access: http://localhost:8000/admin/
```

**Local Development:**
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt && cp .env.example .env
python manage.py migrate && python manage.py createsuperuser
python manage.py runserver  # http://localhost:8000/admin/
```

**Production on Render:**
1. Push to GitHub → [Render Dashboard](https://dashboard.render.com) → New Blueprint
2. Connect repo (auto-deploys via `render.yaml`)
3. Create superuser via Render Shell

## Features

- ✅ JWT Authentication (Djoser)
- ✅ Unfold admin theme with import/export
- ✅ Celery async tasks + Beat scheduler
- ✅ Clean Architecture (modular apps)
- ✅ Auto-migrations on startup
- ✅ WhiteNoise static files
- ✅ Health check endpoint

## Key Endpoints

```
POST   /api/v1/auth/token/         - JWT token
GET    /api/v1/store/products/     - List products
POST   /api/v1/store/orders/       - Create order
GET    /admin/                      - Admin panel
GET    /api/docs/                   - API docs
```

## Useful Commands
