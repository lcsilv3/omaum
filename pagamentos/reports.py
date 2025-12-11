# Definição dos relatórios do app Pagamentos
RELATORIOS = [
    {
        "nome": "Painel Geral de Pagamentos",
        "descricao": "Indicadores consolidados por período e status dos recebimentos.",
        "url": "pagamentos:painel_geral",
        "exportacoes": [],
    },
    {
        "nome": "Painel Mensal",
        "descricao": "Evolução mês a mês dos pagamentos.",
        "url": "pagamentos:painel_mensal",
        "exportacoes": [],
    },
    {
        "nome": "Painel Financeiro",
        "descricao": "Visão financeira com comparativos e distribuição.",
        "url": "pagamentos:painel_financeiro",
        "exportacoes": [],
    },
    {
        "nome": "Relatório Financeiro",
        "descricao": "Relatório detalhado filtrável por período, status e aluno.",
        "url": "pagamentos:relatorio_financeiro",
        "exportacoes": ["csv", "excel", "pdf"],
    },
    {
        "nome": "Pagamentos por Turma",
        "descricao": "Distribuição de pagamentos por turma para acompanhamento acadêmico.",
        "url": "pagamentos:relatorio_pagamentos_turma",
        "exportacoes": [],
    },
    {
        "nome": "Listagem de Pagamentos",
        "descricao": "Consulta operacional com filtros e ações rápidas.",
        "url": "pagamentos:listar_pagamentos",
        "exportacoes": ["csv", "excel", "pdf"],
    },
    {
        "nome": "Exportação Consolidada",
        "descricao": "Exporte pagamentos em massa para planilhas e documentos.",
        "url": "pagamentos:exportar_pagamentos_csv",
        "exportacoes": ["csv", "excel", "pdf"],
    },
    {
        "nome": "Importação de Pagamentos",
        "descricao": "Importe registros a partir de planilha CSV.",
        "url": "pagamentos:importar_pagamentos_csv",
        "exportacoes": ["csv"],
    },
]
