from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('api/pages/', views.page_list, name='page-list'),
    path('api/pages/<slug:slug>/', views.page_detail, name='page-detail'),
    path('api/contact/', views.contact_message, name='contact-message'),
]
