/**
 * Módulo para busca dinâmica de países, estados e cidades
 */
const LocalidadeSearch = {
    
    /**
     * Inicializa os campos de busca de localidade
     */
    init: function() {
        this.initPaisSearch();
        this.initEstadoSearch();
        this.initCidadeSearch();
    },
    
    /**
     * Inicializa busca de países
     */
    initPaisSearch: function() {
        const paisInput = document.getElementById('id_pais_nacionalidade_search');
        const paisHidden = document.getElementById('id_pais_nacionalidade');
        const paisResults = document.getElementById('pais-results');
        
        if (!paisInput) return;
        
        let searchTimeout;
        
        paisInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 2) {
                paisResults.innerHTML = '';
                paisResults.style.display = 'none';
                return;
            }
            
            searchTimeout = setTimeout(() => {
                LocalidadeSearch.searchPaises(query, paisResults, paisInput, paisHidden);
            }, 300);
        });
        
        // Esconder resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!paisInput.contains(e.target) && !paisResults.contains(e.target)) {
                paisResults.style.display = 'none';
            }
        });
    },
    
    /**
     * Busca países via API
     */
    searchPaises: function(query, resultsContainer, inputField, hiddenField) {
        fetch(`/alunos/api/paises/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = '';
                
                if (data.length === 0) {
                    resultsContainer.innerHTML = '<div class="search-result-item no-results">Nenhum país encontrado</div>';
                } else {
                    data.forEach(pais => {
                        const item = document.createElement('div');
                        item.className = 'search-result-item';
                        item.innerHTML = `
                            <strong>${pais.nome}</strong><br>
                            <small>Nacionalidade: ${pais.nacionalidade}</small>
                        `;
                        
                        item.addEventListener('click', function() {
                            inputField.value = pais.display;
                            hiddenField.value = pais.id;
                            resultsContainer.style.display = 'none';
                        });
                        
                        resultsContainer.appendChild(item);
                    });
                }
                
                resultsContainer.style.display = 'block';
            })
            .catch(error => {
                console.error('Erro ao buscar países:', error);
                resultsContainer.innerHTML = '<div class="search-result-item error">Erro ao buscar países</div>';
                resultsContainer.style.display = 'block';
            });
    },
    
    /**
     * Inicializa busca de estados
     */
    initEstadoSearch: function() {
        const estadoInput = document.getElementById('id_estado_search');
        const estadoHidden = document.getElementById('id_estado_naturalidade');
        const estadoResults = document.getElementById('estado-results');
        
        if (!estadoInput) return;
        
        let searchTimeout;
        
        estadoInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 1) {
                estadoResults.innerHTML = '';
                estadoResults.style.display = 'none';
                // Limpar cidades quando estado é limpo
                LocalidadeSearch.clearCidades();
                return;
            }
            
            searchTimeout = setTimeout(() => {
                LocalidadeSearch.searchEstados(query, estadoResults, estadoInput, estadoHidden);
            }, 300);
        });
    },
    
    /**
     * Busca estados via API
     */
    searchEstados: function(query, resultsContainer, inputField, hiddenField) {
        fetch(`/alunos/api/estados/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = '';
                
                if (data.length === 0) {
                    resultsContainer.innerHTML = '<div class="search-result-item no-results">Nenhum estado encontrado</div>';
                } else {
                    data.forEach(estado => {
                        const item = document.createElement('div');
                        item.className = 'search-result-item';
                        item.innerHTML = `
                            <strong>${estado.nome}</strong> (${estado.codigo})<br>
                            <small>Região: ${estado.regiao}</small>
                        `;
                        
                        item.addEventListener('click', function() {
                            inputField.value = estado.display;
                            hiddenField.value = estado.id;
                            resultsContainer.style.display = 'none';
                            
                            // Limpar campo de cidade quando estado muda
                            LocalidadeSearch.clearCidades();
                        });
                        
                        resultsContainer.appendChild(item);
                    });
                }
                
                resultsContainer.style.display = 'block';
            })
            .catch(error => {
                console.error('Erro ao buscar estados:', error);
                resultsContainer.innerHTML = '<div class="search-result-item error">Erro ao buscar estados</div>';
                resultsContainer.style.display = 'block';
            });
    },
    
    /**
     * Inicializa busca de cidades
     */
    initCidadeSearch: function() {
        const cidadeInput = document.getElementById('id_cidade_naturalidade_search');
        const cidadeHidden = document.getElementById('id_cidade_naturalidade');
        const cidadeResults = document.getElementById('cidade-results');
        
        if (!cidadeInput) return;
        
        let searchTimeout;
        
        cidadeInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 1) {
                cidadeResults.innerHTML = '';
                cidadeResults.style.display = 'none';
                return;
            }
            
            searchTimeout = setTimeout(() => {
                LocalidadeSearch.searchCidades(query, cidadeResults, cidadeInput, cidadeHidden);
            }, 300);
        });
    },
    
    /**
     * Busca cidades via API
     */
    searchCidades: function(query, resultsContainer, inputField, hiddenField) {
        fetch(`/alunos/api/cidades/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = '';
                
                if (data.length === 0) {
                    resultsContainer.innerHTML = '<div class="search-result-item no-results">Nenhuma cidade encontrada</div>';
                } else {
                    data.forEach(cidade => {
                        const item = document.createElement('div');
                        item.className = 'search-result-item';
                        item.innerHTML = `
                            <strong>${cidade.nome}</strong><br>
                            <small>Estado: ${cidade.estado}</small>
                        `;
                        
                        item.addEventListener('click', function() {
                            inputField.value = cidade.display;
                            hiddenField.value = cidade.id;
                            resultsContainer.style.display = 'none';
                        });
                        
                        resultsContainer.appendChild(item);
                    });
                }
                
                resultsContainer.style.display = 'block';
            })
            .catch(error => {
                console.error('Erro ao buscar cidades:', error);
                resultsContainer.innerHTML = '<div class="search-result-item error">Erro ao buscar cidades</div>';
                resultsContainer.style.display = 'block';
            });
    },
    
    /**
     * Limpa os campos de cidade
     */
    clearCidades: function() {
        const cidadeInput = document.getElementById('id_cidade_naturalidade_search');
        const cidadeHidden = document.getElementById('id_cidade_naturalidade');
        const cidadeResults = document.getElementById('cidade-results');
        
        if (cidadeInput) cidadeInput.value = '';
        if (cidadeHidden) cidadeHidden.value = '';
        if (cidadeResults) cidadeResults.innerHTML = '';
    }
};
