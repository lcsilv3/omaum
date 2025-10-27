# Definição dos relatórios do app Atividades
RELATORIOS = [
    {
        "nome": "Relatório de Atividades",
        "descricao": "Panorama geral das atividades cadastradas.",
        "url": "atividades:relatorio_atividades",
        "exportacoes": ["csv", "excel", "pdf"],
    },
    {
        "nome": "Participação por Atividade",
        "descricao": "Resumo de participação e presença por atividade.",
        "url": "atividades:relatorio_participacao_atividades",
        "exportacoes": ["csv", "excel"],
    },
    {
        "nome": "Carga de Instrutores",
        "descricao": "Distribuição da carga de trabalho dos instrutores.",
        "url": "atividades:relatorio_carga_instrutores",
        "exportacoes": ["csv", "excel"],
    },
    {
        "nome": "Carências e Frequência",
        "descricao": "Relatório de frequência e carências por turma.",
        "url": "atividades:relatorio_frequencia_turma",
        "exportacoes": ["csv", "excel"],
    },
    {
        "nome": "Cronograma Curso × Turmas",
        "descricao": "Grade de aulas planejadas por curso e turma.",
        "url": "atividades:relatorio_cronograma_curso_turmas",
        "exportacoes": ["csv", "excel"],
    },
    {
        "nome": "Histórico do Aluno",
        "descricao": "Eventos e atividades concluídas por aluno.",
        "url": "atividades:relatorio_historico_aluno",
        "exportacoes": ["csv", "excel", "pdf"],
    },
]
