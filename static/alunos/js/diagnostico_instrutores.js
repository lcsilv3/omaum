document.addEventListener('DOMContentLoaded', function() {
    const mostrarElegiveisCheckbox = document.getElementById('mostrar-elegiveis');
    const mostrarInelegiveisCheckbox = document.getElementById('mostrar-inelegiveis');
    const tabela = document.getElementById('tabela-diagnostico');

    function atualizarVisibilidade() {
        if (!tabela) return;

        const mostrarElegiveis = mostrarElegiveisCheckbox.checked;
        const mostrarInelegiveis = mostrarInelegiveisCheckbox.checked;
        
        const linhas = tabela.querySelectorAll('tbody tr');
        
        linhas.forEach(linha => {
            const isElegivel = linha.classList.contains('elegivel');
            const isInelegivel = linha.classList.contains('inelegivel');

            if (isElegivel) {
                linha.style.display = mostrarElegiveis ? '' : 'none';
            } else if (isInelegivel) {
                linha.style.display = mostrarInelegiveis ? '' : 'none';
            }
        });
    }
    
    if (mostrarElegiveisCheckbox && mostrarInelegiveisCheckbox) {
        mostrarElegiveisCheckbox.addEventListener('change', atualizarVisibilidade);
        mostrarInelegiveisCheckbox.addEventListener('change', atualizarVisibilidade);
        
        // Chama a função uma vez no início para garantir o estado correto
        atualizarVisibilidade();
    }
});
