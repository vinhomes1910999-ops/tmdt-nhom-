from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductImageViewSet, PromotionViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'images', ProductImageViewSet, basename='productimage')
router.register(r'promotions', PromotionViewSet, basename='promotion')

urlpatterns = [
    path('', include(router.urls)),
]
