from django.urls import path
from . import api_views

urlpatterns = [
    path('categories/', api_views.CategoryListView.as_view(), name='api_category_list'),
    path('', api_views.ProductListView.as_view(), name='api_product_list'),
    path('<slug:slug>/', api_views.ProductDetailView.as_view(), name='api_product_detail'),
]