# Definição dos relatórios do app Atividades
RELATORIOS = [
    {
        "nome": "Painel de Atividades",
        "descricao": "Dashboard com KPIs e gráficos de acompanhamento.",
        "url": "atividades:dashboard_atividades",
        "exportacoes": [],
    },
    {
        "nome": "Relatório por Curso/Turma",
        "descricao": "Listagem analítica de atividades por curso e turma.",
        "url": "atividades:relatorio_atividades",
        "exportacoes": ["csv", "excel", "pdf"],
    },
    {
        "nome": "Participação por Atividade",
        "descricao": "Indicadores e exportações de participação dos alunos.",
        "url": "atividades:relatorio_participacao_atividades",
        "exportacoes": ["csv", "excel", "pdf"],
    },
    {
        "nome": "Carga de Instrutores",
        "descricao": "Distribuição da carga horária por instrutor.",
        "url": "atividades:relatorio_carga_instrutores",
        "exportacoes": ["csv", "excel", "pdf"],
    },
    {
        "nome": "Carências e Frequência",
        "descricao": "Apuração de carências e frequência por turma/curso.",
        "url": "atividades:relatorio_frequencia_turma",
        "exportacoes": ["csv", "excel"],
    },
    {
        "nome": "Cronograma Curso × Turmas",
        "descricao": "Cronograma consolidado por curso e turmas.",
        "url": "atividades:relatorio_cronograma_curso_turmas",
        "exportacoes": ["csv", "excel", "pdf"],
    },
    {
        "nome": "Histórico do Aluno",
        "descricao": "Histórico e jornadas por atividade do aluno.",
        "url": "atividades:relatorio_historico_aluno",
        "exportacoes": ["csv", "excel", "pdf"],
    },
]
