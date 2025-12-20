/**
 * Script para matrícula em lote de alunos em turma
 * Implementa filtros, seleção múltipla e envio AJAX
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos DOM
    const formFiltros = document.getElementById('form-filtros-matricula');
    const btnLimparFiltros = document.getElementById('btn-limpar-filtros');
    const checkboxSelecionarTodos = document.getElementById('checkbox-selecionar-todos');
    const btnSelecionarTodosPagina = document.getElementById('btn-selecionar-todos-pagina');
    const btnDesmarcarTodos = document.getElementById('btn-desmarcar-todos');
    const btnMatricularSelecionados = document.getElementById('btn-matricular-selecionados');
    const badgeContador = document.getElementById('badge-contador-selecionados');
    const tbodyAlunos = document.getElementById('tbody-alunos-elegiveis');
    const loadingAlunos = document.getElementById('loading-alunos');
    const turmaIdElement = document.getElementById('turma-id');
    
    // Verificar se os elementos essenciais existem
    if (!turmaIdElement || !tbodyAlunos) {
        console.warn('Elementos essenciais para matrícula em lote não encontrados.');
        return;
    }
    
    const turmaId = turmaIdElement.value;

    // Estado
    let alunosSelecionados = new Set();

    /**
     * Atualiza o contador de alunos selecionados
     */
    function atualizarContador() {
        const count = alunosSelecionados.size;
        badgeContador.textContent = `${count} selecionado${count !== 1 ? 's' : ''}`;
        btnMatricularSelecionados.disabled = count === 0;
    }

    /**
     * Busca alunos elegíveis com filtros via AJAX
     */
    function buscarAlunosElegiveis() {
        const formData = new FormData(formFiltros);
        const params = new URLSearchParams(formData);
        
        // Mostrar loading apenas se não houver dados na tabela
        const temDados = tbodyAlunos.querySelector('tr') !== null;
        if (!temDados) {
            loadingAlunos.style.display = 'flex';
        }

        fetch(`/turmas/${turmaId}/api/alunos-elegiveis/?${params.toString()}`, {
            signal: AbortSignal.timeout(10000) // 10 segundos timeout
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                loadingAlunos.style.display = 'none';
                
                if (data.success) {
                    renderizarTabela(data.alunos);
                } else {
                    console.error('API retornou erro:', data.error);
                    mostrarErro('Erro ao carregar alunos: ' + data.error);
                }
            })
            .catch(error => {
                loadingAlunos.style.display = 'none';
                console.error('Erro ao buscar alunos:', error);
                
                if (error.name === 'TimeoutError') {
                    mostrarErro('Tempo esgotado ao carregar alunos. Tente novamente.');
                } else if (error.name === 'AbortError') {
                    mostrarErro('Requisição cancelada.');
                } else {
                    mostrarErro('Erro ao carregar alunos. Verifique o console para detalhes.');
                }
            });
    }

    /**
     * Renderiza a tabela de alunos
     */
    function renderizarTabela(alunos) {
        if (alunos.length === 0) {
            tbodyAlunos.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-muted">
                        <i class="fas fa-info-circle"></i> Nenhum aluno encontrado com os filtros aplicados.
                    </td>
                </tr>
            `;
            return;
        }

        tbodyAlunos.innerHTML = alunos.map(aluno => {
            const isChecked = alunosSelecionados.has(aluno.id);
            return `
                <tr>
                    <td>
                        <input type="checkbox" 
                               class="form-check-input checkbox-aluno" 
                               value="${aluno.id}" 
                               data-nome="${aluno.nome}"
                               ${isChecked ? 'checked' : ''}>
                    </td>
                    <td>${aluno.nome}</td>
                    <td>${aluno.cpf}</td>
                    <td>${aluno.numero_iniciatico}</td>
                    <td>${aluno.situacao}</td>
                    <td>${aluno.grau}</td>
                </tr>
            `;
        }).join('');

        // Reattach event listeners
        attachCheckboxListeners();
    }

    /**
     * Anexa listeners aos checkboxes de alunos
     */
    function attachCheckboxListeners() {
        const checkboxes = document.querySelectorAll('.checkbox-aluno');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const alunoId = parseInt(this.value);
                if (this.checked) {
                    alunosSelecionados.add(alunoId);
                } else {
                    alunosSelecionados.delete(alunoId);
                    checkboxSelecionarTodos.checked = false;
                }
                atualizarContador();
            });
        });
    }

    /**
     * Matricula alunos selecionados
     */
    function matricularSelecionados() {
        if (alunosSelecionados.size === 0) {
            mostrarErro('Selecione pelo menos um aluno para matricular.');
            return;
        }

        // Confirmar
        const count = alunosSelecionados.size;
        if (!confirm(`Deseja matricular ${count} aluno${count !== 1 ? 's' : ''} nesta turma?`)) {
            return;
        }

        // Desabilitar botão
        btnMatricularSelecionados.disabled = true;
        btnMatricularSelecionados.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';

        // Enviar
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(`/turmas/${turmaId}/matricular-em-lote/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                alunos_ids: Array.from(alunosSelecionados)
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success || data.matriculados > 0) {
                // Mostrar mensagem de sucesso
                mostrarSucesso(data.mensagem);
                
                // Mostrar falhas se houver
                if (data.falhas && data.falhas.length > 0) {
                    mostrarFalhas(data.falhas);
                }
                
                // Recarregar página após 2 segundos
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else {
                mostrarErro(data.mensagem || 'Erro ao matricular alunos.');
                btnMatricularSelecionados.disabled = false;
                btnMatricularSelecionados.innerHTML = '<i class="fas fa-user-plus"></i> Matricular Selecionados';
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            mostrarErro('Erro ao processar matrículas. Tente novamente.');
            btnMatricularSelecionados.disabled = false;
            btnMatricularSelecionados.innerHTML = '<i class="fas fa-user-plus"></i> Matricular Selecionados';
        });
    }

    /**
     * Mostra mensagem de sucesso
     */
    function mostrarSucesso(mensagem) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show';
        alert.innerHTML = `
            <i class="fas fa-check-circle"></i> ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.container').insertBefore(alert, document.querySelector('.container').firstChild);
    }

    /**
     * Mostra mensagem de erro
     */
    function mostrarErro(mensagem) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = `
            <i class="fas fa-exclamation-circle"></i> ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.container').insertBefore(alert, document.querySelector('.container').firstChild);
    }

    /**
     * Mostra lista de falhas
     */
    function mostrarFalhas(falhas) {
        const lista = falhas.map(f => `<li><strong>${f.aluno_nome}</strong>: ${f.erro}</li>`).join('');
        const alert = document.createElement('div');
        alert.className = 'alert alert-warning alert-dismissible fade show';
        alert.innerHTML = `
            <strong><i class="fas fa-exclamation-triangle"></i> Alguns alunos não foram matriculados:</strong>
            <ul class="mb-0 mt-2">${lista}</ul>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.container').insertBefore(alert, document.querySelector('.container').firstChild);
    }

    // Event Listeners
    if (formFiltros) {
        formFiltros.addEventListener('submit', function(e) {
            e.preventDefault();
            buscarAlunosElegiveis();
        });
    }

    if (btnLimparFiltros) {
        btnLimparFiltros.addEventListener('click', function() {
            formFiltros.reset();
            // Manter situação "Ativo" selecionada
            document.getElementById('filtro-situacao').value = 'a';
            buscarAlunosElegiveis();
        });
    }

    if (checkboxSelecionarTodos) {
        checkboxSelecionarTodos.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.checkbox-aluno');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
                const alunoId = parseInt(checkbox.value);
                if (this.checked) {
                    alunosSelecionados.add(alunoId);
                } else {
                    alunosSelecionados.delete(alunoId);
                }
            });
            atualizarContador();
        });
    }

    if (btnSelecionarTodosPagina) {
        btnSelecionarTodosPagina.addEventListener('click', function() {
            checkboxSelecionarTodos.checked = true;
            checkboxSelecionarTodos.dispatchEvent(new Event('change'));
        });
    }

    if (btnDesmarcarTodos) {
        btnDesmarcarTodos.addEventListener('click', function() {
            checkboxSelecionarTodos.checked = false;
            checkboxSelecionarTodos.dispatchEvent(new Event('change'));
        });
    }

    if (btnMatricularSelecionados) {
        btnMatricularSelecionados.addEventListener('click', matricularSelecionados);
    }

    // Inicializar listeners dos checkboxes existentes (tabela já renderizada pelo Django)
    attachCheckboxListeners();
    
    // Atualizar contador inicial
    atualizarContador();
    
    // NÃO buscar alunos automaticamente - a tabela já vem do Django
    // Apenas buscar quando o usuário aplicar filtros via formFiltros.submit
});
