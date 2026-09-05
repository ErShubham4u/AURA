from django.shortcuts import render
from .models import Product


def home(request):
    products = Product.objects.filter(is_featured=True)

    return render(
        request,
        "store/home.html",
        {"products": products}
    )


def shop(request):
    products = Product.objects.all().order_by("-created_at")

    return render(
        request,
        "store/shop.html",
        {"products": products}
    )


def men_products(request):
    products = Product.objects.filter(category="men")

    return render(
        request,
        "store/shop.html",
        {"products": products, "category_name": "Men's Perfumes"}
    )


def women_products(request):
    products = Product.objects.filter(category="women")

    return render(
        request,
        "store/shop.html",
        {"products": products, "category_name": "Women's Perfumes"}
    )


def unisex_products(request):
    products = Product.objects.filter(category="unisex")

    return render(
        request,
        "store/shop.html",
        {"products": products, "category_name": "Unisex Perfumes"}
    )