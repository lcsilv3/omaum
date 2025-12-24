# Definição dos relatórios do app Presenças
RELATORIOS = [
    {
        "nome": "Painel de Presenças",
        "descricao": "Indicadores executivos e visão geral das presenças.",
        "url": "presencas:dashboard",
        "exportacoes": [],
    },
    {
        "nome": "Boletim de Frequência do Aluno",
        "descricao": "Frequência mensal detalhada por aluno.",
        "url": "relatorios_presenca:boletim_frequencia_aluno",
        "exportacoes": ["csv", "pdf"],
    },
    {
        "nome": "Relatório Consolidado",
        "descricao": "Consolidação por turma e período com exportações.",
        "url": "relatorios_presenca:relatorio_form",
        "exportacoes": ["csv", "pdf"],
    },
    {
        "nome": "Frequência por Atividade",
        "descricao": "Frequência dos alunos por atividade específica.",
        "url": "relatorios_presenca:frequencia_por_atividade",
        "exportacoes": ["csv", "pdf"],
    },
    {
        "nome": "Relatório de Faltas",
        "descricao": "Alunos com maior número de faltas no período.",
        "url": "relatorios_presenca:relatorio_faltas",
        "exportacoes": ["csv"],
    },
    {
        "nome": "Alunos com Carência",
        "descricao": "Identificação de alunos no limite de carência.",
        "url": "relatorios_presenca:alunos_com_carencia",
        "exportacoes": ["csv"],
    },
]
