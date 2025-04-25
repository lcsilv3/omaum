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