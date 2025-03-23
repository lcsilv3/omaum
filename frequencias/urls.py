from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_frequencias, name='listar_frequencias'),
    path('registrar/', views.registrar_frequencia, name='registrar_frequencia'),
    path('registrar/turma/<int:turma_id>/', views.registrar_frequencia_turma, name='registrar_frequencia_turma'),
    path('estatisticas/', views.estatisticas_frequencia, name='estatisticas_frequencia'),
    path('<int:id>/', views.detalhe_frequencia, name='detalhe_frequencia'),
    path('<int:id>/editar/', views.editar_frequencia, name='editar_frequencia'),
    path('<int:id>/excluir/', views.excluir_frequencia, name='excluir_frequencia'),
    path('bulk-actions/', views.bulk_actions, name='frequencia_bulk_actions'),
]
