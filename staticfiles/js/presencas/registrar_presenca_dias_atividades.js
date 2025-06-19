document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-presenca');
    const mensagemAjax = document.getElementById('mensagem-ajax');

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const btn = form.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                btn.textContent = 'Salvando...';
            }
            const formData = new FormData(form);
            fetch('/presencas/registrar-presenca/dias-atividades/ajax/', {
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
                } else if (data.message) {
                    mostrarErroAjax(data.message);
                    if (data.message.includes('sessão')) {
                        setTimeout(() => {
                            window.location.href = '/presencas/registrar-presenca/dados-basicos/';
                        }, 2500);
                    }
                } else if (data.errors) {
                    mostrarErroAjax('Preencha todos os campos obrigatórios.');
                } else {
                    mostrarErroAjax('Erro inesperado. Tente novamente.');
                }
            })
            .catch(error => {
                mostrarErroAjax('Erro ao enviar dados. Tente novamente.');
            })
            .finally(() => {
                if (btn) {
                    btn.disabled = false;
                    btn.textContent = 'Salvar e avançar';
                }
            });
        });
    }
});