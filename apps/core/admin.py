from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html

from apps.store.admin import ProductAdmin, ProductImageInline
from apps.store.models import Product
from apps.tags.models import TaggedItem

from .models import User, Group


class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ["tag"]
    extra = 1


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)

# Unregister the default Django Group to avoid duplication
admin.site.unregister(DjangoGroup)


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "is_superuser"]
    list_filter = ["is_staff", "is_superuser", "is_active"]
    search_fields = ["username", "email"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )
    readonly_fields = ["date_joined", "last_login"]


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    list_display = ["name"]
    search_fields = ["name"]

