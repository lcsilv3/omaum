from django.urls import path
from . import views

urlpatterns = [
    path('alunos/', views.relatorio_alunos, name='relatorio_alunos'),
    path('alunos/pdf/', views.relatorio_alunos_pdf, name='relatorio_alunos_pdf'),
]
