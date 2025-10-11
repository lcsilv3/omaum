# Definição dos relatórios do app Alunos
RELATORIOS = [
    {
        "nome": "Painel de Alunos",
        "descricao": "Dashboard com KPIs e gráficos sobre os alunos.",
        "url": "alunos:painel",
        "exportacoes": [],
    },
    {
        "nome": "Ficha Cadastral",
        "descricao": "Ficha completa dos alunos, com filtros e exportação.",
        "url": "alunos:relatorio_ficha_cadastral",
        "exportacoes": ["csv", "xls", "pdf"],
    },
    {
        "nome": "Dados Iniciáticos",
        "descricao": "Relatório de dados iniciáticos, grau, situação e tempo de casa.",
        "url": "alunos:relatorio_dados_iniciaticos",
        "exportacoes": ["csv", "xls"],
    },
    {
        "nome": "Histórico do Aluno",
        "descricao": "Eventos, registros e histórico individual ou geral.",
        "url": "alunos:relatorio_historico_aluno",
        "exportacoes": ["csv", "xls", "pdf"],
    },
    {
        "nome": "Auditoria de Dados",
        "descricao": "Auditoria de campos obrigatórios e dados faltantes.",
        "url": "alunos:relatorio_auditoria_dados",
        "exportacoes": ["csv", "xls", "pdf"],
    },
    {
        "nome": "Demográfico",
        "descricao": "Distribuição por faixa etária, cidade e sexo, com gráficos.",
        "url": "alunos:relatorio_demografico",
        "exportacoes": ["csv", "xls"],
    },
    {
        "nome": "Aniversariantes",
        "descricao": "Lista de aniversariantes do mês, com exportação e integração futura.",
        "url": "alunos:relatorio_aniversariantes",
        "exportacoes": ["csv", "xls"],
    },
]

# Print simples para depuração: garantir que RELATORIOS está definido corretamente
print(f"[DEBUG] RELATORIOS definido em reports.py: {RELATORIOS}")
