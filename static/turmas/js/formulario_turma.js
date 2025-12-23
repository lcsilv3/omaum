/**
 * Script para o formulário de turmas (criar e editar)
 * Baseado no padrão estabelecido em alunos/static/alunos/js/formulario_aluno.js
 */

document.addEventListener('DOMContentLoaded', function() {
    // ========================================================================
    // INICIALIZAÇÃO GERAL
    // ========================================================================
    
    console.log('[Turmas] Formulário inicializado');
    
    // Inicializa os acordeões (collapsibles)
    initializeCollapseToggles();
    
    // Aplica máscara no campo de horário
    initializeHorarioMask();
    
    // Validação customizada antes do submit
    initializeFormValidation();
    
    // ========================================================================
    // FUNÇÕES DE UI
    // ========================================================================
    
    /**
     * Inicializa os botões de colapso das seções
     */
    function initializeCollapseToggles() {
        document.querySelectorAll('.collapse-toggle').forEach(toggle => {
            toggle.addEventListener('click', function() {
                const chevron = this.querySelector('.chevron');
                setTimeout(() => {
                    chevron.style.transform = this.classList.contains('collapsed') 
                        ? 'rotate(0deg)' 
                        : 'rotate(90deg)';
                }, 150);
            });
        });
    }
    
    /**
     * Aplica máscara no campo de horário (HH:MM às HH:MM)
     */
    function initializeHorarioMask() {
        const horarioInput = document.getElementById('id_horario');
        if (!horarioInput) return;
        
        horarioInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, ''); // Remove tudo que não é dígito
            
            if (value.length >= 1) {
                // Primeiro dígito da hora inicial
                let formatted = value.substring(0, 2);
                
                if (value.length >= 3) {
                    // Adiciona : após HH
                    formatted += ':' + value.substring(2, 4);
                }
                
                if (value.length >= 5) {
                    // Adiciona " às "
                    formatted += ' às ' + value.substring(4, 6);
                }
                
                if (value.length >= 7) {
                    // Adiciona : após segundo HH
                    formatted += ':' + value.substring(6, 8);
                }
                
                e.target.value = formatted;
            }
        });
        
        // Adiciona placeholder interativo
        horarioInput.addEventListener('focus', function() {
            if (!this.value) {
                this.placeholder = 'Ex: 19:00 às 22:00';
            }
        });
    }
    
    /**
     * Validação customizada do formulário
     */
    function initializeFormValidation() {
        const form = document.getElementById('form-turma');
        if (!form) return;
        
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Validar horário (formato HH:MM às HH:MM)
            const horarioInput = document.getElementById('id_horario');
            if (horarioInput && horarioInput.value) {
                const horarioRegex = /^([0-1][0-9]|2[0-3]):[0-5][0-9] às ([0-1][0-9]|2[0-3]):[0-5][0-9]$/;
                if (!horarioRegex.test(horarioInput.value)) {
                    horarioInput.classList.add('is-invalid');
                    showFieldError(horarioInput, 'Formato inválido. Use HH:MM às HH:MM (ex: 19:00 às 22:00)');
                    isValid = false;
                } else {
                    horarioInput.classList.remove('is-invalid');
                    removeFieldError(horarioInput);
                }
            }
            
            // Validar vagas (deve ser maior que 0)
            const vagasInput = document.getElementById('id_vagas');
            if (vagasInput && vagasInput.value) {
                const vagas = parseInt(vagasInput.value);
                if (vagas <= 0) {
                    vagasInput.classList.add('is-invalid');
                    showFieldError(vagasInput, 'O número de vagas deve ser maior que zero.');
                    isValid = false;
                } else {
                    vagasInput.classList.remove('is-invalid');
                    removeFieldError(vagasInput);
                }
            }
            
            // Validar percentual de presença (0-100)
            const percInput = document.getElementById('id_perc_presenca_minima');
            if (percInput && percInput.value) {
                const perc = parseInt(percInput.value);
                if (perc < 0 || perc > 100) {
                    percInput.classList.add('is-invalid');
                    showFieldError(percInput, 'O percentual deve estar entre 0 e 100.');
                    isValid = false;
                } else {
                    percInput.classList.remove('is-invalid');
                    removeFieldError(percInput);
                }
            }
            
            if (!isValid) {
                e.preventDefault();
                // Scroll para o primeiro erro
                const firstError = document.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    }
    
    /**
     * Mostra mensagem de erro em um campo
     */
    function showFieldError(field, message) {
        // Remove erro anterior se existir
        removeFieldError(field);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }
    
    /**
     * Remove mensagem de erro de um campo
     */
    function removeFieldError(field) {
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    // ========================================================================
    // DESTAQUE DE CAMPOS COM ERRO AO CARREGAR A PÁGINA
    // ========================================================================
    
    // Adiciona classe is-invalid APENAS aos campos que têm mensagens de erro reais
    // (não considera asteriscos de campos obrigatórios como erro)
    document.querySelectorAll('.errorlist').forEach(errorElement => {
        const field = errorElement.closest('.mb-3, .col-md-6, .col-md-4, .col-12')?.querySelector('input, select, textarea');
        if (field) {
            field.classList.add('is-invalid');
            field.setAttribute('aria-invalid', 'true');
        }
    });
    
    // Procura por mensagens de erro específicas do Django (invalid-feedback)
    document.querySelectorAll('.invalid-feedback:not(:empty)').forEach(errorElement => {
        const field = errorElement.previousElementSibling;
        if (field && (field.tagName === 'INPUT' || field.tagName === 'SELECT' || field.tagName === 'TEXTAREA')) {
            field.classList.add('is-invalid');
            field.setAttribute('aria-invalid', 'true');
        }
    });
    
    // Marca o card com borda vermelha se houver erros REAIS nele
    document.querySelectorAll('.card').forEach(card => {
        if (card.querySelector('.is-invalid, .errorlist')) {
            card.classList.add('border-danger');
            
            // Adiciona badge de erro no header
            const header = card.querySelector('.card-header h5');
            if (header && !header.querySelector('.badge-error')) {
                const badge = document.createElement('span');
                badge.className = 'badge bg-danger ms-2 badge-error';
                badge.innerHTML = '<i class="fas fa-exclamation-circle"></i> Erro';
                header.appendChild(badge);
            }
            
            // Expande o card automaticamente
            const collapseDiv = card.querySelector('.collapse');
            if (collapseDiv && !collapseDiv.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(collapseDiv, { toggle: true });
            }
        }
    });
});
