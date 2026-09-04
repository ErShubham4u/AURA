from django.shortcuts import render

def home(request):
    return render(request, "store/home.html")

from django.shortcuts import render
from .models import Product


def home(request):

    products = Product.objects.filter(
        is_featured=True
    )

    return render(
        request,
        "store/home.html",
        {
            "products": products
        }
    )