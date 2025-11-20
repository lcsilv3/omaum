// Inicialização dos módulos para o formulário de turmas
document.addEventListener('DOMContentLoaded', function() {
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
$(document).ready(function() {
    // Inicializar Select2 para o dropdown de cursos
    $('.curso-select').select2({
        theme: 'bootstrap4',
        width: '100%'
    });
});

document.addEventListener("DOMContentLoaded", function () {
  // Máscara para horário (__:__ "às" __:__) com preenchimento guiado
  const horarioInput = document.querySelector('input[name="horario"]');
  if (horarioInput) {
    const MASCARA_HORARIO = '__:__ "às" __:__';
    const POSICOES_DIGITOS = [0, 1, 3, 4, 11, 12, 14, 15];
    const limparNaoDigitos = (valor) => valor.replace(/\D/g, '').slice(0, 8);

    const formatarHorario = (digitos) => {
      const caracteres = MASCARA_HORARIO.split('');
      POSICOES_DIGITOS.forEach((posicao, indice) => {
        caracteres[posicao] = digitos[indice] || '_';
      });
      return caracteres.join('');
    };

    const atualizarInput = (alvo, digitos) => {
      alvo.dataset.horarioDigitos = digitos;
      if (digitos.length === 0) {
        alvo.value = MASCARA_HORARIO;
      } else {
        alvo.value = formatarHorario(digitos);
      }
      posicionarCursor(alvo, digitos.length);
    };

    const posicionarCursor = (alvo, quantidadeDigitos) => {
      const mapaPosicoes = [0, 1, 3, 4, 11, 12, 14, 15, MASCARA_HORARIO.length];
      const posicao = mapaPosicoes[Math.min(quantidadeDigitos, mapaPosicoes.length - 1)];
      requestAnimationFrame(() => {
        try {
          alvo.setSelectionRange(posicao, posicao);
        } catch (err) {
          // Ignora navegadores que não suportam setSelectionRange
        }
      });
    };

    const iniciarMascaraSeNecessario = () => {
      const digitosIniciais = limparNaoDigitos(horarioInput.value || '');
      if (digitosIniciais) {
        atualizarInput(horarioInput, digitosIniciais);
      } else {
        horarioInput.dataset.horarioDigitos = '';
        horarioInput.value = '';
      }
      horarioInput.placeholder = MASCARA_HORARIO;
    };

    horarioInput.addEventListener('focus', () => {
      const digitos = horarioInput.dataset.horarioDigitos || '';
      atualizarInput(horarioInput, digitos);
    });

    horarioInput.addEventListener('blur', () => {
      const digitos = horarioInput.dataset.horarioDigitos || '';
      if (digitos.length === 0) {
        horarioInput.value = '';
      } else {
        horarioInput.value = formatarHorario(digitos);
      }
    });

    horarioInput.addEventListener('keydown', (event) => {
      if (event.ctrlKey || event.metaKey) {
        return;
      }

      const digitosAtuais = horarioInput.dataset.horarioDigitos || '';
      const tecla = event.key;

      if (tecla === 'Backspace') {
        event.preventDefault();
        atualizarInput(horarioInput, digitosAtuais.slice(0, -1));
        return;
      }

      if (tecla === 'Delete') {
        event.preventDefault();
        atualizarInput(horarioInput, '');
        return;
      }

      if (tecla.length === 1) {
        if (/\d/.test(tecla)) {
          event.preventDefault();
          if (digitosAtuais.length >= POSICOES_DIGITOS.length) {
            return;
          }
          atualizarInput(horarioInput, digitosAtuais + tecla);
        } else {
          event.preventDefault();
        }
        return;
      }
      // Permite outras teclas de navegação (Tab, Enter, setas, etc.)
    });

    horarioInput.addEventListener('paste', (event) => {
      event.preventDefault();
      const texto = (event.clipboardData || window.clipboardData).getData('text') || '';
      const digitos = limparNaoDigitos(texto);
      atualizarInput(horarioInput, digitos);
    });

    iniciarMascaraSeNecessario();
  }

  // Máscara para número do livro (apenas números)
  const numLivroInput = document.querySelector('input[name="num_livro"]');
  if (numLivroInput) {
    numLivroInput.addEventListener("input", function (e) {
      e.target.value = e.target.value.replace(/\D/g, "").slice(0, 3);
    });
  }

  // Atualizar data de término das atividades ao alterar início (padrão: +90 dias)
  const inicioInput = document.querySelector('input[name="data_inicio_ativ"]');
  const terminoInput = document.querySelector('input[name="data_termino_atividades"]');
  if (inicioInput && terminoInput) {
    inicioInput.addEventListener("change", function () {
      if (!terminoInput.value) {
        const inicio = new Date(inicioInput.value);
        if (!isNaN(inicio)) {
          const termino = new Date(inicio);
          termino.setDate(termino.getDate() + 90);
          terminoInput.value = termino.toISOString().split("T")[0];
        }
      }
    });
  }
});
