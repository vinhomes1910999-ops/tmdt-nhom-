from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product
def cart_detail(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.all()

    total_price = sum(
        item.subtotal for item in items
    )

    return render(request, "cart/cart.html", {
        "cart_items": items,
        "total_price": total_price
    })


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1

    item.save()

    return redirect("cart:cart_detail")


def increase_quantity(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect("cart:cart_detail")


def decrease_quantity(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart:cart_detail")


def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect("cart:cart_detail")