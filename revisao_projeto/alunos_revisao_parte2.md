'''
# Revisão da Funcionalidade: alunos

## Arquivos forms.py:


### Arquivo: alunos\templates\alunos\formulario_aluno.html

html
{% extends 'base.html' %}

{% block title %}{% if aluno.cpf %}Editar{% else %}Novo{% endif %} Aluno{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if aluno and aluno.cpf %}Editar{% else %}Novo{% endif %} Aluno</h1>
        <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <!-- Adicionar ID ao formulário para facilitar a seleção no JavaScript -->
    <form method="post" enctype="multipart/form-data" id="form-aluno" novalidate>
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <!-- Adicionar logo após a abertura da tag <form> -->
        <div class="alert alert-info">
            <p><strong>Atenção:</strong> Preencha todos os campos obrigatórios e certifique-se de que a data de nascimento está preenchida.</p>
            <p>Os campos com formato específico (CPF, CEP, telefones) serão automaticamente ajustados ao salvar.</p>
        </div>
        
        <div class="card mb-4 border-primary">
            <div class="card-header bg-primary text-white">
                <h5>Dados Pessoais</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="row">
                            <div class="col-md-6">
                                {% include 'includes/form_field.html' with field=form.cpf %}
                                {% include 'includes/form_field.html' with field=form.nome %}
                                {% include 'includes/form_field.html' with field=form.data_nascimento %}
                                {% include 'includes/form_field.html' with field=form.hora_nascimento %}
                            </div>
                            <div class="col-md-6">
                                {% include 'includes/form_field.html' with field=form.email %}
                                {% include 'includes/form_field.html' with field=form.sexo %}
                                {% include 'includes/form_field.html' with field=form.situacao %}
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <!-- Moldura tracejada azul brilhante sem cabeçalho -->
                        <div class="border rounded p-3 mb-3 text-center" 
                             style="border-style: dashed !important; 
                                    border-color: #007bff !important; 
                                    border-width: 2px !important;
                                    width: 200px;  /* Largura fixa para o contêiner */
                                    height: 200px; /* Altura fixa para o contêiner */
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: center;
                                    overflow: hidden;
                                    margin: 0 auto;">
                            {% if aluno.foto %}
                                <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" 
                                     style="max-width: 180px;
                                            max-height: 180px;
                                            width: auto;
                                            height: auto;
                                            object-fit: contain;
                                            display: block;">
                            {% else %}
                                <div class="text-muted">Sem foto</div>
                            {% endif %}
                        </div>
                        
                        <!-- Campo de upload separado da moldura -->
                        <div class="form-group">
                            {{ form.foto }}
                            {% if form.foto.help_text %}
                                <small class="form-text text-muted">{{ form.foto.help_text }}</small>
                            {% endif %}
                            {% for error in form.foto.errors %}
                                <div class="alert alert-danger">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-info">
            <div class="card-header bg-info text-white">
                <h5>Dados Iniciáticos</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.numero_iniciatico %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome_iniciatico %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-secondary">
            <div class="card-header bg-secondary text-white">
                <h5>Nacionalidade e Naturalidade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nacionalidade %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.naturalidade %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-success">
            <div class="card-header bg-success text-white">
                <h5>Endereço</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        {% include 'includes/form_field.html' with field=form.rua %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.numero_imovel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.complemento %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.bairro %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.cep %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-8">
                        {% include 'includes/form_field.html' with field=form.cidade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.estado %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-warning">
            <div class="card-header bg-warning text-dark">
                <h5>Contatos de Emergência</h5>
            </div>
            <div class="card-body">
                <h6>Primeiro Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.nome_primeiro_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.celular_primeiro_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_relacionamento_primeiro_contato %}
                    </div>
                </div>
                
                <h6 class="mt-3">Segundo Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.nome_segundo_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.celular_segundo_contato %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_relacionamento_segundo_contato %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-danger">
            <div class="card-header bg-danger text-white">
                <h5>Informações Médicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.tipo_sanguineo %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.fator_rh %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.convenio_medico %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.hospital %}
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.alergias %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.condicoes_medicas_gerais %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary" id="btn-salvar">
                {% if aluno and aluno.cpf %}Atualizar{% else %}Cadastrar{% endif %} Aluno
            </button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const fotoInput = document.getElementById('id_foto');
        const fotoContainer = document.querySelector('.border.rounded.p-3.mb-3.text-center');
        
        if (fotoInput && fotoContainer) {
            fotoInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    // Limpar o conteúdo atual do container
                    fotoContainer.innerHTML = '';
                    
                    // Limpar mensagens de erro relacionadas à foto
                    const errorMessages = fotoInput.parentElement.querySelectorAll('.alert.alert-danger');
                    errorMessages.forEach(function(errorMsg) {
                        errorMsg.style.display = 'none';
                    });
                    
                    // Criar a imagem de preview
                    const preview = document.createElement('img');
                    preview.style.maxWidth = '180px';
                    preview.style.maxHeight = '180px';
                    preview.style.width = 'auto';
                    preview.style.height = 'auto';
                    preview.style.objectFit = 'contain';
                    preview.style.display = 'block';
                    
                    // Configurar o leitor de arquivo
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                        preview.alt = 'Preview da foto';
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                    
                    // Adicionar a imagem ao container
                    fotoContainer.appendChild(preview);
                    
                    // Adicionar uma mensagem de sucesso temporária
                    const successMsg = document.createElement('div');
                    successMsg.className = 'alert alert-success mt-2';
                    successMsg.textContent = 'Nova imagem selecionada com sucesso!';
                    fotoInput.parentElement.appendChild(successMsg);
                    
                    // Remover a mensagem de sucesso após 3 segundos
                    setTimeout(function() {
                        successMsg.remove();
                    }, 3000);
                }
            });
        }
        
        // Verificar se há mensagem "Atualmente:" e ajustar o layout
        const currentImageText = document.querySelector('.form-group a');
        if (currentImageText) {
            const clearCheckbox = document.querySelector('input[name="foto-clear"]');
            const clearLabel = document.querySelector('label[for="foto-clear_id"]');
            
            if (clearCheckbox && clearLabel) {
                // Melhorar o layout da opção de limpar
                const clearContainer = document.createElement('div');
                clearContainer.className = 'form-check mt-2';
                
                clearCheckbox.className = 'form-check-input';
                clearLabel.className = 'form-check-label';
                
                clearContainer.appendChild(clearCheckbox);
                clearContainer.appendChild(clearLabel);
                
                // Substituir o texto "Atualmente:" por um layout mais limpo
                const currentImageContainer = document.createElement('div');
                currentImageContainer.className = 'mb-2';
                currentImageContainer.innerHTML = '<strong>Imagem atual:</strong> ';
                currentImageContainer.appendChild(currentImageText.cloneNode(true));
                
                // Substituir os elementos originais
                const parentElement = clearCheckbox.parentElement;
                parentElement.innerHTML = '';
                parentElement.appendChild(currentImageContainer);
                parentElement.appendChild(clearContainer);
            }
        }
    });
</script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('form-aluno');
        
        form.addEventListener('submit', function(e) {
            // Remove masks before submission
            const cpfField = document.getElementById('id_cpf');
            const cepField = document.getElementById('id_cep');
            const celular1Field = document.getElementById('id_celular_primeiro_contato');
            const celular2Field = document.getElementById('id_celular_segundo_contato');
            
            if (cpfField) cpfField.value = cpfField.value.replace(/\D/g, '');
            if (cepField) cepField.value = cepField.value.replace(/\D/g, '');
            if (celular1Field) celular1Field.value = celular1Field.value.replace(/\D/g, '');
            if (celular2Field) celular2Field.value = celular2Field.value.replace(/\D/g, '');
            
            // Continue with form submission
            return true;
        });
    });
</script>
{% endblock %}




### Arquivo: alunos\templates\alunos\importar_alunos.html

html
{% extends 'base.html' %}

{% block title %}Importar Alunos{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Importar Alunos</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="mb-3">Faça upload de um arquivo CSV contendo os dados dos alunos.</p>
            
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="csv_file" class="form-label">Arquivo CSV</label>
                    <input type="file" name="csv_file" id="csv_file" class="form-control" accept=".csv" required>
                    <div class="form-text">O arquivo deve ter cabeçalhos: CPF, Nome, Email, etc.</div>
                </div>
                
                <div class="d-flex">
                    <button type="submit" class="btn btn-primary me-2">Importar</button>
                    <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'alunos:listar_alunos' %}" class="btn btn-link">Voltar para a lista de alunos</a>
    </div>
</div>
{% endblock %}



### Arquivo: alunos\templates\alunos\listar_alunos.html

html
{% extends 'base.html' %}

{% block title %}Lista de Alunos{% endblock %}

{% block extra_css %}
<style>
    .btn-group-responsive {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    @media (max-width: 768px) {
        .action-buttons {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        
        .btn-responsive {
            width: 100%;
            margin-bottom: 0.25rem;
        }
    }
    
    .table-responsive {
        overflow-x: auto;
    }
    
    .table th, .table td {
        white-space: nowrap;
    }
    
    .aluno-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .aluno-avatar {
        flex-shrink: 0;
    }
    
    .aluno-nome {
        font-weight: 500;
    }
    
    .dropdown-menu-actions {
        min-width: 8rem;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-3">
        <h1 class="mb-3 mb-md-0">Lista de Alunos</h1>
        
        <!-- Botões agrupados com dropdown em telas menores -->
        <div class="btn-group-responsive">
            <a href="javascript:history.back()" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            
            <a href="{% url 'alunos:criar_aluno' %}" class="btn btn-primary">
                <i class="fas fa-plus"></i> Novo Aluno
            </a>
            
            <!-- Dropdown para ações secundárias em telas menores -->
            <div class="d-none d-md-block">
                <a href="{% url 'alunos:exportar_alunos' %}" class="btn btn-success">
                    <i class="fas fa-file-export"></i> Exportar CSV
                </a>
                
                <a href="{% url 'alunos:importar_alunos' %}" class="btn btn-info">
                    <i class="fas fa-file-import"></i> Importar CSV
                </a>
                
                <a href="{% url 'alunos:relatorio_alunos' %}" class="btn btn-warning">
                    <i class="fas fa-chart-bar"></i> Relatório
                </a>
                
                <a href="{% url 'alunos:dashboard' %}" class="btn btn-dark">
                    <i class="fas fa-tachometer-alt"></i> Dashboard
                </a>
            </div>
            
            <!-- Dropdown para telas menores -->
            <div class="dropdown d-md-none">
                <button class="btn btn-outline-primary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas fa-ellipsis-h"></i> Mais ações
                </button>
                <ul class="dropdown-menu dropdown-menu-end dropdown-menu-actions" aria-labelledby="dropdownMenuButton">
                    <li><a class="dropdown-item" href="{% url 'alunos:exportar_alunos' %}">
                        <i class="fas fa-file-export"></i> Exportar CSV
                    </a></li>
                    <li><a class="dropdown-item" href="{% url 'alunos:importar_alunos' %}">
                        <i class="fas fa-file-import"></i> Importar CSV
                    </a></li>
                    <li><a class="dropdown-item" href="{% url 'alunos:relatorio_alunos' %}">
                        <i class="fas fa-chart-bar"></i> Relatório
                    </a></li>
                    <li><a class="dropdown-item" href="{% url 'alunos:dashboard' %}">
                        <i class="fas fa-tachometer-alt"></i> Dashboard
                    </a></li>
                    <li><a class="dropdown-item" href="{% url 'alunos:diagnostico_instrutores' %}">
                        <i class="fas fa-user-check"></i> Diagnóstico Instrutores
                    </a></li>
                </ul>
            </div>
        </div>
    </div>
    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6 col-lg-7">
                    <div class="input-group">
                        <input type="text" name="q" class="form-control" placeholder="Buscar por nome, CPF ou email..." value="{{ query }}">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-search"></i> Buscar
                        </button>
                    </div>
                </div>
                <div class="col-md-4 col-lg-3">
                    <select name="curso" class="form-select" title="Selecione um curso" aria-label="Selecione um curso">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                            <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == curso_selecionado %}selected{% endif %}>{{ curso.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2 col-lg-2">
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                </div>
            </form>
        </div>
        <div class="card-body">
            {% if error_message %}
            <div class="alert alert-danger">
                {{ error_message }}
            </div>
            {% endif %}
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead class="table-light">
                        <tr>
                            <th>Nome</th>
                            <th>CPF</th>
                            <th>Nº Iniciático</th>
                            <th>Email</th>
                            <th class="text-center">Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in alunos %}
                            <tr>
                                <td>
                                    <div class="aluno-info">
                                        {% if aluno.foto %}
                                            <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" 
                                                 class="rounded-circle aluno-avatar" width="40" height="40" 
                                                 style="object-fit: cover;">
                                        {% else %}
                                            <div class="rounded-circle bg-secondary aluno-avatar d-flex align-items-center justify-content-center" 
                                                 style="width: 40px; height: 40px; color: white;">
                                                {{ aluno.nome|first|upper }}
                                            </div>
                                        {% endif %}
                                        <span class="aluno-nome">{{ aluno.nome }}</span>
                                    </div>
                                </td>
                                <td>{{ aluno.cpf }}</td>
                                <td>{{ aluno.numero_iniciatico|default:"N/A" }}</td>
                                <td>{{ aluno.email }}</td>
                                <td>
                                    {% if aluno.cpf %}
                                        <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-sm btn-info" title="Ver detalhes completos do aluno">Detalhes</a>
                                        <a href="{% url 'alunos:editar_aluno' aluno.cpf %}" class="btn btn-sm btn-warning" title="Editar informações do aluno">Editar</a>
                                        <a href="{% url 'alunos:excluir_aluno' aluno.cpf %}" class="btn btn-sm btn-danger" title="Excluir este aluno">Excluir</a>
                                    {% else %}
                                        <span class="text-muted">CPF não disponível</span>
                                    {% endif %}
                                </td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="5" class="text-center">
                                    <p class="my-3">Nenhum aluno cadastrado.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer d-flex flex-column flex-md-row justify-content-between align-items-center">
            <p class="text-muted mb-md-0">Total: {{ alunos.count|default:"0" }} aluno(s)</p>
            {% if page_obj.has_other_pages %}
                <nav aria-label="Paginação">
                    <ul class="pagination justify-content-center mb-0">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}&curso={{ curso_selecionado }}">Anterior</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Anterior</span>
                            </li>
                        {% endif %}

                        {% for num in page_obj.paginator.page_range %}
                            {% if page_obj.number == num %}
                                <li class="page-item active">
                                    <span class="page-link">{{ num }}</span>
                                </li>
                            {% else %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ num }}&q={{ query }}&curso={{ curso_selecionado }}">{{ num }}</a>
                                </li>
                            {% endif %}
                        {% endfor %}

                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}&curso={{ curso_selecionado }}">Próxima</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Próxima</span>
                            </li>
                        {% endif %}
                    </ul>
                </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: alunos\templates\alunos\registro.html

html
{% extends 'base.html' %}

{% block content %}
<h2>Registro</h2>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Registrar</button>
</form>

<a href="javascript:history.back()" class="back-button">Voltar</a>

<style>
    .back-button {
        margin-top: 20px;
        display: inline-block;
        padding: 10px 20px;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        text-decoration: none;
        color: #333;
        border-radius: 5px;
    }
</style>
{% endblock %}




### Arquivo: alunos\templates\alunos\relatorio_alunos.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Alunos{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Relatório de Alunos</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="card-title">Estatísticas Gerais</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Total de Alunos</h5>
                            <p class="card-text display-4">{{ total_alunos }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Masculino</h5>
                            <p class="card-text display-4">{{ total_masculino }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Feminino</h5>
                            <p class="card-text display-4">{{ total_feminino }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Outros</h5>
                            <p class="card-text display-4">{{ total_outros }}</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Idade Média</h5>
                            <p class="card-text display-4">{{ idade_media|floatformat:1 }} anos</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}



'''