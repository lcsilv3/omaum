/**
 * Instrutor Search Module
 * 
 * Implementa funcionalidade de busca e seleção de instrutores
 * (principal, auxiliar, auxiliar de instrução) em formulários de turmas.
 * 
 * Usa AJAX para buscar alunos ativos que possam ser instrutores,
 * valida elegibilidade e popula campos do formulário.
 */

(function() {
  'use strict';

  /**
   * Configuração de campos de instrutor
   */
  const INSTRUCTOR_FIELDS = {
    instrutor: {
      searchInputId: 'search-instrutor',
      resultsId: 'search-results-instrutor',
      selectedContainerId: 'selected-instrutor-container',
      selectedInfoId: 'selected-instrutor-info',
      errorId: 'instrutor-error',
      formFieldId: 'id_instrutor',
      type: 'principal'
    },
    instrutor_auxiliar: {
      searchInputId: 'search-instrutor-auxiliar',
      resultsId: 'search-results-instrutor-auxiliar',
      selectedContainerId: 'selected-instrutor-auxiliar-container',
      selectedInfoId: 'selected-instrutor-auxiliar-info',
      errorId: 'instrutor-auxiliar-error',
      formFieldId: 'id_instrutor_auxiliar',
      type: 'auxiliar'
    },
    auxiliar_instrucao: {
      searchInputId: 'search-auxiliar-instrucao',
      resultsId: 'search-results-auxiliar-instrucao',
      selectedContainerId: 'selected-auxiliar-instrucao-container',
      selectedInfoId: 'selected-auxiliar-instrucao-info',
      errorId: 'auxiliar-instrucao-error',
      formFieldId: 'id_auxiliar_instrucao',
      type: 'auxiliar_instrucao'
    }
  };

  /**
   * Classe para gerenciar busca e seleção de instrutores
   */
  class InstrutorSearch {
    constructor(fieldName, config) {
      this.fieldName = fieldName;
      this.config = config;
      this.debounceTimer = null;
      this.selectedInstrutor = null;
      this.init();
    }

    init() {
      const searchInput = document.getElementById(this.config.searchInputId);
      if (!searchInput) {
        console.warn(`[InstrutorSearch] Elemento ${this.config.searchInputId} não encontrado`);
        return;
      }

      // Event listeners para o campo de busca
      searchInput.addEventListener('input', (e) => this.handleInput(e));
      searchInput.addEventListener('focus', (e) => this.handleFocus(e));
      searchInput.addEventListener('blur', () => this.handleBlur());

      // Restaurar seleção anterior se houver
      this.restoreSelection();
    }

    /**
     * Trata evento de input com debounce
     */
    handleInput(event) {
      clearTimeout(this.debounceTimer);
      const query = event.target.value.trim();

      if (query.length < 2) {
        this.hideResults();
        return;
      }

      this.debounceTimer = setTimeout(() => {
        this.search(query);
      }, 300);
    }

    /**
     * Trata evento de focus - mostra resultados salvos se houver
     */
    handleFocus() {
      const resultsContainer = document.getElementById(this.config.resultsId);
      if (resultsContainer && resultsContainer.style.display !== 'none') {
        resultsContainer.style.display = 'block';
      }
    }

    /**
     * Trata evento de blur com delay para permitir click em resultado
     */
    handleBlur() {
      setTimeout(() => {
        this.hideResults();
      }, 200);
    }

    /**
     * Executa busca de instrutores via AJAX
     */
    async search(query) {
      const resultsContainer = document.getElementById(this.config.resultsId);
      if (!resultsContainer) return;

      try {
        // Mostrar carregamento
        resultsContainer.innerHTML = '<div class="list-group-item text-muted"><small>Buscando...</small></div>';
        resultsContainer.style.display = 'block';

        // Fazer requisição AJAX
        const response = await fetch(`/alunos/api/instrutores/?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const instrutores = await response.json();

        if (Array.isArray(instrutores) && instrutores.length > 0) {
          this.renderResults(instrutores, resultsContainer);
        } else {
          resultsContainer.innerHTML = '<div class="list-group-item text-muted"><small>Nenhum instrutor encontrado</small></div>';
        }
      } catch (error) {
        console.error('[InstrutorSearch] Erro na busca:', error);
        resultsContainer.innerHTML = '<div class="list-group-item text-danger"><small>Erro ao buscar instrutores</small></div>';
      }
    }

    /**
     * Renderiza resultados da busca como itens clicáveis
     */
    renderResults(instrutores, container) {
      const html = instrutores.map(instrutor => `
        <button type="button" class="list-group-item list-group-item-action" data-cpf="${instrutor.cpf}">
          <div class="d-flex w-100 justify-content-between align-items-start">
            <div class="flex-grow-1">
              <strong>${this.escapeHtml(instrutor.nome)}</strong>
              <br>
              <small class="text-muted">
                CPF: ${this.formatCPF(instrutor.cpf)}
                ${instrutor.numero_iniciatico ? ` | Nº Init: ${instrutor.numero_iniciatico}` : ''}
              </small>
            </div>
            ${instrutor.foto ? `<img src="${instrutor.foto}" class="rounded-circle ms-2" style="width: 40px; height: 40px; object-fit: cover;">` : ''}
          </div>
        </button>
      `).join('');

      container.innerHTML = html;

      // Adicionar event listeners aos itens
      container.querySelectorAll('button').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const cpf = btn.dataset.cpf;
          const instrutor = instrutores.find(i => i.cpf === cpf);
          if (instrutor) {
            this.selectInstrutor(instrutor);
          }
        });
      });
    }

    /**
     * Seleciona um instrutor e atualiza o formulário
     */
    selectInstrutor(instrutor) {
      this.selectedInstrutor = instrutor;

      // Atualizar campo oculto do formulário
      const formField = document.getElementById(this.config.formFieldId);
      if (formField) {
        formField.value = instrutor.cpf;
      }

      // Atualizar input de busca
      const searchInput = document.getElementById(this.config.searchInputId);
      if (searchInput) {
        searchInput.value = instrutor.nome;
      }

      // Mostrar informações do selecionado
      this.showSelection(instrutor);

      // Verificar elegibilidade (opcional: validar se já é instrutor em outra turma)
      this.checkEligibility(instrutor.cpf);

      // Esconder resultados
      this.hideResults();
    }

    /**
     * Mostra informações do instrutor selecionado
     */
    showSelection(instrutor) {
      const container = document.getElementById(this.config.selectedContainerId);
      const infoDiv = document.getElementById(this.config.selectedInfoId);

      if (!container || !infoDiv) return;

      let html = `
        <div class="d-flex align-items-start">
          ${instrutor.foto ? `<img src="${instrutor.foto}" class="rounded-circle me-3" style="width: 60px; height: 60px; object-fit: cover;">` : ''}
          <div class="flex-grow-1">
            <strong>${this.escapeHtml(instrutor.nome)}</strong><br>
            <small class="text-muted">
              CPF: ${this.formatCPF(instrutor.cpf)}<br>
              ${instrutor.numero_iniciatico ? `Nº Iniciático: ${instrutor.numero_iniciatico}<br>` : ''}
              Situação: ${instrutor.situacao || 'Ativo'}
            </small>
            <div class="mt-2">
              <button type="button" class="btn btn-sm btn-outline-secondary clear-btn">
                <i class="fas fa-times"></i> Remover
              </button>
            </div>
          </div>
        </div>
      `;

      infoDiv.innerHTML = html;
      container.classList.remove('d-none');

      // Listener para limpar seleção
      const clearBtn = container.querySelector('.clear-btn');
      if (clearBtn) {
        clearBtn.addEventListener('click', (e) => {
          e.preventDefault();
          this.clearSelection();
        });
      }
    }

    /**
     * Limpa a seleção de instrutor
     */
    clearSelection() {
      this.selectedInstrutor = null;

      // Limpar campo oculto
      const formField = document.getElementById(this.config.formFieldId);
      if (formField) {
        formField.value = '';
      }

      // Limpar input de busca
      const searchInput = document.getElementById(this.config.searchInputId);
      if (searchInput) {
        searchInput.value = '';
        searchInput.focus();
      }

      // Esconder container de seleção
      const container = document.getElementById(this.config.selectedContainerId);
      if (container) {
        container.classList.add('d-none');
      }

      // Esconder erro
      const errorDiv = document.getElementById(this.config.errorId);
      if (errorDiv) {
        errorDiv.classList.add('d-none');
      }

      this.hideResults();
    }

    /**
     * Verifica elegibilidade do instrutor (se já atua em outra turma)
     */
    async checkEligibility(cpf) {
      try {
        const response = await fetch(`/alunos/api/alunos/${cpf}/detalhes/`);
        if (!response.ok) return;

        const data = await response.json();
        const errorDiv = document.getElementById(this.config.errorId);

        if (!errorDiv) return;

        if (data.e_instrutor && data.turmas && data.turmas.length > 0) {
          // Instrutor já atua em outra turma
          const turmas = data.turmas.map(t => `${t.nome} (${t.curso})`).join(', ');
          errorDiv.innerHTML = `⚠️ Atenção: Este aluno já atua como instrutor em: ${turmas}`;
          errorDiv.classList.remove('d-none');
        } else {
          errorDiv.classList.add('d-none');
        }
      } catch (error) {
        console.warn('[InstrutorSearch] Erro ao verificar elegibilidade:', error);
      }
    }

    /**
     * Restaura seleção anterior se houver campo preenchido
     */
    restoreSelection() {
      const formField = document.getElementById(this.config.formFieldId);
      if (formField && formField.value) {
        const cpf = formField.value;
        this.searchAndRestore(cpf);
      }
    }

    /**
     * Busca e restaura instrutor selecionado anterior
     */
    async searchAndRestore(cpf) {
      try {
        const response = await fetch(`/alunos/api/alunos/${cpf}/`);
        if (!response.ok) return;

        const data = await response.json();
        if (data.success && data.aluno) {
          const instrutor = {
            cpf: data.aluno.cpf,
            nome: data.aluno.nome,
            foto: data.aluno.foto
          };
          this.showSelection(instrutor);
          this.selectedInstrutor = instrutor;

          // Atualizar input de busca
          const searchInput = document.getElementById(this.config.searchInputId);
          if (searchInput) {
            searchInput.value = instrutor.nome;
          }
        }
      } catch (error) {
        console.warn('[InstrutorSearch] Erro ao restaurar seleção:', error);
      }
    }

    /**
     * Esconde container de resultados
     */
    hideResults() {
      const resultsContainer = document.getElementById(this.config.resultsId);
      if (resultsContainer) {
        resultsContainer.style.display = 'none';
      }
    }

    /**
     * Formata CPF para exibição
     */
    formatCPF(cpf) {
      if (!cpf || cpf.length !== 11) return cpf;
      return `${cpf.substring(0, 3)}.${cpf.substring(3, 6)}.${cpf.substring(6, 9)}-${cpf.substring(9)}`;
    }

    /**
     * Escapa caracteres especiais HTML
     */
    escapeHtml(text) {
      if (!text) return '';
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }
  }

  /**
   * Inicializa o módulo quando o DOM está pronto
   */
  document.addEventListener('DOMContentLoaded', function() {
    Object.entries(INSTRUCTOR_FIELDS).forEach(([fieldName, config]) => {
      const searchInput = document.getElementById(config.searchInputId);
      if (searchInput) {
        new InstrutorSearch(fieldName, config);
      }
    });
  });

  // Exportar para uso em outros contextos se necessário
  window.InstrutorSearch = InstrutorSearch;

})();
