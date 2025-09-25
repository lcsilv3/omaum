// JS do Painel de Alunos: carrega KPIs, gráficos e tabela via AJAX


document.addEventListener('DOMContentLoaded', function() {
    carregarKPIs();
    carregarGraficos();
    inicializarTabelaPainel();
});

function carregarKPIs() {
    fetch('/alunos/api/painel/kpis/')
        .then(resp => resp.json())
        .then(data => {
            document.getElementById('painel-kpis').innerHTML = `
                <div class="col-md-3 mb-3">
                    <div class="card text-white bg-primary"><div class="card-body"><h5>Total de Alunos</h5><p class="display-4">${data.total_alunos}</p></div></div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card text-white bg-success"><div class="card-body"><h5>Alunos Ativos</h5><p class="display-4">${data.alunos_ativos}</p></div></div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card text-white bg-info"><div class="card-body"><h5>Média de Idade</h5><p class="display-4">${data.media_idade}</p></div></div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card text-white bg-warning"><div class="card-body"><h5>Qualidade dos Dados</h5><p class="display-4">${data.qualidade_dados}%</p></div></div>
                </div>
            `;
        });
}

function carregarGraficos() {
    fetch('/alunos/api/painel/graficos/')
        .then(resp => resp.json())
        .then(data => {
            // Gráfico de Situação
            new Chart(document.getElementById('grafico-situacao'), {
                type: 'pie',
                data: {
                    labels: data.situacao.labels,
                    datasets: [{
                        data: data.situacao.values,
                        backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d']
                    }]
                }
            });
            // Gráfico de Novos por Mês
            new Chart(document.getElementById('grafico-novos-mes'), {
                type: 'bar',
                data: {
                    labels: data.novos_mes.labels,
                    datasets: [{
                        label: 'Novos Alunos',
                        data: data.novos_mes.values,
                        backgroundColor: '#007bff'
                    }]
                }
            });
        });
}

function inicializarTabelaPainel() {
    // Filtros e paginação
    const painelTabela = document.getElementById('painel-tabela');
    const filtroNome = document.getElementById('filtro-nome');
    const filtroCpf = document.getElementById('filtro-cpf');
    const filtroSituacao = document.getElementById('filtro-situacao');
    const btnExportarCsv = document.getElementById('btn-exportar-csv');
    const btnExportarXls = document.getElementById('btn-exportar-xls');

    let paginaAtual = 1;

    function montarUrlTabela(page=1) {
        const params = new URLSearchParams();
        if (filtroNome && filtroNome.value) params.append('nome', filtroNome.value);
        if (filtroCpf && filtroCpf.value) params.append('cpf', filtroCpf.value);
        if (filtroSituacao && filtroSituacao.value) params.append('situacao', filtroSituacao.value);
        params.append('page', page);
        return `/alunos/api/painel/tabela/?${params.toString()}`;
    }

    function carregarTabela(page=1) {
        fetch(montarUrlTabela(page))
            .then(resp => resp.text())
            .then(html => {
                painelTabela.innerHTML = html;
                paginaAtual = page;
                inicializarPaginacao();
                inicializarTooltips();
            });
    }

    function inicializarPaginacao() {
        const paginacao = document.getElementById('paginacao-alunos');
        if (paginacao) {
            paginacao.querySelectorAll('a.page-link').forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const page = this.dataset.page;
                    if (page) carregarTabela(page);
                });
            });
        }
    }

    function inicializarTooltips() {
        if (window.bootstrap && bootstrap.Tooltip) {
            document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
                new bootstrap.Tooltip(el);
            });
        }
    }

    // Filtros
    [filtroNome, filtroCpf, filtroSituacao].forEach(filtro => {
        if (filtro) {
            filtro.addEventListener('input', function() {
                carregarTabela(1);
            });
        }
    });

    // Exportação CSV
    if (btnExportarCsv) {
        btnExportarCsv.addEventListener('click', function() {
            window.open(montarUrlTabela(paginaAtual) + '&export=csv', '_blank');
        });
    }
    // Exportação Excel
    if (btnExportarXls) {
        btnExportarXls.addEventListener('click', function() {
            window.open(montarUrlTabela(paginaAtual) + '&export=xls', '_blank');
        });
    }

    // Carregar tabela inicial
    carregarTabela(1);
}
