/**
 * 🎯 LOGS DE DEBUG PARA CLIQUES NOS BOTÕES
 * 
 * INSTRUÇÕES:
 * 1. Abra a página de registrar presenças
 * 2. Abra o console do navegador (F12)
 * 3. Cole este código completo no console e pressione Enter
 * 4. Agora teste os botões - você verá logs detalhados de cada clique
 */

console.log('🎯 [DEBUG] ===== INSTALANDO LOGS DE CLIQUES =====');

// ===== INTERCEPTA CLIQUES NO BOTÃO FINALIZAR =====
document.addEventListener('DOMContentLoaded', function() {
    const btnFinalizar = document.querySelector('button[type="submit"]');
    if (btnFinalizar && btnFinalizar.textContent.includes('Finalizar')) {
        btnFinalizar.addEventListener('click', function(e) {
            console.log('🚀 [CLIQUE] ===================================');
            console.log('🚀 [CLIQUE] BOTÃO FINALIZAR REGISTRO CLICADO!');
            console.log('🚀 [CLIQUE] Hora:', new Date().toLocaleString());
            console.log('🚀 [CLIQUE] Texto do botão:', this.textContent.trim());
            console.log('🚀 [CLIQUE] ===================================');
        });
        console.log('✅ [DEBUG] Log instalado no botão Finalizar Registro');
    }
});

// ===== INTERCEPTA CLIQUES NOS BOTÕES DO MODAL =====
function interceptarModal() {
    const modal = document.getElementById('presencaModal');
    if (modal) {
        // Botão Salvar Presenças
        const btnSalvar = modal.querySelector('.btn-salvar-presenca');
        if (btnSalvar && !btnSalvar.hasAttribute('data-debug-log')) {
            btnSalvar.addEventListener('click', function(e) {
                console.log('💾 [CLIQUE] ===================================');
                console.log('💾 [CLIQUE] BOTÃO SALVAR PRESENÇAS CLICADO!');
                console.log('💾 [CLIQUE] Hora:', new Date().toLocaleString());
                console.log('💾 [CLIQUE] ===================================');
            });
            btnSalvar.setAttribute('data-debug-log', 'true');
            console.log('✅ [DEBUG] Log instalado no botão Salvar Presenças');
        }
        
        // Botão Cancelar
        const btnCancelar = modal.querySelector('.btn-secondary');
        if (btnCancelar && btnCancelar.textContent.includes('Cancelar') && !btnCancelar.hasAttribute('data-debug-log')) {
            btnCancelar.addEventListener('click', function(e) {
                console.log('❌ [CLIQUE] ===================================');
                console.log('❌ [CLIQUE] BOTÃO CANCELAR CLICADO!');
                console.log('❌ [CLIQUE] Hora:', new Date().toLocaleString());
                console.log('❌ [CLIQUE] ===================================');
            });
            btnCancelar.setAttribute('data-debug-log', 'true');
            console.log('✅ [DEBUG] Log instalado no botão Cancelar');
        }
    }
}

// Executa interceptação inicial
interceptarModal();

// Monitor contínuo para novos modais
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
            const modal = document.getElementById('presencaModal');
            if (modal && modal.style.display !== 'none') {
                setTimeout(interceptarModal, 100);
            }
        }
    });
});

const modal = document.getElementById('presencaModal');
if (modal) {
    observer.observe(modal, { attributes: true, attributeFilter: ['style'] });
    console.log('✅ [DEBUG] Monitor de modal instalado');
}

console.log('✅ [DEBUG] Todos os logs de cliques instalados!');
console.log('📋 [DEBUG] Agora teste os botões e veja os logs aqui no console.');

// Função global para reinstalar se necessário
window.reinstalarLogsDebug = function() {
    interceptarModal();
    console.log('🔄 [DEBUG] Logs reinstalados!');
};
