from django.urls import path
from . import views

app_name = 'cargos'

urlpatterns = [
    path('', views.listar_cargos, name='listar_cargos'),
    path('criar/', views.criar_cargo, name='criar_cargo'),
    path('<int:id>/editar/', views.editar_cargo, name='editar_cargo'),
    path('<int:id>/excluir/', views.excluir_cargo, name='excluir_cargo'),
    path('<int:id>/detalhes/', views.detalhar_cargo, name='detalhar_cargo'),
    path('atribuir/', views.atribuir_cargo, name='atribuir_cargo'),
    path('remover-atribuicao/<int:id>/', views.remover_atribuicao_cargo, name='remover_atribuicao_cargo'),
]