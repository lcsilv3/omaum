# Plano de Reforço das Regras de Encerramento e Exclusão de Turmas

**Data:** 20/11/2025  
**Responsável:** GitHub Copilot (GPT-5.1-Codex)  
**Escopo:** Aplicativos `turmas`, `matriculas`, `atividades`, `presencas`, `notas`, `pagamentos`, `relatorios_presenca`, `core`.

---

## 1. Diagnóstico Atual

1. A exclusão de turmas (`turmas.views.excluir_turma`) bloqueia operações se encontrar dependências em matrículas, atividades, registros de presença, notas ou pagamentos. Sem vínculos, a deleção é permitida.
2. O encerramento administrativo usa `Turma.data_fim` e o serviço `turma_services.encerrar_turma`, que apenas registra auditoria (`encerrada_em`, `encerrada_por`) e não aciona bloqueios automáticos nos demais apps.
3. `_bloquear_operacao_em_turma_encerrada` impede novas matrículas, mas cada módulo ainda precisa validar manualmente `esta_encerrada` para evitar alterações.
4. Não há hoje badge padronizada para “Encerrada”, tampouco distinção visual entre encerramento com/sem vínculos.
5. Não existe fluxo de reabertura pós-encerramento; remover a data fim é a única forma de “reabilitar” uma turma.

## 2. Regras Solicitadas

1. **Exclusão direta quando sem vínculos:** se nenhuma relação ativa estiver presente em qualquer módulo, a turma pode ser excluída imediatamente.
2. **Encerramento com vínculos:** ao confirmar o encerramento em uma turma com dependências, deve surgir badge "Encerrada" em vermelho e todos os módulos relacionados passam a negar alterações (somente leitura ou bloqueio de formulários) enquanto durar o estado.
3. **Reabertura controlada:** caso a turma tenha sido encerrada indevidamente, deve haver processo específico acessível apenas a administradores para reabilitar a turma (removendo bloqueios e auditorias com rastreabilidade).
4. **Encerramento sem vínculos:** quando a turma não tem dependências, apenas o badge "Encerrada" é exibido; não há bloqueios adicionais porque não subsistem dados acoplados.

## 3. Impacto Cruzado por Módulo

| Módulo | Impactos principais |
| --- | --- |
| `turmas` | Ajustar views/forms para avaliar dependências em ambos os fluxos (exclusão/encerramento), renderizar badge vermelho condicional e expor ação de reabertura com permissão restrita. |
| `matriculas` | Bloquear criação/edição/cancelamento quando `turma.esta_encerrada` e existirem vínculos. Liberar apenas consulta. |
| `atividades` | Travar associação/dissociação de turmas encerradas; impedir alterações em atividades vinculadas a turmas bloqueadas. |
| `presencas` | Impedir novos registros de presença, edição ou importações relacionadas à turma encerrada com vínculos. |
| `notas` | Proibir lançamento ou alteração de notas ligadas à turma enquanto bloqueada. |
| `pagamentos` | Manter somente leitura de pagamentos derivados de alunos/matrículas da turma bloqueada; impedir recalculo/edição. |
| `relatorios_presenca` | Ajustar filtros dinâmicos para mostrar badge e estado bloqueado, além de evitar callbacks que tentem atualizar dados. |
| `core` | Centralizar verificação de bloqueio para evitar lógica duplicada (ex.: service utilitário `turma_services.verificar_bloqueio_total`). |

## 4. Recomendações Técnicas

### 4.1 Exclusão sem dependências

- Reutilizar a rotina existente em `excluir_turma`, garantindo que a verificação considere todos os relacionamentos relevantes (incluindo pagamentos via `aluno__matricula__turma`).
- Caso nenhum resultado seja encontrado, seguir com `turma.delete()` sem popups adicionais.
- Registrar auditoria de exclusão no log para futura rastreabilidade.

### 4.2 Encerramento com dependências

1. **Detecção de vínculos:**
   - Criar helper `turma_services.listar_dependencias(turma)` retornando contagens por app.
   - Quando `data_fim` for preenchida e `listar_dependencias` retornar valores > 0, marcar flag interna `turma.bloqueio_total = True` (novo campo booleano sugerido) ou persistir estado derivado (`status_operacional = BLOQUEADA`).
2. **Badge e UI:**
   - Atualizar templates (`turmas/listar_turmas.html` e `detalhar_turma.html`) para renderizar badge vermelho quando `bloqueio_total` estiver ativo.
   - Incluir tooltip explicando que alterações estão suspensas por causa de vínculos.
3. **Bloqueio global:**
   - Adicionar decorator/validador compartilhado (ex.: `@bloqueia_turma_encerrada`) usado em views de `matriculas`, `atividades`, `presencas`, `notas`, `pagamentos`.
   - Retornar mensagem padrão: “Turma encerrada com vínculos. Operação disponível apenas em modo leitura.”
4. **Observabilidade:**
   - Registrar o usuário e timestamp que acionou o bloqueio.
   - Criar evento no log central (`logging.getLogger("turmas.bloqueios")`).

### 4.3 Reabertura restrita

- Expor ação “Reabrir turma” somente para usuários com `is_superuser` ou permissão customizada `turmas.pode_reabrir_turma`.
- Fluxo sugerido:
  1. Formulário exige justificativa obrigatória.
  2. Serviço `turma_services.reabrir_turma(turma, usuario, justificativa)` limpa `data_fim`, `encerrada_em`, `encerrada_por`, remove flag de bloqueio e cria entrada de auditoria reversa.
  3. Notificar via `messages.success` e registrar no log quem reabilitou.
- Caso existam dependências críticas (ex.: notas consolidadas), exigir confirmação dupla.

### 4.4 Encerramento sem vínculos

- Se `listar_dependencias` retornar zero, permitir encerramento normal (apenas `data_fim` + badge simples).
- Badge pode permanecer cinza, diferenciando visualmente do estado com bloqueio total.
- Nenhum bloqueio adicional é acionado.

## 5. Fluxos Operacionais

```
[Solicitar exclusão]
  └─> Verificar dependências → (zero) → Excluir imediatamente
                           └→ (existem) → Exibir mensagem e impedir exclusão

[Encerrar turma]
  └─> Definir data_fim → Calcular dependências
                       → (zero) → Registrar encerramento + badge cinza
                       → (existem) → Registrar encerramento + badge vermelho + bloquear módulos

[Reabrir turma]
  └─> Apenas administrador → fornecer justificativa → serviço reverte bloqueios e datas
```

## 6. Plano de Implementação

1. **Camada de serviço:** implementar `listar_dependencias`, `ativar_bloqueio_total`, `reabrir_turma` e atualizar `encerrar_turma` para usar essas funções.
2. **Modelos/migrações:** adicionar campos opcionais (`bloqueio_total`, `bloqueio_por`, `bloqueio_em`, `justificativa_reabertura`).
3. **Views/templates:**
   - Atualizar formulários de edição/exclusão para exibir badges e avisos.
   - Criar view de reabertura com permissão específica.
4. **Validações cruzadas:** aplicar decorator ou mixin de bloqueio nas views dos módulos afetados.
5. **Testes:**
   - Cobrir cenários com e sem dependências para exclusão.
   - Testar encerramento com vínculos garantindo que operações subsequentes sejam bloqueadas.
   - Verificar que apenas administradores conseguem reabrir e que auditoria é criada.
6. **Documentação/treinamento:** atualizar MANUAL_USUARIO e guias de instrutores para explicar os novos estados.

## 7. Casos de Teste Essenciais

1. **Exclusão direta:** criar turma sem vínculos e confirmar que a exclusão funciona de primeira.
2. **Exclusão bloqueada:** turma com matrículas deve apresentar mensagem de dependência e permanecer existente.
3. **Encerramento com vínculos:** após definir data_fim, verificar badge vermelho, logs e impedimento de criar novas presenças.
4. **Encerramento sem vínculos:** definir data_fim e observar apenas badge cinza, mantendo capacidade de exclusão futura.
5. **Reabertura autorizada:** admin consegue remover data_fim via fluxo dedicado; usuários comuns recebem 403.
6. **Auditoria:** logs e campos `encerrada_em/por` e justificativa de reabertura registrados corretamente.

---

**Próximos passos:** validar este plano com o time funcional, aprovar migração de dados para novos campos e então implementar conforme o cronograma definido em `plano_refatoracao_turmas_2025-11-20.md`.
