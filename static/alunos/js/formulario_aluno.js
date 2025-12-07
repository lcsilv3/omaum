document.addEventListener('DOMContentLoaded', function() {
    // ========================================================================
    // INICIALIZAÇÃO GERAL E ESTILIZAÇÃO
    // ========================================================================

    // Injeta estilos CSS para melhorar a aparência do formset
    injectFormsetStyles();

    // Inicializa os acordeões (collapsibles)
    initializeCollapseToggles();

    // Inicializa a lógica de preview da imagem
    initializeImagePreview();

    // Remove máscaras dos campos antes do submit do formulário (função de masks.js)
    if (typeof addSubmitMaskRemover === 'function') {
        addSubmitMaskRemover('form-aluno');
    } else {
        console.warn('Função addSubmitMaskRemover() não encontrada. Carregue masks.js');
    }

    // ========================================================================
    // LÓGICA DO FORMSET DE HISTÓRICO
    // ========================================================================

    // Inicializa a lógica de adição/remoção de formulários do formset
    initializeHistoricoFormset();

    // ========================================================================
    // LÓGICA DOS SELECTS DINÂMICOS (TIPO -> CÓDIGO)
    // ========================================================================

    // Obter URLs do template
    const URL_TIPOS = document.body.dataset.tiposCodigosApiUrl;
    const URL_CODIGOS_POR_TIPO = document.body.dataset.codigosPorTipoApiUrl;

    // Inicializa a lógica dos selects dinâmicos
    initializeDynamicSelects(URL_TIPOS, URL_CODIGOS_POR_TIPO);
});


// ========================================================================
// SEÇÃO: ESTILOS E UTILITÁRIOS DE UI
// ========================================================================

function injectFormsetStyles() {
    const style = document.createElement('style');
    style.innerHTML = `
        .historico-form .form-label { font-weight: 500; }
        .historico-form .form-text { margin-top: 0.25rem; }
        .historico-row { align-items: stretch !important; }
        .historico-row > [class*='col-'] { display: flex; flex-direction: column; }
        .historico-row .mb-3 { flex: 1 1 auto; display: flex; flex-direction: column; margin-bottom: .5rem !important; }
        .historico-row select[disabled] { background: #e9ecef; }
        .historico-row .action-wrapper { justify-content: flex-end; }
        /* Oculta labels repetidos para compactar a UI em telas maiores */
        @media (min-width: 992px) {
            #historico-form-list .historico-form:not(:first-child) .historico-row .form-label {
                position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
                overflow: hidden; clip: rect(0,0,0,0); border: 0;
            }
            .historico-row .tipo-wrapper { flex: 0 0 23%; max-width: 23%; }
            .historico-row .codigo-wrapper { flex: 0 0 23%; max-width: 23%; }
            .historico-row .ordem-wrapper { flex: 0 0 14%; max-width: 14%; }
            .historico-row .data-wrapper { flex: 0 0 14%; max-width: 14%; }
            .historico-row .action-wrapper { flex: 0 0 13%; max-width: 13%; }
        }
    `;
    document.head.appendChild(style);
}

function initializeCollapseToggles() {
    document.querySelectorAll('.collapse-toggle').forEach(toggle => {
        toggle.addEventListener('click', function() {
            const chevron = this.querySelector('.chevron');
            setTimeout(() => {
                chevron.style.transform = this.classList.contains('collapsed') ? 'rotate(0deg)' : 'rotate(90deg)';
            }, 150);
        });
    });
}

function initializeImagePreview() {
    const fotoInput = document.getElementById('id_foto');
    const fotoContainer = document.querySelector('.border.rounded.p-3.mb-3.text-center');
    if (!fotoInput || !fotoContainer) return;

    fotoInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            fotoContainer.innerHTML = ''; // Limpa o conteúdo anterior
            const preview = document.createElement('img');
            preview.style.cssText = 'max-width: 180px; max-height: 180px; width: auto; height: auto; object-fit: contain; display: block;';
            
            const reader = new FileReader();
            reader.onload = e => { preview.src = e.target.result; };
            reader.readAsDataURL(this.files[0]);
            
            fotoContainer.appendChild(preview);
        }
    });
}




// ========================================================================
// SEÇÃO: GERENCIAMENTO DO FORMSET DE HISTÓRICO
// ========================================================================

function initializeHistoricoFormset() {
    const list = document.getElementById('historico-form-list');
    const addBtn = document.getElementById('add-historico-form');
    const emptyTemplate = document.getElementById('empty-historico-form');
    const totalFormsInput = document.querySelector('input[name="historico-TOTAL_FORMS"]');
    const maxFormsInput = document.querySelector('input[name="historico-MAX_NUM_FORMS"]');

    if (!list || !addBtn || !emptyTemplate || !totalFormsInput) {
        console.error('Elementos do formset de histórico não encontrados.');
        return;
    }

    let formCount = parseInt(totalFormsInput.value, 10);
    const maxForms = maxFormsInput ? parseInt(maxFormsInput.value, 10) : 1000;

    addBtn.addEventListener('click', () => {
        if (formCount >= maxForms) {
            alert(`Número máximo de registros de histórico atingido (${maxForms}).`);
            return;
        }

        const newFormHtml = emptyTemplate.innerHTML.replace(/__prefix__/g, formCount);
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = newFormHtml;
        const newFormElement = tempDiv.firstElementChild;
        
        list.appendChild(newFormElement);
        totalFormsInput.value = ++formCount;

        // Dispara um evento customizado para que outros scripts (como o de selects dinâmicos) possam agir
        newFormElement.dispatchEvent(new CustomEvent('formset:added', { bubbles: true }));
    });

    list.addEventListener('click', e => {
        const removeBtn = e.target.closest('.remove-historico-form');
        if (removeBtn) {
            const formElement = removeBtn.closest('.historico-form');
            if (formElement) {
                // Em vez de remover, marca para deleção se for um form existente,
                // ou simplesmente remove se for um form novo.
                const deleteCheckbox = formElement.querySelector('input[type="checkbox"][name$="-DELETE"]');
                if (deleteCheckbox) {
                    deleteCheckbox.checked = true;
                    formElement.style.display = 'none'; // Oculta o formulário
                } else {
                    formElement.remove();
                    // A contagem de forms não deve ser decrementada aqui, pois o Django cuida disso no backend.
                    // Apenas atualizamos os índices se necessário, mas a abordagem do Django com __prefix__ evita isso.
                }
            }
        }
    });
}


// ========================================================================
// SEÇÃO: SELECTS DINÂMICOS (TIPO -> CÓDIGO)
// ========================================================================

function initializeDynamicSelects(urlTipos, urlCodigosPorTipo) {
    let cacheTipos = null;
    const cacheCodigos = {};

    function fetchTipos() {
        if (cacheTipos) return Promise.resolve(cacheTipos);
        return fetch(urlTipos).then(r => r.json()).then(data => {
            if (data.status === 'success') {
                cacheTipos = data.tipos;
                return cacheTipos;
            }
            throw new Error(data.message || 'Erro ao carregar tipos');
        });
    }

    function fetchCodigos(tipoId) {
        if (cacheCodigos[tipoId]) return Promise.resolve(cacheCodigos[tipoId]);
        const url = new URL(urlCodigosPorTipo, window.location.origin);
        url.searchParams.set('tipo_id', tipoId);
        return fetch(url).then(r => r.json()).then(data => {
            if (data.status === 'success') {
                cacheCodigos[tipoId] = data.codigos;
                return data.codigos;
            }
            throw new Error(data.message || 'Erro ao carregar códigos');
        });
    }

    function populateSelect(selectEl, items, placeholder, selectedValue) {
        selectEl.innerHTML = `<option value="">${placeholder}</option>`;
        items.forEach(item => {
            const opt = document.createElement('option');
            opt.value = item.id;
            opt.textContent = item.descricao ? `${item.nome} (${item.descricao})` : item.nome;
            if (String(selectedValue) === String(item.id)) {
                opt.selected = true;
            }
            selectEl.appendChild(opt);
        });
        selectEl.disabled = false;
    }

    function setupLine(container) {
        const tipoSelect = container.querySelector('select.tipo-codigo-select');
        const codigoSelect = container.querySelector('select.codigo-select');
        if (!tipoSelect || !codigoSelect) return;

        const initialTipo = tipoSelect.dataset.initial || tipoSelect.value;
        const initialCodigo = codigoSelect.dataset.initial || codigoSelect.value;

        fetchTipos().then(tipos => {
            populateSelect(tipoSelect, tipos, '-- selecione o tipo --', initialTipo);
            if (initialTipo) {
                codigoSelect.disabled = true;
                codigoSelect.innerHTML = '<option value="">Carregando...</option>';
                fetchCodigos(initialTipo).then(codigos => {
                    populateSelect(codigoSelect, codigos, '-- selecione o código --', initialCodigo);
                });
            } else {
                codigoSelect.disabled = true;
                codigoSelect.innerHTML = '<option value="">-- escolha o tipo --</option>';
            }
        });

        tipoSelect.addEventListener('change', () => {
            const tipoId = tipoSelect.value;
            codigoSelect.disabled = true;
            codigoSelect.innerHTML = '<option value="">Carregando...</option>';
            if (tipoId) {
                fetchCodigos(tipoId).then(codigos => {
                    populateSelect(codigoSelect, codigos, '-- selecione o código --', null);
                });
            } else {
                codigoSelect.innerHTML = '<option value="">-- escolha o tipo --</option>';
            }
        });
    }

    // Configura as linhas existentes
    document.querySelectorAll('.historico-form').forEach(setupLine);

    // Ouve por novos formulários adicionados ao formset
    document.getElementById('historico-form-list').addEventListener('formset:added', e => {
        setupLine(e.target);
    });
}
