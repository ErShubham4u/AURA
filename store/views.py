from django.shortcuts import render, redirect, get_object_or_404
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


def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )

    return render(
        request,
        "store/product_detail.html",
        {"product": product}
    )


def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def cart(request):

    cart_data = request.session.get("cart", {})

    cart_items = []
    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        item_total = product.discount_price or product.price
        item_total = item_total * quantity

        total += item_total

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "item_total": item_total,
        })

    return render(
        request,
        "store/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


def increase_quantity(request, product_id):

    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def decrease_quantity(request, product_id):

    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, product_id):

    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")