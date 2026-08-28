from rest_framework import serializers
from .models import Category, Product, ProductImage, Promotion

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary']

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    current_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'price', 'current_price', 'rating', 'is_featured']

    def get_current_price(self, obj):
        return float(obj.current_price)

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    current_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'description', 'price', 'current_price', 'discount_price', 'gender', 'size', 'color', 'stock', 'rating', 'is_featured', 'images']

    def get_current_price(self, obj):
        return float(obj.current_price)

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'code', 'description', 'discount_type', 'discount_value', 'min_purchase']
