# Definição dos relatórios do app Frequências
RELATORIOS = [
    {
        "nome": "Painel de Frequências",
        "descricao": "Indicadores executivos e visão geral das frequências.",
        "url": "frequencias:dashboard",
        "exportacoes": [],
    },
    {
        "nome": "Relatório de Frequências Mensais",
        "descricao": "Indicadores completos por turma, mês e ano.",
        "url": "frequencias:relatorio_frequencias",
        "exportacoes": [],
    },
    {
        "nome": "Frequência por Turma",
        "descricao": "Listagem operacional e acompanhamento mensal por turma.",
        "url": "frequencias:listar_frequencias",
        "exportacoes": ["csv"],
    },
    {
        "nome": "Painel Operacional",
        "descricao": "Visualização consolidada por período para equipes acadêmicas.",
        "url": "frequencias:painel_frequencias",
        "exportacoes": [],
    },
    {
        "nome": "Exportação Consolidada",
        "descricao": "Exporte frequências em lote para tratamento externo.",
        "url": "frequencias:exportar_frequencias",
        "exportacoes": ["csv"],
    },
    {
        "nome": "Importação de Frequências",
        "descricao": "Importe registros de frequência a partir de planilhas CSV.",
        "url": "frequencias:importar_frequencias",
        "exportacoes": ["csv"],
    },
]
