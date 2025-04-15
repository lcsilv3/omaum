from django.urls import path
from . import views

app_name = "relatorios"  # This line is crucial

urlpatterns = [
    path("", views.index, name="index"),
    path("alunos/", views.relatorio_alunos, name="relatorio_alunos"),
    path(
        "alunos/pdf/", views.relatorio_alunos_pdf, name="relatorio_alunos_pdf"
    ),
    path("presencas/", views.relatorio_presencas, name="relatorio_presencas"),
    path(
        "presencas/pdf/",
        views.relatorio_presencas_pdf,
        name="relatorio_presencas_pdf",
    ),
    path("punicoes/", views.relatorio_punicoes, name="relatorio_punicoes"),
    path(
        "punicoes/pdf/",
        views.relatorio_punicoes_pdf,
        name="relatorio_punicoes_pdf",
    ),
]
