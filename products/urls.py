from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Trang chủ
    path('', views.home_view, name='home'),

    # Danh sách sản phẩm & lọc theo danh mục
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.product_list, name='category_products'),

    # Chi tiết sản phẩm
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),

    # Đánh giá & bình luận sản phẩm
    path('<int:product_id>/review/', views.add_review, name='add_review'),
    path('<int:product_id>/comment/', views.add_comment, name='add_comment'),
]
