/**
 * Módulo para busca e seleção de instrutores
 */
const InstrutorSearch = (function() {
    let csrfToken = '';
    let showAllStudents = false;
    let ignoreEligibility = false;
    
    // Função para verificar elegibilidade
    function verificarElegibilidade(cpf, tipoInstrutor) {
        console.log(`Verificando elegibilidade do instrutor ${tipoInstrutor} com CPF: ${cpf}`);
        
        const errorElement = document.getElementById(`${tipoInstrutor}-error`);
        if (!errorElement) {
            console.error(`Elemento de erro não encontrado para ${tipoInstrutor}`);
            return;
        }
        
        // Limpar mensagem de erro anterior
        errorElement.textContent = '';
        errorElement.classList.add('d-none');
        
        // Se estamos ignorando verificações de elegibilidade, não fazer a verificação
        if (ignoreEligibility) {
            console.log('Ignorando verificação de elegibilidade (modo de depuração ativo)');
            return;
        }
        
        // Fazer requisição para verificar elegibilidade
        fetch(`/alunos/api/verificar-elegibilidade/${cpf}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(`Resposta da verificação de elegibilidade:`, data);
                
                if (!data.elegivel) {
                    // Mostrar mensagem de erro específica
                    errorElement.textContent = data.motivo || "Este aluno não pode ser instrutor.";
                    errorElement.classList.remove('d-none');
                    
                    // Se estamos mostrando todos os alunos, não bloqueamos a seleção
                    if (!showAllStudents) {
                        // Limpar seleção
                        const selectElement = document.getElementById(`id_${tipoInstrutor}`);
                        if (selectElement) {
                            selectElement.value = '';
                        }
                    }
                }
            })
            .catch(error => {
                console.error(`Erro ao verificar elegibilidade: ${error.message}`);
                errorElement.textContent = `Erro na busca: ${error.message}`;
                errorElement.classList.remove('d-none');
            });
    }
    
    // Função para selecionar um instrutor
    function selectInstructor(cpf, nome, numero, situacao, turmas, tipoInstrutor) {
        console.log(`Selecionando ${tipoInstrutor}: ${nome} (${cpf})`);
        
        // Atualizar o select oculto
        const selectElement = document.getElementById(`id_${tipoInstrutor}`);
        if (selectElement) {
            selectElement.value = cpf;
        }
        
        // Atualizar a exibição
        const containerElement = document.getElementById(`selected-${tipoInstrutor}-container`);
        const infoElement = document.getElementById(`selected-${tipoInstrutor}-info`);
        
        if (containerElement && infoElement) {
            // Criar HTML para turmas, se disponível
            let turmasHtml = '';
            if (turmas && turmas.length > 0) {
                turmasHtml = `
                    <div class="mt-2">
                        <strong>Turmas:</strong>
                        <ul class="mb-0 ps-3">
                            ${turmas.map(turma => `<li>${turma}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            infoElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <strong>${nome}</strong><br>
                        CPF: ${cpf} | Nº Iniciático: ${numero || 'N/A'}<br>
                        <span class="badge ${situacao === 'ATIVO' ? 'bg-success' : 'bg-danger'}">${situacao || 'Não informado'}</span>
                        ${turmasHtml}
                    </div>
                    <button type="button" class="btn btn-sm btn-danger remove-instructor">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            
            containerElement.classList.remove('d-none');
            
            // Adicionar evento para remover instrutor
            const removeButton = infoElement.querySelector('.remove-instructor');
            if (removeButton) {
                removeButton.addEventListener('click', function() {
                    selectElement.value = '';
                    containerElement.classList.add('d-none');
                    infoElement.innerHTML = '';
                    
                    // Limpar mensagem de erro
                    const errorElement = document.getElementById(`${tipoInstrutor}-error`);
                    if (errorElement) {
                        errorElement.textContent = '';
                        errorElement.classList.add('d-none');
                    }
                });
            }
        }
        
        // Verificar elegibilidade
        verificarElegibilidade(cpf, tipoInstrutor);
    }
    
    // Função para configurar a busca de instrutores
    function setupInstructorSearch(tipoInstrutor) {
        console.log(`Configurando busca para ${tipoInstrutor}`);
        
        const searchInput = document.getElementById(`search-${tipoInstrutor}`);
        const searchResults = document.getElementById(`search-results-${tipoInstrutor}`);
        
        if (!searchInput || !searchResults) {
            console.error(`Elementos de busca não encontrados para ${tipoInstrutor}`);
            return;
        }
        
        // Evento de digitação
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            // Fazer requisição para buscar alunos
            const url = showAllStudents || ignoreEligibility ? 
                `/alunos/search/?q=${encodeURIComponent(query)}` : 
                `/alunos/api/search-instrutores/?q=${encodeURIComponent(query)}`;
            
            fetch(url, {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(`Resultados da busca para ${tipoInstrutor}:`, data);
                
                // Limpar resultados anteriores
                searchResults.innerHTML = '';
                
                // Verificar se há erro na resposta
                if (data && data.error) {
                    searchResults.innerHTML = `<div class="list-group-item text-danger">Erro na busca: ${data.error}</div>`;
                    searchResults.style.display = 'block';
                    return;
                }
                
                // Garantir que data seja um array
                const alunos = Array.isArray(data) ? data : [];
                
                if (alunos.length === 0) {
                    searchResults.innerHTML = '<div class="list-group-item">Nenhum resultado encontrado</div>';
                    searchResults.style.display = 'block';
                    return;
                }
                
                // Adicionar resultados
                alunos.forEach(aluno => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.className = 'list-group-item list-group-item-action';
                    item.dataset.cpf = aluno.cpf;
                    item.dataset.nome = aluno.nome;
                    item.dataset.numero = aluno.numero_iniciatico;
                    item.dataset.situacao = aluno.situacao || 'Não informado';
                    
                    // Preparar informações de turmas
                    let turmasHtml = '';
                    let turmasArray = [];
                    
                    if (aluno.turmas_como_instrutor && aluno.turmas_como_instrutor.length > 0) {
                        turmasArray = turmasArray.concat(aluno.turmas_como_instrutor.map(t => `${t} (Instrutor)`));
                    }
                    
                    if (aluno.turmas_como_aluno && aluno.turmas_como_aluno.length > 0) {
                        turmasArray = turmasArray.concat(aluno.turmas_como_aluno.map(t => `${t} (Aluno)`));
                    }
                    
                    if (turmasArray.length > 0) {
                        turmasHtml = `
                            <div class="small mt-1">
                                <strong>Turmas:</strong>
                                <ul class="mb-0 ps-3">
                                    ${turmasArray.map(turma => `<li>${turma}</li>`).join('')}
                                </ul>
                            </div>
                        `;
                    }
                    
                    item.innerHTML = `
                        <div>
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>${aluno.nome}</strong>
                                    <span class="badge ${aluno.situacao === 'ATIVO' ? 'bg-success' : 'bg-danger'} ms-2">${aluno.situacao || 'Não informado'}</span>
                                </div>
                                <div class="text-muted">
                                    <small>CPF: ${aluno.cpf}</small>
                                    <small class="ms-2">Nº: ${aluno.numero_iniciatico || 'N/A'}</small>
                                </div>
                            </div>
                            ${turmasHtml}
                        </div>
                    `;                    
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        selectInstructor(
                            this.dataset.cpf,
                            this.dataset.nome,
                            this.dataset.numero,
                            this.dataset.situacao,
                            turmasArray,
                            tipoInstrutor
                        );
                        searchResults.style.display = 'none';
                        searchInput.value = '';
                    });
                    
                    searchResults.appendChild(item);
                });
                
                searchResults.style.display = 'block';
            })
            .catch(error => {
                console.error(`Erro na busca de ${tipoInstrutor}:`, error);
                searchResults.innerHTML = `<div class="list-group-item text-danger">Erro na busca: ${error.message}</div>`;
                searchResults.style.display = 'block';
            });        });
        
        // Esconder resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
    
    return {
        init: function(token, allowAllStudents = false) {
            console.log('Inicializando módulo de busca de instrutores');
            csrfToken = token;
            showAllStudents = allowAllStudents;
            
            // Configurar busca para cada tipo de instrutor
            setupInstructorSearch('instrutor');
            setupInstructorSearch('instrutor-auxiliar');
            setupInstructorSearch('auxiliar-instrucao');
            
            console.log(`Modo de exibição: ${showAllStudents ? 'todos os alunos' : 'apenas elegíveis'}`);
            
            // Verificar se o modo de depuração está ativo
            const debugSwitch = document.getElementById('ignore-eligibility');
            if (debugSwitch) {
                ignoreEligibility = debugSwitch.checked;
                console.log(`Modo de depuração: ${ignoreEligibility ? 'ativo' : 'inativo'}`);
            }
        },
        
        setIgnoreEligibility: function(value) {
            ignoreEligibility = value;
            console.log(`Modo de depuração ${ignoreEligibility ? 'ativado' : 'desativado'}`);
        }
    };
})();