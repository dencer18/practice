from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from .admin_mixins import ExportAsCSVMixin

from .models import Product, Order



class OrderInline(admin.TabularInline):
    model = Product.orders.through
    extra=0

@admin.action(description="Archived product")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description="Unarchived product")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived", "created_by",
    list_display_links="pk", "name"
    ordering = "-pk",
    search_fields = "name", "description", "discount"
    fieldsets = [
        (None, {
            "fields": ("name","description")
        }),
        ("Price options",{
            "fields": ("price", "discount",),
            "classes": ("wide","collapse",),
        }),
        (
            ("Extra options", {
                "fields": ("archived",),
                "classes": ("collapse",),
                "description": "Extra options. Field 'arhived' is for soft delete",
            })
        )
    ]
   
    def description_short(self, obj: Product)->str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."
    
    description_short.short_description = "Short descr"


class ProductInline(admin.StackedInline):
    model = Order.products.through
    extra=0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_adress", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj:Order)->str:
        return obj.user.first_name or obj.user.username
