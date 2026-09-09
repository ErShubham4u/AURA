
from django.contrib import admin

from .models import Product, Order, OrderItem


# ==========================================
# PRODUCT ADMIN
# ==========================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "discount_price",
        "stock",
        "size",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "category",
        "is_featured",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "fragrance_notes",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = (
        "-created_at",
    )


# ==========================================
# ORDER ITEM INLINE
# ==========================================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False

    fields = (
        "product",
        "quantity",
        "price",
        "total",
    )

    readonly_fields = (
        "product",
        "quantity",
        "price",
        "total",
    )


# ==========================================
# ORDER ADMIN
# ==========================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "mobile",
        "city",
        "pincode",
        "total_amount",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "city",
        "created_at",
    )

    search_fields = (
        "name",
        "mobile",
        "city",
        "pincode",
        "address",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    inlines = [
        OrderItemInline,
    ]


# ==========================================
# ORDER ITEM ADMIN
# ==========================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "total",
    )

    list_filter = (
        "product",
    )

    search_fields = (
        "product__name",
        "order__name",
        "order__mobile",
    )

    ordering = (
        "-id",
    )
