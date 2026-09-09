from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("men/", views.men_products, name="men"),
    path("women/", views.women_products, name="women"),
    path("unisex/", views.unisex_products, name="unisex"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
    "cart/increase/<int:product_id>/",
    views.increase_quantity,
    name="increase_quantity"
),

path(
    "cart/decrease/<int:product_id>/",
    views.decrease_quantity,
    name="decrease_quantity"
),

path(
    "cart/remove/<int:product_id>/",
    views.remove_from_cart,
    name="remove_from_cart"
),

path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),
]