from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    profilo,
    CustomTokenObtainPairView,
    ProtectedView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path("profilo/", profilo, name="profilo"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
