/**
 * JavaScript para relatórios de presença com filtros dinâmicos.
 * Implementa funcionalidades AJAX conforme premissas estabelecidas.
 */

$(document).ready(function() {
    // Inicializar componentes
    initFiltrosDinamicos();
    initValidacaoFormulario();
    initGeracaoRelatorio();
});

/**
 * Inicializa filtros dinâmicos interdependentes.
 * Conforme premissa: filtros são interdependentes e dinâmicos.
 */
function initFiltrosDinamicos() {
    // Filtro de turma atualiza atividades e períodos
    $('#id_turma').on('change', function() {
        const turmaId = $(this).val();
        
        if (turmaId) {
            atualizarAtividades(turmaId);
            atualizarPeriodos(turmaId);
        } else {
            limparFiltrosDependentes();
        }
    });
    
    // Filtro de tipo de relatório atualiza campos necessários
    $('#id_tipo_relatorio').on('change', function() {
        const tipoRelatorio = $(this).val();
        atualizarCamposRelatorio(tipoRelatorio);
    });
    
    // Validação em tempo real
    $('form input, form select').on('change blur', function() {
        validarParametrosAjax();
    });
}

/**
 * Atualiza lista de atividades baseado na turma selecionada.
 */
function atualizarAtividades(turmaId) {
    const $atividades = $('#id_atividade');
    const $loading = $('#loading-atividades');
    
    // Mostrar loading
    $loading.show();
    $atividades.prop('disabled', true);
    
    $.ajax({
        url: '/relatorios-presenca/ajax/atividades-turma/',
        method: 'POST',
        data: {
            'turma_id': turmaId,
            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            // Limpar opções existentes
            $atividades.empty();
            $atividades.append('<option value="">Todas as Atividades</option>');
            
            // Adicionar novas opções
            response.atividades.forEach(function(atividade) {
                $atividades.append(
                    `<option value="${atividade.id}">${atividade.nome}</option>`
                );
            });
            
            // Reabilitar campo
            $atividades.prop('disabled', false);
            $loading.hide();
        },
        error: function(xhr, status, error) {
            console.error('Erro ao carregar atividades:', error);
            mostrarAlerta('Erro ao carregar atividades', 'danger');
            $loading.hide();
            $atividades.prop('disabled', false);
        }
    });
}

/**
 * Atualiza lista de períodos baseado na turma selecionada.
 */
function atualizarPeriodos(turmaId) {
    const $periodos = $('#id_periodo');
    const $loading = $('#loading-periodos');
    
    if (!$periodos.length) return; // Campo não existe neste formulário
    
    // Mostrar loading
    $loading.show();
    $periodos.prop('disabled', true);
    
    $.ajax({
        url: '/relatorios-presenca/ajax/periodos-turma/',
        method: 'POST',
        data: {
            'turma_id': turmaId,
            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            // Limpar opções existentes
            $periodos.empty();
            $periodos.append('<option value="">Selecione o período</option>');
            
            // Adicionar novas opções
            response.periodos.forEach(function(periodo) {
                $periodos.append(
                    `<option value="${periodo.valor}">${periodo.nome}</option>`
                );
            });
            
            // Reabilitar campo
            $periodos.prop('disabled', false);
            $loading.hide();
        },
        error: function(xhr, status, error) {
            console.error('Erro ao carregar períodos:', error);
            mostrarAlerta('Erro ao carregar períodos', 'danger');
            $loading.hide();
            $periodos.prop('disabled', false);
        }
    });
}

/**
 * Limpa filtros dependentes quando turma é desmarcada.
 */
function limparFiltrosDependentes() {
    // Limpar atividades
    const $atividades = $('#id_atividade');
    $atividades.empty();
    $atividades.append('<option value="">Selecione uma turma primeiro</option>');
    $atividades.prop('disabled', true);
    
    // Limpar períodos
    const $periodos = $('#id_periodo');
    if ($periodos.length) {
        $periodos.empty();
        $periodos.append('<option value="">Selecione uma turma primeiro</option>');
        $periodos.prop('disabled', true);
    }
}

/**
 * Atualiza campos do formulário baseado no tipo de relatório.
 */
function atualizarCamposRelatorio(tipoRelatorio) {
    // Ocultar todos os grupos de campos específicos
    $('.campo-especifico').hide();
    
    // Mostrar campos relevantes para o tipo selecionado
    switch (tipoRelatorio) {
        case 'consolidado':
            $('#grupo-periodo-range').show();
            $('#grupo-atividade').show();
            break;
            
        case 'mensal':
        case 'coleta':
            $('#grupo-periodo-mensal').show();
            $('#grupo-atividade').show();
            break;
            
        case 'controle_geral':
            // Apenas turma é necessária
            break;
            
        default:
            // Ocultar todos os campos específicos
            break;
    }
    
    // Atualizar labels e help texts
    atualizarLabelsFormulario(tipoRelatorio);
}

/**
 * Atualiza labels e textos de ajuda baseado no tipo de relatório.
 */
function atualizarLabelsFormulario(tipoRelatorio) {
    const configuracoes = {
        'consolidado': {
            'titulo': 'Relatório Consolidado por Período',
            'descricao': 'Gera relatório com visão consolidada da presença por período, agrupando dados mensais.'
        },
        'mensal': {
            'titulo': 'Relatório de Apuração Mensal',
            'descricao': 'Gera relatório detalhado de presença para um mês específico.'
        },
        'coleta': {
            'titulo': 'Formulário de Coleta Mensal',
            'descricao': 'Gera formulário em branco para coleta manual de dados de presença.'
        },
        'controle_geral': {
            'titulo': 'Relatório de Controle Geral da Turma',
            'descricao': 'Gera relatório completo com informações gerais da turma e estatísticas.'
        }
    };
    
    const config = configuracoes[tipoRelatorio];
    if (config) {
        $('#titulo-relatorio').text(config.titulo);
        $('#descricao-relatorio').text(config.descricao);
    }
}

/**
 * Inicializa validação do formulário.
 */
function initValidacaoFormulario() {
    // Validação customizada do Bootstrap
    $('form').on('submit', function(e) {
        if (!this.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        $(this).addClass('was-validated');
    });
}

/**
 * Valida parâmetros via AJAX em tempo real.
 */
function validarParametrosAjax() {
    const $form = $('#form-relatorio');
    const dados = $form.serialize();
    
    $.ajax({
        url: '/relatorios-presenca/ajax/validar-parametros/',
        method: 'POST',
        data: dados,
        success: function(response) {
            if (response.valido) {
                limparErrosValidacao();
                habilitarBotaoGerar();
            } else {
                mostrarErrosValidacao(response.erros);
                desabilitarBotaoGerar();
            }
        },
        error: function(xhr, status, error) {
            console.error('Erro na validação:', error);
        }
    });
}

/**
 * Mostra erros de validação no formulário.
 */
function mostrarErrosValidacao(erros) {
    // Limpar erros anteriores
    limparErrosValidacao();
    
    // Mostrar novos erros
    const $containerErros = $('#erros-validacao');
    $containerErros.empty();
    
    if (erros.length > 0) {
        const $lista = $('<ul class="list-unstyled mb-0"></ul>');
        
        erros.forEach(function(erro) {
            $lista.append(`<li><i class="fas fa-exclamation-triangle"></i> ${erro}</li>`);
        });
        
        $containerErros.append($lista);
        $containerErros.show();
    }
}

/**
 * Limpa erros de validação.
 */
function limparErrosValidacao() {
    $('#erros-validacao').hide().empty();
}

/**
 * Habilita botão de gerar relatório.
 */
function habilitarBotaoGerar() {
    $('#btn-gerar-relatorio').prop('disabled', false);
}

/**
 * Desabilita botão de gerar relatório.
 */
function desabilitarBotaoGerar() {
    $('#btn-gerar-relatorio').prop('disabled', true);
}

/**
 * Inicializa funcionalidades de geração de relatório.
 */
function initGeracaoRelatorio() {
    // Loading durante geração
    $('#form-relatorio').on('submit', function() {
        const $btn = $('#btn-gerar-relatorio');
        const textoOriginal = $btn.html();
        
        // Mostrar loading
        $btn.html('<i class="fas fa-spinner fa-spin"></i> Gerando...');
        $btn.prop('disabled', true);
        
        // Mostrar progresso
        $('#progresso-geracao').show();
        
        // Simular progresso (em implementação real, usar WebSocket ou polling)
        simularProgresso();
    });
}

/**
 * Simula progresso de geração (placeholder para implementação real).
 */
function simularProgresso() {
    const $barra = $('#barra-progresso');
    let progresso = 0;
    
    const intervalo = setInterval(function() {
        progresso += Math.random() * 20;
        
        if (progresso >= 100) {
            progresso = 100;
            clearInterval(intervalo);
        }
        
        $barra.css('width', progresso + '%');
        $barra.attr('aria-valuenow', progresso);
        $barra.text(Math.round(progresso) + '%');
    }, 500);
}

/**
 * Mostra alerta na interface.
 */
function mostrarAlerta(mensagem, tipo = 'info') {
    const $alerta = $(`
        <div class="alert alert-${tipo} alert-dismissible fade show" role="alert">
            ${mensagem}
            <button type="button" class="close" data-dismiss="alert">
                <span>&times;</span>
            </button>
        </div>
    `);
    
    $('#container-alertas').append($alerta);
    
    // Auto-remover após 5 segundos
    setTimeout(function() {
        $alerta.alert('close');
    }, 5000);
}

/**
 * Utilitários para formatação de dados.
 */
const Utils = {
    /**
     * Formata data para exibição.
     */
    formatarData: function(data) {
        return new Date(data).toLocaleDateString('pt-BR');
    },
    
    /**
     * Formata tamanho de arquivo.
     */
    formatarTamanho: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    /**
     * Debounce para otimizar chamadas AJAX.
     */
    debounce: function(func, wait) {
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
};

// Aplicar debounce na validação
const validarParametrosDebounced = Utils.debounce(validarParametrosAjax, 300);

