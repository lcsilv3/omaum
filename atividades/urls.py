from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    # URLs for Academic Activities
    path('academicas/', views.listar_atividades_academicas, name='academica_lista'),
    path('academicas/criar/', views.criar_atividade_academica, name='academica_criar'),
    path('academicas/<int:pk>/editar/', views.editar_atividade_academica, name='academica_editar'),
    path('academicas/<int:pk>/excluir/', views.excluir_atividade_academica, name='academica_excluir'),
    
    # URLs for Ritualistic Activities
    path('ritualisticas/', views.listar_atividades_ritualisticas, name='ritualistica_lista'),
    path('ritualisticas/criar/', views.criar_atividade_ritualistica, name='ritualistica_criar'),
    path('ritualisticas/<int:pk>/editar/', views.editar_atividade_ritualistica, name='ritualistica_editar'),
    path('ritualisticas/<int:pk>/excluir/', views.excluir_atividade_ritualistica, name='ritualistica_excluir'),
]