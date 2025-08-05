// Teste simples para verificar se o JS está sendo carregado
console.log('=== TESTE JS CARREGADO ===');
console.log('Arquivo registrar_presenca_dias_atividades.js foi carregado!');

// Função de teste simples
window.testeInterceptador = function() {
    console.log('=== TESTE INTERCEPTADOR MANUAL ===');
    
    const modal = document.getElementById('presencaModal');
    console.log('Modal encontrado:', modal);
    
    if (modal) {
        const btnSalvar = modal.querySelector('.btn-salvar-presenca');
        console.log('Botão salvar encontrado:', btnSalvar);
        console.log('Classe do botão:', btnSalvar ? btnSalvar.className : 'N/A');
        console.log('onclick original:', btnSalvar ? btnSalvar.getAttribute('onclick') : 'N/A');
        
        if (btnSalvar) {
            // Instala interceptador de teste
            btnSalvar.removeAttribute('onclick');
            btnSalvar.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('*** INTERCEPTADOR DE TESTE FUNCIONANDO ***');
                alert('Interceptador ativo! Modal não deve fechar.');
                return false;
            };
            console.log('Interceptador de teste instalado!');
        }
    }
};

// Teste automático após 2 segundos
setTimeout(function() {
    console.log('=== TESTE AUTOMÁTICO APÓS 2 SEGUNDOS ===');
    window.testeInterceptador();
}, 2000);
