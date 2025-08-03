// Script de debug para investigar o modal de presenças
// Cole isso no console do navegador para diagnosticar o problema

console.log('=== DEBUG MODAL DE PRESENÇAS ===');

// 1. Verifica se o modal existe
const modal = document.getElementById('presencaModal');
console.log('1. Modal encontrado:', modal);

// 2. Verifica se o botão salvar existe
const btnSalvar = modal ? modal.querySelector('.btn-salvar-presenca') : null;
console.log('2. Botão salvar encontrado:', btnSalvar);

// 3. Verifica onclick atual do botão
if (btnSalvar) {
    console.log('3. onclick atual do botão:', btnSalvar.getAttribute('onclick'));
    console.log('4. onclick function:', btnSalvar.onclick);
}

// 4. Verifica se a função abrirModalPresenca existe
console.log('5. Função abrirModalPresenca existe:', typeof window.abrirModalPresenca);

// 5. Verifica se PresencaApp existe
console.log('6. PresencaApp existe:', typeof window.PresencaApp);
if (window.PresencaApp) {
    console.log('7. salvarPresencaDia existe:', typeof window.PresencaApp.salvarPresencaDia);
    console.log('8. fecharModalPresenca existe:', typeof window.PresencaApp.fecharModalPresenca);
}

// 6. Lista todos os scripts carregados
const scripts = Array.from(document.scripts).map(s => s.src || 'inline');
console.log('9. Scripts carregados:', scripts);

// 7. Verifica se nosso arquivo está carregado
const nossoScript = scripts.find(s => s.includes('registrar_presenca_dias_atividades.js'));
console.log('10. Nosso script carregado:', nossoScript);

// 8. Função para testar interceptador manualmente
window.testarInterceptador = function() {
    console.log('=== TESTE MANUAL DO INTERCEPTADOR ===');
    const modal = document.getElementById('presencaModal');
    const btnSalvar = modal ? modal.querySelector('.btn-salvar-presenca') : null;
    
    if (btnSalvar) {
        console.log('Instalando interceptador manualmente...');
        btnSalvar.removeAttribute('onclick');
        btnSalvar.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('*** INTERCEPTADOR MANUAL ATIVO ***');
            alert('Interceptador funcionando! Modal não deve fechar automaticamente.');
        };
        console.log('Interceptador manual instalado. Teste o botão "Salvar Presenças".');
    } else {
        console.log('ERRO: Botão não encontrado para teste manual.');
    }
};

console.log('=== COMANDOS DISPONÍVEIS ===');
console.log('- testarInterceptador() - Instala interceptador manual para teste');
console.log('- window.PresencaApp - Examinar objeto principal');
console.log('- window.abrirModalPresenca - Examinar função de abrir modal');
