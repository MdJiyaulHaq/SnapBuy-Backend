"""
URL configuration for SnapBuy API.
"""

from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from apps.core.views import home

# API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="SnapBuy API",
        default_version="v1",
        description="E-commerce Backend API",
        contact=openapi.Contact(email="support@snapbuy.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Home page
    path("", home, name="home"),
    # Admin
    path("admin/", admin.site.urls),
    # API v1
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/", include("apps.store.urls")),
    path("api/v1/", include("apps.tags.urls")),
    path("api/v1/", include("apps.likes.urls")),
    path("api/v1/", include("apps.playground.urls")),
    # API Documentation
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/docs/schema/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
]

# Debug toolbar and silk in development
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        path("silk/", include("silk.urls", namespace="silk")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
