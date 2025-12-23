/**
 * Filtros dinâmicos para listagem de matrículas
 * Atualiza a tabela via AJAX sem recarregar a página
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    const statusSelect = document.querySelector('select[name="status"]');
    const turmaSelect = document.querySelector('select[name="turma"]');
    const tableContainer = document.querySelector('.table-responsive');
    const paginationContainer = document.querySelector('.pagination')?.parentElement;
    
    if (!searchInput || !statusSelect || !turmaSelect) {
        console.warn('Filtros não encontrados na página');
        return;
    }
    
    /**
     * Função debounce para evitar muitas requisições
     */
    function debounce(callback, delay = 200) {
        let timeoutId;
        return function(...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => callback.apply(this, args), delay);
        };
    }
    
    /**
     * Busca matrículas via AJAX
     */
    async function buscarMatriculas() {
        const search = searchInput.value.trim();
        const status = statusSelect.value;
        const turma = turmaSelect.value;
        
        // Construir URL com parâmetros
        const params = new URLSearchParams();
        if (search) params.append('search', search);
        if (status) params.append('status', status);
        if (turma) params.append('turma', turma);
        
        const url = `${window.location.pathname}?${params.toString()}`;
        
        // Mostrar loading
        if (tableContainer) {
            tableContainer.style.opacity = '0.5';
            tableContainer.style.pointerEvents = 'none';
        }
        
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/html'
                }
            });
            
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            
            // Se a resposta for JSON (API), processar
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                atualizarTabela(data.matriculas);
            } else {
                // Se for HTML, extrair a tabela do HTML retornado
                const html = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                // Atualizar tabela
                const novaTabela = doc.querySelector('.table-responsive');
                if (novaTabela && tableContainer) {
                    tableContainer.innerHTML = novaTabela.innerHTML;
                }
                
                // Atualizar paginação
                const novaPaginacao = doc.querySelector('.pagination')?.parentElement;
                if (novaPaginacao && paginationContainer) {
                    paginationContainer.innerHTML = novaPaginacao.innerHTML;
                }
            }
            
            // Atualizar URL sem recarregar página
            window.history.pushState({}, '', url);
            
        } catch (error) {
            console.error('Erro ao buscar matrículas:', error);
            
            if (tableContainer) {
                tableContainer.innerHTML = `
                    <div class="alert alert-danger" role="alert">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Erro ao carregar matrículas. Tente novamente.
                    </div>
                `;
            }
        } finally {
            if (tableContainer) {
                tableContainer.style.opacity = '1';
                tableContainer.style.pointerEvents = 'auto';
            }
        }
    }
    
    /**
     * Atualizar tabela com dados JSON (se API retornar JSON)
     */
    function atualizarTabela(matriculas) {
        if (!tableContainer) return;
        
        if (matriculas.length === 0) {
            tableContainer.innerHTML = `
                <div class="alert alert-info" role="alert">
                    <i class="fas fa-info-circle me-2"></i>
                    Nenhuma matrícula encontrada com os filtros selecionados.
                </div>
            `;
            return;
        }
        
        let html = `
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Aluno</th>
                        <th>Turma</th>
                        <th>Data Matrícula</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        matriculas.forEach(m => {
            const statusBadgeClass = m.status === 'A' ? 'success' : (m.status === 'C' ? 'danger' : 'secondary');
            const statusText = m.status === 'A' ? 'Ativa' : (m.status === 'C' ? 'Cancelada' : 'Finalizada');
            
            html += `
                <tr>
                    <td>${m.id}</td>
                    <td>${m.aluno_nome}</td>
                    <td>${m.turma_nome}</td>
                    <td>${m.data_matricula}</td>
                    <td><span class="badge bg-${statusBadgeClass}">${statusText}</span></td>
                    <td>
                        <div class="btn-group" role="group">
                            <a href="/matriculas/${m.id}/" class="btn btn-sm btn-info" title="Ver detalhes">
                                <i class="fas fa-eye"></i>
                            </a>
                            <a href="/matriculas/${m.id}/editar/" class="btn btn-sm btn-warning" title="Editar">
                                <i class="fas fa-edit"></i>
                            </a>
                            ${m.status === 'A' ? `
                            <a href="/matriculas/${m.id}/cancelar/" class="btn btn-sm btn-danger" title="Cancelar">
                                <i class="fas fa-ban"></i>
                            </a>
                            ` : ''}
                        </div>
                    </td>
                </tr>
            `;
        });
        
        html += `
                </tbody>
            </table>
        `;
        
        tableContainer.innerHTML = html;
    }
    
    // Criar função debounced
    const buscarMatriculasDebounced = debounce(buscarMatriculas, 200);
    
    // Event listeners
    searchInput.addEventListener('input', buscarMatriculasDebounced);
    statusSelect.addEventListener('change', buscarMatriculas);
    turmaSelect.addEventListener('change', buscarMatriculas);
    
    // Remover botão "Filtrar" se existir (não é mais necessário)
    const btnFiltrar = document.querySelector('button[type="submit"]');
    if (btnFiltrar && btnFiltrar.textContent.includes('Filtrar')) {
        btnFiltrar.remove();
    }
    
    // Prevenir submit do form (agora é tudo AJAX)
    const filterForm = document.querySelector('form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            buscarMatriculas();
        });
    }
});
