/**
 * 🚨 DEBUG CRÍTICO: INTERCEPTA FORM.SUBMIT()
 * 
 * O problema foi descoberto! A função "Confirmar Envio" usa form.submit()
 * ao invés de fetch(), por isso não víamos as requisições!
 */

console.log('🚨 [FORM-SUBMIT-DEBUG] ===== INTERCEPTANDO FORM.SUBMIT() =====');

// ===== INTERCEPTA FORM.SUBMIT() =====
const originalSubmit = HTMLFormElement.prototype.submit;
HTMLFormElement.prototype.submit = function() {
    console.log('🚨🚨🚨 [FORM-SUBMIT] ===================================');
    console.log('🚨🚨🚨 [FORM-SUBMIT] *** FORM.SUBMIT() INTERCEPTADO! ***');
    console.log('🚨🚨🚨 [FORM-SUBMIT] Form ID:', this.id);
    console.log('🚨🚨🚨 [FORM-SUBMIT] Form action:', this.action);
    console.log('🚨🚨🚨 [FORM-SUBMIT] Form method:', this.method);
    console.log('🚨🚨🚨 [FORM-SUBMIT] Timestamp:', new Date().toLocaleString());
    
    // Lista todos os campos do formulário
    const formData = new FormData(this);
    console.log('📋 [FORM-SUBMIT] ===== DADOS DO FORMULÁRIO =====');
    let temPresencas = false;
    
    for (let [key, value] of formData.entries()) {
        if (key.includes('json')) {
            try {
                const parsed = JSON.parse(value);
                console.log(`📋 [FORM-SUBMIT] ${key}:`, JSON.stringify(parsed, null, 2));
                if (key === 'presencas_json' && Object.keys(parsed).length > 0) {
                    temPresencas = true;
                    console.log('✅ [FORM-SUBMIT] DADOS DE PRESENÇA ENCONTRADOS!');
                }
            } catch (err) {
                console.log(`📋 [FORM-SUBMIT] ${key}: (não é JSON válido)`, value);
            }
        } else {
            console.log(`📋 [FORM-SUBMIT] ${key}:`, value);
        }
    }
    
    if (!temPresencas) {
        console.log('❌ [FORM-SUBMIT] NENHUM DADO DE PRESENÇA ENCONTRADO NO FORMULÁRIO!');
    } else {
        console.log('✅ [FORM-SUBMIT] Formulário contém dados de presença válidos!');
    }
    
    console.log('🚨🚨🚨 [FORM-SUBMIT] ===================================');
    
    // Chama o submit original
    console.log('📤 [FORM-SUBMIT] Executando submit original...');
    return originalSubmit.call(this);
};

// ===== INTERCEPTA EVENTO DE SUBMIT =====
document.addEventListener('submit', function(e) {
    console.log('📤 [EVENT-SUBMIT] ===================================');
    console.log('📤 [EVENT-SUBMIT] *** EVENTO SUBMIT DETECTADO! ***');
    console.log('📤 [EVENT-SUBMIT] Form ID:', e.target.id);
    console.log('📤 [EVENT-SUBMIT] Form action:', e.target.action);
    console.log('📤 [EVENT-SUBMIT] Event type:', e.type);
    console.log('📤 [EVENT-SUBMIT] Timestamp:', new Date().toLocaleString());
    console.log('📤 [EVENT-SUBMIT] ===================================');
}, true);

// ===== INTERCEPTA CLIQUES EM CONFIRMAR ENVIO =====
document.addEventListener('click', function(e) {
    const target = e.target;
    const text = target.textContent?.trim() || '';
    
    if (text.includes('Confirmar') && text.includes('Envio')) {
        console.log('🔥🔥🔥 [CONFIRMAR-CRÍTICO] ===================================');
        console.log('🔥🔥🔥 [CONFIRMAR-CRÍTICO] *** BOTÃO CONFIRMAR ENVIO CLICADO! ***');
        console.log('🔥🔥🔥 [CONFIRMAR-CRÍTICO] Texto completo:', text);
        console.log('🔥🔥🔥 [CONFIRMAR-CRÍTICO] ID:', target.id);
        console.log('🔥🔥🔥 [CONFIRMAR-CRÍTICO] Classes:', target.className);
        console.log('🔥🔥🔥 [CONFIRMAR-CRÍTICO] onclick:', target.getAttribute('onclick'));
        console.log('🔥🔥🔥 [CONFIRMAR-CRÍTICO] ===================================');
    }
}, true);

console.log('✅ [FORM-SUBMIT-DEBUG] Interceptadores instalados!');
console.log('📋 [FORM-SUBMIT-DEBUG] Agora teste o fluxo completo:');
console.log('  1. Marque presenças');
console.log('  2. Clique em "Salvar Presenças"');
console.log('  3. Clique em "Finalizar Registro Completo"');
console.log('  4. Clique em "Confirmar Envio"');
console.log('  5. Observe os logs de form.submit()!');
