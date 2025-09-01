document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filtro-form');
    const tabelaContainer = document.getElementById('tabela-container');
    const spinner = document.getElementById('loading-spinner');
    const paginacaoContainer = document.querySelector('.card-footer');

    // Função para obter o valor de um cookie pelo nome
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Função central para buscar alunos via AJAX
    function fetchAlunos(url) {
        spinner.style.display = 'block';
        tabelaContainer.style.display = 'none';

        const csrftoken = getCookie('csrftoken');

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    let errorMsg = `Erro na requisição: ${response.statusText}`;
                    try {
                        const data = JSON.parse(text);
                        if (data && data.error) {
                            errorMsg = data.error;
                        }
                    } catch (e) {
                        errorMsg = text || errorMsg;
                    }
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = errorMsg;
                    throw new Error(tempDiv.textContent || tempDiv.innerText || 'Ocorreu um erro desconhecido.');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data && data.tabela_html && data.paginacao_html) {
                tabelaContainer.innerHTML = data.tabela_html;
                paginacaoContainer.innerHTML = data.paginacao_html;
            } else {
                throw new Error('Resposta inválida do servidor.');
            }
        })
        .catch(error => {
            console.error('Erro ao buscar alunos:', error);
            tabelaContainer.innerHTML = `<p class="text-danger">${error.message || 'Ocorreu um erro ao carregar os dados.'}</p>`;
        })
        .finally(() => {
            spinner.style.display = 'none';
            tabelaContainer.style.display = 'block';
        });
    }

    // Manipulador para o envio do formulário de filtro
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        formData.delete('csrfmiddlewaretoken');
        const params = new URLSearchParams(formData);
        const searchUrl = `/alunos/search/?${params.toString()}`;
        fetchAlunos(searchUrl);
    });

    // Delegação de evento para os links de paginação
    paginacaoContainer.addEventListener('click', function(e) {
        const pageLink = e.target.closest('a.page-link');
        if (pageLink) {
            e.preventDefault();
            const url = pageLink.getAttribute('href');
            if (url) {
                fetchAlunos(url);
            }
        }
    });
});
