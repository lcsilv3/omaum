from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import RelatorioViewSet

app_name = "relatorios"

# API Router
router = DefaultRouter()
router.register(r"api/relatorios", RelatorioViewSet)

urlpatterns = [
    # API URLs
    path("", include(router.urls)),
    # Template URLs
    path("", views.listar_relatorios, name="listar_relatorios"),
    path("<int:relatorio_id>/", views.detalhar_relatorio, name="detalhar_relatorio"),
    path("criar/", views.criar_relatorio, name="criar_relatorio"),
    path("<int:relatorio_id>/editar/", views.editar_relatorio, name="editar_relatorio"),
    path(
        "<int:relatorio_id>/excluir/", views.excluir_relatorio, name="excluir_relatorio"
    ),
    path("alunos/", views.relatorio_alunos, name="relatorio_alunos"),
    path("alunos/pdf/", views.relatorio_alunos_pdf, name="relatorio_alunos_pdf"),
    path("presencas/", views.relatorio_presencas, name="relatorio_presencas"),
    path(
        "presencas/pdf/", views.relatorio_presencas_pdf, name="relatorio_presencas_pdf"
    ),
    path("historico/", views.relatorio_historico, name="relatorio_historico"),
    path(
        "historico/pdf/",
        views.relatorio_historico_pdf,
        name="relatorio_historico_pdf",
    ),
    # Relatórios de Turmas
    path("turmas/", views.relatorio_turmas, name="relatorio_turmas"),
    path(
        "turmas/pdf/",
        views.relatorio_turmas_pdf,
        name="relatorio_turmas_pdf",
    ),
    # Relatórios de Atividades
    path(
        "atividades/",
        views.relatorio_atividades,
        name="relatorio_atividades",
    ),
    path(
        "atividades/pdf/",
        views.relatorio_atividades_pdf,
        name="relatorio_atividades_pdf",
    ),
]
