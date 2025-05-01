from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name='home'),
    path("marketplace/", views.marketplace, name='marketplace'),
    path("analyze/", views.analyze, name='analyze'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("mint/", views.mint, name='mint'),
    path("propertydetail/", views.mint, name='property_detail'),
]