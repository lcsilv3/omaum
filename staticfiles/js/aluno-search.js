/**
 * OMAUM - Sistema de Gestão de Iniciados
 * Arquivo: aluno-search.js
 * Descrição: Busca dinâmica de alunos via AJAX para formulários.
 * Responsável: Equipe OMAUM
 * Última atualização: 2025-06-15
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filtro-form');
    const tabelaContainer = document.getElementById('tabela-container');
    const paginacaoContainer = document.querySelector('.card-footer');
    const spinner = document.getElementById('loading-spinner');

    function fetchAlunos(page = 1) {
        spinner.style.display = 'block';
        tabelaContainer.style.display = 'none';

        const formData = new FormData(form);
        const params = new URLSearchParams(formData);
        params.set('page', page);

        fetch(`/alunos/search/?${params.toString()}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Resposta JSON recebida:', data);
            if (data.alunos) {
                console.log('Renderizando tabela com os dados brutos.');
                tabelaContainer.innerHTML = '';
                data.alunos.forEach(aluno => {
                    tabelaContainer.innerHTML += `
                        <tr>
                            <td>${aluno.cpf}</td>
                            <td>${aluno.nome}</td>
                            <td>${aluno.email}</td>
                            <td><img src="${aluno.foto}" alt="Foto de ${aluno.nome}" style="width: 50px; height: 50px;"></td>
                        </tr>`;
                });
                paginacaoContainer.innerHTML = `
                    <nav>
                        <ul class="pagination">
                            <li class="page-item ${data.page === 1 ? 'disabled' : ''}">
                                <a class="page-link" href="?page=${data.page - 1}" aria-label="Anterior">
                                    <span aria-hidden="true">&laquo;</span>
                                </a>
                            </li>
                            ${Array.from({ length: data.num_pages }, (_, i) => `
                                <li class="page-item ${data.page === i + 1 ? 'active' : ''}">
                                    <a class="page-link" href="?page=${i + 1}">${i + 1}</a>
                                </li>`).join('')}
                            <li class="page-item ${data.page === data.num_pages ? 'disabled' : ''}">
                                <a class="page-link" href="?page=${data.page + 1}" aria-label="Próximo">
                                    <span aria-hidden="true">&raquo;</span>
                                </a>
                            </li>
                        </ul>
                    </nav>`;
            } else if (data.success === false) {
                console.warn('Nenhum resultado encontrado.');
                tabelaContainer.innerHTML = '<p class="text-warning">Nenhum resultado encontrado.</p>';
                paginacaoContainer.innerHTML = '';
            } else {
                console.error('Resposta inválida do servidor:', data);
                tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados. Resposta inválida do servidor.</p>';
            }
        })
        .catch(error => {
            console.error('Erro ao buscar alunos:', error);
            tabelaContainer.innerHTML = '<p class="text-danger">Erro ao carregar os dados. Verifique sua conexão ou tente novamente mais tarde.</p>';
        })
        .finally(() => {
            spinner.style.display = 'none';
            tabelaContainer.style.display = 'block';
        });
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        fetchAlunos();
    });

    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('page-link')) {
            e.preventDefault();
            const url = e.target.getAttribute('href');

            if (url) {
                spinner.style.display = 'block';
                tabelaContainer.style.display = 'none';

                fetch(url, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro na requisição');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Resposta JSON recebida:', data);
                    if (data.alunos) {
                        console.log('Renderizando tabela com os dados brutos.');
                        tabelaContainer.innerHTML = '';
                        data.alunos.forEach(aluno => {
                            tabelaContainer.innerHTML += `
                                <tr>
                                    <td>${aluno.cpf}</td>
                                    <td>${aluno.nome}</td>
                                    <td>${aluno.email}</td>
                                    <td><img src="${aluno.foto}" alt="Foto de ${aluno.nome}" style="width: 50px; height: 50px;"></td>
                                </tr>`;
                        });
                        paginacaoContainer.innerHTML = `
                            <nav>
                                <ul class="pagination">
                                    <li class="page-item ${data.page === 1 ? 'disabled' : ''}">
                                        <a class="page-link" href="?page=${data.page - 1}" aria-label="Anterior">
                                            <span aria-hidden="true">&laquo;</span>
                                        </a>
                                    </li>
                                    ${Array.from({ length: data.num_pages }, (_, i) => `
                                        <li class="page-item ${data.page === i + 1 ? 'active' : ''}">
                                            <a class="page-link" href="?page=${i + 1}">${i + 1}</a>
                                        </li>`).join('')}
                                    <li class="page-item ${data.page === data.num_pages ? 'disabled' : ''}">
                                        <a class="page-link" href="?page=${data.page + 1}" aria-label="Próximo">
                                            <span aria-hidden="true">&raquo;</span>
                                        </a>
                                    </li>
                                </ul>
                            </nav>`;
                    } else if (data.success === false) {
                        console.warn('Nenhum resultado encontrado.');
                        tabelaContainer.innerHTML = '<p class="text-warning">Nenhum resultado encontrado.</p>';
                        paginacaoContainer.innerHTML = '';
                    } else {
                        console.error('Resposta inválida do servidor:', data);
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
