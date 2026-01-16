from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

from apps.store import models
from apps.store.models import (Address, Cart, CartItem, Collection, Customer, Order,
                          OrderItem, Product, ProductImage, Promotion)


# Register your models here.
@admin.register(Promotion)
class PromotionAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    search_fields = ["description"]
    list_display = ["description", "discount"]
    list_editable = ["discount"]
    list_per_page = 10


@admin.register(Collection)
class CollectionAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ["title", "featured_product", "product_count"]
    list_per_page = 10
    search_fields = ["title"]
    autocomplete_fields = ["featured_product"]

    @admin.display(description="Product Count")
    def product_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": f"{collection.id}"})
        )
        return format_html('<a href="{}">{}</a>', url, collection.product_count)

    # Modify the base queryset to include the product count:
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count("product"))


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ["thumbnail"]

    def thumbnail(self, instance):
        if instance.image.name != "":
            return format_html(
                f'<img src = "{instance.image.url}" class = "thumbnail" /> '
            )
        return ""


@admin.register(Product)
class ProductAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    autocomplete_fields = ["collection"]
    actions = ["clear_inventory"]
    inlines = [ProductImageInline]
    list_select_related = ["collection"]
    list_display = [
        "title",
        "unit_price",
        "inventory_status",
        "collection_featured_product",
    ]
    list_editable = ["unit_price"]
    list_per_page = 10
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ["title"]}

    def collection_featured_product(self, product):
        return product.collection.featured_product

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f"{updated_count} products were successfully updated."
        )

    class Media:
        css = {"all": ["store/styles.css"]}


@admin.register(Customer)
class CustomerAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    list_per_page = 10
    search_fields = ["first_name__istartswith", "last_name__istartswith"]
    list_select_related = ["user"]
    ordering = ["user__first_name", "user__last_name"]

    def orders_count(self, customer):
        return customer.orders.count()


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ["product"]
    readonly_fields = ["unit_price"]
    extra = 1


@admin.register(Order)
class OrderAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    inlines = [OrderItemInline]
    autocomplete_fields = ["customer"]
    list_select_related = ["customer"]
    list_display = ["id", "Order_placed_at", "customer_name"]
    list_per_page = 10

    @admin.display(ordering="-placed_at")
    def customer_name(self, order):
        full_name = order.customer.user.first_name + " " + order.customer.user.last_name
        return full_name


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ["id", "order", "product", "quantity", "unit_price"]
    list_per_page = 10


@admin.register(Address)
class AddressAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ["street", "city"]
    list_per_page = 10


@admin.register(Cart)
class CartAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ["id", "created_at"]
    list_per_page = 10


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ["id", "cart", "product", "quantity"]
    list_per_page = 10
