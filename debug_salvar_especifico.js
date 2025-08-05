/**
 * 🎯 DEBUG ESPECÍFICO: FOCA NO BOTÃO "SALVAR PRESENÇAS"
 * 
 * Este script intercepta especificamente o botão "Salvar Presenças"
 * para descobrir por que os dados não chegam ao Django
 */

console.log('🎯 [DEBUG-SALVAR] ===== INTERCEPTADOR ESPECÍFICO PARA SALVAR =====');

// ===== INTERCEPTA FETCH =====
const originalFetch = window.fetch;
window.fetch = function(...args) {
    console.log('🚨 [FETCH-CRITICAL] ===================================');
    console.log('🚨 [FETCH-CRITICAL] *** REQUISIÇÃO CRÍTICA INTERCEPTADA! ***');
    console.log('🚨 [FETCH-CRITICAL] URL:', args[0]);
    console.log('🚨 [FETCH-CRITICAL] Method:', args[1]?.method || 'GET');
    console.log('🚨 [FETCH-CRITICAL] Headers:', args[1]?.headers);
    console.log('🚨 [FETCH-CRITICAL] Body type:', typeof args[1]?.body);
    console.log('🚨 [FETCH-CRITICAL] Body content:', args[1]?.body);
    console.log('🚨 [FETCH-CRITICAL] ===================================');
    
    return originalFetch.apply(this, args).then(response => {
        console.log('📥 [RESPONSE-CRITICAL] ===================================');
        console.log('📥 [RESPONSE-CRITICAL] *** RESPOSTA CRÍTICA! ***');
        console.log('📥 [RESPONSE-CRITICAL] Status:', response.status);
        console.log('📥 [RESPONSE-CRITICAL] URL:', args[0]);
        console.log('📥 [RESPONSE-CRITICAL] ===================================');
        return response;
    });
};

// ===== INTERCEPTA ESPECIFICAMENTE O BOTÃO SALVAR =====
document.addEventListener('click', function(e) {
    const target = e.target;
    const text = target.textContent?.trim() || '';
    
    if (text.includes('Salvar') && text.includes('Presenças')) {
        console.log('🔥🔥🔥 [SALVAR-CRÍTICO] ===================================');
        console.log('🔥🔥🔥 [SALVAR-CRÍTICO] *** BOTÃO SALVAR PRESENÇAS CLICADO! ***');
        console.log('🔥🔥🔥 [SALVAR-CRÍTICO] Texto completo:', text);
        console.log('🔥🔥🔥 [SALVAR-CRÍTICO] ID:', target.id);
        console.log('🔥🔥🔥 [SALVAR-CRÍTICO] Classes:', target.className);
        console.log('🔥🔥🔥 [SALVAR-CRÍTICO] onclick:', target.getAttribute('onclick'));
        console.log('🔥🔥🔥 [SALVAR-CRÍTICO] Função chamada:', target.getAttribute('onclick'));
        console.log('🔥🔥🔥 [SALVAR-CRÍTICO] Element:', target);
        console.log('🔥🔥🔥 [SALVAR-CRÍTICO] ===================================');
        
        // Tenta interceptar a função que será chamada
        if (target.getAttribute('onclick')) {
            console.log('🎯 [SALVAR-CRÍTICO] Função onclick detectada:', target.getAttribute('onclick'));
        }
    }
}, true);

// ===== MONITORA FUNÇÃO ESPECÍFICA DO PRESENÇA MANAGER =====
if (window.PresencaManager && window.PresencaManager.salvarDiaAtual) {
    const originalSalvar = window.PresencaManager.salvarDiaAtual;
    window.PresencaManager.salvarDiaAtual = function(...args) {
        console.log('🚨🚨🚨 [SALVAR-INTERCEPTED] ===================================');
        console.log('🚨🚨🚨 [SALVAR-INTERCEPTED] *** FUNÇÃO salvarDiaAtual() CHAMADA! ***');
        console.log('🚨🚨🚨 [SALVAR-INTERCEPTED] Arguments:', args);
        console.log('🚨🚨🚨 [SALVAR-INTERCEPTED] Timestamp:', new Date().toLocaleString());
        console.log('🚨🚨🚨 [SALVAR-INTERCEPTED] ===================================');
        
        const result = originalSalvar.apply(this, args);
        
        console.log('✅ [SALVAR-INTERCEPTED] Função executada, resultado:', result);
        return result;
    };
    console.log('✅ [DEBUG-SALVAR] Interceptador instalado na função salvarDiaAtual()');
} else {
    console.log('⚠️ [DEBUG-SALVAR] PresencaManager.salvarDiaAtual não encontrado ainda');
}

// ===== VERIFICA PERIODICAMENTE SE A FUNÇÃO EXISTE =====
let tentativas = 0;
const verificarFuncao = setInterval(() => {
    tentativas++;
    if (window.PresencaManager && window.PresencaManager.salvarDiaAtual && !window.PresencaManager.salvarDiaAtual.toString().includes('INTERCEPTED')) {
        const originalSalvar = window.PresencaManager.salvarDiaAtual;
        window.PresencaManager.salvarDiaAtual = function(...args) {
            console.log('🚨🚨🚨 [SALVAR-INTERCEPTED] ===================================');
            console.log('🚨🚨🚨 [SALVAR-INTERCEPTED] *** FUNÇÃO salvarDiaAtual() CHAMADA! ***');
            console.log('🚨🚨🚨 [SALVAR-INTERCEPTED] Arguments:', args);
            console.log('🚨🚨🚨 [SALVAR-INTERCEPTED] Timestamp:', new Date().toLocaleString());
            console.log('🚨🚨🚨 [SALVAR-INTERCEPTED] ===================================');
            
            const result = originalSalvar.apply(this, args);
            
            console.log('✅ [SALVAR-INTERCEPTED] Função executada, resultado:', result);
            return result;
        };
        console.log('✅ [DEBUG-SALVAR] Interceptador instalado na função salvarDiaAtual() (tentativa', tentativas, ')');
        clearInterval(verificarFuncao);
    } else if (tentativas > 20) {
        console.log('❌ [DEBUG-SALVAR] Não foi possível interceptar salvarDiaAtual após 20 tentativas');
        clearInterval(verificarFuncao);
    }
}, 500);

console.log('✅ [DEBUG-SALVAR] Interceptador específico instalado!');
console.log('🎯 [DEBUG-SALVAR] Agora clique em "Salvar Presenças" e veja os logs detalhados!');
