/**
 * Script otimizado para registro rápido de presenças
 * Inclui funcionalidades de performance, cache e UX avançadas
 */

class RegistroRapidoManager {
    constructor() {
        this.alunosData = [];
        this.presencasModificadas = {};
        this.cache = new Map();
        this.debounceTimers = new Map();
        this.autoSaveEnabled = false;
        this.autoSaveInterval = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupKeyboardShortcuts();
        this.setupAutoSave();
        this.loadFromLocalStorage();
    }
    
    setupEventListeners() {
        // Eventos dos formulários
        $('#turma').on('change', () => this.onTurmaChange());
        $('#atividade').on('change', () => this.onAtividadeChange());
        $('#data').on('change', () => this.onDataChange());
        
        // Busca com debounce otimizado
        $('#buscaAluno').on('input', (e) => {
            this.debounceBusca(e.target.value);
        });
        
        // Touch events para mobile
        if ('ontouchstart' in window) {
            this.setupTouchEvents();
        }
        
        // Eventos de visibilidade da página
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.saveToLocalStorage();
            } else {
                this.loadFromLocalStorage();
            }
        });
    }
    
    setupKeyboardShortcuts() {
        $(document).keydown((e) => {
            // Verificar se não está em um input
            if ($(e.target).is('input, textarea, select')) {
                return;
            }
            
            if (e.ctrlKey || e.metaKey) {
                switch(e.which) {
                    case 65: // Ctrl+A
                        e.preventDefault();
                        this.marcarTodosPresente();
                        break;
                    case 68: // Ctrl+D  
                        e.preventDefault();
                        this.marcarTodosAusente();
                        break;
                    case 83: // Ctrl+S
                        e.preventDefault();
                        this.salvarPresencas();
                        break;
                    case 76: // Ctrl+L
                        e.preventDefault();
                        this.limparSelecoes();
                        break;
                    case 82: // Ctrl+R
                        e.preventDefault();
                        this.recarregarAlunos();
                        break;
                }
            } else {
                switch(e.which) {
                    case 27: // Esc
                        this.fecharModais();
                        break;
                    case 113: // F2
                        e.preventDefault();
                        this.toggleAutoSave();
                        break;
                }
            }
        });
    }
    
    setupTouchEvents() {
        // Gestos de swipe para marcar presença
        let startX, startY;
        
        $(document).on('touchstart', '.aluno-card', function(e) {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        
        $(document).on('touchend', '.aluno-card', (e) => {
            if (!startX || !startY) return;
            
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            
            const diffX = startX - endX;
            const diffY = startY - endY;
            
            // Swipe horizontal
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                const alunoId = parseInt($(e.currentTarget).data('aluno-id'));
                
                if (diffX > 0) {
                    // Swipe left - Ausente
                    this.marcarPresenca(alunoId, false);
                } else {
                    // Swipe right - Presente
                    this.marcarPresenca(alunoId, true);
                }
                
                // Feedback háptico se disponível
                if (navigator.vibrate) {
                    navigator.vibrate(50);
                }
            }
            
            startX = startY = null;
        });
    }
    
    setupAutoSave() {
        // Auto-save a cada 30 segundos se habilitado
        this.autoSaveInterval = setInterval(() => {
            if (this.autoSaveEnabled && Object.keys(this.presencasModificadas).length > 0) {
                this.salvarPresencas(true); // true = silent save
            }
        }, 30000);
    }
    
    debounceBusca(query) {
        const timerId = 'busca';
        
        // Cancelar timer anterior
        if (this.debounceTimers.has(timerId)) {
            clearTimeout(this.debounceTimers.get(timerId));
        }
        
        // Criar novo timer
        const timer = setTimeout(() => {
            if (query.length >= 2) {
                this.buscarAlunos(query);
            } else {
                $('#resultadosBusca').empty();
            }
            this.debounceTimers.delete(timerId);
        }, 300);
        
        this.debounceTimers.set(timerId, timer);
    }
    
    carregarAlunosTurma() {
        const turmaId = $('#turma').val();
        const atividadeId = $('#atividade').val();
        const data = $('#data').val();
        
        if (!turmaId || !atividadeId || !data) {
            this.showToast('Por favor, selecione turma, atividade e data', 'warning');
            return;
        }
        
        // Verificar cache primeiro
        const cacheKey = `alunos-${turmaId}-${data}`;
        if (this.cache.has(cacheKey)) {
            this.alunosData = this.cache.get(cacheKey);
            this.renderizarAlunos();
            this.mostrarInterface();
            return;
        }
        
        this.showLoading(true);
        
        $.ajax({
            url: '/presencas/ajax/alunos-turma/',
            data: { 'turma_id': turmaId },
            success: (response) => {
                if (response.alunos) {
                    this.alunosData = response.alunos;
                    
                    // Salvar no cache
                    this.cache.set(cacheKey, this.alunosData);
                    
                    this.renderizarAlunos();
                    this.mostrarInterface();
                    this.atualizarEstatisticas();
                }
            },
            error: (xhr) => {
                this.showToast('Erro ao carregar alunos da turma', 'error');
                console.error('Erro AJAX:', xhr);
            },
            complete: () => {
                this.showLoading(false);
            }
        });
    }
    
    renderizarAlunos() {
        const grid = $('#alunosGrid');
        grid.empty();
        
        // Usar DocumentFragment para performance
        const fragment = document.createDocumentFragment();
        
        this.alunosData.forEach((aluno) => {
            const alunoElement = this.criarElementoAluno(aluno);
            fragment.appendChild(alunoElement);
        });
        
        grid[0].appendChild(fragment);
        
        // Aplicar animações CSS
        $('.aluno-card').each((index, element) => {
            $(element).css('animation-delay', `${index * 50}ms`);
        });
    }
    
    criarElementoAluno(aluno) {
        const presencaAtual = this.presencasModificadas[aluno.id] !== undefined 
            ? this.presencasModificadas[aluno.id] 
            : aluno.presente;
            
        const jaRegistrado = aluno.ja_registrado;
        
        let statusClass = '';
        let statusBadge = '';
        
        if (presencaAtual === true) {
            statusClass = 'presente';
            statusBadge = '<span class="status-badge presente">Presente</span>';
        } else if (presencaAtual === false) {
            statusClass = 'ausente';
            statusBadge = '<span class="status-badge ausente">Ausente</span>';
        } else if (jaRegistrado) {
            statusClass = 'ja-registrado';
            statusBadge = '<span class="status-badge ja-registrado">Registrado</span>';
        }
        
        const div = document.createElement('div');
        div.className = `aluno-card ${statusClass}`;
        div.setAttribute('data-aluno-id', aluno.id);
        
        div.innerHTML = `
            ${statusBadge}
            <div class="aluno-info">
                <h5>${this.escapeHtml(aluno.nome)}</h5>
                <div class="cpf">CPF: ${aluno.cpf}</div>
                <div class="curso">${this.escapeHtml(aluno.curso)}</div>
            </div>
            <div class="presenca-controls">
                <button type="button" class="btn-presenca btn-presente ${presencaAtual === true ? 'active' : ''}" 
                        onclick="registroManager.marcarPresenca(${aluno.id}, true)">
                    <i class="fas fa-check"></i> Presente
                </button>
                <button type="button" class="btn-presenca btn-ausente ${presencaAtual === false ? 'active' : ''}" 
                        onclick="registroManager.marcarPresenca(${aluno.id}, false)">
                    <i class="fas fa-times"></i> Ausente
                </button>
            </div>
            <button type="button" class="btn-observacao" onclick="registroManager.toggleObservacao(${aluno.id})">
                + Observação
            </button>
            <textarea class="observacao-input" id="obs-${aluno.id}" 
                      placeholder="Digite uma observação..."></textarea>
        `;
        
        return div;
    }
    
    marcarPresenca(alunoId, presente) {
        this.presencasModificadas[alunoId] = presente;
        
        const card = $(`.aluno-card[data-aluno-id="${alunoId}"]`);
        const btnPresente = card.find('.btn-presente');
        const btnAusente = card.find('.btn-ausente');
        
        // Animação de feedback
        card.addClass('selecting');
        setTimeout(() => card.removeClass('selecting'), 200);
        
        // Atualizar estado visual
        btnPresente.toggleClass('active', presente);
        btnAusente.toggleClass('active', !presente);
        
        card.removeClass('presente ausente')
            .addClass(presente ? 'presente' : 'ausente');
        
        // Atualizar badge
        card.find('.status-badge').remove();
        const badgeClass = presente ? 'presente' : 'ausente';
        const badgeText = presente ? 'Presente' : 'Ausente';
        card.prepend(`<span class="status-badge ${badgeClass}">${badgeText}</span>`);
        
        this.atualizarEstatisticas();
        this.saveToLocalStorage();
    }
    
    marcarTodosPresente() {
        this.alunosData.forEach(aluno => {
            this.marcarPresenca(aluno.id, true);
        });
        this.showToast('Todos marcados como presentes', 'success');
    }
    
    marcarTodosAusente() {
        this.alunosData.forEach(aluno => {
            this.marcarPresenca(aluno.id, false);
        });
        this.showToast('Todos marcados como ausentes', 'warning');
    }
    
    limparSelecoes() {
        if (!confirm('Deseja limpar todas as seleções?')) return;
        
        this.presencasModificadas = {};
        $('.observacao-input').val('');
        $('.aluno-card').removeClass('com-observacao presente ausente');
        
        this.renderizarAlunos();
        this.atualizarEstatisticas();
        this.clearLocalStorage();
        
        this.showToast('Seleções limparas', 'info');
    }
    
    salvarPresencas(silent = false) {
        const turmaId = $('#turma').val();
        const atividadeId = $('#atividade').val();
        const data = $('#data').val();
        
        if (!turmaId || !atividadeId || !data) {
            if (!silent) this.showToast('Configure turma, atividade e data', 'warning');
            return;
        }
        
        const presencas = this.prepararDadosPresencas();
        
        if (presencas.length === 0) {
            if (!silent) this.showToast('Nenhuma presença foi marcada', 'warning');
            return;
        }
        
        if (!silent) this.showLoading(true);
        
        $.ajax({
            url: '/presencas/ajax/salvar-lote/',
            method: 'POST',
            data: JSON.stringify({
                turma_id: parseInt(turmaId),
                atividade_id: parseInt(atividadeId),
                data: data,
                presencas: presencas
            }),
            contentType: 'application/json',
            success: (response) => {
                if (response.success) {
                    if (!silent) {
                        this.showToast(
                            `Presenças salvas! ${response.registradas} registradas, ${response.atualizadas} atualizadas`, 
                            'success'
                        );
                    }
                    
                    // Limpar modificações salvas
                    this.presencasModificadas = {};
                    this.clearLocalStorage();
                    
                    // Recarregar se não for silent
                    if (!silent) {
                        setTimeout(() => this.carregarAlunosTurma(), 1000);
                    }
                }
            },
            error: (xhr) => {
                const errorMsg = xhr.responseJSON?.error || 'Erro interno';
                if (!silent) this.showToast(`Erro: ${errorMsg}`, 'error');
            },
            complete: () => {
                if (!silent) this.showLoading(false);
            }
        });
    }
    
    prepararDadosPresencas() {
        return Object.keys(this.presencasModificadas).map(alunoId => ({
            aluno_id: parseInt(alunoId),
            presente: this.presencasModificadas[alunoId],
            observacao: $(`#obs-${alunoId}`).val() || ''
        }));
    }
    
    buscarAlunos(query) {
        const turmaId = $('#turma').val();
        
        $.ajax({
            url: '/presencas/ajax/buscar-alunos/',
            data: {
                'q': query,
                'turma_id': turmaId,
                'limit': 10
            },
            success: (response) => {
                this.renderizarResultadosBusca(response.alunos || []);
            },
            error: () => {
                $('#resultadosBusca').html('<p class="text-danger">Erro na busca</p>');
            }
        });
    }
    
    renderizarResultadosBusca(alunos) {
        const container = $('#resultadosBusca');
        
        if (alunos.length === 0) {
            container.html('<p class="text-muted">Nenhum aluno encontrado</p>');
            return;
        }
        
        const html = alunos.map(aluno => `
            <div class="aluno-card busca-result" onclick="registroManager.adicionarAlunoRapido(${aluno.id}, '${this.escapeHtml(aluno.nome)}', '${aluno.cpf}')">
                <div class="aluno-info">
                    <h5>${this.escapeHtml(aluno.nome)}</h5>
                    <div class="cpf">CPF: ${aluno.cpf}</div>
                    <div class="curso">${this.escapeHtml(aluno.curso)}</div>
                </div>
            </div>
        `).join('');
        
        container.html(html);
    }
    
    adicionarAlunoRapido(alunoId, nome, cpf) {
        const alunoExiste = this.alunosData.find(a => a.id === alunoId);
        
        if (!alunoExiste) {
            this.alunosData.push({
                id: alunoId,
                nome: nome,
                cpf: cpf,
                curso: 'Busca Individual',
                presente: null,
                ja_registrado: false
            });
            
            this.renderizarAlunos();
            this.atualizarEstatisticas();
        }
        
        // Focar e destacar aluno
        this.focarAluno(alunoId);
        
        // Limpar busca
        $('#buscaAluno').val('');
        $('#resultadosBusca').empty();
    }
    
    focarAluno(alunoId) {
        const alunoCard = $(`.aluno-card[data-aluno-id="${alunoId}"]`);
        
        if (alunoCard.length) {
            // Scroll suave
            alunoCard[0].scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
            
            // Destacar temporariamente
            alunoCard.addClass('destacado');
            setTimeout(() => alunoCard.removeClass('destacado'), 2000);
        }
    }
    
    toggleObservacao(alunoId) {
        const card = $(`.aluno-card[data-aluno-id="${alunoId}"]`);
        card.toggleClass('com-observacao');
        
        if (card.hasClass('com-observacao')) {
            const textarea = $(`#obs-${alunoId}`);
            setTimeout(() => textarea.focus(), 100);
        }
    }
    
    atualizarEstatisticas() {
        let totalPresentes = 0;
        let totalAusentes = 0;
        let totalPendentes = 0;
        
        this.alunosData.forEach(aluno => {
            const presencaAtual = this.presencasModificadas[aluno.id] !== undefined 
                ? this.presencasModificadas[aluno.id] 
                : aluno.presente;
                
            if (presencaAtual === true) {
                totalPresentes++;
            } else if (presencaAtual === false) {
                totalAusentes++;
            } else {
                totalPendentes++;
            }
        });
        
        // Animação nos números
        this.animarNumero('#totalAlunos', this.alunosData.length);
        this.animarNumero('#totalPresentes', totalPresentes);
        this.animarNumero('#totalAusentes', totalAusentes);
        this.animarNumero('#totalPendentes', totalPendentes);
    }
    
    animarNumero(selector, novoValor) {
        const elemento = $(selector);
        const valorAtual = parseInt(elemento.text()) || 0;
        
        if (valorAtual === novoValor) return;
        
        $({ value: valorAtual }).animate({ value: novoValor }, {
            duration: 500,
            step: function() {
                elemento.text(Math.floor(this.value));
            },
            complete: function() {
                elemento.text(novoValor);
            }
        });
    }
    
    mostrarInterface() {
        $('#buscaSection').slideDown();
        $('#alunosContainer').slideDown();
        $('#statsBar').slideDown();
    }
    
    showLoading(show) {
        if (show) {
            $('#loading').fadeIn();
        } else {
            $('#loading').fadeOut();
        }
    }
    
    showToast(message, type = 'info', duration = 5000) {
        const toastClass = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        }[type] || 'alert-info';
        
        const toast = $(`
            <div class="alert ${toastClass} alert-dismissible fade show toast-custom" 
                 style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px; animation: slideInRight 0.3s ease;">
                <i class="fas fa-${this.getToastIcon(type)}"></i> ${message}
                <button type="button" class="close" data-dismiss="alert">
                    <span>&times;</span>
                </button>
            </div>
        `);
        
        $('body').append(toast);
        
        setTimeout(() => {
            toast.fadeOut(() => toast.remove());
        }, duration);
    }
    
    getToastIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    // Persistência Local
    saveToLocalStorage() {
        const data = {
            presencasModificadas: this.presencasModificadas,
            turma: $('#turma').val(),
            atividade: $('#atividade').val(),
            data: $('#data').val(),
            timestamp: Date.now()
        };
        
        try {
            localStorage.setItem('registro_rapido_data', JSON.stringify(data));
        } catch (e) {
            console.warn('Erro ao salvar no localStorage:', e);
        }
    }
    
    loadFromLocalStorage() {
        try {
            const data = localStorage.getItem('registro_rapido_data');
            if (!data) return;
            
            const parsed = JSON.parse(data);
            
            // Verificar se não é muito antigo (24h)
            if (Date.now() - parsed.timestamp > 24 * 60 * 60 * 1000) {
                this.clearLocalStorage();
                return;
            }
            
            // Restaurar dados
            if (parsed.presencasModificadas) {
                this.presencasModificadas = parsed.presencasModificadas;
            }
            
            if (parsed.turma) $('#turma').val(parsed.turma).trigger('change');
            if (parsed.atividade) $('#atividade').val(parsed.atividade).trigger('change');
            if (parsed.data) $('#data').val(parsed.data);
            
        } catch (e) {
            console.warn('Erro ao carregar do localStorage:', e);
            this.clearLocalStorage();
        }
    }
    
    clearLocalStorage() {
        try {
            localStorage.removeItem('registro_rapido_data');
        } catch (e) {
            console.warn('Erro ao limpar localStorage:', e);
        }
    }
    
    // Utilitários
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Event handlers
    onTurmaChange() {
        this.cache.clear(); // Limpar cache ao mudar turma
        $('#alunosContainer').hide();
        $('#buscaSection').hide();
        $('#statsBar').hide();
    }
    
    onAtividadeChange() {
        // Implementar se necessário
    }
    
    onDataChange() {
        this.cache.clear(); // Limpar cache ao mudar data
    }
    
    toggleAutoSave() {
        this.autoSaveEnabled = !this.autoSaveEnabled;
        const status = this.autoSaveEnabled ? 'ativado' : 'desativado';
        this.showToast(`Auto-save ${status}`, 'info');
    }
    
    recarregarAlunos() {
        this.cache.clear();
        this.carregarAlunosTurma();
    }
    
    fecharModais() {
        $('#keyboardShortcuts').removeClass('show');
        $('.observacao-input').blur();
    }
}

// Instância global
let registroManager;

// Inicializar quando document estiver pronto
$(document).ready(function() {
    registroManager = new RegistroRapidoManager();
    
    // Funções globais para compatibilidade com template
    window.carregarAlunosTurma = () => registroManager.carregarAlunosTurma();
    window.marcarTodosPresente = () => registroManager.marcarTodosPresente();
    window.marcarTodosAusente = () => registroManager.marcarTodosAusente();
    window.salvarPresencas = () => registroManager.salvarPresencas();
    window.limparSelecoes = () => registroManager.limparSelecoes();
    window.toggleKeyboardShortcuts = () => $('#keyboardShortcuts').toggleClass('show');
});
