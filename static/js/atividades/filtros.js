document.addEventListener('DOMContentLoaded', function () {
    const $form = document.getElementById('filtro-atividades');
    const $q = document.getElementById('id_q');
    const $curso = document.getElementById('id_curso');
    const $turma = document.getElementById('id_turmas');
    const $tabela = document.querySelector('.table-responsive tbody');
    const $alerta = document.getElementById('alerta-nenhum-resultado');

    // Dica extra: sempre inicia o alerta oculto
    $alerta.style.display = 'none';

    function atualizaFiltros(mantemCurso = true, mantemTurma = true) {
        const params = new URLSearchParams(new FormData($form)).toString();
        fetch('/atividades/api/filtrar-atividades/?' + params, {
            headers: { 'x-requested-with': 'XMLHttpRequest' }
        })
            .then(resp => resp.json())
            .then(data => {
                // Atualiza tabela
                $tabela.innerHTML = data.atividades_html;

                // Mostra/oculta alerta de nenhum resultado
                if (
                    data.atividades_html.includes('Nenhuma atividade encontrada')
                ) {
                    $alerta.style.display = 'block';
                } else {
                    $alerta.style.display = 'none';
                }

                // Atualiza cursos mantendo seleção
                const cursoSelecionado = mantemCurso ? $curso.value : '';
                $curso.innerHTML = '';
                const optTodosCursos = document.createElement('option');
                optTodosCursos.value = '';
                optTodosCursos.textContent = 'Todos os cursos';
                $curso.appendChild(optTodosCursos);

                if (data.cursos.length > 0) {
                    data.cursos.forEach(curso => {
                        const opt = document.createElement('option');
                        opt.value = curso.id;
                        opt.textContent = curso.nome;
                        if (String(curso.id) === String(cursoSelecionado)) {
                            opt.selected = true;
                        }
                        $curso.appendChild(opt);
                    });
                } else {
                    // Se não houver cursos, mantém apenas a opção "Todos"
                    optTodosCursos.selected = true;
                }

                // Atualiza turmas mantendo seleção
                const turmaSelecionada = mantemTurma ? $turma.value : '';
                $turma.innerHTML = '';
                const optTodasTurmas = document.createElement('option');
                optTodasTurmas.value = '';
                optTodasTurmas.textContent = 'Todas as turmas';
                $turma.appendChild(optTodasTurmas);

                if (data.turmas.length > 0) {
                    data.turmas.forEach(turma => {
                        const opt = document.createElement('option');
                        opt.value = turma.id;
                        opt.textContent = turma.nome;
                        if (String(turma.id) === String(turmaSelecionada)) {
                            opt.selected = true;
                        }
                        $turma.appendChild(opt);
                    });
                } else {
                    // Se não houver turmas, mantém apenas a opção "Todas"
                    optTodasTurmas.selected = true;
                }

                // Se só houver um curso possível para a turma selecionada, seleciona automaticamente
                if (!cursoSelecionado && data.cursos.length === 1) {
                    $curso.value = data.cursos[0].id;
                }
                // Se só houver uma turma possível para o curso selecionado, seleciona automaticamente
                if (!turmaSelecionada && data.turmas.length === 1) {
                    $turma.value = data.turmas[0].id;
                }
            });
    }

    // Atualiza a tabela automaticamente ao digitar (com debounce)
    let debounceTimer;
    $q.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            atualizaFiltros(true, true);
        }, 300); // 300ms de atraso
    });

    $curso.addEventListener('change', function () {
        // Ao trocar o curso, limpa turma selecionada
        $turma.value = '';
        atualizaFiltros(true, false);
    });

    $turma.addEventListener('change', function () {
        // Ao trocar a turma, pode ser necessário ajustar o curso
        atualizaFiltros(false, true);
    });

    $form.addEventListener('submit', function (e) {
        e.preventDefault();
        atualizaFiltros(true, true);
    });
});