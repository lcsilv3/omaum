/**
 * JavaScript para formulário de matrícula
 * Funcionalidades:
 * - Autocomplete para Turma e Aluno
 * - Validação de status da turma
 * - Exibição de informações em tempo real
 * - Validações client-side
 */

document.addEventListener('DOMContentLoaded', function() {
    // Função para inicializar Select2
    function initializeSelect2(element) {
        if (typeof jQuery !== 'undefined' && jQuery.fn.select2) {
            const $element = jQuery(element);
            // Destruir instância existente se houver
            if ($element.data('select2')) {
                $element.select2('destroy');
            }
            // Inicializar Select2
            $element.select2({
                theme: 'bootstrap-5',
                language: 'pt-BR',
                placeholder: $element.data('placeholder') || 'Selecione...',
                allowClear: true,
                width: '100%'
            });
        }
    }
    
    // Aguardar um pouco e inicializar TODOS os campos
    setTimeout(function() {
        // Adicionar classe aos selects de turma e aluno se não tiver
        const turmaSelect = document.getElementById('id_turma');
        const alunoSelect = document.getElementById('id_aluno');
        
        if (turmaSelect && !turmaSelect.classList.contains('select2-enable')) {
            turmaSelect.classList.add('select2-enable');
        }
        if (alunoSelect && !alunoSelect.classList.contains('select2-enable')) {
            alunoSelect.classList.add('select2-enable');
        }
        
        // Inicializar Select2 em TODOS os .select2-enable
        jQuery('.select2-enable').each(function() {
            initializeSelect2(this);
        });
    }, 100);
    
    // Também reinicializar quando collapse for mostrado (caso esteja fechado inicialmente)
    document.querySelectorAll('.collapse').forEach(function(collapseEl) {
        collapseEl.addEventListener('shown.bs.collapse', function() {
            jQuery(this).find('.select2-enable').each(function() {
                initializeSelect2(this);
            });
        });
    });
    
    const turmaSelect = document.getElementById('id_turma');
    const alunoSelect = document.getElementById('id_aluno');
    const submitButton = document.querySelector('button[type="submit"]');
    
    // Container para info da turma (será criado dinamicamente)
    let turmaInfoContainer = document.getElementById('turma-info-container');
    if (!turmaInfoContainer && turmaSelect) {
        turmaInfoContainer = document.createElement('div');
        turmaInfoContainer.id = 'turma-info-container';
        turmaInfoContainer.className = 'mt-2';
        turmaSelect.closest('.col-md-12').appendChild(turmaInfoContainer);
    }
    
    // Container para info do aluno
    let alunoInfoContainer = document.getElementById('aluno-info-container');
    if (!alunoInfoContainer && alunoSelect) {
        alunoInfoContainer = document.createElement('div');
        alunoInfoContainer.id = 'aluno-info-container';
        alunoInfoContainer.className = 'mt-2';
        alunoSelect.closest('.col-md-6').appendChild(alunoInfoContainer);
    }
    
    /**
     * M4: Validação de status da turma
     * M7: Exibição de informações da turma em tempo real
     */
    if (turmaSelect) {
        turmaSelect.addEventListener('change', async function() {
            const turmaId = this.value;
            
            if (!turmaId) {
                turmaInfoContainer.innerHTML = '';
                submitButton.disabled = false;
                return;
            }
            
            // Mostrar loading
            turmaInfoContainer.innerHTML = `
                <div class="alert alert-info d-flex align-items-center">
                    <div class="spinner-border spinner-border-sm me-2" role="status">
                        <span class="visually-hidden">Carregando...</span>
                    </div>
                    <span>Carregando informações da turma...</span>
                </div>
            `;
            
            try {
                const response = await fetch(`/matriculas/ajax/turma-info/${turmaId}/`);
                
                if (!response.ok) {
                    throw new Error('Erro ao buscar informações da turma');
                }
                
                const data = await response.json();
                
                // M4: Validar status da turma
                if (data.status !== 'A') {
                    turmaInfoContainer.innerHTML = `
                        <div class="alert alert-danger" role="alert">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            <strong>Atenção!</strong> Esta turma está <strong>${data.status_display}</strong>. 
                            Apenas turmas ativas podem receber matrículas.
                        </div>
                    `;
                    submitButton.disabled = true;
                    submitButton.title = 'Não é possível matricular em turma não ativa';
                    return;
                }
                
                // M7: Exibir informações da turma
                const vagasDisponiveisClass = data.vagas_disponiveis > 0 ? 'success' : 'danger';
                const vagasDisponiveis Text = data.vagas_disponiveis > 0 
                    ? `${data.vagas_disponiveis} vaga(s) disponível(is)` 
                    : 'Turma lotada';
                
                turmaInfoContainer.innerHTML = `
                    <div class="card border-${data.status === 'A' ? 'success' : 'danger'}">
                        <div class="card-body p-3">
                            <h6 class="card-title mb-2">
                                <i class="fas fa-info-circle me-1"></i> 
                                Informações da Turma
                            </h6>
                            <div class="row g-2 small">
                                <div class="col-md-6">
                                    <strong>Curso:</strong> ${data.curso}
                                </div>
                                <div class="col-md-6">
                                    <strong>Status:</strong> 
                                    <span class="badge bg-${data.status === 'A' ? 'success' : 'secondary'}">${data.status_display}</span>
                                </div>
                                <div class="col-md-6">
                                    <strong>Instrutor:</strong> ${data.instrutor}
                                </div>
                                <div class="col-md-6">
                                    <strong>Horário:</strong> ${data.dia_semana} - ${data.horario}
                                </div>
                                <div class="col-md-6">
                                    <strong>Local:</strong> ${data.local}
                                </div>
                                <div class="col-md-6">
                                    <strong>Vagas:</strong> ${data.vagas_ocupadas}/${data.vagas_total} 
                                    <span class="badge bg-${vagasDisponiveisClass}">${vagasDisponiveis Text}</span>
                                </div>
                                <div class="col-12">
                                    <div class="progress" style="height: 20px;">
                                        <div class="progress-bar bg-${data.percentual_ocupacao >= 90 ? 'danger' : 'success'}" 
                                             role="progressbar" 
                                             style="width: ${data.percentual_ocupacao}%"
                                             aria-valuenow="${data.percentual_ocupacao}" 
                                             aria-valuemin="0" 
                                             aria-valuemax="100">
                                            ${data.percentual_ocupacao}% ocupado
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                
                // Habilitar submit se turma está ativa
                submitButton.disabled = false;
                submitButton.title = '';
                
                // Avisar se turma está quase lotada
                if (data.vagas_disponiveis <= 0) {
                    turmaInfoContainer.insertAdjacentHTML('beforeend', `
                        <div class="alert alert-warning mt-2" role="alert">
                            <i class="fas fa-exclamation-circle me-2"></i>
                            <strong>Atenção!</strong> Esta turma não possui vagas disponíveis.
                        </div>
                    `);
                }
                
            } catch (error) {
                console.error('Erro ao carregar info da turma:', error);
                turmaInfoContainer.innerHTML = `
                    <div class="alert alert-danger" role="alert">
                        <i class="fas fa-times-circle me-2"></i>
                        Erro ao carregar informações da turma.
                    </div>
                `;
            }
        });
        
        // Disparar evento se já houver turma selecionada (modo edição)
        if (turmaSelect.value) {
            turmaSelect.dispatchEvent(new Event('change'));
        }
    }
    
    /**
     * M8: Exibição de informações do aluno em tempo real
     */
    if (alunoSelect) {
        alunoSelect.addEventListener('change', async function() {
            const alunoId = this.value;
            
            if (!alunoId) {
                alunoInfoContainer.innerHTML = '';
                return;
            }
            
            // Mostrar loading
            alunoInfoContainer.innerHTML = `
                <div class="alert alert-info d-flex align-items-center p-2">
                    <div class="spinner-border spinner-border-sm me-2" role="status">
                        <span class="visually-hidden">Carregando...</span>
                    </div>
                    <span class="small">Carregando dados do aluno...</span>
                </div>
            `;
            
            try {
                const response = await fetch(`/matriculas/ajax/aluno-info/${alunoId}/`);
                
                if (!response.ok) {
                    throw new Error('Erro ao buscar informações do aluno');
                }
                
                const data = await response.json();
                
                let html = `
                    <div class="card border-info">
                        <div class="card-body p-2">
                            <h6 class="card-title mb-2 small">
                                <i class="fas fa-user me-1"></i> 
                                Informações do Aluno
                            </h6>
                            <div class="small">
                                <div><strong>CPF:</strong> ${data.cpf}</div>
                                <div><strong>Grau Atual:</strong> 
                                    <span class="badge bg-primary">${data.grau_atual}</span>
                                </div>
                                <div><strong>Status:</strong> 
                                    <span class="badge bg-${data.status === 'Ativo' ? 'success' : 'secondary'}">${data.status}</span>
                                </div>
                `;
                
                // Avisar se aluno já está em outra turma ativa
                if (data.tem_turmas_ativas) {
                    html += `
                                <div class="alert alert-warning mt-2 mb-0 p-2" role="alert">
                                    <i class="fas fa-exclamation-triangle me-1"></i>
                                    <strong>Atenção!</strong> Este aluno já está matriculado em:
                                    <ul class="mb-0 mt-1 ps-3">
                    `;
                    data.turmas_ativas.forEach(turma => {
                        html += `<li><strong>${turma.nome}</strong> (desde ${turma.data_matricula})</li>`;
                    });
                    html += `
                                    </ul>
                                    <small class="d-block mt-1">A matrícula em múltiplas turmas ativas pode ser bloqueada pelo sistema.</small>
                                </div>
                    `;
                }
                
                html += `
                            </div>
                        </div>
                    </div>
                `;
                
                alunoInfoContainer.innerHTML = html;
                
            } catch (error) {
                console.error('Erro ao carregar info do aluno:', error);
                alunoInfoContainer.innerHTML = `
                    <div class="alert alert-danger p-2" role="alert">
                        <i class="fas fa-times-circle me-1"></i>
                        <small>Erro ao carregar informações do aluno.</small>
                    </div>
                `;
            }
        });
        
        // Disparar evento se já houver aluno selecionado (modo edição)
        if (alunoSelect.value) {
            alunoSelect.dispatchEvent(new Event('change'));
        }
    }
    
    /**
     * Validação adicional no submit
     */
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Verificar se turma e aluno foram selecionados
            if (!turmaSelect.value) {
                e.preventDefault();
                alert('Por favor, selecione uma turma.');
                turmaSelect.focus();
                return false;
            }
            
            if (!alunoSelect.value) {
                e.preventDefault();
                alert('Por favor, selecione um aluno.');
                alunoSelect.focus();
                return false;
            }
            
            // Desabilitar botão para evitar duplo submit
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Salvando...';
        });
    }
});
