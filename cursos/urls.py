from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.listar_cursos, name='listar_cursos'),
    path('novo/', views.criar_curso, name='criar_curso'),
    path('<int:id>/detalhes/', views.detalhar_curso, name='detalhar_curso'),
    path('<int:id>/editar/', views.editar_curso, name='editar_curso'),
    path('<int:id>/excluir/', views.excluir_curso, name='excluir_curso'),
]
