from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_cargos_administrativos, name='listar_cargos_administrativos'),
    path('<str:codigo_cargo>/', views.detalhe_cargo, name='detalhe_cargo'),
]