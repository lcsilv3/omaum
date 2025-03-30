// Variáveis para controle de inatividade
let inactivityTimer;
const inactivityTimeout = 30 * 60 * 1000; // 30 minutos em milissegundos

// Função para verificar o status da sessão e do token CSRF
function checkSessionStatus() {
    // Fazer uma requisição AJAX para verificar o status da sessão
    fetch('/core/csrf_check/', {  // Corrigir o caminho para incluir 'core/'
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
            <strong>Atenção!</strong> Sua sessão pode ter expirado devido à inatividade. 
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

// Função para reiniciar o timer de inatividade
function resetInactivityTimer() {
    // Limpar o timer existente
    clearTimeout(inactivityTimer);
    
    // Iniciar um novo timer
    inactivityTimer = setTimeout(() => {
        // Após 30 minutos de inatividade, verificar a sessão
        checkSessionStatus();
    }, inactivityTimeout);
}

// Lista de eventos que indicam atividade do usuário
const userActivityEvents = [
    'mousedown', 'mousemove', 'keypress', 
    'scroll', 'touchstart', 'click', 'keydown'
];

// Inicializar o monitoramento de atividade do usuário
function initInactivityMonitoring() {
    // Adicionar listeners para todos os eventos de atividade
    userActivityEvents.forEach(eventType => {
        document.addEventListener(eventType, resetInactivityTimer, { passive: true });
    });
    
    // Iniciar o timer pela primeira vez
    resetInactivityTimer();
}

// Também verificar quando o usuário retorna à aba
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        // Reiniciar o timer quando o usuário volta para a aba
        resetInactivityTimer();
    }
});

// Inicializar o monitoramento de inatividade quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    // Iniciar o monitoramento de inatividade
    initInactivityMonitoring();
});