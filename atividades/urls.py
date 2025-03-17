from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    path('academicas/', views.AtividadeAcademicaListView.as_view(), name='atividade_academica_list'),
    path('ritualisticas/', views.AtividadeRitualisticaListView.as_view(), name='atividade_ritualistica_list'),
    path('academicas/criar/', views.atividade_academica_create, name='atividade_academica_create'),
    path('ritualisticas/criar/', views.atividade_ritualistica_create, name='atividade_ritualistica_create'),
    # Adicione outras URLs conforme necessário
]