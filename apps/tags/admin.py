from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Tag


# Register your models here.
@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]
