from django.urls import path
from . import views

app_name = "relatorios"

urlpatterns = [
    path("", views.listar_relatorios, name="listar_relatorios"),
    path("<int:relatorio_id>/", views.detalhar_relatorio, name="detalhar_relatorio"),
    path("criar/", views.criar_relatorio, name="criar_relatorio"),
    path("<int:relatorio_id>/editar/", views.editar_relatorio, name="editar_relatorio"),
    path("<int:relatorio_id>/excluir/", views.excluir_relatorio, name="excluir_relatorio"),
    path("alunos/", views.relatorio_alunos, name="relatorio_alunos"),
    path("alunos/pdf/", views.relatorio_alunos_pdf, name="relatorio_alunos_pdf"),
    path("presencas/", views.relatorio_presencas, name="relatorio_presencas"),
    path("presencas/pdf/", views.relatorio_presencas_pdf, name="relatorio_presencas_pdf"),
    path("punicoes/", views.relatorio_punicoes, name="relatorio_punicoes"),
    path("punicoes/pdf/", views.relatorio_punicoes_pdf, name="relatorio_punicoes_pdf"),
]