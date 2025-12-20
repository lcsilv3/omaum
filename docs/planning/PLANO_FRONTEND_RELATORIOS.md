# Plano de Ação – Finalização do Frontend dos Relatórios OmAum

## Objetivo
Finalizar a entrega do módulo de relatórios, implementando todos os templates HTML, elementos de interface e integrações JavaScript necessários para que os recursos já prontos no backend estejam acessíveis e utilizáveis pelo usuário final.

---

## 1. Boletim de Frequência do Aluno

### 1.1. Criar o template principal `boletim_frequencia_aluno.html`
- Filtros: Curso, Turma, Aluno, Mês, Ano (combos e inputs).
- Botão "Buscar" para carregar o boletim via AJAX.
- Botões "Exportar CSV" e "Exportar PDF".
- Área/container para a tabela do boletim (renderizada via AJAX).
- Mensagens de validação e carregamento.

### 1.2. Criar o template parcial `_boletim_frequencia_aluno_tabela.html`
- Renderiza apenas a tabela de dados do boletim do aluno.
- Usado para atualização dinâmica via AJAX.

### 1.3. Ajustar/confirmar o JavaScript
- Garantir que o JS orquestra:
  - Atualização dos combos (Curso → Turma → Aluno).
  - Chamada AJAX para buscar e renderizar a tabela do boletim.
  - Exportação CSV/PDF via chamada GET.

---

## 2. Exportação PDF e Botões

### 2.1. Adicionar botões "Exportar PDF" e "Exportar CSV"
- Nos templates dos relatórios:
  - Consolidado de Presença
  - Boletim de Frequência do Aluno
  - Frequência por Atividade
  - Alunos com Carência
- Garantir que os botões disparam as URLs de exportação já implementadas no backend.

---

## 3. Relatórios Adicionais

### 3.1. Frequência por Atividade
- Criar o template `frequencia_por_atividade.html`:
  - Filtros: Turma, Atividade, Período.
  - Botão "Buscar".
  - Botões de exportação.
  - Tabela de resultados.
  - Mensagens de validação/carregamento.

### 3.2. Alunos com Carência
- Criar o template `alunos_com_carencia.html`:
  - Filtros: Curso, Turma, Período.
  - Botão "Buscar".
  - Botões de exportação.
  - Tabela de resultados.
  - Mensagens de validação/carregamento.

### 3.3. Relatório de Faltas
- Desenvolver a view (se necessário) e o template `relatorio_faltas.html`:
  - Filtros: Turma, Período.
  - Botão "Buscar".
  - Botões de exportação.
  - Tabela de resultados.
  - Mensagens de validação/carregamento.

---

## 4. Testes e Validação
- Validar que todos os filtros, buscas e exportações funcionam corretamente.
- Garantir responsividade e acessibilidade dos templates.
- Revisar mensagens de erro e feedback visual.

---

## 5. Checklist Final
- [ ] Todos os templates criados e integrados.
- [ ] Botões de exportação presentes e funcionais.
- [ ] Filtros dinâmicos e AJAX funcionando.
- [ ] Testes manuais realizados.
- [ ] Documentação atualizada se necessário.

---

*Plano gerado automaticamente em 16/09/2025 para garantir a entrega completa do frontend dos relatórios OmAum.*
