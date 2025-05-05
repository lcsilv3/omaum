'''
# Revisão da Funcionalidade: frequencias

## Arquivos forms.py:


### Arquivo: frequencias\templates\frequencias\detalhar_notificacao.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Notificação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Detalhes da Notificação</h1>
        <div>
            {% if notificacao.carencia %}
            <a href="{% url 'frequencias:detalhar_carencia' notificacao.carencia.id %}" class="btn btn-secondary me-2">
                <i class="fas fa-exclamation-triangle"></i> Ver Carência
            </a>
            {% endif %}
            <a href="javascript:history.back()" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
        </div>
    </div>
    
    <!-- Status da notificação -->
    <div class="alert 
        {% if notificacao.status == 'PENDENTE' %}alert-secondary
        {% elif notificacao.status == 'ENVIADA' %}alert-info
        {% elif notificacao.status == 'LIDA' %}alert-primary
        {% elif notificacao.status == 'RESPONDIDA' %}alert-success
        {% endif %}">
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h5 class="alert-heading mb-1">
                    {% if notificacao.status == 'PENDENTE' %}
                    <i class="fas fa-clock"></i> Notificação Pendente
                    {% elif notificacao.status == 'ENVIADA' %}
                    <i class="fas fa-paper-plane"></i> Notificação Enviada
                    {% elif notificacao.status == 'LIDA' %}
                    <i class="fas fa-envelope-open"></i> Notificação Lida
                    {% elif notificacao.status == 'RESPONDIDA' %}
                    <i class="fas fa-reply"></i> Notificação Respondida
                    {% endif %}
                </h5>
                <p class="mb-0">
                    {% if notificacao.status == 'PENDENTE' %}
                    Esta notificação ainda não foi enviada ao aluno.
                    {% elif notificacao.status == 'ENVIADA' %}
                    Esta notificação foi enviada em {{ notificacao.data_envio|date:"d/m/Y H:i" }}.
                    {% elif notificacao.status == 'LIDA' %}
                    Esta notificação foi lida pelo aluno em {{ notificacao.data_leitura|date:"d/m/Y H:i" }}.
                    {% elif notificacao.status == 'RESPONDIDA' %}
                    Esta notificação foi respondida pelo aluno em {{ notificacao.data_resposta|date:"d/m/Y H:i" }}.
                    {% endif %}
                </p>
            </div>
            <div>
                {% if notificacao.status == 'PENDENTE' %}
                <a href="{% url 'frequencias:enviar_notificacao' notificacao.id %}" class="btn btn-primary">
                    <i class="fas fa-paper-plane"></i> Enviar Agora
                </a>
                {% elif notificacao.status == 'ENVIADA' or notificacao.status == 'LIDA' %}
                <a href="{% url 'frequencias:reenviar_notificacao' notificacao.id %}" class="btn btn-outline-primary">
                    <i class="fas fa-sync"></i> Reenviar
                </a>
                {% endif %}
            </div>
        </div>
    </div>
    
    <!-- Informações do destinatário -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Destinatário</h5>
        </div>
        <div class="card-body">
            <div class="d-flex align-items-center">
                {% if notificacao.aluno.foto %}
                <img src="{{ notificacao.aluno.foto.url }}" alt="{{ notificacao.aluno.nome }}" 
                     class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                {% else %}
                <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                     style="width: 60px; height: 60px; color: white; font-size: 1.5rem;">
                    {{ notificacao.aluno.nome|first|upper }}
                </div>
                {% endif %}
                <div>
                    <h5 class="mb-1">{{ notificacao.aluno.nome }}</h5>
                    <p class="mb-0">{{ notificacao.aluno.email }}</p>
                    {% if notificacao.aluno.celular_primeiro_contato %}
                    <p class="mb-0">{{ notificacao.aluno.celular_primeiro_contato }}</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    
    <!-- Conteúdo da notificação -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Conteúdo da Notificação</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p class="mb-0">{{ notificacao.assunto }}</p>
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
            
            <div class="mt-3">
                <p class="text-muted mb-0">
                    <small>Criada por: {{ notificacao.criado_por.get_full_name|default:notificacao.criado_por.username }} em {{ notificacao.data_criacao|date:"d/m/Y H:i" }}</small>
                </p>
            </div>
        </div>
    </div>
    
    <!-- Resposta do aluno (se houver) -->
    {% if notificacao.resposta %}
    <div class="card mb-4 border-success">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Resposta do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p class="mb-0">{{ notificacao.resposta.assunto }}</p>
            </div>
            
            <div class="mb-3">
                <h6>Mensagem:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ notificacao.resposta.mensagem|linebreaks }}
                </div>
            </div>
            
            {% if notificacao.resposta.anexos.all %}
            <div>
                <h6>Anexos:</h6>
                <ul class="list-group">
                    {% for anexo in notificacao.resposta.anexos.all %}
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
            
            <div class="mt-3">
                <p class="text-muted mb-0">
                    <small>Respondido em: {{ notificacao.data_resposta|date:"d/m/Y H:i" }}</small>
                </p>
            </div>
            
            {% if notificacao.resposta.solicitar_compensacao %}
            <div class="alert alert-warning mt-3">
                <i class="fas fa-exclamation-circle"></i> O aluno solicitou opções de compensação de faltas.
            </div>
            {% endif %}
        </div>
    </div>
    {% endif %}
    
    <!-- Ações -->
    <div class="card mb-4">
        <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Ações</h5>
        </div>
        <div class="card-body">
            <div class="d-flex flex-wrap gap-2">
                {% if notificacao.status == 'PENDENTE' %}
                <a href="{% url 'frequencias:editar_notificacao' notificacao.id %}" class="btn btn-warning">
                    <i class="fas fa-edit"></i> Editar Notificação
                </a>
                <a href="{% url 'frequencias:enviar_notificacao' notificacao.id %}" class="btn btn-primary">
                    <i class="fas fa-paper-plane"></i> Enviar Notificação
                </a>
                {% elif notificacao.status == 'ENVIADA' or notificacao.status == 'LIDA' %}
                <a href="{% url 'frequencias:reenviar_notificacao' notificacao.id %}" class="btn btn-primary">
                    <i class="fas fa-sync"></i> Reenviar Notificação
                </a>
                {% endif %}
                
                {% if notificacao.status == 'RESPONDIDA' %}
                <a href="{% url 'frequencias:responder_aluno' notificacao.id %}" class="btn btn-success">
                    <i class="fas fa-reply"></i> Responder ao Aluno
                </a>
                {% endif %}
                
                {% if notificacao.carencia and notificacao.carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:resolver_carencia' notificacao.carencia.id %}" class="btn btn-success">
                    <i class="fas fa-check"></i> Resolver Carência
                </a>
                {% endif %}
                
                <a href="{% url 'frequencias:historico_frequencia' notificacao.aluno.cpf %}" class="btn btn-info">
                    <i class="fas fa-history"></i> Ver Histórico de Frequência
                </a>
                
                <a href="{% url 'alunos:detalhar_aluno' notificacao.aluno.cpf %}" class="btn btn-primary">
                    <i class="fas fa-user"></i> Ver Perfil do Aluno
                </a>
            </div>
        </div>
    </div>
    
    <!-- Histórico de ações -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Histórico de Ações</h5>
        </div>
        <div class="card-body p-0">
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-plus-circle text-success"></i> 
                            <strong>Notificação criada</strong> por {{ notificacao.criado_por.get_full_name|default:notificacao.criado_por.username }}
                        </div>
                        <div>{{ notificacao.data_criacao|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                
                {% if notificacao.data_envio %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-paper-plane text-primary"></i> 
                            <strong>Notificação enviada</strong>
                            {% if notificacao.enviado_por %}
                            por {{ notificacao.enviado_por.get_full_name|default:notificacao.enviado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ notificacao.data_envio|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if notificacao.data_leitura %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-envelope-open text-info"></i> 
                            <strong>Notificação lida</strong> pelo aluno
                        </div>
                        <div>{{ notificacao.data_leitura|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if notificacao.data_resposta %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-reply text-success"></i> 
                            <strong>Notificação respondida</strong> pelo aluno
                        </div>
                        <div>{{ notificacao.data_resposta|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% for log in notificacao.logs.all %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas {{ log.get_icone }} {{ log.get_cor }}"></i> 
                            <strong>{{ log.acao }}</strong>
                            {% if log.usuario %}
                            por {{ log.usuario.get_full_name|default:log.usuario.username }}
                            {% endif %}
                        </div>
                        <div>{{ log.data|date:"d/m/Y H:i" }}</div>
                    </div>
                    {% if log.detalhes %}
                    <div class="mt-1 text-muted">
                        <small>{{ log.detalhes }}</small>
                    </div>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\editar_carencia.html

html
{% extends 'base.html' %}

{% block title %}Editar Carência{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-warning text-dark">
                    <h4 class="mb-0">Editar Carência</h4>
                </div>
                <div class="card-body">
                    <div class="mb-4">
                        <div class="d-flex align-items-center">
                            {% if carencia.aluno.foto %}
                            <img src="{{ carencia.aluno.foto.url }}" alt="{{ carencia.aluno.nome }}" 
                                 class="rounded-circle me-3" width="60" height="60">
                            {% else %}
                            <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                                 style="width: 60px; height: 60px; color: white; font-size: 24px;">
                                {{ carencia.aluno.nome|first|upper }}
                            </div>
                            {% endif %}
                            <div>
                                <h5 class="mb-1">{{ carencia.aluno.nome }}</h5>
                                <p class="mb-0 text-muted">{{ carencia.aluno.cpf }}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card mb-4">
                        <div class="card-body">
                            <p><strong>Frequência Mensal:</strong> {{ carencia.frequencia_mensal.turma.nome }} - {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</p>
                            <p><strong>Percentual de Presença:</strong> {{ carencia.percentual_presenca }}%</p>
                            <p><strong>Percentual Mínimo Exigido:</strong> {{ carencia.frequencia_mensal.percentual_minimo }}%</p>
                            <p><strong>Déficit:</strong> {{ carencia.frequencia_mensal.percentual_minimo|subtract:carencia.percentual_presenca|floatformat:1 }}%</p>
                        </div>
                    </div>
                    
                    <form method="post" novalidate>
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                        <div class="alert alert-danger">
                            {% for error in form.non_field_errors %}
                            <p>{{ error }}</p>
                            {% endfor %}
                        </div>
                        {% endif %}
                        
                        <div class="mb-3">
                            <label for="{{ form.observacoes.id_for_label }}" class="form-label">{{ form.observacoes.label }}</label>
                            {{ form.observacoes }}
                            {% if form.observacoes.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.observacoes.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.observacoes.help_text %}
                            <div class="form-text">{{ form.observacoes.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.status.id_for_label }}" class="form-label">{{ form.status.label }}</label>
                            {{ form.status }}
                            {% if form.status.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.status.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.status.help_text %}
                            <div class="form-text">{{ form.status.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3" id="data_resolucao_container" style="display: none;">
                            <label for="{{ form.data_resolucao.id_for_label }}" class="form-label">{{ form.data_resolucao.label }}</label>
                            {{ form.data_resolucao }}
                            {% if form.data_resolucao.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.data_resolucao.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.data_resolucao.help_text %}
                            <div class="form-text">{{ form.data_resolucao.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex justify-content-between mt-4">
                            <a href="{% url 'frequencias:detalhar_frequencia_mensal' carencia.frequencia_mensal.id %}" class="btn btn-secondary">
                                <i class="fas fa-arrow-left"></i> Voltar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Salvar
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Mostrar/ocultar campo de data de resolução com base no status
        const statusSelect = document.getElementById('id_status');
        const dataResolucaoContainer = document.getElementById('data_resolucao_container');
        
        function toggleDataResolucao() {
            if (statusSelect.value === 'RESOLVIDO') {
                dataResolucaoContainer.style.display = 'block';
                document.getElementById('id_data_resolucao').setAttribute('required', 'required');
            } else {
                dataResolucaoContainer.style.display = 'none';
                document.getElementById('id_data_resolucao').removeAttribute('required');
            }
        }
        
        // Executar na inicialização
        toggleDataResolucao();
        
        // Adicionar evento de mudança
        statusSelect.addEventListener('change', toggleDataResolucao);
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\editar_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Registro de FrequÃªncia</h1>
  
    <form method="post">
      {% csrf_token %}
      {% include 'includes/form_errors.html' %}
    
      {% for field in form %}
        {% include 'includes/form_field.html' %}
      {% endfor %}
    
      <button type="submit" class="btn btn-primary">Atualizar</button>
      <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\editar_notificacao.html

html
{% extends 'base.html' %}

{% block title %}Editar Notificação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Editar Notificação</h1>
        <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    {% if notificacao.status != 'PENDENTE' %}
    <div class="alert alert-warning">
        <i class="fas fa-exclamation-triangle"></i> Esta notificação já foi enviada e não pode ser editada.
    </div>
    {% else %}
    
    <!-- Informações da carência -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações da Carência</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> {{ notificacao.carencia.aluno.nome }}</p>
                    <p><strong>CPF:</strong> {{ notificacao.carencia.aluno.cpf }}</p>
                    <p><strong>Email:</strong> {{ notificacao.carencia.aluno.email }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Turma:</strong> {{ notificacao.carencia.frequencia_mensal.turma.nome }}</p>
                    <p><strong>Curso:</strong> {{ notificacao.carencia.frequencia_mensal.turma.curso.nome }}</p>
                    <p><strong>Período:</strong> {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }}</p>
                </div>
            </div>
            
            <div class="mt-3">
                <h6>Percentual de Presença:</h6>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar bg-danger" role="progressbar" 
                         style="width: {{ notificacao.carencia.percentual_presenca }}%;" 
                         aria-valuenow="{{ notificacao.carencia.percentual_presenca }}" 
                         aria-valuemin="0" aria-valuemax="100">
                        {{ notificacao.carencia.percentual_presenca }}%
                    </div>
                </div>
                <small class="text-muted">Mínimo exigido: 75%</small>
            </div>
        </div>
    </div>
    
    <!-- Formulário de edição -->
    <div class="card mb-4">
        <div class="card-header bg-warning text-dark">
            <h5 class="mb-0">Editar Notificação</h5>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="assunto" class="form-label">Assunto</label>
                    <input type="text" class="form-control" id="assunto" name="assunto" 
                           value="{{ notificacao.assunto }}" required>
                </div>
                
                <div class="mb-3">
                    <label for="mensagem" class="form-label">Mensagem</label>
                    <textarea class="form-control" id="mensagem" name="mensagem" rows="10" required>{{ notificacao.mensagem }}</textarea>
                </div>
                
                <div class="mb-3">
                    <label for="anexos" class="form-label">Anexos (opcional)</label>
                    <input type="file" class="form-control" id="anexos" name="anexos" multiple>
                </div>
                
                {% if notificacao.anexos.all %}
                <div class="mb-3">
                    <label class="form-label">Anexos Atuais</label>
                    <ul class="list-group">
                        {% for anexo in notificacao.anexos.all %}
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            <span>{{ anexo.nome }}</span>
                            <div>
                                <a href="{{ anexo.arquivo.url }}" class="btn btn-sm btn-outline-primary me-2" download>
                                    <i class="fas fa-download"></i> Download
                                </a>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="checkbox" id="remover_anexo_{{ anexo.id }}" 
                                           name="remover_anexos" value="{{ anexo.id }}">
                                    <label class="form-check-label" for="remover_anexo_{{ anexo.id }}">Remover</label>
                                </div>
                            </div>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <div>
                        <button type="submit" class="btn btn-warning me-2" name="action" value="salvar">
                            <i class="fas fa-save"></i> Salvar Alterações
                        </button>
                        <button type="submit" class="btn btn-primary" name="action" value="salvar_enviar">
                            <i class="fas fa-paper-plane"></i> Salvar e Enviar
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Modelos de mensagem -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Modelos de Mensagem</h5>
        </div>
        <div class="card-body">
            <div class="accordion" id="accordionModelos">
                <div class="accordion-item">
                    <h2 class="accordion-header" id="headingOne">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                                data-bs-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                            Modelo 1: Notificação Padrão
                        </button>
                    </h2>
                    <div id="collapseOne" class="accordion-collapse collapse" aria-labelledby="headingOne" data-bs-parent="#accordionModelos">
                        <div class="accordion-body">
                            <div class="d-flex justify-content-between mb-2">
                                <strong>Assunto: Notificação de Carência de Frequência</strong>
                                <button class="btn btn-sm btn-outline-primary usar-modelo" data-modelo="1">
                                    <i class="fas fa-copy"></i> Usar este modelo
                                </button>
                            </div>
                            <pre class="bg-light p-3 rounded">Prezado(a) {{ notificacao.carencia.aluno.nome }},

Esperamos que esteja bem. Estamos entrando em contato para informar que foi identificada uma carência de frequência em suas aulas do curso {{ notificacao.carencia.frequencia_mensal.turma.curso.nome }}, na turma {{ notificacao.carencia.frequencia_mensal.turma.nome }}, durante o período de {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }}.

Seu percentual de presença no período foi de {{ notificacao.carencia.percentual_presenca }}%, abaixo do mínimo exigido de 75%.

Gostaríamos de lembrá-lo(a) que a frequência regular é fundamental para o bom aproveitamento do curso e constitui um dos requisitos para aprovação.

Solicitamos que entre em contato conosco para justificar as ausências e discutir possíveis alternativas para compensação das aulas perdidas.

Estamos à disposição para quaisquer esclarecimentos.

Atenciosamente,
Equipe Pedagógica</pre>
                        </div>
                    </div>
                </div>
                
                <div class="accordion-item">
                    <h2 class="accordion-header" id="headingTwo">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                                data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                            Modelo 2: Notificação com Urgência
                        </button>
                    </h2>
                    <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionModelos">
                        <div class="accordion-body">
                            <div class="d-flex justify-content-between mb-2">
                                <strong>Assunto: URGENTE - Notificação de Carência de Frequência</strong>
                                <button class="btn btn-sm btn-outline-primary usar-modelo" data-modelo="2">
                                    <i class="fas fa-copy"></i> Usar este modelo
                                </button>
                            </div>
                            <pre class="bg-light p-3 rounded">Prezado(a) {{ notificacao.carencia.aluno.nome }},

NOTIFICAÇÃO URGENTE

Identificamos uma situação crítica em relação à sua frequência no curso {{ notificacao.carencia.frequencia_mensal.turma.curso.nome }}, turma {{ notificacao.carencia.frequencia_mensal.turma.nome }}.

Seu percentual de presença no período de {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }} foi de apenas {{ notificacao.carencia.percentual_presenca }}%, muito abaixo do mínimo exigido de 75%.

Esta situação coloca em risco sua aprovação no curso e, caso não seja regularizada com urgência, poderá resultar em reprovação por frequência insuficiente.

Solicitamos seu comparecimento à secretaria no prazo máximo de 3 dias úteis para apresentar justificativas e discutir medidas de recuperação.

Caso já possua justificativas para as ausências (atestados médicos ou outros documentos), favor responder a este e-mail com os documentos anexados.

Atenciosamente,
Coordenação Pedagógica</pre>
                        </div>
                    </div>
                </div>
                
                <div class="accordion-item">
                    <h2 class="accordion-header" id="headingThree">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                                data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                            Modelo 3: Notificação com Opções de Recuperação
                        </button>
                    </h2>
                    <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionModelos">
                        <div class="accordion-body">
                            <div class="d-flex justify-content-between mb-2">
                                <strong>Assunto: Notificação de Carência e Opções de Recuperação</strong>
                                <button class="btn btn-sm btn-outline-primary usar-modelo" data-modelo="3">
                                    <i class="fas fa-copy"></i> Usar este modelo
                                </button>
                            </div>
                            <pre class="bg-light p-3 rounded">Prezado(a) {{ notificacao.carencia.aluno.nome }},

Esperamos que esteja bem. Estamos entrando em contato para informar que foi identificada uma carência de frequência em suas aulas do curso {{ notificacao.carencia.frequencia_mensal.turma.curso.nome }}, na turma {{ notificacao.carencia.frequencia_mensal.turma.nome }}, durante o período de {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }}.

Seu percentual de presença no período foi de {{ notificacao.carencia.percentual_presenca }}%, abaixo do mínimo exigido de 75%.

Para regularizar sua situação, oferecemos as seguintes opções de recuperação:

1. Participação em aulas de reposição nos dias XX/XX e XX/XX, das XX:XX às XX:XX.
2. Realização de trabalho complementar sobre os temas abordados nas aulas perdidas.
3. Participação em atividades extras programadas para os dias XX/XX.

Solicitamos que entre em contato conosco até o dia XX/XX para informar qual opção deseja seguir.

Lembramos que a regularização da frequência é fundamental para a continuidade no curso e para o aproveitamento adequado do conteúdo.

Estamos à disposição para quaisquer esclarecimentos.

Atenciosamente,
Equipe Pedagógica</pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    {% endif %}
</div>

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Manipuladores para os botões de modelo
        const botoesModelo = document.querySelectorAll('.usar-modelo');
        const campoAssunto = document.getElementById('assunto');
        const campoMensagem = document.getElementById('mensagem');
        
        // Modelos de assunto
        const assuntosModelo = {
            "1": "Notificação de Carência de Frequência",
            "2": "URGENTE - Notificação de Carência de Frequência",
            "3": "Notificação de Carência e Opções de Recuperação"
        };
        
        // Função para obter o texto do modelo
        function obterTextoModelo(modeloId) {
            const acordeao = document.querySelector(`#collapse${modeloId} pre`);
            return acordeao ? acordeao.textContent.trim() : '';
        }
        
        // Adicionar evento de clique aos botões de modelo
        botoesModelo.forEach(botao => {
            botao.addEventListener('click', function() {
                const modeloId = this.getAttribute('data-modelo');
                
                // Confirmar antes de substituir o conteúdo atual
                if (campoMensagem.value.trim() !== '') {
                    if (!confirm('Isso substituirá o conteúdo atual da mensagem. Deseja continuar?')) {
                        return;
                    }
                }
                
                // Preencher os campos com o modelo selecionado
                campoAssunto.value = assuntosModelo[modeloId] || '';
                campoMensagem.value = obterTextoModelo(modeloId);
                
                // Fechar o acordeão
                const accordion = bootstrap.Collapse.getInstance(document.querySelector(`#collapse${modeloId}`));
                if (accordion) {
                    accordion.hide();
                }
                
                // Rolar até o formulário
                document.querySelector('.card-header.bg-warning').scrollIntoView({ behavior: 'smooth' });
            });
        });
    });
</script>
{% endblock %}
{% endblock %}



### Arquivo: frequencias\templates\frequencias\enviar_notificacao.html

html
{% extends 'base.html' %}

{% block title %}Enviar Notificação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Enviar Notificação</h1>
        <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    {% if notificacao.status != 'PENDENTE' %}
    <div class="alert alert-warning">
        <i class="fas fa-exclamation-triangle"></i> Esta notificação já foi enviada em {{ notificacao.data_envio|date:"d/m/Y H:i" }}.
    </div>
    {% else %}
    
    <!-- Informações do destinatário -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Destinatário</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="d-flex align-items-center mb-3">
                        {% if notificacao.carencia.aluno.foto %}
                        <img src="{{ notificacao.carencia.aluno.foto.url }}" alt="{{ notificacao.carencia.aluno.nome }}" 
                             class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                        {% else %}
                        <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                             style="width: 60px; height: 60px; color: white; font-size: 1.5rem;">
                            {{ notificacao.carencia.aluno.nome|first|upper }}
                        </div>
                        {% endif %}
                        <div>
                            <h5 class="mb-1">{{ notificacao.carencia.aluno.nome }}</h5>
                            <p class="text-muted mb-0">{{ notificacao.carencia.aluno.email }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <p><strong>Turma:</strong> {{ notificacao.carencia.frequencia_mensal.turma.nome }}</p>
                    <p><strong>Curso:</strong> {{ notificacao.carencia.frequencia_mensal.turma.curso.nome }}</p>
                    <p><strong>Período:</strong> {{ notificacao.carencia.frequencia_mensal.get_mes_display }}/{{ notificacao.carencia.frequencia_mensal.ano }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Prévia da notificação -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Prévia da Notificação</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p>{{ notificacao.assunto }}</p>
            </div>
            
            <div>
                <h6>Mensagem:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ notificacao.mensagem|linebreaks }}
                </div>
            </div>
            
            {% if notificacao.anexos.all %}
            <div class="mt-3">
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
            
            <div class="mt-3">
                <a href="{% url 'frequencias:editar_notificacao' notificacao.id %}" class="btn btn-warning">
                    <i class="fas fa-edit"></i> Editar Notificação
                </a>
            </div>
        </div>
    </div>
    
    <!-- Formulário de envio -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Enviar Notificação</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="enviar_copia" name="enviar_copia">
                    <label class="form-check-label" for="enviar_copia">
                        Enviar cópia para mim
                    </label>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="marcar_acompanhamento" name="marcar_acompanhamento" checked>
                    <label class="form-check-label" for="marcar_acompanhamento">
                        Marcar carência como "Em Acompanhamento"
                    </label>
                </div>
                
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> A notificação será enviada para o email <strong>{{ notificacao.carencia.aluno.email }}</strong>. 
                    Certifique-se de que o endereço está correto.
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_notificacao' notificacao.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-paper-plane"></i> Enviar Notificação
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    {% endif %}
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\estatisticas_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Estatísticas de Frequência</h1>
   
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
   
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="aluno" class="form-label">Aluno</label>
                    <select name="aluno" id="aluno" class="form-select">
                        <option value="">Todos</option>
                        {% for aluno in alunos %}
                            <option value="{{ aluno.id }}" {% if aluno_id == aluno.id|stringformat:"s" %}selected{% endif %}>{{ aluno.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select name="turma" id="turma" class="form-select">
                        <option value="">Todas</option>
                        {% for turma in turmas %}
                            <option value="{{ turma.id }}" {% if turma_id == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.id }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ data_fim }}">
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                    <a href="{% url 'estatisticas_frequencia' %}" class="btn btn-secondary">Limpar Filtros</a>
                </div>
            </form>
        </div>
    </div>
   
    <!-- Resumo Estatístico -->
    <div class="row">
        <div class="col-md-4">
            <div class="card text-white bg-primary mb-4">
                <div class="card-header">Total de Registros</div>
                <div class="card-body">
                    <h5 class="card-title">{{ total }}</h5>
                    <p class="card-text">registros de frequência</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-success mb-4">
                <div class="card-header">Presenças</div>
                <div class="card-body">
                    <h5 class="card-title">{{ presentes }}</h5>
                    <p class="card-text">alunos presentes ({{ taxa_presenca|floatformat:2 }}%)</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-danger mb-4">
                <div class="card-header">Ausências</div>
                <div class="card-body">
                    <h5 class="card-title">{{ ausentes }}</h5>
                    <p class="card-text">alunos ausentes ({{ 100|sub:taxa_presenca|floatformat:2 }}%)</p>
                </div>
            </div>
        </div>
    </div>
   
    <!-- Gráfico (pode ser implementado com Chart.js) -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Gráfico de Frequência</h5>
        </div>
        <div class="card-body">
            <canvas id="graficoFrequencia" width="400" height="200"></canvas>
        </div>
    </div>
   
    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
        <a href="{% url 'listar_frequencias' %}" class="btn btn-secondary">Voltar para Lista</a>
    </div>
</div>

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        var ctx = document.getElementById('graficoFrequencia').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Presentes', 'Ausentes'],
                datasets: [{
                    label: 'Frequência',
                    data: [{{ presentes }}, {{ ausentes }}],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Distribuição de Frequência'
                    }
                }
            }
        });
    });
</script>
{% endblock %}
{% endblock %}




### Arquivo: frequencias\templates\frequencias\excluir_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Registro de Frequência</h1>
  
    <div class="alert alert-danger">
      <p>Tem certeza que deseja excluir o registro de frequência de <strong>{{ frequencia.aluno.nome }}</strong> na atividade <strong>{{ frequencia.atividade.nome }}</strong> do dia <strong>{{ frequencia.data|date:"d/m/Y" }}</strong>?</p>
    </div>
  
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Sim, excluir</button>
      <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\excluir_frequencia_mensal.html

html
{% extends 'base.html' %}

{% block title %}Excluir Frequência Mensal{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">
                    <h4 class="mb-0">Confirmar Exclusão</h4>
                </div>
                <div class="card-body">
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Você está prestes a excluir a seguinte frequência mensal:
                    </div>
                    
                    <div class="card mb-3">
                        <div class="card-body">
                            <p><strong>Turma:</strong> {{ frequencia.turma.nome }}</p>
                            <p><strong>Período:</strong> {{ frequencia.get_mes_display }}/{{ frequencia.ano }}</p>
                            <p><strong>Percentual Mínimo:</strong> {{ frequencia.percentual_minimo }}%</p>
                            <p><strong>Alunos em Carência:</strong> {{ frequencia.carencias.count }}</p>
                        </div>
                    </div>
                    
                    <p class="text-danger">Esta ação não pode ser desfeita e também excluirá todas as carências associadas. Deseja continuar?</p>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-danger">
                                <i class="fas fa-trash"></i> Confirmar Exclusão
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\filtro_painel_frequencias.html

html
{% extends 'base.html' %}

{% block title %}Painel de Frequências - Filtros{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Painel de Frequências</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Selecione a Turma e o Período</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="row mb-3">
                    <div class="col-md-12">
                        <label for="{{ form.turma.id_for_label }}" class="form-label">{{ form.turma.label }}</label>
                        {{ form.turma }}
                        {% if form.turma.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.turma.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-3">
                        <label for="{{ form.mes_inicio.id_for_label }}" class="form-label">{{ form.mes_inicio.label }}</label>
                        {{ form.mes_inicio }}
                        {% if form.mes_inicio.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.mes_inicio.errors }}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-3">
                        <label for="{{ form.ano_inicio.id_for_label }}" class="form-label">{{ form.ano_inicio.label }}</label>
                        {{ form.ano_inicio }}
                        {% if form.ano_inicio.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.ano_inicio.errors }}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-3">
                        <label for="{{ form.mes_fim.id_for_label }}" class="form-label">{{ form.mes_fim.label }}</label>
                        {{ form.mes_fim }}
                        {% if form.mes_fim.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.mes_fim.errors }}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-3">
                        <label for="{{ form.ano_fim.id_for_label }}" class="form-label">{{ form.ano_fim.label }}</label>
                        {{ form.ano_fim }}
                        {% if form.ano_fim.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.ano_fim.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="text-end">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-search"></i> Gerar Relatório
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Validar que a data final é posterior à data inicial
        const form = document.querySelector('form');
        form.addEventListener('submit', function(e) {
            const mesInicio = parseInt(document.getElementById('id_mes_inicio').value);
            const anoInicio = parseInt(document.getElementById('id_ano_inicio').value);
            const mesFim = parseInt(document.getElementById('id_mes_fim').value);
            const anoFim = parseInt(document.getElementById('id_ano_fim').value);
            
            const dataInicio = new Date(anoInicio, mesInicio - 1, 1);
            const dataFim = new Date(anoFim, mesFim - 1, 1);
            
            if (dataFim < dataInicio) {
                e.preventDefault();
                alert('A data final deve ser posterior à data inicial.');
            }
        });
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\formulario_frequencia_mensal.html

html
{% extends 'base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">{{ titulo }}</h4>
                </div>
                <div class="card-body">
                    <form method="post" novalidate>
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                        <div class="alert alert-danger">
                            {% for error in form.non_field_errors %}
                            <p>{{ error }}</p>
                            {% endfor %}
                        </div>
                        {% endif %}
                        
                        <div class="mb-3">
                            <label for="{{ form.turma.id_for_label }}" class="form-label">{{ form.turma.label }}</label>
                            {{ form.turma }}
                            {% if form.turma.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.turma.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.turma.help_text %}
                            <div class="form-text">{{ form.turma.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.mes.id_for_label }}" class="form-label">{{ form.mes.label }}</label>
                                    {{ form.mes }}
                                    {% if form.mes.errors %}
                                    <div class="invalid-feedback d-block">
                                        {% for error in form.mes.errors %}
                                        {{ error }}
                                        {% endfor %}
                                    </div>
                                    {% endif %}
                                    {% if form.mes.help_text %}
                                    <div class="form-text">{{ form.mes.help_text }}</div>
                                    {% endif %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.ano.id_for_label }}" class="form-label">{{ form.ano.label }}</label>
                                    {{ form.ano }}
                                    {% if form.ano.errors %}
                                    <div class="invalid-feedback d-block">
                                        {% for error in form.ano.errors %}
                                        {{ error }}
                                        {% endfor %}
                                    </div>
                                    {% endif %}
                                    {% if form.ano.help_text %}
                                    <div class="form-text">{{ form.ano.help_text }}</div>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.percentual_minimo.id_for_label }}" class="form-label">
                                {{ form.percentual_minimo.label }}
                            </label>
                            <div class="input-group">
                                {{ form.percentual_minimo }}
                                <span class="input-group-text">%</span>
                            </div>
                            {% if form.percentual_minimo.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.percentual_minimo.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.percentual_minimo.help_text %}
                            <div class="form-text">{{ form.percentual_minimo.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex justify-content-between mt-4">
                            <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
                                <i class="fas fa-arrow-left"></i> Voltar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Salvar
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        $('.select2').select2({
            theme: 'bootstrap-5',
            width: '100%'
        });
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\gerar_frequencia_mensal.html

html
{% extends 'base.html' %}

{% block title %}Gerar Frequência Mensal{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Gerar Frequência Mensal</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Selecione a Turma e o Período</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="row mb-3">
                    <div class="col-md-12">
                        <label for="{{ form.turma.id_for_label }}" class="form-label">{{ form.turma.label }}</label>
                        {{ form.turma }}
                        {% if form.turma.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.turma.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="{{ form.mes.id_for_label }}" class="form-label">{{ form.mes.label }}</label>
                        {{ form.mes }}
                        {% if form.mes.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.mes.errors }}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-4">
                        <label for="{{ form.ano.id_for_label }}" class="form-label">{{ form.ano.label }}</label>
                        {{ form.ano }}
                        {% if form.ano.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.ano.errors }}
                            </div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-4">
                        <label for="{{ form.percentual_minimo.id_for_label }}" class="form-label">{{ form.percentual_minimo.label }}</label>
                        {{ form.percentual_minimo }}
                        {% if form.percentual_minimo.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.percentual_minimo.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Esta operação irá gerar ou atualizar o registro de frequência mensal para a turma e período selecionados. Todas as presenças registradas no período serão consideradas no cálculo.
                </div>
                
                <div class="text-end">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-calculator"></i> Gerar Frequência
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\gerenciar_carencias.html

html
{% extends 'base.html' %}

{% block title %}Gerenciar Carências{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Gerenciar Carências</h1>
        <div>
            <a href="{% url 'frequencias:detalhar_frequencia_mensal' frequencia.id %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
        </div>
    </div>
    
    <!-- Informações da frequência -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações da Frequência</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <p><strong>Turma:</strong> {{ frequencia.turma.nome }}</p>
                </div>
                <div class="col-md-4">
                    <p><strong>Mês/Ano:</strong> {{ frequencia.get_mes_display }}/{{ frequencia.ano }}</p>
                </div>
                <div class="col-md-4">
                    <p><strong>Percentual Mínimo:</strong> {{ frequencia.percentual_minimo }}%</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Lista de alunos com carência -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Alunos com Carência</h5>
        </div>
        <div class="card-body">
            {% if carencias %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Aluno</th>
                                <th class="text-center">Presenças</th>
                                <th class="text-center">Percentual</th>
                                <th class="text-center">Carências</th>
                                <th class="text-center">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for carencia in carencias %}
                                <tr>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {% if carencia.aluno.foto %}
                                                <img src="{{ carencia.aluno.foto.url }}" alt="Foto de {{ carencia.aluno.nome }}" 
                                                    class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                                            {% else %}
                                                <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center me-2" 
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
                                    <td class="text-center">
                                        {{ carencia.total_presencas }}/{{ carencia.total_atividades }}
                                    </td>
                                    <td class="text-center">
                                        {{ carencia.percentual_presenca|floatformat:1 }}%
                                    </td>
                                    <td class="text-center">
                                        <span class="badge bg-danger">{{ carencia.numero_carencias }}</span>
                                    </td>
                                    <td class="text-center">
                                        <form method="post" action="{% url 'frequencias:atualizar_carencia' carencia.id %}" class="d-inline">
                                            {% csrf_token %}
                                            <input type="hidden" name="liberado" value="true">
                                            <button type="submit" class="btn btn-success btn-sm">
                                                <i class="fas fa-check"></i> Liberar
                                            </button>
                                        </form>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-success">
                    <i class="fas fa-check-circle me-2"></i> Não há alunos com carência nesta frequência.
                </div>
            {% endif %}
        </div>
        <div class="card-footer">
            <a href="{% url 'frequencias:detalhar_frequencia_mensal' frequencia.id %}" class="btn btn-secondary">
                Voltar
            </a>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\historico_frequencia.html

html
{% extends 'base.html' %}

{% block title %}Histórico de Frequência - {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Histórico de Frequência</h1>
        <div>
            <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-secondary me-2">
                <i cla                        if (data.turmas) {
                    data.turmas.forEach(turma => {
                        const option = document.createElement('option');
                        option.value = turma.id;
                        option.textContent = turma.nome;
                        turmaSelect.appendChild(option);
                    });
                }
            })
            .catch(error => console.error('Erro ao buscar turmas:', error));
    }
});
});
</script>
{% endblock %}
{% endblock %}
ss="fas fa-user"></i> Perfil do Aluno
            </a>
            <a href="{% url 'frequencias:exportar_historico' aluno.cpf %}" class="btn btn-success">
                <i class="fas fa-download"></i> Exportar
            </a>
        </div>
    </div>
    
    <!-- Informações do aluno -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="d-flex align-items-center">
                        {% if aluno.foto %}
                        <img src="{{ aluno.foto.url }}" alt="{{ aluno.nome }}" 
                             class="rounded-circle me-3" width="80" height="80" style="object-fit: cover;">
                        {% else %}
                        <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                             style="width: 80px; height: 80px; color: white; font-size: 2rem;">
                            {{ aluno.nome|first|upper }}
                        </div>
                        {% endif %}
                        <div>
                            <h4 class="mb-1">{{ aluno.nome }}</h4>
                            <p class="text-muted mb-0">{{ aluno.email }}</p>
                            <p class="mb-0">CPF: {{ aluno.cpf }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Situação:</strong> 
                                {% if aluno.situacao == 'ATIVO' %}
                                <span class="badge bg-success">Ativo</span>
                                {% elif aluno.situacao == 'AFASTADO' %}
                                <span class="badge bg-warning">Afastado</span>
                                {% elif aluno.situacao == 'EXCLUIDO' %}
                                <span class="badge bg-danger">Excluído</span>
                                {% else %}
                                <span class="badge bg-secondary">{{ aluno.get_situacao_display }}</span>
                                {% endif %}
                            </p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Nº Iniciático:</strong> {{ aluno.numero_iniciatico|default:"N/A" }}</p>
                        </div>
                    </div>
                    <p><strong>Média de Frequência Geral:</strong> 
                        <span class="badge {% if media_geral < 75 %}bg-danger{% elif media_geral < 85 %}bg-warning{% else %}bg-success{% endif %} p-2">
                            {{ media_geral|floatformat:1 }}%
                        </span>
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-4">
                    <label for="curso" class="form-label">Curso</label>
                    <select class="form-select" id="curso" name="curso">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                        <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == filtros.curso %}selected{% endif %}>
                            {{ curso.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-4">
                    <label for="turma" class="form-label">Turma</label>
                    <select class="form-select" id="turma" name="turma">
                        <option value="">Todas as turmas</option>
                        {% for turma in turmas %}
                        <option value="{{ turma.id }}" {% if turma.id|stringformat:"s" == filtros.turma %}selected{% endif %}>
                            {{ turma.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-4">
                    <label for="periodo" class="form-label">Período</label>
                    <select class="form-select" id="periodo" name="periodo">
                        <option value="">Todos os períodos</option>
                        {% for ano in anos %}
                            <optgroup label="{{ ano }}">
                                {% for mes in meses %}
                                <option value="{{ ano }}-{{ mes.0 }}" 
                                        {% if filtros.periodo == ano|stringformat:"s"|add:"-"|add:mes.0 %}selected{% endif %}>
                                    {{ mes.1 }}/{{ ano }}
                                </option>
                                {% endfor %}
                            </optgroup>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'frequencias:historico_frequencia' aluno.cpf %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Gráfico de frequência -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Evolução da Frequência</h5>
        </div>
        <div class="card-body">
            <canvas id="graficoFrequencia" height="200"></canvas>
        </div>
    </div>
    
    <!-- Tabela de frequências -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Registros de Frequência</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Curso</th>
                            <th>Turma</th>
                            <th>Período</th>
                            <th>Presenças</th>
                            <th>Faltas</th>
                            <th>Total Aulas</th>
                            <th>% Presença</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for registro in registros %}
                        <tr>
                            <td>{{ registro.turma.curso.nome }}</td>
                            <td>{{ registro.turma.nome }}</td>
                            <td>{{ registro.get_mes_display }}/{{ registro.ano }}</td>
                            <td>{{ registro.presencas }}</td>
                            <td>{{ registro.faltas }}</td>
                            <td>{{ registro.total_aulas }}</td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar {% if registro.percentual_presenca < 75 %}bg-danger{% elif registro.percentual_presenca < 85 %}bg-warning{% else %}bg-success{% endif %}" 
                                         role="progressbar" style="width: {{ registro.percentual_presenca }}%;" 
                                         aria-valuenow="{{ registro.percentual_presenca }}" aria-valuemin="0" aria-valuemax="100">
                                        {{ registro.percentual_presenca|floatformat:1 }}%
                                    </div>
                                </div>
                            </td>
                            <td>
                                {% if registro.percentual_presenca < 75 %}
                                    {% if registro.carencia %}
                                        {% if registro.carencia.status == 'PENDENTE' %}
                                        <span class="badge bg-danger">Carência Pendente</span>
                                        {% elif registro.carencia.status == 'EM_ACOMPANHAMENTO' %}
                                        <span class="badge bg-warning text-dark">Em Acompanhamento</span>
                                        {% elif registro.carencia.status == 'RESOLVIDO' %}
                                        <span class="badge bg-success">Carência Resolvida</span>
                                        {% endif %}
                                    {% else %}
                                    <span class="badge bg-danger">Carência</span>
                                    {% endif %}
                                {% else %}
                                <span class="badge bg-success">Regular</span>
                                {% endif %}
                            </td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'frequencias:detalhar_frequencia_mensal' registro.id %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    {% if registro.carencia %}
                                    <a href="{% url 'frequencias:detalhar_carencia' registro.carencia.id %}" class="btn btn-sm btn-warning">
                                        <i class="fas fa-exclamation-triangle"></i>
                                    </a>
                                    {% endif %}
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="9" class="text-center py-3">
                                <p class="mb-0">Nenhum registro de frequência encontrado com os filtros selecionados.</p>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
            <div>
                <p class="mb-0">Exibindo {{ registros|length }} de {{ total_registros }} registros</p>
            </div>
            
            {% if registros.has_other_pages %}
            <nav aria-label="Paginação">
                <ul class="pagination mb-0">
                    {% if registros.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ registros.previous_page_number }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}" aria-label="Anterior">
                            <span aria-hidden="true">«</span>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link" aria-hidden="true">«</span>
                    </li>
                    {% endif %}
                    
                    {% for i in registros.paginator.page_range %}
                        {% if registros.number == i %}
                        <li class="page-item active"><span class="page-link">{{ i }}</span></li>
                        {% else %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ i }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}">{{ i }}</a>
                        </li>
                        {% endif %}
                    {% endfor %}
                    
                    {% if registros.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ registros.next_page_number }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}" aria-label="Próxima">
                            <span aria-hidden="true">»</span>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link" aria-hidden="true">»</span>
                    </li>
                    {% endif %}
                </ul>
            </nav>
            {% endif %}
        </div>
    </div>
    
    <!-- Carências -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Histórico de Carências</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Curso</th>
                            <th>Turma</th>
                            <th>Período</th>
                            <th>% Presença</th>
                            <th>Data Identificação</th>
                            <th>Status</th>
                            <th>Notificação</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for carencia in carencias %}
                        <tr>
                            <td>{{ carencia.frequencia_mensal.turma.curso.nome }}</td>
                            <td>{{ carencia.frequencia_mensal.turma.nome }}</td>
                            <td>{{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar bg-danger" role="progressbar" 
                                         style="width: {{ carencia.percentual_presenca }}%;" 
                                         aria-valuenow="{{ carencia.percentual_presenca }}" aria-valuemin="0" aria-valuemax="100">
                                        {{ carencia.percentual_presenca|floatformat:1 }}%
                                    </div>
                                </div>
                            </td>
                            <td>{{ carencia.data_identificacao|date:"d/m/Y" }}</td>
                            <td>
                                {% if carencia.status == 'PENDENTE' %}
                                <span class="badge bg-danger">Pendente</span>
                                {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}
                                <span class="badge bg-warning text-dark">Em Acompanhamento</span>
                                {% elif carencia.status == 'RESOLVIDO' %}
                                <span class="badge bg-success">Resolvido</span>
                                {% endif %}
                            </td>
                            <td>
                                {% if carencia.notificacao %}
                                    {% if carencia.notificacao.status == 'PENDENTE' %}
                                    <span class="badge bg-secondary">Não Enviada</span>
                                    {% elif carencia.notificacao.status == 'ENVIADA' %}
                                    <span class="badge bg-info">Enviada</span>
                                    {% elif carencia.notificacao.status == 'LIDA' %}
                                    <span class="badge bg-primary">Lida</span>
                                    {% elif carencia.notificacao.status == 'RESPONDIDA' %}
                                    <span class="badge bg-success">Respondida</span>
                                    {% endif %}
                                {% else %}
                                <span class="badge bg-secondary">Não Criada</span>
                                {% endif %}
                            </td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    {% if carencia.notificacao %}
                                    <a href="{% url 'frequencias:detalhar_notificacao' carencia.notificacao.id %}" class="btn btn-sm btn-primary">
                                        <i class="fas fa-envelope"></i>
                                    </a>
                                    {% endif %}
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="8" class="text-center py-3">
                                <p class="mb-0">Nenhuma carência encontrada com os filtros selecionados.</p>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de evolução da frequência
        const ctxFrequencia = document.getElementById('graficoFrequencia').getContext('2d');
        new Chart(ctxFrequencia, {
            type: 'line',
            data: {
                labels: {{ periodos_labels|safe }},
                datasets: [{
                    label: 'Percentual de Presença',
                    data: {{ percentuais_presenca|safe }},
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.raw.toFixed(1) + '%';
                            }
                        }
                    },
                    annotation: {
                        annotations: {
                            line1: {
                                type: 'line',
                                yMin: 75,
                                yMax: 75,
                                borderColor: 'rgba(255, 0, 0, 0.5)',
                                borderWidth: 2,
                                borderDash: [6, 6],
                                label: {
                                    content: 'Mínimo (75%)',
                                    enabled: true,
                                    position: 'end'
                                }
                            }
                        }
                    }
                }
            }
        });
        
        // Atualizar turmas quando o curso for alterado
        const cursoSelect = document.getElementById('curso');
        const turmaSelect = document.getElementById('turma');
        
        cursoSelect.addEventListener('change', function() {
            const cursoId = this.value;
            
            // Limpar o select de turmas
            turmaSelect.innerHTML = '<option value="">Todas as turmas</option>';
            
            if (cursoId) {
                // Fazer uma requisição AJAX para buscar as turmas do curso
                fetch(`/frequencias/api/turmas-por-curso/${cursoId}/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.turmas



### Arquivo: frequencias\templates\frequencias\iniciar_acompanhamento.html

html
{% extends 'base.html' %}

{% block title %}Iniciar Acompanhamento de Carência{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Iniciar Acompanhamento de Carência</h1>
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
                    <p><strong>Curso:</strong> {{ carencia.frequencia_mensal.turma.curso.nome }}</p>
                    <p><strong>Turma:</strong> {{ carencia.frequencia_mensal.turma.nome }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Período:</strong> {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</p>
                    <p><strong>Percentual de Presença:</strong> {{ carencia.percentual_presenca }}%</p>
                    <p><strong>Status Atual:</strong> {{ carencia.get_status_display }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Formulário de acompanhamento -->
    <div class="card mb-4">
        <div class="card-header bg-warning text-dark">
            <h5 class="mb-0">Iniciar Acompanhamento</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="observacoes" class="form-label">Observações</label>
                    <textarea class="form-control" id="observacoes" name="observacoes" rows="5" required></textarea>
                    <div class="form-text">Descreva as ações que serão tomadas para acompanhar esta carência.</div>
                </div>
                
                <div class="mb-3">
                    <label for="prazo_resolucao" class="form-label">Prazo Estimado para Resolução</label>
                    <input type="date" class="form-control" id="prazo_resolucao" name="prazo_resolucao" 
                           min="{{ data_atual|date:'Y-m-d' }}" required>
                    <div class="form-text">Defina um prazo para a resolução desta carência.</div>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="criar_notificacao" name="criar_notificacao" checked>
                    <label class="form-check-label" for="criar_notificacao">
                        Criar notificação para o aluno
                    </label>
                </div>
                
                <div id="notificacao_fields" class="border p-3 rounded mb-3">
                    <h6>Dados da Notificação</h6>
                    
                    <div class="mb-3">
                        <label for="assunto" class="form-label">Assunto</label>
                        <input type="text" class="form-control" id="assunto" name="assunto" 
                               value="Notificação de Carência - {{ carencia.frequencia_mensal.turma.curso.nome }}">
                    </div>
                    
                    <div class="mb-3">
                        <label for="mensagem" class="form-label">Mensagem</label>
                        <textarea class="form-control" id="mensagem" name="mensagem" rows="5">Prezado(a) {{ carencia.aluno.nome }},

Identificamos que sua frequência no curso {{ carencia.frequencia_mensal.turma.curso.nome }}, turma {{ carencia.frequencia_mensal.turma.nome }}, no período de {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }} está abaixo do mínimo necessário (75%).

Seu percentual atual de presença é de {{ carencia.percentual_presenca }}%.

Por favor, entre em contato com a secretaria para regularizar sua situação.

Atenciosamente,
Equipe OMAUM</textarea>
                    </div>
                    
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="enviar_agora" name="enviar_agora" checked>
                        <label class="form-check-label" for="enviar_agora">
                            Enviar notificação imediatamente
                        </label>
                    </div>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <button type="submit" class="btn btn-warning">
                        <i class="fas fa-clock"></i> Iniciar Acompanhamento
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const criarNotificacaoCheckbox = document.getElementById('criar_notificacao');
        const notificacaoFields = document.getElementById('notificacao_fields');
        
        criarNotificacaoCheckbox.addEventListener('change', function() {
            notificacaoFields.style.display = this.checked ? 'block' : 'none';
        });
        
        // Definir prazo padrão para 7 dias a partir de hoje
        const prazoInput = document.getElementById('prazo_resolucao');
        if (prazoInput) {
            const hoje = new Date();
            const prazo = new Date(hoje);
            prazo.setDate(hoje.getDate() + 7);
            
            const ano = prazo.getFullYear();
            const mes = String(prazo.getMonth() + 1).padStart(2, '0');
            const dia = String(prazo.getDate()).padStart(2, '0');
            
            prazoInput.value = `${ano}-${mes}-${dia}`;
        }
    });
</script>
{% endblock %}


'''