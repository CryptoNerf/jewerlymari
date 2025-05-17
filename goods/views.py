from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from goods.models import Products

def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)

    if category_slug == 'all' or category_slug is None:
        goods = Products.objects.all()
    elif category_slug == 'kolechki':
        goods = Products.objects.filter(category__slug=category_slug)
    elif category_slug == 'seryozhki':
        goods = Products.objects.filter(category__slug=category_slug)
    elif category_slug == 'drugoe':
        goods = Products.objects.filter(category__slug=category_slug)
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    paginator = Paginator(goods, 6)
    current_page = paginator.get_page(page)

    context = {
        "title": "Украшения Мари - Каталог",
        "goods": current_page,
        "category_slug": category_slug,
        "paginator": paginator,
        "page_obj": current_page
    }
    return render(request, "goods/catalog.html", context)

def product(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)

    context = {
        'product': product
    }

    return render(request, "goods/product.html", context=context)
