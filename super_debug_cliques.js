/**
 * 🔍 SUPER DEBUG: INTERCEPTA TODOS OS CLIQUES E REQUESTS
 * 
 * INSTRUÇÕES:
 * 1. Abra a página de registrar presenças
 * 2. Abra o console do navegador (F12)
 * 3. Cole este código completo no console e pressione Enter
 * 4. Teste os botões - você verá logs SUPER detalhados de tudo
 */

console.log('🔍 [SUPER-DEBUG] ===== INSTALANDO INTERCEPTADORES COMPLETOS =====');

// ===== INTERCEPTA TODAS AS REQUISIÇÕES FETCH =====
const originalFetch = window.fetch;
window.fetch = function(...args) {
    console.log('🌐 [FETCH] ===================================');
    console.log('🌐 [FETCH] REQUISIÇÃO INTERCEPTADA!');
    console.log('🌐 [FETCH] URL:', args[0]);
    console.log('🌐 [FETCH] Options:', args[1]);
    console.log('🌐 [FETCH] Timestamp:', new Date().toLocaleString());
    
    // Se for FormData, tenta listar os dados
    if (args[1] && args[1].body instanceof FormData) {
        console.log('📋 [FETCH] Dados do FormData:');
        for (let [key, value] of args[1].body.entries()) {
            console.log(`📋 [FETCH] ${key}:`, value);
        }
    }
    
    // Se for JSON, tenta mostrar o conteúdo
    if (args[1] && args[1].body && typeof args[1].body === 'string') {
        console.log('📋 [FETCH] Dados JSON enviados:');
        try {
            const jsonData = JSON.parse(args[1].body);
            console.log('📋 [FETCH] JSON:', JSON.stringify(jsonData, null, 2));
        } catch (e) {
            console.log('📋 [FETCH] String:', args[1].body);
        }
    }
    
    // Se tiver headers, mostra também
    if (args[1] && args[1].headers) {
        console.log('📋 [FETCH] Headers:');
        if (args[1].headers instanceof Headers) {
            for (let [key, value] of args[1].headers.entries()) {
                console.log(`📋 [FETCH] ${key}: ${value}`);
            }
        } else {
            console.log('📋 [FETCH] Headers object:', args[1].headers);
        }
    }
    
    console.log('🌐 [FETCH] ===================================');
    
    return originalFetch.apply(this, args).then(response => {
        console.log('📥 [FETCH-RESPONSE] ===================================');
        console.log('📥 [FETCH-RESPONSE] RESPOSTA RECEBIDA!');
        console.log('📥 [FETCH-RESPONSE] URL:', args[0]);
        console.log('📥 [FETCH-RESPONSE] Status:', response.status);
        console.log('📥 [FETCH-RESPONSE] StatusText:', response.statusText);
        
        // Intercepta e lê o conteúdo da resposta
        const clonedResponse = response.clone();
        clonedResponse.text().then(responseText => {
            console.log('📄 [FETCH-CONTENT] ===================================');
            console.log('📄 [FETCH-CONTENT] CONTEÚDO DA RESPOSTA:');
            console.log('📄 [FETCH-CONTENT] URL:', args[0]);
            try {
                const jsonData = JSON.parse(responseText);
                console.log('📄 [FETCH-CONTENT] JSON:', JSON.stringify(jsonData, null, 2));
            } catch (e) {
                console.log('📄 [FETCH-CONTENT] TEXT:', responseText.substring(0, 500));
                if (responseText.length > 500) {
                    console.log('📄 [FETCH-CONTENT] (texto truncado, total:', responseText.length, 'chars)');
                }
            }
            console.log('📄 [FETCH-CONTENT] ===================================');
        }).catch(err => {
            console.log('❌ [FETCH-CONTENT] Erro ao ler resposta:', err);
        });
        
        console.log('📥 [FETCH-RESPONSE] ===================================');
        return response;
    }).catch(error => {
        console.log('❌ [FETCH-ERROR] ===================================');
        console.log('❌ [FETCH-ERROR] ERRO NA REQUISIÇÃO!');
        console.log('❌ [FETCH-ERROR] URL:', args[0]);
        console.log('❌ [FETCH-ERROR] Error:', error);
        console.log('❌ [FETCH-ERROR] ===================================');
        throw error;
    });
};

// ===== INTERCEPTA SUBMIT DE FORMULÁRIOS =====
document.addEventListener('submit', function(e) {
    console.log('📤 [FORM-SUBMIT] ===================================');
    console.log('📤 [FORM-SUBMIT] FORMULÁRIO ENVIADO!');
    console.log('📤 [FORM-SUBMIT] Form ID:', e.target.id);
    console.log('📤 [FORM-SUBMIT] Form action:', e.target.action);
    console.log('📤 [FORM-SUBMIT] Form method:', e.target.method);
    console.log('📤 [FORM-SUBMIT] Event:', e);
    console.log('📤 [FORM-SUBMIT] Timestamp:', new Date().toLocaleString());
    
    // Lista todos os campos do formulário
    const formData = new FormData(e.target);
    console.log('📋 [FORM-SUBMIT] Dados do formulário:');
    for (let [key, value] of formData.entries()) {
        if (key.includes('json')) {
            try {
                const parsed = JSON.parse(value);
                console.log(`📋 [FORM-SUBMIT] ${key}:`, JSON.stringify(parsed, null, 2));
            } catch (err) {
                console.log(`📋 [FORM-SUBMIT] ${key}: (não é JSON)`, value);
            }
        } else {
            console.log(`📋 [FORM-SUBMIT] ${key}:`, value);
        }
    }
    console.log('📤 [FORM-SUBMIT] ===================================');
}, true);

// ===== INTERCEPTA TODOS OS CLIQUES =====
document.addEventListener('click', function(e) {
    const target = e.target;
    
    // Se for um botão importante, loga detalhadamente
    if (target.tagName === 'BUTTON' || target.type === 'submit' || 
        target.classList.contains('btn') ||
        target.textContent.includes('Finalizar') ||
        target.textContent.includes('Confirmar') ||
        target.textContent.includes('Salvar') ||
        target.textContent.includes('Cancelar')) {
        
        console.log('🎯 [CLICK] ===================================');
        console.log('🎯 [CLICK] BOTÃO CLICADO!');
        console.log('🎯 [CLICK] Texto:', target.textContent.trim());
        console.log('🎯 [CLICK] ID:', target.id);
        console.log('🎯 [CLICK] Classes:', target.className);
        console.log('🎯 [CLICK] Type:', target.type);
        console.log('🎯 [CLICK] onclick:', target.getAttribute('onclick'));
        console.log('🎯 [CLICK] Element:', target);
        console.log('🎯 [CLICK] Timestamp:', new Date().toLocaleString());
        console.log('🎯 [CLICK] ===================================');
    }
}, true);

// ===== MONITORA MUDANÇAS NO DOM (MODAIS) =====
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'attributes') {
            const target = mutation.target;
            if (target.id && (target.id.includes('modal') || target.id.includes('Modal'))) {
                console.log('👁️ [DOM] ===================================');
                console.log('👁️ [DOM] MODAL MODIFICADO!');
                console.log('👁️ [DOM] Modal ID:', target.id);
                console.log('👁️ [DOM] Attribute changed:', mutation.attributeName);
                console.log('👁️ [DOM] New value:', target.getAttribute(mutation.attributeName));
                console.log('👁️ [DOM] Display:', target.style.display);
                console.log('👁️ [DOM] Classes:', target.className);
                console.log('👁️ [DOM] ===================================');
                
                // Intercepta botões do modal de confirmação especificamente
                if (target.id === 'modal-confirmacao-finalizacao' && target.style.display === 'block') {
                    setTimeout(() => {
                        console.log('🎯 [MODAL-CONF] Modal de confirmação aberto! Interceptando botões...');
                        
                        const btnConfirmar = target.querySelector('.btn-confirmar');
                        const btnCancelar = target.querySelector('.btn-cancelar');
                        
                        if (btnConfirmar && !btnConfirmar.hasAttribute('data-intercepted')) {
                            btnConfirmar.addEventListener('click', function(e) {
                                console.log('🔥 [INTERCEPT] ===================================');
                                console.log('🔥 [INTERCEPT] BOTÃO CONFIRMAR ENVIO INTERCEPTADO!');
                                console.log('🔥 [INTERCEPT] Timestamp:', new Date().toLocaleString());
                                console.log('🔥 [INTERCEPT] Element:', this);
                                console.log('🔥 [INTERCEPT] Event:', e);
                                console.log('🔥 [INTERCEPT] ===================================');
                            }, true);
                            btnConfirmar.setAttribute('data-intercepted', 'true');
                            console.log('✅ [MODAL-CONF] Interceptador instalado no botão Confirmar Envio');
                        }
                        
                        if (btnCancelar && !btnCancelar.hasAttribute('data-intercepted')) {
                            btnCancelar.addEventListener('click', function(e) {
                                console.log('❌ [INTERCEPT] ===================================');
                                console.log('❌ [INTERCEPT] BOTÃO CANCELAR (MODAL) INTERCEPTADO!');
                                console.log('❌ [INTERCEPT] Timestamp:', new Date().toLocaleString());
                                console.log('❌ [INTERCEPT] Element:', this);
                                console.log('❌ [INTERCEPT] Event:', e);
                                console.log('❌ [INTERCEPT] ===================================');
                            }, true);
                            btnCancelar.setAttribute('data-intercepted', 'true');
                            console.log('✅ [MODAL-CONF] Interceptador instalado no botão Cancelar');
                        }
                    }, 100);
                }
            }
        }
    });
});

observer.observe(document.body, {
    attributes: true,
    subtree: true,
    attributeFilter: ['style', 'class']
});

// ===== MONITORA MENSAGENS DE ERRO =====
const errorObserver = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1 && 
                    (node.classList.contains('alert') || 
                     node.classList.contains('error') ||
                     node.textContent.includes('erro') ||
                     node.textContent.includes('Nenhuma presença'))) {
                    
                    console.log('⚠️ [ERROR] ===================================');
                    console.log('⚠️ [ERROR] MENSAGEM DE ERRO DETECTADA!');
                    console.log('⚠️ [ERROR] Elemento:', node);
                    console.log('⚠️ [ERROR] Texto:', node.textContent.trim());
                    console.log('⚠️ [ERROR] Classes:', node.className);
                    console.log('⚠️ [ERROR] Timestamp:', new Date().toLocaleString());
                    console.log('⚠️ [ERROR] ===================================');
                }
            });
        }
    });
});

errorObserver.observe(document.body, {
    childList: true,
    subtree: true
});

// ===== MONITORA CONSOLE LOGS =====
const originalConsoleLog = console.log;
console.log = function(...args) {
    // Se for um log relacionado ao sistema de presenças, destaca
    const message = args.join(' ');
    if (message.includes('[DEBUG-CLIQUE]') || 
        message.includes('[DEBUG-SUBMIT]') || 
        message.includes('presenca') || 
        message.includes('modal') ||
        message.includes('finalizar')) {
        
        originalConsoleLog('🔥 [LOG-INTERCEPTED]', ...args);
    } else {
        originalConsoleLog(...args);
    }
};

console.log('✅ [SUPER-DEBUG] Todos os interceptadores instalados!');
console.log('📋 [SUPER-DEBUG] Agora você verá logs SUPER detalhados de:');
console.log('  • Todos os cliques em botões importantes');
console.log('  • Todas as requisições fetch');
console.log('  • Todos os submits de formulário');
console.log('  • Todas as mudanças em modais');
console.log('  • Todas as mensagens de erro que aparecerem');
console.log('  • Botões específicos do modal de confirmação');
console.log('🎯 [SUPER-DEBUG] Teste agora o fluxo completo!');
console.log('📋 [SUPER-DEBUG] INSTRUÇÕES:');
console.log('  1. Selecione um dia no calendário');
console.log('  2. Clique no dia azul para abrir o modal');
console.log('  3. Marque as presenças e clique em "Salvar Presenças"');
console.log('  4. Clique em "Finalizar Registro Completo"');
console.log('  5. No modal de confirmação, clique em "Confirmar Envio"');
console.log('  6. Observe TODOS os logs no console!');
