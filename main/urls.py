from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.buypage, name='buypage'),
    path('category/<slug:category_slug>/', views.buypage, name='category'),
    path('product/<slug:product_slug>/', views.product, name='product'),
    path('about/', views.about, name='about'),
]
