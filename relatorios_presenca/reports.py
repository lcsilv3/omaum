# Definição dos relatórios do app relatorios_presenca
RELATORIOS = [
    {
        "nome": "Consolidado de Presença",
        "descricao": "Relatório consolidado de presença",
        "url": "relatorios_presenca:consolidado",
        "exportacoes": ["csv", "excel"],
    },
    {
        "nome": "Boletim de Frequência do Aluno",
        "descricao": "Boletim de frequência detalhado",
        "url": "relatorios_presenca:boletim",
        "exportacoes": ["csv", "pdf"],
    },
]
