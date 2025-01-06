from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "quantity", "price", "status", "is_archived")
    list_filter = ("category", "status", "is_archived")
    search_fields = ("name", "identifier")
    ordering = ("name",)


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "region", "inn", "phone_number_1", "is_archived")
    list_filter = ("region", "is_archived")
    search_fields = ("full_name", "inn", "phone_number_1")


@admin.register(SalesHistory)
class SalesHistoryAdmin(admin.ModelAdmin):
    list_display = ("distributor", "product", "quantity", "sale_date", "total_sum")
    list_filter = ("sale_date",)
    search_fields = ("distributor__full_name", "product__name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "distributor", "created_at", "total_amount")
    list_filter = ("created_at",)
    search_fields = ("invoice_number", "distributor__full_name")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "total")
    search_fields = ("order__invoice_number", "product__name")


@admin.register(ReturnHistory)
class ReturnHistoryAdmin(admin.ModelAdmin):
    list_display = ("distributor", "product", "quantity", "return_date", "return_status", "total_sum")
    list_filter = ("return_date", "return_status")
    search_fields = ("distributor__full_name", "product__name")
