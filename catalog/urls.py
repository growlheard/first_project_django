from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('index/<int:pk>/', views.product_detail, name='product_detail'),
    path('index/', views.index, name='index'),
]