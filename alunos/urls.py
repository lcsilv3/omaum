from django.urls import path
from . import views
from .views import api_views

app_name = "alunos"

urlpatterns = [
    path("", views.listar_alunos, name="listar_alunos"),
    path("criar/", views.criar_aluno, name="criar_aluno"),
    path("<str:cpf>/detalhes/", views.detalhar_aluno, name="detalhar_aluno"),
    path("<str:cpf>/editar/", views.editar_aluno, name="editar_aluno"),
    path("<str:cpf>/excluir/", views.excluir_aluno, name="excluir_aluno"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("exportar/", views.exportar_alunos, name="exportar_alunos"),
    path("importar/", views.importar_alunos, name="importar_alunos"),
    path("relatorio/", views.relatorio_alunos, name="relatorio_alunos"),
    path("search/", views.search_alunos, name="search_alunos"),
    path(
        "<str:cpf>/confirmar-remocao-instrutoria/<str:nova_situacao>/",
        views.confirmar_remocao_instrutoria,
        name="confirmar_remocao_instrutoria",
    ),
    path(
        "api/search-instrutores/",
        views.search_instrutores,
        name="search_instrutores",
    ),
    path("api/get-aluno/<str:cpf>/", views.get_aluno, name="get_aluno"),
    path(
        "api/detalhes/<str:cpf>/",
        views.get_aluno_detalhes,
        name="get_aluno_detalhes"
    ),
    path(
        "api/verificar-elegibilidade/<str:cpf>/",
        api_views.verificar_elegibilidade_endpoint,
        name="verificar_elegibilidade_instrutor",
    ),
    path(
        "diagnostico-instrutores/",
        views.diagnostico_instrutores,
        name="diagnostico_instrutores",
    ),
]