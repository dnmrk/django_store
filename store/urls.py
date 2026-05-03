"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .admin import StorAdminSite

# Override the default admin site
admin.site.__class__ = StorAdminSite 

@staff_member_required
def analytics_dashboard(request):
    return render(request, 'admin/analytics_dashboard.html')

urlpatterns = [
    path('admin/dashboard/', analytics_dashboard, name='analytics_dashboard'),
    path('admin/', admin.site.urls),
    path('api/products/', include('products.api_urls')),
    path('api/cart/', include('cart.api_urls')),
    path('api/orders/', include('orders.api_urls')),
    path('api/auth/', include('users.api_urls')),
    path('api/forecast/', include('forecasting.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('users/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('products.urls', namespace='products')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
