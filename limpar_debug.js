/**
 * 🧹 LIMPAR LOGS DE DEBUG
 * Execute no console para remover todos os interceptadores de debug
 */

console.clear();
console.log('🧹 Limpando interceptadores de debug...');

// Restaurar fetch original se foi interceptado
if (window.originalFetch) {
    window.fetch = window.originalFetch;
    console.log('✅ Fetch original restaurado');
}

// Restaurar form.submit original se foi interceptado
if (window.originalSubmit) {
    HTMLFormElement.prototype.submit = window.originalSubmit;
    console.log('✅ Form.submit original restaurado');
}

console.log('🎉 Debug limpo! Sistema funcionando normalmente.');
