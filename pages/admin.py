from django.contrib import admin

# Register your models here.
# pages/admin.py
from django.contrib import admin
from .models import ContactMessage, StaticPage

admin.site.register(ContactMessage)
admin.site.register(StaticPage)