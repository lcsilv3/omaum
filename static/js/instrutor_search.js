/**
 * Módulo para gerenciamento de busca e seleção de instrutores
 */
const InstrutorSearch = (function() {
    // Variáveis privadas do módulo
    let instrutoresElegiveis = [];
    let csrfToken;

    /**
     * Inicializa o módulo de busca de instrutores
     * @param {string} csrfTokenValue - Token CSRF para requisições AJAX
     */
    function init(csrfTokenValue) {
        csrfToken = csrfTokenValue;
        carregarInstrutoresElegiveis();
        
        // Configurar os campos de busca
        setupInstructorSearch(
            'search-instrutor',
            'search-results-instrutor',
            'selected-instrutor-container',
            'selected-instrutor-info',
            'id_instrutor'
        );
        
        setupInstructorSearch(
            'search-instrutor-auxiliar',
            'search-results-instrutor-auxiliar',
            'selected-instrutor-auxiliar-container',
            'selected-instrutor-auxiliar-info',
            'id_instrutor_auxiliar'
        );
        
        setupInstructorSearch(
            'search-auxiliar-instrucao',
            'search-results-auxiliar-instrucao',
            'selected-auxiliar-instrucao-container',
            'selected-auxiliar-instrucao-info',
            'id_auxiliar_instrucao'
        );
        
        // Configurar validação do formulário
        setupFormValidation();
    }

    /**
     * Carrega a lista de instrutores elegíveis via AJAX
     */
    function carregarInstrutoresElegiveis() {
        fetch('/alunos/api/search-instrutores/', {
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            instrutoresElegiveis = data;
            console.log(`Carregados ${instrutoresElegiveis.length} instrutores elegíveis`);
        })
        .catch(error => {
            console.error('Erro ao carregar instrutores elegíveis:', error);
        });
    }

    /**
     * Configura a busca de instrutores para um campo específico
     */
    function setupInstructorSearch(searchId, resultsId, containerId, infoId, selectId) {
        const searchInput = document.getElementById(searchId);
        const searchResults = document.getElementById(resultsId);
        const selectedContainer = document.getElementById(containerId);
        const selectedInfo = document.getElementById(infoId);
        const selectElement = document.getElementById(selectId);
        
        // Criar elemento para mensagens de erro
        const errorElement = document.createElement('div');
        errorElement.className = 'alert alert-danger mt-2 d-none';
        selectedContainer.after(errorElement);
        
        let searchTimeout;
        
        // Configurar eventos de busca
        searchInput.addEventListener('input', handleSearchInput);
        
        // Ocultar resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
        
        /**
         * Manipula o evento de input no campo de busca
         */
        function handleSearchInput() {
            clearTimeout(searchTimeout);
            
            const query = this.value.trim();
            
            // Limpar mensagens de erro
            errorElement.classList.add('d-none');
            
            // Limpar resultados se a consulta for muito curta
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
                return;
            }
            
            // Definir timeout para evitar muitas requisições
            searchTimeout = setTimeout(function() {
                // Mostrar indicador de carregamento
                searchResults.innerHTML = '<div class="list-group-item text-muted">Buscando...</div>';
                searchResults.style.display = 'block';
                
                // Buscar alunos que correspondem à consulta
                fetch(`/alunos/search/?q=${encodeURIComponent(query)}`, {
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    searchResults.innerHTML = '';
                    
                    if (data.error) {
                        searchResults.innerHTML = `<div class="list-group-item text-danger">Erro ao buscar alunos: ${data.error}</div>`;
                        return;
                    }
                    
                    if (data.length === 0) {
                        searchResults.innerHTML = '<div class="list-group-item">Nenhum aluno encontrado</div>';
                        return;
                    }
                    
                    // Exibir resultados
                    data.forEach(aluno => {
                        const item = document.createElement('a');
                        item.href = '#';
                        item.className = 'list-group-item list-group-item-action';
                        item.innerHTML = `
                            <div class="d-flex justify-content-between">
                                <div>${aluno.nome}</div>
                                <div class="text-muted">
                                    <small>CPF: ${aluno.cpf}</small>
                                    ${aluno.numero_iniciatico !== "N/A" ? `<small class="ms-2">Nº: ${aluno.numero_iniciatico}</small>` : ''}
                                </div>
                            </div>
                        `;
                        
                        // Adicionar evento de clique para selecionar o aluno
                        item.addEventListener('click', function(e) {
                            e.preventDefault();
                            verificarElegibilidadeInstrutor(aluno);
                        });
                        
                        searchResults.appendChild(item);
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                    searchResults.innerHTML = '<div class="list-group-item text-danger">Erro ao buscar alunos</div>';
                });
            }, 300);
        }
        
        /**
         * Verifica se um aluno pode ser instrutor
         * @param {Object} aluno - Dados do aluno a ser verificado
         */
        function verificarElegibilidadeInstrutor(aluno) {
            // Verificar se o aluno já foi selecionado em outro campo
            const outrosSelects = Array.from(document.querySelectorAll('select[name^="instrutor"]')).filter(s => s.id !== selectId);
            const jaEstaEmUso = outrosSelects.some(select => select.value === aluno.cpf);
            
            if (jaEstaEmUso) {
                errorElement.textContent = `O aluno ${aluno.nome} já está selecionado como instrutor em outro campo.`;
                errorElement.classList.remove('d-none');
                return;
            }
            
            // Mostrar mensagem de carregamento
            errorElement.innerHTML = `<div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div> Verificando elegibilidade de ${aluno.nome}...`;
            errorElement.classList.remove('d-none');
            errorElement.classList.remove('alert-danger');
            errorElement.classList.add('alert-info');
            
            // Verificar se o aluno pode ser instrutor
            fetch(`/alunos/api/verificar-elegibilidade/${aluno.cpf}/`)
                .then(response => response.json())
                .then(data => {
                    if (!data.elegivel) {
                        errorElement.textContent = data.motivo || "Este aluno não pode ser instrutor.";
                        errorElement.classList.remove('d-none');
                        console.error(`Aluno inelegível: ${data.motivo}`);
                    } else {
                        errorElement.classList.add('d-none');
                        console.log("Aluno elegível para ser instrutor");
                        selecionarInstrutor(aluno);
                    }
                })
                .catch(error => {
                    console.error("Erro ao verificar elegibilidade:", error);
                    errorElement.textContent = "Erro na busca: Não foi possível verificar a elegibilidade.";
                    errorElement.classList.remove('d-none');
                });        }
        
        /**
         * Seleciona um instrutor após verificação de elegibilidade
         * @param {Object} aluno - Dados do aluno a ser selecionado
         */
        function selecionarInstrutor(aluno) {
            // Limpar as opções existentes no select
            while (selectElement.options.length > 0) {
                selectElement.remove(0);
            }
            
            // Criar e adicionar a opção para o aluno selecionado
            const option = new Option(aluno.nome, aluno.cpf, true, true);
            selectElement.appendChild(option);
            
            // Atualizar a interface
            searchInput.value = aluno.nome;
            selectedInfo.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${aluno.nome}</strong><br>
                        CPF: ${aluno.cpf}<br>
                        ${aluno.numero_iniciatico !== "N/A" ? `Número Iniciático: ${aluno.numero_iniciatico}` : ''}
                    </div>
                    <button type="button" class="btn btn-sm btn-outline-danger" id="remove-${selectId}">
                        <i class="fas fa-times"></i> Remover
                    </button>
                </div>
            `;
            
            selectedContainer.classList.remove('d-none');
            searchResults.style.display = 'none';
            errorElement.classList.add('d-none');
            
            // Adicionar evento para remover o instrutor
            document.getElementById(`remove-${selectId}`).addEventListener('click', function() {
                selectElement.value = '';
                searchInput.value = '';
                selectedContainer.classList.add('d-none');
            });
        }
    }

    /**
     * Configura a validação do formulário antes do envio
     */
    function setupFormValidation() {
        const form = document.querySelector('form');
        form.addEventListener('submit', function(e) {
            // Verificar se há erros visíveis
            const errosVisiveis = document.querySelectorAll('.alert-danger:not(.d-none)');
            if (errosVisiveis.length > 0) {
                e.preventDefault();
                alert('Por favor, corrija os erros antes de enviar o formulário.');
                return;
            }
            
            // Verificar se os instrutores são diferentes entre si
            const instrutorPrincipal = document.getElementById('id_instrutor').value;
            const instrutorAuxiliar = document.getElementById('id_instrutor_auxiliar').value;
            const auxiliarInstrucao = document.getElementById('id_auxiliar_instrucao').value;
            
            const instrutoresSelecionados = [instrutorPrincipal, instrutorAuxiliar, auxiliarInstrucao].filter(Boolean);
            const instrutoresUnicos = new Set(instrutoresSelecionados);
            
            if (instrutoresSelecionados.length !== instrutoresUnicos.size) {
                e.preventDefault();
                alert('Não é possível selecionar o mesmo aluno para diferentes funções de instrução.');
                return;
            }
            
            // Mostrar os selects antes do envio
            document.getElementById('id_instrutor').style.display = '';
            document.getElementById('id_instrutor_auxiliar').style.display = '';
            document.getElementById('id_auxiliar_instrucao').style.display = '';
        });
    }

    // API pública do módulo
    return {
        init: init
    };
})();
