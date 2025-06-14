'''
# Arquivos da Raiz do Projeto Django


### Arquivo: static\js\modules\instrutor-search.js

text
// Módulo de busca de instrutores
const InstrutorSearch = {
    ignoreEligibility: false,
    csrfToken: null,
    
    init: function(csrfToken, ignoreEligibility) {
        this.csrfToken = csrfToken;
        this.ignoreEligibility = ignoreEligibility || false;
        
        // Configuração única para todos os campos de busca de instrutor
        const camposInstrutor = [
            {
                inputId: 'search-instrutor',
                resultsId: 'search-results-instrutor',
                containerId: 'selected-instrutor-container',
                infoId: 'selected-instrutor-info',
                selectId: 'id_instrutor',
                errorId: 'instrutor-error'
            },
            {
                inputId: 'search-instrutor-auxiliar',
                resultsId: 'search-results-instrutor-auxiliar',
                containerId: 'selected-instrutor-auxiliar-container',
                infoId: 'selected-instrutor-auxiliar-info',
                selectId: 'id_instrutor_auxiliar',
                errorId: 'instrutor-auxiliar-error'
            },
            {
                inputId: 'search-auxiliar-instrucao',
                resultsId: 'search-results-auxiliar-instrucao',
                containerId: 'selected-auxiliar-instrucao-container',
                infoId: 'selected-auxiliar-instrucao-info',
                selectId: 'id_auxiliar_instrucao',
                errorId: 'auxiliar-instrucao-error'
            }
        ];
        
        // Configurar cada campo de busca
        camposInstrutor.forEach(campo => {
            const inputElement = document.getElementById(campo.inputId);
            if (inputElement) {
                this.configurarBuscaInstrutores(
                    campo.inputId,
                    campo.resultsId,
                    campo.containerId,
                    campo.infoId,
                    campo.selectId,
                    campo.errorId
                );
                
                // Garantir que cada botão "Limpar seleção" seja único
                this.garantirBotaoLimparUnico(campo.containerId);
            }
        });
    },
    
    setIgnoreEligibility: function(value) {
        this.ignoreEligibility = value;
    },
    
    configurarBuscaInstrutores: function(inputId, resultadosId, selecionadoContainerId, selecionadoInfoId, selectId, errorId) {
        const inputBusca = document.getElementById(inputId);
        const resultadosContainer = document.getElementById(resultadosId);
        const selecionadoContainer = document.getElementById(selecionadoContainerId);
        const selecionadoInfo = document.getElementById(selecionadoInfoId);
        const selectElement = document.getElementById(selectId);
        const errorElement = document.getElementById(errorId);
        
        if (!inputBusca || !resultadosContainer || !selecionadoContainer || !selectElement) {
            console.error('Elementos não encontrados para configurar busca:', inputId);
            return;
        }
        
        // Função para buscar alunos
        const buscarAlunos = (query) => {
            if (query.length < 2) {
                resultadosContainer.style.display = 'none';
                return;
            }
            
            // Fazer requisição AJAX para buscar alunos
            fetch(`/alunos/api/search-instrutores/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    // Limpar resultados anteriores
                    resultadosContainer.innerHTML = '';
                    
                    if (data.length === 0) {
                        // Nenhum resultado encontrado
                        const noResults = document.createElement('div');
                        noResults.className = 'list-group-item';
                        noResults.textContent = 'Nenhum resultado encontrado';
                        resultadosContainer.appendChild(noResults);
                    } else {
                        // Adicionar cada aluno encontrado à lista de resultados
                        data.forEach(aluno => {
                            const item = document.createElement('a');
                            item.href = '#';
                            item.className = 'list-group-item list-group-item-action';
                            item.dataset.cpf = aluno.cpf;
                            item.dataset.nome = aluno.nome;
                            item.dataset.numeroIniciativo = aluno.numero_iniciatico;
                            item.dataset.situacao = aluno.situacao;
                            
                            // Verificar se o aluno está ativo
                            if (aluno.situacao_codigo !== 'ATIVO') {
                                item.classList.add('text-danger');
                            }
                            
                            // Criar HTML para o item de resultado
                            item.innerHTML = `
                                <div class="d-flex align-items-center">
                                    <div class="me-2">
                                        ${aluno.foto ? `<img src="${aluno.foto}" width="32" height="32" class="rounded-circle">` :
                                        `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center"
                                              style="width: 32px; height: 32px; font-size: 14px;">
                                            ${aluno.nome.charAt(0).toUpperCase()}
                                         </div>`}
                                    </div>
                                    <div>
                                        <div><strong>${aluno.nome}</strong></div>
                                        <small>CPF: ${aluno.cpf} | Nº Iniciático: ${aluno.numero_iniciatico || 'N/A'}</small>
                                    </div>
                                </div>
                            `;
                            
                            // Adicionar evento de clique para selecionar o aluno
                            item.addEventListener('click', (e) => {
                                e.preventDefault();
                                
                                // Verificar elegibilidade do aluno se necessário
                                fetch(`/alunos/api/verificar-elegibilidade/${aluno.cpf}/`)
                                    .then(response => response.json())
                                    .then(data => {
                                        // Selecionar o aluno
                                        inputBusca.value = aluno.nome;
                                        
                                        // Atualizar o select oculto
                                        selectElement.value = aluno.cpf;
                                        
                                        // Atualizar a exibição do aluno selecionado
                                        selecionadoInfo.innerHTML = `
                                            <strong>${aluno.nome}</strong><br>
                                            CPF: ${aluno.cpf}<br>
                                            Número Iniciático: ${aluno.numero_iniciatico || 'N/A'}<br>
                                            <span class="badge bg-${getSituacaoClass(aluno.situacao)}">${aluno.situacao}</span>
                                            <div class="mt-2 small">
                                                <div><strong>Status como instrutor:</strong> <span id="${tipo}-status">Verificando...</span></div>
                                                <div class="mt-1"><strong>Turmas:</strong> <span id="${tipo}-turmas">Carregando...</span></div>
                                            </div>
                                        `;
                                        
                                        // Fazer uma requisição adicional para obter mais informações sobre o aluno
                                        fetch(`/alunos/api/detalhes/${aluno.cpf}/`)
                                            .then(response => response.json())
                                            .then(data => {
                                                // Para instrutor principal
                                                $(`#instrutor-status`).text(data.e_instrutor ? 'É instrutor' : 'Não é instrutor');
                                                $(`#instrutor-turmas`).html(turmasHtml);

                                                // Para instrutor auxiliar
                                                $(`#instrutor-auxiliar-status`).text(data.e_instrutor ? 'É instrutor' : 'Não é instrutor');
                                                $(`#instrutor-auxiliar-turmas`).html(turmasHtml);

                                                // Para auxiliar de instrução
                                                $(`#auxiliar-instrucao-status`).text(data.e_instrutor ? 'É instrutor' : 'Não é instrutor');
                                                $(`#auxiliar-instrucao-turmas`).html(turmasHtml);
                                            })
                                            .catch(error => {
                                                console.error('Erro ao buscar detalhes do aluno:', error);
                                                $(`#${tipo}-status`).text('Informação não disponível');
                                                $(`#${tipo}-turmas`).text('Informação não disponível');
                                            });
                                        
                                        // Exibir o container do aluno selecionado
                                        selecionadoContainer.classList.remove('d-none');
                                        
                                        // Exibir aviso se o aluno não for elegível
                                        if (!data.elegivel && errorElement && !this.ignoreEligibility) {
                                            errorElement.innerHTML = `<strong>Aviso:</strong> ${data.motivo}`;
                                            errorElement.classList.remove('d-none');
                                        } else if (errorElement) {
                                            errorElement.classList.add('d-none');
                                        }
                                        
                                        // Ocultar os resultados da busca
                                        resultadosContainer.style.display = 'none';
                                    });
                            });
                            
                            resultadosContainer.appendChild(item);
                        });
                    }
                    
                    // Mostrar container de resultados
                    resultadosContainer.style.display = 'block';
                })
                .catch(error => {
                    console.error('Erro ao buscar alunos:', error);
                    // Mostrar erro no console mas não interromper a experiência do usuário
                });
        };
        
        // Adicionar evento de input para buscar alunos enquanto digita
        inputBusca.addEventListener('input', function() {
            const query = this.value.trim();
            buscarAlunos(query);
        });
        
        // Adicionar evento de clique para limpar e fechar ao clicar fora
        document.addEventListener('click', function(e) {
            if (!inputBusca.contains(e.target) && !resultadosContainer.contains(e.target)) {
                resultadosContainer.style.display = 'none';
            }
        });
        
        // Adicionar evento de foco para mostrar resultados novamente
        inputBusca.addEventListener('focus', function() {
            const query = this.value.trim();
            if (query.length >= 2) {
                buscarAlunos(query);
            }
        });
        
        // Adicionar botão para limpar a seleção se ainda não existir
        if (!selecionadoContainer.nextElementSibling || !selecionadoContainer.nextElementSibling.classList.contains('btn-outline-secondary')) {
            const limparBtn = document.createElement('button');
            limparBtn.type = 'button';
            limparBtn.className = 'btn btn-sm btn-outline-secondary mt-2';
            limparBtn.textContent = 'Limpar seleção';
            limparBtn.addEventListener('click', function() {
                // Limpar o input de busca
                inputBusca.value = '';
                
                // Limpar o select oculto
                selectElement.value = '';
                
                // Esconder o container de aluno selecionado
                selecionadoContainer.classList.add('d-none');
                
                // Esconder mensagens de erro
                if (errorElement) {
                    errorElement.classList.add('d-none');
                }
            });
            
            // Adicionar o botão após o container de aluno selecionado
            selecionadoContainer.parentNode.insertBefore(limparBtn, selecionadoContainer.nextSibling);
        }
    }
};

// Função auxiliar para determinar a classe do badge de situação
function getSituacaoClass(situacao) {
    switch(situacao) {
        case 'Ativo': return 'success';
        case 'Inativo': return 'warning';
        case 'Afastado': return 'warning';
        case 'Excluído': return 'danger';
        case 'Falecido': return 'dark';
        default: return 'secondary';
    }
}




### Arquivo: static\js\turmas\form.js

text
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