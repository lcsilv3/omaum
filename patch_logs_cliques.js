/**
 * 🎯 PATCH: ADICIONA LOGS DE DEBUG AOS CLIQUES
 * 
 * Este script adiciona logs adicionais às funções principais para debug.
 * Cole no console do navegador após carregar a página.
 */

console.log('🎯 [PATCH] Aplicando logs de debug aos cliques...');

// Patch para PresencaManager.fecharModal
if (window.PresencaManager && window.PresencaManager.fecharModal) {
    const originalFecharModal = window.PresencaManager.fecharModal;
    
    window.PresencaManager.fecharModal = function() {
        // 🎯 LOG DE DEBUG PARA CLIQUE NO BOTÃO CANCELAR
        console.log('❌ [DEBUG-CLIQUE] ========================================');
        console.log('❌ [DEBUG-CLIQUE] BOTÃO "CANCELAR" FOI CLICADO!');
        console.log('❌ [DEBUG-CLIQUE] Timestamp:', new Date().toLocaleString());
        console.log('❌ [DEBUG-CLIQUE] Função fecharModal() chamada');
        console.log('❌ [DEBUG-CLIQUE] ========================================');
        
        // Chama a função original
        return originalFecharModal.call(this);
    };
    
    console.log('✅ [PATCH] Log instalado em PresencaManager.fecharModal');
} else {
    console.log('❌ [PATCH] PresencaManager.fecharModal não encontrado');
}

// Patch para PresencaManager.salvarDiaAtual (adicional)
if (window.PresencaManager && window.PresencaManager.salvarDiaAtual) {
    const originalSalvarDiaAtual = window.PresencaManager.salvarDiaAtual;
    
    window.PresencaManager.salvarDiaAtual = function() {
        // 🎯 LOG DE DEBUG ADICIONAL PARA CLIQUE NO BOTÃO SALVAR
        console.log('🔥 [DEBUG-CLIQUE-PATCH] ========================================');
        console.log('🔥 [DEBUG-CLIQUE-PATCH] BOTÃO "SALVAR PRESENÇAS" CLICADO (PATCH)!');
        console.log('🔥 [DEBUG-CLIQUE-PATCH] Timestamp:', new Date().toLocaleString());
        console.log('🔥 [DEBUG-CLIQUE-PATCH] Função salvarDiaAtual() chamada via patch');
        console.log('🔥 [DEBUG-CLIQUE-PATCH] ========================================');
        
        // Chama a função original
        return originalSalvarDiaAtual.call(this);
    };
    
    console.log('✅ [PATCH] Log adicional instalado em PresencaManager.salvarDiaAtual');
} else {
    console.log('❌ [PATCH] PresencaManager.salvarDiaAtual não encontrado');
}

// Patch para função global fecharModalPresenca (compatibilidade)
if (window.fecharModalPresenca) {
    const originalFecharModalPresencaGlobal = window.fecharModalPresenca;
    
    window.fecharModalPresenca = function() {
        console.log('❌ [DEBUG-CLIQUE-GLOBAL] ========================================');
        console.log('❌ [DEBUG-CLIQUE-GLOBAL] FUNÇÃO GLOBAL fecharModalPresenca() CHAMADA!');
        console.log('❌ [DEBUG-CLIQUE-GLOBAL] Timestamp:', new Date().toLocaleString());
        console.log('❌ [DEBUG-CLIQUE-GLOBAL] ========================================');
        
        return originalFecharModalPresencaGlobal.call(this);
    };
    
    console.log('✅ [PATCH] Log instalado em função global fecharModalPresenca');
} else {
    console.log('❌ [PATCH] Função global fecharModalPresenca não encontrada');
}

console.log('✅ [PATCH] Todos os patches de debug aplicados!');
console.log('📋 [PATCH] Agora teste os botões e observe os logs no console.');
