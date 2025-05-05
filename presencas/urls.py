from django.urls import path
from . import views
from . import api_views

app_name = 'presencas'

urlpatterns = [
   # Views principais
   path('', views.listar_presencas, name='listar_presencas'),
   path('registrar/', views.registrar_presenca, name='registrar_presenca'),
   path('editar/<int:presenca_id>/', views.editar_presenca, name='editar_presenca'),
   path('excluir/<int:presenca_id>/', views.excluir_presenca, name='excluir_presenca'),
   path('multiplas/', views.registrar_presencas_multiplas, name='registrar_presencas_multiplas'),
   path('multiplas/selecionar/<str:data>/<str:turmas>/<str:atividades>/', 
        views.selecionar_alunos_presencas, name='selecionar_alunos_presencas'),
   path('exportar/', views.exportar_presencas_csv, name='exportar_presencas_csv'),
   path('relatorio/', views.relatorio_presencas, name='relatorio_presencas'),
    
   # APIs
   path('api/obter-alunos-por-turmas/', api_views.obter_alunos_por_turmas, name='api_obter_alunos_por_turmas'),
   path('api/obter-atividades-por-data/', api_views.obter_atividades_por_data, name='api_obter_atividades_por_data'),
   path('api/salvar-presencas-multiplas/', api_views.salvar_presencas_multiplas, name='api_salvar_presencas_multiplas'),
   path('api/atividades-por-turma/<int:turma_id>/', views.api_atividades_por_turma, name='api_atividades_por_turma'),
   path('filtrar/', views.filtrar_presencas, name='filtrar_presencas'),
]
