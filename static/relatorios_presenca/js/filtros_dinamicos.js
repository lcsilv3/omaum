document.addEventListener('DOMContentLoaded', function() {
    const cursoSelect = document.getElementById('curso_id');
    const turmaSelect = document.getElementById('turma_id');
    const alunoSelect = document.getElementById('aluno_id'); // Assuming an aluno select will be added later

    // Function to fetch turmas based on selected curso
    function fetchTurmas() {
        const cursoId = cursoSelect.value;
        if (!cursoId) {
            turmaSelect.innerHTML = '<option value="">Selecione uma Turma</option>';
            turmaSelect.disabled = true;
            alunoSelect.innerHTML = '<option value="">Selecione um Aluno</option>';
            alunoSelect.disabled = true;
            return;
        }
        turmaSelect.innerHTML = '<option value="">Carregando turmas...</option>';
        turmaSelect.disabled = true;
        alunoSelect.innerHTML = '<option value="">Selecione um Aluno</option>';
        alunoSelect.disabled = true;
        fetch(`/relatorios-presenca/ajax/turmas-por-curso/?curso_id=${cursoId}`)
            .then(response => {
                if (!response.ok) throw new Error('Erro ao buscar turmas. Código: ' + response.status);
                return response.json();
            })
            .then(data => {
                if (data.turmas && data.turmas.length > 0) {
                    turmaSelect.innerHTML = '<option value="">Selecione uma Turma</option>';
                    data.turmas.forEach(turma => {
                        const option = document.createElement('option');
                        option.value = turma.id;
                        option.textContent = turma.nome;
                        turmaSelect.appendChild(option);
                    });
                    turmaSelect.disabled = false;
                } else {
                    turmaSelect.innerHTML = '<option value="">Nenhuma turma encontrada</option>';
                }
                alunoSelect.innerHTML = '<option value="">Selecione um Aluno</option>';
                alunoSelect.disabled = true;
            })
            .catch(error => {
                turmaSelect.innerHTML = `<option value="">${error.message || 'Erro ao buscar turmas.'}</option>`;
            });
    }

    // Function to fetch alunos based on selected turma
    function fetchAlunos() {
        const turmaId = turmaSelect.value;
        if (!turmaId) {
            alunoSelect.innerHTML = '<option value="">Selecione um Aluno</option>';
            alunoSelect.disabled = true;
            return;
        }
        alunoSelect.innerHTML = '<option value="">Carregando alunos...</option>';
        alunoSelect.disabled = true;
        fetch(`/relatorios-presenca/ajax/alunos-por-turma/?turma_id=${turmaId}`)
            .then(response => {
                if (!response.ok) throw new Error('Erro ao buscar alunos. Código: ' + response.status);
                return response.json();
            })
            .then(data => {
                if (data.alunos && data.alunos.length > 0) {
                    alunoSelect.innerHTML = '<option value="">Selecione um Aluno</option>';
                    data.alunos.forEach(aluno => {
                        const option = document.createElement('option');
                        option.value = aluno.id;
                        option.textContent = aluno.nome;
                        alunoSelect.appendChild(option);
                    });
                    alunoSelect.disabled = false;
                } else {
                    alunoSelect.innerHTML = '<option value="">Nenhum aluno encontrado</option>';
                }
            })
            .catch(error => {
                alunoSelect.innerHTML = `<option value="">${error.message || 'Erro ao buscar alunos.'}</option>`;
            });
    }


    // --- AJAX para busca e exportação do boletim do aluno ---
    const btnBuscar = document.getElementById('btnBuscar');
    const btnExportarCSV = document.getElementById('btnExportarCSV');
    const btnExportarPDF = document.getElementById('btnExportarPDF');
    const tabelaBoletim = document.getElementById('tabela-boletim');
    const mesInput = document.getElementById('mes');
    const anoInput = document.getElementById('ano');

    function getBoletimParams() {
        return {
            curso_id: cursoSelect.value,
            turma_id: turmaSelect.value,
            aluno_id: alunoSelect.value,
            mes: mesInput.value,
            ano: anoInput.value
        };
    }

    function montarQueryString(params) {
        return Object.entries(params)
            .filter(([_, v]) => v)
            .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
            .join('&');
    }

    function mostrarSpinner() {
        tabelaBoletim.innerHTML = '<div class="text-center my-3" role="status" aria-live="polite"><div class="spinner-border text-primary" role="status" aria-label="Carregando"></div><div>Carregando boletim...</div></div>';
    }

    function buscarBoletimAJAX() {
        const params = getBoletimParams();
        if (!params.aluno_id || !params.mes || !params.ano) {
            tabelaBoletim.innerHTML = '<div class="alert alert-warning" role="alert">Preencha todos os filtros obrigatórios.</div>';
            return;
        }
        const url = `/relatorios-presenca/boletim/aluno/?${montarQueryString(params)}&partial=1`;
        mostrarSpinner();
        fetch(url, { credentials: 'same-origin' })
            .then(r => {
                if (!r.ok) throw new Error('Erro ao buscar boletim. Código: ' + r.status);
                return r.text();
            })
            .then(html => { tabelaBoletim.innerHTML = html; })
            .catch(err => {
                tabelaBoletim.innerHTML = `<div class="alert alert-danger" role="alert">${err.message || 'Erro inesperado ao buscar boletim.'}</div>`;
            });
    }

    function exportarBoletim(formato) {
        const params = getBoletimParams();
        if (!params.aluno_id || !params.mes || !params.ano) {
            alert('Preencha todos os filtros obrigatórios.');
            return;
        }
        const url = `/relatorios-presenca/boletim/aluno/?${montarQueryString(params)}&formato=${formato}`;
        window.open(url, '_blank');
    }

    if (btnBuscar) btnBuscar.addEventListener('click', buscarBoletimAJAX);
    if (btnExportarCSV) btnExportarCSV.addEventListener('click', function() { exportarBoletim('csv'); });
    if (btnExportarPDF) btnExportarPDF.addEventListener('click', function() { exportarBoletim('pdf'); });

    // Event Listeners para combos
    if (cursoSelect) {
        cursoSelect.addEventListener('change', fetchTurmas);
    }
    if (turmaSelect) {
        turmaSelect.addEventListener('change', fetchAlunos);
    }

    // Initial state
    fetchTurmas(); // Populate turmas if a curso is pre-selected
    fetchAlunos(); // Populate alunos if a turma is pre-selected
});