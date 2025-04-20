from django.urls import path
from . import views

app_name = "relatorios"

urlpatterns = [
    path(
        "", views.listar_relatorios, name="listar_relatorios"
    ),  # Alterado de 'index' para 'listar_relatorios'
    path("alunos/", views.relatorio_alunos, name="relatorio_alunos"),
    path(
        "alunos/pdf/", views.relatorio_alunos_pdf, name="relatorio_alunos_pdf"
    ),
    path("presencas/", views.relatorio_presencas, name="relatorio_presencas"),
    path("punicoes/", views.relatorio_punicoes, name="relatorio_punicoes"),
]
