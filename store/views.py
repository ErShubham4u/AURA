from django.core.serializers import python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.db import transaction


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

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from .models import Product, Order, OrderItem


def checkout(request):

    # GET CART FROM SESSION
    cart_data = request.session.get("cart", {})

    # IF CART IS EMPTY
    if not cart_data:
        return redirect("cart")

    cart_items = []
    total = 0

    # ==============================
    # GET CART PRODUCTS
    # ==============================

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        # CHECK STOCK
        if quantity > product.stock:
            return redirect("cart")

        # GET SELLING PRICE
        price = product.discount_price or product.price

        # CALCULATE ITEM TOTAL
        item_total = price * quantity

        # CALCULATE CART TOTAL
        total += item_total

        # ADD ITEM TO CART ITEMS
        cart_items.append({
            "product": product,
            "quantity": quantity,
            "item_total": item_total,
        })

    # ==============================
    # HANDLE PLACE ORDER
    # ==============================

    if request.method == "POST":

        # GET CUSTOMER DETAILS
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        payment_method = request.POST.get("payment_method")

        # ==============================
        # CREATE ORDER
        # ==============================

        with transaction.atomic():

            order = Order.objects.create(
                name=name,
                mobile=mobile,
                address=address,
                city=city,
                pincode=pincode,
                payment_method=payment_method,
                total_amount=total,
            )

            # ==============================
            # CREATE ORDER ITEMS
            # + REDUCE STOCK
            # ==============================

            for product_id, quantity in cart_data.items():

                product = get_object_or_404(
                    Product,
                    id=product_id
                )

                # CHECK STOCK AGAIN
                if quantity > product.stock:
                    return redirect("cart")

                # GET SELLING PRICE
                price = product.discount_price or product.price

                # CALCULATE ITEM TOTAL
                item_total = price * quantity

                # CREATE ORDER ITEM
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price,
                    total=item_total,
                )

                # REDUCE STOCK
                product.stock -= quantity
                product.save()

        # PRINT ORDER ID
        print("Order Created:", order.id)

        # ==============================
        # CLEAR CART
        # ==============================

        request.session["cart"] = {}
        request.session.modified = True

        # ==============================
        # ORDER SUCCESS PAGE
        # ==============================

        return render(
            request,
            "store/order_success.html",
            {
                "order": order,
            }
        )

    # ==============================
    # CHECKOUT PAGE
    # ==============================

    return render(
        request,
        "store/checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )
