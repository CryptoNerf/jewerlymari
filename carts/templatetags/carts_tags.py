# templatetags/carts_tags.py
from django import template
from carts.models import Cart

register = template.Library()

@register.simple_tag()
def user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(account=request.user)
    return Cart.objects.none()
