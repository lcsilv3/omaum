document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filtro-turmas-form');
    const tabelaContainer = document.getElementById('tabela-turmas-container');
    const spinner = document.getElementById('turmas-spinner');
    const footer = document.getElementById('turmas-card-footer');
    const searchInput = document.getElementById('id_q');
    const cursoSelect = document.getElementById('id_curso');
    const statusSelect = document.getElementById('id_status');

    if (!form || !tabelaContainer || !spinner) {
        return;
    }

    let debounceTimer = null;

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        fetchTurmas();
    });

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => fetchTurmas(), 120);
        });
    }

    if (cursoSelect) {
        cursoSelect.addEventListener('change', function() {
            fetchTurmas();
        });
    }

    if (statusSelect) {
        statusSelect.addEventListener('change', function() {
            fetchTurmas();
        });
    }

    document.addEventListener('click', function(event) {
        const link = event.target.closest('.page-link-turmas');
        if (link) {
            event.preventDefault();
            const url = new URL(link.href, window.location.origin);
            const extraParams = new URLSearchParams(url.search);
            fetchTurmas(extraParams);
        }
    });

    function fetchTurmas(extraParams) {
        spinner.style.display = 'block';
        tabelaContainer.style.display = 'none';

        const formData = new FormData(form);
        const params = new URLSearchParams(formData);

        if (extraParams) {
            for (const [key, value] of extraParams.entries()) {
                if (value && key !== 'csrfmiddlewaretoken') {
                    params.set(key, value);
                }
            }
        }

        const url = `${window.location.pathname}?${params.toString()}`;

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(async response => {
                if (response.status === 401 || response.redirected) {
                    tabelaContainer.innerHTML = '<p class="text-danger">Sua sessão expirou. Faça login novamente para continuar.</p>';
                    spinner.style.display = 'none';
                    tabelaContainer.style.display = 'block';
                    return null;
                }
                if (!response.ok) {
                    throw new Error('Erro na requisição');
                }
                return response.json();
            })
            .then(data => {
                if (!data) {
                    return;
                }

                if (data.tabela_html) {
                    tabelaContainer.innerHTML = data.tabela_html;
                } else {
                    tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados. Resposta inválida do servidor.</p>';
                }

                if (footer) {
                    if (data.rodape_html) {
                        footer.innerHTML = data.rodape_html;
                    } else if (data.paginacao_html) {
                        footer.innerHTML = data.paginacao_html;
                    }
                }
            })
            .catch(() => {
                tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados. Verifique sua conexão ou tente novamente mais tarde.</p>';
            })
            .finally(() => {
                spinner.style.display = 'none';
                tabelaContainer.style.display = 'block';
            });
    }
});
