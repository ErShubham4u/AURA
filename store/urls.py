from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("men/", views.men_products, name="men"),
    path("women/", views.women_products, name="women"),
    path("unisex/", views.unisex_products, name="unisex"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
]