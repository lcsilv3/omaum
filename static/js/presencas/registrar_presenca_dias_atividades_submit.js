// Script para submit AJAX e exibição de mensagens na etapa 3 (dias/atividades)
// Supervisor: Copilot (Django Web)


// Exibe um modal customizado com todos os erros detalhados
function mostrarModalErrosDetalhados(erros) {
    const modal = document.getElementById('modalConfirmacaoPresenca');
    const body = document.getElementById('modalConfirmacaoBody');
    if (!modal || !body) return;
    let html = '<div style="color:#b71c1c;font-weight:500;margin-bottom:8px;">Foram encontrados os seguintes problemas ao finalizar o registro:</div>';
    html += '<ul style="padding-left:18px;">';
    (Array.isArray(erros) ? erros : [erros]).forEach(function(erro) {
        html += `<li style='margin-bottom:4px;'>${erro}</li>`;
    });
    html += '</ul>';
    body.innerHTML = html;
    modal.style.display = 'flex';
    modal.classList.add('show');
    document.body.classList.add('modal-open');
    // Esconde botão cancelar, muda texto do confirmar para 'Fechar'
    modal.querySelector('.btn-cancelar').style.display = 'none';
    const btnConfirmar = modal.querySelector('.btn-confirmar');
    btnConfirmar.querySelector('.btn-confirmar-text').textContent = 'Fechar';
    btnConfirmar.onclick = function() {
        modal.style.display = 'none';
        modal.classList.remove('show');
        document.body.classList.remove('modal-open');
    };
}

function mostrarErroAjaxEtapa3(msg) {
    // Se for array, exibe modal detalhado
    if (Array.isArray(msg)) {
        mostrarModalErrosDetalhados(msg);
        return;
    }
    const erroDiv = document.getElementById('mensagem-erro-ajax');
    if (erroDiv) {
        erroDiv.textContent = msg;
        erroDiv.classList.remove('d-none');
        erroDiv.classList.add('alert-danger');
        erroDiv.focus();
        erroDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function limparErroAjaxEtapa3() {
    const erroDiv = document.getElementById('mensagem-erro-ajax');
    if (erroDiv) {
        erroDiv.textContent = '';
        erroDiv.classList.add('d-none');
        erroDiv.classList.remove('alert-danger');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-presenca');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            limparErroAjaxEtapa3();
            const formData = new FormData(form);
            fetch('/presencas/registrar-presenca/dias-atividades/ajax/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: formData
            })
            .then(async response => {
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        window.location.href = data.redirect_url;
                    } else if (data.errors) {
                        mostrarErroAjaxEtapa3(data.errors || 'Erro de validação.');
                    } else {
                        mostrarErroAjaxEtapa3('Erro desconhecido.');
                    }
                } else {
                    // Tenta extrair mensagem de erro detalhada
                    let msg = 'Erro ao registrar presenças.';
                    try {
                        const data = await response.json();
                        if (data && data.errors) {
                            msg = data.errors;
                        } else if (data && data.detail) {
                            msg = data.detail;
                        }
                    } catch {}
                    mostrarErroAjaxEtapa3(msg);
                }
            })
            .catch(error => {
                mostrarErroAjaxEtapa3('Erro de rede ao enviar dados. Tente novamente.');
            });
        });
    }
});

// Mantém o estado do formulário em caso de erro: não limpar campos, não resetar seleção.
// Só limpar/resetar se o registro for bem-sucedido (redirect).
