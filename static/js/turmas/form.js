// Inicialização dos módulos para o formulário de turmas
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== TURMAS FORM.JS CARREGADO ===');
    
    // PARTE 1: Corrigir carregamento das datas
    function formatarDataParaInput(dataStr) {
        if (!dataStr) return '';
        
        // Se já estiver no formato correto, retorna
        if (/^\d{4}-\d{2}-\d{2}$/.test(dataStr)) return dataStr;
        
        // Tentar extrair data do formato DD/MM/YYYY
        const partes = dataStr.split('/');
        if (partes.length === 3) {
            return `${partes[2]}-${partes[1].padStart(2, '0')}-${partes[0].padStart(2, '0')}`;
        }
        
        return '';
    }
    
    const dataInicioInput = document.getElementById('id_data_inicio');
    const dataFimInput = document.getElementById('id_data_fim');
    
    if (dataInicioInput) {
        const dataInicioTexto = dataInicioInput.nextElementSibling ? dataInicioInput.nextElementSibling.textContent : '';
        const match = dataInicioTexto.match(/Data atual: (\d{2}\/\d{2}\/\d{4})/);
        if (match && match[1]) {
            dataInicioInput.value = formatarDataParaInput(match[1]);
            console.log('Data início definida como:', dataInicioInput.value);
        }
    }
    
    if (dataFimInput) {
        const dataFimTexto = dataFimInput.nextElementSibling ? dataFimInput.nextElementSibling.textContent : '';
        const match = dataFimTexto.match(/Data atual: (\d{2}\/\d{2}\/\d{4})/);
        if (match && match[1]) {
            dataFimInput.value = formatarDataParaInput(match[1]);
            console.log('Data fim definida como:', dataFimInput.value);
        }
    }
    
    // PARTE 2: Remover botões "Limpar seleção" duplicados
    function removerBotoesDuplicados() {
        // Definir os elementos que devem ter apenas um botão de limpar
        const containers = [
            'selected-instrutor-container',
            'selected-instrutor-auxiliar-container',
            'selected-auxiliar-instrucao-container'
        ];
        
        containers.forEach(containerId => {
            const container = document.getElementById(containerId);
            if (!container) return;
            
            // Encontrar todos os botões de limpar após este container
            const botoes = [];
            let proximoElemento = container.nextElementSibling;
            
            while (proximoElemento) {
                if (proximoElemento.tagName === 'BUTTON' && 
                    proximoElemento.textContent.trim() === 'Limpar seleção') {
                    botoes.push(proximoElemento);
                }
                proximoElemento = proximoElemento.nextElementSibling;
            }
            
            // Manter apenas o primeiro botão e remover os outros
            if (botoes.length > 1) {
                for (let i = 1; i < botoes.length; i++) {
                    if (botoes[i].parentNode) {
                        botoes[i].parentNode.removeChild(botoes[i]);
                    }
                }
            }
        });
    }
    
    // Executar a remoção de botões duplicados após um pequeno atraso
    // para garantir que todos os elementos estejam carregados
    setTimeout(removerBotoesDuplicados, 500);
});

// Adicione este código ao seu arquivo JavaScript para inicializar o Select2
// Protegido para não quebrar o restante do script caso o select2 não esteja carregado
$(document).ready(function() {
  if (window.jQuery && $.fn && $.fn.select2) {
    $('.curso-select').select2({
      theme: 'bootstrap4',
      width: '100%'
    });
  } else {
    console.warn('Select2 não encontrado; pulando inicialização para evitar quebra do formulário.');
  }
});

document.addEventListener("DOMContentLoaded", function () {
  // Máscara para horário (__:__ às __:__)
  const horarioInput = document.querySelector('input[name="horario"]');
  if (horarioInput) {
    console.log('Campo horário encontrado, aplicando máscara...');

    const template = '__:__ às __:__';
    const slots = [0, 1, 3, 4, 9, 10, 12, 13]; // posições dos dígitos

    // Define o placeholder uma vez
    horarioInput.placeholder = template;

    const formatHorario = (raw) => {
      const digits = (raw || '').replace(/\D/g, '').slice(0, 8);
      if (!digits) return ''; // Retorna vazio se não houver dígitos
      
      const chars = template.split('');
      const digitArray = digits.split('');

      slots.forEach((slotIndex, i) => {
        if (digitArray[i]) {
          chars[slotIndex] = digitArray[i];
        }
      });
      return chars.join('');
    };

    const applyFormat = (inputEl) => {
      const selectionStart = inputEl.selectionStart;
      const originalLength = inputEl.value.length;
      
      const formatted = formatHorario(inputEl.value);
      inputEl.value = formatted;

      // Lógica para posicionar o cursor de forma inteligente
      if (formatted.length > originalLength) {
        // Se um caractere foi adicionado (geralmente um número), move o cursor
        inputEl.setSelectionRange(selectionStart + 1, selectionStart + 1);
      } else {
        // Se um caractere foi removido, mantém a posição
        inputEl.setSelectionRange(selectionStart, selectionStart);
      }

      // Se o cursor estiver no final, move para o próximo slot vazio
      const nextSlot = formatted.indexOf('_');
      if (selectionStart > nextSlot && nextSlot !== -1) {
        inputEl.setSelectionRange(nextSlot, nextSlot);
      }
    };

    horarioInput.addEventListener('input', (e) => {
      applyFormat(e.target);
    });

    horarioInput.addEventListener('focus', (e) => {
        // Ao focar, move o cursor para a primeira posição editável
        const firstSlot = e.target.value.indexOf('_');
        const cursorPos = firstSlot === -1 ? e.target.value.length : firstSlot;
        // Usar setTimeout para garantir que o cursor seja posicionado após a ação de foco padrão
        setTimeout(() => {
            e.target.setSelectionRange(cursorPos, cursorPos);
        }, 0);
    });

    horarioInput.addEventListener('blur', (e) => {
      // Opcional: limpa se estiver parcialmente preenchido e inválido
      const digits = (e.target.value.match(/\d/g) || []).length;
      if (digits > 0 && digits < 8) {
        // Comportamento pode ser definido aqui: limpar, alertar, etc.
        // Por enquanto, vamos manter o valor parcial.
      } else if (digits === 0) {
        e.target.value = ''; // Limpa se não houver nenhum número
      }
    });

    // Formatar valor existente ao carregar a página
    if (horarioInput.value) {
        applyFormat(horarioInput);
    }
  }

  // Máscara para número do livro (apenas números)
  const numLivroInput = document.querySelector('input[name="num_livro"]');
  if (numLivroInput) {
    numLivroInput.addEventListener("input", function (e) {
      e.target.value = e.target.value.replace(/\D/g, "").slice(0, 3);
    });
  }

  // Atualizar data de término das atividades ao alterar início (padrão: +24 meses)
  const inicioInput = document.querySelector('input[name="data_inicio_ativ"]');
  const terminoInput = document.querySelector('input[name="data_termino_atividades"]');
  if (inicioInput && terminoInput) {
    inicioInput.addEventListener("change", function () {
      if (!terminoInput.value) {
        const inicio = new Date(inicioInput.value);
        if (!isNaN(inicio)) {
          const termino = new Date(inicio);
          termino.setMonth(termino.getMonth() + 24);
          terminoInput.value = termino.toISOString().split("T")[0];
        }
      }
    });
  }
});
