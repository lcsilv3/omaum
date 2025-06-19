/**
 * Centraliza o carregamento dinâmico das turmas ao selecionar um curso.
 * Para funcionar, os campos devem ter os IDs padrão: id_curso e id_turmas.
 * Opcional: inclua um elemento com id="no-turmas-msg" para mensagens.
 * 
 * Chame: window.initTurmasAjax({ url: '/atividades/ajax/turmas-por-curso/' });
 */
window.initTurmasAjax = function(options) {
    const cursoSelect = document.getElementById('id_curso');
    const turmasSelect = document.getElementById('id_turmas');
    const selectAllTurmas = document.getElementById('select-all-turmas');
    let noTurmasMsg = document.getElementById('no-turmas-msg');
    const url = options && options.url ? options.url : '/atividades/ajax/turmas-por-curso/';

    if (!cursoSelect || !turmasSelect) return;

    if (!noTurmasMsg) {
        noTurmasMsg = document.createElement('div');
        noTurmasMsg.id = 'no-turmas-msg';
        noTurmasMsg.className = 'text-muted mt-2';
        turmasSelect.parentNode.appendChild(noTurmasMsg);
    }

    function atualizarTurmas(cursoId, turmasSelecionadas=[]) {
        if (!cursoId) {
            turmasSelect.innerHTML = '';
            noTurmasMsg.textContent = '';
            return;
        }
        fetch(`${url}?curso=${cursoId}`)
            .then(response => response.json())
            .then(data => {
                turmasSelect.innerHTML = '';
                if (data.turmas.length === 0) {
                    noTurmasMsg.textContent = 'Não há turmas para este curso.';
                } else {
                    noTurmasMsg.textContent = '';
                    data.turmas.forEach(function(turma) {
                        const option = document.createElement('option');
                        option.value = turma.id;
                        option.textContent = turma.nome;
                        if (turmasSelecionadas.includes(String(turma.id))) {
                            option.selected = true;
                        }
                        turmasSelect.appendChild(option);
                    });
                }
            });
    }

    cursoSelect.addEventListener('change', function() {
        atualizarTurmas(this.value);
    });

    // Ao carregar a página, filtra as turmas se já houver curso selecionado
    const turmasSelecionadas = Array.from(turmasSelect.selectedOptions).map(opt => opt.value);
    if (cursoSelect.value) {
        atualizarTurmas(cursoSelect.value, turmasSelecionadas);
    } else {
        turmasSelect.innerHTML = '';
        noTurmasMsg.textContent = '';
    }

    // Selecionar todas as turmas (se existir o checkbox)
    if (selectAllTurmas && turmasSelect) {
        selectAllTurmas.addEventListener('change', function() {
            for (let option of turmasSelect.options) {
                option.selected = this.checked;
            }
        });
        turmasSelect.addEventListener('change', function() {
            selectAllTurmas.checked = Array.from(turmasSelect.options).every(opt => opt.selected);
        });
    }
};