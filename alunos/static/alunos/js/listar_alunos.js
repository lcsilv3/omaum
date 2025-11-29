document.addEventListener('DOMContentLoaded', function() {
    // Função para buscar e atualizar os cards de relatórios no modal
    function atualizarCardsRelatorios() {
        fetch('/alunos/search/?ajax_relatorios=1', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.cards_relatorios_html) {
                var modalBody = document.querySelector('#modalRelatoriosAlunos .modal-body');
                if (modalBody) {
                    modalBody.innerHTML = data.cards_relatorios_html;
                }
            }
        });
    }

    const form = document.getElementById('filtro-form');
    const tabelaContainer = document.getElementById('tabela-container');
    const spinner = document.getElementById('loading-spinner');
    const searchInput = document.getElementById('search-aluno');
    const cursoSelect = document.getElementById('curso-select');
    
    let debounceTimer = null;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        fetchAlunos();
    });

    // Busca ao digitar no campo de pesquisa (com debounce de 100ms)
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                fetchAlunos();
            }, 100);
        });
    }

    // Busca ao mudar o curso
    if (cursoSelect) {
        cursoSelect.addEventListener('change', function() {
            fetchAlunos();
        });
    }

    // Dispara AJAX ao abrir o modal de relatórios
    var modalRelatorios = document.getElementById('modalRelatoriosAlunos');
    if (modalRelatorios) {
        modalRelatorios.addEventListener('show.bs.modal', function () {
            atualizarCardsRelatorios();
        });
    }

    function fetchAlunos() {
        spinner.style.display = 'block';
        tabelaContainer.style.display = 'none';

        const formData = new FormData(form);
        const params = new URLSearchParams(formData);

        fetch(`/alunos/search/?${params.toString()}`, {
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
                throw new Error(`Erro na requisição: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            if (data.tabela_html && data.paginacao_html) {
                tabelaContainer.innerHTML = data.tabela_html;
                document.querySelector('.card-footer').innerHTML = data.paginacao_html;
                // Atualiza dinamicamente o conteúdo do modal de relatórios, se presente
                if (data.cards_relatorios_html) {
                    var modalBody = document.querySelector('#modalRelatoriosAlunos .modal-body');
                    if (modalBody) {
                        modalBody.innerHTML = data.cards_relatorios_html;
                    }
                }
            } else {
                tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados. Resposta inválida do servidor.</p>';
            }
        })
        .catch(error => {
            tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados. Verifique sua conexão ou tente novamente mais tarde.</p>';
        })
        .finally(() => {
            spinner.style.display = 'none';
            tabelaContainer.style.display = 'block';
        });
    }

    // Adiciona evento de clique para links de paginação
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('page-link')) {
            e.preventDefault();
            const url = e.target.getAttribute('href');
            if (url) {
                // Mantém os filtros atuais ao paginar
                const params = new URLSearchParams(url.split('?')[1] || '');
                // Adiciona filtros do formulário se existirem
                const formData = new FormData(form);
                for (const [key, value] of formData.entries()) {
                    if (value && key !== 'csrfmiddlewaretoken') {
                        params.set(key, value);
                    }
                }
                spinner.style.display = 'block';
                tabelaContainer.style.display = 'none';
                fetch(`/alunos/search/?${params.toString()}`, {
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
                    if (!data) return;
                    if (data.tabela_html && data.paginacao_html) {
                        tabelaContainer.innerHTML = data.tabela_html;
                        document.querySelector('.card-footer').innerHTML = data.paginacao_html;
                        // Atualiza dinamicamente o conteúdo do modal de relatórios, se presente
                        if (data.cards_relatorios_html) {
                            var modalBody = document.querySelector('#modalRelatoriosAlunos .modal-body');
                            if (modalBody) {
                                modalBody.innerHTML = data.cards_relatorios_html;
                            }
                        }
                    } else {
                        tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados.</p>';
                    }
                })
                .catch(error => {
                    console.error('Erro ao buscar alunos:', error);
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