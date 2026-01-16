from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm


from .models import Tag


# Register your models here.
@admin.register(Tag)
class TagAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ["label"]
    search_fields = ["label"]
