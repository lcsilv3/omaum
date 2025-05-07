from django.urls import path
from . import views

app_name = "presencas"

urlpatterns = [
   path("", views.listar_presencas, name="listar_presencas"),
   path("registrar-em-massa/", views.registrar_presenca_em_massa, name="registrar_presenca_em_massa"),
   path("registrar/", views.registrar_presenca, name="registrar_presenca"),
   path("editar/<int:presenca_id>/", views.editar_presenca, name="editar_presenca"),
   path("excluir/<int:presenca_id>/", views.excluir_presenca, name="excluir_presenca"),
   path("detalhar/<int:presenca_id>/", views.detalhar_presenca, name="detalhar_presenca"),
   path("turma/<int:turma_id>/registrar/", views.registrar_presenca_turma, name="registrar_presenca_turma"),
   path("exportar/csv/", views.exportar_presencas, name="exportar_presencas_csv"),
   path("relatorio/", views.relatorio_presencas, name="relatorio_presencas"),
   path("api/atividades-por-turma/<int:turma_id>/", views.api_atividades_por_turma, name="api_atividades_por_turma"),
   path("api/alunos-por-turma/<int:turma_id>/", views.api_alunos_por_turma, name="api_alunos_por_turma"),
   path("exportar/", views.exportar_presencas, name="exportar_presencas"),
   path("importar/", views.importar_presencas, name="importar_presencas"),
]
