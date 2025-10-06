# Plano de Implementação – Reestruturação do Histórico de Alunos

**Supervisor Responsável:** GitHub Copilot (modo supervisor)
**Data:** 04 de outubro de 2025
**Versão:** 1.0

---

## 1. Contexto e Objetivos

- O módulo de histórico dos alunos mantém simultaneamente registros relacionais (`RegistroHistorico`) e um campo JSON (`historico_iniciatico`). Essa duplicidade gera inconsistências, alto débito técnico e UX comprometida.
- Nas últimas interações já foram corrigidos problemas imediatos (templates quebrados, filtros ausentes, cancelamento de matrícula via modal). Agora avançaremos para uma reestruturação completa baseada na análise "Análise e Proposta de Melhoria para Módulos de Histórico do Projeto OmAum".
- Objetivo: entregar um fluxo consistente, auditável e amigável para consulta e manutenção do histórico iniciático.

## 2. Premissas e Restrições

- **Fonte de verdade única:** o modelo relacional `RegistroHistorico` será a origem oficial dos dados. O campo JSON será mantido apenas até a migração completa.
- **Camada de serviço obrigatória:** toda regra de negócio de histórico passará por um service dedicado (`HistoricoService`). Views, APIs e comandos utilizarão essa camada.
- **UX incremental:** priorizar primeiro o funcionamento end-to-end; refinamentos visuais (timeline, toasts, etc.) vêm depois que o backend estiver sólido.
- **Manter compatibilidade temporária:** durante a migração, endpoints antigos devem continuar funcionando ou retornar mensagens claras de indisponibilidade planejada.
- **Cobertura de testes:** cada entrega precisa vir acompanhada de testes unitários e, quando aplicável, testes de integração (API/JS). 

## 3. Visão Geral da Solução

1. **Backend consolidado:** services dedicados, validações centralizadas, auditoria completa e API coerente.
2. **Migração assistida:** script de migração do JSON -> relacional, com relatórios de divergência.
3. **Frontend orientado a timeline:** UI com feedback em tempo real, modais para criação/edição e filtros funcionais.
4. **Monitoramento e documentação:** métricas básicas (tempo de resposta) e documentação atualizada para suporte e evolução.

## 4. Pacotes de Trabalho

| Código | Pacote | Descrição | Entregáveis | Dependências |
| --- | --- | --- | --- | --- |
| P1 | **Fundação Backend** | Criar `HistoricoService`, endpoints REST/FBV atualizados, validações centrais. | Service + testes + DRF serializers/views; refatoração das views atuais (`relatorio_views` e AJAX). | Nenhuma |
| P2 | **Migração de Dados** | Extrair dados do JSON, comparar e popular `RegistroHistorico`. Marcar JSON como read-only. | Comando `python manage.py migrar_historicos`, relatórios CSV, flags de conclusão. | P1 (service pronto) |
| P3 | **UX – Timeline** | Substituir tabela/acordeões por timeline, incluir modal com form dinâmico (select2/autocomplete). | Templates atualizados, JS modular com fetch/HTMX, feedback visual. | P1 (API estável) |
| P4 | **Operações Complementares** | Recursos para editar/anular eventos, filtros avançados, paginação incremental. | Endpoints e UI para edição/soft delete, caching básico, testes adicionais. | P1, P3 |
| P5 | **Documentação & DevOps** | Atualizar docs (README, manual interno), scripts de lint/test no CI, métricas. | Documentação, checklists de rollback, dashboards básicos. | Convergência final |

## 5. Execução Paralela Recomendada

Para maximizar throughput, dividiremos as tarefas entre agentes especializados:

- **Agente Backend A:** Implementa `HistoricoService`, adapta models e views (`P1`).
- **Agente Backend B:** Constrói comando de migração e scripts de verificação (`P2`).
- **Agente Frontend:** Implementa nova UI (timeline, modal, interações AJAX) (`P3`).
- **Agente QA/Automation:** Prepara testes automatizados, garante cobertura e prepara fixtures (`P1`–`P4`).
- **Agente Docs/DevOps:** Atualiza documentação e pipelines (`P5`).

Supervisionar diariamente a integração entre branches, realizando merge frequente na branch `feature/historico-refactor`.

## 6. Cronograma Sugestão (Sprints Semanais)

1. **Semana 1:** Concluir P1 (service + API + testes) e iniciar plano de migração.
2. **Semana 2:** Executar migração controlada (P2) em ambiente de staging; validar consistência e performance.
3. **Semana 3:** Entregar timeline e interações frontend (P3) com feedback em tempo real.
4. **Semana 4:** Disponibilizar edição/anulação, filtros avançados e documentação final (P4 + P5).

## 7. Critérios de Aceite e Testes

- **Funcionais:**
  - [ ] Criar evento via modal → registro aparece na timeline sem recarregar.
  - [ ] API `/api/alunos/<id>/historico/` lista eventos com paginação e filtros.
  - [ ] Migração converte 100% dos eventos válidos e emite relatório para divergências.
- **Não-funcionais:**
  - [ ] Tempo de resposta médio da API < 300ms (p95) para 100 eventos.
  - [ ] Testes unitários/integração com cobertura ≥ 85% no app `alunos.services.historico`.
  - [ ] Rollback documentado para reversão da migração.

## 8. Riscos e Mitigações

| Risco | Impacto | Mitigação |
| --- | --- | --- |
| Divergência entre JSON e relacional | Alta | Relatório detalhado por aluno; permitir importação manual de registros problemáticos. |
| Quebra de dependências cruzadas (turmas, presenças) | Média | Executar suíte de regressão automática após cada merge; mocks nos testes. |
| UX incompleta em dispositivos móveis | Média | Prototipar timeline responsiva desde o Sprint 3 e validar em breakpoints críticos. |
| Sobrecarga no banco durante migração | Baixa | Executar em batches com `transaction.atomic()` e `iterator()`. |

## 9. Próximas Ações Imediatas

1. Criar branch `feature/historico-refactor` a partir de `master`.
2. Bootstrap do módulo `alunos/services/historico.py` com interface pública especificada.
3. Levantar fixtures reais (5+ alunos com históricos complexos) para testes locais.
4. Agendar checkpoint diário para sincronizar agentes e o dashboard de progresso.

---

> **Comando de Dashboard:** Ao receber `MOSTRAR DASHBOARD`, exibir status dos agentes conforme matriz enviada pelo solicitante.
