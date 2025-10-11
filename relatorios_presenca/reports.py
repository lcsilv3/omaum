# Definição dos relatórios do app relatorios_presenca
RELATORIOS = [
    {
        "nome": "Boletim de Frequência do Aluno",
        "descricao": "Boletim de frequência detalhado",
        "url": "relatorios_presenca:boletim_frequencia_aluno",
        "exportacoes": ["csv", "pdf"],
    },
    {
        "nome": "Relatório Consolidado de Presença",
        "descricao": "Resumo por curso, turma e período com exportações.",
        "url": "relatorios_presenca:relatorio_form",
        "exportacoes": ["xls", "csv"],
    },
]
