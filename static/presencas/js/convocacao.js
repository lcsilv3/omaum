// JS para alternância do badge de convocação via AJAX

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toggle-convocacao-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const alunoId = btn.getAttribute('data-aluno');
            const atividadeId = btn.getAttribute('data-atividade');
            const key = btn.getAttribute('data-key');
            fetch('/presencas/ajax/toggle-convocacao/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ aluno_id: alunoId, atividade_id: atividadeId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const badge = document.getElementById('badge-convocacao-' + key);
                    if (badge) {
                        badge.textContent = data.convocado ? 'Convocado' : 'Não Convocado';
                        badge.className = 'badge ' + (data.convocado ? 'bg-primary' : 'bg-secondary') + ' badge-convocacao';
                    }
                } else {
                    alert('Erro ao alternar convocação: ' + (data.error || 'Erro desconhecido.'));
                }
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
