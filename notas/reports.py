# Definição dos relatórios do app Notas
RELATORIOS = [
    {
        "nome": "Painel de Notas",
        "descricao": "Indicadores e distribuição das notas dos alunos.",
        "url": "notas:dashboard_notas",
        "exportacoes": [],
    },
    {
        "nome": "Listagem de Notas",
        "descricao": "Consulta operacional com filtros e ações por aluno e curso.",
        "url": "notas:listar_notas",
        "exportacoes": ["csv", "excel"],
    },
    {
        "nome": "Exportação CSV",
        "descricao": "Baixe as notas filtradas em formato CSV.",
        "url": "notas:exportar_notas_csv",
        "exportacoes": ["csv"],
    },
    {
        "nome": "Exportação Excel",
        "descricao": "Baixe as notas filtradas em planilha Excel.",
        "url": "notas:exportar_notas_excel",
        "exportacoes": ["excel"],
    },
]
