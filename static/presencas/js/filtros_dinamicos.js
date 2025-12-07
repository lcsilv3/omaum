// c:/omaum/presencas/static/presencas/js/filtros_dinamicos.js
const PresencasFiltros = (function() {
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  function montarParams(elms) {
    const params = {};
    if (elms.turma && elms.turma.value) params['turma_id'] = elms.turma.value;
    if (elms.aluno && elms.aluno.value) params['aluno_id'] = elms.aluno.value;
    if (elms.mes && elms.mes.value) params['mes'] = elms.mes.value;
    if (elms.ano && elms.ano.value) params['ano'] = elms.ano.value;
    return params;
  }

  function atualizarTabela(urlDados, elms) {
    const params = montarParams(elms);
    const url = new URL(urlDados, window.location.origin);
    for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
    url.searchParams.set('partial', '1');
    fetch(url.toString(), { credentials: 'same-origin' })
      .then(r => r.text())
      .then(html => { elms.alvo.innerHTML = html; })
      .catch(err => console.error('Erro ao atualizar tabela:', err));
  }

  function carregarTurmas(urlTurmas, selectTurma) {
    fetch(urlTurmas, { credentials: 'same-origin' })
      .then(r => r.json())
      .then(j => {
        selectTurma.innerHTML = '<option value="">-- selecione --</option>';
        (j.turmas || []).forEach(t => {
          const opt = document.createElement('option');
          opt.value = t.id; 
          opt.textContent = t.nome;
          selectTurma.appendChild(opt);
        });
      })
      .catch(err => console.error('Erro ao carregar turmas:', err));
  }

  function carregarAlunos(urlAlunos, turmaId, selectAluno) {
    if (!selectAluno) return;
    const url = new URL(urlAlunos, window.location.origin);
    if (turmaId) url.searchParams.set('turma_id', turmaId);
    fetch(url.toString(), { credentials: 'same-origin' })
      .then(r => r.json())
      .then(j => {
        selectAluno.innerHTML = '<option value="">-- selecione --</option>';
        (j.alunos || []).forEach(a => {
          const opt = document.createElement('option');
          opt.value = a.id; 
          opt.textContent = a.nome;
          selectAluno.appendChild(opt);
        });
      })
      .catch(err => console.error('Erro ao carregar alunos:', err));
  }

  function iniciar(cfg) {
    const elms = cfg.elementos;
    
    // Carrega turmas iniciais
    carregarTurmas(cfg.urls.turmas, elms.turma);
    
    // Configura event listeners
    if (elms.aluno) {
      elms.turma.addEventListener('change', () => {
        carregarAlunos(cfg.urls.alunos, elms.turma.value, elms.aluno);
        atualizarTabela(cfg.urls.dados, elms);
      });
      elms.aluno.addEventListener('change', () => atualizarTabela(cfg.urls.dados, elms));
    } else {
      elms.turma.addEventListener('change', () => atualizarTabela(cfg.urls.dados, elms));
    }
    
    if (elms.mes) {
      elms.mes.addEventListener('change', () => atualizarTabela(cfg.urls.dados, elms));
    }
    if (elms.ano) {
      elms.ano.addEventListener('change', () => atualizarTabela(cfg.urls.dados, elms));
    }

    // Configura botão de exportar
    if (cfg.botaoExportar && typeof cfg.onExportar === 'function') {
      cfg.botaoExportar.addEventListener('click', () => {
        cfg.onExportar(montarParams(elms));
      });
    }
  }

  return { iniciar };
})();
