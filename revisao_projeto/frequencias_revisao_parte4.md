'''
# Revisão da Funcionalidade: frequencias

## Arquivos forms.py:


### Arquivo: frequencias\templates\frequencias\relatorio_frequencias.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Frequências{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
  <div class="d-flex justify-content-between align-items-center mb-3">
      <h1>Relatório de Frequências</h1>
      <div class="btn-group">
          <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
              <i class="fas fa-arrow-left"></i> Voltar
          </a>
          <button id="btn-imprimir" class="btn btn-primary">
              <i class="fas fa-print"></i> Imprimir
          </button>
          <button id="btn-exportar-pdf" class="btn btn-danger">
              <i class="fas fa-file-pdf"></i> Exportar PDF
          </button>
          <button id="btn-exportar-excel" class="btn btn-success">
              <i class="fas fa-file-excel"></i> Exportar Excel
          </button>
      </div>
  </div>
    
  <!-- Filtros -->
  <div class="card mb-4 no-print">
      <div class="card-header bg-light">
          <h5 class="mb-0">Filtros</h5>
      </div>
      <div class="card-body">
          <form method="get" class="row g-3">
              <div class="col-md-3">
                  <label for="turma" class="form-label">Turma</label>
                  <select name="turma" id="turma" class="form-select select2">
                      <option value="">Todas as turmas</option>
                      {% for turma in turmas %}
                      <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"s" %}selected{% endif %}>
                          {{ turma.nome }}
                      </option>
                      {% endfor %}
                  </select>
              </div>
              <div class="col-md-2">
                  <label for="mes" class="form-label">Mês</label>
                  <select name="mes" id="mes" class="form-select">
                      <option value="">Todos os meses</option>
                      {% for mes_valor, mes_nome in meses_choices %}
                      <option value="{{ mes_valor }}" {% if request.GET.mes == mes_valor %}selected{% endif %}>
                          {{ mes_nome }}
                      </option>
                      {% endfor %}
                  </select>
              </div>
              <div class="col-md-2">
                  <label for="ano" class="form-label">Ano</label>
                  <select name="ano" id="ano" class="form-select">
                      <option value="">Todos os anos</option>
                      {% for ano in anos %}
                      <option value="{{ ano }}" {% if request.GET.ano == ano|stringformat:"s" %}selected{% endif %}>
                          {{ ano }}
                      </option>
                      {% endfor %}
                  </select>
              </div>
              <div class="col-md-3">
                  <label for="status" class="form-label">Status da Carência</label>
                  <select name="status" id="status" class="form-select">
                      <option value="">Todos os status</option>
                      <option value="PENDENTE" {% if request.GET.status == "PENDENTE" %}selected{% endif %}>Pendente</option>
                      <option value="EM_ACOMPANHAMENTO" {% if request.GET.status == "EM_ACOMPANHAMENTO" %}selected{% endif %}>Em Acompanhamento</option>
                      <option value="RESOLVIDO" {% if request.GET.status == "RESOLVIDO" %}selected{% endif %}>Resolvido</option>
                  </select>
              </div>
              <div class="col-12 mt-3">
                  <button type="submit" class="btn btn-primary">
                      <i class="fas fa-filter"></i> Filtrar
                  </button>
                  <a href="{% url 'frequencias:relatorio_frequencias' %}" class="btn btn-secondary">
                      <i class="fas fa-broom"></i> Limpar Filtros
                  </a>
              </div>
          </form>
      </div>
  </div>
    
  <!-- Cabeçalho do relatório -->
  <div class="card mb-4">
      <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
              <div>
                  <h2 class="mb-1">Relatório de Frequências</h2>
                  <p class="text-muted mb-0">Gerado em: {{ data_geracao|date:"d/m/Y H:i" }}</p>
              </div>
              <div class="text-end">
                  <h5>Filtros aplicados:</h5>
                  <p class="mb-0">
                      Turma: {{ turma_selecionada|default:"Todas" }} |
                      Período: {{ mes_selecionado|default:"Todos os meses" }}/{{ ano_selecionado|default:"Todos os anos" }} |
                      Status: {{ status_selecionado|default:"Todos" }}
                  </p>
              </div>
          </div>
      </div>
  </div>
    
  <!-- Resumo estatístico -->
  <div class="card mb-4">
      <div class="card-header bg-light">
          <h5 class="mb-0">Resumo Estatístico</h5>
      </div>
      <div class="card-body">
          <div class="row">
              <div class="col-md-3">
                  <div class="card text-center mb-3">
                      <div class="card-body">
                          <h5 class="card-title">Total de Frequências</h5>
                          <p class="card-text display-4">{{ total_frequencias }}</p>
                      </div>
                  </div>
              </div>
              <div class="col-md-3">
                  <div class="card text-center mb-3">
                      <div class="card-body">
                          <h5 class="card-title">Total de Carências</h5>
                          <p class="card-text display-4">{{ total_carencias }}</p>
                      </div>
                  </div>
              </div>
              <div class="col-md-3">
                  <div class="card text-center mb-3">
                      <div class="card-body">
                          <h5 class="card-title">Carências Pendentes</h5>
                          <p class="card-text display-4">{{ carencias_pendentes }}</p>
                      </div>
                  </div>
              </div>
              <div class="col-md-3">
                  <div class="card text-center mb-3">
                      <div class="card-body">
                          <h5 class="card-title">Carências Resolvidas</h5>
                          <p class="card-text display-4">{{ carencias_resolvidas }}</p>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>
    
  <!-- Tabela de carências -->
  <div class="card mb-4">
      <div class="card-header bg-light">
          <h5 class="mb-0">Lista de Carências</h5>
      </div>
      <div class="card-body">
          <div class="table-responsive">
              <table class="table table-striped table-hover">
                  <thead class="table-dark">
                      <tr>
                          <th>Aluno</th>
                          <th>Turma</th>
                          <th>Período</th>
                          <th>Percentual</th>
                          <th>Status</th>
                          <th>Data de Resolução</th>
                          <th>Observações</th>
                      </tr>
                  </thead>
                  <tbody>
                      {% for carencia in carencias %}
                      <tr>
                          <td>
                              <div class="d-flex align-items-center">
                                  {% if carencia.aluno.foto %}
                                  <img src="{{ carencia.aluno.foto.url }}" alt="{{ carencia.aluno.nome }}" 
                                       class="rounded-circle me-2" width="40" height="40">
                                  {% else %}
                                  <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                       style="width: 40px; height: 40px; color: white;">
                                      {{ carencia.aluno.nome|first|upper }}
                                  </div>
                                  {% endif %}
                                  <div>
                                      <div>{{ carencia.aluno.nome }}</div>
                                      <small class="text-muted">{{ carencia.aluno.cpf }}</small>
                                  </div>
                              </div>
                          </td>
                          <td>{{ carencia.frequencia_mensal.turma.nome }}</td>
                          <td>{{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</td>
                          <td>
                              <div class="progress" style="height: 20px;">
                                  <div class="progress-bar bg-danger" role="progressbar" 
                                       style="width: {{ carencia.percentual_presenca }}%;" 
                                       aria-valuenow="{{ carencia.percentual_presenca }}" 
                                       aria-valuemin="0" aria-valuemax="100">
                                      {{ carencia.percentual_presenca }}%
                                  </div>
                              </div>
                          </td>
                          <td>
                              {% if carencia.status == 'PENDENTE' %}
                              <span class="badge bg-danger">Pendente</span>
                              {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}
                              <span class="badge bg-warning text-dark">Em Acompanhamento</span>
                              {% elif carencia.status == 'RESOLVIDO' %}
                              <span class="badge bg-success">Resolvido</span>
                              {% endif %}
                          </td>
                          <td>{{ carencia.data_resolucao|date:"d/m/Y"|default:"-" }}</td>
                          <td>{{ carencia.observacoes|default:"-" }}</td>
                      </tr>
                      {% empty %}
                      <tr>
                          <td colspan="7" class="text-center py-4">
                              <div class="alert alert-info mb-0">
                                  Nenhuma carência encontrada com os filtros selecionados.
                              </div>
                          </td>
                      </tr>
                      {% endfor %}
                  </tbody>
              </table>
          </div>
            
          <!-- Paginação -->
          {% if page_obj.has_other_pages %}
          <nav aria-label="Paginação" class="mt-4 no-print">
              <ul class="pagination justify-content-center">
                  {% if page_obj.has_previous %}
                  <li class="page-item">
                      <a class="page-link" href="?page=1{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                          <i class="fas fa-angle-double-left"></i>
                      </a>
                  </li>
                  <li class="page-item">
                      <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                          <i class="fas fa-angle-left"></i>
                      </a>
                  </li>
                  {% else %}
                  <li class="page-item disabled">
                      <span class="page-link"><i class="fas fa-angle-double-left"></i></span>
                  </li>
                  <li class="page-item disabled">
                      <span class="page-link"><i class="fas fa-angle-left"></i></span>
                  </li>
                  {% endif %}
                    
                  {% for num in page_obj.paginator.page_range %}
                      {% if page_obj.number == num %}
                      <li class="page-item active">
                          <span class="page-link">{{ num }}</span>
                      </li>
                      {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                      <li class="page-item">
                          <a class="page-link" href="?page={{ num }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                              {{ num }}
                          </a>
                      </li>
                      {% endif %}
                  {% endfor %}
                    
                  {% if page_obj.has_next %}
                  <li class="page-item">
                      <a class="page-link" href="?page={{ page_obj.next_page_number }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                          <i class="fas fa-angle-right"></i>
                      </a>
                  </li>
                  <li class="page-item">
                      <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                          <i class="fas fa-angle-double-right"></i>
                      </a>
                  </li>
                  {% else %}
                  <li class="page-item disabled">
                      <span class="page-link"><i class="fas fa-angle-right"></i></span>
                  </li>
                  <li class="page-item disabled">
                      <span class="page-link"><i class="fas fa-angle-double-right"></i></span>
                  </li>
                  {% endif %}
              </ul>
          </nav>
          {% endif %}
      </div>
      <div class="card-footer">
          <div class="d-flex justify-content-between align-items-center">
              <span>Total: {{ page_obj.paginator.count }} carências</span>
              <span class="no-print">Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span>
          </div>
      </div>
  </div>
    
  <!-- Gráfico de carências por turma -->
  <div class="card mb-4">
      <div class="card-header bg-light">
          <h5 class="mb-0">Carências por Turma</h5>
      </div>
      <div class="card-body">
          <canvas id="grafico-carencias-turma" height="300"></canvas>
      </div>
  </div>
    
  <!-- Gráfico de evolução mensal -->
  <div class="card mb-4">
      <div class="card-header bg-light">
          <h5 class="mb-0">Evolução Mensal de Carências</h5>
      </div>
      <div class="card-body">
          <canvas id="grafico-evolucao-mensal" height="300"></canvas>
      </div>
  </div>
    
  <!-- Rodapé do relatório -->
  <div class="card mb-4">
      <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
              <div>
                  <p class="mb-0">Relatório gerado em: {{ data_geracao|date:"d/m/Y H:i" }}</p>
              </div>
              <div>
                  <p class="mb-0">Sistema de Gestão Acadêmica - OMAUM</p>
              </div>
          </div>
      </div>
  </div>
</div>

<!-- Estilos para impressão -->
<style>
    @media print {
        .no-print {
            display: none !important;
        }
        
        .container-fluid {
            width: 100%;
            padding: 0;
            margin: 0;
        }
        
        .card {
            border: none !important;
            margin-bottom: 20px !important;
        }
        
        .card-header {
            background-color: #f8f9fa !important;
            color: #000 !important;
            border-bottom: 1px solid #dee2e6 !important;
        }
        
        .table {
            width: 100% !important;
            border-collapse: collapse !important;
        }
        
        .table th, .table td {
            border: 1px solid #dee2e6 !important;
            padding: 8px !important;
        }
        
        .table thead th {
            background-color: #f8f9fa !important;
            color: #000 !important;
            border-bottom: 2px solid #dee2e6 !important;
        }
        
        .badge {
            border: 1px solid #000 !important;
            padding: 3px 6px !important;
        }
        
        .badge-danger {
            background-color: #fff !important;
            color: #000 !important;
            border: 1px solid #dc3545 !important;
        }
        
        .badge-warning {
            background-color: #fff !important;
            color: #000 !important;
            border: 1px solid #ffc107 !important;
        }
        
        .badge-success {
            background-color: #fff !important;
            color: #000 !important;
            border: 1px solid #28a745 !important;
        }
        
        .progress {
            border: 1px solid #dee2e6 !important;
            background-color: #f8f9fa !important;
        }
        
        .progress-bar {
            background-color: #6c757d !important;
            color: #fff !important;
        }
    }
</style>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        $('.select2').select2({
            theme: 'bootstrap-5',
            width: '100%'
        });
        
        // Gráfico de carências por turma
        const ctxCarenciasTurma = document.getElementById('grafico-carencias-turma').getContext('2d');
        new Chart(ctxCarenciasTurma, {
            type: 'bar',
            data: {
                labels: {{ turmas_labels|safe }},
                datasets: [
                    {
                        label: 'Pendentes',
                        data: {{ carencias_pendentes_por_turma|safe }},
                        backgroundColor: 'rgba(220, 53, 69, 0.7)',
                        borderColor: 'rgba(220, 53, 69, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Em Acompanhamento',
                        data: {{ carencias_em_acompanhamento_por_turma|safe }},
                        backgroundColor: 'rgba(255, 193, 7, 0.7)',
                        borderColor: 'rgba(255, 193, 7, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Resolvidas',
                        data: {{ carencias_resolvidas_por_turma|safe }},
                        backgroundColor: 'rgba(40, 167, 69, 0.7)',
                        borderColor: 'rgba(40, 167, 69, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        stacked: true
                    },
                    x: {
                        stacked: true
                    }
                }
            }
        });
        
        // Gráfico de evolução mensal
        const ctxEvolucaoMensal = document.getElementById('grafico-evolucao-mensal').getContext('2d');
        new Chart(ctxEvolucaoMensal, {
            type: 'line',
            data: {
                labels: {{ meses_completos|safe }},
                datasets: [
                    {
                        label: 'Novas Carências',
                        data: {{ novas_carencias_por_mes|safe }},
                        borderColor: 'rgba(220, 53, 69, 1)',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        fill: true,
                        tension: 0.3
                    },
                    {
                        label: 'Carências Resolvidas',
                        data: {{ carencias_resolvidas_por_mes|safe }},
                        borderColor: 'rgba(40, 167, 69, 1)',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        fill: true,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        // Botão de impressão
        document.getElementById('btn-imprimir').addEventListener('click', function() {
            window.print();
        });
        
        // Botão de exportar para PDF
        document.getElementById('btn-exportar-pdf').addEventListener('click', function() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF('p', 'mm', 'a4');
            
            // Título do documento
            doc.setFontSize(18);
            doc.text('Relatório de Frequências', 105, 15, { align: 'center' });
            
            // Data de geração
            doc.setFontSize(10);
            doc.text('Gerado em: {{ data_geracao|date:"d/m/Y H:i" }}', 105, 22, { align: 'center' });
            
            // Filtros aplicados
            doc.setFontSize(12);
            doc.text('Filtros: {{ turma_selecionada|default:"Todas as turmas" }} | {{ mes_selecionado|default:"Todos os meses" }}/{{ ano_selecionado|default:"Todos os anos" }} | {{ status_selecionado|default:"Todos os status" }}', 105, 30, { align: 'center' });
            
            // Resumo estatístico
            doc.setFontSize(14);
            doc.text('Resumo Estatístico', 14, 40);
            
            doc.setFontSize(12);
            doc.text('Total de Frequências: {{ total_frequencias }}', 14, 50);
            doc.text('Total de Carências: {{ total_carencias }}', 14, 58);
            doc.text('Carências Pendentes: {{ carencias_pendentes }}', 14, 66);
            doc.text('Carências Resolvidas: {{ carencias_resolvidas }}', 14, 74);
            
            // Capturar gráficos
            html2canvas(document.getElementById('grafico-carencias-turma')).then(function(canvas) {
                const imgData = canvas.toDataURL('image/png');
                doc.addPage();
                doc.text('Carências por Turma', 105, 15, { align: 'center' });
                doc.addImage(imgData, 'PNG', 10, 30, 190, 100);
                
                html2canvas(document.getElementById('grafico-evolucao-mensal')).then(function(canvas) {
                    const imgData = canvas.toDataURL('image/png');
                    doc.addPage();
                    doc.text('Evolução Mensal de Carências', 105, 15, { align: 'center' });
                    doc.addImage(imgData, 'PNG', 10, 30, 190, 100);
                    
                    // Salvar o PDF
                    doc.save('relatorio-frequencias.pdf');
                });
            });
        });
        
        // Botão de exportar para Excel
        document.getElementById('btn-exportar-excel').addEventListener('click', function() {
            // Preparar dados para o Excel
            const dados = [
                ['Relatório de Frequências - {{ data_geracao|date:"d/m/Y H:i" }}'],
                ['Filtros: {{ turma_selecionada|default:"Todas as turmas" }} | {{ mes_selecionado|default:"Todos os meses" }}/{{ ano_selecionado|default:"Todos os anos" }} | {{ status_selecionado|default:"Todos os status" }}'],
                [''],
                ['Resumo Estatístico'],
                ['Total de Frequências', '{{ total_frequencias }}'],
                ['Total de Carências', '{{ total_carencias }}'],
                ['Carências Pendentes', '{{ carencias_pendentes }}'],
                ['Carências Resolvidas', '{{ carencias_resolvidas }}'],
                [''],
                ['Lista de Carências'],
                ['Aluno', 'CPF', 'Turma', 'Período', 'Percentual', 'Status', 'Data de Resolução', 'Observações']
            ];
            
            // Adicionar dados das carências
            {% for carencia in todas_carencias %}
            dados.push([
                '{{ carencia.aluno.nome }}',
                '{{ carencia.aluno.cpf }}',
                '{{ carencia.frequencia_mensal.turma.nome }}',
                '{{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}',
                '{{ carencia.percentual_presenca }}%',
                '{% if carencia.status == "PENDENTE" %}Pendente{% elif carencia.status == "EM_ACOMPANHAMENTO" %}Em Acompanhamento{% else %}Resolvido{% endif %}',
                '{{ carencia.data_resolucao|date:"d/m/Y"|default:"-" }}',
                '{{ carencia.observacoes|default:"-" }}'
            ]);
            {% endfor %}
            
            // Criar planilha
            const ws = XLSX.utils.aoa_to_sheet(dados);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Relatório de Frequências");
            
            // Ajustar largura das colunas
            const wscols = [
                {wch: 30}, // Aluno
                {wch: 15}, // CPF
                {wch: 25}, // Turma
                {wch: 15}, // Período
                {wch: 12}, // Percentual
                {wch: 20}, // Status
                {wch: 15}, // Data de Resolução
                {wch: 40}  // Observações
            ];
            ws['!cols'] = wscols;
            
            // Salvar arquivo
            XLSX.writeFile(wb, "relatorio-frequencias.xlsx");
        });
    });
</script>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\resolver_carencia.html

html
{% extends 'base.html' %}

{% block title %}Resolver Carência{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Resolver Carência</h1>
        <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <!-- Informações da carência -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Informações da Carência</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> {{ carencia.aluno.nome }}</p>
                    <p><strong>CPF:</strong> {{ carencia.aluno.cpf }}</p>
                    <p><strong>Turma:</strong> {{ carencia.frequencia_mensal.turma.nome }}</p>
                    <p><strong>Curso:</strong> {{ carencia.frequencia_mensal.turma.curso.nome }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Período:</strong> {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</p>
                    <p><strong>Percentual de Presença:</strong> {{ carencia.percentual_presenca|floatformat:1 }}%</p>
                    <p><strong>Percentual Mínimo:</strong> {{ carencia.frequencia_mensal.percentual_minimo }}%</p>
                    <p><strong>Status Atual:</strong> {{ carencia.get_status_display }}</p>
                </div>
            </div>
            
            <div class="mt-3">
                <h6>Percentual de Presença:</h6>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar bg-danger" role="progressbar" 
                         style="width: {{ carencia.percentual_presenca }}%;" 
                         aria-valuenow="{{ carencia.percentual_presenca }}" 
                         aria-valuemin="0" aria-valuemax="100">
                        {{ carencia.percentual_presenca|floatformat:1 }}%
                    </div>
                </div>
                <div class="d-flex justify-content-between mt-1">
                    <small class="text-muted">0%</small>
                    <small class="text-danger">Mínimo: {{ carencia.frequencia_mensal.percentual_minimo }}%</small>
                    <small class="text-muted">100%</small>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Formulário de resolução -->
    <div class="card mb-4">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Resolver Carência</h5>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="motivo_resolucao" class="form-label">Motivo da Resolução</label>
                    <select class="form-select" id="motivo_resolucao" name="motivo_resolucao" required>
                        <option value="">Selecione um motivo</option>
                        <option value="COMPENSACAO">Compensação de Faltas</option>
                        <option value="JUSTIFICATIVA">Justificativa Aceita</option>
                        <option value="DISPENSA">Dispensa Médica</option>
                        <option value="ERRO_REGISTRO">Erro no Registro de Presença</option>
                        <option value="OUTRO">Outro Motivo</option>
                    </select>
                </div>
                
                <div class="mb-3">
                    <label for="observacoes" class="form-label">Observações</label>
                    <textarea class="form-control" id="observacoes" name="observacoes" rows="5" required></textarea>
                    <div class="form-text">Descreva detalhadamente o motivo da resolução desta carência.</div>
                </div>
                
                <div class="mb-3">
                    <label for="documentos" class="form-label">Documentos Comprobatórios (opcional)</label>
                    <input type="file" class="form-control" id="documentos" name="documentos" multiple>
                    <div class="form-text">Anexe documentos que comprovem a justificativa (atestados, declarações, etc).</div>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="notificar_aluno" name="notificar_aluno" checked>
                    <label class="form-check-label" for="notificar_aluno">
                        Notificar aluno sobre a resolução
                    </label>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-check"></i> Resolver Carência
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\responder_notificacao.html

html
{% extends 'base.html' %}

{% block title %}Responder Notificação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Responder Notificação</h1>
        <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <!-- Informações da notificação original -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Notificação Original</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p>{{ notificacao.assunto }}</p>
            </div>
            
            <div class="mb-3">
                <h6>Mensagem:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ notificacao.mensagem|linebreaks }}
                </div>
            </div>
            
            {% if notificacao.anexos.all %}
            <div>
                <h6>Anexos:</h6>
                <ul class="list-group">
                    {% for anexo in notificacao.anexos.all %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>{{ anexo.nome }}</span>
                        <a href="{{ anexo.arquivo.url }}" class="btn btn-sm btn-outline-primary" download>
                            <i class="fas fa-download"></i> Download
                        </a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Formulário de resposta -->
    <div class="card mb-4">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Sua Resposta</h5>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="assunto" class="form-label">Assunto</label>
                    <input type="text" class="form-control" id="assunto" name="assunto" 
                           value="RE: {{ notificacao.assunto }}" required>
                </div>
                
                <div class="mb-3">
                    <label for="mensagem" class="form-label">Mensagem</label>
                    <textarea class="form-control" id="mensagem" name="mensagem" rows="10" required></textarea>
                    <div class="form-text">Explique a situação e forneça justificativas para as faltas, se possível.</div>
                </div>
                
                <div class="mb-3">
                    <label for="anexos" class="form-label">Anexos (opcional)</label>
                    <input type="file" class="form-control" id="anexos" name="anexos" multiple>
                    <div class="form-text">Você pode anexar atestados médicos, declarações ou outros documentos que justifiquem suas ausências.</div>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="solicitar_compensacao" name="solicitar_compensacao">
                    <label class="form-check-label" for="solicitar_compensacao">
                        Solicitar opções de compensação de faltas
                    </label>
                    <div class="form-text">Marque esta opção se deseja solicitar atividades para compensar as faltas.</div>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-paper-plane"></i> Enviar Resposta
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Dicas para justificativas -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Dicas para Justificativas</h5>
        </div>
        <div class="card-body">
            <ul class="mb-0">
                <li>Seja claro e objetivo ao explicar os motivos das faltas.</li>
                <li>Anexe documentos comprobatórios sempre que possível (atestados médicos, declarações, etc.).</li>
                <li>Se as faltas foram por motivos de saúde, mencione o período e o tratamento realizado.</li>
                <li>Caso tenha problemas de transporte ou trabalho, explique a situação detalhadamente.</li>
                <li>Demonstre seu interesse em recuperar o conteúdo perdido e melhorar sua frequência.</li>
                <li>Se necessário, solicite uma reunião presencial para discutir sua situação.</li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\visualizar_resposta.html

html
{% extends 'base.html' %}

{% block title %}Resposta da Notificação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Resposta da Notificação</h1>
        <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <!-- Informações da notificação -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Informações da Notificação</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> {{ notificacao.carencia.aluno.nome }}</p>
                    <p><strong>Turma:</strong> {{ notificacao.carencia.frequencia_mensal.turma.nome }}</p>
                    <p><strong>Período:</strong> {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Data de Envio:</strong> {{ notificacao.data_envio|date:"d/m/Y H:i" }}</p>
                    <p><strong>Data de Leitura:</strong> {{ notificacao.data_leitura|date:"d/m/Y H:i" }}</p>
                    <p><strong>Data de Resposta:</strong> {{ notificacao.data_resposta|date:"d/m/Y H:i" }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Resposta do aluno -->
    <div class="card mb-4">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Resposta do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p>{{ resposta.assunto }}</p>
            </div>
            
            <div>
                <h6>Mensagem:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ resposta.mensagem|linebreaks }}
                </div>
            </div>
            
            {% if resposta.anexos.all %}
            <div class="mt-3">
                <h6>Anexos:</h6>
                <ul class="list-group">
                    {% for anexo in resposta.anexos.all %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>{{ anexo.nome }}</span>
                        <a href="{{ anexo.arquivo.url }}" class="btn btn-sm btn-outline-primary" download>
                            <i class="fas fa-download"></i> Download
                        </a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Formulário de resposta ao aluno -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Responder ao Aluno</h5>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="assunto" class="form-label">Assunto</label>
                    <input type="text" class="form-control" id="assunto" name="assunto" 
                           value="Re: {{ resposta.assunto }}" required>
                </div>
                
                <div class="mb-3">
                    <label for="mensagem" class="form-label">Mensagem</label>
                    <textarea class="form-control" id="mensagem" name="mensagem" rows="6" required></textarea>
                    <div class="form-text">Escreva sua resposta ao aluno.</div>
                </div>
                
                <div class="mb-3">
                    <label for="anexos" class="form-label">Anexos (opcional)</label>
                    <input type="file" class="form-control" id="anexos" name="anexos" multiple>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="resolver_carencia" name="resolver_carencia">
                    <label class="form-check-label" for="resolver_carencia">
                        Marcar carência como resolvida
                    </label>
                </div>
                
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-paper-plane"></i> Enviar Resposta
                </button>
            </form>
        </div>
    </div>
    
    <!-- Histórico de comunicações -->
    <div class="card mb-4">
        <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Histórico de Comunicações</h5>
        </div>
        <div class="card-body">
            <div class="chat-container">
                <!-- Notificação original -->
                <div class="chat-message outgoing">
                    <div class="message-header">
                        <strong>Você</strong> <span class="text-muted">{{ notificacao.data_envio|date:"d/m/Y H:i" }}</span>
                    </div>
                    <div class="message-content">
                        <h6>{{ notificacao.assunto }}</h6>
                        <div class="message-body">
                            {{ notificacao.mensagem|linebreaks }}
                        </div>
                        {% if notificacao.anexos.all %}
                        <div class="message-attachments">
                            <strong>Anexos:</strong>
                            <ul>
                                {% for anexo in notificacao.anexos.all %}
                                <li>
                                    <a href="{{ anexo.arquivo.url }}" download>{{ anexo.nome }}</a>
                                </li>
                                {% endfor %}
                            </ul>
                        </div>
                        {% endif %}
                    </div>
                </div>
                
                <!-- Resposta do aluno -->
                <div class="chat-message incoming">
                    <div class="message-header">
                        <strong>{{ notificacao.carencia.aluno.nome }}</strong> <span class="text-muted">{{ notificacao.data_resposta|date:"d/m/Y H:i" }}</span>
                    </div>
                    <div class="message-content">
                        <h6>{{ resposta.assunto }}</h6>
                        <div class="message-body">
                            {{ resposta.mensagem|linebreaks }}
                        </div>
                        {% if resposta.anexos.all %}
                        <div class="message-attachments">
                            <strong>Anexos:</strong>
                            <ul>
                                {% for anexo in resposta.anexos.all %}
                                <li>
                                    <a href="{{ anexo.arquivo.url }}" download>{{ anexo.nome }}</a>
                                </li>
                                {% endfor %}
                            </ul>
                        </div>
                        {% endif %}
                    </div>
                </div>
                
                <!-- Respostas anteriores -->
                {% for mensagem in historico_mensagens %}
                <div class="chat-message {% if mensagem.enviado_por_sistema %}outgoing{% else %}incoming{% endif %}">
                    <div class="message-header">
                        <strong>{% if mensagem.enviado_por_sistema %}Você{% else %}{{ notificacao.carencia.aluno.nome }}{% endif %}</strong> 
                        <span class="text-muted">{{ mensagem.data_envio|date:"d/m/Y H:i" }}</span>
                    </div>
                    <div class="message-content">
                        <h6>{{ mensagem.assunto }}</h6>
                        <div class="message-body">
                            {{ mensagem.mensagem|linebreaks }}
                        </div>
                        {% if mensagem.anexos.all %}
                        <div class="message-attachments">
                            <strong>Anexos:</strong>
                            <ul>
                                {% for anexo in mensagem.anexos.all %}
                                <li>
                                    <a href="{{ anexo.arquivo.url }}" download>{{ anexo.nome }}</a>
                                </li>
                                {% endfor %}
                            </ul>
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <!-- Botões de ação -->
    <div class="d-flex justify-content-between mb-5">
        <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
        
        <div>
            {% if notificacao.carencia.status != 'RESOLVIDO' %}
            <a href="{% url 'frequencias:resolver_carencia' notificacao.carencia.id %}" class="btn btn-success">
                <i class="fas fa-check-circle"></i> Resolver Carência
            </a>
            {% endif %}
        </div>
    </div>
</div>

<style>
    /* Estilos para o chat */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .chat-message {
        max-width: 80%;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    .outgoing {
        align-self: flex-end;
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .incoming {
        align-self: flex-start;
        background-color: #f5f5f5;
        border-left: 4px solid #9e9e9e;
    }
    
    .message-header {
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    
    .message-body {
        white-space: pre-line;
    }
    
    .message-attachments {
        margin-top: 0.75rem;
        padding-top: 0.75rem;
        border-top: 1px dashed rgba(0,0,0,0.1);
    }
</style>
{% endblock %}


'''