"""URLs do aplicativo Matriculas."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatriculaViewSet

app_name = "matriculas"

router = DefaultRouter()
router.register(r'matriculas', MatriculaViewSet, basename='matricula')

urlpatterns = [
    path('', include(router.urls)),
]
