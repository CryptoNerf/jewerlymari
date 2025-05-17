# carts/views.py
from django.shortcuts import redirect, render, get_object_or_404
from carts.models import Cart
from goods.models import Products

def cart_add(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(account=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(account=request.user, product=product, quantity=1)

    return redirect(request.META['HTTP_REFERER'])

def cart_change(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    action = request.GET.get('action')

    if action == 'increment':
        cart.quantity += 1
    elif action == 'decrement' and cart.quantity > 1:
        cart.quantity -= 1
    
    cart.save()
    return redirect(request.META['HTTP_REFERER'])

def cart_remove(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart.delete()
    return redirect(request.META['HTTP_REFERER'])

def cart_detail(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(account=request.user)
    else:
        carts = Cart.objects.none()  # Пустой QuerySet если пользователь не аутентифицирован

    context = {
        'carts': carts,
    }
    return render(request, 'carts/accounts_cart.html', context)
