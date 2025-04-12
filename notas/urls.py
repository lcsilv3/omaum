from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.listar_notas, name='listar_notas'),
]
