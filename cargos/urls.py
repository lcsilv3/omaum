from django.urls import path
from . import views

app_name = 'cargos'

urlpatterns = [
    path('', views.listar_cargos, name='listar_cargos'),
    path('novo/', views.criar_cargo, name='criar_cargo'),
    path('<int:id>/editar/', views.editar_cargo, name='editar_cargo'),
    path('<int:id>/excluir/', views.excluir_cargo, name='excluir_cargo'),
    path('<int:id>/detalhes/', views.detalhes_cargo, name='detalhes_cargo'),
]