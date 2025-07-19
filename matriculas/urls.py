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
    path('realizar/', views_tradicionais.criar_matricula, name='realizar_matricula'),
    path('<int:matricula_id>/', views_tradicionais.detalhar_matricula,
         name='detalhar_matricula'),
    path('<int:matricula_id>/editar/', views_tradicionais.editar_matricula,
         name='editar_matricula'),
    path('<int:matricula_id>/excluir/', views_tradicionais.excluir_matricula,
         name='excluir_matricula'),
    
    # Views AJAX
    path('ajax/buscar-turmas/', views_tradicionais.buscar_turmas,
         name='buscar_turmas'),
    path('ajax/buscar-alunos/', views_tradicionais.buscar_alunos,
         name='buscar_alunos'),
         
    # Views de exportação/importação (placeholders)
    path('exportar/', views_tradicionais.exportar_matriculas, name='exportar_matriculas'),
    path('importar/', views_tradicionais.importar_matriculas, name='importar_matriculas'),
    
    # API REST
    path('api/', include(router.urls)),
]
