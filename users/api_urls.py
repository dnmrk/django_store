from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api_views

urlpatterns = [
    path('register/', api_views.RegisterView.as_view(), name='api_register'),
    path('login/', TokenObtainPairView.as_view(), name='api_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('profile/', api_views.ProfileView.as_view(), name='api_profile'),
]