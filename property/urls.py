from django.urls import path
from . import views

urlpatterns = [
    path('marketplace/', views.marketplace, name='marketplace'),
    path('buy/', views.buy_properties, name='buy_properties'),
    path('rent/', views.rent_properties, name='rent_properties'),
]