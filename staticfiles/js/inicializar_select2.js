/**
 * OMAUM - Sistema de Gestão de Iniciados
 * Arquivo: inicializar_select2.js
 * Descrição: Inicialização global do Select2 para garantir consistência visual e funcional.
 * Responsável: Equipe OMAUM
 * Última atualização: 2025-06-15
 */

/**
 * Inicialização global do Select2 para o sistema OMAUM
 * Este arquivo centraliza a configuração do Select2 para garantir consistência
 */
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se o jQuery e o Select2 estão disponíveis
    if (typeof $ === 'function' && typeof $.fn.select2 === 'function') {
        // Inicializar todos os elementos com classe select2
        $('.select2').each(function() {
            // Verificar se o elemento já foi inicializado
            if (!$(this).hasClass('select2-hidden-accessible')) {
                $(this).select2({
                    theme: 'bootstrap4',
                    width: '100%',
                    language: {
                        noResults: function() {
                            return "Nenhum resultado encontrado";
                        },
                        searching: function() {
                            return "Buscando...";
                        }
                    }
                });
            }
        });
        
        // Corrigir problemas de z-index em modais
        $(document).on('shown.bs.modal', function() {
            $('.select2-container').css('z-index', '1060');
        });
        
        // Garantir que os Select2 sejam destruídos corretamente antes de reinicializar
        $(document).on('hidden.bs.modal', function() {
            $('.select2-hidden-accessible', this).select2('destroy');
        });
        
        console.log('Select2 inicializado globalmente');
    } else {
        console.warn('jQuery ou Select2 não estão disponíveis. A inicialização global do Select2 foi ignorada.');
    }
});

// Adicionar este script para garantir que o Select2 seja inicializado corretamente
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar Select2 para campos de seleção múltipla
    if (typeof $.fn.select2 === 'function') {
        $('.form-control[multiple]').select2({
            theme: 'bootstrap4',
            placeholder: 'Selecione as opções',
            allowClear: true,
            width: '100%'
        });
        
        // Desabilitar o campo de turmas quando "todas as turmas" estiver marcado
        const todasTurmasCheckbox = document.getElementById('id_todas_turmas');
        const turmasSelect = document.getElementById('id_turmas');
        
        if (todasTurmasCheckbox && turmasSelect) {
            function toggleTurmasField() {
                if (todasTurmasCheckbox.checked) {
                    $(turmasSelect).prop('disabled', true).trigger('change');
                } else {
                    $(turmasSelect).prop('disabled', false).trigger('change');
                }
            }
            
            // Inicializar
            toggleTurmasField();
            
            // Adicionar listener para mudanças
            todasTurmasCheckbox.addEventListener('change', toggleTurmasField);
        }
    }
});