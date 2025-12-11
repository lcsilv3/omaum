# Definição dos relatórios do app Turmas
RELATORIOS = [
    {
        "nome": "Frequência por Turma",
        "descricao": "Relatório de frequência por turma",
        "url": "turmas:listar_turmas",
        "exportacoes": ["csv"],
    },
    {
        "nome": "Relatórios (Curso/Turma)",
        "descricao": "Relatórios consolidados de cursos e turmas.",
        "url": "atividades:relatorio_atividades",
        "exportacoes": [],
    },
]
