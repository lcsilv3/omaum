from django.urls import path
from .views.pagamento_views import (
    listar_pagamentos, criar_pagamento, editar_pagamento, excluir_pagamento,
    detalhar_pagamento, pagamentos_aluno, registrar_pagamento_rapido,
    importar_pagamentos_csv, exportar_pagamentos_csv, exportar_pagamentos_excel,
    exportar_pagamentos_pdf, turmas_por_curso, buscar_alunos
)
from .views.relatorio_views import (
    relatorio_financeiro, pagamentos_por_turma,
    dados_grafico_pagamentos, dados_distribuicao_pagamentos
)
from .views.dashboard_views import dashboard, dashboard_pagamentos, dashboard_financeiro

app_name = 'pagamentos'

urlpatterns = [
    # Pagamentos
    path('', listar_pagamentos, name='listar_pagamentos'),
    path('novo/', criar_pagamento, name='criar_pagamento'),
    path('<int:pagamento_id>/editar/', editar_pagamento, name='editar_pagamento'),
    path('<int:pagamento_id>/excluir/', excluir_pagamento, name='excluir_pagamento'),
    path('<int:pagamento_id>/', detalhar_pagamento, name='detalhar_pagamento'),

    # Pagamentos por aluno e pagamento rápido
    path('aluno/<str:cpf>/', pagamentos_aluno, name='pagamentos_aluno'),
    path('aluno/<str:cpf>/registrar-rapido/', registrar_pagamento_rapido, name='registrar_pagamento_rapido'),

    # Importação e exportação
    path('importar/', importar_pagamentos_csv, name='importar_pagamentos_csv'),
    path('exportar/csv/', exportar_pagamentos_csv, name='exportar_pagamentos_csv'),
    path('exportar/excel/', exportar_pagamentos_excel, name='exportar_pagamentos_excel'),
    path('exportar/pdf/', exportar_pagamentos_pdf, name='exportar_pagamentos_pdf'),

    # Relatórios
    path('relatorio/', relatorio_financeiro, name='relatorio_financeiro'),
    path('relatorio/turma/', pagamentos_por_turma, name='relatorio_pagamentos_turma'),

    # Dashboards
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/pagamentos/', dashboard_pagamentos, name='dashboard_pagamentos'),
    path('dashboard/financeiro/', dashboard_financeiro, name='dashboard_financeiro'),

    # APIs para gráficos
    path('pagamentos/grafico-pagamentos/', dados_grafico_pagamentos, name='dados_grafico_pagamentos'),
    path('pagamentos/distribuicao-pagamentos/', dados_distribuicao_pagamentos, name='dados_distribuicao_pagamentos'),

    # Turmas por curso
    path('turmas-por-curso/', turmas_por_curso, name='turmas_por_curso'),

    # Buscar alunos (API)
    path('alunos/buscar/', buscar_alunos, name='buscar_alunos'),
]