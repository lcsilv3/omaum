from django.urls import path
from . import views

urlpatterns = [
    # URLs para Curso
    path('cursos/', views.CursoListView.as_view(), name='curso_list'),
    path('cursos/novo/', views.CursoCreateView.as_view(), name='curso_create'),
    path('cursos/<str:pk>/editar/', views.CursoUpdateView.as_view(), name='curso_update'),
    path('cursos/<str:pk>/deletar/', views.CursoDeleteView.as_view(), name='curso_delete'),

    # URLs para Turma
    path('', views.TurmaListView.as_view(), name='turma_list'),
    path('nova/', views.TurmaCreateView.as_view(), name='turma_create'),
    path('<int:pk>/editar/', views.TurmaUpdateView.as_view(), name='turma_update'),
    path('<int:pk>/deletar/', views.TurmaDeleteView.as_view(), name='turma_delete'),
]