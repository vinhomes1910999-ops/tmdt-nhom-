from django.contrib import admin
from .models import Category, Product, ProductImage, Promotion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock']
    list_filter = ['category', 'gender', 'is_active']
    search_fields = ['name']
    inlines = [ProductImageInline]

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_value', 'discount_type', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code']
