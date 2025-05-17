from django.contrib.auth import login, authenticate
from django.db.models import F, Prefetch, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.forms import UserRegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required

from orders.models import Order, OrderItem

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)

    # Измените фильтрацию заказов
    orders = (
        Order.objects.filter(account=request.user).prefetch_related(
            Prefetch(
                'orderitem_set',
                queryset=OrderItem.objects.select_related('product')
            )
        ).order_by('-id')
    )
    
    for order in orders:
        order.total_price = order.orderitem_set.aggregate(total=Sum(F('price') * F('quantity')))['total']

    context = {
        'form': form,
        'orders': orders,
    }
    return render(request, 'accounts/profile.html', context)


def accounts_cart(request):
    return render(request, 'accounts/accounts_cart.html')

def my_orders(request):

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:profile'))
        # else:
        #     # Возвращаем страницу, которая содержит модальное окно, с контекстом, чтобы показать ошибки
        #     context = {
        #         'form': form
        #     }
    else:
        form = ProfileForm(instance=request.user)

    orders = (
            Order.objects.filter(user=request.user).prefetch_related(
                Prefetch(
                    'orderitem_set',
                    queryset=OrderItem.objects.select_related('product')
                )
            ).order_by('-id')
        )
    
    for order in orders:
        order.total_price = order.orderitem_set.aggregate(total=Sum(F('price') * F('quantity')))['total']

    context = {
        "title": "Спорт Лайн - Мои заказы", 
        'form': form,
        'orders': orders,
        }
    return render(request, "accounts/profile.html", context)