from rest_framework.routers import DefaultRouter
from .views import AutoreViewSet, LibroViewSet, ScarpeViewSet
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register(r"libri", LibroViewSet, basename="libro")
router.register(r"autori", AutoreViewSet, basename="autore")
router.register(r"scarpe", ScarpeViewSet, basename='scarpe')

urlpatterns = [
    path("", include(router.urls)),
]
