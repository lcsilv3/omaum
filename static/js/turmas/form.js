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
  // Máscara para horário (__:__ às __:__)
  const horarioInput = document.querySelector('input[name="horario"]');
  if (horarioInput) {
    horarioInput.addEventListener("input", function (e) {
      let v = e.target.value.replace(/\D/g, "");
      if (v.length > 4) v = v.slice(0, 8);
      if (v.length >= 4) {
        e.target.value = v.slice(0, 2) + ":" + v.slice(2, 4) + " às " + (v.slice(4, 6) || "") + (v.length > 6 ? ":" + v.slice(6, 8) : "");
      } else if (v.length >= 2) {
        e.target.value = v.slice(0, 2) + ":" + v.slice(2, 4);
      } else {
        e.target.value = v;
      }
    });
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
