from django.urls import path
from . import views

app_name = 'presencas'

urlpatterns = [
    path('lista/', views.listar_presencas, name='listar_presencas'),  # Alterado para usar a função existente
    path('registrar/', views.registrar_presenca, name='registrar_presenca'),
    path('editar/<int:id>/', views.editar_presenca, name='editar_presenca'),
    path('excluir/<int:id>/', views.excluir_presenca, name='excluir_presenca'),
    path('relatorio/', views.relatorio_presencas, name='relatorio_presencas'),
]
