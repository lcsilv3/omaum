// Script de feedback visual melhorado para registro de presenças
// Melhora a experiência do usuário com mensagens visuais claras

(function() {
    'use strict';
    
    // Mostrar indicador de "salvando" ao marcar presenças
    const originalSalvarDiaAtual = window.PresencaApp.salvarDiaAtual;
    window.PresencaApp.salvarDiaAtual = function() {
        // Mostrar feedback visual
        const modal = document.getElementById('presencaModal');
        const btnSalvar = modal?.querySelector('.btn-salvar-presenca');
        
        if (btnSalvar) {
            const textoOriginal = btnSalvar.innerHTML;
            btnSalvar.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Salvando...';
            btnSalvar.disabled = true;
            
            // Restaurar após a operação
            setTimeout(() => {
                btnSalvar.innerHTML = textoOriginal;
                btnSalvar.disabled = false;
            }, 300);
        }
        
        // Chamar função original
        originalSalvarDiaAtual.call(this);
    };
    
    // Melhorar visual ao marcar/desmarcar presenças
    const originalTogglePresenca = window.PresencaApp.togglePresencaAluno;
    window.PresencaApp.togglePresencaAluno = function(cpfAluno, botaoPresenca) {
        if (botaoPresenca) {
            botaoPresenca.style.transition = 'all 0.2s ease';
            botaoPresenca.style.transform = 'scale(0.95)';
            
            setTimeout(() => {
                botaoPresenca.style.transform = 'scale(1)';
            }, 100);
        }
        
        return originalTogglePresenca.call(this, cpfAluno, botaoPresenca);
    };
    
    // Adicionar feedback ao abrir modal
    const originalAbrirModal = window.PresencaApp.abrirModalPresenca;
    window.PresencaApp.abrirModalPresenca = function(atividadeId, dia) {
        // Chamar função original
        originalAbrirModal.call(this, atividadeId, dia);
        
        // Adicionar animação de entrada
        const modal = document.getElementById('presencaModal');
        if (modal) {
            modal.style.animation = 'fadeIn 0.3s ease';
            // Scroll para o topo do modal
            const modalBody = modal.querySelector('.modal-body');
            if (modalBody) {
                modalBody.scrollTop = 0;
            }
        }
    };
    
    // Adicionar feedback ao fechar modal
    const originalFecharModal = window.PresencaApp.fecharModalPresenca;
    window.PresencaApp.fecharModalPresenca = function() {
        const modal = document.getElementById('presencaModal');
        if (modal) {
            modal.style.animation = 'fadeOut 0.3s ease';
        }
        
        setTimeout(() => {
            originalFecharModal.call(this);
        }, 150);
    };
    
    // Melhorar feedback ao selecionar dias
    document.addEventListener('flatpickr-ready', function() {
        setTimeout(() => {
            const inputs = document.querySelectorAll('.dias-datepicker');
            inputs.forEach(input => {
                const parent = input.parentElement;
                if (parent) {
                    parent.style.transition = 'border-color 0.3s ease';
                    
                    input.addEventListener('focus', function() {
                        parent.style.borderColor = '#0d6efd';
                        parent.style.boxShadow = '0 0 0 0.2rem rgba(13, 110, 253, 0.25)';
                    });
                    
                    input.addEventListener('blur', function() {
                        parent.style.borderColor = '#ced4da';
                        parent.style.boxShadow = 'none';
                    });
                }
            });
        }, 500);
    });
    
    // Toast de notificação customizado
    window.PresencaApp.mostrarNotificacao = function(mensagem, tipo = 'info', duracao = 3000) {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 16px 20px;
            background-color: ${
                tipo === 'sucesso' ? '#198754' :
                tipo === 'erro' ? '#dc3545' :
                tipo === 'aviso' ? '#ffc107' :
                '#0dcaf0'
            };
            color: ${tipo === 'aviso' ? '#000' : '#fff'};
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 9999;
            animation: slideIn 0.3s ease;
            font-size: 14px;
            max-width: 300px;
        `;
        
        const icone = {
            'sucesso': 'check-circle',
            'erro': 'exclamation-circle',
            'aviso': 'exclamation-triangle',
            'info': 'info-circle'
        }[tipo] || 'info-circle';
        
        toast.innerHTML = `<i class="fas fa-${icone} me-2"></i>${mensagem}`;
        document.body.appendChild(toast);
        
        // Remover após duração
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, duracao);
    };
    
    // Adicionar estilos de animação
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        @keyframes slideIn {
            from { 
                transform: translateX(400px);
                opacity: 0;
            }
            to { 
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from { 
                transform: translateX(0);
                opacity: 1;
            }
            to { 
                transform: translateX(400px);
                opacity: 0;
            }
        }
        .btn:disabled {
            cursor: not-allowed;
            opacity: 0.6;
        }
        .badge-presenca {
            transition: all 0.2s ease;
            cursor: pointer;
            user-select: none;
        }
        .badge-presenca:hover {
            transform: scale(1.05);
        }
        .badge-presente {
            background-color: #198754 !important;
            color: white !important;
            border: 1px solid #198754;
        }
        .badge-ausente {
            background-color: #dc3545 !important;
            color: white !important;
            border: 1px solid #dc3545;
        }
    `;
    document.head.appendChild(style);
    
    console.log('✅ Feedback visual melhorado carregado com sucesso!');
})();
