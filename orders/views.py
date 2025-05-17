from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
import qrcode

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from django.core.files.base import ContentFile

@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    account = request.user
                    cart_items = Cart.objects.filter(account=account)

                    if cart_items.exists():
                        order = Order.objects.create(
                            account=account,
                            phone_number=form.cleaned_data['phone_number'],
                            # requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            # payment_on_get=form.cleaned_data['payment_on_get'],
                            first_name = form.cleaned_data['first_name'],
                            last_name = form.cleaned_data['last_name'],
                        )

                        total_amount = 0  # Общая сумма заказа
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное количество товара {name} на складе. В наличии - {product.quantity}')

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()
                            total_amount += price * quantity

                        total_amount_in_cents = int(total_amount * 100)
                        qr_data = (
                        f"ST00012|Name=Украшения Мари|PersonalAcc=40817810711524044721|"
                        f"BankName=ВТБ|BIC=043601968|CorrespAcc=30101810422023601968|"
                        f"Currency=RUB|Sum={total_amount_in_cents}|Purpose=Оплата заказа №{order.id}"
                        )

                        buffer = BytesIO()
                        qr = qrcode.make(qr_data)
                        qr.save(buffer, format="PNG")

                        qr_image_file = ContentFile(buffer.getvalue(), 'qr_code.png')  # Создание файла
                        order.qr_image.save('qr_code.png', qr_image_file, save=True)
                        cart_items.delete()

                        messages.success(request, 'Заказ оформлен!')
                        return redirect(reverse("orders:qr_code", kwargs={'order_id': order.id}))
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('cart:order')  # Убедитесь, что этот URL существует и правильный
        else:
            messages.error(request, 'Форма заполнена неверно. Пожалуйста, исправьте ошибки.')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'orders': True,
    }
    return render(request, 'orders/create_order.html', context=context)


def qr_code(request, order_id):
    order = Order.objects.get(pk=order_id)  # Получение заказа по ID
    qr_image_url = order.qr_image.url if order.qr_image else None  # URL изображения QR-кода

    context = {
        'qr_image_url': qr_image_url,  # Передача URL изображения в контекст
    }

    return render(request, 'orders/qr_code.html', context)