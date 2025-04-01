from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    path('academicas/', views.listar_atividades_academicas, name='listar_atividades_academicas'),
    path('academicas/criar/', views.criar_atividade_academica, name='criar_atividade_academica'),
    path('academicas/<int:pk>/', views.detalhar_atividade_academica, name='detalhar_atividade_academica'),
    path('academicas/<int:pk>/editar/', views.editar_atividade_academica, name='editar_atividade_academica'),
    path('academicas/<int:pk>/excluir/', views.excluir_atividade_academica, name='excluir_atividade_academica'),
    
    path('ritualisticas/', views.listar_atividades_ritualisticas, name='listar_atividades_ritualisticas'),
    path('ritualisticas/criar/', views.criar_atividade_ritualistica, name='criar_atividade_ritualistica'),
    path('ritualisticas/<int:pk>/', views.detalhar_atividade_ritualistica, name='detalhar_atividade_ritualistica'),
    path('ritualisticas/<int:pk>/editar/', views.editar_atividade_ritualistica, name='editar_atividade_ritualistica'),
    path('ritualisticas/<int:pk>/excluir/', views.excluir_atividade_ritualistica, name='excluir_atividade_ritualistica'),
]