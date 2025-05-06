from django.urls import path
from .views.frequencia_mensal import (
    listar_frequencias,
    criar_frequencia_mensal,
    editar_frequencia_mensal,
    excluir_frequencia_mensal,
    detalhar_frequencia_mensal,
    recalcular_carencias
)
from .views.carencia import (
    editar_carencia,
    resolver_carencia,
    detalhar_carencia,
    iniciar_acompanhamento
)
from .views.notificacao import (
    listar_notificacoes_carencia,
    criar_notificacao,
    detalhar_notificacao,
    editar_notificacao,
    enviar_notificacao,
    reenviar_notificacao,
    responder_aluno
)
from .views.relatorio import (
    relatorio_frequencias,
    exportar_frequencia_csv,
    historico_frequencia,
    exportar_historico
)
from .views.dashboard import (
    dashboard,
    painel_frequencias,
    visualizar_painel_frequencias
)
from .views import api_views

app_name = 'frequencias'

urlpatterns = [
    # Views principais
    path('', listar_frequencias, name='listar_frequencias'),
    path('criar/', criar_frequencia_mensal, name='criar_frequencia_mensal'),
    path('editar/<int:frequencia_id>/', editar_frequencia_mensal, name='editar_frequencia_mensal'),
    path('excluir/<int:frequencia_id>/', excluir_frequencia_mensal, name='excluir_frequencia_mensal'),
    path('detalhar/<int:frequencia_id>/', detalhar_frequencia_mensal, name='detalhar_frequencia_mensal'),
    path('recalcular/<int:frequencia_id>/', recalcular_carencias, name='recalcular_carencias'),
    
    # Carências
    path('carencias/editar/<int:carencia_id>/', editar_carencia, name='editar_carencia'),
    path('carencias/resolver/<int:carencia_id>/', resolver_carencia, name='resolver_carencia'),
    path('carencias/detalhar/<int:carencia_id>/', detalhar_carencia, name='detalhar_carencia'),
    path('carencias/iniciar-acompanhamento/<int:carencia_id>/', iniciar_acompanhamento, name='iniciar_acompanhamento'),
    
    # Notificações
    path('notificacoes/', listar_notificacoes_carencia, name='listar_notificacoes_carencia'),
    path('notificacoes/criar/<int:carencia_id>/', criar_notificacao, name='criar_notificacao'),
    path('notificacoes/detalhar/<int:notificacao_id>/', detalhar_notificacao, name='detalhar_notificacao'),
    path('notificacoes/editar/<int:notificacao_id>/', editar_notificacao, name='editar_notificacao'),
    path('notificacoes/enviar/<int:notificacao_id>/', enviar_notificacao, name='enviar_notificacao'),
    path('notificacoes/reenviar/<int:notificacao_id>/', reenviar_notificacao, name='reenviar_notificacao'),
    path('notificacoes/responder/<int:notificacao_id>/', responder_aluno, name='responder_aluno'),
    
    # Exportação e relatórios
    path('exportar/<int:frequencia_id>/', exportar_frequencia_csv, name='exportar_frequencia_csv'),
    path('painel/', painel_frequencias, name='painel_frequencias'),
    path('painel/visualizar/<int:turma_id>/<int:mes_inicio>/<int:ano_inicio>/<int:mes_fim>/<int:ano_fim>/', 
         visualizar_painel_frequencias, name='visualizar_painel_frequencias'),
    path('relatorio/', relatorio_frequencias, name='relatorio_frequencias'),
    path('historico/<str:aluno_cpf>/', historico_frequencia, name='historico_frequencia'),
    path('historico/<str:aluno_cpf>/exportar/', exportar_historico, name='exportar_historico'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    
    # APIs
    path('api/dados-frequencia/<int:frequencia_id>/', api_views.obter_dados_frequencia, name='api_obter_dados_frequencia'),
    path('api/dados-painel-frequencias/', api_views.obter_dados_painel_frequencias, name='api_obter_dados_painel_frequencias'),
]
