'''
# Arquivos da Raiz do Projeto Django


### Arquivo: static\js\turmas\form_fix.js

text
/**
 * Script para corrigir problemas no formulário de turmas
 * Especificamente para resolver o problema de duplicação do Select2
 */
document.addEventListener('DOMContentLoaded', function() {
    // Destruir qualquer instância existente do Select2 antes de inicializar
    if ($.fn.select2) {
        $('.curso-select').select2('destroy');
        
        // Inicializar Select2 para o campo de curso com configurações corretas
        $('.curso-select').select2({
            theme: 'bootstrap4',
            placeholder: 'Selecione um curso',
            width: '100%',
            dropdownParent: $('body') // Garantir que o dropdown seja anexado ao body
        });
        
        // Remover qualquer dropdown duplicado que possa ter sido criado
        $('.select2-container--open').not(':first').remove();
    }
    
    // Corrigir botões duplicados de "Limpar seleção"
    const containers = [
        'selected-instrutor-container',
        'selected-instrutor-auxiliar-container',
        'selected-auxiliar-instrucao-container'
    ];
    
    containers.forEach(containerId => {
        const botoes = document.querySelectorAll(`#${containerId} + button`);
        // Se houver mais de um botão, remover os extras
        if (botoes.length > 1) {
            for (let i = 1; i < botoes.length; i++) {
                botoes[i].remove();
            }
        }
    });
});


'''