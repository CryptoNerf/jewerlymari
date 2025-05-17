from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from goods.models import Categories, Products

def buypage(request, category_slug=None):
    categories = Categories.objects.all()
    page = request.GET.get('page', 1)

    if category_slug and category_slug != 'all':
        products = Products.objects.filter(category__slug=category_slug)
    else:
        products = Products.objects.all()

    paginator = Paginator(products, 6)
    current_page = paginator.get_page(page)

    context = {
        "categories": categories,
        "goods": current_page,
        "category_slug": category_slug,
        "paginator": paginator,
        "page_obj": current_page
    }
    return render(request, "main/buypage.html", context)

def about(request):
    context = {
        'title': 'О нас',
        'content': "О нас",
        'textonpage': "СЛОВО СЛОВО СЛОВО",
    }
    return render(request, 'main/about.html', context)

def product(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    context = {
        'product': product
    }
    return render(request, "goods/product.html", context=context)
