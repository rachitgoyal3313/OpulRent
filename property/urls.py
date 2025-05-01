from django.urls import path
from . import views

urlpatterns = [
    path('marketplace/', views.marketplace, name='marketplace'),
    path('mint/', views.mint, name='mint'),
    path('buy/', views.buy_properties, name='buy_properties'),
    path('rent/', views.rent_properties, name='rent_properties'),
    path('property/<int:property_id>/<str:property_type>/', views.property_detail, name='property_detail'),
    path('property/<int:property_id>/<str:property_type>/action/', views.property_action, name='property_action'),
    path('property/<int:property_id>/purchase/confirmation/', views.purchase_confirmation, name='purchase_confirmation'),
    path('property/<int:property_id>/rental/confirmation/', views.rental_confirmation, name='rental_confirmation'),
]