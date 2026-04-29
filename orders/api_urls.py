from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.OrderListView.as_view(), name='api_order_list'),
    path('create/', api_views.OrderCreateView.as_view(), name='api_order_create'),
    path('<int:pk>/', api_views.OrderDetailView.as_view(), name='api_order_detail'),
]
