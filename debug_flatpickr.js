/* 
🔧 TESTE DE DEBUG RÁPIDO PARA FLATPICKR
Execute este código no console do navegador para diagnosticar o problema
*/

console.log('🔍 DIAGNÓSTICO FLATPICKR');
console.log('========================');

// 1. Verificar se Flatpickr está disponível
console.log('1. Flatpickr disponível:', typeof flatpickr !== 'undefined');
console.log('   - window.flatpickr:', typeof window.flatpickr);

// 2. Verificar se inputs existem
const inputs = document.querySelectorAll('.dias-datepicker');
console.log('2. Inputs .dias-datepicker encontrados:', inputs.length);

inputs.forEach((input, idx) => {
    console.log(`   Input ${idx}:`, {
        id: input.id,
        classes: input.className,
        atividade: input.dataset.atividade,
        maxdias: input.dataset.maxdias,
        temFlatpickr: !!input._flatpickr
    });
});

// 3. Verificar se PresencaManager existe e foi inicializado
console.log('3. PresencaManager disponível:', typeof window.PresencaManager !== 'undefined');
if (window.PresencaManager) {
    console.log('   - Turma ID:', window.PresencaManager.turmaId);
    console.log('   - Atividades:', Object.keys(window.PresencaManager.atividades).length);
}

// 4. Verificar console de erros
console.log('4. Verificar se há erros no console acima...');

// 5. Tentar inicializar manualmente um Flatpickr
if (inputs.length > 0 && typeof flatpickr !== 'undefined') {
    const primeiroInput = inputs[0];
    console.log('5. Testando inicialização manual do primeiro input...');
    
    try {
        const testInstance = flatpickr(primeiroInput, {
            mode: 'multiple',
            dateFormat: 'd/m/Y',
            locale: 'pt'
        });
        console.log('   ✅ Teste manual funcionou!', !!testInstance);
        testInstance.destroy(); // Limpa o teste
    } catch (error) {
        console.log('   ❌ Erro no teste manual:', error);
    }
}

console.log('========================');
console.log('FIM DO DIAGNÓSTICO');
