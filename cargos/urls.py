from django.urls import path
from . import views

app_name = 'cargos'

urlpatterns = [
    path('', views.listar_cargos_administrativos, name='listar_cargos_administrativos'),
    path('novo/', views.criar_cargo, name='criar_cargo'),
    path('<str:codigo_cargo>/', views.detalhe_cargo, name='detalhe_cargo'),
    path('<str:codigo_cargo>/editar/', views.editar_cargo, name='editar_cargo'),
    path('<str:codigo_cargo>/excluir/', views.excluir_cargo, name='excluir_cargo'),
]