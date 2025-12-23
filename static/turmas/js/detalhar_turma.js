/**
 * Script para a página de detalhes da turma
 * Baseado no padrão estabelecido em alunos/static/alunos/js/detalhar_aluno.js
 */

document.addEventListener('DOMContentLoaded', function() {
    // ========================================================================
    // INICIALIZAÇÃO
    // ========================================================================
    
    console.log('[Turmas] Detalhes da turma inicializado');
    
    // Inicializa os botões de controle global
    initializeGlobalControls();
    
    // Inicializa os acordeões (collapsibles)
    initializeCollapseToggles();
    
    // ========================================================================
    // CONTROLES GLOBAIS
    // ========================================================================
    
    /**
     * Inicializa os botões "Expandir tudo" e "Recolher tudo"
     */
    function initializeGlobalControls() {
        const btnExpandir = document.getElementById('btn-expandir-secoes');
        const btnRecolher = document.getElementById('btn-recolher-secoes');
        
        if (btnExpandir) {
            btnExpandir.addEventListener('click', function() {
                expandirTodasSecoes();
            });
        }
        
        if (btnRecolher) {
            btnRecolher.addEventListener('click', function() {
                recolherTodasSecoes();
            });
        }
    }
    
    /**
     * Expande todas as seções recolhíveis
     */
    function expandirTodasSecoes() {
        document.querySelectorAll('.collapse').forEach(collapse => {
            if (!collapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(collapse, { toggle: true });
            }
        });
        
        // Atualiza os chevrons
        setTimeout(() => {
            document.querySelectorAll('.chevron').forEach(chevron => {
                chevron.style.transform = 'rotate(90deg)';
            });
        }, 350);
    }
    
    /**
     * Recolhe todas as seções recolhíveis
     */
    function recolherTodasSecoes() {
        document.querySelectorAll('.collapse').forEach(collapse => {
            if (collapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(collapse, { toggle: true });
            }
        });
        
        // Atualiza os chevrons
        setTimeout(() => {
            document.querySelectorAll('.chevron').forEach(chevron => {
                chevron.style.transform = 'rotate(0deg)';
            });
        }, 350);
    }
    
    /**
     * Inicializa os botões de colapso das seções
     */
    function initializeCollapseToggles() {
        document.querySelectorAll('.collapse-toggle').forEach(toggle => {
            toggle.addEventListener('click', function() {
                const chevron = this.querySelector('.chevron');
                const targetId = this.getAttribute('href');
                const target = document.querySelector(targetId);
                
                setTimeout(() => {
                    if (target && target.classList.contains('show')) {
                        chevron.style.transform = 'rotate(90deg)';
                    } else {
                        chevron.style.transform = 'rotate(0deg)';
                    }
                }, 350);
            });
        });
    }
    
    // ========================================================================
    // TOOLTIPS E POPOVERS (se necessário no futuro)
    // ========================================================================
    
    // Inicializa tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
