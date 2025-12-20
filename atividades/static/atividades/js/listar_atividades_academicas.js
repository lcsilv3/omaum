document.addEventListener('DOMContentLoaded', function() {
    console.log('[Atividades] Script carregado - versão 20251220');
    
    const form = document.getElementById('filtro-atividades-form');
    const tabelaContainer = document.getElementById('tabela-atividades-container');
    const spinner = document.getElementById('atividades-spinner');
    const footer = document.getElementById('atividades-card-footer');
    const cursoSelect = document.getElementById('id_curso');
    const turmaSelect = document.getElementById('id_turma');
    const searchInput = document.getElementById('id_q');

    if (!form || !tabelaContainer || !spinner) {
        console.error('[Atividades] Elementos não encontrados:', { form, tabelaContainer, spinner });
        return;
    }
    
    console.log('[Atividades] Elementos encontrados, inicializando...');

    let debounceTimer = null;

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        fetchAtividades();
    });

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => fetchAtividades(), 500);
        });
    }

    if (cursoSelect) {
        cursoSelect.addEventListener('change', function() {
            fetchAtividades();
        });
    }

    if (turmaSelect) {
        turmaSelect.addEventListener('change', function() {
            fetchAtividades();
        });
    }

    document.addEventListener('click', function(event) {
        const link = event.target.closest('.page-link-atividades');
        if (link) {
            event.preventDefault();
            const url = new URL(link.href, window.location.origin);
            const extraParams = new URLSearchParams(url.search);
            fetchAtividades(extraParams);
        }
    });

    function fetchAtividades(extraParams) {
        console.log('[Atividades] Iniciando fetch...', { extraParams });
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
        console.log('[Atividades] URL da requisição:', url);

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(async response => {
                console.log('[Atividades] Response status:', response.status);
                console.log('[Atividades] Content-Type:', response.headers.get('content-type'));
                
                if (response.status === 401 || response.redirected) {
                    tabelaContainer.innerHTML = '<p class="text-danger">Sua sessão expirou. Faça login novamente para continuar.</p>';
                    spinner.style.display = 'none';
                    tabelaContainer.style.display = 'block';
                    return null;
                }
                if (!response.ok) {
                    throw new Error('Erro na requisição');
                }
                
                // Verificar se é JSON antes de tentar parsear
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    const text = await response.text();
                    console.error('[Atividades] Resposta não é JSON:', text.substring(0, 200));
                    throw new Error('Servidor retornou HTML em vez de JSON');
                }
                
                return response.json();
            })
            .then(data => {
                if (!data) {
                    return;
                }
                
                console.log('[Atividades] Dados recebidos:', Object.keys(data));

                if (data.tabela_html) {
                    tabelaContainer.innerHTML = data.tabela_html;
                } else {
                    tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados. Resposta inválida do servidor.</p>';
                }

                if (cursoSelect && data.cursos_html) {
                    cursoSelect.innerHTML = data.cursos_html;
                }

                if (turmaSelect && data.turmas_html) {
                    turmaSelect.innerHTML = data.turmas_html;
                }

                if (footer) {
                    if (data.rodape_html) {
                        footer.innerHTML = data.rodape_html;
                    } else if (data.paginacao_html) {
                        footer.innerHTML = data.paginacao_html;
                    }
                }
            })
            .catch((error) => {
                console.error('[Atividades] Erro na requisição:', error);
                tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados. Verifique sua conexão ou tente novamente mais tarde.</p>';
            })
            .finally(() => {
                spinner.style.display = 'none';
                tabelaContainer.style.display = 'block';
            });
    }
});
