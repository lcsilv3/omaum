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
    // Adicionar classe form-select antes de inicializar o Select2
    const cursoSelect = $('#id_curso');
    if (cursoSelect.length) {
      cursoSelect.addClass('form-select');
      cursoSelect.select2({
        theme: 'bootstrap-5',
        width: '100%',
        placeholder: 'Selecione',
        allowClear: false
      });
    }
  } else {
    console.warn('Select2 não encontrado; pulando inicialização para evitar quebra do formulário.');
    // Se Select2 não estiver disponível, pelo menos adicionar a classe form-select
    const cursoSelect = document.getElementById('id_curso');
    if (cursoSelect) {
      cursoSelect.classList.add('form-select');
    }
  }

  // ============================================================================
  // MÁSCARA DE HORÁRIO: __:__ às __:__
  // ============================================================================
  const horarioInput = document.querySelector('input[name="horario"]');
  
  if (horarioInput) {

    const TEMPLATE = '__:__ às __:__';
    const DIGIT_POSITIONS = [0, 1, 3, 4, 9, 10, 12, 13];
    const MAX_DIGITS = 8;

    // Estado para armazenar os dígitos digitados
    let currentDigits = [];

    /**
     * Aplica a máscara com os dígitos atuais
     */
    function applyMask() {
      const chars = TEMPLATE.split('');
      currentDigits.forEach((digit, i) => {
        if (i < DIGIT_POSITIONS.length) {
          chars[DIGIT_POSITIONS[i]] = digit;
        }
      });
      return chars.join('');
    }

    /**
     * Atualiza o valor do input com a máscara aplicada
     */
    function updateValue() {
      horarioInput.value = applyMask();
    }

    /**
     * Valida se o horário está dentro dos limites
     */
    function validateTime() {
      if (currentDigits.length < 4) return true;
      
      const h1 = parseInt(currentDigits[0] + currentDigits[1], 10);
      const m1 = parseInt(currentDigits[2] + currentDigits[3], 10);
      if (h1 > 23 || m1 > 59) return false;

      if (currentDigits.length >= 8) {
        const h2 = parseInt(currentDigits[4] + currentDigits[5], 10);
        const m2 = parseInt(currentDigits[6] + currentDigits[7], 10);
        if (h2 > 23 || m2 > 59) return false;
      }

      return true;
    }

    /**
     * Posiciona o cursor na próxima posição editável
     */
    function setCursorPosition() {
      const pos = currentDigits.length < DIGIT_POSITIONS.length 
        ? DIGIT_POSITIONS[currentDigits.length] 
        : TEMPLATE.length;
      setTimeout(() => {
        horarioInput.setSelectionRange(pos, pos);
      }, 0);
    }

    /**
     * Handler para keydown - captura teclas antes de modificar o input
     */
    function handleKeyDown(e) {
      // Permitir navegação
      if (['Tab', 'Shift', 'Control', 'Alt', 'Meta'].includes(e.key)) {
        return;
      }

      // Bloquear setas (usuário não deve navegar manualmente)
      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) {
        e.preventDefault();
        return;
      }

      // Backspace: remove último dígito
      if (e.key === 'Backspace') {
        e.preventDefault();
        if (currentDigits.length > 0) {
          currentDigits.pop();
          updateValue();
          setCursorPosition();
        }
        return;
      }

      // Delete: mesma ação que Backspace
      if (e.key === 'Delete') {
        e.preventDefault();
        if (currentDigits.length > 0) {
          currentDigits.pop();
          updateValue();
          setCursorPosition();
        }
        return;
      }

      // Apenas dígitos
      if (!/^\d$/.test(e.key)) {
        e.preventDefault();
        return;
      }

      // Não permitir mais de 8 dígitos
      if (currentDigits.length >= MAX_DIGITS) {
        e.preventDefault();
        return;
      }

      // Adicionar dígito temporariamente para validação
      e.preventDefault();
      const testDigits = [...currentDigits, e.key];
      currentDigits = testDigits;

      // Validar horário
      if (!validateTime()) {
        // Se inválido, não adiciona o dígito
        currentDigits.pop();
        return;
      }

      // Se válido, atualizar
      updateValue();
      setCursorPosition();
    }

    /**
     * Handler para input - previne qualquer modificação direta
     */
    function handleInput(e) {
      e.preventDefault();
      // Sempre restaurar o valor com a máscara
      updateValue();
      setCursorPosition();
    }

    /**
     * Handler para paste - previne colar
     */
    function handlePaste(e) {
      e.preventDefault();
    }

    /**
     * Handler para focus
     */
    function handleFocus() {
      // Garantir que o template está visível
      if (!horarioInput.value || horarioInput.value.length !== TEMPLATE.length) {
        updateValue();
      }
      setCursorPosition();
    }

    /**
     * Handler para blur
     */
    function handleBlur() {
      if (currentDigits.length === 0) {
        horarioInput.value = '';
      }
    }

    /**
     * Inicializa o campo
     */
    function initializeField() {
      // Extrair dígitos do valor inicial (se existir)
      const initialValue = horarioInput.value;
      if (initialValue) {
        const digits = initialValue.replace(/\D/g, '').slice(0, MAX_DIGITS).split('');
        currentDigits = digits;
      }
      updateValue();
    }

    // Inicializar
    initializeField();

    // Registrar eventos
    horarioInput.addEventListener('keydown', handleKeyDown);
    horarioInput.addEventListener('input', handleInput);
    horarioInput.addEventListener('paste', handlePaste);
    horarioInput.addEventListener('focus', handleFocus);
    horarioInput.addEventListener('blur', handleBlur);
  }

  // ============================================================================
  // MÁSCARA PARA NÚMERO DO LIVRO (apenas números, máx 3 dígitos)
  // ============================================================================
  const numLivroInput = document.querySelector('input[name="num_livro"]');
  if (numLivroInput) {
    numLivroInput.addEventListener("input", function (e) {
      e.target.value = e.target.value.replace(/\D/g, "").slice(0, 3);
    });
  }
});
