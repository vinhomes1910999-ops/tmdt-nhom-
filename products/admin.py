from django.contrib import admin

# Register your models here.
# products/admin.py
from django.contrib import admin
from .models import Category, Product, ProductImage, Promotion, Review, Comment

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Promotion)
admin.site.register(Review)
admin.site.register(Comment)