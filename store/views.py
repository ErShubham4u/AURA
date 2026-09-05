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