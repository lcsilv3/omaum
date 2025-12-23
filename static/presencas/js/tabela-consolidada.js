/**
 * Sistema JavaScript Interativo para Tabela de Presenças Consolidada
 * Funcionalidades Excel-like para edição in-line e navegação horizontal
 * 
 * @author Agente 9 - Sistema Omaum
 * @version 1.0.0
 */

class TabelaConsolidada {
    constructor(options = {}) {
        // Configurações padrão
        this.config = {
            selectorTabela: '.tabela-consolidada',
            selectorControles: '.controles-navegacao',
            urlAtualizar: '/presencas/api/atualizar-presencas/',
            urlEstatisticas: '/presencas/api/calcular-estatisticas/',
            urlValidar: '/presencas/api/validar-dados/',
            debounceDelay: 1000,
            maxAtividadesVisiveis: 8,
            autoSave: true,
            tooltipDelay: 500,
            ...options
        };

        // Estado da aplicação
        this.estado = {
            editandoCelula: null,
            alteracoesPendentes: new Map(),
            atividadeAtual: 0,
            totalAtividades: 0,
            loading: false,
            errorCount: 0,
            undoStack: [],
            redoStack: []
        };

        // Cache e performance
        this.cache = {
            alunos: new Map(),
            atividades: new Map(),
            estatisticas: new Map()
        };

        // Timers
        this.timers = {
            autoSave: null,
            tooltip: null,
            debounce: null
        };

        this.init();
    }

    /**
     * Inicialização da classe
     */
    init() {
        try {
            this.bindEvents();
            this.configurarNavegacao();
            this.carregarDadosIniciais();
            this.configurarAtalhosTeclado();
            this.iniciarAutoSave();
            
            console.log('TabelaConsolidada: Inicializada com sucesso');
        } catch (error) {
            console.error('TabelaConsolidada: Erro na inicialização:', error);
            this.mostrarErro('Erro ao inicializar sistema de presenças');
        }
    }

    /**
     * Configuração de event listeners
     */
    bindEvents() {
        const tabela = document.querySelector(this.config.selectorTabela);
        if (!tabela) {
            throw new Error('Tabela não encontrada');
        }

        // Event delegation para performance
        tabela.addEventListener('dblclick', this.handleDuploClick.bind(this));
        tabela.addEventListener('keydown', this.handleKeyDown.bind(this));
        tabela.addEventListener('blur', this.handleBlur.bind(this), true);
        tabela.addEventListener('input', this.handleInput.bind(this));
        tabela.addEventListener('mouseover', this.handleMouseOver.bind(this));
        tabela.addEventListener('mouseout', this.handleMouseOut.bind(this));

        // Controles de navegação
        const controles = document.querySelector(this.config.selectorControles);
        if (controles) {
            controles.addEventListener('click', this.handleNavegacao.bind(this));
        }

        // Botões de ação
        this.bindActionButtons();

        // Resize da janela
        window.addEventListener('resize', this.debounce(this.ajustarLayout.bind(this), 250));
    }

    /**
     * Configuração dos botões de ação
     */
    bindActionButtons() {
        // Salvar manual
        const btnSalvar = document.querySelector('.btn-salvar');
        if (btnSalvar) {
            btnSalvar.addEventListener('click', this.salvarManual.bind(this));
        }

        // Recalcular estatísticas
        const btnRecalcular = document.querySelector('.btn-recalcular');
        if (btnRecalcular) {
            btnRecalcular.addEventListener('click', this.recalcularEstatisticas.bind(this));
        }

        // Busca rápida
        const inputBusca = document.querySelector('.busca-rapida');
        if (inputBusca) {
            inputBusca.addEventListener('input', 
                this.debounce(this.buscarAluno.bind(this), 300)
            );
        }
    }

    /**
     * Configuração de atalhos de teclado
     */
    configurarAtalhosTeclado() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+S - Salvar
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                this.salvarManual();
                return;
            }

            // Ctrl+Z - Undo
            if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
                e.preventDefault();
                this.undo();
                return;
            }

            // Ctrl+Shift+Z ou Ctrl+Y - Redo
            if ((e.ctrlKey && e.shiftKey && e.key === 'Z') || (e.ctrlKey && e.key === 'y')) {
                e.preventDefault();
                this.redo();
                return;
            }

            // F2 - Editar célula selecionada
            if (e.key === 'F2') {
                e.preventDefault();
                const celulaSelecionada = document.querySelector('.celula-selecionada');
                if (celulaSelecionada) {
                    this.editarCelula(celulaSelecionada);
                }
                return;
            }

            // Escape - Cancelar edição
            if (e.key === 'Escape' && this.estado.editandoCelula) {
                e.preventDefault();
                this.cancelarEdicao();
                return;
            }

            // Setas para navegação
            if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
                this.navegarCelulas(e);
            }
        });
    }

    /**
     * Handle duplo clique para edição
     */
    handleDuploClick(e) {
        const celula = e.target.closest('.celula-editavel');
        if (celula && !this.estado.editandoCelula) {
            e.preventDefault();
            this.editarCelula(celula);
        }
    }

    /**
     * Handle teclas pressionadas na tabela
     */
    handleKeyDown(e) {
        if (this.estado.editandoCelula) {
            const input = this.estado.editandoCelula.querySelector('input');
            if (!input) return;

            switch (e.key) {
                case 'Enter':
                    e.preventDefault();
                    this.confirmarEdicao();
                    break;
                case 'Escape':
                    e.preventDefault();
                    this.cancelarEdicao();
                    break;
                case 'Tab':
                    e.preventDefault();
                    this.confirmarEdicao();
                    this.navegarProximaCelula(e.shiftKey);
                    break;
            }
        }
    }

    /**
     * Handle perda de foco
     */
    handleBlur(e) {
        if (this.estado.editandoCelula && 
            !this.estado.editandoCelula.contains(e.target) &&
            !e.relatedTarget?.closest('.tooltip')) {
            
            this.confirmarEdicao();
        }
    }

    /**
     * Handle input changes
     */
    handleInput(e) {
        if (this.estado.editandoCelula && e.target.tagName === 'INPUT') {
            this.validarInput(e.target);
        }
    }

    /**
     * Handle mouse over para tooltips
     */
    handleMouseOver(e) {
        const elemento = e.target.closest('[data-tooltip]');
        if (elemento) {
            this.clearTimeout('tooltip');
            this.timers.tooltip = setTimeout(() => {
                this.mostrarTooltip(elemento);
            }, this.config.tooltipDelay);
        }
    }

    /**
     * Handle mouse out para esconder tooltips
     */
    handleMouseOut(e) {
        const elemento = e.target.closest('[data-tooltip]');
        if (elemento) {
            this.clearTimeout('tooltip');
            this.esconderTooltip();
        }
    }

    /**
     * Ativa edição in-line de uma célula
     */
    editarCelula(celula) {
        if (this.estado.editandoCelula) {
            this.confirmarEdicao();
        }

        if (!celula.classList.contains('celula-editavel')) {
            return;
        }

        try {
            const valorAtual = celula.textContent.trim();
            const tipo = celula.dataset.tipo || 'text';
            
            // Criar input baseado no tipo
            const input = this.criarInputEdicao(tipo, valorAtual);
            
            // Salvar estado original
            celula.dataset.valorOriginal = valorAtual;
            
            // Substituir conteúdo
            celula.innerHTML = '';
            celula.appendChild(input);
            celula.classList.add('editando');
            
            // Focar e selecionar
            input.focus();
            if (input.type === 'text') {
                input.select();
            }
            
            this.estado.editandoCelula = celula;
            
            console.log('Editando célula:', celula.dataset);
        } catch (error) {
            console.error('Erro ao editar célula:', error);
            this.mostrarErro('Erro ao ativar edição');
        }
    }

    /**
     * Cria input apropriado para edição
     */
    criarInputEdicao(tipo, valor) {
        const input = document.createElement('input');
        
        switch (tipo) {
            case 'number':
                input.type = 'number';
                input.min = '0';
                input.max = '1';
                input.step = '0.01';
                input.value = parseFloat(valor) || 0;
                break;
            case 'presence':
                input.type = 'text';
                input.value = valor;
                input.pattern = '[PpFfJj]';
                input.maxLength = '1';
                break;
            default:
                input.type = 'text';
                input.value = valor;
        }
        
        input.className = 'input-edicao';
        return input;
    }

    /**
     * Confirma edição atual
     */
    confirmarEdicao() {
        if (!this.estado.editandoCelula) return;

        const celula = this.estado.editandoCelula;
        const input = celula.querySelector('input');
        
        if (!input) {
            this.cancelarEdicao();
            return;
        }

        try {
            const novoValor = input.value.trim();
            const valorOriginal = celula.dataset.valorOriginal;
            
            // Validar valor
            if (!this.validarValor(novoValor, celula.dataset.tipo)) {
                this.mostrarErro('Valor inválido');
                input.focus();
                return;
            }
            
            // Verificar se houve mudança
            if (novoValor !== valorOriginal) {
                // Salvar para undo
                this.salvarEstadoUndo(celula, valorOriginal, novoValor);
                
                // Atualizar célula
                this.atualizarCelula(celula, novoValor);
                
                // Marcar para salvamento
                this.marcarAlteracao(celula);
            }
            
            this.finalizarEdicao(celula, novoValor);
            
        } catch (error) {
            console.error('Erro ao confirmar edição:', error);
            this.cancelarEdicao();
        }
    }

    /**
     * Cancela edição atual
     */
    cancelarEdicao() {
        if (!this.estado.editandoCelula) return;

        const celula = this.estado.editandoCelula;
        const valorOriginal = celula.dataset.valorOriginal || '';
        
        this.finalizarEdicao(celula, valorOriginal);
    }

    /**
     * Finaliza processo de edição
     */
    finalizarEdicao(celula, valor) {
        celula.textContent = valor;
        celula.classList.remove('editando');
        delete celula.dataset.valorOriginal;
        
        this.estado.editandoCelula = null;
    }

    /**
     * Atualiza célula com novo valor
     */
    atualizarCelula(celula, novoValor) {
        const alunoId = celula.dataset.alunoId;
        const atividadeId = celula.dataset.atividadeId;
        const tipo = celula.dataset.tipo;
        
        // Atualizar display
        if (tipo === 'presence') {
            celula.textContent = novoValor.toUpperCase();
            celula.className = `celula-editavel celula-${this.getClassePresenca(novoValor)}`;
        } else {
            celula.textContent = novoValor;
        }
        
        // Recalcular percentuais se necessário
        if (tipo === 'presence') {
            this.recalcularPercentualAluno(alunoId);
        }
    }

    /**
     * Marca alteração para salvamento
     */
    marcarAlteracao(celula) {
        const key = `${celula.dataset.alunoId}_${celula.dataset.atividadeId}`;
        const alteracao = {
            aluno_id: parseInt(celula.dataset.alunoId),
            turma_id: parseInt(celula.dataset.turmaId),
            atividade_id: parseInt(celula.dataset.atividadeId),
            periodo: celula.dataset.periodo,
            valor: celula.textContent.trim(),
            tipo: celula.dataset.tipo,
            timestamp: Date.now()
        };
        
        this.estado.alteracoesPendentes.set(key, alteracao);
        
        // Marcar visualmente
        celula.classList.add('alterado');
        
        // Auto-save se habilitado
        if (this.config.autoSave) {
            this.agendarAutoSave();
        }
        
        this.atualizarContadorAlteracoes();
    }

    /**
     * Navegação entre células
     */
    navegarCelulas(e) {
        const celulaAtual = document.activeElement.closest('.celula-editavel') || 
                           document.querySelector('.celula-selecionada');
        
        if (!celulaAtual) return;

        const linha = celulaAtual.closest('tr');
        const coluna = Array.from(linha.children).indexOf(celulaAtual);
        
        let proximaCelula = null;
        
        switch (e.key) {
            case 'ArrowLeft':
                proximaCelula = celulaAtual.previousElementSibling;
                break;
            case 'ArrowRight':
                proximaCelula = celulaAtual.nextElementSibling;
                break;
            case 'ArrowUp':
                const linhaAnterior = linha.previousElementSibling;
                if (linhaAnterior) {
                    proximaCelula = linhaAnterior.children[coluna];
                }
                break;
            case 'ArrowDown':
                const proximaLinha = linha.nextElementSibling;
                if (proximaLinha) {
                    proximaCelula = proximaLinha.children[coluna];
                }
                break;
        }
        
        if (proximaCelula && proximaCelula.classList.contains('celula-editavel')) {
            e.preventDefault();
            this.selecionarCelula(proximaCelula);
        }
    }

    /**
     * Seleciona uma célula
     */
    selecionarCelula(celula) {
        document.querySelectorAll('.celula-selecionada').forEach(c => {
            c.classList.remove('celula-selecionada');
        });
        
        celula.classList.add('celula-selecionada');
        celula.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    /**
     * Navegação horizontal entre atividades
     */
    configurarNavegacao() {
        const tabela = document.querySelector(this.config.selectorTabela);
        if (!tabela) return;

        const atividadesColunas = tabela.querySelectorAll('th[data-atividade-id]');
        this.estado.totalAtividades = atividadesColunas.length;
        
        this.atualizarIndicadoresNavegacao();
    }

    /**
     * Handle cliques nos controles de navegação
     */
    handleNavegacao(e) {
        const btn = e.target.closest('.btn-navegacao');
        if (!btn) return;

        e.preventDefault();
        
        const acao = btn.dataset.acao;
        
        switch (acao) {
            case 'anterior':
                this.navegarAnterior();
                break;
            case 'proximo':
                this.navegarProximo();
                break;
            case 'primeira':
                this.navegarPrimeira();
                break;
            case 'ultima':
                this.navegarUltima();
                break;
        }
    }

    /**
     * Navegar para atividade anterior
     */
    navegarAnterior() {
        if (this.estado.atividadeAtual > 0) {
            this.estado.atividadeAtual--;
            this.atualizarVisibilidadeAtividades();
        }
    }

    /**
     * Navegar para próxima atividade
     */
    navegarProximo() {
        const maxInicio = Math.max(0, this.estado.totalAtividades - this.config.maxAtividadesVisiveis);
        if (this.estado.atividadeAtual < maxInicio) {
            this.estado.atividadeAtual++;
            this.atualizarVisibilidadeAtividades();
        }
    }

    /**
     * Navegar para primeira atividade
     */
    navegarPrimeira() {
        this.estado.atividadeAtual = 0;
        this.atualizarVisibilidadeAtividades();
    }

    /**
     * Navegar para última atividade
     */
    navegarUltima() {
        this.estado.atividadeAtual = Math.max(0, this.estado.totalAtividades - this.config.maxAtividadesVisiveis);
        this.atualizarVisibilidadeAtividades();
    }

    /**
     * Atualiza visibilidade das colunas de atividades
     */
    atualizarVisibilidadeAtividades() {
        const tabela = document.querySelector(this.config.selectorTabela);
        if (!tabela) return;

        const colunas = tabela.querySelectorAll('th[data-atividade-id], td[data-atividade-id]');
        
        colunas.forEach((coluna, index) => {
            const atividadeIndex = parseInt(coluna.dataset.atividadeIndex || index);
            const visivel = atividadeIndex >= this.estado.atividadeAtual && 
                          atividadeIndex < (this.estado.atividadeAtual + this.config.maxAtividadesVisiveis);
            
            coluna.style.display = visivel ? '' : 'none';
        });
        
        this.atualizarIndicadoresNavegacao();
        this.animarTransicao();
    }

    /**
     * Atualiza indicadores de navegação
     */
    atualizarIndicadoresNavegacao() {
        const indicador = document.querySelector('.indicador-posicao');
        if (indicador) {
            const inicio = this.estado.atividadeAtual + 1;
            const fim = Math.min(this.estado.atividadeAtual + this.config.maxAtividadesVisiveis, 
                                this.estado.totalAtividades);
            indicador.textContent = `${inicio}-${fim} de ${this.estado.totalAtividades}`;
        }

        // Habilitar/desabilitar botões
        const btnAnterior = document.querySelector('.btn-navegacao[data-acao="anterior"]');
        const btnProximo = document.querySelector('.btn-navegacao[data-acao="proximo"]');
        
        if (btnAnterior) {
            btnAnterior.disabled = this.estado.atividadeAtual === 0;
        }
        
        if (btnProximo) {
            const maxInicio = Math.max(0, this.estado.totalAtividades - this.config.maxAtividadesVisiveis);
            btnProximo.disabled = this.estado.atividadeAtual >= maxInicio;
        }
    }

    /**
     * Animação de transição suave
     */
    animarTransicao() {
        const tabela = document.querySelector(this.config.selectorTabela);
        if (tabela) {
            tabela.style.transition = 'all 0.3s ease';
            setTimeout(() => {
                tabela.style.transition = '';
            }, 300);
        }
    }

    /**
     * Salvamento automático
     */
    iniciarAutoSave() {
        if (!this.config.autoSave) return;
        
        this.timers.autoSave = setInterval(() => {
            if (this.estado.alteracoesPendentes.size > 0) {
                this.salvarAlteracoes();
            }
        }, this.config.debounceDelay * 3);
    }

    /**
     * Agenda auto-save com debounce
     */
    agendarAutoSave() {
        this.clearTimeout('debounce');
        this.timers.debounce = setTimeout(() => {
            this.salvarAlteracoes();
        }, this.config.debounceDelay);
    }

    /**
     * Salvamento manual
     */
    async salvarManual() {
        if (this.estado.alteracoesPendentes.size === 0) {
            this.mostrarMensagem('Nenhuma alteração pendente', 'info');
            return;
        }
        
        await this.salvarAlteracoes();
    }

    /**
     * Salva alterações no backend
     */
    async salvarAlteracoes() {
        if (this.estado.loading || this.estado.alteracoesPendentes.size === 0) {
            return;
        }

        this.setLoading(true);
        
        try {
            const alteracoes = Array.from(this.estado.alteracoesPendentes.values());
            
            const response = await this.fetchAPI(this.config.urlAtualizar, {
                method: 'POST',
                body: JSON.stringify({
                    presencas: alteracoes,
                    batch_id: this.gerarBatchId()
                })
            });

            if (response.success) {
                this.processarSucessoSalvamento(response);
            } else {
                this.processarErroSalvamento(response);
            }
            
        } catch (error) {
            console.error('Erro ao salvar alterações:', error);
            this.mostrarErro('Erro de conexão ao salvar');
            this.estado.errorCount++;
        } finally {
            this.setLoading(false);
        }
    }

    /**
     * Processa sucesso no salvamento
     */
    processarSucessoSalvamento(response) {
        const salvos = response.data?.presencas_atualizadas || [];
        
        // Limpar alterações salvas
        salvos.forEach(presenca => {
            const key = `${presenca.aluno_id}_${presenca.atividade_id}`;
            this.estado.alteracoesPendentes.delete(key);
        });
        
        // Remover marcação visual
        document.querySelectorAll('.alterado').forEach(celula => {
            celula.classList.remove('alterado');
        });
        
        this.mostrarMensagem(`${salvos.length} alterações salvas com sucesso`, 'success');
        this.atualizarContadorAlteracoes();
        
        // Recalcular estatísticas se necessário
        if (response.data?.recalcular_estatisticas) {
            this.recalcularEstatisticas();
        }
    }

    /**
     * Processa erro no salvamento
     */
    processarErroSalvamento(response) {
        const erros = response.errors || [];
        const mensagem = response.message || 'Erro desconhecido';
        
        console.error('Erro no salvamento:', erros);
        this.mostrarErro(`Erro ao salvar: ${mensagem}`);
        
        // Marcar itens com erro
        erros.forEach(erro => {
            if (erro.aluno_id && erro.atividade_id) {
                const celula = document.querySelector(
                    `[data-aluno-id="${erro.aluno_id}"][data-atividade-id="${erro.atividade_id}"]`
                );
                if (celula) {
                    celula.classList.add('erro-salvamento');
                }
            }
        });
    }

    /**
     * Recalcula estatísticas do aluno
     */
    recalcularPercentualAluno(alunoId) {
        const linha = document.querySelector(`tr[data-aluno-id="${alunoId}"]`);
        if (!linha) return;

        const celulasPresenca = linha.querySelectorAll('.celula-editavel[data-tipo="presence"]');
        let presentes = 0;
        let total = 0;

        celulasPresenca.forEach(celula => {
            const valor = celula.textContent.trim().toUpperCase();
            if (valor && valor !== '-') {
                total++;
                if (valor === 'P') {
                    presentes++;
                }
            }
        });

        const percentual = total > 0 ? ((presentes / total) * 100).toFixed(1) : '0.0';
        
        const celulaPercentual = linha.querySelector('.celula-percentual');
        if (celulaPercentual) {
            celulaPercentual.textContent = `${percentual}%`;
            
            // Atualizar classe baseada no percentual
            const valor = parseFloat(percentual);
            celulaPercentual.className = 'celula-percentual';
            if (valor >= 75) {
                celulaPercentual.classList.add('alta');
            } else if (valor >= 50) {
                celulaPercentual.classList.add('media');
            } else {
                celulaPercentual.classList.add('baixa');
            }
        }
    }

    /**
     * Recalcula todas as estatísticas
     */
    async recalcularEstatisticas() {
        if (this.estado.loading) return;
        
        this.setLoading(true);
        
        try {
            const turmaId = document.querySelector('[data-turma-id]')?.dataset.turmaId;
            
            const response = await this.fetchAPI(this.config.urlEstatisticas, {
                method: 'POST',
                body: JSON.stringify({
                    turma_id: parseInt(turmaId)
                })
            });

            if (response.success) {
                this.atualizarEstatisticasDisplay(response.data);
                this.mostrarMensagem('Estatísticas recalculadas', 'success');
            } else {
                this.mostrarErro('Erro ao recalcular estatísticas');
            }
            
        } catch (error) {
            console.error('Erro ao recalcular estatísticas:', error);
            this.mostrarErro('Erro de conexão');
        } finally {
            this.setLoading(false);
        }
    }

    /**
     * Atualiza display das estatísticas
     */
    atualizarEstatisticasDisplay(dados) {
        // Atualizar percentuais individuais
        if (dados.alunos) {
            dados.alunos.forEach(aluno => {
                const linha = document.querySelector(`tr[data-aluno-id="${aluno.id}"]`);
                if (linha) {
                    const celulaPercentual = linha.querySelector('.celula-percentual');
                    if (celulaPercentual) {
                        celulaPercentual.textContent = `${aluno.percentual}%`;
                    }
                }
            });
        }

        // Atualizar estatísticas gerais
        if (dados.estatisticas_gerais) {
            const stats = dados.estatisticas_gerais;
            
            const mediaGeral = document.querySelector('.media-geral');
            if (mediaGeral) {
                mediaGeral.textContent = `${stats.media_presenca}%`;
            }
            
            const totalAlunos = document.querySelector('.total-alunos');
            if (totalAlunos) {
                totalAlunos.textContent = stats.total_alunos;
            }
        }
    }

    /**
     * Sistema de tooltips dinâmicos
     */
    mostrarTooltip(elemento) {
        const conteudo = this.gerarConteudoTooltip(elemento);
        if (!conteudo) return;

        // Remover tooltip existente
        this.esconderTooltip();

        // Criar novo tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.innerHTML = conteudo;
        
        document.body.appendChild(tooltip);
        
        // Posicionar tooltip
        this.posicionarTooltip(tooltip, elemento);
        
        // Animar entrada
        setTimeout(() => {
            tooltip.classList.add('visivel');
        }, 10);
    }

    /**
     * Gera conteúdo do tooltip
     */
    gerarConteudoTooltip(elemento) {
        const tipo = elemento.dataset.tooltip;
        
        switch (tipo) {
            case 'aluno':
                return this.tooltipAluno(elemento);
            case 'atividade':
                return this.tooltipAtividade(elemento);
            case 'estatistica':
                return this.tooltipEstatistica(elemento);
            default:
                return elemento.dataset.tooltipContent || null;
        }
    }

    /**
     * Tooltip para informações do aluno
     */
    tooltipAluno(elemento) {
        const alunoId = elemento.dataset.alunoId;
        const nome = elemento.textContent.trim();
        
        return `
            <div class="tooltip-header">
                <strong>${nome}</strong>
            </div>
            <div class="tooltip-body">
                <p>ID: ${alunoId}</p>
                <p>Duplo-clique para editar</p>
                <p>F2 para editar selecionado</p>
            </div>
        `;
    }

    /**
     * Tooltip para informações da atividade
     */
    tooltipAtividade(elemento) {
        const atividadeId = elemento.dataset.atividadeId;
        const nome = elemento.textContent.trim();
        
        return `
            <div class="tooltip-header">
                <strong>${nome}</strong>
            </div>
            <div class="tooltip-body">
                <p>ID da Atividade: ${atividadeId}</p>
                <p>Use P (Presente), F (Falta), J (Justificada)</p>
            </div>
        `;
    }

    /**
     * Posiciona tooltip na tela
     */
    posicionarTooltip(tooltip, elemento) {
        const rect = elemento.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();
        
        let top = rect.bottom + 10;
        let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
        
        // Ajustar se sair da tela
        if (left < 10) left = 10;
        if (left + tooltipRect.width > window.innerWidth - 10) {
            left = window.innerWidth - tooltipRect.width - 10;
        }
        
        if (top + tooltipRect.height > window.innerHeight - 10) {
            top = rect.top - tooltipRect.height - 10;
        }
        
        tooltip.style.top = `${top}px`;
        tooltip.style.left = `${left}px`;
    }

    /**
     * Esconde tooltip atual
     */
    esconderTooltip() {
        const tooltipExistente = document.querySelector('.tooltip');
        if (tooltipExistente) {
            tooltipExistente.remove();
        }
    }

    /**
     * Busca rápida de alunos
     */
    buscarAluno(e) {
        const termo = e.target.value.toLowerCase().trim();
        
        if (termo.length < 2) {
            this.mostrarTodosAlunos();
            return;
        }

        const linhas = document.querySelectorAll('tbody tr[data-aluno-id]');
        let encontrados = 0;

        linhas.forEach(linha => {
            const nomeAluno = linha.querySelector('.nome-aluno')?.textContent.toLowerCase() || '';
            const visivel = nomeAluno.includes(termo);
            
            linha.style.display = visivel ? '' : 'none';
            if (visivel) encontrados++;
        });

        this.atualizarResultadoBusca(encontrados, termo);
    }

    /**
     * Mostra todos os alunos (limpa busca)
     */
    mostrarTodosAlunos() {
        document.querySelectorAll('tbody tr[data-aluno-id]').forEach(linha => {
            linha.style.display = '';
        });
        this.atualizarResultadoBusca(null);
    }

    /**
     * Atualiza contador de resultados da busca
     */
    atualizarResultadoBusca(encontrados, termo = '') {
        const contador = document.querySelector('.contador-busca');
        if (contador) {
            if (encontrados !== null) {
                contador.textContent = `${encontrados} resultado(s) para "${termo}"`;
                contador.style.display = 'block';
            } else {
                contador.style.display = 'none';
            }
        }
    }

    /**
     * Sistema de Undo/Redo
     */
    salvarEstadoUndo(celula, valorAntigo, valorNovo) {
        const estado = {
            celula: {
                alunoId: celula.dataset.alunoId,
                atividadeId: celula.dataset.atividadeId,
                tipo: celula.dataset.tipo
            },
            valorAntigo,
            valorNovo,
            timestamp: Date.now()
        };
        
        this.estado.undoStack.push(estado);
        
        // Limitar tamanho do stack
        if (this.estado.undoStack.length > 50) {
            this.estado.undoStack.shift();
        }
        
        // Limpar redo stack
        this.estado.redoStack = [];
    }

    /**
     * Desfazer última ação
     */
    undo() {
        if (this.estado.undoStack.length === 0) return;
        
        const estado = this.estado.undoStack.pop();
        const celula = this.encontrarCelula(estado.celula);
        
        if (celula) {
            // Salvar para redo
            this.estado.redoStack.push(estado);
            
            // Reverter valor
            this.atualizarCelula(celula, estado.valorAntigo);
            this.marcarAlteracao(celula);
            
            this.mostrarMensagem('Ação desfeita', 'info');
        }
    }

    /**
     * Refazer última ação desfeita
     */
    redo() {
        if (this.estado.redoStack.length === 0) return;
        
        const estado = this.estado.redoStack.pop();
        const celula = this.encontrarCelula(estado.celula);
        
        if (celula) {
            // Salvar para undo novamente
            this.estado.undoStack.push(estado);
            
            // Aplicar valor
            this.atualizarCelula(celula, estado.valorNovo);
            this.marcarAlteracao(celula);
            
            this.mostrarMensagem('Ação refeita', 'info');
        }
    }

    /**
     * Encontra célula pelos dados
     */
    encontrarCelula(dados) {
        return document.querySelector(
            `[data-aluno-id="${dados.alunoId}"][data-atividade-id="${dados.atividadeId}"][data-tipo="${dados.tipo}"]`
        );
    }

    /**
     * Validação de valores
     */
    validarValor(valor, tipo) {
        switch (tipo) {
            case 'presence':
                return /^[PpFfJj]?$/.test(valor);
            case 'number':
                const num = parseFloat(valor);
                return !isNaN(num) && num >= 0 && num <= 1;
            default:
                return true;
        }
    }

    /**
     * Validação em tempo real do input
     */
    validarInput(input) {
        const valor = input.value;
        const tipo = input.closest('.celula-editavel')?.dataset.tipo;
        
        const valido = this.validarValor(valor, tipo);
        
        input.classList.toggle('invalido', !valido);
        
        if (!valido) {
            input.title = 'Valor inválido';
        } else {
            input.title = '';
        }
        
        return valido;
    }

    /**
     * Carrega dados iniciais
     */
    async carregarDadosIniciais() {
        try {
            // Cachear informações dos alunos
            document.querySelectorAll('tr[data-aluno-id]').forEach(linha => {
                const alunoId = linha.dataset.alunoId;
                const nome = linha.querySelector('.nome-aluno')?.textContent.trim();
                this.cache.alunos.set(alunoId, { nome });
            });

            // Cachear informações das atividades
            document.querySelectorAll('th[data-atividade-id]').forEach(header => {
                const atividadeId = header.dataset.atividadeId;
                const nome = header.textContent.trim();
                this.cache.atividades.set(atividadeId, { nome });
            });

            console.log('Dados iniciais carregados:', {
                alunos: this.cache.alunos.size,
                atividades: this.cache.atividades.size
            });
            
        } catch (error) {
            console.error('Erro ao carregar dados iniciais:', error);
        }
    }

    /**
     * Fetch API com tratamento de erros
     */
    async fetchAPI(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        };

        const response = await fetch(url, { ...defaultOptions, ...options });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    }

    /**
     * Obtém CSRF token
     */
    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    /**
     * Gera ID único para batch
     */
    gerarBatchId() {
        return `batch_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Utilitários de interface
     */
    setLoading(loading) {
        this.estado.loading = loading;
        
        const indicator = document.querySelector('.loading-indicator');
        if (indicator) {
            indicator.style.display = loading ? 'block' : 'none';
        }
        
        const btnSalvar = document.querySelector('.btn-salvar');
        if (btnSalvar) {
            btnSalvar.disabled = loading;
            btnSalvar.textContent = loading ? 'Salvando...' : 'Salvar';
        }
    }

    /**
     * Mostra mensagem para o usuário
     */
    mostrarMensagem(mensagem, tipo = 'info') {
        const alertas = document.querySelector('.alertas');
        if (!alertas) return;

        const alerta = document.createElement('div');
        alerta.className = `alerta alerta-${tipo}`;
        alerta.textContent = mensagem;
        
        alertas.appendChild(alerta);
        
        // Auto-remover após 5 segundos
        setTimeout(() => {
            alerta.remove();
        }, 5000);
    }

    /**
     * Mostra erro para o usuário
     */
    mostrarErro(mensagem) {
        this.mostrarMensagem(mensagem, 'error');
        console.error('TabelaConsolidada Error:', mensagem);
    }

    /**
     * Atualiza contador de alterações pendentes
     */
    atualizarContadorAlteracoes() {
        const contador = document.querySelector('.contador-alteracoes');
        if (contador) {
            const total = this.estado.alteracoesPendentes.size;
            contador.textContent = total;
            contador.style.display = total > 0 ? 'inline' : 'none';
        }
    }

    /**
     * Ajusta layout responsivo
     */
    ajustarLayout() {
        const tabela = document.querySelector(this.config.selectorTabela);
        if (!tabela) return;

        const larguraDisponivel = tabela.parentElement.clientWidth;
        const larguraMinimaCelula = 80;
        const maxVisiveis = Math.floor(larguraDisponivel / larguraMinimaCelula) - 3; // -3 para colunas fixas
        
        this.config.maxAtividadesVisiveis = Math.max(4, Math.min(maxVisiveis, 12));
        this.atualizarVisibilidadeAtividades();
    }

    /**
     * Obtém classe CSS para presença
     */
    getClassePresenca(valor) {
        switch (valor.toUpperCase()) {
            case 'P': return 'presente';
            case 'F': return 'falta';
            case 'J': return 'justificada';
            default: return 'indefinida';
        }
    }

    /**
     * Debounce helper
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Clear timeout helper
     */
    clearTimeout(timerName) {
        if (this.timers[timerName]) {
            clearTimeout(this.timers[timerName]);
            this.timers[timerName] = null;
        }
    }

    /**
     * Limpeza ao destruir
     */
    destroy() {
        Object.values(this.timers).forEach(timer => {
            if (timer) clearTimeout(timer);
        });
        
        this.estado.alteracoesPendentes.clear();
        this.cache.alunos.clear();
        this.cache.atividades.clear();
        this.cache.estatisticas.clear();
        
        console.log('TabelaConsolidada: Destruída');
    }
}

// Inicialização automática quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.tabelaConsolidada = new TabelaConsolidada();
});

// Exportar para uso global
window.TabelaConsolidada = TabelaConsolidada;
