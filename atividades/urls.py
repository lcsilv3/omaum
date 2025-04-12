from django.urls import path
from . import views

app_name = 'atividades'  # Definindo o namespace

urlpatterns = [
    path('', views.index, name='listar'),  # Página de índice/agregador
    # Atividades Acadêmicas
    path('academicas/', views.listar_atividades_academicas, name='listar_atividades_academicas'),
    path('academicas/criar/', views.criar_atividade_academica, name='criar_atividade_academica'),
    path('academicas/editar/<int:pk>/', views.editar_atividade_academica, name='editar_atividade_academica'),
    path('academicas/excluir/<int:pk>/', views.excluir_atividade_academica, name='excluir_atividade_academica'),
    path('academicas/detalhar/<int:pk>/', views.detalhar_atividade_academica, name='detalhar_atividade_academica'),
    path('academicas/confirmar-exclusao/<int:pk>/', views.confirmar_exclusao_academica, name='confirmar_exclusao_academica'),
    
    # Atividades Ritualísticas
    path('ritualisticas/', views.listar_atividades_ritualisticas, name='listar_atividades_ritualisticas'),
    path('ritualisticas/criar/', views.criar_atividade_ritualistica, name='criar_atividade_ritualistica'),
    path('ritualisticas/editar/<int:pk>/', views.editar_atividade_ritualistica, name='editar_atividade_ritualistica'),
    path('ritualisticas/excluir/<int:pk>/', views.excluir_atividade_ritualistica, name='excluir_atividade_ritualistica'),
    path('ritualisticas/detalhar/<int:pk>/', views.detalhar_atividade_ritualistica, name='detalhar_atividade_ritualistica'),
    path('ritualisticas/confirmar-exclusao/<int:pk>/', views.confirmar_exclusao_ritualistica, name='confirmar_exclusao_ritualistica'),
]
