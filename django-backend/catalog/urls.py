from rest_framework.routers import DefaultRouter
from .views import AutoreViewSet, LibroViewSet
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register("libri", LibroViewSet, basename="libro")
router.register("autori", AutoreViewSet, basename="autore")

urlpatterns = [
    path("", include(router.urls)),
]
