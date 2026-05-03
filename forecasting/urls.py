from django.urls import path
from . import views

urlpatterns = [
    path('revenue/', views.RevenueForecastView.as_view(), name='forecast_revenue'),
    path('products/', views.ProductDemandForecastView.as_view(), name='forecast_products'),
]