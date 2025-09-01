document.addEventListener('DOMContentLoaded', function() {
    // ========================================================================
    // INICIALIZAÇÃO GERAL E MANIPULADORES DE EVENTOS
    // ========================================================================

    // Obter URLs e dados do template
    const historicoApiUrl = document.body.dataset.historicoApiUrl;
    const addEventoApiUrl = document.body.dataset.addEventoApiUrl;
    const tiposCodigosApiUrl = document.body.dataset.tiposCodigosApiUrl;
    const codigosPorTipoApiUrl = document.body.dataset.codigosPorTipoApiUrl;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Inicializa os acordeões (collapsibles)
    initializeCollapseToggles();

    // Aplica máscaras de formatação (função de masks.js)
    if (typeof applyDisplayMasks === 'function') {
        applyDisplayMasks();
    } else {
        console.warn('Função applyDisplayMasks() não encontrada. Carregue masks.js');
    }

    // Lógica do histórico paginado
    if (document.getElementById('btn-carregar-historico')) {
        initializeHistoricoPaginado(historicoApiUrl);
    }

    // Lógica do formulário de adicionar evento
    if (document.getElementById('form-adicionar-evento')) {
        initializeAdicionarEventoForm(addEventoApiUrl, tiposCodigosApiUrl, codigosPorTipoApiUrl, csrfToken);
    }
});


// ========================================================================
// SEÇÃO: LÓGICA DOS ACORDEÕES (COLLAPSE)
// ========================================================================

function initializeCollapseToggles() {
    document.querySelectorAll('.collapse-toggle').forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            const chevron = this.querySelector('.chevron');
            // A classe 'collapsed' é gerenciada pelo Bootstrap.
            // O timeout garante que a rotação ocorra após o estado do Bootstrap ser atualizado.
            setTimeout(() => {
                if (toggle.classList.contains('collapsed')) {
                    chevron.style.transform = 'rotate(0deg)';
                } else {
                    chevron.style.transform = 'rotate(90deg)';
                }
            }, 150); // 150ms é um valor seguro para a transição do Bootstrap
        });
    });
}




// ========================================================================
// SEÇÃO: HISTÓRICO INICIÁTICO PAGINADO (AJAX)
// ========================================================================

function initializeHistoricoPaginado(apiUrl) {
    const btnCarregar = document.getElementById('btn-carregar-historico');
    const btnCarregarMais = document.getElementById('btn-carregar-mais-historico');
    const statusEl = document.getElementById('historico-status');
    const tabelaContainer = document.getElementById('historico-tabela-container');
    const tbody = document.getElementById('historico-tbody');
    
    let pagina = 1;
    const pageSize = 25;
    let totalPages = 1;
    let carregando = false;

    function atualizarStatus() {
        statusEl.textContent = `Página ${pagina - 1} de ${totalPages}`;
    }

    function toggleBotoes() {
        if (pagina <= totalPages) {
            btnCarregarMais.classList.remove('d-none');
        } else {
            btnCarregarMais.classList.add('d-none');
        }
    }

    function renderRows(items) {
        const placeholder = document.getElementById('historico-placeholder');
        if (placeholder) {
            placeholder.remove();
        }
        for (const it of items) {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${it.tipo_codigo}</td>
                <td title="${it.descricao}">${it.codigo}</td>
                <td>${new Date(it.data_os).toLocaleDateString('pt-BR')}</td>
                <td title="${it.observacoes}">${(it.observacoes || '-').substring(0, 40)}</td>
            `;
            tbody.appendChild(tr);
        }
    }

    function carregarPagina() {
        if (carregando) return;
        carregando = true;
        statusEl.textContent = 'Carregando...';
        
        const url = `${apiUrl}?page=${pagina}&page_size=${pageSize}`;
        
        fetch(url)
            .then(r => r.json())
            .then(data => {
                if (data.status === 'success') {
                    totalPages = data.total_pages;
                    renderRows(data.results);
                    pagina += 1;
                    atualizarStatus();
                    toggleBotoes();
                } else {
                    statusEl.textContent = 'Erro ao carregar.';
                }
            })
            .catch(() => { statusEl.textContent = 'Falha de rede.'; })
            .finally(() => { carregando = false; });
    }

    btnCarregar.addEventListener('click', function() {
        tabelaContainer.classList.remove('d-none');
        btnCarregar.classList.add('d-none');
        pagina = 1;
        tbody.innerHTML = '<tr id="historico-placeholder"><td colspan="4" class="text-center text-muted">Carregando...</td></tr>';
        carregarPagina();
    });

    btnCarregarMais.addEventListener('click', function() {
        carregarPagina();
    });
}


// ========================================================================
// SEÇÃO: ADICIONAR EVENTO AO HISTÓRICO (FORMULÁRIO AJAX)
// ========================================================================

function initializeAdicionarEventoForm(addEventoApiUrl, tiposCodigosApiUrl, codigosPorTipoApiUrl, csrfToken) {
    const tipoEventoSelect = document.getElementById('tipo_evento');
    const codigoEventoSelect = document.getElementById('codigo_evento');
    const form = document.getElementById('form-adicionar-evento');

    // 1. Carregar os tipos de evento iniciais
    carregarTiposCodigos(tiposCodigosApiUrl);

    // 2. Configurar event listeners para os selects
    tipoEventoSelect.addEventListener('change', function() {
        const tipoId = this.value;
        const tooltipCodigo = document.getElementById('tooltip-codigo-evento');
        
        if (tipoId) {
            carregarCodigosPorTipo(tipoId, codigosPorTipoApiUrl);
            codigoEventoSelect.disabled = false;
            
            const selectedOption = this.options[this.selectedIndex];
            const descricao = selectedOption.getAttribute('data-descricao');
            document.getElementById('tooltip-tipo-evento').textContent = descricao || 'Descrição não disponível';
        } else {
            codigoEventoSelect.innerHTML = '<option value="">Selecione</option>';
            codigoEventoSelect.disabled = true;
            tooltipCodigo.textContent = 'Selecione primeiro o tipo de evento';
        }
    });

    codigoEventoSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const descricao = selectedOption.getAttribute('data-descricao');
        document.getElementById('tooltip-codigo-evento').textContent = descricao || 'Descrição não disponível';
    });

    // 3. Configurar a submissão do formulário via AJAX
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        adicionarEventoHistorico(addEventoApiUrl, csrfToken);
    });
}

function carregarTiposCodigos(tiposCodigosApiUrl) {
    fetch(tiposCodigosApiUrl)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const select = document.getElementById('tipo_evento');
                select.innerHTML = '<option value="">Selecione</option>';
                
                data.tipos.forEach(tipo => {
                    const option = document.createElement('option');
                    option.value = tipo.id;
                    option.textContent = tipo.nome;
                    option.setAttribute('data-descricao', tipo.descricao || '');
                    select.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Erro ao carregar tipos de códigos:', error);
        });
}

function carregarCodigosPorTipo(tipoId, codigosPorTipoApiUrl) {
    fetch(`${codigosPorTipoApiUrl}?tipo_id=${tipoId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const select = document.getElementById('codigo_evento');
                select.innerHTML = '<option value="">Selecione</option>';
                
                data.codigos.forEach(codigo => {
                    const option = document.createElement('option');
                    option.value = codigo.id;
                    option.textContent = codigo.nome;
                    option.setAttribute('data-descricao', codigo.descricao || '');
                    select.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Erro ao carregar códigos:', error);
        });
}

function adicionarEventoHistorico(addEventoApiUrl, csrfToken) {
    const form = document.getElementById('form-adicionar-evento');
    const formData = new FormData(form);
    const data = {
        aluno_id: formData.get('aluno_id'),
        tipo_evento: document.getElementById('tipo_evento').options[document.getElementById('tipo_evento').selectedIndex].text,
        codigo_id: formData.get('codigo_evento'),
        ordem_servico: formData.get('ordem_servico'),
        data_os: formData.get('data_os'),
        data_evento: formData.get('data_evento'),
        observacoes: formData.get('observacoes')
    };
    
    fetch(addEventoApiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            mostrarMensagem('Evento adicionado com sucesso!', 'success');
            form.reset();
            document.getElementById('codigo_evento').disabled = true;
            document.getElementById('tooltip-tipo-evento').textContent = 'Selecione o tipo de evento para ver a descrição';
            document.getElementById('tooltip-codigo-evento').textContent = 'Selecione primeiro o tipo de evento';
            
            // Recarrega a página para mostrar o evento na lista de recentes
            setTimeout(() => location.reload(), 1500);
        } else {
            mostrarMensagem('Erro ao adicionar evento: ' + (data.message || 'Verifique os campos.'), 'error');
        }
    })
    .catch(error => {
        console.error('Erro na requisição AJAX:', error);
        mostrarMensagem('Ocorreu um erro de comunicação com o servidor.', 'error');
    });
}

function mostrarMensagem(mensagem, tipo) {
    // Remove qualquer alerta existente para evitar duplicatas
    const existingAlert = document.querySelector('.alert-dismissible');
    if (existingAlert) {
        existingAlert.remove();
    }

    const alertClass = tipo === 'success' ? 'alert-success' : 'alert-danger';
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    const form = document.getElementById('form-adicionar-evento');
    form.insertAdjacentHTML('beforebegin', alertHtml);
    
    // Auto-remove após 5 segundos
    setTimeout(() => {
        const alert = document.querySelector('.alert-dismissible');
        if (alert) {
            // Usar a API do Bootstrap para um fechamento suave, se disponível
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                alert.remove();
            }
        }
    }, 5000);
}
