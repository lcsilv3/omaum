/**
 * 🎯 DEBUG: LOGS PARA CLIQUES NOS BOTÕES
 * 
 * Este script adiciona logs detalhados para confirmar que você está clicando nos botões.
 * 
 * INSTRUÇÕES:
 * 1. Abra a página de registrar presenças
 * 2. Abra o console (F12)
 * 3. Cole este script no console e pressione Enter
 * 4. Os logs aparecerão sempre que você clicar nos botões
 */

console.log('🎯 [DEBUG-CLIQUES] ===== INSTALANDO LOGS DE CLIQUES =====');

// ===== 1. LOG PARA BOTÃO SALVAR PRESENÇAS (MODAL) =====
function instalarLogBotaoSalvarModal() {
    console.log('🔍 [DEBUG-CLIQUES] Procurando botão "Salvar Presenças" do modal...');
    
    // Aguarda o modal aparecer
    const verificarModal = setInterval(() => {
        const modal = document.getElementById('presencaModal');
        if (modal && modal.style.display !== 'none') {
            const btnSalvar = modal.querySelector('.btn-salvar-presenca');
            if (btnSalvar && !btnSalvar.hasAttribute('data-debug-instalado')) {
                console.log('✅ [DEBUG-CLIQUES] Botão "Salvar Presenças" encontrado!');
                
                // Salva a função original
                const onclickOriginal = btnSalvar.getAttribute('onclick');
                const funcaoOriginal = btnSalvar.onclick;
                
                // Instala interceptador
                btnSalvar.removeAttribute('onclick');
                btnSalvar.onclick = function(e) {
                    console.log('🔥 [DEBUG-CLIQUES] ========================================');
                    console.log('🔥 [DEBUG-CLIQUES] BOTÃO "SALVAR PRESENÇAS" CLICADO!');
                    console.log('🔥 [DEBUG-CLIQUES] Timestamp:', new Date().toLocaleString());
                    console.log('🔥 [DEBUG-CLIQUES] Event:', e);
                    console.log('🔥 [DEBUG-CLIQUES] Botão:', this);
                    console.log('🔥 [DEBUG-CLIQUES] onclick original:', onclickOriginal);
                    console.log('🔥 [DEBUG-CLIQUES] ========================================');
                    
                    // Chama a função original
                    if (funcaoOriginal) {
                        console.log('🔥 [DEBUG-CLIQUES] Executando função original (onclick)...');
                        return funcaoOriginal.call(this, e);
                    } else if (onclickOriginal) {
                        console.log('🔥 [DEBUG-CLIQUES] Executando onclick original (string)...');
                        return eval(onclickOriginal);
                    } else {
                        console.log('🔥 [DEBUG-CLIQUES] Tentando chamar PresencaManager.salvarDiaAtual()...');
                        if (window.PresencaManager && window.PresencaManager.salvarDiaAtual) {
                            return window.PresencaManager.salvarDiaAtual();
                        }
                    }
                };
                
                btnSalvar.setAttribute('data-debug-instalado', 'true');
                clearInterval(verificarModal);
                console.log('✅ [DEBUG-CLIQUES] Interceptador instalado no botão "Salvar Presenças"!');
            }
        }
    }, 500);
    
    // Para o verificador após 30 segundos
    setTimeout(() => {
        clearInterval(verificarModal);
    }, 30000);
}

// ===== 2. LOG PARA BOTÃO FINALIZAR REGISTRO COMPLETO =====
function instalarLogBotaoFinalizar() {
    console.log('🔍 [DEBUG-CLIQUES] Procurando botão "Finalizar Registro Completo"...');
    
    const btnFinalizar = document.querySelector('button[type="submit"]');
    if (btnFinalizar && btnFinalizar.textContent.includes('Finalizar')) {
        console.log('✅ [DEBUG-CLIQUES] Botão "Finalizar Registro Completo" encontrado!');
        
        // Adiciona event listener para capture e bubble
        btnFinalizar.addEventListener('click', function(e) {
            console.log('🚀 [DEBUG-CLIQUES] ========================================');
            console.log('🚀 [DEBUG-CLIQUES] BOTÃO "FINALIZAR REGISTRO" CLICADO!');
            console.log('🚀 [DEBUG-CLIQUES] Timestamp:', new Date().toLocaleString());
            console.log('🚀 [DEBUG-CLIQUES] Event:', e);
            console.log('🚀 [DEBUG-CLIQUES] Botão:', this);
            console.log('🚀 [DEBUG-CLIQUES] Formulário será enviado...');
            console.log('🚀 [DEBUG-CLIQUES] ========================================');
        }, true); // true = capture phase
        
        btnFinalizar.addEventListener('click', function(e) {
            console.log('🎯 [DEBUG-CLIQUES] Bubble phase - Finalizar clicado novamente');
        }, false); // false = bubble phase
        
        console.log('✅ [DEBUG-CLIQUES] Interceptadores instalados no botão "Finalizar"!');
    } else {
        console.log('❌ [DEBUG-CLIQUES] Botão "Finalizar Registro Completo" NÃO encontrado!');
        
        // Lista todos os botões submit para debug
        const botoesSubmit = document.querySelectorAll('button[type="submit"]');
        console.log('🔍 [DEBUG-CLIQUES] Botões submit encontrados:', botoesSubmit.length);
        botoesSubmit.forEach((btn, index) => {
            console.log(`🔍 [DEBUG-CLIQUES] Botão ${index}:`, btn.textContent.trim());
        });
    }
}

// ===== 3. LOG PARA BOTÃO CANCELAR (MODAL) =====
function instalarLogBotaoCancelar() {
    console.log('🔍 [DEBUG-CLIQUES] Instalando log para botão "Cancelar" do modal...');
    
    // Aguarda o modal aparecer
    const verificarModal = setInterval(() => {
        const modal = document.getElementById('presencaModal');
        if (modal && modal.style.display !== 'none') {
            const btnCancelar = modal.querySelector('.btn-secondary');
            if (btnCancelar && btnCancelar.textContent.includes('Cancelar') && !btnCancelar.hasAttribute('data-debug-cancelar-instalado')) {
                console.log('✅ [DEBUG-CLIQUES] Botão "Cancelar" encontrado!');
                
                // Salva a função original
                const onclickOriginal = btnCancelar.getAttribute('onclick');
                const funcaoOriginal = btnCancelar.onclick;
                
                // Instala interceptador
                btnCancelar.removeAttribute('onclick');
                btnCancelar.onclick = function(e) {
                    console.log('❌ [DEBUG-CLIQUES] ========================================');
                    console.log('❌ [DEBUG-CLIQUES] BOTÃO "CANCELAR" CLICADO!');
                    console.log('❌ [DEBUG-CLIQUES] Timestamp:', new Date().toLocaleString());
                    console.log('❌ [DEBUG-CLIQUES] Event:', e);
                    console.log('❌ [DEBUG-CLIQUES] Modal será fechado...');
                    console.log('❌ [DEBUG-CLIQUES] ========================================');
                    
                    // Chama a função original
                    if (funcaoOriginal) {
                        return funcaoOriginal.call(this, e);
                    } else if (onclickOriginal) {
                        return eval(onclickOriginal);
                    } else {
                        console.log('❌ [DEBUG-CLIQUES] Tentando chamar PresencaManager.fecharModal()...');
                        if (window.PresencaManager && window.PresencaManager.fecharModal) {
                            return window.PresencaManager.fecharModal();
                        }
                    }
                };
                
                btnCancelar.setAttribute('data-debug-cancelar-instalado', 'true');
                clearInterval(verificarModal);
                console.log('✅ [DEBUG-CLIQUES] Interceptador instalado no botão "Cancelar"!');
            }
        }
    }, 500);
    
    // Para o verificador após 30 segundos
    setTimeout(() => {
        clearInterval(verificarModal);
    }, 30000);
}

// ===== 4. MONITOR CONTÍNUO PARA MODAIS NOVOS =====
function monitorarModalNovo() {
    console.log('👁️ [DEBUG-CLIQUES] Iniciando monitor contínuo para novos modais...');
    
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                const modal = document.getElementById('presencaModal');
                if (modal && modal.style.display !== 'none' && modal.classList.contains('show')) {
                    console.log('👁️ [DEBUG-CLIQUES] Novo modal detectado! Instalando logs...');
                    setTimeout(() => {
                        instalarLogBotaoSalvarModal();
                        instalarLogBotaoCancelar();
                    }, 100);
                }
            }
        });
    });
    
    const modal = document.getElementById('presencaModal');
    if (modal) {
        observer.observe(modal, { 
            attributes: true, 
            attributeFilter: ['style', 'class'] 
        });
        console.log('✅ [DEBUG-CLIQUES] Observer instalado!');
    }
}

// ===== EXECUÇÃO =====
console.log('🚀 [DEBUG-CLIQUES] Iniciando instalação dos logs...');

// Instala log no botão finalizar (sempre disponível)
instalarLogBotaoFinalizar();

// Instala logs no modal se estiver aberto
instalarLogBotaoSalvarModal();
instalarLogBotaoCancelar();

// Inicia monitor contínuo
monitorarModalNovo();

console.log('✅ [DEBUG-CLIQUES] Todos os logs de cliques foram instalados!');
console.log('📋 [DEBUG-CLIQUES] Agora teste os botões e observe os logs no console.');

// ===== FUNÇÃO GLOBAL PARA REINSTALAR =====
window.reinstalarLogsCliques = function() {
    console.log('🔄 [DEBUG-CLIQUES] Reinstalando logs de cliques...');
    instalarLogBotaoFinalizar();
    instalarLogBotaoSalvarModal();
    instalarLogBotaoCancelar();
    console.log('✅ [DEBUG-CLIQUES] Logs reinstalados!');
};

console.log('🎯 [DEBUG-CLIQUES] Use window.reinstalarLogsCliques() se precisar reinstalar os logs.');
