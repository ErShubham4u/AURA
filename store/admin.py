

from django.contrib import admin
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "discount_price",
        "stock",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "category",
        "is_featured",
    )

    search_fields = (
        "name",
        "description",
        "fragrance_notes",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "mobile",
        "total_amount",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "name",
        "mobile",
        "city",
        "pincode",
    )