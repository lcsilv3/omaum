// Limpa todos os campos de texto e desmarca checkboxes ao abrir a tela de dias das atividades
// para evitar que o navegador restaure valores antigos.
document.addEventListener('DOMContentLoaded', function () {
    // Limpa todos os campos de texto
    document.querySelectorAll('.obs-dia').forEach(function(input) {
        input.value = '';
    });
    // Desmarca todos os checkboxes
    document.querySelectorAll('.dia-checkbox').forEach(function(checkbox) {
        checkbox.checked = false;
    });
});
