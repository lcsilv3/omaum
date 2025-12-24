"""
URL routing principal para o aplicativo presencas.

Estrutura modular para melhor manutenibilidade:
- urls_listagem.py: Endpoints de listagem
- urls_registro.py: Fluxo wizard de registro
- urls_edicao.py: Edição lote e individual
- urls_detalhar.py: Visualização detalhada
- urls_operacoes.py: CRUD e operações auxiliares
- urls_reports.py: Relatórios
- api/urls.py: API REST
"""

from django.urls import path, include

app_name = "presencas"

urlpatterns = [
    # Listagem de presenças
    path("", include("presencas.urls_listagem")),
    
    # Fluxo wizard de registro
    path("registrar/", include("presencas.urls_registro")),
    
    # Edição (lote e individual)
    path("editar/", include("presencas.urls_edicao")),
    
    # Detalhamento/visualização
    path("detalhar/", include("presencas.urls_detalhar")),
    
    # Operações CRUD e auxiliares
    path("", include("presencas.urls_operacoes")),
    
    # Estatísticas e dashboards
    path("", include("presencas.urls_estatisticas")),
    
    # API REST
    path("api/", include("presencas.api.urls")),
    
    # Relatórios
    path("relatorios/", include("presencas.urls_reports")),
]
