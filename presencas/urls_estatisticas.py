"""
URLs para as views de estatísticas de presença.
"""

from django.urls import path
from . import views_estatisticas

app_name = 'presencas_estatisticas'

urlpatterns = [
    # Dashboard
    path('dashboard/', views_estatisticas.dashboard_presencas, name='dashboard'),
    
    # Consolidado por aluno
    path('consolidado/aluno/<int:aluno_id>/', 
         views_estatisticas.consolidado_aluno, 
         name='consolidado_aluno'),
    
    # Tabela consolidada
    path('consolidado/tabela/', 
         views_estatisticas.tabela_consolidada, 
         name='tabela_consolidada'),
    
    # Estatísticas da turma
    path('estatisticas/turma/<int:turma_id>/', 
         views_estatisticas.estatisticas_turma, 
         name='estatisticas_turma'),
    
    # Recalcular carências
    path('recalcular-carencias/', 
         views_estatisticas.recalcular_carencias, 
         name='recalcular_carencias'),
    
    # Exportar consolidado
    path('exportar/consolidado/', 
         views_estatisticas.exportar_consolidado, 
         name='exportar_consolidado'),
]
