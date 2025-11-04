# Definição dos relatórios do app relatorios_presenca
RELATORIOS = [
    {
        "nome": "Boletim de Frequência do Aluno",
        "descricao": "Boletim de frequência detalhado",
        "url": "relatorios_presenca:boletim_frequencia_aluno",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "relatorios_presenca:boletim_frequencia_aluno",
                "query": {"formato": "csv"},
            },
            {
                "label": "PDF",
                "url_name": "relatorios_presenca:boletim_frequencia_aluno",
                "query": {"formato": "pdf"},
            },
        ],
    },
    {
        "nome": "Frequência por Atividade",
        "descricao": "Resumo de presença por atividade e período.",
        "url": "relatorios_presenca:frequencia_por_atividade",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "relatorios_presenca:frequencia_por_atividade",
                "query": {"formato": "csv"},
            },
            {
                "label": "PDF",
                "url_name": "relatorios_presenca:frequencia_por_atividade",
                "query": {"formato": "pdf"},
            },
        ],
    },
    {
        "nome": "Alunos com Carência",
        "descricao": "Alunos com maior número de carências no período.",
        "url": "relatorios_presenca:alunos_com_carencia",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "relatorios_presenca:alunos_com_carencia",
                "query": {"formato": "csv"},
            },
            {
                "label": "PDF",
                "url_name": "relatorios_presenca:alunos_com_carencia",
                "query": {"formato": "pdf"},
            },
        ],
    },
    {
        "nome": "Relatório de Faltas",
        "descricao": "Alunos com maior número de faltas por turma.",
        "url": "relatorios_presenca:relatorio_faltas",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "relatorios_presenca:relatorio_faltas",
                "query": {"formato": "csv"},
            },
            {
                "label": "PDF",
                "url_name": "relatorios_presenca:relatorio_faltas",
                "query": {"formato": "pdf"},
            },
        ],
    },
    {
        "nome": "Relatório Consolidado de Presença",
        "descricao": "Resumo por curso, turma e período com exportações.",
        "url": "relatorios_presenca:relatorio_form",
        "exportacoes": [],
    },
]
