# Definição dos relatórios do app Atividades
RELATORIOS = [
    {
        "nome": "Relatório de Atividades",
        "descricao": "Panorama geral das atividades cadastradas.",
        "url": "atividades:relatorio_atividades",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "atividades:exportar_atividades",
                "kwargs": {"formato": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "atividades:exportar_atividades",
                "kwargs": {"formato": "excel"},
            },
            {
                "label": "PDF",
                "url_name": "atividades:exportar_atividades",
                "kwargs": {"formato": "pdf"},
            },
        ],
    },
    {
        "nome": "Participação por Atividade",
        "descricao": "Resumo de participação e presença por atividade.",
        "url": "atividades:relatorio_participacao_atividades",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "atividades:exportar_relatorio_participacao",
                "kwargs": {"formato": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "atividades:exportar_relatorio_participacao",
                "kwargs": {"formato": "excel"},
            },
        ],
    },
    {
        "nome": "Carga de Instrutores",
        "descricao": "Distribuição da carga de trabalho dos instrutores.",
        "url": "atividades:relatorio_carga_instrutores",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "atividades:exportar_relatorio_carga_instrutores",
                "kwargs": {"formato": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "atividades:exportar_relatorio_carga_instrutores",
                "kwargs": {"formato": "excel"},
            },
            {
                "label": "PDF",
                "url_name": "atividades:exportar_relatorio_carga_instrutores",
                "kwargs": {"formato": "pdf"},
            },
        ],
    },
    {
        "nome": "Carências e Frequência",
        "descricao": "Relatório de frequência e carências por turma.",
        "url": "atividades:relatorio_frequencia_turmas",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "atividades:exportar_relatorio_frequencia",
                "kwargs": {"formato": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "atividades:exportar_relatorio_frequencia",
                "kwargs": {"formato": "excel"},
            },
            {
                "label": "PDF",
                "url_name": "atividades:exportar_relatorio_frequencia",
                "kwargs": {"formato": "pdf"},
            },
        ],
    },
    {
        "nome": "Cronograma Curso × Turmas",
        "descricao": "Grade de aulas planejadas por curso e turma.",
        "url": "atividades:relatorio_cronograma_curso_turmas",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "atividades:exportar_relatorio_cronograma",
                "kwargs": {"formato": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "atividades:exportar_relatorio_cronograma",
                "kwargs": {"formato": "excel"},
            },
            {
                "label": "PDF",
                "url_name": "atividades:exportar_relatorio_cronograma",
                "kwargs": {"formato": "pdf"},
            },
        ],
    },
    {
        "nome": "Histórico do Aluno",
        "descricao": "Eventos e atividades concluídas por aluno.",
        "url": "atividades:relatorio_historico_aluno",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "atividades:exportar_relatorio_historico_aluno",
                "kwargs": {"formato": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "atividades:exportar_relatorio_historico_aluno",
                "kwargs": {"formato": "excel"},
            },
            {
                "label": "PDF",
                "url_name": "atividades:exportar_relatorio_historico_aluno",
                "kwargs": {"formato": "pdf"},
            },
        ],
    },
]
