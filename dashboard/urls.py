from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name='home'),
    path("marketplace/", views.marketplace, name='marketplace'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("propertydetail/", views.dashboard, name='property_detail'),
]