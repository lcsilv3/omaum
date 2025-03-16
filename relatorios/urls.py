from django.urls import path
from . import views

urlpatterns = [
    path('alunos/', views.relatorio_alunos, name='relatorio_alunos'),
    # Outras URLs...
]

