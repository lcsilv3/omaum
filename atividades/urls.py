from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    path('academicas/', views.atividade_academica_list, name='atividade_academica_list'),
    path('ritualisticas/', views.listar_atividades_ritualisticas, name='atividade_ritualistica_list'),
    
    # URLs para atividades acadêmicas
    path('academicas/criar/', views.criar_atividade_academica, name='academica_criar'),
    path('academicas/editar/<int:pk>/', views.editar_atividade_academica, name='academica_editar'),
    path('academicas/excluir/<int:pk>/', views.excluir_atividade_academica, name='academica_excluir'),
    path('academicas/lista/', views.atividade_academica_list, name='academica_lista'),
    
    # URLs para atividades ritualísticas
    path('ritualisticas/criar/', views.criar_atividade_ritualistica, name='ritualistica_criar'),
    path('ritualisticas/editar/<int:pk>/', views.editar_atividade_ritualistica, name='ritualistica_editar'),
    path('ritualisticas/excluir/<int:pk>/', views.excluir_atividade_ritualistica, name='ritualistica_excluir'),
    path('ritualisticas/lista/', views.listar_atividades_ritualisticas, name='ritualistica_lista'),
]