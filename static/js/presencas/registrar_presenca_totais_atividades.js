/**
 * Exibe uma mensagem de erro no bloco de erro AJAX do template.
 * @param {string} msg - Mensagem de erro a ser exibida.
 */
function mostrarErroAjax(msg) {
    const ajaxError = document.getElementById('mensagem-erro-ajax');
    if (ajaxError) {
        ajaxError.textContent = msg;
        ajaxError.classList.remove('d-none');
    }
}

/**
 * Limpa a mensagem de erro AJAX.
 */
function limparErroAjax() {
    const ajaxError = document.getElementById('mensagem-erro-ajax');
    if (ajaxError) {
        ajaxError.textContent = '';
        ajaxError.classList.add('d-none');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-totais-atividades');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            limparErroAjax();
            const formData = new FormData(form);
            fetch('/presencas/registrar-presenca/totais-atividades/ajax/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.redirect_url;
                } else if (data.errors && data.errors.atividade) {
                    mostrarErroAjax(data.errors.atividade[0]);
                } else {
                    mostrarErroAjax('Preencha todos os campos obrigatórios.');
                }
            })
            .catch(error => {
                mostrarErroAjax('Erro ao enviar dados. Tente novamente.');
            });
        });
    }
});