/**
 * PRESENÇA MANAGER - ARQUITETURA SIMPLIFICADA
 * Supervisor: Agente Django Web Autônomo
 * Substitui: presenca_app.js + registrar_presenca_dias_atividades.js + registrar_presenca_dias_atividades_submit.js
 * 
 * FILOSOFIA:
 * - UM arquivo, UMA responsabilidade
 * - Controle MANUAL pelo usuário
 * - SEM navegação automática
 * - SEM interceptadores complexos
 * - Fluxo LINEAR e previsível
 */

window.PresencaManager = {
    // 📊 ESTADO CENTRALIZADO
    turmaId: null,
    atividades: {},
    alunosData: [],
    
    // 🎯 CONTROLE DE FLUXO
    atividadeAtual: null,
    diaAtual: null,
    diasSelecionados: {},
    presencasRegistradas: {},
    convocadosIndividuais: {},
    
    // 📈 PROGRESSO
    totalDiasPendentes: 0,
    diasConcluidos: 0,
    
    // 🔧 CONFIGURAÇÕES
    debug: true,
    _processandoSalvamento: false, // Flag para evitar conflitos durante salvamento
    
    /**
     * 🚀 INICIALIZAÇÃO
     */
    init: function() {
        this.log('� [CRITICAL] INÍCIO init()');
        this.log('�🚀 Inicializando PresencaManager...');
        
        // DETECTA CONFLITOS COM SCRIPTS ANTIGOS
        this.detectarConflitos();
        
        this.carregarAlunos();
        this.configurarEventos();
        this.configurarFlatpickr();
        
        // VERIFICA ENVIO AUTOMÁTICO APÓS ERRO
        this.verificarEnvioAutomaticamente();
        
        this.log('✅ PresencaManager inicializado');
        this.log('🔥 [CRITICAL] FIM init()');
    },
    
    /**
     * 🔍 VERIFICAR ENVIO AUTOMATICAMENTE NA INICIALIZAÇÃO
     */
    verificarEnvioAutomaticamente: function() {
        const mensagemErro = document.querySelector('.alert-warning');
        const temErroPresenca = mensagemErro && mensagemErro.textContent.includes('Nenhuma presença foi registrada');
        
        if (temErroPresenca) {
            this.log('🔍 [AUTO-VERIF] Mensagem de erro detectada, verificando estado salvo...');
            
            // Executa a verificação automática após um delay
            setTimeout(() => {
                if (window.verificarEnvioRealizado) {
                    const resultado = window.verificarEnvioRealizado();
                    if (resultado && !resultado.enviadoComSucesso && resultado.estadoRecuperado) {
                        this.log('💡 [AUTO-VERIF] Estado recuperado! Use os calendários para finalizar.');
                        this.mostrarMensagem('📁 Estado anterior recuperado! Seus dados foram restaurados. Finalize o registro novamente.', 'info');
                    }
                }
            }, 2000);
        }
    },
    
    /**
     * 🔍 DETECTAR CONFLITOS COM SCRIPTS ANTIGOS
     */
    detectarConflitos: function() {
        this.log('🔍 [CRITICAL] Detectando possíveis conflitos...');
        
        // Verifica window.PresencaApp
        if (window.PresencaApp && typeof window.PresencaApp.abrirModalPresenca === 'function') {
            this.log('⚠️ [CRITICAL] PresencaApp antigo DETECTADO! Pode causar conflitos!');
            this.log('⚠️ [CRITICAL] PresencaApp.abrirModalPresenca existe:', !!window.PresencaApp.abrirModalPresenca);
        }
        
        // Verifica outros scripts legados
        if (window.salvarPresencaDia) {
            this.log('⚠️ [CRITICAL] Função global salvarPresencaDia() DETECTADA!');
        }
        if (window.marcarTodosPresentes) {
            this.log('⚠️ [CRITICAL] Função global marcarTodosPresentes() DETECTADA!');
        }
        
        // Verifica elementos DOM com event listeners
        const modal = document.getElementById('presencaModal');
        if (modal) {
            // getEventListeners só existe nas DevTools, não no runtime normal
            if (typeof getEventListeners !== 'undefined') {
                const listeners = getEventListeners(modal);
                this.log('🔍 [CRITICAL] Event listeners no modal:', listeners);
            } else {
                this.log('🔍 [CRITICAL] getEventListeners não disponível (normal em produção)');
            }
        }
        
        // Lista todas as funções globais relacionadas a presença
        const globalFunctions = [];
        for (let prop in window) {
            if (typeof window[prop] === 'function' && prop.toLowerCase().includes('presenc')) {
                globalFunctions.push(prop);
            }
        }
        this.log('🔍 [CRITICAL] Funções globais com "presenc":', globalFunctions);
        
        this.log('✅ [CRITICAL] Detecção de conflitos concluída');
    },
    
    /**
     * 📝 LOGGING CENTRALIZADO
     */
    log: function(msg, data = null) {
        if (this.debug) {
            console.log(`[PresencaManager] ${msg}`, data || '');
        }
    },
    
    /**
     * 👥 CARREGAR ALUNOS VIA AJAX
     */
    carregarAlunos: function() {
        const turmaId = this.obterTurmaId();
        if (!turmaId) {
            this.log('❌ Turma ID não encontrado');
            return;
        }
        
        this.log('📡 Carregando alunos da turma:', turmaId);
        
        fetch(`/presencas/ajax/alunos-turma/?turma_id=${turmaId}`)
            .then(response => response.json())
            .then(data => {
                if (data.alunos && data.alunos.length > 0) {
                    this.alunosData = data.alunos;
                    this.log('✅ Alunos carregados:', this.alunosData.length);
                } else {
                    this.log('⚠️ Nenhum aluno encontrado');
                    this.alunosData = [];
                }
            })
            .catch(error => {
                this.log('❌ Erro ao carregar alunos:', error);
                this.alunosData = [];
            });
    },
    
    /**
     * 🔄 GARANTIR QUE ALUNOS SEJAM CARREGADOS (COM PROMISE)
     */
    garantirAlunosCarregados: function() {
        return new Promise((resolve, reject) => {
            // Se já temos alunos carregados, resolve imediatamente
            if (this.alunosData && this.alunosData.length > 0) {
                this.log('✅ Alunos já carregados:', this.alunosData.length);
                resolve(this.alunosData);
                return;
            }
            
            const turmaId = this.obterTurmaId();
            if (!turmaId) {
                this.log('❌ Turma ID não encontrado');
                reject(new Error('Turma ID não encontrado'));
                return;
            }
            
            this.log('📡 Carregando alunos da turma:', turmaId);
            
            fetch(`/presencas/ajax/alunos-turma/?turma_id=${turmaId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.alunos && data.alunos.length > 0) {
                        this.alunosData = data.alunos;
                        this.log('✅ Alunos carregados:', this.alunosData.length);
                        resolve(this.alunosData);
                    } else {
                        this.log('⚠️ Nenhum aluno encontrado na resposta');
                        this.alunosData = [];
                        reject(new Error('Nenhum aluno encontrado para esta turma'));
                    }
                })
                .catch(error => {
                    this.log('❌ Erro ao carregar alunos:', error);
                    this.alunosData = [];
                    reject(error);
                });
        });
    },
    
    /**
     * 🆔 OBTER TURMA ID
     */
    obterTurmaId: function() {
        // Tenta múltiplas fontes para obter o turma ID
        if (typeof window.turmaId !== 'undefined' && window.turmaId) return window.turmaId;
        if (typeof window.PresencaApp !== 'undefined' && window.PresencaApp.turmaIdFinal) {
            return window.PresencaApp.turmaIdFinal;
        }
        
        // Tenta extrair do contexto Django (se disponível)
        const scripts = document.querySelectorAll('script');
        for (let script of scripts) {
            const content = script.textContent;
            const match = content.match(/turmaId\s*[=:]\s*(\d+)/);
            if (match) return parseInt(match[1]);
        }
        
        return null;
    },
    
    /**
     * ⚙️ CONFIGURAR EVENTOS GLOBAIS
     */
    configurarEventos: function() {
        // Modal: fechar com ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isModalAberto()) {
                this.fecharModal();
            }
        });
        
        // Modal: fechar clicando fora
        const modal = document.getElementById('presencaModal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.fecharModal();
                }
            });
        }
        
        // Form: validação antes do submit
        const form = document.getElementById('form-presenca');
        if (form) {
            form.addEventListener('submit', (e) => this.validarSubmit(e));
        }
        
        this.log('✅ Eventos configurados');
    },
    
    /**
     * 📅 CONFIGURAR FLATPICKR PARA TODAS AS ATIVIDADES
     */
    configurarFlatpickr: function() {
        this.log('🔥 [CRITICAL] INÍCIO configurarFlatpickr()');
        
        const inputs = document.querySelectorAll('.dias-datepicker');
        this.log('🔍 [CRITICAL] Inputs encontrados:', inputs.length);
        
        if (inputs.length === 0) {
            this.log('❌ [CRITICAL] NENHUM INPUT .dias-datepicker encontrado!');
            return;
        }
        
        inputs.forEach((input, index) => {
            const atividadeId = input.dataset.atividade;
            const maxDias = parseInt(input.dataset.maxdias) || 0;
            
            this.log(`📅 [${index}] Configurando Flatpickr para atividade ${atividadeId} (max: ${maxDias} dias)`);
            this.log(`📅 [${index}] Input ID: ${input.id}, Classes: ${input.className}`);
            
            // Verifica se o Flatpickr está disponível
            if (typeof flatpickr === 'undefined') {
                this.log('❌ [CRITICAL] Flatpickr não está carregado!');
                return;
            }
            
            try {
                const fpInstance = flatpickr(input, {
                    mode: 'multiple',
                    dateFormat: 'd',
                    minDate: this.obterPrimeiroDiaDoMes(),
                    maxDate: this.obterUltimoDiaDoMes(),
                    locale: 'pt',
                    onChange: (selectedDates, dateStr, instance) => {
                        this.onFlatpickrChange(atividadeId, selectedDates, maxDias, instance);
                    },
                    onDayCreate: (dObj, dStr, fp, dayElem) => {
                        this.onFlatpickrDayCreate(atividadeId, dayElem);
                    },
                    onReady: (selectedDates, dateStr, instance) => {
                        this.onFlatpickrReady(instance);
                    }
                });

                this.log(`✅ [${index}] Flatpickr inicializado para atividade ${atividadeId}`);

                // Torna o ícone clicável
                const icon = input.parentElement.querySelector('.calendar-icon');
                if (icon) {
                    this.log(`🔧 [${index}] Configurando clique no ícone`);
                    icon.addEventListener('click', () => {
                        this.log(`🖱️ [${index}] Ícone clicado - abrindo calendário`);
                        if (input._flatpickr) {
                            input._flatpickr.open();
                        } else {
                            this.log(`❌ [${index}] _flatpickr não encontrado no input!`);
                        }
                    });
                } else {
                    this.log(`⚠️ [${index}] Ícone .calendar-icon não encontrado`);
                }
                
                // Adiciona clique no próprio input também
                input.addEventListener('click', () => {
                    this.log(`🖱️ [${index}] Input clicado - abrindo calendário`);
                    if (input._flatpickr) {
                        input._flatpickr.open();
                    }
                });
                
            } catch (error) {
                this.log(`❌ [${index}] Erro ao inicializar Flatpickr:`, error);
            }
        });
        
        this.log('🔥 [CRITICAL] FIM configurarFlatpickr()');
    },
    
    /**
     * 📅 HANDLER: FLATPICKR CHANGE
     */
    onFlatpickrChange: function(atividadeId, selectedDates, maxDias, instance) {
        this.log(`� INÍCIO onFlatpickrChange() - Atividade: ${atividadeId}, Dias: ${selectedDates.length}`);
        this.log(`�📅 Flatpickr onChange - Atividade: ${atividadeId}, Dias: ${selectedDates.length}`);
        
        // VERIFICAÇÃO DE CHAMADAS DUPLICADAS
        if (this._lastFlatpickrCall) {
            const agora = Date.now();
            const intervalo = agora - this._lastFlatpickrCall.timestamp;
            if (intervalo < 100 && 
                this._lastFlatpickrCall.atividade === atividadeId && 
                this._lastFlatpickrCall.dias === selectedDates.length) {
                this.log(`⚠️ POSSÍVEL CHAMADA DUPLICADA detectada! Intervalo: ${intervalo}ms`);
            }
        }
        this._lastFlatpickrCall = {
            timestamp: Date.now(),
            atividade: atividadeId,
            dias: selectedDates.length
        };
        
        // Validação de limite
        if (selectedDates.length > maxDias) {
            this.log(`❌ Limite excedido: ${selectedDates.length} > ${maxDias}`);
            this.mostrarMensagem(`Você só pode selecionar até ${maxDias} dia(s) para esta atividade.`, 'warning');
            selectedDates.pop();
            instance.setDate(selectedDates, true);
            this.log('🔥 FIM onFlatpickrChange() - LIMITE EXCEDIDO');
            return;
        }
        
        // Atualiza estado interno
        this.diasSelecionados[atividadeId] = selectedDates.map(date => date.getDate()).sort((a, b) => a - b);
        this.log('📊 Estado interno atualizado:', this.diasSelecionados[atividadeId]);
        
        // Atualiza campos de observação
        this.log('📝 Atualizando campos de observação...');
        this.atualizarCamposObservacao(atividadeId, this.diasSelecionados[atividadeId]);
        this.log('✅ Campos de observação atualizados');
        
        // Atualiza indicadores visuais
        this.log('🎨 Atualizando indicadores visuais...');
        this.atualizarIndicadoresVisuais(atividadeId, instance);
        this.log('✅ Indicadores visuais atualizados');
        
        this.log(`✅ Dias selecionados para atividade ${atividadeId}:`, this.diasSelecionados[atividadeId]);
        this.log('🔥 FIM onFlatpickrChange()');
    },
    
    /**
     * 📅 HANDLER: FLATPICKR DAY CREATE
     */
    onFlatpickrDayCreate: function(atividadeId, dayElem) {
        const dia = parseInt(dayElem.textContent);
        
        // Adiciona evento de clique APENAS para dias selecionados
        dayElem.addEventListener('click', (e) => {
            this.log(`🖱️ [CLICK] Clique no dia ${dia} da atividade ${atividadeId}`);
            
            // Verifica se há modal aberto - se sim, evita conflitos
            if (this.isModalAberto()) {
                this.log('⚠️ [CLICK] Modal já está aberto, ignorando clique');
                return;
            }
            
            // Verifica se estamos processando uma operação de salvamento
            if (this._processandoSalvamento) {
                this.log('⚠️ [CLICK] Salvamento em andamento, ignorando clique');
                return;
            }
            
            // Aguarda o Flatpickr processar a seleção
            setTimeout(() => {
                // Dupla verificação de estado para garantir estabilidade
                if (dayElem.classList.contains('selected') && !this.isModalAberto()) {
                    this.log(`✅ [CLICK] Abrindo modal para atividade ${atividadeId}, dia ${dia}`);
                    this.abrirModal(atividadeId, dia);
                } else {
                    this.log(`❌ [CLICK] Dia não selecionado ou modal já aberto - atividade ${atividadeId}, dia ${dia}`);
                }
            }, 200); // Aumentado para 200ms para mais estabilidade
        });
        
        // Adiciona hover para dias selecionados
        dayElem.addEventListener('mouseenter', () => {
            if (dayElem.classList.contains('selected') && !this.isModalAberto()) {
                dayElem.style.cursor = 'pointer';
                dayElem.title = 'Clique para marcar presenças dos alunos';
            } else if (this.isModalAberto()) {
                dayElem.style.cursor = 'not-allowed';
                dayElem.title = 'Feche o modal de presenças primeiro';
            }
        });
        
        // Indica se já há presenças registradas
        if (this.temPresencasRegistradas(atividadeId, dia)) {
            dayElem.classList.add('day-with-presence');
        }
    },
    
    /**
     * 📅 HANDLER: FLATPICKR READY
     */
    onFlatpickrReady: function(instance) {
        // Adiciona botão OK se não existir
        if (!instance.calendarContainer.querySelector('.flatpickr-ok')) {
            const okBtn = document.createElement('button');
            okBtn.type = 'button';
            okBtn.textContent = 'OK';
            okBtn.className = 'flatpickr-ok';
            okBtn.onclick = () => instance.close();
            instance.calendarContainer.appendChild(okBtn);
        }
        
        // Adiciona dica se não existir
        if (!instance.calendarContainer.querySelector('.calendar-hint')) {
            const hint = document.createElement('div');
            hint.className = 'calendar-hint';
            hint.innerHTML = '💡 <strong>Dica:</strong> Após selecionar os dias, clique em cada dia <strong>azul</strong> para marcar as presenças';
            instance.calendarContainer.appendChild(hint);
        }
    },
    
    /**
     * 🗓️ HELPERS DE DATA
     */
    obterPrimeiroDiaDoMes: function() {
        // Extrai do contexto Django se disponível
        if (typeof window.ano !== 'undefined' && typeof window.mes !== 'undefined') {
            return new Date(window.ano, window.mes - 1, 1);
        }
        return new Date(new Date().getFullYear(), new Date().getMonth(), 1);
    },
    
    obterUltimoDiaDoMes: function() {
        // Extrai do contexto Django se disponível
        if (typeof window.ano !== 'undefined' && typeof window.mes !== 'undefined') {
            return new Date(window.ano, window.mes, 0);
        }
        return new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0);
    },
    
    /**
     * 📝 ATUALIZAR CAMPOS DE OBSERVAÇÃO
     */
    atualizarCamposObservacao: function(atividadeId, dias) {
        const obsDiv = document.getElementById(`obs-dias-${atividadeId}`);
        if (!obsDiv) return;
        
        obsDiv.innerHTML = '';
        
        dias.forEach(dia => {
            const input = document.createElement('input');
            input.type = 'text';
            input.name = `obs_${atividadeId}_${dia}`;
            input.className = 'form-control obs-dia';
            input.placeholder = `Obs. do dia ${dia}`;
            input.maxLength = 200;
            obsDiv.appendChild(input);
        });
        
        this.log(`📝 Campos de observação atualizados para atividade ${atividadeId}`);
    },
    
    /**
     * 🎨 ATUALIZAR INDICADORES VISUAIS
     */
    atualizarIndicadoresVisuais: function(atividadeId, instance) {
        const calendar = instance.calendarContainer;
        const dayElements = calendar.querySelectorAll('.flatpickr-day');
        
        dayElements.forEach(dayElem => {
            const dia = parseInt(dayElem.textContent);
            
            // Aplica estilo para dias selecionados
            if (dayElem.classList.contains('selected')) {
                dayElem.classList.add('day-selected');
                dayElem.style.cursor = 'pointer';
            }
            
            // Indica dias com presenças registradas
            if (this.temPresencasRegistradas(atividadeId, dia)) {
                dayElem.classList.add('day-with-presence');
            }
        });
        
        // Mostra/esconde dica
        const hint = calendar.querySelector('.calendar-hint');
        if (hint) {
            const selectedDays = calendar.querySelectorAll('.flatpickr-day.selected');
            hint.style.display = selectedDays.length > 0 ? 'block' : 'none';
        }
    },
    
    /**
     * ✅ VERIFICAR SE TEM PRESENÇAS REGISTRADAS
     */
    temPresencasRegistradas: function(atividadeId, dia) {
        return !!(this.presencasRegistradas[atividadeId] && 
                  this.presencasRegistradas[atividadeId][dia] && 
                  Object.keys(this.presencasRegistradas[atividadeId][dia]).length > 0);
    },
    
    /**
     * 🪟 ABRIR MODAL DE PRESENÇA
     */
    abrirModal: function(atividadeId, dia) {
        this.log(`🪟 Abrindo modal - Atividade: ${atividadeId}, Dia: ${dia}`);
        
        // Verifica se há salvamento em andamento
        if (this._processandoSalvamento) {
            this.log('⚠️ [MODAL] Salvamento em andamento, aguardando conclusão...');
            this.mostrarMensagem('Aguarde a conclusão da operação anterior...', 'warning');
            return;
        }
        
        // Verifica se já há modal aberto
        if (this.isModalAberto()) {
            this.log('⚠️ [MODAL] Modal já está aberto, fechando primeiro...');
            this.fecharModal();
            
            // Aguarda um pouco antes de abrir o novo modal
            setTimeout(() => {
                this.executarAberturaModal(atividadeId, dia);
            }, 300);
            return;
        }
        
        this.executarAberturaModal(atividadeId, dia);
    },
    
    /**
     * 🔄 EXECUTAR ABERTURA DO MODAL (MÉTODO AUXILIAR)
     */
    executarAberturaModal: function(atividadeId, dia) {
        this.log(`🔄 [MODAL] Executando abertura - Atividade: ${atividadeId}, Dia: ${dia}`);
        
        // Define estado atual
        this.atividadeAtual = atividadeId;
        this.diaAtual = dia;
        
        // GARANTE que alunos sejam carregados ANTES de abrir o modal
        this.garantirAlunosCarregados().then(() => {
            // Inicializa presenças como "presente" se não existirem
            this.inicializarPresencasDoDia(atividadeId, dia);
            
            // Atualiza cabeçalho do modal
            this.atualizarCabecalhoModal(atividadeId, dia);
            
            // Preenche lista de alunos
            this.preencherListaAlunos();
            
            // Exibe o modal
            const modal = document.getElementById('presencaModal');
            modal.style.display = 'flex';
            modal.classList.add('show');
            modal.classList.remove('d-none');
            document.body.classList.add('modal-open');
            
            this.log('✅ Modal aberto com sucesso');
        }).catch(error => {
            this.log('❌ Erro ao carregar alunos:', error);
            alert('Erro ao carregar dados dos alunos. Tente novamente.');
        });
    },
    
    /**
     * ➕ INICIALIZAR PRESENÇAS DO DIA
     */
    inicializarPresencasDoDia: function(atividadeId, dia) {
        if (!this.presencasRegistradas[atividadeId]) {
            this.presencasRegistradas[atividadeId] = {};
        }
        
        if (!this.presencasRegistradas[atividadeId][dia]) {
            this.presencasRegistradas[atividadeId][dia] = {};
            
            // Inicializa todos os alunos como presente
            this.alunosData.forEach(aluno => {
                const cpfAluno = aluno.cpf || aluno.id;
                this.presencasRegistradas[atividadeId][dia][cpfAluno] = {
                    presente: true,
                    justificativa: '',
                    convocado: true // 🔧 NOVA FUNCIONALIDADE: Estado de convocação persistido
                };
            });
            
            this.log(`➕ Presenças inicializadas para atividade ${atividadeId}, dia ${dia}`);
        }
        
        // 🔧 NOVA FUNCIONALIDADE: Carrega estado de convocação salvo
        this.carregarEstadoConvocacao(atividadeId, dia);
    },
    
    /**
     * 📥 CARREGAR ESTADO DE CONVOCAÇÃO SALVO
     */
    carregarEstadoConvocacao: function(atividadeId, dia) {
        this.log(`📥 [CONVOCACAO] Carregando estado de convocação para atividade ${atividadeId}, dia ${dia}`);
        
        // Carrega estado salvo nas presenças
        const presencasDoDia = this.presencasRegistradas[atividadeId]?.[dia];
        if (presencasDoDia) {
            Object.keys(presencasDoDia).forEach(cpfAluno => {
                const presenca = presencasDoDia[cpfAluno];
                if (presenca && typeof presenca.convocado !== 'undefined') {
                    this.convocadosIndividuais[cpfAluno] = presenca.convocado;
                    this.log(`📥 [CONVOCACAO] CPF ${cpfAluno}: ${presenca.convocado ? 'Convocado' : 'Não Convocado'}`);
                } else {
                    // Se não tem estado salvo, usa padrão: convocado
                    this.convocadosIndividuais[cpfAluno] = true;
                    this.log(`📥 [CONVOCACAO] CPF ${cpfAluno}: Usando padrão (Convocado)`);
                }
            });
        }
        
        this.log(`📥 [CONVOCACAO] Estado carregado:`, this.convocadosIndividuais);
    },
    
    /**
     * 💾 SALVAR ESTADO DE CONVOCAÇÃO
     */
    salvarEstadoConvocacao: function(cpfAluno) {
        if (!this.atividadeAtual || !this.diaAtual) return;
        
        // Garante que a estrutura existe
        if (!this.presencasRegistradas[this.atividadeAtual]) {
            this.presencasRegistradas[this.atividadeAtual] = {};
        }
        if (!this.presencasRegistradas[this.atividadeAtual][this.diaAtual]) {
            this.presencasRegistradas[this.atividadeAtual][this.diaAtual] = {};
        }
        if (!this.presencasRegistradas[this.atividadeAtual][this.diaAtual][cpfAluno]) {
            this.presencasRegistradas[this.atividadeAtual][this.diaAtual][cpfAluno] = {
                presente: true,
                justificativa: ''
            };
        }
        
        // Salva o estado de convocação
        const estadoConvocacao = this.convocadosIndividuais[cpfAluno];
        this.presencasRegistradas[this.atividadeAtual][this.diaAtual][cpfAluno].convocado = estadoConvocacao;
        
        this.log(`💾 [CONVOCACAO] Estado salvo - CPF: ${cpfAluno}, Convocado: ${estadoConvocacao}`);
        this.log(`💾 [CONVOCACAO] Presença completa:`, this.presencasRegistradas[this.atividadeAtual][this.diaAtual][cpfAluno]);
    },
    
    /**
     * 📋 ATUALIZAR CABEÇALHO DO MODAL
     */
    atualizarCabecalhoModal: function(atividadeId, dia) {
        // Obter nome da atividade
        const nomeAtividade = this.obterNomeAtividade(atividadeId);
        const isConvocada = this.isAtividadeConvocada(atividadeId);
        
        // Formatar data
        const dataFormatada = this.formatarData(dia);
        
        // Título principal
        const modalTitle = document.getElementById('modalTitle');
        if (modalTitle) {
            modalTitle.textContent = `Marcar Presença - (${dataFormatada})`;
        }
        
        // Subtítulo com nome da atividade
        const modalAtividadeNome = document.getElementById('modalAtividadeNome');
        if (modalAtividadeNome) {
            let html = nomeAtividade ? `[${nomeAtividade}]` : '';
            if (isConvocada) {
                html += ' <span style="color:#b8860b; margin-left:8px; font-size:0.9em;">Atividade com convocação</span>';
            }
            modalAtividadeNome.innerHTML = html;
        }
        
        this.log(`📋 Cabeçalho do modal atualizado: ${nomeAtividade} (${dataFormatada})`);
    },
    
    /**
     * 📅 FORMATAR DATA
     */
    formatarData: function(dia) {
        const mes = (typeof window.mes !== 'undefined' ? window.mes : new Date().getMonth() + 1).toString().padStart(2, '0');
        const ano = typeof window.ano !== 'undefined' ? window.ano : new Date().getFullYear();
        return `${dia.toString().padStart(2, '0')}/${mes}/${ano}`;
    },
    
    /**
     * 🏷️ OBTER NOME DA ATIVIDADE
     */
    obterNomeAtividade: function(atividadeId) {
        // Tenta dados do contexto Django primeiro
        if (typeof window.atividadesData !== 'undefined' && window.atividadesData[atividadeId]) {
            return window.atividadesData[atividadeId].nome;
        }
        
        // Tenta PresencaApp para compatibilidade
        if (typeof window.PresencaApp !== 'undefined' && window.PresencaApp.atividadesNomes) {
            return window.PresencaApp.atividadesNomes[atividadeId];
        }
        
        // Tenta extrair do DOM
        const card = document.querySelector(`[data-atividade="${atividadeId}"]`);
        if (card) {
            const nomeElement = card.closest('.atividade-card')?.querySelector('.atividade-nome');
            if (nomeElement) return nomeElement.textContent.trim();
        }
        
        return `Atividade ${atividadeId}`;
    },
    
    /**
     * 🔔 VERIFICAR SE ATIVIDADE É CONVOCADA
     */
    isAtividadeConvocada: function(atividadeId) {
        // Tenta dados do contexto Django primeiro
        if (typeof window.atividadesData !== 'undefined' && window.atividadesData[atividadeId]) {
            return window.atividadesData[atividadeId].convocacao === true;
        }
        
        // Tenta PresencaApp para compatibilidade
        if (typeof window.PresencaApp !== 'undefined' && window.PresencaApp.atividadesConvocadas) {
            return window.PresencaApp.atividadesConvocadas[atividadeId] === true;
        }
        
        return false;
    },
    
    /**
     * 👥 PREENCHER LISTA DE ALUNOS NO MODAL
     */
    preencherListaAlunos: function() {
        this.log('🔥 [RELOAD DEBUG] ================================');
        this.log('🔥 [RELOAD DEBUG] INICIANDO preencherListaAlunos()');
        this.log('🔥 [RELOAD DEBUG] ================================');
        this.log('🔍 [RELOAD DEBUG] Estado de convocação no início:', JSON.stringify(this.convocadosIndividuais, null, 2));
        
        const container = document.getElementById('alunosContainer');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (this.alunosData.length === 0) {
            container.innerHTML = '<div class="alert alert-warning"><i class="fas fa-exclamation-triangle me-2"></i>Nenhum aluno encontrado para esta turma.</div>';
            return;
        }
        
        const isConvocada = this.isAtividadeConvocada(this.atividadeAtual);
        this.log(`🔍 [RELOAD DEBUG] Atividade é convocada: ${isConvocada}`);
        
        this.alunosData.forEach((aluno, index) => {
            const cpfAluno = aluno.cpf || aluno.id;
            const presencaAtual = this.obterPresencaAluno(cpfAluno);
            
            this.log(`🔥 [RELOAD ALUNO ${cpfAluno}] =====================================================`);
            this.log(`👤 [ALUNO] Criando item ${index}: CPF=${cpfAluno}, Nome=${aluno.nome}`);
            this.log(`📊 [ALUNO] Presença atual obtida:`, presencaAtual);
            this.log(`🔍 [ALUNO] Estado de convocação em convocadosIndividuais[${cpfAluno}]:`, this.convocadosIndividuais[cpfAluno]);
            
            // Container do aluno
            const alunoDiv = document.createElement('div');
            alunoDiv.className = 'aluno-presenca-item';
            alunoDiv.setAttribute('data-cpf', cpfAluno); // 🔧 CORREÇÃO: Adiciona atributo data-cpf para identificar o aluno
            
            this.log(`🔧 [ALUNO] Atributo data-cpf="${cpfAluno}" adicionado ao container ${index}`);
            
            // Badge de convocação (se aplicável)
            if (isConvocada) {
                this.log(`🔔 [ALUNO] Criando badge de convocação para CPF ${cpfAluno}...`);
                const badgeConvocado = this.criarBadgeConvocacao(cpfAluno);
                alunoDiv.appendChild(badgeConvocado);
                this.log(`✅ [ALUNO] Badge de convocação criado e adicionado`);
            }
            
            // Nome do aluno
            const nomeDiv = this.criarNomeAluno(aluno);
            alunoDiv.appendChild(nomeDiv);
            
            // Controles de presença
            const controlesDiv = this.criarControlesPresenca(cpfAluno, presencaAtual);
            alunoDiv.appendChild(controlesDiv);
            
            container.appendChild(alunoDiv);
            
            this.log(`🔥 [RELOAD ALUNO ${cpfAluno}] FIM ==========================================`);
        });
        
        this.log('🔥 [RELOAD DEBUG] ================================');
        this.log('🔥 [RELOAD DEBUG] FINALIZANDO preencherListaAlunos()');
        this.log('🔥 [RELOAD DEBUG] Estado de convocação no final:', JSON.stringify(this.convocadosIndividuais, null, 2));
        this.log('🔥 [RELOAD DEBUG] ================================');
        
        this.log(`👥 Lista de alunos preenchida: ${this.alunosData.length} alunos`);
    },
    
    /**
     * 🔔 CRIAR BADGE DE CONVOCAÇÃO
     */
    criarBadgeConvocacao: function(cpfAluno) {
        this.log(`🔥 [BADGE CRIAÇÃO] ================================`);
        this.log(`🔥 [BADGE CRIAÇÃO] Criando badge para CPF: ${cpfAluno}`);
        this.log(`🔍 [BADGE CRIAÇÃO] Estado atual em convocadosIndividuais[${cpfAluno}]:`, this.convocadosIndividuais[cpfAluno]);
        this.log(`🔍 [BADGE CRIAÇÃO] typeof convocadosIndividuais[${cpfAluno}]:`, typeof this.convocadosIndividuais[cpfAluno]);
        
        // � CORREÇÃO CRÍTICA: Só inicializa se o estado for realmente undefined
        if (this.convocadosIndividuais[cpfAluno] === undefined) {
            this.log(`⚠️ [BADGE CRIAÇÃO] Estado realmente undefined - inicializando para true`);
            this.convocadosIndividuais[cpfAluno] = true; // Default: convocado
            this.log(`✅ [BADGE CRIAÇÃO] DEPOIS da inicialização: convocadosIndividuais[${cpfAluno}] = ${this.convocadosIndividuais[cpfAluno]}`);
        } else {
            this.log(`✅ [BADGE CRIAÇÃO] Estado já existe (${this.convocadosIndividuais[cpfAluno]}), mantendo sem alteração`);
        }
        
        const badge = document.createElement('span');
        badge.className = 'badge badge-convocado me-2 badge-uniforme';
        badge.style.cursor = 'pointer';
        badge.style.fontSize = '0.95em';
        badge.style.height = '28px';
        badge.style.minWidth = '90px';
        badge.style.display = 'flex';
        badge.style.alignItems = 'center';
        badge.style.justifyContent = 'center';
        
        this.log(`🎨 [BADGE CRIAÇÃO] Chamando atualizarBadgeConvocacao...`);
        this.atualizarBadgeConvocacao(badge, cpfAluno);
        this.log(`✅ [BADGE CRIAÇÃO] Badge atualizado`);
        
        // Evento de clique para alternar
        badge.addEventListener('click', () => {
            this.log(`🖱️ [BADGE CLICK] Badge clicado para CPF: ${cpfAluno}`);
            this.log(`🔍 [BADGE CLICK] Estado ANTES do toggle: ${this.convocadosIndividuais[cpfAluno]}`);
            this.convocadosIndividuais[cpfAluno] = !this.convocadosIndividuais[cpfAluno];
            this.log(`🔄 [BADGE CLICK] Estado DEPOIS do toggle: ${this.convocadosIndividuais[cpfAluno]}`);
            this.atualizarBadgeConvocacao(badge, cpfAluno);
            
            // 🔧 NOVA FUNCIONALIDADE: Salva estado de convocação imediatamente
            this.salvarEstadoConvocacao(cpfAluno);
        });
        
        this.log(`🔥 [BADGE CRIAÇÃO] Badge criado para CPF ${cpfAluno} com estado final: ${this.convocadosIndividuais[cpfAluno]}`);
        this.log(`🔥 [BADGE CRIAÇÃO] ================================`);
        
        return badge;
    },
    
    /**
     * 🔄 ATUALIZAR BADGE DE CONVOCAÇÃO
     */
    atualizarBadgeConvocacao: function(badge, cpfAluno) {
        const isConvocado = this.convocadosIndividuais[cpfAluno];
        badge.textContent = isConvocado ? 'Convocado' : 'Não Convocado';
        badge.style.backgroundColor = isConvocado ? '#1976d2' : '#bdbdbd';
        badge.style.color = 'white';
        badge.title = isConvocado ? 'Clique para marcar como não convocado' : 'Clique para marcar como convocado';
    },
    
    /**
     * 👤 CRIAR NOME DO ALUNO
     */
    criarNomeAluno: function(aluno) {
        const nomeDiv = document.createElement('div');
        nomeDiv.className = 'aluno-nome';
        nomeDiv.style.fontSize = '0.95em';
        nomeDiv.style.flexGrow = '1';
        nomeDiv.style.maxWidth = '170px';
        nomeDiv.style.overflow = 'hidden';
        nomeDiv.style.textOverflow = 'ellipsis';
        nomeDiv.style.whiteSpace = 'nowrap';
        
        let nomeExibido = aluno.nome;
        if (aluno.nome.length > 25) {
            nomeExibido = aluno.nome.slice(0, 25) + '...';
            nomeDiv.title = aluno.nome;
        }
        
        nomeDiv.textContent = nomeExibido;
        return nomeDiv;
    },
    
    /**
     * 🎛️ CRIAR CONTROLES DE PRESENÇA
     */
    criarControlesPresenca: function(cpfAluno, presencaAtual) {
        const controlesDiv = document.createElement('div');
        controlesDiv.className = 'aluno-controles d-flex align-items-center';
        controlesDiv.style.gap = '8px';
        
        // Botão de presença
        const botaoPresenca = this.criarBotaoPresenca(cpfAluno, presencaAtual);
        controlesDiv.appendChild(botaoPresenca);
        
        // Campo de justificativa
        const justificativaDiv = this.criarCampoJustificativa(cpfAluno, presencaAtual);
        controlesDiv.appendChild(justificativaDiv);
        
        return controlesDiv;
    },
    
    /**
     * 🔘 CRIAR BOTÃO DE PRESENÇA
     */
    criarBotaoPresenca: function(cpfAluno, presencaAtual) {
        const botao = document.createElement('button');
        botao.type = 'button';
        botao.className = 'badge-presenca badge-uniforme';
        botao.style.fontSize = '0.95em';
        botao.style.height = '28px';
        botao.style.minWidth = '80px';
        botao.style.display = 'flex';
        botao.style.alignItems = 'center';
        botao.style.justifyContent = 'center';
        botao.style.border = 'none';
        botao.style.borderRadius = '4px';
        botao.style.cursor = 'pointer';
        botao.style.transition = 'all 0.3s ease';
        
        // Evento de clique
        botao.addEventListener('click', () => this.togglePresenca(cpfAluno));
        
        // Atualiza aparência inicial
        this.atualizarBotaoPresenca(botao, cpfAluno);
        
        return botao;
    },
    
    /**
     * 🔄 ATUALIZAR BOTÃO DE PRESENÇA
     */
    atualizarBotaoPresenca: function(botao, cpfAluno) {
        this.log(`🔘 [BOTAO] Atualizando botão para CPF: ${cpfAluno}`);
        
        const presenca = this.obterPresencaAluno(cpfAluno);
        const isPresente = presenca ? presenca.presente : true;
        
        this.log(`📊 [BOTAO] Estado da presença:`, {cpf: cpfAluno, presente: isPresente, presenca: presenca});
        this.log(`📊 [BOTAO] Estado atual do botão ANTES:`, {
            texto: botao.textContent,
            classes: botao.className,
            backgroundColor: botao.style.backgroundColor,
            color: botao.style.color
        });
        
        // Remove todas as classes de estado anteriores
        botao.classList.remove('badge-presente', 'badge-ausente');
        
        // Atualiza texto e classes
        botao.textContent = isPresente ? 'Presente' : 'Ausente';
        botao.className = `badge-presenca badge-uniforme ${isPresente ? 'badge-presente' : 'badge-ausente'}`;
        
        // FORÇA a aplicação dos estilos inline para garantir que funcionem
        if (isPresente) {
            botao.style.setProperty('background-color', '#198754', 'important');
            botao.style.setProperty('color', 'white', 'important');
            this.log(`🟢 [BOTAO] Aplicando estilo PRESENTE (verde) com !important`);
        } else {
            botao.style.setProperty('background-color', '#dc3545', 'important');
            botao.style.setProperty('color', 'white', 'important');
            this.log(`🔴 [BOTAO] Aplicando estilo AUSENTE (vermelho) com !important`);
        }
        
        // Força um reflow/repaint do elemento
        botao.offsetHeight; // Trigger reflow
        
        this.log(`📊 [BOTAO] Estado atual do botão DEPOIS:`, {
            texto: botao.textContent,
            classes: botao.className,
            backgroundColor: botao.style.backgroundColor,
            color: botao.style.color
        });
        
        this.log(`✅ [BOTAO] Botão atualizado - Texto: "${botao.textContent}", Classes: "${botao.className}"`);
    },
    
    /**
     * 📝 CRIAR CAMPO DE JUSTIFICATIVA
     */
    criarCampoJustificativa: function(cpfAluno, presencaAtual) {
        const div = document.createElement('div');
        div.className = 'justificativa-campo';
        div.style.maxWidth = '180px';
        div.style.minWidth = '120px';
        
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'form-control form-control-sm';
        input.placeholder = 'Justificativa (opcional)';
        input.maxLength = 200;
        input.style.fontSize = '0.95em';
        
        // Valor inicial
        if (presencaAtual && presencaAtual.justificativa) {
            input.value = presencaAtual.justificativa;
        }
        
        // Evento de mudança
        input.addEventListener('change', (e) => {
            this.atualizarJustificativa(cpfAluno, e.target.value);
        });
        
        // Truncamento visual com tooltip
        input.addEventListener('input', (e) => {
            if (e.target.value.length > 25) {
                e.target.title = e.target.value;
            } else {
                e.target.title = '';
            }
        });
        
        div.appendChild(input);
        
        // Controla visibilidade baseado na presença
        const presenca = this.obterPresencaAluno(cpfAluno);
        const isPresente = presenca ? presenca.presente : true;
        div.style.display = isPresente ? 'none' : 'block';
        
        return div;
    },
    
    /**
     * 📊 OBTER PRESENÇA DO ALUNO
     */
    obterPresencaAluno: function(cpfAluno) {
        if (!this.atividadeAtual || !this.diaAtual) return null;
        
        const atividade = this.presencasRegistradas[this.atividadeAtual];
        if (!atividade) return null;
        
        const dia = atividade[this.diaAtual];
        if (!dia) return null;
        
        return dia[cpfAluno] || null;
    },
    
    /**
     * 🔄 TOGGLE PRESENÇA DO ALUNO
     */
    togglePresenca: function(cpfAluno) {
        if (!this.atividadeAtual || !this.diaAtual) return;
        
        // Garante estrutura
        if (!this.presencasRegistradas[this.atividadeAtual]) {
            this.presencasRegistradas[this.atividadeAtual] = {};
        }
        if (!this.presencasRegistradas[this.atividadeAtual][this.diaAtual]) {
            this.presencasRegistradas[this.atividadeAtual][this.diaAtual] = {};
        }
        
        const atual = this.presencasRegistradas[this.atividadeAtual][this.diaAtual][cpfAluno];
        const novoPresente = atual ? !atual.presente : true; // 🔧 CORREÇÃO: Se não existe, assume PRESENTE por padrão
        
        // Atualiza estado preservando convocação
        this.presencasRegistradas[this.atividadeAtual][this.diaAtual][cpfAluno] = {
            presente: novoPresente,
            justificativa: atual ? atual.justificativa : '',
            convocado: atual && atual.convocado !== undefined ? atual.convocado : (this.convocadosIndividuais[cpfAluno] !== undefined ? this.convocadosIndividuais[cpfAluno] : true) // 🔧 CORREÇÃO: Preserva estado atual
        };
        
        // Atualiza interface
        this.atualizarInterfaceAluno(cpfAluno);
        
        this.log(`🔄 Toggle presença - Aluno: ${cpfAluno}, Presente: ${novoPresente}`);
    },
    
    /**
     * 🔄 ATUALIZAR INTERFACE DO ALUNO
     */
    atualizarInterfaceAluno: function(cpfAluno) {
        this.log(`🔄 [INTERFACE] Atualizando interface do aluno: ${cpfAluno}`);
        
        // 🔍 DEBUG DETALHADO: Lista todos os elementos disponíveis
        const todosAlunos = document.querySelectorAll('.aluno-presenca-item');
        this.log(`🔍 [INTERFACE] Total de containers .aluno-presenca-item encontrados: ${todosAlunos.length}`);
        
        todosAlunos.forEach((div, idx) => {
            const dataCpf = div.getAttribute('data-cpf');
            this.log(`🔍 [INTERFACE] Container ${idx}: data-cpf="${dataCpf}"`);
        });
        
        // Busca o container do aluno usando múltiplas estratégias
        let alunoDiv = document.querySelector(`[data-cpf="${cpfAluno}"]`);
        
        if (!alunoDiv) {
            this.log(`❌ [INTERFACE] Busca por data-cpf="${cpfAluno}" falhou, tentando busca alternativa...`);
            
            // Estratégia alternativa: busca por posição na lista (se só há 1 aluno)
            if (todosAlunos.length === 1) {
                alunoDiv = todosAlunos[0];
                this.log(`🔄 [INTERFACE] Usando o único container disponível como fallback`);
                // Adiciona o data-cpf que estava faltando
                alunoDiv.setAttribute('data-cpf', cpfAluno);
                this.log(`� [INTERFACE] Adicionado data-cpf="${cpfAluno}" ao container`);
            } else {
                this.log(`❌ [INTERFACE] Múltiplos containers encontrados, não é possível determinar qual usar`);
                return;
            }
        }
        
        this.log(`✅ [INTERFACE] Container encontrado para CPF: ${cpfAluno}`);
        
        // Atualiza botão de presença
        const botao = alunoDiv.querySelector('.badge-presenca');
        if (botao) {
            this.log(`🔘 [INTERFACE] Botão encontrado, atualizando...`);
            this.atualizarBotaoPresenca(botao, cpfAluno);
            this.log(`✅ [INTERFACE] Botão de presença atualizado`);
        } else {
            this.log(`❌ [INTERFACE] Botão de presença não encontrado no container`);
            // Lista todos os elementos filhos para debug
            const filhos = alunoDiv.querySelectorAll('*');
            this.log(`🔍 [INTERFACE] Elementos filhos no container:`, Array.from(filhos).map(el => el.className));
        }
        
        // Atualiza visibilidade da justificativa
        const justificativaDiv = alunoDiv.querySelector('.justificativa-campo');
        if (justificativaDiv) {
            const presenca = this.obterPresencaAluno(cpfAluno);
            const isPresente = presenca ? presenca.presente : true;
            justificativaDiv.style.display = isPresente ? 'none' : 'block';
            this.log(`📝 [INTERFACE] Justificativa ${isPresente ? 'oculta' : 'exibida'}`);
        } else {
            this.log(`⚠️ [INTERFACE] Campo de justificativa não encontrado`);
        }
        
        this.log(`✅ [INTERFACE] Interface do aluno ${cpfAluno} atualizada com sucesso`);
    },
    
    /**
     * ✏️ ATUALIZAR JUSTIFICATIVA
     */
    atualizarJustificativa: function(cpfAluno, valor) {
        if (!this.atividadeAtual || !this.diaAtual) return;
        
        const presenca = this.presencasRegistradas[this.atividadeAtual]?.[this.diaAtual]?.[cpfAluno];
        if (presenca) {
            presenca.justificativa = valor;
            // 🔧 Garante que o estado de convocação seja preservado
            if (typeof presenca.convocado === 'undefined') {
                presenca.convocado = this.convocadosIndividuais[cpfAluno] || true;
            }
            this.log(`✏️ Justificativa atualizada - Aluno: ${cpfAluno}, Valor: "${valor}"`);
        }
    },
    
    /**
     * ⚡ MARCAR TODOS PRESENTES (MODO RÁPIDO)
     */
    marcarTodosPresentes: function() {
        if (!this.atividadeAtual || !this.diaAtual) return;
        
        this.log('🔥 [DEBUG CRÍTICO] ================================');
        this.log('🔥 [DEBUG CRÍTICO] INICIANDO TODOS PRESENTES');
        this.log('🔥 [DEBUG CRÍTICO] ================================');
        this.log('⚡ [MODO RAPIDO] Estado COMPLETO de convocação ANTES:', JSON.stringify(this.convocadosIndividuais, null, 2));
        this.log('⚡ [MODO RAPIDO] Quantidade de alunos a processar:', this.alunosData.length);
        
        // 🔍 DIAGNÓSTICO: Verifica estado inicial de cada badge no DOM
        this.alunosData.forEach(aluno => {
            const cpfAluno = aluno.cpf || aluno.id;
            const badgeElement = document.querySelector(`[data-cpf="${cpfAluno}"] .badge-convocado`);
            if (badgeElement) {
                this.log(`🔍 [DOM ANTES] CPF ${cpfAluno}: Badge DOM texto = "${badgeElement.textContent}" | cor = ${badgeElement.style.backgroundColor}`);
            }
        });
        
        this.alunosData.forEach(aluno => {
            const cpfAluno = aluno.cpf || aluno.id;
            
            this.log(`🔥 [ALUNO ${cpfAluno}] =====================================================`);
            
            // Estado ANTES da operação
            const estadoConvocacaoAtual = this.convocadosIndividuais[cpfAluno];
            const presencaAnterior = this.presencasRegistradas[this.atividadeAtual]?.[this.diaAtual]?.[cpfAluno];
            
            this.log(`🔍 [ANTES] CPF: ${cpfAluno}`);
            this.log(`🔍 [ANTES] convocadosIndividuais[${cpfAluno}] =`, estadoConvocacaoAtual);
            this.log(`🔍 [ANTES] typeof convocadosIndividuais[${cpfAluno}] =`, typeof estadoConvocacaoAtual);
            this.log(`🔍 [ANTES] convocadosIndividuais[${cpfAluno}] !== undefined =`, estadoConvocacaoAtual !== undefined);
            this.log(`🔍 [ANTES] Presença anterior:`, presencaAnterior);
            
            // Atualiza estado
            if (!this.presencasRegistradas[this.atividadeAtual]) {
                this.presencasRegistradas[this.atividadeAtual] = {};
            }
            if (!this.presencasRegistradas[this.atividadeAtual][this.diaAtual]) {
                this.presencasRegistradas[this.atividadeAtual][this.diaAtual] = {};
            }
            
            // 🔧 CORREÇÃO CRÍTICA: Usa a lógica mais rigorosa
            let estadoConvocacaoFinal;
            if (estadoConvocacaoAtual !== undefined) {
                estadoConvocacaoFinal = estadoConvocacaoAtual;
                this.log(`✅ [LÓGICA] Usando estado atual: ${estadoConvocacaoFinal}`);
            } else {
                estadoConvocacaoFinal = true;
                this.log(`⚠️ [LÓGICA] Estado undefined, usando padrão: ${estadoConvocacaoFinal}`);
            }
            
            this.log(`🎯 [DECISÃO] Estado final escolhido: ${estadoConvocacaoFinal}`);
            
            this.presencasRegistradas[this.atividadeAtual][this.diaAtual][cpfAluno] = {
                presente: true,
                justificativa: '',
                convocado: estadoConvocacaoFinal
            };
            
            this.log(`💾 [SALVO] Dados salvos:`, this.presencasRegistradas[this.atividadeAtual][this.diaAtual][cpfAluno]);
            this.log(`🔥 [ALUNO ${cpfAluno}] FIM ==========================================`);
        });
        
        // Recarrega a lista para refletir mudanças
        this.log('🔄 [RELOAD] Chamando preencherListaAlunos()...');
        this.preencherListaAlunos();
        this.log('✅ [RELOAD] preencherListaAlunos() concluído');
        
        // 🔍 DIAGNÓSTICO: Verifica estado final de cada badge no DOM
        this.log('🔍 [DOM DEPOIS] Verificando badges após reload:');
        this.alunosData.forEach(aluno => {
            const cpfAluno = aluno.cpf || aluno.id;
            const badgeElement = document.querySelector(`[data-cpf="${cpfAluno}"] .badge-convocado`);
            if (badgeElement) {
                this.log(`🔍 [DOM DEPOIS] CPF ${cpfAluno}: Badge DOM texto = "${badgeElement.textContent}" | cor = ${badgeElement.style.backgroundColor}`);
            }
        });
        
        this.log('🔥 [DEBUG CRÍTICO] ================================');
        this.log('🔥 [DEBUG CRÍTICO] FINALIZANDO TODOS PRESENTES');
        this.log('🔥 [DEBUG CRÍTICO] Estado FINAL de convocação:', JSON.stringify(this.convocadosIndividuais, null, 2));
        this.log('🔥 [DEBUG CRÍTICO] ================================');
        
        this.log('⚡ Todos os alunos marcados como presentes');
        this.mostrarMensagem('Todos os alunos foram marcados como presentes!', 'success');
    },
    
    /**
     * ⚡ MARCAR TODOS AUSENTES (MODO RÁPIDO)
     */
    marcarTodosAusentes: function() {
        if (!this.atividadeAtual || !this.diaAtual) return;
        
        this.log('🔥 [DEBUG CRÍTICO] ================================');
        this.log('🔥 [DEBUG CRÍTICO] INICIANDO TODOS AUSENTES');
        this.log('🔥 [DEBUG CRÍTICO] ================================');
        this.log('⚡ [MODO RAPIDO] Estado COMPLETO de convocação ANTES:', JSON.stringify(this.convocadosIndividuais, null, 2));
        
        this.alunosData.forEach(aluno => {
            const cpfAluno = aluno.cpf || aluno.id;
            
            this.log(`🔥 [ALUNO ${cpfAluno}] =====================================================`);
            
            // Estado ANTES da operação
            const estadoConvocacaoAtual = this.convocadosIndividuais[cpfAluno];
            const presencaAnterior = this.presencasRegistradas[this.atividadeAtual]?.[this.diaAtual]?.[cpfAluno];
            
            this.log(`🔍 [ANTES] CPF: ${cpfAluno}`);
            this.log(`🔍 [ANTES] convocadosIndividuais[${cpfAluno}] =`, estadoConvocacaoAtual);
            this.log(`🔍 [ANTES] typeof convocadosIndividuais[${cpfAluno}] =`, typeof estadoConvocacaoAtual);
            this.log(`🔍 [ANTES] convocadosIndividuais[${cpfAluno}] !== undefined =`, estadoConvocacaoAtual !== undefined);
            this.log(`🔍 [ANTES] Presença anterior:`, presencaAnterior);
            
            // Atualiza estado
            if (!this.presencasRegistradas[this.atividadeAtual]) {
                this.presencasRegistradas[this.atividadeAtual] = {};
            }
            if (!this.presencasRegistradas[this.atividadeAtual][this.diaAtual]) {
                this.presencasRegistradas[this.atividadeAtual][this.diaAtual] = {};
            }
            
            // 🔧 CORREÇÃO CRÍTICA: Usa a lógica mais rigorosa
            let estadoConvocacaoFinal;
            if (estadoConvocacaoAtual !== undefined) {
                estadoConvocacaoFinal = estadoConvocacaoAtual;
                this.log(`✅ [LÓGICA] Usando estado atual: ${estadoConvocacaoFinal}`);
            } else {
                estadoConvocacaoFinal = true;
                this.log(`⚠️ [LÓGICA] Estado undefined, usando padrão: ${estadoConvocacaoFinal}`);
            }
            
            this.log(`🎯 [DECISÃO] Estado final escolhido: ${estadoConvocacaoFinal}`);
            
            this.presencasRegistradas[this.atividadeAtual][this.diaAtual][cpfAluno] = {
                presente: false,
                justificativa: '',
                convocado: estadoConvocacaoFinal
            };
            
            this.log(`💾 [SALVO] Dados salvos:`, this.presencasRegistradas[this.atividadeAtual][this.diaAtual][cpfAluno]);
            this.log(`🔥 [ALUNO ${cpfAluno}] FIM ==========================================`);
        });
        
        // Recarrega a lista para refletir mudanças
        this.log('🔄 [RELOAD] Chamando preencherListaAlunos()...');
        this.preencherListaAlunos();
        this.log('✅ [RELOAD] preencherListaAlunos() concluído');
        
        this.log('🔥 [DEBUG CRÍTICO] ================================');
        this.log('🔥 [DEBUG CRÍTICO] FINALIZANDO TODOS AUSENTES');
        this.log('🔥 [DEBUG CRÍTICO] Estado FINAL de convocação:', JSON.stringify(this.convocadosIndividuais, null, 2));
        this.log('🔥 [DEBUG CRÍTICO] ================================');
        
        this.log('⚡ Todos os alunos marcados como ausentes');
        this.mostrarMensagem('Todos os alunos foram marcados como ausentes!', 'warning');
    },
    
    /**
     * 💾 SALVAR PRESENÇAS DO DIA ATUAL
     */
    salvarDiaAtual: function() {
        // 🎯 LOG DE DEBUG PARA CLIQUE NO BOTÃO
        console.log('🔥 [DEBUG-CLIQUE] ========================================');
        console.log('🔥 [DEBUG-CLIQUE] BOTÃO "SALVAR PRESENÇAS" FOI CLICADO!');
        console.log('🔥 [DEBUG-CLIQUE] Timestamp:', new Date().toLocaleString());
        console.log('🔥 [DEBUG-CLIQUE] Função salvarDiaAtual() chamada');
        console.log('🔥 [DEBUG-CLIQUE] ========================================');
        
        this.log('🔥 INÍCIO salvarDiaAtual()');
        
        if (!this.atividadeAtual || !this.diaAtual) {
            this.log('❌ Atividade ou dia não definidos - SAINDO', {atividade: this.atividadeAtual, dia: this.diaAtual});
            this.mostrarMensagem('Erro: dia ou atividade não definidos', 'danger');
            return;
        }
        
        // 🔒 BLOQUEIA OUTRAS OPERAÇÕES DURANTE O SALVAMENTO
        this._processandoSalvamento = true;
        this.log('🔒 [LOCK] Salvamento iniciado - bloqueando outras operações');
        
        this.log(`💾 Salvando presenças - Atividade: ${this.atividadeAtual}, Dia: ${this.diaAtual}`);
        
        // Atualiza o Flatpickr para garantir que o dia esteja selecionado
        this.log('🔧 Chamando atualizarFlatpickr()...');
        this.atualizarFlatpickr();
        this.log('✅ atualizarFlatpickr() concluído');
        
        // Fecha o modal automaticamente após salvar
        this.log('📨 Exibindo mensagem de sucesso...');
        this.mostrarMensagem(`Presenças do dia ${this.diaAtual} registradas com sucesso!`, 'success');
        this.log('✅ Mensagem exibida');
        
        // Atualiza indicadores visuais no calendário
        this.log('🎨 Marcando dia como processado...');
        this.marcarDiaComoProcessado(this.atividadeAtual, this.diaAtual);
        this.log('✅ Dia marcado visualmente');
        
        this.log('✅ Presenças salvas com sucesso');
        
        // 🎯 PRESERVA ID DA ATIVIDADE E DIA ANTES DE QUALQUER OPERAÇÃO
        this.log('🔍 [UX] DEBUG CRÍTICO - Estado ANTES da preservação:');
        this.log('🔍 [UX] this.atividadeAtual (antes):', this.atividadeAtual);
        this.log('🔍 [UX] this.diaAtual (antes):', this.diaAtual);
        this.log('🔍 [UX] typeof this.atividadeAtual:', typeof this.atividadeAtual);
        
        const atividadeParaReabrir = this.atividadeAtual; // Salva ANTES de qualquer operação
        const diaProcessado = this.diaAtual; // Também preserva o dia
        
        this.log('💾 [UX] ID da atividade preservado para reabertura:', atividadeParaReabrir);
        this.log('💾 [UX] Dia processado preservado:', diaProcessado);
        this.log('💾 [UX] typeof atividadeParaReabrir:', typeof atividadeParaReabrir);
        
        // VALIDAÇÃO CRÍTICA DOS DADOS
        if (!atividadeParaReabrir) {
            this.log('❌ [UX] ERRO CRÍTICO: atividadeAtual está undefined/null antes de preservar!');
            this.log('❌ [UX] this.atividadeAtual:', this.atividadeAtual);
            this.log('❌ [UX] this.diaAtual:', this.diaAtual);
            this.log('❌ [UX] Tentando recuperar de outras fontes...');
            
            // Tenta recuperar do DOM ou contexto
            const modal = document.getElementById('presencaModal');
            if (modal) {
                const modalTitle = modal.querySelector('#modalTitle');
                const modalAtividade = modal.querySelector('#modalAtividadeNome');
                this.log('🔍 [UX] Modal title:', modalTitle?.textContent);
                this.log('🔍 [UX] Modal atividade:', modalAtividade?.textContent);
            }
            
            // Tenta extrair de qualquer input ativo
            const inputsAtivos = document.querySelectorAll('.dias-datepicker');
            inputsAtivos.forEach((input, idx) => {
                if (input._flatpickr && input._flatpickr.isOpen) {
                    this.log(`🔍 [UX] Input ativo ${idx}:`, input.dataset.atividade);
                }
            });
        } else {
            this.log('✅ [UX] Dados preservados com sucesso!');
        }
        
        // Fecha o modal IMEDIATAMENTE após 1 segundo
        this.log('⏰ [CRITICAL] Configurando setTimeout para fechar modal em 1s...');
        const timeoutId = setTimeout(() => {
            this.log('🚪 [CRITICAL] EXECUTANDO setTimeout - Fechando modal FORÇADAMENTE...');
            this.log('🎯 [UX] Validando dados preservados dentro do setTimeout:');
            this.log('🎯 [UX] atividadeParaReabrir:', atividadeParaReabrir);
            this.log('🎯 [UX] diaProcessado:', diaProcessado);
            
            // FORÇA o fechamento imediato usando ESTRATÉGIAS EXTREMAS
            const modal = document.getElementById('presencaModal');
            if (modal) {
                modal.style.setProperty('display', 'none', 'important');
                modal.style.setProperty('visibility', 'hidden', 'important');
                modal.style.setProperty('opacity', '0', 'important');
                modal.style.setProperty('z-index', '-99999', 'important');
                modal.style.setProperty('position', 'fixed', 'important');
                modal.style.setProperty('top', '-9999px', 'important');
                modal.style.setProperty('left', '-9999px', 'important');
                modal.classList.remove('show');
                modal.classList.add('d-none');
                modal.removeAttribute('style'); // Remove todos os estilos inline
                modal.style.display = 'none'; // Reaplica sem !important
                document.body.classList.remove('modal-open');
                
                // Remove qualquer backdrop
                const backdrops = document.querySelectorAll('.modal-backdrop, .presenca-modal-backdrop');
                backdrops.forEach(backdrop => backdrop.remove());
            }
            
            // Chama também o método normal (que vai limpar this.atividadeAtual)
            this.fecharModal();
            
            this.log('✅ [CRITICAL] Modal fechado via setTimeout FORÇADO');
            
            // 🎯 NOVA FUNCIONALIDADE: Reabre o calendário automaticamente após fechar modal
            this.log('📅 [UX] Reabrindo calendário para facilitar seleção do próximo dia...');
            this.log('🎯 [UX] Usando atividade preservada (final):', atividadeParaReabrir);
            
            // Valida novamente antes de chamar
            if (atividadeParaReabrir) {
                setTimeout(() => {
                    this.reabrirCalendarioAutomaticamente(atividadeParaReabrir);
                    
                    // 🔓 LIBERA OPERAÇÕES APÓS REABERTURA DO CALENDÁRIO
                    setTimeout(() => {
                        this._processandoSalvamento = false;
                        this.log('🔓 [UNLOCK] Salvamento concluído - liberando outras operações');
                    }, 500); // Aguarda 500ms para estabilizar
                    
                }, 300); // Pequeno delay para garantir que o modal foi fechado
            } else {
                this.log('❌ [UX] ERRO CRÍTICO: atividadeParaReabrir está undefined no momento da reabertura!');
                // 🔓 LIBERA MESMO EM CASO DE ERRO
                this._processandoSalvamento = false;
                this.log('🔓 [UNLOCK] Salvamento concluído (com erro) - liberando outras operações');
            }
            
        }, 1000);
        
        this.log('⏰ [CRITICAL] setTimeout configurado com ID:', timeoutId);
        this.log('🔥 FIM salvarDiaAtual()');
    },
    
    /**
     * 📅 REABRIR CALENDÁRIO AUTOMATICAMENTE (UX MELHORADA)
     */
    reabrirCalendarioAutomaticamente: function(atividadeId) {
        this.log('🎯 [UX] INÍCIO reabrirCalendarioAutomaticamente()');
        this.log('🎯 [UX] Parâmetro atividadeId recebido:', atividadeId);
        this.log('🎯 [UX] Tipo do parâmetro:', typeof atividadeId);
        
        if (!atividadeId) {
            this.log('❌ [UX] ID da atividade não fornecido, tentando usar this.atividadeAtual...');
            atividadeId = this.atividadeAtual;
            this.log('🔄 [UX] Valor de this.atividadeAtual:', atividadeId);
        }
        
        if (!atividadeId) {
            this.log('❌ [UX] ID da atividade ainda não disponível - ABORTANDO');
            return;
        }
        
        this.log('✅ [UX] Processando com atividadeId:', atividadeId);
        
        // Busca o input do Flatpickr para esta atividade
        const inputId = `dias-atividade-${atividadeId}`;
        this.log('🔍 [UX] Procurando input com ID:', inputId);
        const input = document.getElementById(inputId);
        
        if (!input) {
            this.log('❌ [UX] Input não encontrado para ID:', inputId);
            // Lista todos os inputs disponíveis para debug
            const todosInputs = document.querySelectorAll('[id^="dias-atividade-"]');
            this.log('🔍 [UX] Inputs disponíveis:', Array.from(todosInputs).map(inp => inp.id));
            return;
        }
        
        if (!input._flatpickr) {
            this.log('❌ [UX] Flatpickr não encontrado no input:', inputId);
            return;
        }
        
        this.log('📅 [UX] Reabrindo calendário da atividade:', atividadeId);
        
        try {
            // Primeiro, verifica se o calendário não está já aberto
            if (input._flatpickr.isOpen) {
                this.log('⚠️ [UX] Calendário já está aberto, fechando primeiro...');
                input._flatpickr.close();
                
                // Aguarda um pouco antes de reabrir
                setTimeout(() => {
                    this.executarReaberturaCalendario(input, atividadeId);
                }, 200);
            } else {
                this.executarReaberturaCalendario(input, atividadeId);
            }
            
        } catch (error) {
            this.log('❌ [UX] Erro ao reabrir calendário:', error);
        }
        
        this.log('🎯 [UX] FIM reabrirCalendarioAutomaticamente()');
    },
    
    /**
     * 🔄 EXECUTAR REABERTURA DO CALENDÁRIO (MÉTODO AUXILIAR)
     */
    executarReaberturaCalendario: function(input, atividadeId) {
        this.log('🔄 [UX] Executando reabertura do calendário...');
        
        // Abre o calendário
        input._flatpickr.open();
        this.log('✅ [UX] Calendário reaberto com sucesso');
        
        // Foca no input para melhor UX
        input.focus();
        
        // Scroll suave até o card da atividade para garantir visibilidade
        const atividadeCard = input.closest('.atividade-card');
        if (atividadeCard) {
            atividadeCard.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
            this.log('📍 [UX] Scroll para o card da atividade realizado');
        }
        
        // Adiciona uma dica visual temporária no calendário
        setTimeout(() => {
            this.adicionarDicaVisualCalendario(input._flatpickr);
        }, 400); // Aumentado para dar tempo de estabilizar
        
        // Adiciona indicador visual de que o calendário está estabilizado
        setTimeout(() => {
            if (input._flatpickr && input._flatpickr.calendarContainer) {
                const calendar = input._flatpickr.calendarContainer;
                calendar.style.transition = 'all 0.3s ease';
                calendar.style.transform = 'scale(1.02)';
                
                setTimeout(() => {
                    calendar.style.transform = 'scale(1)';
                    this.log('🎯 [UX] Calendário estabilizado e pronto para uso');
                }, 200);
            }
        }, 600);
    },
    
    /**
     * 💡 ADICIONAR DICA VISUAL NO CALENDÁRIO
     */
    adicionarDicaVisualCalendario: function(flatpickrInstance) {
        if (!flatpickrInstance || !flatpickrInstance.calendarContainer) return;
        
        const calendar = flatpickrInstance.calendarContainer;
        
        // Remove dica anterior se existir
        const dicaAnterior = calendar.querySelector('.dica-proximo-dia');
        if (dicaAnterior) {
            dicaAnterior.remove();
        }
        
        // Cria nova dica
        const dica = document.createElement('div');
        dica.className = 'dica-proximo-dia';
        
        // Verifica se há dias pendentes para personalizar a mensagem
        const diasPendentes = this.verificarDiasPendentes(flatpickrInstance);
        let mensagem = '';
        
        if (diasPendentes.length > 0) {
            mensagem = `🎯 <strong>Próximo passo:</strong> Clique no dia <strong style="color:#1976d2;">${diasPendentes[0]}</strong> para marcar presenças ou selecione novos dias`;
        } else {
            mensagem = '🎯 <strong>Próximo passo:</strong> Clique nos dias <strong style="color:#1976d2;">azuis selecionados</strong> para marcar presenças ou selecione novos dias';
        }
        
        dica.innerHTML = mensagem;
        dica.style.cssText = `
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border: 2px solid #1976d2;
            border-radius: 8px;
            padding: 12px;
            margin: 10px 0;
            font-size: 0.9em;
            text-align: center;
            box-shadow: 0 2px 8px rgba(25, 118, 210, 0.2);
            animation: dica-pulse 2s ease-in-out;
        `;
        
        // Adiciona animação CSS
        if (!document.querySelector('#dica-animation-style')) {
            const style = document.createElement('style');
            style.id = 'dica-animation-style';
            style.textContent = `
                @keyframes dica-pulse {
                    0% { transform: scale(0.95); opacity: 0.7; }
                    50% { transform: scale(1.02); opacity: 1; }
                    100% { transform: scale(1); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
        
        // Insere a dica no calendário
        calendar.appendChild(dica);
        
        // Remove a dica após 8 segundos
        setTimeout(() => {
            if (dica.parentNode) {
                dica.style.opacity = '0';
                dica.style.transition = 'opacity 0.5s ease-out';
                setTimeout(() => dica.remove(), 500);
            }
        }, 8000);
        
        this.log('💡 [UX] Dica visual adicionada ao calendário');
    },
    
    /**
     * 📋 VERIFICAR DIAS PENDENTES (SELECIONADOS MAS SEM PRESENÇAS)
     */
    verificarDiasPendentes: function(flatpickrInstance) {
        if (!flatpickrInstance || !flatpickrInstance.selectedDates) return [];
        
        const diasSelecionados = flatpickrInstance.selectedDates.map(date => date.getDate());
        const diasPendentes = [];
        
        // Extrai ID da atividade do input
        const input = flatpickrInstance.input;
        const atividadeId = input?.dataset?.atividade;
        
        if (!atividadeId) return diasSelecionados;
        
        // Verifica quais dias selecionados ainda não têm presenças registradas
        diasSelecionados.forEach(dia => {
            if (!this.temPresencasRegistradas(atividadeId, dia)) {
                diasPendentes.push(dia);
            }
        });
        
        this.log('📋 [UX] Dias pendentes encontrados:', diasPendentes);
        return diasPendentes.sort((a, b) => a - b);
    },
    
    /**
     * 📅 ATUALIZAR FLATPICKR APÓS SALVAR
     */
    atualizarFlatpickr: function() {
        const input = document.getElementById(`dias-atividade-${this.atividadeAtual}`);
        if (!input || !input._flatpickr) return;
        
        const flatpickr = input._flatpickr;
        let datas = flatpickr.selectedDates || [];
        const diaSalvo = parseInt(this.diaAtual);
        
        // Verifica se o dia já está selecionado
        const jaExiste = datas.some(d => d.getDate() === diaSalvo);
        
        if (!jaExiste) {
            // Adiciona o dia à seleção
            datas.push(new Date(
                flatpickr.currentYear, 
                flatpickr.currentMonth, 
                diaSalvo
            ));
            
            // Ordena os dias
            datas.sort((a, b) => a.getDate() - b.getDate());
            
            // Atualiza o Flatpickr
            flatpickr.setDate(datas, true);
            
            this.log(`📅 Flatpickr atualizado - Dia ${diaSalvo} adicionado`);
        }
    },
    
    /**
     * ✅ MARCAR DIA COMO PROCESSADO VISUALMENTE
     */
    marcarDiaComoProcessado: function(atividadeId, dia) {
        const input = document.getElementById(`dias-atividade-${atividadeId}`);
        if (!input || !input._flatpickr) return;
        
        const calendar = input._flatpickr.calendarContainer;
        const dayElements = calendar.querySelectorAll('.flatpickr-day');
        
        dayElements.forEach(dayElem => {
            if (parseInt(dayElem.textContent) === parseInt(dia)) {
                dayElem.classList.add('day-with-presence');
                this.log(`✅ Dia ${dia} marcado visualmente como processado`);
            }
        });
    },
    
    /**
     * 🚪 FECHAR MODAL
     */
    fecharModal: function() {
        this.log('� INÍCIO fecharModal()');
        this.log('�🚪 Fechando modal...');
        
        const modal = document.getElementById('presencaModal');
        if (modal) {
            this.log('🔍 Modal encontrado, alterando display...');
            modal.style.display = 'none';
            modal.classList.remove('show');
            document.body.classList.remove('modal-open');
            this.log('✅ Estilos do modal alterados');
        } else {
            this.log('❌ Modal NÃO encontrado no DOM!');
        }
        
        // Limpa estado atual
        this.log('🧹 Limpando estado atual...');
        const estadoAnterior = {atividade: this.atividadeAtual, dia: this.diaAtual};
        this.atividadeAtual = null;
        this.diaAtual = null;
        this.log('🧹 Estado limpo:', estadoAnterior);
        
        this.log('✅ Modal fechado com sucesso');
        this.log('🔥 FIM fecharModal()');
    },
    
    /**
     * ❓ VERIFICAR SE MODAL ESTÁ ABERTO
     */
    isModalAberto: function() {
        const modal = document.getElementById('presencaModal');
        if (!modal) return false;
        
        // Múltiplas verificações para garantir precisão
        const displayCheck = modal.style.display === 'flex';
        const classCheck = modal.classList.contains('show') && !modal.classList.contains('d-none');
        const visibilityCheck = modal.style.visibility !== 'hidden';
        const opacityCheck = modal.style.opacity !== '0';
        
        const isOpen = displayCheck && classCheck && visibilityCheck && opacityCheck;
        
        this.log(`❓ [MODAL] Verificação de estado:`, {
            display: modal.style.display,
            classes: modal.className,
            visibility: modal.style.visibility,
            opacity: modal.style.opacity,
            isOpen: isOpen
        });
        
        return isOpen;
    },
    
    /**
     * 📨 MOSTRAR MENSAGEM
     */
    mostrarMensagem: function(texto, tipo = 'info') {
        const mensagemDiv = document.getElementById('mensagem-ajax');
        if (!mensagemDiv) return;
        
        mensagemDiv.className = `alert alert-${tipo}`;
        mensagemDiv.textContent = texto;
        mensagemDiv.classList.remove('d-none');
        
        // Auto-esconder após 3 segundos
        setTimeout(() => {
            mensagemDiv.classList.add('d-none');
        }, 3000);
        
        this.log(`📨 Mensagem exibida (${tipo}): ${texto}`);
    },
    
    /**
     * ✅ VALIDAR SUBMIT DO FORMULÁRIO
     */
    validarSubmit: function(e) {
        this.log('🔥 [SUBMIT DEBUG] ================================');
        this.log('🔥 [SUBMIT DEBUG] VALIDANDO FORMULÁRIO');
        this.log('🔥 [SUBMIT DEBUG] ================================');
        this.log('📊 [SUBMIT] presencasRegistradas:', JSON.stringify(this.presencasRegistradas, null, 2));
        this.log('📅 [SUBMIT] diasSelecionados:', JSON.stringify(this.diasSelecionados, null, 2));
        this.log('🔍 [SUBMIT] window._presenca_confirmado:', window._presenca_confirmado);
        
        // Se o usuário já confirmou, permite o envio
        if (window._presenca_confirmado) {
            this.log('✅ [SUBMIT] Usuário já confirmou - permitindo envio');
            this.log('🔥 [SUBMIT DEBUG] ENVIANDO FORMULÁRIO CONFIRMADO');
            return true;
        }
        
        // Sempre previne o envio inicial para mostrar modal de confirmação
        e.preventDefault();
        
        this.log('🔍 [SUBMIT] Checando se há dados para enviar...');
        
        // Verifica se há dados mínimos para mostrar o modal
        const temAlgumDado = Object.keys(this.diasSelecionados).length > 0 || 
                            Object.keys(this.presencasRegistradas).length > 0;
        
        if (!temAlgumDado) {
            this.log('❌ [SUBMIT] Nenhum dado encontrado - mostrando erro');
            this.mostrarMensagem('Selecione os dias e marque as presenças antes de finalizar.', 'danger');
            return false;
        }
        
        // Gera resumo para modal de confirmação
        this.log('📋 [SUBMIT] Gerando resumo...');
        const resultado = this.gerarResumoFinalizacao();
        this.log('📋 [SUBMIT] Resultado do resumo:', resultado);
        
        // Adiciona dados ao formulário antes de exibir o modal
        this.log('📝 [SUBMIT] Adicionando dados ao formulário...');
        const dadosAdicionados = this.adicionarDadosAoFormulario();
        this.log('📝 [SUBMIT] Dados adicionados:', dadosAdicionados);
        
        // Exibe modal de confirmação
        this.log('📋 [SUBMIT] Exibindo modal de confirmação...');
        this.exibirModalConfirmacao(resultado);
        
        this.log('🔥 [SUBMIT DEBUG] Modal de confirmação exibido');
        return false;
    },
    
    /**
     * 📋 ADICIONAR DADOS AO FORMULÁRIO
     */
    adicionarDadosAoFormulario: function() {
        this.log('🔥 [FORM DEBUG] ================================');
        this.log('🔥 [FORM DEBUG] ADICIONANDO DADOS AO FORMULÁRIO');
        this.log('🔥 [FORM DEBUG] ================================');
        
        const form = document.getElementById('form-presenca');
        if (!form) {
            this.log('❌ [FORM] Formulário não encontrado');
            return;
        }
        
        this.log('✅ [FORM] Formulário encontrado');
        this.log('📊 [FORM] Dados a serem enviados:');
        this.log('📊 [FORM] presencasRegistradas:', JSON.stringify(this.presencasRegistradas, null, 2));
        this.log('📊 [FORM] convocadosIndividuais:', JSON.stringify(this.convocadosIndividuais, null, 2));
        this.log('📊 [FORM] diasSelecionados:', JSON.stringify(this.diasSelecionados, null, 2));
        
        // Remove campos antigos para evitar duplicação
        form.querySelectorAll('input[name^="presencas_json"], input[name^="convocados_json"], input[name^="dias_json"]').forEach(el => {
            this.log(`🗑️ [FORM] Removendo campo antigo: ${el.name}`);
            el.remove();
        });
        
        // 1️⃣ ADICIONA DADOS DE PRESENÇAS
        if (Object.keys(this.presencasRegistradas).length > 0) {
            const inputPresencas = document.createElement('input');
            inputPresencas.type = 'hidden';
            inputPresencas.name = 'presencas_json';
            inputPresencas.value = JSON.stringify(this.presencasRegistradas);
            form.appendChild(inputPresencas);
            this.log('✅ [FORM] Campo presencas_json adicionado');
            this.log('📝 [FORM] Valor:', inputPresencas.value);
        } else {
            this.log('⚠️ [FORM] Nenhuma presença registrada para enviar');
        }
        
        // 2️⃣ ADICIONA DADOS DE CONVOCAÇÃO (se houver)
        if (Object.keys(this.convocadosIndividuais).length > 0) {
            const inputConvocados = document.createElement('input');
            inputConvocados.type = 'hidden';
            inputConvocados.name = 'convocados_json';
            inputConvocados.value = JSON.stringify(this.convocadosIndividuais);
            form.appendChild(inputConvocados);
            this.log('✅ [FORM] Campo convocados_json adicionado');
            this.log('📝 [FORM] Valor:', inputConvocados.value);
        } else {
            this.log('⚠️ [FORM] Nenhuma convocação individual para enviar');
        }
        
        // 3️⃣ ADICIONA DIAS SELECIONADOS
        if (Object.keys(this.diasSelecionados).length > 0) {
            const inputDias = document.createElement('input');
            inputDias.type = 'hidden';
            inputDias.name = 'dias_json';
            inputDias.value = JSON.stringify(this.diasSelecionados);
            form.appendChild(inputDias);
            this.log('✅ [FORM] Campo dias_json adicionado');
            this.log('📝 [FORM] Valor:', inputDias.value);
        } else {
            this.log('⚠️ [FORM] Nenhum dia selecionado para enviar');
        }
        
        // 4️⃣ ATUALIZA TAMBÉM OS CAMPOS NATIVOS DO FLATPICKR
        this.log('🔄 [FORM] Atualizando campos nativos do Flatpickr...');
        Object.keys(this.diasSelecionados).forEach(atividadeId => {
            const dias = this.diasSelecionados[atividadeId];
            if (dias && dias.length > 0) {
                const input = document.getElementById(`dias-atividade-${atividadeId}`);
                if (input && input._flatpickr) {
                    // Reconstrói as datas para o Flatpickr
                    const ano = typeof window.ano !== 'undefined' ? window.ano : new Date().getFullYear();
                    const mes = typeof window.mes !== 'undefined' ? window.mes : new Date().getMonth() + 1;
                    
                    const datas = dias.map(dia => new Date(ano, mes - 1, dia));
                    input._flatpickr.setDate(datas, true);
                    this.log(`✅ [FORM] Flatpickr atualizado para atividade ${atividadeId}: dias ${dias.join(', ')}`);
                } else {
                    this.log(`❌ [FORM] Input ou Flatpickr não encontrado para atividade ${atividadeId}`);
                }
            }
        });
        
        // 5️⃣ VERIFICA SE TODOS OS DADOS NECESSÁRIOS ESTÃO PRESENTES
        const temPresencas = Object.keys(this.presencasRegistradas).length > 0;
        const temDias = Object.keys(this.diasSelecionados).length > 0;
        
        this.log('🔍 [FORM] VERIFICAÇÃO FINAL:');
        this.log(`📊 [FORM] Tem presenças: ${temPresencas}`);
        this.log(`📅 [FORM] Tem dias selecionados: ${temDias}`);
        
        if (!temPresencas || !temDias) {
            this.log('❌ [FORM] DADOS INSUFICIENTES PARA ENVIO!');
            this.log('💡 [FORM] Certifique-se de:');
            this.log('   - Selecionar dias nos calendários');
            this.log('   - Marcar presenças clicando nos dias azuis');
            return false;
        }
        
        this.log('🔥 [FORM DEBUG] ================================');
        this.log('🔥 [FORM DEBUG] DADOS ADICIONADOS COM SUCESSO');
        this.log('🔥 [FORM DEBUG] ================================');
        
        return true;
    },
    
    /**
     * 🔍 DEBUGAR FORMULÁRIO ANTES DO ENVIO
     */
    debugarFormulario: function() {
        const form = document.getElementById('form-presenca');
        if (!form) {
            this.log('❌ [DEBUG FORM] Formulário não encontrado');
            return;
        }
        
        this.log('🔍 [DEBUG FORM] ================================');
        this.log('🔍 [DEBUG FORM] ESTADO DO FORMULÁRIO');
        this.log('🔍 [DEBUG FORM] ================================');
        
        // Verificar todos os campos do formulário
        const formData = new FormData(form);
        
        this.log('📝 [DEBUG FORM] Dados do FormData:');
        for (let [key, value] of formData.entries()) {
            this.log(`   ${key}: ${value}`);
        }
        
        // Verificar campos hidden específicos
        const camposEspeciais = ['presencas_json', 'convocados_json', 'dias_json'];
        camposEspeciais.forEach(campo => {
            const input = form.querySelector(`input[name="${campo}"]`);
            if (input) {
                this.log(`✅ [DEBUG FORM] ${campo} encontrado:`, input.value);
            } else {
                this.log(`❌ [DEBUG FORM] ${campo} NÃO encontrado`);
            }
        });
        
        // Verificar estado interno
        this.log('📊 [DEBUG FORM] Estado interno:');
        this.log('   presencasRegistradas:', Object.keys(this.presencasRegistradas).length);
        this.log('   diasSelecionados:', Object.keys(this.diasSelecionados).length);
        this.log('   convocadosIndividuais:', Object.keys(this.convocadosIndividuais).length);
        
        this.log('🔍 [DEBUG FORM] ================================');
        
        return {
            temFormulario: !!form,
            camposPresentes: camposEspeciais.filter(campo => form.querySelector(`input[name="${campo}"]`)),
            estadoInterno: {
                presencas: Object.keys(this.presencasRegistradas).length,
                dias: Object.keys(this.diasSelecionados).length,
                convocados: Object.keys(this.convocadosIndividuais).length
            }
        };
    },

    /**
     * 📋 FUNÇÃO: GERAR RESUMO PARA FINALIZAÇÃO
     */
    gerarResumoFinalizacao: function() {
        this.log('📋 [RESUMO] Gerando resumo para finalização...');
        
        const erros = [];
        const avisos = [];
        let totalPresencas = 0;
        let totalDiasSelecionados = 0;
        const atividadesComProblemas = [];
        const atividadesCompletas = [];
        
        // Analisa cada atividade individualmente
        Object.keys(this.diasSelecionados).forEach(atividadeId => {
            const diasDaAtividade = this.diasSelecionados[atividadeId] || [];
            const nomeAtividade = this.obterNomeAtividade(atividadeId);
            const presencasDaAtividade = this.presencasRegistradas[atividadeId] || {};
            
            totalDiasSelecionados += diasDaAtividade.length;
            
            const diasComPresenca = [];
            const diasSemPresenca = [];
            let presencasAtividade = 0;
            
            diasDaAtividade.forEach(dia => {
                const presencasDia = presencasDaAtividade[dia];
                if (presencasDia && Object.keys(presencasDia).length > 0) {
                    diasComPresenca.push(dia);
                    presencasAtividade += Object.keys(presencasDia).length;
                } else {
                    diasSemPresenca.push(dia);
                }
            });
            
            totalPresencas += presencasAtividade;
            
            // Analisa problemas específicos da atividade
            if (diasSemPresenca.length > 0) {
                const diasTexto = diasSemPresenca.length === 1 ? 
                    `dia ${diasSemPresenca[0]}` : 
                    `dias ${diasSemPresenca.join(', ')}`;
                    
                atividadesComProblemas.push({
                    nome: nomeAtividade,
                    problema: `Presenças não marcadas no ${diasTexto}`,
                    tipo: 'erro'
                });
            } else if (diasComPresenca.length > 0) {
                atividadesCompletas.push({
                    nome: nomeAtividade,
                    dias: diasComPresenca,
                    presencas: presencasAtividade
                });
            }
            
            // Avisos para atividades com presenças incompletas
            if (diasComPresenca.length > 0 && presencasAtividade < diasComPresenca.length * this.alunosData.length) {
                const totalEsperado = diasComPresenca.length * this.alunosData.length;
                avisos.push(`${nomeAtividade}: ${presencasAtividade} de ${totalEsperado} presenças registradas nos dias ${diasComPresenca.join(', ')}`);
            }
        });
        
        // Validações principais
        if (totalDiasSelecionados === 0) {
            erros.push('Nenhum dia foi selecionado nos calendários das atividades.');
        }
        
        if (totalPresencas === 0) {
            erros.push('Nenhuma presença foi registrada. Clique nos dias azuis selecionados para marcar presenças.');
        }
        
        // Adiciona erros específicos das atividades
        atividadesComProblemas.forEach(problema => {
            if (problema.tipo === 'erro') {
                erros.push(`${problema.nome}: ${problema.problema}`);
            }
        });
        
        const sucesso = erros.length === 0;
        const podeFinalizar = sucesso;
        
        this.log(`📋 [RESUMO] Sucesso: ${sucesso}, Presenças: ${totalPresencas}, Dias: ${totalDiasSelecionados}`);
        this.log(`📋 [RESUMO] Atividades completas:`, atividadesCompletas);
        this.log(`📋 [RESUMO] Atividades com problemas:`, atividadesComProblemas);
        
        return {
            sucesso,
            erros,
            avisos,
            podeFinalizar,
            dados: {
                totalPresencas,
                totalDias: totalDiasSelecionados,
                totalAlunos: this.alunosData.length,
                atividadesCompletas,
                atividadesComProblemas
            }
        };
    },

    /**
     * 📋 FUNÇÃO: EXIBIR MODAL DE CONFIRMAÇÃO
     */
    exibirModalConfirmacao: function(resultado) {
        this.log('📋 [MODAL-CONF] Exibindo modal de confirmação:', resultado);
        
        // Busca o modal de confirmação ou cria se não existir
        let modalConf = document.getElementById('modal-confirmacao-finalizacao');
        if (!modalConf) {
            modalConf = this.criarModalConfirmacao();
        }
        
        // Atualiza conteúdo do modal
        const titulo = modalConf.querySelector('.modal-title');
        const corpo = modalConf.querySelector('.modal-body');
        const botaoConfirmar = modalConf.querySelector('.btn-confirmar');
        const botaoCancelar = modalConf.querySelector('.btn-cancelar');
        
        if (!titulo || !corpo || !botaoCancelar) {
            this.log('❌ [MODAL-CONF] Elementos do modal não encontrados, recriando...');
            modalConf.remove();
            modalConf = this.criarModalConfirmacao();
            return this.exibirModalConfirmacao(resultado);
        }
        
        if (resultado.sucesso) {
            titulo.textContent = '✅ Finalização Confirmada';
            titulo.className = 'modal-title text-success';
            
            let html = '<div class="alert alert-success">';
            html += `<strong>📊 Resumo dos dados a serem enviados:</strong><br>`;
            html += `• <strong>${resultado.dados.totalPresencas}</strong> presenças registradas<br>`;
            html += `• <strong>${resultado.dados.totalDias}</strong> dias selecionados<br>`;
            html += `• <strong>${resultado.dados.totalAlunos}</strong> alunos na turma<br><br>`;
            
            // Mostra detalhes das atividades completas
            if (resultado.dados.atividadesCompletas && resultado.dados.atividadesCompletas.length > 0) {
                html += '<strong>🎯 Atividades Prontas:</strong><br>';
                resultado.dados.atividadesCompletas.forEach(atividade => {
                    const diasTexto = atividade.dias.length === 1 ? 
                        `dia ${atividade.dias[0]}` : 
                        `dias ${atividade.dias.join(', ')}`;
                    html += `• <span style="color: #0066cc;"><strong>${atividade.nome}</strong></span>: ${atividade.presencas} presenças no ${diasTexto}<br>`;
                });
            }
            
            html += '</div>';
            
            if (resultado.avisos.length > 0) {
                html += '<div class="alert alert-warning"><strong>⚠️ Observações:</strong><ul>';
                resultado.avisos.forEach(aviso => {
                    html += `<li>${aviso}</li>`;
                });
                html += '</ul></div>';
            }
            
            corpo.innerHTML = html;
            if (botaoConfirmar) {
                botaoConfirmar.textContent = 'Confirmar Envio';
                botaoConfirmar.className = 'btn btn-success';
                botaoConfirmar.style.display = 'inline-block';
            }
        } else {
            titulo.textContent = '❌ Erros Encontrados';
            titulo.className = 'modal-title text-danger';
            
            let html = '<div class="alert alert-danger"><strong>🚫 Problemas que impedem o envio:</strong><ul>';
            resultado.erros.forEach(erro => {
                html += `<li>${erro}</li>`;
            });
            html += '</ul></div>';
            
            // Adiciona instruções específicas
            html += '<div class="alert alert-info">';
            html += '<strong>💡 Como resolver:</strong><br>';
            html += '1️⃣ Selecione os dias nos calendários das atividades<br>';
            html += '2️⃣ Clique nos <span class="badge bg-primary">dias azuis selecionados</span> para marcar presenças<br>';
            html += '3️⃣ Use os botões "Todos Presentes/Ausentes" ou marque individualmente<br>';
            html += '4️⃣ Clique em "Salvar Presenças" em cada dia marcado';
            html += '</div>';
            
            if (resultado.avisos.length > 0) {
                html += '<div class="alert alert-warning"><strong>⚠️ Observações:</strong><ul>';
                resultado.avisos.forEach(aviso => {
                    html += `<li>${aviso}</li>`;
                });
                html += '</ul></div>';
            }
            
            corpo.innerHTML = html;
            if (botaoConfirmar) {
                botaoConfirmar.style.display = 'none';
            }
        }
        
        // Configura eventos dos botões
        if (botaoConfirmar) {
            botaoConfirmar.onclick = () => {
                // 🎯 LOG DE DEBUG PARA CLIQUE NO BOTÃO CONFIRMAR ENVIO
                console.log('🚀 [DEBUG-CLIQUE] ========================================');
                console.log('🚀 [DEBUG-CLIQUE] BOTÃO "CONFIRMAR ENVIO" FOI CLICADO!');
                console.log('🚀 [DEBUG-CLIQUE] Timestamp:', new Date().toLocaleString());
                console.log('🚀 [DEBUG-CLIQUE] Modal de confirmação -> Confirmar Envio');
                console.log('🚀 [DEBUG-CLIQUE] ========================================');
                
                this.log('📋 [MODAL-CONF] Usuário confirmou envio');
                window._presenca_confirmado = true;
                modalConf.style.display = 'none';
                
                // 🔍 DIAGNÓSTICO FINAL ANTES DO ENVIO
                this.log('🔍 [ENVIO] ================================');
                this.log('🔍 [ENVIO] DIAGNÓSTICO FINAL PRÉ-ENVIO');
                this.log('🔍 [ENVIO] ================================');
                
                const form = document.getElementById('form-presenca');
                if (form) {
                    // GARANTIR que os dados estão no formulário ANTES do envio
                    this.log('📝 [ENVIO] Adicionando dados ao formulário uma última vez...');
                    const dadosAdicionados = this.adicionarDadosAoFormulario();
                    
                    if (!dadosAdicionados) {
                        this.log('❌ [ENVIO] ERRO: Dados não foram adicionados corretamente!');
                        alert('Erro: Dados não puderam ser preparados para envio. Tente novamente.');
                        window._presenca_confirmado = false;
                        return;
                    }
                    
                    // Lista todos os campos que serão enviados
                    const formData = new FormData(form);
                    this.log('📝 [ENVIO] Dados que serão enviados:');
                    let temDadosEssenciais = false;
                    
                    for (let [key, value] of formData.entries()) {
                        if (key.includes('json')) {
                            this.log(`   📋 ${key}:`, JSON.stringify(JSON.parse(value), null, 2));
                            if (key === 'presencas_json' && value !== '{}') {
                                temDadosEssenciais = true;
                            }
                        } else {
                            this.log(`   📄 ${key}: ${value}`);
                        }
                    }
                    
                    // Verificação final de segurança
                    if (!temDadosEssenciais) {
                        this.log('❌ [ENVIO] ERRO CRÍTICO: Nenhum dado de presença encontrado!');
                        alert('ERRO: Nenhuma presença foi encontrada para envio. Selecione os dias e marque as presenças antes de finalizar.');
                        window._presenca_confirmado = false;
                        return;
                    }
                    
                    // Salva estado atual no localStorage para recuperação após reload
                    this.salvarEstadoParaRecuperacao();
                    
                    this.log('📤 [ENVIO] Enviando formulário...');
                    
                    // 🔧 CORREÇÃO: Força URL do endpoint AJAX
                    form.action = '/presencas/registrar-presenca/dias-atividades/ajax/';
                    
                    this.log('🎯 [ENVIO] URL de destino:', form.action);
                    this.log('🎯 [ENVIO] Método:', form.method || 'POST');
                    
                    // Força o envio
                    form.submit();
                    
                    this.log('✅ [ENVIO] Comando submit() executado');
                } else {
                    this.log('❌ [ENVIO] Formulário não encontrado!');
                    alert('Erro: Formulário não encontrado. Recarregue a página e tente novamente.');
                }
            };
        }
        
        botaoCancelar.onclick = () => {
            // 🎯 LOG DE DEBUG PARA CLIQUE NO BOTÃO CANCELAR DO MODAL DE CONFIRMAÇÃO
            console.log('❌ [DEBUG-CLIQUE] ========================================');
            console.log('❌ [DEBUG-CLIQUE] BOTÃO "CANCELAR" (MODAL CONFIRMAÇÃO) FOI CLICADO!');
            console.log('❌ [DEBUG-CLIQUE] Timestamp:', new Date().toLocaleString());
            console.log('❌ [DEBUG-CLIQUE] Modal de confirmação -> Cancelar');
            console.log('❌ [DEBUG-CLIQUE] ========================================');
            
            this.log('📋 [MODAL-CONF] Usuário cancelou envio');
            window._presenca_confirmado = false;
            modalConf.style.display = 'none';
        };
        
        // Limpa confirmação anterior ao abrir modal
        window._presenca_confirmado = false;
        
        // Exibe o modal
        modalConf.style.display = 'block';
    },

    /**
     * 📋 FUNÇÃO: CRIAR MODAL DE CONFIRMAÇÃO (SE NÃO EXISTIR)
     */
    criarModalConfirmacao: function() {
        this.log('📋 [MODAL-CONF] Criando modal de confirmação...');
        
        const modalHtml = `
            <div id="modal-confirmacao-finalizacao" class="modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); z-index: 10000;">
                <div class="modal-dialog" style="margin: 50px auto; max-width: 700px;">
                    <div class="modal-content" style="background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <div class="modal-header" style="padding: 15px; border-bottom: 1px solid #ddd; display: flex; justify-content: space-between; align-items: center;">
                            <h5 class="modal-title">Confirmação</h5>
                            <button type="button" class="btn-close" onclick="document.getElementById('modal-confirmacao-finalizacao').style.display='none'" style="background: none; border: none; font-size: 24px; cursor: pointer;">&times;</button>
                        </div>
                        <div class="modal-body" style="padding: 20px; max-height: 400px; overflow-y: auto;">
                            <!-- Conteúdo será preenchido dinamicamente -->
                        </div>
                        <div class="modal-footer" style="padding: 15px; border-top: 1px solid #ddd; text-align: right;">
                            <button type="button" class="btn btn-secondary btn-cancelar" style="margin-right: 10px; padding: 8px 16px; border: 1px solid #6c757d; background: #6c757d; color: white; border-radius: 4px; cursor: pointer;">Cancelar</button>
                            <button type="button" class="btn btn-primary btn-confirmar" style="padding: 8px 16px; border: 1px solid #007bff; background: #007bff; color: white; border-radius: 4px; cursor: pointer;">Confirmar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = document.getElementById('modal-confirmacao-finalizacao');
        
        this.log('📋 [MODAL-CONF] Modal criado com sucesso');
        
        return modal;
    },
    
    /**
     * 💾 SALVAR ESTADO PARA RECUPERAÇÃO APÓS RELOAD
     */
    salvarEstadoParaRecuperacao: function() {
        this.log('💾 [ESTADO] Salvando estado para recuperação...');
        
        const estado = {
            timestamp: Date.now(),
            presencasRegistradas: this.presencasRegistradas,
            diasSelecionados: this.diasSelecionados,
            convocadosIndividuais: this.convocadosIndividuais,
            turmaId: this.turmaId,
            url: window.location.href
        };
        
        try {
            localStorage.setItem('presenca_estado_backup', JSON.stringify(estado));
            this.log('✅ [ESTADO] Estado salvo no localStorage');
        } catch (error) {
            this.log('❌ [ESTADO] Erro ao salvar estado:', error);
        }
    },
    
    /**
     * 🔄 RECUPERAR ESTADO APÓS RELOAD
     */
    recuperarEstadoAposReload: function() {
        this.log('🔄 [ESTADO] Verificando se há estado para recuperar...');
        
        try {
            const estadoSalvo = localStorage.getItem('presenca_estado_backup');
            if (!estadoSalvo) {
                this.log('ℹ️ [ESTADO] Nenhum estado salvo encontrado');
                return false;
            }
            
            const estado = JSON.parse(estadoSalvo);
            const tempoDecorrido = Date.now() - estado.timestamp;
            
            // Só recupera se foi salvo há menos de 5 minutos
            if (tempoDecorrido > 5 * 60 * 1000) {
                this.log('⏰ [ESTADO] Estado muito antigo, ignorando');
                localStorage.removeItem('presenca_estado_backup');
                return false;
            }
            
            // Verifica se estamos na mesma URL
            if (estado.url !== window.location.href) {
                this.log('🔗 [ESTADO] URL diferente, ignorando estado');
                return false;
            }
            
            this.log('🔄 [ESTADO] Recuperando estado...');
            this.presencasRegistradas = estado.presencasRegistradas || {};
            this.diasSelecionados = estado.diasSelecionados || {};
            this.convocadosIndividuais = estado.convocadosIndividuais || {};
            this.turmaId = estado.turmaId;
            
            this.log('✅ [ESTADO] Estado recuperado com sucesso');
            this.log('📊 [ESTADO] Dados recuperados:');
            this.log('   presencasRegistradas:', Object.keys(this.presencasRegistradas).length, 'atividades');
            this.log('   diasSelecionados:', Object.keys(this.diasSelecionados).length, 'atividades');
            this.log('   convocadosIndividuais:', Object.keys(this.convocadosIndividuais).length, 'alunos');
            
            // Limpa o estado salvo após recuperar
            localStorage.removeItem('presenca_estado_backup');
            
            // Atualiza a interface com os dados recuperados
            setTimeout(() => {
                this.atualizarInterfaceComEstadoRecuperado();
            }, 500);
            
            return true;
            
        } catch (error) {
            this.log('❌ [ESTADO] Erro ao recuperar estado:', error);
            localStorage.removeItem('presenca_estado_backup');
            return false;
        }
    },
    
    /**
     * 🎨 ATUALIZAR INTERFACE COM ESTADO RECUPERADO
     */
    atualizarInterfaceComEstadoRecuperado: function() {
        this.log('🎨 [INTERFACE] Atualizando interface com estado recuperado...');
        
        // Atualiza os calendários Flatpickr
        Object.keys(this.diasSelecionados).forEach(atividadeId => {
            const dias = this.diasSelecionados[atividadeId];
            if (dias && dias.length > 0) {
                const input = document.getElementById(`dias-atividade-${atividadeId}`);
                if (input && input._flatpickr) {
                    const ano = typeof window.ano !== 'undefined' ? window.ano : new Date().getFullYear();
                    const mes = typeof window.mes !== 'undefined' ? window.mes : new Date().getMonth() + 1;
                    
                    const datas = dias.map(dia => new Date(ano, mes - 1, dia));
                    input._flatpickr.setDate(datas, true);
                    
                    this.log(`📅 [INTERFACE] Calendário ${atividadeId} atualizado com dias: ${dias.join(', ')}`);
                }
            }
        });
        
        // Mostra mensagem de estado recuperado
        this.mostrarMensagem('Estado anterior recuperado! Seus dados foram preservados.', 'info');
        
        this.log('✅ [INTERFACE] Interface atualizada com estado recuperado');
    }
};

/**
 * � FUNÇÕES GLOBAIS DE DEBUG PARA CONSOLE (continuação)
 */
window.debugarFormulario = function() {
    if (window.PresencaApp) {
        return window.PresencaApp.debugarFormulario();
    } else {
        console.log('❌ PresencaApp não está disponível');
        return null;
    }
};

window.verificarDadosFormulario = function() {
    const form = document.getElementById('form-presenca');
    if (!form) {
        console.log('❌ Formulário não encontrado');
        return;
    }
    
    console.log('🔍 Verificando dados do formulário...');
    const formData = new FormData(form);
    
    console.log('📝 Todos os dados do formulário:');
    for (let [key, value] of formData.entries()) {
        console.log(`   ${key}: ${value}`);
    }
    
    return Array.from(formData.entries());
};

/**
 * �🚀 AUTO-INICIALIZAÇÃO QUANDO DOM ESTIVER PRONTO
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔥 [CRITICAL] DOMContentLoaded disparado!');
    console.log('🔥 [CRITICAL] Estado atual do window:', {
        PresencaManager: !!window.PresencaManager,
        PresencaApp: !!window.PresencaApp,
        flatpickr: !!window.flatpickr
    });
    
    // DETECTA MÚLTIPLAS INSTÂNCIAS
    if (window.__presencaManagerInitialized) {
        console.error('❌ [CRITICAL] PresencaManager já foi inicializado! Possível carregamento duplo!');
        return;
    }
    window.__presencaManagerInitialized = true;
    
    // Aguarda um pouco para garantir que outros scripts carregaram
    setTimeout(() => {
        console.log('🔥 [CRITICAL] Inicializando PresencaManager...');
        window.PresencaManager.init();
        console.log('🔥 [CRITICAL] PresencaManager inicializado!');
    }, 100);
});

/**
 * 🌐 FUNÇÕES GLOBAIS PARA COMPATIBILIDADE COM O TEMPLATE
 */

// Função global para fechar modal (compatibilidade)
function fecharModalPresenca() {
    window.PresencaManager.fecharModal();
}

// Expor PresencaApp para compatibilidade total
window.PresencaApp = {
    // Redirect para PresencaManager
    marcarTodosPresentes: () => window.PresencaManager.marcarTodosPresentes(),
    marcarTodosAusentes: () => window.PresencaManager.marcarTodosAusentes(),
    salvarPresencaDia: () => window.PresencaManager.salvarDiaAtual(),
    fecharModalPresenca: () => window.PresencaManager.fecharModal(),
    abrirModalPresenca: (atividade, dia) => window.PresencaManager.abrirModal(atividade, dia),
    
    // Propriedades compartilhadas
    get presencasRegistradas() { return window.PresencaManager.presencasRegistradas; },
    get alunosData() { return window.PresencaManager.alunosData; },
    get atividadeAtual() { return window.PresencaManager.atividadeAtual; },
    get diaAtual() { return window.PresencaManager.diaAtual; }
};

console.log('🚀 PresencaManager carregado - Arquitetura Simplificada Ativa!');

// MONITOR DE ESTADO DO MODAL (DEBUG CRÍTICO)
window.DebugPresenca = {
    monitorar: function() {
        const modal = document.getElementById('presencaModal');
        if (!modal) {
            console.log('🔍 [MONITOR] Modal não encontrado');
            return;
        }
        
        const estado = {
            display: modal.style.display,
            classes: modal.className,
            bodyClasses: document.body.className,
            visibility: modal.style.visibility || 'visible',
            zIndex: modal.style.zIndex || 'auto',
            PresencaManagerAtual: {
                atividadeAtual: window.PresencaManager?.atividadeAtual,
                diaAtual: window.PresencaManager?.diaAtual,
                isModalAberto: window.PresencaManager?.isModalAberto()
            }
        };
        
        console.log('🔍 [MONITOR] Estado do modal:', estado);
        return estado;
    },
    
    forcarFechar: function() {
        console.log('🔧 [FORCE] Forçando fechamento do modal...');
        const modal = document.getElementById('presencaModal');
        if (modal) {
            console.log('📊 [FORCE] Estado ANTES:', {
                display: modal.style.display,
                classes: modal.className,
                visibility: modal.style.visibility
            });
            
            // FORÇA o fechamento com múltiplas estratégias EXTREMAS
            modal.style.setProperty('display', 'none', 'important');
            modal.style.setProperty('visibility', 'hidden', 'important');
            modal.style.setProperty('opacity', '0', 'important');
            modal.style.setProperty('z-index', '-99999', 'important');
            modal.style.setProperty('position', 'fixed', 'important');
            modal.style.setProperty('top', '-9999px', 'important');
            modal.style.setProperty('left', '-9999px', 'important');
            modal.classList.remove('show');
            modal.classList.add('d-none');
            modal.removeAttribute('style'); // Remove todos os estilos inline
            modal.style.display = 'none !important'; // Reaplica o display
            document.body.classList.remove('modal-open');
            
            // Força remoção de qualquer backdrop
            const backdrops = document.querySelectorAll('.modal-backdrop, .presenca-modal-backdrop');
            backdrops.forEach(backdrop => backdrop.remove());
            
            // Chama também o método do PresencaManager
            if (window.PresencaManager && window.PresencaManager.fecharModal) {
                window.PresencaManager.atividadeAtual = null;
                window.PresencaManager.diaAtual = null;
            }
            
            console.log('� [FORCE] Estado DEPOIS:', {
                display: modal.style.display,
                classes: modal.className,
                visibility: modal.style.visibility,
                opacity: modal.style.opacity,
                zIndex: modal.style.zIndex
            });
            
            console.log('✅ [FORCE] Modal fechado à força!');
        } else {
            console.log('❌ [FORCE] Modal não encontrado!');
        }
    },
    
    destruirModal: function() {
        console.log('💥 [DESTROY] DESTRUINDO modal completamente...');
        const modal = document.getElementById('presencaModal');
        if (modal) {
            // Salva o HTML para poder recriar depois se necessário
            window._modalHTML = modal.outerHTML;
            modal.remove();
            console.log('💥 [DESTROY] Modal REMOVIDO do DOM!');
            
            // Limpa estado do PresencaManager
            if (window.PresencaManager) {
                window.PresencaManager.atividadeAtual = null;
                window.PresencaManager.diaAtual = null;
            }
            
            document.body.classList.remove('modal-open');
            console.log('✅ [DESTROY] Modal destruído com sucesso!');
        } else {
            console.log('❌ [DESTROY] Modal não encontrado!');
        }
    },
    
    recriarModal: function() {
        console.log('🔨 [RECREATE] Recriando modal...');
        if (window._modalHTML) {
            document.body.insertAdjacentHTML('beforeend', window._modalHTML);
            console.log('✅ [RECREATE] Modal recriado!');
        } else {
            console.log('❌ [RECREATE] HTML do modal não foi salvo!');
        }
    },
    
    emergencia: function() {
        console.log('🚨 [EMERGENCY] EXECUTANDO PROTOCOLO DE EMERGÊNCIA!');
        
        // Etapa 1: Força fechamento
        this.forcarFechar();
        
        // Etapa 2: Limpa timeouts
        this.verificarSetTimeouts();
        
        // Etapa 3: Se ainda estiver aberto, destrói
        setTimeout(() => {
            const modal = document.getElementById('presencaModal');
            if (modal && modal.style.display !== 'none') {
                console.log('🚨 [EMERGENCY] Modal ainda aberto! DESTRUINDO...');
                this.destruirModal();
            }
        }, 100);
        
        console.log('✅ [EMERGENCY] Protocolo de emergência executado!');
    },
    
    verificarSetTimeouts: function() {
        console.log('⏰ [DEBUG] Verificando setTimeouts ativos...');
        console.log('⏰ [DEBUG] Note: Esta funcionalidade requer ferramentas avançadas de debug');
        // Não há uma forma nativa de listar todos os setTimeouts ativos
        // Mas podemos verificar se há algum conflito
        
        // Vamos limpar qualquer setTimeout que possa estar interferindo
        for (let i = 1; i < 10000; i++) {
            clearTimeout(i);
        }
        console.log('🧹 [DEBUG] Limpeza de setTimeouts concluída');
    },
    
    verificarCalendarios: function() {
        console.log('📅 [DEBUG] === DIAGNÓSTICO DE CALENDÁRIOS ===');
        
        // Verifica se Flatpickr está carregado
        console.log('📦 [DEBUG] Flatpickr carregado:', typeof flatpickr !== 'undefined');
        
        // Verifica inputs
        const inputs = document.querySelectorAll('.dias-datepicker');
        console.log('🔍 [DEBUG] Inputs .dias-datepicker encontrados:', inputs.length);
        
        inputs.forEach((input, index) => {
            const atividadeId = input.dataset.atividade;
            const maxDias = input.dataset.maxdias;
            const temFlatpickr = !!input._flatpickr;
            
            console.log(`📅 [DEBUG] Input ${index}:`, {
                id: input.id,
                atividade: atividadeId,
                maxDias: maxDias,
                temFlatpickr: temFlatpickr,
                classes: input.className,
                style: input.style.cssText,
                readonly: input.readOnly,
                disabled: input.disabled
            });
            
            // Verifica ícone
            const icon = input.parentElement?.querySelector('.calendar-icon');
            console.log(`🔍 [DEBUG] Ícone ${index}:`, {
                encontrado: !!icon,
                classes: icon?.className,
                style: icon?.style.cssText
            });
        });
        
        // Função utilitária para testar reabertura do calendário
        window.testarReaberturaCalendario = function(atividadeId) {
            console.log('🧪 [TEST] Testando reabertura do calendário para atividade:', atividadeId);
            if (PresencaManager && PresencaManager.reabrirCalendarioAutomaticamente) {
                PresencaManager.reabrirCalendarioAutomaticamente(atividadeId);
            } else {
                console.log('❌ [TEST] PresencaManager não disponível');
            }
        };
        
        // Função de emergência para reabrir calendário da última atividade
        window.reabrirUltimoCalendario = function() {
            console.log('🚨 [EMERGENCY] Tentando reabrir último calendário...');
            
            // Tenta extrair da variável global atividadesData
            if (typeof window.atividadesData !== 'undefined') {
                const atividades = Object.keys(window.atividadesData);
                console.log('🔍 [EMERGENCY] Atividades disponíveis:', atividades);
                
                if (atividades.length > 0) {
                    // Pega a primeira atividade como fallback
                    const atividadeId = atividades[0];
                    console.log('🎯 [EMERGENCY] Usando atividade:', atividadeId);
                    if (PresencaManager && PresencaManager.reabrirCalendarioAutomaticamente) {
                        PresencaManager.reabrirCalendarioAutomaticamente(atividadeId);
                    }
                } else {
                    console.log('❌ [EMERGENCY] Nenhuma atividade encontrada');
                }
            } else {
                console.log('❌ [EMERGENCY] atividadesData não disponível');
            }
        };
        
        console.log('🧪 [DEBUG] Função de teste criada: testarReaberturaCalendario(atividadeId)');
        console.log('🚨 [DEBUG] Função de emergência criada: reabrirUltimoCalendario()');
        console.log('💡 [DEBUG] Exemplo de uso: testarReaberturaCalendario(3)');
        console.log('📅 [DEBUG] === FIM DIAGNÓSTICO ===');
    }
};

// DISPONIBILIZA IMEDIATAMENTE
console.log('🔍 [MONITOR] DebugPresenca disponível IMEDIATAMENTE!');
console.log('� [EMERGENCY] Use DebugPresenca.emergencia() para PROTOCOLO DE EMERGÊNCIA!');
console.log('�🔧 [FORCE] Use DebugPresenca.forcarFechar() para forçar fechamento BRUTAL!');
console.log('💥 [DESTROY] Use DebugPresenca.destruirModal() para REMOVER modal do DOM!');
console.log('🔨 [RECREATE] Use DebugPresenca.recriarModal() para recriar modal!');
console.log('⏰ [DEBUG] Use DebugPresenca.verificarSetTimeouts() para limpar timeouts!');
console.log('📅 [CALENDAR] Use DebugPresenca.verificarCalendarios() para diagnosticar calendários!');

// 🧪 FUNÇÕES GLOBAIS DE TESTE (disponíveis no console)
window.testarReaberturaCalendario = function(atividadeId) {
    console.log('🧪 [TEST] Testando reabertura do calendário para atividade:', atividadeId);
    if (window.PresencaManager && window.PresencaManager.reabrirCalendarioAutomaticamente) {
        window.PresencaManager.reabrirCalendarioAutomaticamente(atividadeId);
    } else {
        console.log('❌ [TEST] PresencaManager não disponível');
    }
};

window.reabrirUltimoCalendario = function() {
    console.log('🚨 [EMERGENCY] Tentando reabrir último calendário...');
    
    // Tenta extrair da variável global atividadesData
    if (typeof window.atividadesData !== 'undefined') {
        const atividades = Object.keys(window.atividadesData);
        console.log('🔍 [EMERGENCY] Atividades disponíveis:', atividades);
        
        if (atividades.length > 0) {
            // Pega a primeira atividade como fallback
            const atividadeId = atividades[0];
            console.log('🎯 [EMERGENCY] Usando atividade:', atividadeId);
            if (window.PresencaManager && window.PresencaManager.reabrirCalendarioAutomaticamente) {
                window.PresencaManager.reabrirCalendarioAutomaticamente(atividadeId);
            }
        } else {
            console.log('❌ [EMERGENCY] Nenhuma atividade encontrada');
        }
    } else {
        console.log('❌ [EMERGENCY] atividadesData não disponível');
    }
};

window.debugarEstadoPresenca = function() {
    console.log('🔍 [DEBUG] === ESTADO ATUAL DO PRESENCA MANAGER ===');
    console.log('PresencaManager disponível:', !!window.PresencaManager);
    
    if (window.PresencaManager) {
        console.log('atividadeAtual:', window.PresencaManager.atividadeAtual);
        console.log('diaAtual:', window.PresencaManager.diaAtual);
        console.log('diasSelecionados:', window.PresencaManager.diasSelecionados);
        console.log('presencasRegistradas:', Object.keys(window.PresencaManager.presencasRegistradas || {}));
        console.log('_processandoSalvamento:', window.PresencaManager._processandoSalvamento);
        console.log('isModalAberto():', window.PresencaManager.isModalAberto());
    }
    
    console.log('atividadesData global:', window.atividadesData);
    console.log('turmaId global:', window.turmaId);
    
    // Lista inputs disponíveis
    const inputs = document.querySelectorAll('[id^="dias-atividade-"]');
    console.log('Inputs de calendário disponíveis:', Array.from(inputs).map(inp => ({
        id: inp.id,
        atividade: inp.dataset.atividade,
        flatpickr: !!inp._flatpickr,
        isOpen: inp._flatpickr?.isOpen || false
    })));
    
    // Verifica modal
    const modal = document.getElementById('presencaModal');
    if (modal) {
        console.log('Estado do modal:', {
            display: modal.style.display,
            classes: modal.className,
            visibility: modal.style.visibility,
            opacity: modal.style.opacity
        });
    }
    
    console.log('🔍 [DEBUG] === FIM DEBUG ===');
};

// Expõe as funções
console.log('🧪 [SETUP] Funções de teste GLOBAIS disponíveis:');
console.log('✅ testarReaberturaCalendario(atividadeId)');
console.log('✅ reabrirUltimoCalendario()');
console.log('✅ debugarEstadoPresenca()');
console.log('✅ estabilizarCalendario(atividadeId) - NOVO!');
console.log('✅ diagnosticarSistema() - DIAGNÓSTICO COMPLETO!');

// 🧪 FUNÇÃO DE TESTE: Simular dados para teste
window.simularDadosParaTeste = function() {
    console.log('🧪 [TESTE] Simulando dados para teste...');
    
    const pm = window.PresencaManager;
    if (!pm) {
        console.log('❌ [TESTE] PresencaManager não encontrado');
        return;
    }
    
    // Simula seleção de dias
    pm.diasSelecionados = {
        "1": [3],
        "2": [5]
    };
    
    // Simula presenças registradas
    pm.presencasRegistradas = {
        "1": {
            "3": {
                "12345678901": { presente: true, justificativa: "", convocado: true }
            }
        },
        "2": {
            "5": {
                "12345678901": { presente: false, justificativa: "Faltou", convocado: true }
            }
        }
    };
    
    console.log('✅ [TESTE] Dados simulados adicionados');
    console.log('📊 [TESTE] diasSelecionados:', pm.diasSelecionados);
    console.log('📊 [TESTE] presencasRegistradas:', pm.presencasRegistradas);
    
    // Atualiza os calendários visuais
    Object.keys(pm.diasSelecionados).forEach(atividadeId => {
        const input = document.getElementById(`dias-atividade-${atividadeId}`);
        if (input && input._flatpickr) {
            const dias = pm.diasSelecionados[atividadeId];
            const ano = window.ano || new Date().getFullYear();
            const mes = window.mes || new Date().getMonth() + 1;
            const datas = dias.map(dia => new Date(ano, mes - 1, dia));
            input._flatpickr.setDate(datas, true);
            console.log(`📅 [TESTE] Calendário atualizado para atividade ${atividadeId}`);
        }
    });
    
    console.log('🧪 [TESTE] Agora você pode tentar "Finalizar Registro"');
};

// 🆘 FUNÇÃO DE EMERGÊNCIA PARA ESTABILIZAR CALENDÁRIO
window.estabilizarCalendario = function(atividadeId) {
    console.log('🆘 [ESTABILIZAR] Forçando estabilização do calendário para atividade:', atividadeId);
    
    if (!atividadeId) {
        console.log('❌ [ESTABILIZAR] ID da atividade é obrigatório');
        return;
    }
    
    const input = document.getElementById(`dias-atividade-${atividadeId}`);
    if (!input || !input._flatpickr) {
        console.log('❌ [ESTABILIZAR] Input ou Flatpickr não encontrado');
        return;
    }
    
    const flatpickr = input._flatpickr;
    
    // Força fechamento se estiver aberto
    if (flatpickr.isOpen) {
        console.log('🔧 [ESTABILIZAR] Fechando calendário...');
        flatpickr.close();
    }
    
    // Aguarda e reabre
    setTimeout(() => {
        console.log('🔧 [ESTABILIZAR] Reabrindo calendário...');
        flatpickr.open();
        
        // Força foco
        setTimeout(() => {
            input.focus();
            console.log('✅ [ESTABILIZAR] Calendário estabilizado');
        }, 200);
    }, 300);
    
    // Libera qualquer bloqueio de salvamento
    if (window.PresencaManager) {
        window.PresencaManager._processandoSalvamento = false;
        console.log('🔓 [ESTABILIZAR] Flag de salvamento liberada');
    }
};

// 🔧 FUNÇÃO DE DIAGNÓSTICO COMPLETO
window.diagnosticarSistema = function() {
    console.log('🔧 [DIAGNÓSTICO] ================================');
    console.log('🔧 [DIAGNÓSTICO] SISTEMA COMPLETO');
    console.log('🔧 [DIAGNÓSTICO] ================================');
    
    if (!window.PresencaManager) {
        console.log('❌ [DIAGNÓSTICO] PresencaManager não encontrado!');
        return;
    }
    
    const pm = window.PresencaManager;
    
    console.log('📊 [DIAGNÓSTICO] Estado atual:');
    console.log('   - alunosData:', pm.alunosData.length, 'alunos');
    console.log('   - presencasRegistradas:', Object.keys(pm.presencasRegistradas).length, 'atividades');
    console.log('   - diasSelecionados:', Object.keys(pm.diasSelecionados).length, 'atividades');
    console.log('   - convocadosIndividuais:', Object.keys(pm.convocadosIndividuais).length, 'alunos');
    
    console.log('📋 [DIAGNÓSTICO] Dados detalhados:');
    console.log('   presencasRegistradas:', JSON.stringify(pm.presencasRegistradas, null, 2));
    console.log('   diasSelecionados:', JSON.stringify(pm.diasSelecionados, null, 2));
    console.log('   convocadosIndividuais:', JSON.stringify(pm.convocadosIndividuais, null, 2));
    
    // Verifica formulário
    const form = document.getElementById('form-presenca');
    console.log('📝 [DIAGNÓSTICO] Formulário encontrado:', !!form);
    
    if (form) {
        const camposHidden = form.querySelectorAll('input[type="hidden"]');
        console.log('📝 [DIAGNÓSTICO] Campos hidden no formulário:', camposHidden.length);
        camposHidden.forEach(campo => {
            console.log(`   - ${campo.name}: ${campo.value.substring(0, 100)}...`);
        });
    }
    
    // Verifica calendários
    const calendarios = document.querySelectorAll('.dias-datepicker');
    console.log('📅 [DIAGNÓSTICO] Calendários encontrados:', calendarios.length);
    calendarios.forEach((input, idx) => {
        const atividadeId = input.dataset.atividade;
        const temFlatpickr = !!input._flatpickr;
        const valor = input.value;
        console.log(`   [${idx}] Atividade ${atividadeId}: Flatpickr=${temFlatpickr}, Valor="${valor}"`);
    });
    
    // 🎯 ANÁLISE DE PROBLEMAS ESPECÍFICOS
    console.log('🎯 [DIAGNÓSTICO] Análise de Problemas:');
    const problemas = [];
    
    Object.keys(pm.diasSelecionados).forEach(atividadeId => {
        const diasSelecionados = pm.diasSelecionados[atividadeId] || [];
        const presencasAtividade = pm.presencasRegistradas[atividadeId] || {};
        const nomeAtividade = pm.obterNomeAtividade ? pm.obterNomeAtividade(atividadeId) : `Atividade ${atividadeId}`;
        
        console.log(`   📋 ${nomeAtividade}:`);
        console.log(`      Dias selecionados: [${diasSelecionados.join(', ')}]`);
        
        diasSelecionados.forEach(dia => {
            const presencasDia = presencasAtividade[dia];
            if (!presencasDia || Object.keys(presencasDia).length === 0) {
                const problema = `${nomeAtividade}: Dia ${dia} selecionado mas SEM PRESENÇAS marcadas`;
                problemas.push(problema);
                console.log(`      ❌ Dia ${dia}: SEM PRESENÇAS MARCADAS`);
                console.log(`      💡 SOLUÇÃO: Clique no dia ${dia} azul no calendário para marcar presenças`);
            } else {
                console.log(`      ✅ Dia ${dia}: ${Object.keys(presencasDia).length} presenças registradas`);
            }
        });
    });
    
    if (problemas.length > 0) {
        console.log('⚠️ [DIAGNÓSTICO] PROBLEMAS ENCONTRADOS:');
        problemas.forEach((problema, idx) => {
            console.log(`   ${idx + 1}. ${problema}`);
        });
        console.log('💡 [DIAGNÓSTICO] Use resolverTravamento() para corrigir automaticamente');
    } else {
        console.log('✅ [DIAGNÓSTICO] Nenhum problema encontrado!');
    }
    
    console.log('🔧 [DIAGNÓSTICO] ================================');
    console.log('📋 [DIAGNÓSTICO] Para testar envio: window.PresencaManager.debugarFormulario()');
    console.log('📋 [DIAGNÓSTICO] Para verificar resumo: window.PresencaManager.gerarResumoFinalizacao()');
    console.log('🎯 [DIAGNÓSTICO] Para resolver problemas: resolverTravamento()');
    console.log('🔧 [DIAGNÓSTICO] ================================');
    
    return {
        problemas: problemas,
        temProblemas: problemas.length > 0,
        sugestoes: problemas.length > 0 ? ['Clique nos dias azuis dos calendários para marcar presenças'] : ['Sistema OK']
    };
};

// 🎯 FUNÇÃO PARA RESOLVER TRAVAMENTOS
window.resolverTravamento = function() {
    console.log('🎯 [RESOLVER] ================================');
    console.log('🎯 [RESOLVER] DETECTANDO E RESOLVENDO TRAVAMENTOS');
    console.log('🎯 [RESOLVER] ================================');
    
    const PM = window.PresencaManager;
    if (!PM) {
        console.log('❌ [RESOLVER] PresencaManager não encontrado');
        return false;
    }
    
    // 1. Fecha qualquer modal aberto
    const modal = document.getElementById('presencaModal');
    if (modal && modal.style.display !== 'none') {
        console.log('🚪 [RESOLVER] Fechando modal aberto...');
        PM.fecharModal();
    }
    
    // 2. Reset estado interno
    console.log('🔄 [RESOLVER] Resetando estado interno...');
    PM.atividadeAtual = null;
    PM.diaAtual = null;
    PM._processandoSalvamento = false;
    
    // 3. Verifica e corrige Flatpickr
    console.log('📅 [RESOLVER] Verificando calendários...');
    const inputs = document.querySelectorAll('.dias-datepicker');
    let calendáriosCorrigidos = 0;
    
    inputs.forEach(input => {
        if (input._flatpickr) {
            try {
                if (input._flatpickr.isOpen) {
                    input._flatpickr.close();
                    console.log(`📅 [RESOLVER] Calendário ${input.id} fechado`);
                }
                calendáriosCorrigidos++;
            } catch (error) {
                console.log(`❌ [RESOLVER] Erro no calendário ${input.id}:`, error);
            }
        }
    });
    
    // 4. Detecta dias selecionados sem presenças
    console.log('🔍 [RESOLVER] Detectando problemas específicos...');
    const problemas = [];
    
    Object.keys(PM.diasSelecionados).forEach(atividadeId => {
        const diasSelecionados = PM.diasSelecionados[atividadeId] || [];
        const presencasAtividade = PM.presencasRegistradas[atividadeId] || {};
        const nomeAtividade = PM.obterNomeAtividade ? PM.obterNomeAtividade(atividadeId) : `Atividade ${atividadeId}`;
        
        diasSelecionados.forEach(dia => {
            const presencasDia = presencasAtividade[dia];
            if (!presencasDia || Object.keys(presencasDia).length === 0) {
                problemas.push({
                    atividadeId: atividadeId,
                    dia: dia,
                    nome: nomeAtividade,
                    inputId: `dias-atividade-${atividadeId}`
                });
            }
        });
    });
    
    if (problemas.length > 0) {
        console.log('⚠️ [RESOLVER] Problemas detectados:');
        problemas.forEach((problema, idx) => {
            console.log(`   ${idx + 1}. ${problema.nome}: Dia ${problema.dia} sem presenças`);
        });
        
        console.log('💡 [RESOLVER] INSTRUÇÕES PARA RESOLVER:');
        problemas.forEach((problema, idx) => {
            console.log(`   ${idx + 1}. Clique no dia ${problema.dia} azul no calendário da atividade "${problema.nome}"`);
            console.log(`      (Input ID: ${problema.inputId})`);
        });
        
        // Destaca visualmente o primeiro problema
        if (problemas[0]) {
            const inputProblema = document.getElementById(problemas[0].inputId);
            if (inputProblema) {
                inputProblema.style.border = '3px solid #ff4444';
                inputProblema.style.animation = 'pulse 1s infinite';
                console.log(`🎯 [RESOLVER] Destacando visualmente o calendário "${problemas[0].inputId}"`);
                
                // Remove destaque após 10 segundos
                setTimeout(() => {
                    inputProblema.style.border = '';
                    inputProblema.style.animation = '';
                }, 10000);
            }
        }
    } else {
        console.log('✅ [RESOLVER] Nenhum problema detectado');
    }
    
    console.log('🎯 [RESOLVER] ================================');
    console.log(`✅ [RESOLVER] Sistema estabilizado (${calendáriosCorrigidos} calendários processados)`);
    console.log(`📊 [RESOLVER] Problemas detectados: ${problemas.length}`);
    console.log('🎯 [RESOLVER] ================================');
    
    return {
        sucesso: true,
        problemas: problemas,
        calendáriosCorrigidos: calendáriosCorrigidos
    };
};

// 🔍 FUNÇÃO PARA VERIFICAR SE OS DADOS FORAM REALMENTE ENVIADOS
window.verificarEnvioRealizado = function() {
    console.log('🔍 [VERIFICAR] ================================');
    console.log('🔍 [VERIFICAR] VERIFICANDO SE DADOS FORAM ENVIADOS');
    console.log('🔍 [VERIFICAR] ================================');
    
    // Verifica se há mensagem de erro na página
    const mensagemErro = document.querySelector('.alert-warning');
    const temErroPresenca = mensagemErro && mensagemErro.textContent.includes('Nenhuma presença foi registrada');
    
    if (temErroPresenca) {
        console.log('❌ [VERIFICAR] CONFIRMADO: Dados NÃO foram gravados no Django');
        console.log('❌ [VERIFICAR] Mensagem de erro encontrada:', mensagemErro.textContent.trim());
        
        // Verifica se há estado no localStorage
        const estadoSalvo = localStorage.getItem('presenca_estado_backup');
        if (estadoSalvo) {
            console.log('💾 [VERIFICAR] Estado encontrado no localStorage');
            const estado = JSON.parse(estadoSalvo);
            console.log('📊 [VERIFICAR] Dados no localStorage:');
            console.log('   presencasRegistradas:', Object.keys(estado.presencasRegistradas || {}).length, 'atividades');
            console.log('   diasSelecionados:', Object.keys(estado.diasSelecionados || {}).length, 'atividades');
            console.log('   convocadosIndividuais:', Object.keys(estado.convocadosIndividuais || {}).length, 'alunos');
            
            console.log('🔄 [VERIFICAR] Recuperando estado automaticamente...');
            window.PresencaManager.recuperarEstadoAposReload();
            
            return {
                enviadoComSucesso: false,
                problemaDetectado: 'Dados não foram gravados no Django',
                estadoRecuperado: true,
                proximoPasso: 'Os dados foram recuperados. Verifique os calendários e tente enviar novamente.'
            };
        } else {
            return {
                enviadoComSucesso: false,
                problemaDetectado: 'Dados não foram gravados no Django e não há backup local',
                estadoRecuperado: false,
                proximoPasso: 'Você precisará selecionar os dias e marcar as presenças novamente.'
            };
        }
    } else {
        console.log('✅ [VERIFICAR] Nenhuma mensagem de erro encontrada');
        console.log('✅ [VERIFICAR] Possivelmente os dados foram enviados com sucesso');
        
        // Limpa qualquer estado salvo
        localStorage.removeItem('presenca_estado_backup');
        
        return {
            enviadoComSucesso: true,
            problemaDetectado: null,
            proximoPasso: 'Dados enviados com sucesso!'
        };
    }
    
    console.log('🔍 [VERIFICAR] ================================');
};

// 🧪 FUNÇÃO PARA TESTAR DADOS ANTES DO ENVIO
window.testarDadosParaEnvio = function() {
    console.log('🧪 [TESTE] ================================');
    console.log('🧪 [TESTE] TESTANDO DADOS PARA ENVIO');
    console.log('🧪 [TESTE] ================================');
    
    const PM = window.PresencaManager;
    if (!PM) {
        console.log('❌ [TESTE] PresencaManager não encontrado');
        return false;
    }
    
    // Simula a adição de dados ao formulário
    const resultado = PM.adicionarDadosAoFormulario();
    
    // Verifica o formulário
    const form = document.getElementById('form-presenca');
    if (!form) {
        console.log('❌ [TESTE] Formulário não encontrado');
        return false;
    }
    
    const formData = new FormData(form);
    const campos = {};
    
    for (let [key, value] of formData.entries()) {
        campos[key] = value;
    }
    
    console.log('📊 [TESTE] Campos do formulário:');
    Object.keys(campos).forEach(key => {
        if (key.includes('json')) {
            console.log(`   ${key}:`, JSON.parse(campos[key]));
        } else {
            console.log(`   ${key}: ${campos[key]}`);
        }
    });
    
    // Verifica se tem dados essenciais
    const temPresencas = campos.presencas_json && campos.presencas_json !== '{}';
    const temDias = campos.dias_json && campos.dias_json !== '{}';
    
    console.log('✅ [TESTE] Verificação:');
    console.log(`   Tem presenças: ${temPresencas}`);
    console.log(`   Tem dias: ${temDias}`);
    console.log(`   Pronto para envio: ${temPresencas && temDias}`);
    
    console.log('🧪 [TESTE] ================================');
    
    return {
        formEncontrado: true,
        dadosAdicionados: resultado,
        temPresencas: temPresencas,
        temDias: temDias,
        prontoParaEnvio: temPresencas && temDias,
        campos: campos
    };
};

/**
 * 🔍 ANÁLISE REVERSA - TESTE DE ENVIO ESPECÍFICO
 */
function testarEnvioEspecifico() {
    console.log('🔍 ANÁLISE REVERSA - TESTE DE ENVIO ESPECÍFICO');
    console.log('=' + '='.repeat(49));
    
    const PM = window.PresencaManager;
    if (!PM) {
        console.error('❌ PresencaManager não encontrado');
        return;
    }
    
    // 1️⃣ Verificar dados atuais
    console.log('📊 DADOS ATUAIS:');
    console.log('presencasRegistradas:', JSON.stringify(PM.presencasRegistradas, null, 2));
    console.log('convocadosIndividuais:', JSON.stringify(PM.convocadosIndividuais, null, 2));
    console.log('diasSelecionados:', JSON.stringify(PM.diasSelecionados, null, 2));
    
    // 2️⃣ Simular dados se vazio
    if (Object.keys(PM.presencasRegistradas).length === 0) {
        console.log('⚠️ Nenhuma presença registrada, simulando dados...');
        PM.presencasRegistradas = {
            "1": {
                "3": {
                    "12345678901": {
                        "presente": true,
                        "convocado": true
                    }
                }
            }
        };
        console.log('✅ Dados simulados adicionados');
    }
    
    // 3️⃣ Testar formulário
    const form = document.getElementById('form-presenca');
    if (!form) {
        console.error('❌ Formulário não encontrado');
        return;
    }
    
    // 4️⃣ Adicionar dados ao formulário
    PM.adicionarDadosAoFormulario();
    
    // 5️⃣ Verificar FormData
    const formData = new FormData(form);
    console.log('📝 DADOS DO FORMULÁRIO:');
    for (let [key, value] of formData.entries()) {
        console.log(`   ${key}: ${value}`);
        if (key === 'presencas_json') {
            try {
                const parsed = JSON.parse(value);
                console.log(`   ${key} (parsed):`, parsed);
            } catch (e) {
                console.error(`   ❌ Erro ao parsear ${key}:`, e);
            }
        }
    }
    
    // 6️⃣ Enviar para Django
    console.log('🚀 ENVIANDO PARA DJANGO...');
    
    fetch('/presencas/registrar-presenca/dias-atividades/ajax/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('✅ RESPOSTA DO DJANGO:', data);
        if (data.success) {
            console.log('🎉 SUCESSO!');
        } else {
            console.log('❌ FALHA:', data.message);
        }
    })
    .catch(error => {
        console.error('❌ ERRO DE REDE:', error);
    });
}

// Expor função globalmente
window.testarEnvioEspecifico = testarEnvioEspecifico;

