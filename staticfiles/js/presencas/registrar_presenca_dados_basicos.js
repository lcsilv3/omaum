// Script para manipulação do formulário de registro de presença (dados básicos)
// ...copie o JS inline do template para cá...

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

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-dados-basicos');
    const cursoSelect = document.getElementById('id_curso');
    const turmaSelect = document.getElementById('id_turma');
    const loadingTurmas = document.getElementById('loading-turmas');

    if (cursoSelect && turmaSelect) {
        cursoSelect.addEventListener('change', function () {
            const cursoId = this.value;
            turmaSelect.innerHTML = '<option value="">---------</option>';
            if (!cursoId) return;
            loadingTurmas.classList.remove('d-none');
            fetch(`/presencas/registrar-presenca/turmas-por-curso/?curso_id=${cursoId}`)
                .then(response => response.json())
                .then(turmas => {
                    turmas.forEach(turma => {
                        const opt = document.createElement('option');
                        opt.value = turma.id;
                        opt.textContent = turma.nome;
                        turmaSelect.appendChild(opt);
                    });
                })
                .finally(() => loadingTurmas.classList.add('d-none'));
        });
    }

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            fetch('/presencas/registrar-presenca/dados-basicos/ajax/', {
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
                } else {
                    mostrarErroAjax('Preencha todos os campos obrigatórios.');
                }
            })
            .catch(error => {
                mostrarErroAjax('Erro ao enviar dados. Tente novamente.');
            });
        });
    }

    // Ano/Mês
    const mesAnoAtual = document.getElementById('mes-ano-atual');
    const inputAno = document.getElementById('id_ano');
    const inputMes = document.getElementById('id_mes');
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');

    function atualizarMesAno() {
        const ano = parseInt(inputAno.value);
        const mes = parseInt(inputMes.value);
        const nomesMeses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ];
        mesAnoAtual.textContent = `${nomesMeses[mes - 1]} / ${ano}`;
    }

    if (mesAnoAtual && inputAno && inputMes) {
        atualizarMesAno();

        btnPrev.addEventListener('click', function () {
            let ano = parseInt(inputAno.value);
            let mes = parseInt(inputMes.value);
            mes--;
            if (mes < 1) {
                mes = 12;
                ano--;
            }
            inputAno.value = ano;
            inputMes.value = mes;
            atualizarMesAno();
        });

        btnNext.addEventListener('click', function () {
            let ano = parseInt(inputAno.value);
            let mes = parseInt(inputMes.value);
            mes++;
            if (mes > 12) {
                mes = 1;
                ano++;
            }
            inputAno.value = ano;
            inputMes.value = mes;
            atualizarMesAno();
        });
    }
});