document.addEventListener('DOMContentLoaded', function() {
    // Configuração para os três tipos de instrutores
    const instrutorTypes = [
        {
            searchInputId: 'search-instrutor',
            resultsContainerId: 'search-results-instrutor',
            selectedContainerId: 'selected-instrutor-container',
            selectedInfoId: 'selected-instrutor-info',
            errorContainerId: 'instrutor-error',
            selectId: 'id_instrutor',
            clearBtnId: 'clear-instrutor-btn'
        },
        {
            searchInputId: 'search-instrutor-auxiliar',
            resultsContainerId: 'search-results-instrutor-auxiliar',
            selectedContainerId: 'selected-instrutor-auxiliar-container',
            selectedInfoId: 'selected-instrutor-auxiliar-info',
            errorContainerId: 'instrutor-auxiliar-error',
            selectId: 'id_instrutor_auxiliar',
            clearBtnId: 'clear-instrutor-auxiliar-btn'
        },
        {
            searchInputId: 'search-auxiliar-instrucao',
            resultsContainerId: 'search-results-auxiliar-instrucao',
            selectedContainerId: 'selected-auxiliar-instrucao-container',
            selectedInfoId: 'selected-auxiliar-instrucao-info',
            errorContainerId: 'auxiliar-instrucao-error',
            selectId: 'id_auxiliar_instrucao',
            clearBtnId: 'clear-auxiliar-instrucao-btn'
        }
    ];

    // Inicializar cada tipo de instrutor
    instrutorTypes.forEach(config => {
        initInstrutorSearch(config);
    });

    // Função para inicializar a busca de instrutor
    function initInstrutorSearch(config) {
        const searchInput = document.getElementById(config.searchInputId);
        const resultsContainer = document.getElementById(config.resultsContainerId);
        const selectedContainer = document.getElementById(config.selectedContainerId);
        const selectedInfo = document.getElementById(config.selectedInfoId);
        const errorContainer = document.getElementById(config.errorContainerId);
        const selectElement = document.getElementById(config.selectId);
        
        // Adicionar botão de limpar se não existir
        let clearBtn = document.getElementById(config.clearBtnId);
        if (!clearBtn && selectedContainer) {
            clearBtn = document.createElement('button');
            clearBtn.id = config.clearBtnId;
            clearBtn.type = 'button';
            clearBtn.className = 'btn btn-sm btn-outline-secondary mt-2';
            clearBtn.textContent = 'Limpar seleção';
            clearBtn.style.display = 'none';
            selectedContainer.parentNode.insertBefore(clearBtn, selectedContainer.nextSibling);
        }

        if (!searchInput || !resultsContainer || !selectedContainer || !selectedInfo || !selectElement) {
            console.error('Elementos necessários não encontrados para', config.searchInputId);
            return;
        }

        // Verificar se já existe um instrutor selecionado (para edição)
        if (selectElement.value) {
            const selectedOption = selectElement.options[selectElement.selectedIndex];
            if (selectedOption.value) {
                // Simular seleção do instrutor existente
                fetchInstrutorDetails(selectedOption.value, config);
                if (clearBtn) clearBtn.style.display = 'inline-block';
            }
        }

        // Evento de input para busca
        searchInput.addEventListener('input', debounce(function() {
            const query = searchInput.value.trim();
            
            if (query.length < 2) {
                resultsContainer.style.display = 'none';
                return;
            }
            
            // Fazer a requisição para a API
            fetch(`/alunos/api/instrutores/?q=${encodeURIComponent(query)}`, {
                credentials: 'same-origin',  // CRÍTICO: Envia cookies de sessão
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'  // Identifica como AJAX
                }
            })
                .then(response => {
                    // Detecta redirect para login (não autenticado)
                    if (response.redirected && response.url.includes('/entrar/')) {
                        throw new Error('UNAUTHORIZED: Sessão expirada. Faça login novamente.');
                    }
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(data => {
                    resultsContainer.innerHTML = '';
                    
                    if (data.length === 0) {
                        resultsContainer.innerHTML = '<div class="list-group-item">Nenhum resultado encontrado</div>';
                        resultsContainer.style.display = 'block';
                        return;
                    }
                    
                    data.forEach(aluno => {
                        const item = document.createElement('a');
                        item.href = '#';
                        item.className = 'list-group-item list-group-item-action';
                        item.dataset.cpf = aluno.cpf;
                        item.dataset.nome = aluno.nome;
                        item.dataset.numeroIniciativo = aluno.numero_iniciatico;
                        item.dataset.situacao = aluno.situacao;
                        
                        // Gera iniciais do nome para avatar placeholder
                        const iniciais = aluno.nome.split(' ')
                            .filter(parte => parte.length > 0)
                            .slice(0, 2)
                            .map(parte => parte.charAt(0).toUpperCase())
                            .join('');
                        
                        let avatarHtml = '';
                        if (aluno.foto) {
                            // Avatar com fallback: se a imagem falhar, mostra iniciais
                            avatarHtml = `
                                <img src="${aluno.foto}" 
                                     width="32" 
                                     height="32" 
                                     class="rounded-circle"
                                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
                                     style="object-fit: cover;">
                                <div class="rounded-circle bg-secondary text-white align-items-center justify-content-center" 
                                     style="width: 32px; height: 32px; font-size: 14px; display: none;">
                                    ${iniciais}
                                </div>
                            `;
                        } else {
                            // Sem foto: mostra iniciais diretamente
                            avatarHtml = `
                                <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" 
                                     style="width: 32px; height: 32px; font-size: 14px;">
                                    ${iniciais}
                                </div>
                            `;
                        }
                        
                        item.innerHTML = `
                            <div class="d-flex align-items-center">
                                <div class="me-2">
                                    ${avatarHtml}
                                </div>
                                <div>
                                    <div><strong>${aluno.nome}</strong></div>
                                    <small>CPF: ${aluno.cpf} | Nº Iniciático: ${aluno.numero_iniciatico}</small>
                                </div>
                            </div>
                        `;
                        
                        item.addEventListener('click', function(e) {
                            e.preventDefault();
                            selectInstrutor(aluno.cpf, config);
                        });
                        
                        resultsContainer.appendChild(item);
                    });
                    
                    resultsContainer.style.display = 'block';
                })
                .catch(error => {
                    console.error('Erro ao buscar instrutores:', error);
                    let errorMessage = 'Erro ao buscar instrutores. ';
                    
                    if (error.message.includes('UNAUTHORIZED')) {
                        errorMessage = '<strong>Sessão expirada!</strong> Recarregue a página e faça login novamente.';
                        // Opcional: Redirecionar automaticamente após 3 segundos
                        setTimeout(() => {
                            window.location.reload();
                        }, 3000);
                    } else if (error.message.includes('404')) {
                        errorMessage += 'Endpoint não encontrado. Contate o administrador.';
                    } else if (error.message.includes('500')) {
                        errorMessage += 'Erro no servidor. Tente novamente.';
                    } else if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
                        errorMessage += 'Erro de conexão. Verifique sua internet.';
                    } else {
                        errorMessage += error.message || 'Erro desconhecido.';
                    }
                    
                    resultsContainer.innerHTML = `<div class="list-group-item text-danger">
                        <i class="fas fa-exclamation-triangle me-2"></i>${errorMessage}
                    </div>`;
                    resultsContainer.style.display = 'block';
                });
        }, 300));

        // Fechar resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
                resultsContainer.style.display = 'none';
            }
        });

        // Evento para limpar seleção
        if (clearBtn) {
            clearBtn.addEventListener('click', function() {
                clearInstrutor(config);
            });
        }
    }

    // Função para selecionar um instrutor
    function selectInstrutor(cpf, config) {
        const searchInput = document.getElementById(config.searchInputId);
        const resultsContainer = document.getElementById(config.resultsContainerId);
        const clearBtn = document.getElementById(config.clearBtnId);
        
        // Limpar resultados e campo de busca
        resultsContainer.style.display = 'none';
        searchInput.value = '';
        
        // Buscar detalhes do instrutor e atualizar a UI
        fetchInstrutorDetails(cpf, config);
        
        // Mostrar botão de limpar
        if (clearBtn) clearBtn.style.display = 'inline-block';
    }

    // Função para buscar detalhes do instrutor
    function fetchInstrutorDetails(cpf, config) {
        const selectedContainer = document.getElementById(config.selectedContainerId);
        const selectedInfo = document.getElementById(config.selectedInfoId);
        const errorContainer = document.getElementById(config.errorContainerId);
        const selectElement = document.getElementById(config.selectId);
        
        // Mostrar loading
        selectedInfo.innerHTML = '<div class="text-center"><div class="spinner-border spinner-border-sm" role="status"></div> Carregando...</div>';
        selectedContainer.classList.remove('d-none');
        
        // Buscar detalhes do aluno
        fetch(`/alunos/api/get-aluno/${cpf}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const aluno = data.aluno;
                    
                    // Atualizar o select oculto
                    selectElement.value = aluno.cpf;
                    
                    // Verificar elegibilidade como instrutor
                    fetch(`/alunos/api/verificar-elegibilidade/${aluno.cpf}/`)
                        .then(response => response.json())
                        .then(eligibilityData => {
                            // Buscar detalhes adicionais (turmas, etc)
                            fetch(`/alunos/api/detalhes/${aluno.cpf}/`)
                                .then(response => response.json())
                                .then(detailsData => {
                                    // Atualizar UI com todas as informações
                                    updateInstrutorUI(aluno, eligibilityData, detailsData, config);
                                })
                                .catch(error => {
                                    console.error('Erro ao buscar detalhes do instrutor:', error);
                                    updateInstrutorUI(aluno, eligibilityData, { success: false }, config);
                                });
                        })
                        .catch(error => {
                            console.error('Erro ao verificar elegibilidade:', error);
                            updateInstrutorUI(aluno, { elegivel: false, motivo: 'Erro ao verificar elegibilidade' }, { success: false }, config);
                        });
                } else {
                    errorContainer.textContent = 'Erro ao buscar informações do aluno.';
                    errorContainer.classList.remove('d-none');
                    selectedContainer.classList.add('d-none');
                }
            })
            .catch(error => {
                console.error('Erro ao buscar aluno:', error);
                errorContainer.textContent = 'Erro ao buscar informações do aluno.';
                errorContainer.classList.remove('d-none');
                selectedContainer.classList.add('d-none');
            });
    }

    // Função para atualizar a UI com os detalhes do instrutor
    function updateInstrutorUI(aluno, eligibilityData, detailsData, config) {
        const selectedContainer = document.getElementById(config.selectedContainerId);
        const selectedInfo = document.getElementById(config.selectedInfoId);
        const errorContainer = document.getElementById(config.errorContainerId);
        
        // Limpar mensagens de erro
        errorContainer.classList.add('d-none');
        
        // Construir HTML para o instrutor selecionado
        let avatarHtml = '';
        if (aluno.foto) {
            avatarHtml = `<img src="${aluno.foto}" width="48" height="48" class="rounded-circle mb-2">`;
        }
        
        let statusBadge = '';
        if (aluno.situacao) {
            const badgeClass = aluno.situacao === 'ATIVO' ? 'bg-success' : 'bg-warning';
            statusBadge = `<span class="badge ${badgeClass}">${aluno.situacao}</span>`;
        }
        
        let turmasHtml = 'Nenhuma';
        if (detailsData.success && detailsData.turmas && detailsData.turmas.length > 0) {
            turmasHtml = detailsData.turmas.map(t => t.nome).join(', ');
        }
        
        let statusInstrutor = 'Não verificado';
        if (eligibilityData.elegivel) {
            statusInstrutor = '<span class="text-success">Elegível</span>';
        } else {
            statusInstrutor = `<span class="text-warning">Não elegível</span>`;
            if (eligibilityData.motivo) {
                statusInstrutor += ` - ${eligibilityData.motivo}`;
            }
        }
        
        selectedInfo.innerHTML = `
            ${avatarHtml}
            <strong>${aluno.nome}</strong><br>
            CPF: ${aluno.cpf}<br>
            Número Iniciático: ${aluno.numero_iniciatico || 'N/A'}<br>
            ${statusBadge}
            <div class="mt-2 small">
                <div><strong>Status como instrutor:</strong> ${statusInstrutor}</div>
                <div class="mt-1"><strong>Turmas:</strong> ${turmasHtml}</div>
            </div>
        `;
        
        selectedContainer.classList.remove('d-none');
        
        // Mostrar aviso se não for elegível
        if (!eligibilityData.elegivel) {
            errorContainer.textContent = eligibilityData.motivo || 'Este aluno não atende aos requisitos para ser instrutor.';
            errorContainer.classList.remove('d-none');
        }
    }

    // Função para limpar um instrutor
    function clearInstrutor(config) {
        const searchInput = document.getElementById(config.searchInputId);
        const selectedContainer = document.getElementById(config.selectedContainerId);
        const selectedInfo = document.getElementById(config.selectedInfoId);
        const errorContainer = document.getElementById(config.errorContainerId);
        const selectElement = document.getElementById(config.selectId);
        const clearBtn = document.getElementById(config.clearBtnId);
        
        // Limpar campo de busca
        searchInput.value = '';
        
        // Limpar seleção
        selectElement.value = '';
        
        // Ocultar contêiner de seleção e erro
        selectedContainer.classList.add('d-none');
        errorContainer.classList.add('d-none');
        
        // Resetar texto de info
        selectedInfo.textContent = `Nenhum ${config.searchInputId.replace('search-', '').replace(/-/g, ' ')} selecionado`;
        
        // Ocultar botão de limpar
        if (clearBtn) clearBtn.style.display = 'none';
    }

    // Função de debounce para evitar muitas requisições
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
});