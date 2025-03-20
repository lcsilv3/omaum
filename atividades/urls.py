from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    path('academicas/', views.AtividadeAcademicaListView.as_view(), name='atividade_academica_list'),
    # ... other paths ...
]