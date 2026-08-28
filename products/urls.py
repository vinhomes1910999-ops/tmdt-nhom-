from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Review sản phẩm
    path(
        '<int:product_id>/review/',
        views.add_review,
        name='add_review'
    ),

    # Comment sản phẩm
    path(
        '<int:product_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
]
