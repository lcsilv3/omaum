document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-aluno');
    const searchResults = document.getElementById('search-results');
    
    if (!searchInput || !searchResults) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        
        const query = this.value.trim();
        
        // Clear results if query is too short
        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }
        
        // Set a timeout to avoid making too many requests
        searchTimeout = setTimeout(function() {
            // Show loading indicator
            searchResults.innerHTML = '<div class="list-group-item text-muted">Buscando...</div>';
            searchResults.style.display = 'block';
            
            // Get CSRF token
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(`/alunos/search/?q=${encodeURIComponent(query)}`, {
                headers: {
                    'X-CSRFToken': csrftoken,
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
                    // Handle error response
                    searchResults.innerHTML = `<div class="list-group-item text-danger">Erro ao buscar alunos: ${data.error}</div>`;
                    return;
                }
                
                if (data.length === 0) {
                    searchResults.innerHTML = '<div class="list-group-item">Nenhum aluno encontrado</div>';
                    return;
                }
                
                // Display results
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
                    
                    // Add click event to select this aluno
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        selectAluno(aluno);
                    });
                    
                    searchResults.appendChild(item);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                searchResults.innerHTML = '<div class="list-group-item text-danger">Erro ao buscar alunos</div>';
            });
        }, 300);
    });
    
    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
    
    // Function to select an aluno
    function selectAluno(aluno) {
        // Get the hidden input field for the aluno ID
        const alunoIdField = document.getElementById('id_aluno');
        if (alunoIdField) {
            alunoIdField.value = aluno.cpf;
        }
        
        // Update the search input with the selected aluno's name
        searchInput.value = aluno.nome;
        
        // Hide the search results
        searchResults.style.display = 'none';
        
        // Trigger any additional actions needed when an aluno is selected
        const event = new CustomEvent('alunoSelected', { detail: aluno });
        document.dispatchEvent(event);
    }
});
