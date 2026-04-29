from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.CartDetailView.as_view(), name='api_cart_detail'),
    path('add/', api_views.CartAddView.as_view(), name='api_cart_add'),
    path('remove/<int:product_id>/', api_views.CartRemoveView.as_view(), name='api_cart_remove'),
    path('clear/', api_views.CartClearView.as_view(), name='api_cart_clear'),
]
