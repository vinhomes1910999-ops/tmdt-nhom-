from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", views.add_to_cart, name="add"),
    path("increase/<int:item_id>/", views.increase_quantity, name="increase"),
    path("decrease/<int:item_id>/", views.decrease_quantity, name="decrease"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove"),
 ]