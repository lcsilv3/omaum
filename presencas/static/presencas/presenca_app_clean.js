// JS principal do fluxo de registro de presenças
// Extensão do objeto PresencaApp (se já existir) ou criação se não existir

if (!window.PresencaApp) {
    window.PresencaApp = {};
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

// Função para abrir modal de presença
window.PresencaApp.abrirModalPresenca = function(atividadeId, dia) {
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
            modalAtividadeNome.innerHTML = '';
        }
    }
    
    const modal = document.getElementById('presencaModal');
    modal.style.display = 'flex';
    modal.classList.add('show');
    document.body.classList.add('modal-open');
    
    window.PresencaApp.preencherListaAlunos();
};

// Função para preencher lista de alunos no modal
window.PresencaApp.preencherListaAlunos = function() {
    const container = document.getElementById('alunosContainer');
    container.innerHTML = '';
    
    if (window.PresencaApp.alunosData.length === 0) {
        container.innerHTML = '<div class="alert alert-warning"><i class="fas fa-exclamation-triangle me-2"></i>Nenhum aluno encontrado para esta turma. Verifique se há alunos matriculados e ativos.</div>';
        return;
    }
    
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
    });
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
    if (!window.PresencaApp.atividadeAtual || !window.PresencaApp.diaAtual) return;
    if (!window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual]) return;
    if (!window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual]) return;
    
    const presencaAtual = window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual][cpfAluno];
    if (presencaAtual) {
        presencaAtual.justificativa = valor;
    }
};

window.PresencaApp.fecharModalPresenca = function() {
    const modal = document.getElementById('presencaModal');
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('show');
        document.body.classList.remove('modal-open');
    } else {
        console.error('❌ [CRÍTICO] Modal presencaModal não encontrado!');
    }
};

window.PresencaApp.carregarAlunos = function() {
    // Função placeholder
};

// Função para marcar todos os alunos como presentes
window.PresencaApp.marcarTodosPresentes = function() {
    if (!window.PresencaApp.atividadeAtual || !window.PresencaApp.diaAtual) {
        console.error('❌ [CRÍTICO] Atividade ou dia atual não definidos!');
        return;
    }
    
    window.PresencaApp.alunosData.forEach(function(aluno) {
        const cpfAluno = aluno.cpf || aluno.id;
        if (!window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual]) {
            window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual] = {};
        }
        if (!window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual]) {
            window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual] = {};
        }
        window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual][cpfAluno] = {
            presente: true,
            justificativa: ''
        };
    });
    
    window.PresencaApp.preencherListaAlunos();
};

// Função para marcar todos os alunos como ausentes
window.PresencaApp.marcarTodosAusentes = function() {
    if (!window.PresencaApp.atividadeAtual || !window.PresencaApp.diaAtual) {
        console.error('❌ [CRÍTICO] Atividade ou dia atual não definidos!');
        return;
    }
    
    window.PresencaApp.alunosData.forEach(function(aluno) {
        const cpfAluno = aluno.cpf || aluno.id;
        if (!window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual]) {
            window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual] = {};
        }
        if (!window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual]) {
            window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual] = {};
        }
        window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual][window.PresencaApp.diaAtual][cpfAluno] = {
            presente: false,
            justificativa: ''
        };
    });
    
    window.PresencaApp.preencherListaAlunos();
};

// Função para salvar presenças do dia atual e fechar modal
window.PresencaApp.salvarDiaAtual = function() {
    const form = document.getElementById('form-presenca');
    if (!form) {
        console.error('❌ [CRÍTICO] Formulário form-presenca não encontrado!');
        return;
    }
    
    const presencasDoAtividadeAtual = window.PresencaApp.presencasRegistradas[window.PresencaApp.atividadeAtual];
    if (!presencasDoAtividadeAtual) {
        window.PresencaApp.fecharModalPresenca();
        return;
    }
    
    const presencasDoDiaAtual = presencasDoAtividadeAtual[window.PresencaApp.diaAtual];
    if (!presencasDoDiaAtual) {
        window.PresencaApp.fecharModalPresenca();
        return;
    }
    
    // Remove campos antigos do dia/atividade para evitar duplicatas
    const fieldsToRemove = form.querySelectorAll(
        `input[name^="presenca_${window.PresencaApp.atividadeAtual}_${window.PresencaApp.diaAtual}_"], ` +
        `input[name^="justificativa_${window.PresencaApp.atividadeAtual}_${window.PresencaApp.diaAtual}_"]`
    );
    fieldsToRemove.forEach(field => field.remove());
    
    // Adiciona cada presença como campo hidden no formulário
    for (const [cpfAluno, presencaData] of Object.entries(presencasDoDiaAtual)) {
        const fieldName = `presenca_${window.PresencaApp.atividadeAtual}_${window.PresencaApp.diaAtual}_${cpfAluno}`;
        const fieldValue = presencaData.presente ? "1" : "0";
        
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = fieldName;
        input.value = fieldValue;
        form.appendChild(input);
        
        // Se houver justificativa, adiciona também
        if (presencaData.justificativa && presencaData.justificativa.trim()) {
            const justificativaFieldName = `justificativa_${window.PresencaApp.atividadeAtual}_${window.PresencaApp.diaAtual}_${cpfAluno}`;
            const justificativaInput = document.createElement('input');
            justificativaInput.type = 'hidden';
            justificativaInput.name = justificativaFieldName;
            justificativaInput.value = presencaData.justificativa;
            form.appendChild(justificativaInput);
        }
    }
    
    window.PresencaApp.fecharModalPresenca();
};

// ===== INICIALIZAÇÃO DO FLATPICKR PARA SELEÇÃO DE DIAS =====
window.initializeFlatpickr = function initializeFlatpickr() {
    if (typeof flatpickr === 'undefined') {
        console.error('❌ [CRÍTICO] Flatpickr não está disponível!');
        return;
    }
    
    const inputs = document.querySelectorAll('.dias-datepicker');
    
    if (inputs.length === 0) {
        console.warn('⚠️ Nenhum elemento .dias-datepicker encontrado no DOM');
        return;
    }
    
    inputs.forEach(function(input, index) {
        const atividadeId = input.dataset.atividade;
        const maxDias = parseInt(input.dataset.maxdias) || 999;
        
        try {
            const fp = flatpickr(input, {
                mode: 'multiple',
                dateFormat: 'd/m/Y',
                locale: 'pt',
                inline: false,
                minDate: window.ano ? new Date(window.ano, window.mes - 1, 1) : undefined,
                maxDate: window.ano ? new Date(window.ano, window.mes, 0) : undefined,
                defaultDate: [],
                conjunction: ', ',
                onChange: function(selectedDates, dateStr, instance) {
                    // Valida limite de dias
                    if (selectedDates.length > maxDias) {
                        alert(`Você pode selecionar no máximo ${maxDias} dia(s) para esta atividade.`);
                        selectedDates.splice(maxDias);
                        instance.setDate(selectedDates, false);
                        return;
                    }
                    
                    // Mostra mensagem se atingiu o limite
                    const msgElem = document.getElementById(`msg-limite-${atividadeId}`);
                    if (msgElem) {
                        if (selectedDates.length >= maxDias) {
                            msgElem.innerHTML = `<small class="text-warning">⚠️ Limite de ${maxDias} dia(s) atingido</small>`;
                        } else {
                            msgElem.innerHTML = `<small class="text-muted">${selectedDates.length}/${maxDias} dia(s) selecionado(s)</small>`;
                        }
                    }
                    
                    // Atualiza botões de marcação de presença
                    const obsContainer = document.getElementById(`obs-dias-${atividadeId}`);
                    if (obsContainer) {
                        obsContainer.innerHTML = '';
                        
                        selectedDates.forEach(function(date) {
                            const dia = date.getDate();
                            const buttonDiv = document.createElement('div');
                            buttonDiv.className = 'obs-dia-item';
                            buttonDiv.innerHTML = `
                                <button type="button" class="btn btn-primary btn-sm" 
                                        onclick="window.PresencaApp.abrirModalPresenca(${atividadeId}, ${dia})">
                                    <i class="fas fa-users me-1"></i>
                                    ${dia.toString().padStart(2, '0')}/${window.mes.toString().padStart(2, '0')} - Marcar Presenças
                                </button>
                            `;
                            obsContainer.appendChild(buttonDiv);
                        });
                    }
                }
            });
            
            // Adiciona evento no ícone do calendário
            const icon = input.nextElementSibling;
            if (icon && icon.classList.contains('calendar-icon')) {
                icon.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    fp.open();
                });
            }
        } catch (error) {
            console.error(`❌ [CRÍTICO] Erro ao inicializar calendário para atividade ${atividadeId}:`, error);
        }
    });
}

// Listener para evento flatpickr-ready
document.addEventListener('flatpickr-ready', function() {
    window.initializeFlatpickr();
});

// Se DOM já tiver carregado quando este script executar
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        if (typeof flatpickr !== 'undefined') {
            setTimeout(() => {
                window.initializeFlatpickr();
            }, 100);
        }
    });
} else {
    if (typeof flatpickr !== 'undefined') {
        window.initializeFlatpickr();
    }
}
