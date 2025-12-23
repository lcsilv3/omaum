# Plano de Refatoramento - Aplicativo Presenças

Documento vivo para acompanhar o refino do app Presenças. Atualize o status das fases e tarefas conforme avançar.

## Visao geral
- Objetivo: eliminar riscos de importacao circular, melhorar manutenibilidade e alinhar com convencoes do projeto.
- Escopo inicial: Fase 1 + admin.

## Fase 1 — Critico (CONCLUÍDA ✅)
- [x] Padronizar imports dinamicos com `importlib.import_module` em views/forms/servicos que ainda usam imports diretos de `alunos`, `turmas`, `atividades`, `cursos`.
- [x] Criar admin basico para `RegistroPresenca` (filtros, busca por CPF/nome, `raw_id_fields`, `date_hierarchy`).
- [x] Registrar `PresencaDetalhada` como read-only para debug.
- [x] Documentar o placeholder `ConfiguracaoPresenca` (modelo legado deprecado).

### Arquivos refatorados (Fase 1)
- `presencas/forms.py` - imports dinamicos
- `presencas/views_main.py` - imports dinamicos
- `presencas/views_new.py` - imports dinamicos
- `presencas/views.py` - imports dinamicos
- `presencas/views/consolidado.py` - imports dinamicos
- `presencas/views/registro_rapido.py` - imports dinamicos
- `presencas/views/exportacao_simplificada.py` - imports dinamicos
- `presencas/views_estatisticas.py` - imports dinamicos
- `presencas/views_ext/academicas.py` - imports dinamicos
- `presencas/views_ext/registro_presenca.py` - imports dinamicos + remover inline imports
- `presencas/api/views.py` - imports dinamicos
- `presencas/api_views.py` - imports dinamicos
- `presencas/bulk_operations.py` - imports dinamicos
- `presencas/admin.py` - admin completo criado (badges, filtros, search, raw_id_fields)
- `presencas/models.py` - docstring detalhada para ConfiguracaoPresenca

### Notas de implementacao
- Padrao adotado: `_get_model(app_name, model_name)` helper com `importlib.import_module`
- Todos imports diretos de `alunos`, `turmas`, `atividades`, `cursos` foram substituidos
- Admin implementado com badges coloridos, filtros avancados e otimizacoes (select_related)
- ConfiguracaoPresenca documentado como DEPRECADO com historico e orientacoes

## Fase 2 — Organizacao (80% CONCLUÍDA ⏳)
- [x] Modularizar `presencas/urls.py` em sub-rotas:
  - [x] urls_listagem.py (1 rota: root listing)
  - [x] urls_registro.py (15 rotas: wizard 5 passos + AJAX + filtros)
  - [x] urls_edicao.py (10 rotas: batch + individual edit)
  - [x] urls_detalhar.py (5 rotas: detail views)
  - [x] urls_operacoes.py (6 rotas: CRUD delete/export/import/auxiliares)
  - [x] Refatorar main urls.py (201 linhas → ~35 linhas com include())
  - [x] Remover app_name dos sub-módulos (evitar namespace duplicado)
- [x] Padronizar estrutura de views: mover `views_main.py` para `views/listagem.py` (consolidado com helpers para fluxos em desenvolvimento)
  - [x] Criar `views/listagem.py` com todo conteúdo de views_main.py
  - [x] Atualizar `views/__init__.py` para re-exportar todas as views
  - [x] Remover dependência de `views_main.py`, `views_new.py`, `views.py`
  - [x] Validar imports dinâmicos com _get_model()
- [x] Ajustar imports em todos os urls_*.py para usar .views ao invés de views_main
- [x] Testar reverse() URLs com novo namespace - OK ✅
- [ ] Consolidar testes em um unico diretorio `tests/` (migrar conteudo de `testsuite/`).

## Fase 3 — Qualidade de codigo (planejado)
- [ ] Refatorar `services/calculadora_estatisticas.py` em modulos menores (ex.: `consolidado_aluno.py`, `consolidado_turma.py`, `carencias.py`, `percentuais.py`) mantendo API publica.
- [ ] Adicionar type hints consistentes em services, repositories e forms.
- [ ] Revisar e padronizar `select_related/prefetch_related` em todos os fluxos.

## Fase 4 — Performance e robustez (planejado)
- [ ] Avaliar e adicionar indices em `RegistroPresenca` (ex.: `turma+data`, `atividade+data`, `status+data`).
- [ ] Cache adicional para listas de referencia e estatisticas pesadas (chaves com filtros).
- [ ] Auditoria leve (logs estruturados) para edicao em lote e inline.

## Fase 5 — Docs e DX (planejado)
- [ ] Corrigir linting Markdown em `consolidado_presencas.md` e `services/README.md` (MD022/MD031/MD032/MD040).
- [ ] Atualizar README local do app com arquitetura, fluxos (wizard, lote, inline) e convencoes de import dinamico.

## Registro de progresso
- **Data:** 23/12/2025
- **Responsavel:** Agente IA
- **Fase Atual:** Fase 2 (80% - Views)
- **Status:** ✅ EM ANDAMENTO - Reorganização de Views + URLs modularizado
- **Notas:**
  - Fase 1 (Imports + Admin): 100% CONCLUÍDA ✅
  - Fase 2 (URLs + Views):
    - URLs: 100% CONCLUÍDA ✅ (5 sub-módulos criados, refatoração feita, testes passando)
    - Views: 100% CONCLUÍDA ✅ (views_main.py movido para views/listagem.py, __init__.py re-exporta tudo)
    - Testes de consolidação: Pendente (80%)
  - Fase 3-5: Não iniciado

## Referencias
- Instrucoes do projeto: usar imports dinamicos para evitar circularidade.
- Apps relacionados: `alunos`, `turmas`, `atividades`, `cursos`, `relatorios_presenca`.
