// JS principal do fluxo de registro de presenças
// Extensão do objeto PresencaApp (se já existir) ou criação se não existir
console.log('🔧 [JS] Carregando presenca_app.js...');
console.log('🔧 [JS] PresencaApp atual:', window.PresencaApp);

if (!window.PresencaApp) {
    window.PresencaApp = {};
    console.log('🔧 [JS] PresencaApp criado do zero');
} else {
    console.log('🔧 [JS] PresencaApp já existe, estendendo...');
}

// Adiciona propriedades ao objeto existente ou cria-as se não existirem
Object.assign(window.PresencaApp, {
    modalAtual: window.PresencaApp.modalAtual || null,
    diaAtual: window.PresencaApp.diaAtual || null,
    atividadeAtual: window.PresencaApp.atividadeAtual || null,
    alunosData: window.PresencaApp.alunosData || [],
    presencasRegistradas: window.PresencaApp.presencasRegistradas || {},
    turmaIdFinal: window.PresencaApp.turmaIdFinal || undefined,
    atividadeAtualConvocada: window.PresencaApp.atividadeAtualConvocada || false,
    atividadesConvocadas: window.PresencaApp.atividadesConvocadas || {},
    atividadesNomes: window.PresencaApp.atividadesNomes || {},
    convocadosIndividuais: window.PresencaApp.convocadosIndividuais || {}
});

// Função para abrir modal de presença (FUNÇÃO PRINCIPAL CRÍTICA)
window.PresencaApp.abrirModalPresenca = function(atividadeId, dia) {
    console.log('🚀 [DEBUG] abrirModalPresenca chamada!', { atividadeId, dia });
    console.log('🚀 [DEBUG] PresencaApp atual:', window.PresencaApp);
    console.log('🚀 [DEBUG] presencasRegistradas:', JSON.parse(JSON.stringify(window.PresencaApp.presencasRegistradas)));
    
    window.PresencaApp.atividadeAtual = atividadeId;
    window.PresencaApp.diaAtual = dia;
    window.PresencaApp.atividadeAtualConvocada = window.PresencaApp.atividadesConvocadas ? window.PresencaApp.atividadesConvocadas[atividadeId] === true : false;
    
    // Inicializa presenças como presente para todos os alunos se ainda não houver registro
    if (!window.PresencaApp.presencasRegistradas[atividadeId]) {
        window.PresencaApp.presencasRegistradas[atividadeId] = {};
    }
    if (!window.PresencaApp.presencasRegistradas[atividadeId][dia]) {
        window.PresencaApp.presencasRegistradas[atividadeId][dia] = {};
        if (window.PresencaApp.alunosData && window.PresencaApp.alunosData.length > 0) {
            window.PresencaApp.alunosData.forEach(function(aluno) {
                const cpfAluno = aluno.cpf || aluno.id;
                window.PresencaApp.presencasRegistradas[atividadeId][dia][cpfAluno] = {
                    presente: true,
                    justificativa: ''
                };
            });
        }
    }
    
    var nomeAtividade = window.PresencaApp.atividadesNomes ? window.PresencaApp.atividadesNomes[atividadeId] || '' : '';
    
    // Linha 1: nome da atividade (data selecionada)
    var modalTitle = document.getElementById('modalTitle');
    let dataFormatada = '';
    if (window.PresencaApp.diaAtual) {
        const hoje = new Date();
        const mes = (hoje.getMonth() + 1).toString().padStart(2, '0');
        const ano = hoje.getFullYear();
        const diaStr = window.PresencaApp.diaAtual.toString().padStart(2, '0');
        dataFormatada = `${diaStr}/${mes}/${ano}`;
    }
    if (modalTitle) {
        const tituloCompleto = nomeAtividade ? 
            `${nomeAtividade}${dataFormatada ? ' (' + dataFormatada + ')' : ''}` : 
            `Marcar Presença${dataFormatada ? ' - (' + dataFormatada + ')' : ''}`;
        modalTitle.textContent = tituloCompleto;
    }
    
    // Linha 2: "Atividade com convocação" apenas se houver convocação
    var modalAtividadeNome = document.getElementById('modalAtividadeNome');
    if (modalAtividadeNome) {
        if (window.PresencaApp.atividadeAtualConvocada) {
            modalAtividadeNome.innerHTML = '<span style="font-size:0.92em;color:#b8860b;">Atividade com convocação</span>';
        } else {
            modalAtividadeNome.innerHTML = ''; // Limpa a segunda linha se não houver convocação
        }
    }
    
    const modal = document.getElementById('presencaModal');
    modal.style.display = 'flex';
    modal.classList.add('show');
    document.body.classList.add('modal-open');
    
    console.log('🚀 [DEBUG] Modal aberto, chamando preencherListaAlunos...');
    window.PresencaApp.preencherListaAlunos();
};

// Função para preencher lista de alunos no modal
window.PresencaApp.preencherListaAlunos = function() {
    console.log('📋 [DEBUG] preencherListaAlunos chamada');
    const container = document.getElementById('alunosContainer');
    container.innerHTML = '';
    
    if (window.PresencaApp.alunosData.length === 0) {
        container.innerHTML = '<div class="alert alert-warning"><i class="fas fa-exclamation-triangle me-2"></i>Nenhum aluno encontrado para esta turma. Verifique se há alunos matriculados e ativos.</div>';
        console.log('⚠️ [DEBUG] Nenhum aluno disponível');
        return;
    }
    
    console.log('📋 [DEBUG] Preenchendo lista com', window.PresencaApp.alunosData.length, 'alunos');
    
    window.PresencaApp.alunosData.forEach(function(aluno) {
        const cpfAluno = aluno.cpf || aluno.id;
        const presencaAtual = window.PresencaApp.obterPresencaAluno(window.PresencaApp.atividadeAtual, window.PresencaApp.diaAtual, cpfAluno);
        
        // Nome truncado com tooltip
        const nomeAlunoDiv = document.createElement('div');
        nomeAlunoDiv.className = 'aluno-nome';
        let nomeExibido = aluno.nome;
        if (aluno.nome.length > 25) {
            nomeExibido = aluno.nome.slice(0, 25) + '...';
        }
        nomeAlunoDiv.textContent = nomeExibido;
        nomeAlunoDiv.title = aluno.nome;
        nomeAlunoDiv.style.fontSize = '0.95em';
        
        // Container de controles
        const controlesDiv = document.createElement('div');
        controlesDiv.className = 'aluno-controles d-flex align-items-center';
        controlesDiv.style.gap = '8px';
        
        // Badge de presença (padrão: Presente)
        const botaoPresenca = document.createElement('button');
        botaoPresenca.type = 'button';
        const presentePadrao = presencaAtual && typeof presencaAtual.presente !== 'undefined' ? presencaAtual.presente : true;
        botaoPresenca.className = `badge-presenca badge-uniforme ${presentePadrao ? 'badge-presente' : 'badge-ausente'}`;
        botaoPresenca.onclick = function() { window.PresencaApp.togglePresencaAluno(cpfAluno, botaoPresenca); };
        botaoPresenca.textContent = presentePadrao ? 'Presente' : 'Ausente';
        botaoPresenca.style.fontSize = '0.95em';
        botaoPresenca.style.height = '28px';
        botaoPresenca.style.minWidth = '80px';
        botaoPresenca.style.display = 'flex';
        botaoPresenca.style.alignItems = 'center';
        
        // Campo de justificativa ao lado do badge
        const justificativaDiv = document.createElement('div');
        justificativaDiv.className = 'justificativa-campo';
        justificativaDiv.style.marginTop = '0';
        justificativaDiv.style.display = presentePadrao ? 'none' : 'block';
        justificativaDiv.style.maxWidth = '180px';
        justificativaDiv.style.minWidth = '120px';
        
        // Truncar justificativa e mostrar tooltip
        const justificativaInput = document.createElement('input');
        justificativaInput.type = 'text';
        justificativaInput.className = 'form-control form-control-sm';
        justificativaInput.placeholder = 'Justificativa (opcional)';
        justificativaInput.value = presencaAtual && presencaAtual.justificativa ? presencaAtual.justificativa : '';
        justificativaInput.onchange = function() { window.PresencaApp.atualizarJustificativa(cpfAluno, this.value); };
        justificativaInput.maxLength = 200;
        justificativaInput.style.fontSize = '0.95em';
        justificativaInput.oninput = function() {
            if (this.value.length > 25) {
                this.title = this.value;
                this.value = this.value.slice(0, 25);
            } else {
                this.title = '';
            }
        };
        if (justificativaInput.value.length > 25) {
            justificativaInput.title = justificativaInput.value;
            justificativaInput.value = justificativaInput.value.slice(0, 25);
        }
        justificativaDiv.appendChild(justificativaInput);
        controlesDiv.appendChild(botaoPresenca);
        controlesDiv.appendChild(justificativaDiv);
        
        const alunoDiv = document.createElement('div');
        alunoDiv.className = 'aluno-presenca-item';
        alunoDiv.style.fontSize = '0.95em';
        
        alunoDiv.appendChild(nomeAlunoDiv);
        alunoDiv.appendChild(controlesDiv);
        container.appendChild(alunoDiv);
        
        console.log('📋 [DEBUG] Aluno adicionado:', aluno.nome, '- Presente:', presentePadrao);
    });
    
    console.log('✅ [DEBUG] Lista de alunos preenchida com sucesso!');
};

// Outras funções necessárias
window.PresencaApp.obterPresencaAluno = function(atividadeId, dia, cpfAluno) {
    if (
        window.PresencaApp.presencasRegistradas[atividadeId] &&
        window.PresencaApp.presencasRegistradas[atividadeId][dia] &&
        window.PresencaApp.presencasRegistradas[atividadeId][dia][cpfAluno]
    ) {
        return window.PresencaApp.presencasRegistradas[atividadeId][dia][cpfAluno];
    } else {
        return undefined;
    }
};

window.PresencaApp.togglePresencaAluno = function(cpfAluno, botaoPresenca) {
    if (!window.PresencaApp.atividadeAtual || !window.PresencaApp.diaAtual) return;
    if (!window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual]) {
        window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual] = {};
    }
    if (!window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual]) {
        window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual] = {};
    }
    const atual = window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual][cpfAluno];
    let novoPresente;
    if (!atual) {
        novoPresente = true;
    } else {
        novoPresente = !atual.presente;
    }
    window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual][cpfAluno] = {
        presente: novoPresente,
        justificativa: atual ? atual.justificativa : ''
    };
    if (botaoPresenca) {
        botaoPresenca.classList.toggle('badge-presente', novoPresente);
        botaoPresenca.classList.toggle('badge-ausente', !novoPresente);
        botaoPresenca.textContent = novoPresente ? 'Presente' : 'Ausente';
        const justificativaDiv = botaoPresenca.parentElement.querySelector('.justificativa-campo');
        if (justificativaDiv) {
            justificativaDiv.style.display = novoPresente ? 'none' : 'block';
        }
    }
};

window.PresencaApp.atualizarJustificativa = function(cpfAluno, valor) {
    // Atualiza justificativa no objeto de presenças
    if (!window.PresencaApp.atividadeAtual || !window.PresencaApp.diaAtual) return;
    if (!window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual]) return;
    if (!window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual]) return;
    
    const presencaAtual = window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual][cpfAluno];
    if (presencaAtual) {
        presencaAtual.justificativa = valor;
    }
};

window.PresencaApp.fecharModalPresenca = function() {
    console.log('🚪 [DEBUG] Fechando modal...');
    console.log('🚪 [DEBUG-TRANSIÇÃO] fecharModalPresenca CHAMADA! Stack trace:');
    console.trace('🚪 [DEBUG-TRANSIÇÃO] Stack trace da chamada fecharModalPresenca');
    
    const modal = document.getElementById('presencaModal');
    if (modal) {
        console.log('🚪 [DEBUG-TRANSIÇÃO] Modal encontrado, aplicando fechamento...');
        modal.style.display = 'none';
        modal.classList.remove('show');
        document.body.classList.remove('modal-open');
        console.log('✅ [DEBUG] Modal fechado com sucesso!');
        console.log('✅ [DEBUG-TRANSIÇÃO] Modal realmente fechado - display:', modal.style.display);
    } else {
        console.error('❌ [DEBUG-TRANSIÇÃO] Modal não encontrado para fechar!');
    }
};

window.PresencaApp.carregarAlunos = function() {
    // Função placeholder - pode ser implementada conforme necessário
    console.log('🔧 [DEBUG] carregarAlunos - função disponível');
};

console.log('✅ [JS] presenca_app.js carregado com sucesso!');
console.log('✅ [JS] PresencaApp.abrirModalPresenca disponível:', typeof window.PresencaApp.abrirModalPresenca);
console.log('✅ [JS] Objeto final:', window.PresencaApp);
