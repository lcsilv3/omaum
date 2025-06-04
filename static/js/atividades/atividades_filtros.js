document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando script de filtros de atividades');
    
    // Encontrar os elementos do formulário
    const cursoSelect = document.querySelector('#id_curso');
    const turmaSelect = document.querySelector('#id_turmas');
    
    if (!cursoSelect || !turmaSelect) {
        console.log('Elementos de filtro não encontrados', {
            cursoSelect: cursoSelect ? cursoSelect.id : 'não encontrado',
            turmaSelect: turmaSelect ? turmaSelect.id : 'não encontrado'
        });
        return;
    }
    
    console.log('Elementos encontrados:', {
        cursoSelect: cursoSelect.id,
        turmaSelect: turmaSelect.id
    });
    
    // Função para atualizar as turmas quando o curso mudar
    cursoSelect.addEventListener('change', function() {
        const cursoId = this.value;
        console.log('Curso selecionado:', cursoId);
        
        // Se não houver curso selecionado, limpa as turmas
        if (!cursoId) {
            // Manter apenas a primeira opção (Todas as turmas)
            const primeiraOpcao = turmaSelect.options[0];
            turmaSelect.innerHTML = '';
            turmaSelect.appendChild(primeiraOpcao);
            return;
        }
        
        // Buscar as turmas do curso selecionado
        fetch(`/atividades/ajax/turmas-por-curso/?curso_id=${cursoId}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro na resposta: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Turmas recebidas:', data);
            
            // Limpar o select de turmas mantendo a primeira opção
            const primeiraOpcao = turmaSelect.options[0];
            turmaSelect.innerHTML = '';
            turmaSelect.appendChild(primeiraOpcao);
            
            // Adicionar as novas opções
            if (data.turmas && data.turmas.length > 0) {
                data.turmas.forEach(turma => {
                    const option = document.createElement('option');
                    option.value = turma.id;
                    option.textContent = turma.nome;
                    turmaSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Erro ao buscar turmas:', error);
        });
    });
});