// Módulo para gerenciar o seletor de dias da semana
const DiasSemana = {
    init: function() {
        const diasSemanaDisplay = document.getElementById('dias-semana-display');
        const diasSemanaDropdown = document.getElementById('dias-semana-dropdown');
        const diasSemanaTexto = document.getElementById('dias-semana-texto');
        const diasSemanaHidden = document.getElementById('dias_semana_hidden');
        
        if (!diasSemanaDisplay || !diasSemanaDropdown || !diasSemanaTexto || !diasSemanaHidden) {
            console.warn('Elementos para dias da semana não encontrados');
            return;
        }
        
        // Configuração dos dias da semana
        const diaItems = document.querySelectorAll('.dia-semana-item');
        let diasSelecionados = diasSemanaHidden.value ? diasSemanaHidden.value.split(', ') : [];
        
        // Marcar os dias já selecionados
        diaItems.forEach(item => {
            const dia = item.dataset.dia;
            const checkbox = item.querySelector('input[type="checkbox"]');
            
            if (diasSelecionados.includes(dia)) {
                item.classList.add('selected');
                checkbox.checked = true;
            }
            
            item.addEventListener('click', () => {
                item.classList.toggle('selected');
                checkbox.checked = !checkbox.checked;
                
                // Atualizar a lista de dias selecionados
                diasSelecionados = Array.from(document.querySelectorAll('.dia-semana-item.selected'))
                    .map(el => el.dataset.dia);
                
                // Atualizar o texto exibido
                diasSemanaTexto.textContent = diasSelecionados.length > 0 ?
                    diasSelecionados.join(', ') : 'Selecione os dias da semana';
                
                // Atualizar o campo oculto
                diasSemanaHidden.value = diasSelecionados.join(', ');
            });
        });
        
        // Mostrar/esconder o dropdown
        diasSemanaDisplay.addEventListener('click', () => {
            const isVisible = diasSemanaDropdown.style.display === 'block';
            diasSemanaDropdown.style.display = isVisible ? 'none' : 'block';
            diasSemanaDisplay.classList.toggle('focus', !isVisible);
        });
        
        // Fechar dropdown ao clicar fora
        document.addEventListener('click', (e) => {
            if (!diasSemanaDisplay.contains(e.target) && !diasSemanaDropdown.contains(e.target)) {
                diasSemanaDropdown.style.display = 'none';
                diasSemanaDisplay.classList.remove('focus');
            }
        });
    }
};
