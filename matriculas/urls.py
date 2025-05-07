from django.urls import path
from . import views

app_name = "matriculas"

urlpatterns = [
    path("", views.listar_matriculas, name="listar_matriculas"),
    path("<int:id>/detalhes/", views.detalhar_matricula, name="detalhar_matricula"),
    path("realizar/", views.realizar_matricula, name="realizar_matricula"),
    path("<int:id>/cancelar/", views.cancelar_matricula, name="cancelar_matricula"),
    # Nova URL para cancelar matrícula a partir da turma
    path("turma/<int:turma_id>/aluno/<str:aluno_cpf>/cancelar/", 
         views.cancelar_matricula_por_turma_aluno, 
         name="cancelar_matricula_por_turma_aluno"),
    path("exportar/", views.exportar_matriculas, name="exportar_matriculas"),
    path("importar/", views.importar_matriculas, name="importar_matriculas"),
]
