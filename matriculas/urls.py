"""URLs do aplicativo Matriculas."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatriculaViewSet
from . import views_tradicionais

app_name = "matriculas"

router = DefaultRouter()
router.register(r'matriculas', MatriculaViewSet, basename='matricula')

urlpatterns = [
    # URLs tradicionais seguindo o padrão do contrato
    path('', views_tradicionais.listar_matriculas, name='listar_matriculas'),
    path('criar/', views_tradicionais.criar_matricula, name='criar_matricula'),
    path('<int:matricula_id>/', views_tradicionais.detalhar_matricula,
         name='detalhar_matricula'),
    path('<int:matricula_id>/editar/', views_tradicionais.editar_matricula,
         name='editar_matricula'),
    path('<int:matricula_id>/excluir/', views_tradicionais.excluir_matricula,
         name='excluir_matricula'),
    
    # Views AJAX
    path('ajax/turmas-por-curso/', views_tradicionais.turmas_por_curso,
         name='turmas_por_curso'),
    path('ajax/alunos-disponiveis/', views_tradicionais.alunos_disponiveis,
         name='alunos_disponiveis'),
    
    # API REST
    path('api/', include(router.urls)),
]
