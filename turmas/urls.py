from django.urls import path
from . import views

app_name = 'turmas'

urlpatterns = [
    path('cursos/', views.CursoListView.as_view(), name='curso_list'),
    path('cursos/create/', views.CursoCreateView.as_view(), name='curso_create'),
    path('cursos/<int:pk>/update/', views.CursoUpdateView.as_view(), name='curso_update'),
    path('cursos/<int:pk>/delete/', views.CursoDeleteView.as_view(), name='curso_delete'),
    path('', views.TurmaListView.as_view(), name='turma_list'),
    path('create/', views.TurmaCreateView.as_view(), name='turma_create'),
    path('<int:pk>/update/', views.TurmaUpdateView.as_view(), name='turma_update'),
    path('<int:pk>/delete/', views.TurmaDeleteView.as_view(), name='turma_delete'),
]