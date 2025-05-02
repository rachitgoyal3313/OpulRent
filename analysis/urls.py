from django.urls import path
from . import views

urlpatterns = [
    path("analyze/", views.analyze, name='analyze'),
    # path("predict-investment/", views.predict_investment, name='predict_investment'),  # Commented out
]
