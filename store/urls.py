from django.urls import path

from .views import ProductListView, add_to_cart, cart_detail

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("cart/", cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
]
