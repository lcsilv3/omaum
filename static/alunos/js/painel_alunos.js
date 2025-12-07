document.addEventListener("DOMContentLoaded", function () {
    // URLs das APIs (assumindo que foram definidas em algum lugar, ex: no template)
    const kpisApiUrl = "/alunos/api/painel/kpis/";
    const graficosApiUrl = "/alunos/api/painel/graficos/";
    const tabelaApiUrl = "/alunos/api/painel/tabela/";

    // --- Carregar KPIs ---
    const kpisContainer = document.getElementById("painel-kpis");
    if (kpisContainer) {
        fetch(kpisApiUrl)
            .then((response) => response.json())
            .then((data) => {
                kpisContainer.innerHTML = `
                    <div class="col-md-3">
                        <div class="card text-center mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Total de Alunos</h5>
                                <p class="card-text display-4">${data.total_alunos}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Alunos Ativos</h5>
                                <p class="card-text display-4 text-success">${data.alunos_ativos}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Média de Idade</h5>
                                <p class="card-text display-4">${data.media_idade}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Qualidade dos Dados</h5>
                                <p class="card-text display-4 text-info">${data.qualidade_dados}%</p>
                            </div>
                        </div>
                    </div>
                `;
            })
            .catch(error => {
                kpisContainer.innerHTML = `<div class="col"><div class="alert alert-danger">Erro ao carregar KPIs: ${error}</div></div>`;
            });
    }

    // --- Carregar Gráficos ---
    const graficoSituacaoCtx = document.getElementById("grafico-situacao");
    const graficoNovosMesCtx = document.getElementById("grafico-novos-mes");

    if (graficoSituacaoCtx && graficoNovosMesCtx) {
        fetch(graficosApiUrl)
            .then(response => response.json())
            .then(data => {
                // Gráfico de Situação (Pizza)
                new Chart(graficoSituacaoCtx, {
                    type: 'pie',
                    data: {
                        labels: data.situacao.labels,
                        datasets: [{
                            label: 'Alunos',
                            data: data.situacao.values,
                            backgroundColor: ['#28a745', '#dc3545', '#ffc107', '#6c757d'],
                        }]
                    }
                });

                // Gráfico de Novos Alunos por Mês (Barras)
                new Chart(graficoNovosMesCtx, {
                    type: 'bar',
                    data: {
                        labels: data.novos_mes.labels,
                        datasets: [{
                            label: 'Novos Alunos',
                            data: data.novos_mes.values,
                            backgroundColor: 'rgba(0, 123, 255, 0.5)',
                            borderColor: 'rgba(0, 123, 255, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            })
            .catch(error => console.error("Erro ao carregar dados dos gráficos:", error));
    }

    // --- Carregar Tabela ---
    const tabelaContainer = document.getElementById("painel-tabela");
    if (tabelaContainer) {
        fetch(tabelaApiUrl)
            .then(response => response.text())
            .then(html => {
                tabelaContainer.innerHTML = html;
            })
            .catch(error => {
                tabelaContainer.innerHTML = `<div class="alert alert-danger">Erro ao carregar tabela de alunos: ${error}</div>`;
            });
    }
});
