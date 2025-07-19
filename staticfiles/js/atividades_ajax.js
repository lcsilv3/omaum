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
    let todasTurmas = []; // Armazenar todas as turmas carregadas

    if (!cursoSelect || !turmasSelect) return;

    if (!noTurmasMsg) {
        noTurmasMsg = document.createElement('div');
        noTurmasMsg.id = 'no-turmas-msg';
        noTurmasMsg.className = 'text-muted mt-2';
        turmasSelect.parentNode.appendChild(noTurmasMsg);
    }

    function carregarTodasTurmas() {
        fetch(`${url}`) // Sem parâmetro curso carrega todas
            .then(response => response.json())
            .then(data => {
                todasTurmas = data.turmas || [];
                atualizarTurmasDisplay();
            })
            .catch(error => {
                console.error('Erro ao carregar turmas:', error);
                noTurmasMsg.textContent = 'Erro ao carregar turmas.';
            });
    }

    function atualizarTurmasDisplay(cursoId = null, turmasSelecionadas = []) {
        turmasSelect.innerHTML = '';
        
        let turmasFiltradas = todasTurmas;
        if (cursoId) {
            turmasFiltradas = todasTurmas.filter(turma => turma.curso_id == cursoId);
        }

        if (turmasFiltradas.length === 0) {
            if (cursoId) {
                noTurmasMsg.textContent = 'Não há turmas para este curso.';
            } else {
                noTurmasMsg.textContent = 'Nenhuma turma cadastrada.';
            }
        } else {
            noTurmasMsg.textContent = '';
            turmasFiltradas.forEach(function(turma) {
                const option = document.createElement('option');
                option.value = turma.id;
                option.textContent = turma.nome;
                if (turmasSelecionadas.includes(String(turma.id))) {
                    option.selected = true;
                }
                turmasSelect.appendChild(option);
            });
        }
    }

    function atualizarTurmas(cursoId, turmasSelecionadas=[]) {
        atualizarTurmasDisplay(cursoId, turmasSelecionadas);
    }

    cursoSelect.addEventListener('change', function() {
        atualizarTurmas(this.value);
    });

    // Carregar todas as turmas na inicialização
    carregarTodasTurmas();
    
    // Se há um curso pré-selecionado, aplicar o filtro após carregar as turmas
    if (cursoSelect.value) {
        const turmasSelecionadas = Array.from(turmasSelect.selectedOptions).map(opt => opt.value);
        // Aguardar o carregamento das turmas antes de filtrar
        setTimeout(() => {
            atualizarTurmas(cursoSelect.value, turmasSelecionadas);
        }, 100);
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