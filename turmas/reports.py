# Definição dos relatórios do app Turmas
RELATORIOS = [
    {
        "nome": "Frequência por Turma",
        "descricao": "Relatório de frequência por turma",
        "url": "turmas:listar_turmas",
        "exportacoes": ["csv"],
    },
    {
        "nome": "Painel de Turmas",
        "descricao": "Visão geral com KPIs, turmas populares e estatísticas gerais.",
        "url": "turmas:dashboard_turmas",
        "exportacoes": [],
    },
    {
        "nome": "Estatísticas de Turmas",
        "descricao": "Relatório com totais por curso, instrutor e status.",
        "url": "turmas:relatorio_turmas",
        "exportacoes": [],
    },
    {
        "nome": "Frequência Mensal",
        "descricao": "Consolidado mensal com totais por turma e curso.",
        "url": "frequencias:relatorio_frequencias",
        "exportacoes": ["csv", "pdf"],
    },
    {
        "nome": "Carências e Frequência",
        "descricao": "Resumo de presença e carências por turma.",
        "url": "atividades:relatorio_frequencia_turma",
        "exportacoes": ["csv", "excel"],
    },
    {
        "nome": "Cronograma Curso × Turmas",
        "descricao": "Grade planejada de aulas por curso e turma.",
        "url": "atividades:relatorio_cronograma_curso_turmas",
        "exportacoes": ["csv", "excel"],
    },
    {
        "nome": "Relatório Consolidado de Presença",
        "descricao": "Consolida presenças por curso, turma e período.",
        "url": "relatorios_presenca:relatorio_form",
        "exportacoes": ["xls", "csv"],
    },
]
