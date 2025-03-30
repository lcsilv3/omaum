from django.urls import path
from . import views

app_name = 'presencas'

urlpatterns = [
    path('lista/', views.listar_presencas, name='listar_presencas'),
    path('registrar/', views.registrar_presenca, name='registrar_presenca'),
    path('editar/<int:pk>/', views.editar_presenca, name='editar_presenca'),
    path('excluir/<int:pk>/', views.excluir_presenca, name='excluir_presenca'),
    path('relatorio/', views.relatorio_presencas, name='relatorio_presencas'),
]
