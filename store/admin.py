from django.contrib import admin
from .models import Product


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