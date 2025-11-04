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
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "alunos:relatorio_ficha_cadastral",
                "query": {"export": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "alunos:relatorio_ficha_cadastral",
                "query": {"export": "excel"},
            },
            {
                "label": "PDF",
                "url_name": "alunos:relatorio_ficha_cadastral",
                "query": {"export": "pdf"},
            },
        ],
    },
    {
        "nome": "Dados Iniciáticos",
        "descricao": "Relatório de dados iniciáticos, grau, situação e tempo de casa.",
        "url": "alunos:relatorio_dados_iniciaticos",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "alunos:relatorio_dados_iniciaticos",
                "query": {"export": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "alunos:relatorio_dados_iniciaticos",
                "query": {"export": "xls"},
            },
            {
                "label": "PDF",
                "url_name": "alunos:relatorio_dados_iniciaticos",
                "query": {"export": "pdf"},
            },
        ],
    },
    {
        "nome": "Histórico do Aluno",
        "descricao": "Eventos, registros e histórico individual ou geral.",
        "url": "alunos:relatorio_historico_aluno",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "alunos:relatorio_historico_aluno",
                "query": {"export": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "alunos:relatorio_historico_aluno",
                "query": {"export": "xls"},
            },
            {
                "label": "PDF",
                "url_name": "alunos:relatorio_historico_aluno",
                "query": {"export": "pdf"},
            },
        ],
    },
    {
        "nome": "Auditoria de Dados",
        "descricao": "Auditoria de campos obrigatórios e dados faltantes.",
        "url": "alunos:relatorio_auditoria_dados",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "alunos:relatorio_auditoria_dados",
                "query": {"export": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "alunos:relatorio_auditoria_dados",
                "query": {"export": "xls"},
            },
            {
                "label": "PDF",
                "url_name": "alunos:relatorio_auditoria_dados",
                "query": {"export": "pdf"},
            },
        ],
    },
    {
        "nome": "Demográfico",
        "descricao": "Distribuição por faixa etária, cidade e sexo, com gráficos.",
        "url": "alunos:relatorio_demografico",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "alunos:relatorio_demografico",
                "query": {"export": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "alunos:relatorio_demografico",
                "query": {"export": "xls"},
            },
        ],
    },
    {
        "nome": "Aniversariantes",
        "descricao": "Lista de aniversariantes do mês, com exportação e integração futura.",
        "url": "alunos:relatorio_aniversariantes",
        "exportacoes": [
            {
                "label": "CSV",
                "url_name": "alunos:relatorio_aniversariantes",
                "query": {"export": "csv"},
            },
            {
                "label": "Excel",
                "url_name": "alunos:relatorio_aniversariantes",
                "query": {"export": "xls"},
            },
            {
                "label": "PDF",
                "url_name": "alunos:relatorio_aniversariantes",
                "query": {"export": "pdf"},
            },
        ],
    },
]
