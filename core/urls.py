from django.urls import path
from . import views

urlpatterns =[
    path("cart-details/", views.cart_detail, name='cart-details'),
    path('', views.product_list, name='product-list'),
    path('<slug:category_slug>/', views.product_list, name='product-list-by-category'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product-detail'),
    path("add/<int:product_id>/", views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='remove'),
]