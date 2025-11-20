document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filtro-frequencias');
    const tabelaContainer = document.getElementById('tabela-container');
    const spinner = document.getElementById('loading-spinner');

    if (!form || !tabelaContainer || !spinner) {
        console.error('Elementos necessários não encontrados na página');
        return;
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        fetchFrequencias();
    });

    function fetchFrequencias() {
        spinner.style.display = 'block';
        tabelaContainer.style.display = 'none';

        const formData = new FormData(form);
        const params = new URLSearchParams(formData);

        fetch(`/frequencias/?${params.toString()}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(async response => {
            if (response.status === 401 || response.redirected) {
                tabelaContainer.innerHTML = '<p class="text-danger">Sua sessão expirou. Faça login novamente.</p>';
                spinner.style.display = 'none';
                tabelaContainer.style.display = 'block';
                return null;
            }
            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            if (data.tabela_html && data.paginacao_html) {
                tabelaContainer.innerHTML = data.tabela_html;
                const cardFooter = document.querySelector('.card-footer');
                if (cardFooter) {
                    cardFooter.innerHTML = data.paginacao_html;
                }
            } else {
                tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados.</p>';
            }
        })
        .catch(error => {
            console.error('Erro ao buscar frequências:', error);
            tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados.</p>';
        })
        .finally(() => {
            spinner.style.display = 'none';
            tabelaContainer.style.display = 'block';
        });
    }

    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('page-link')) {
            e.preventDefault();
            const url = e.target.getAttribute('href');
            if (url) {
                const params = new URLSearchParams(url.split('?')[1] || '');
                const formData = new FormData(form);
                for (const [key, value] of formData.entries()) {
                    if (value && key !== 'csrfmiddlewaretoken') {
                        params.set(key, value);
                    }
                }
                spinner.style.display = 'block';
                tabelaContainer.style.display = 'none';
                fetch(`/frequencias/?${params.toString()}`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(async response => {
                    if (response.status === 401 || response.redirected) {
                        tabelaContainer.innerHTML = '<p class="text-danger">Sua sessão expirou.</p>';
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
                    if (!data) return;
                    if (data.tabela_html && data.paginacao_html) {
                        tabelaContainer.innerHTML = data.tabela_html;
                        const cardFooter = document.querySelector('.card-footer');
                        if (cardFooter) {
                            cardFooter.innerHTML = data.paginacao_html;
                        }
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados.</p>';
                })
                .finally(() => {
                    spinner.style.display = 'none';
                    tabelaContainer.style.display = 'block';
                });
            }
        }
    });
});
