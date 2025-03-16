from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    # URLs for AtividadeAcademica
    path('academicas/', views.AtividadeAcademicaListView.as_view(), name='atividade_academica_list'),
    path('academicas/criar/', views.AtividadeAcademicaCreateView.as_view(), name='atividade_academica_create'),   
    path('academicas/<int:pk>/', views.AtividadeAcademicaDetailView.as_view(), name='atividade_academica_detail'),
    path('academicas/<int:pk>/editar/', views.AtividadeAcademicaUpdateView.as_view(), name='atividade_academica_update'),
    path('academicas/<int:pk>/excluir/', views.AtividadeAcademicaDeleteView.as_view(), name='atividade_academica_delete'),

    # URLs for AtividadeRitualistica
    path('ritualisticas/', views.AtividadeRitualisticaListView.as_view(), name='atividade_ritualistica_list'),    
    path('ritualisticas/criar/', views.AtividadeRitualisticaCreateView.as_view(), name='atividade_ritualistica_create'),
    path('ritualisticas/<int:pk>/', views.AtividadeRitualisticaDetailView.as_view(), name='atividade_ritualistica_detail'),
    path('ritualisticas/<int:pk>/editar/', views.AtividadeRitualisticaUpdateView.as_view(), name='atividade_ritualistica_update'),
    path('ritualisticas/<int:pk>/excluir/', views.AtividadeRitualisticaDeleteView.as_view(), name='atividade_ritualistica_delete'),

    path('cadastrar-turma/', views.cadastrar_turma_view, name='cadastrar_turma'),
]
