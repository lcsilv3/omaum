// Função para verificar o status da sessão e do token CSRF
function checkSessionStatus() {
    // Fazer uma requisição AJAX para verificar o status da sessão
    fetch('/csrf_check/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            // Se a resposta não for OK, mostrar alerta de sessão expirada
            showSessionExpiredAlert();
        }
    })
    .catch(error => {
        console.error('Erro ao verificar status da sessão:', error);
        // Em caso de erro, também mostrar o alerta
        showSessionExpiredAlert();
    });
}

// Função para mostrar alerta de sessão expirada
function showSessionExpiredAlert() {
    // Verificar se o alerta já existe para não duplicar
    if (!document.getElementById('session-expired-alert')) {
        const alertDiv = document.createElement('div');
        alertDiv.id = 'session-expired-alert';
        alertDiv.className = 'alert alert-warning alert-dismissible fade show session-alert';
        alertDiv.innerHTML = `
            <strong>Atenção!</strong> Sua sessão pode ter expirado. 
            <button type="button" class="btn btn-sm btn-primary mx-2" onclick="refreshPage()">Recarregar Página</button>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
        `;
        
        // Estilo para o alerta fixo no topo da página
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '10px';
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
        
        document.body.appendChild(alertDiv);
    }
}

// Função para recarregar a página
function refreshPage() {
    window.location.reload();
}

// Verificar a sessão a cada 5 minutos (300000 ms)
// Você pode ajustar este valor conforme necessário
const checkInterval = 300000;
setInterval(checkSessionStatus, checkInterval);

// Também verificar quando o usuário retorna à aba
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        checkSessionStatus();
    }
});

// Verificar status inicial após carregamento da página
document.addEventListener('DOMContentLoaded', function() {
    // Esperar um pouco para garantir que a página esteja totalmente carregada
    setTimeout(checkSessionStatus, 1000);
});