from django.urls import path
from . import views

urlpatterns = [
    path("cart-details/", views.cart_detail, name='cart-detail'),
    path("add/<int:product_id>/", views.cart_add, name='cart_add'),
    path("remove/<int:product_id>/", views.cart_remove, name='remove'),
    path("create/", views.order_created, name='order_create'),
    path("confirmation/<int:order_id>/", views.order_confirmation, name='order_confirmation'),

    path("product/<int:id>/<slug:slug>/", views.product_detail, name='product-detail'),

    path("", views.product_list, name='product-list'),
    path("<slug:category_slug>/", views.product_list, name='product-list-by-category'),
]
