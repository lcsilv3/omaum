# Plano de Implementação de Relatórios do Módulo Atividades

## 1. Visão Geral
- **Objetivo**: ampliar a inteligência operacional do módulo Atividades, fornecendo relatórios estratégicos integrados com Cursos, Turmas, Alunos, Presenças e Frequências.
- **Escopo inicial**: manter o relatório atual ("Relatório de Atividades") e adicionar cinco relatórios complementares, cada um com exportação CSV/Excel/PDF e filtros dinâmicos via AJAX.
- **Premissas-chave**: views function-based, imports dinâmicos com `importlib.import_module`, cabeçalhos padronizados, zero regressões em funcionalidades existentes, nomenclatura de URLs conforme convenções oficiais, documentação e testes atualizados.

## 2. Relatórios Planejados
### 2.1 Relatório de Participação por Atividade
- **Objetivo**: medir adesão dos participantes (presentes, faltas, justificativas, voluntários) por atividade.
- **Fontes de dados**: `atividades.Atividade`, `presencas.RegistroPresenca`, `turmas.Turma`, `alunos.Aluno`.
- **Filtros**: curso, turma, tipo de atividade, status da atividade, intervalo de datas.
- **Exportações**: CSV, Excel, PDF.

### 2.2 Relatório de Carga de Instrutores
- **Objetivo**: consolidar agenda ministrada por instrutores principais, auxiliares e auxiliares de instrução.
- **Fontes**: `turmas.Turma`, `atividades.Atividade`, `alunos.Aluno`.
- **Filtros**: instrutor, curso, status da turma, período.
- **Métricas**: quantidade de atividades por papel, horas planejadas (hora início/fim), status de execução.

### 2.3 Relatório de Carências e Frequência por Turma
- **Objetivo**: acompanhar percentuais de frequência e carências identificadas para cada turma.
- **Fontes**: `frequencias.FrequenciaMensal`, `frequencias.Carencia`, `atividades.Atividade`, `presencas.RegistroPresenca`, `matriculas.Matricula`.
- **Filtros**: curso, turma, mês/ano, status da carência.
- **Métricas**: total de atividades no período, presenças, percentual de aderência, alunos com carência.

### 2.4 Relatório Cronograma Curso × Turmas
- **Objetivo**: visualizar o cronograma completo (planejado x realizado) por curso e turma.
- **Fontes**: `cursos.Curso`, `turmas.Turma`, `atividades.Atividade`.
- **Filtros**: curso, turma, responsável, status, intervalo de datas.
- **Métricas**: atividades confirmadas/realizadas/canceladas, atrasos e adiantamentos.

### 2.5 Relatório Histórico de Participação do Aluno
- **Objetivo**: rastrear todas as participações e atuações de um aluno (participante, instrutor, voluntário).
- **Fontes**: `alunos.Aluno`, `atividades.Atividade`, `presencas.RegistroPresenca`, `turmas.Turma`.
- **Filtros**: aluno, curso, papel desempenhado, período.
- **Resultado**: linha do tempo com status de presença e funções assumidas.

## 3. Arquitetura de Código e Componentes
| Camada | Componentes | Descrição |
| --- | --- | --- |
| **Services** | `atividades/services/relatorios_participacao.py`, `relatorios_instrutores.py`, `relatorios_frequencia.py`, `relatorios_cronograma.py`, `relatorios_historico_aluno.py` | Cada arquivo conterá funções puras que consultam os modelos via imports dinâmicos, agregam métricas e retornam estruturas prontas para renderização/exportação. |
| **Views** | `atividades/views_ext/relatorios.py` | Adição de views para os novos relatórios e exportadores (`relatorio_*`, `exportar_*_<formato>`), mantendo cabeçalho padrão (`_cabecalho_relatorio`). |
| **URLs** | `atividades/urls.py` | Rotas nomeadas seguindo o padrão corporativo (ex.: `relatorio_participacao_atividades`, `exportar_participacao_csv`). |
| **Templates HTML** | `atividades/templates/atividades/relatorio_*.html` | Estendem `base_relatorio.html`, incluem filtros dinâmicos e tabelas responsivas. |
| **Templates PDF** | `atividades/templates/atividades/relatorio_*_pdf.html` | Mantêm tipografia 12 pt/10 pt/9 pt, cabeçalho flex (subtítulo + data). |
| **AJAX Partials** | `atividades/templates/atividades/partials/` | Includes para tabelas e selects, garantindo comportamento sem recarregar a página. |
| **Scripts de Exportação** | Reutilização das views de exportação para CSV/Excel/PDF com `HttpResponse`. |

## 4. Sequenciamento de Entrega
1. **Preparação**
   - Criar services e testes base para cada relatório.
   - Garantir cobertura mínima de testes de unidade nas funções de agregação.
2. **Relatório de Participação por Atividade**
   - Implementar service, view, URLs, templates, exportações e AJAX.
   - Testes de integração (views) + snapshot dos exports.
3. **Relatório de Carga de Instrutores**
   - Repetir ciclo: service → view → templates → exportação → AJAX → testes.
4. **Relatório de Carências e Frequência**
   - Integrar `FrequenciaMensal.calcular_carencias` dentro do service para recalcular sob demanda (quando autorizado) ou consumir dados já persistidos.
5. **Relatório Cronograma Curso × Turmas**
   - Focar em dashboards hierárquicos (Curso → Turma → Atividades), com destaques para atrasos.
6. **Relatório Histórico de Participação do Aluno**
   - Consolidar timeline e exportações.
7. **Documentação & Ajustes Finais**
   - Atualizar `docs/` com instruções operacionais, screenshots e fluxo de uso.
   - Rodar suíte de testes (`python manage.py test atividades presencas frequencias`) e lint (`scripts/lint.py`).

## 5. Paralelismo e Orquestração
- **Divisão por agentes/processos**: cada relatório pode ser tratado como um fluxo independente (service + view + templates), permitindo equipes/agentes paralelos.
- **Sincronização**: um revisor valida padrões de estilo, cabeçalho e nomenclatura de URLs ao final de cada ciclo.
- **Tarefas em lote**: exportações CSV/Excel podem reutilizar estruturas pandas existentes; scripts shell podem ser executados em paralelo com watchers já configurados (monitoramento Ruff, testes rápidos de presenças).

## 6. Testes e Qualidade
- **Testes Unitários**: services com dados sintéticos cobrindo filtros e métricas críticas (presença total, percentual mínimo, horas planejadas).
- **Testes de Integração**: views usando `Client` do Django para garantir status 200, resposta JSON nos endpoints AJAX, e funcionamento das exportações.
- **Testes Visuais**: geração manual de PDFs para validação do cabeçalho e layout.
- **Automação**: considerar fixtures dedicadas em `atividades/tests/fixtures` para reuso nos novos testes.

## 7. Riscos e Mitigações
| Risco | Mitigação |
| --- | --- |
| Volume de dados elevado em exportações | Paginação ou streaming nos exports (avaliar após primeiro teste). |
| Divergência de filtros dinâmicos | Reutilizar lógica de `listar_atividades_academicas` como referência, adicionando testes específicos para AJAX. |
| Inconsistência de horários | Validar e normalizar campos `hora_inicio`/`hora_fim` ao calcular carga de instrutores. |
| Dependência de dados de carência | Service deve verificar se há registros para o período; caso contrário, sinalizar necessidade de execução de `calcular_carencias`. |

## 8. Próximos Passos
1. Validar este plano com stakeholders (Coordenação OMAUM) e priorizar a ordem de desenvolvimento.
2. Alocar agentes ou membros da equipe para cada relatório (padrão: service + view + template + testes).
3. Iniciar pela participação por atividade, por ser base para correlações com frequência.
4. Após cada entrega, atualizar documentação, CHANGELOG e rodar suite de testes/lint.

---
*Documento gerado em 14/10/2025. Supervisão técnica: Equipe Django OMAUM.*
