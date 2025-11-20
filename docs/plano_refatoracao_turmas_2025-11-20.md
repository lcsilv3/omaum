# Plano de Refatoração – Módulo de Turmas
**Data:** 20/11/2025  
**Responsável:** GitHub Copilot (GPT-5.1-Codex)

## 1. Contexto e Objetivos
O módulo `turmas` precisa suportar novas regras de negócio envolvendo controle de datas, encerramento seguro e automações na criação e manutenção das turmas. O presente plano descreve, de forma sistemática e cruzada, as adequações necessárias em modelos, formulários, views, templates, integrações com atividades/presenças/frequências e documentação.

## 2. Diagnóstico Atual
### 2.1 Modelos (`turmas/models.py`)
- O modelo `Turma` possui campos de datas iniciáticas (`data_iniciacao`, `data_inicio_ativ`, `data_prim_aula`, `data_termino_atividades`), porém não existem `data_inicio` e `data_fim` dedicados ao ciclo administrativo da turma.
- Status/flags não impedem edições ou lançamentos quando uma turma deveria estar encerrada.

### 2.2 Formulários (`turmas/forms.py`)
- `TurmaForm` não expõe `data_inicio`/`data_fim`, tampouco validações específicas para encerramento.
- Validação existente cobre apenas datas iniciáticas e número de vagas.

### 2.3 Views (`turmas/views.py`)
- `criar_turma`/`editar_turma` trabalham somente com `TurmaForm`; não há lógica de encerramento, mensagens de confirmação ou logging.
- Não existe processo de transferência em lote nem criação automática de atividades padrão após salvar uma turma.

### 2.4 Templates (`turmas/templates/turmas/*.html`)
- As telas exibem campos `data_inicio` e `data_fim`, mas estão vazios porque o formulário não os fornece.
- Não há messaging específico sobre turmas encerradas.

### 2.5 Integrações com outros módulos
- `atividades`, `presencas` e `frequencias` permitem registrar dados vinculados a qualquer turma ativa no banco; nenhum bloqueio verifica se a turma possui data de fim.
- Não existe rotina para criar automaticamente atividades “Aula” e “Plenilúnio” associadas à nova turma.

### 2.6 Documentação
- Não há registro formal da regra de negócio sobre encerramento de turmas ou transferência em lote de alunos.

## 3. Requisitos de Negócio
1. Campos `data_inicio` e `data_fim` devem existir em `Turma`; `data_inicio` é obrigatório.
2. Ao preencher `data_fim`, a turma é considerada encerrada:
   - Nenhuma nova atividade, presença ou frequência pode ser adicionada/alterada.
   - O usuário deve confirmar o encerramento e receber mensagem clara.
   - Registrar em log (usuario, data/hora) o encerramento.
3. Após o encerramento, oferecer processo em lote para transferir todos os alunos para uma turma existente ou recém-criada.
4. Ao criar uma turma, registrar automaticamente duas atividades básicas: “Aula” e “Plenilúnio”.
5. Documentar as novas regras no diretório `docs/`.

## 4. Plano de Refatoração
### 4.1 Camada de Dados
1. **Novo migration** em `turmas/migrations/` adicionando campos:
   - `data_inicio = models.DateField(verbose_name="Data de Início", null=False)`
   - `data_fim = models.DateField(verbose_name="Data de Fim", blank=True, null=True)`
   - Campos auxiliares para logging de encerramento (ex.: `encerrada_em = models.DateTimeField(null=True, blank=True)` e `encerrada_por = models.ForeignKey(User, ...)`).
2. Atualizar `Turma` em `turmas/models.py` com validações:
   - `data_fim` não pode ser anterior a `data_inicio`.
   - Se `data_fim` estiver preenchida, `encerrada_em`/`encerrada_por` precisam ser definidos.
   - Propriedade `esta_encerrada` para facilitar verificações cruzadas.
3. Ajustar `__str__`, `ordering` e quaisquer consultas afetadas (`views` e relatórios) para incluir os novos campos.

### 4.2 Formulários
1. Atualizar `TurmaForm` para incluir `data_inicio` (obrigatório) e `data_fim` (opcional).
2. Adicionar validações específicas:
   - Forçar confirmação explícita (checkbox ou campo hidden) quando `data_fim` for preenchida.
   - Registrar usuário e horário do encerramento através da view (definir API do formulário para receber `request.user`).
3. Ajustar `help_texts`, `widgets` e mensagens de erro seguindo o padrão do projeto.

### 4.3 Views e Services
1. **Criação de turma (`criar_turma`)**
   - Após `form.save()`, usar um service (`turmas/services.py`) para gerar atividades “Aula” e “Plenilúnio”. O service deve usar `importlib.import_module` para acessar `atividades.models.Atividade` e criar registros relacionados.
2. **Edição (`editar_turma`)**
   - Detectar quando `data_fim` passa de vazio para preenchido e:
     - Exibir modal/mensagem de confirmação.
     - Invocar service de encerramento que grava `encerrada_em`, `encerrada_por` e registra via `logging.getLogger("turmas").info(...)`.
3. **Processo em lote de transferência**
   - Nova view (ex.: `transferir_alunos_turma`) que lista turmas encerradas e permite selecionar a turma destino.
   - Service dedicado para iterar sobre `Matricula` (via `importlib`) movendo alunos ativos.
   - Registrar em log cada transferência e exibir resumo ao usuário.
4. **Bloqueios de criação/edição**
   - Centralizar em um decorator/service (`turmas/services.py`) que valide `turma.esta_encerrada` e levante exceção/mensagem sempre que módulos `atividades`, `presencas` ou `frequencias` tentarem inserir dados.
   - Aplicar nas views correspondentes desses módulos (ex.: `atividades/views.py`, `presencas/views.py`, `frequencias/views.py`).

### 4.4 Templates e UX
1. Atualizar `turmas/templates/turmas/{criar,editar}_turma.html` e `turmas/templates/turmas/turma_form.html` para usar os novos campos do formulário, removendo referências obsoletas.
2. Adicionar mensagens Bootstrap explicando o estado “Turma encerrada” e desabilitar inputs quando `form.instance.esta_encerrada`.
3. Implementar modal de confirmação para encerramento.

### 4.5 Logging e Auditoria
1. Configurar logger específico (ex.: `LOGGING['loggers']['turmas']`) caso ainda não exista.
2. No service de encerramento, registrar `"Turma %s encerrada por %s em %s"` com nível INFO.
3. Opcional: adicionar model `TurmaEncerramentoHistorico` para rastrear múltiplos encerramentos (caso haja reabertura futura), documentando no plano.

### 4.6 Integração com outros módulos
1. **Atividades** (`atividades/views.py`, `atividades/services.py`): antes de criar/editar/excluir atividades, verificar `turma.esta_encerrada` e bloquear com mensagem.
2. **Presenças** (`presencas/views.py`, `presencas/services/`): impedir lançamentos e atualizações.
3. **Frequências** (`frequencias/views.py`): aplicar o mesmo bloqueio.
4. Garantir testes cobrindo esses fluxos, principalmente criando fixtures de turmas encerradas.

### 4.7 Processo em Lote
1. Criar formulário dedicado (`TransferenciaTurmaForm`) permitindo escolher turma origem (encerrada) e destino (ativa ou recém-criada).
2. Implementar service para mover matrículas:
   - Inativar matrículas na turma origem (status “T” – transferido) e criar novas matrículas na turma destino.
   - Emitir sinais/notificações conforme necessário (ex.: ajuste de presença pendente).
3. Disponibilizar relatório/log com resultado da transferência.

### 4.8 Documentação e Comunicação
1. Registrar a regra de encerramento e transferência em um novo capítulo do `docs/GUIA_DESENVOLVEDOR.md` ou documento dedicado.
2. Atualizar `MANUAL_USUARIO.md` com instruções de uso do fluxo (como encerrar turma, confirmar, transferir alunos).
3. Adicionar entrada no `docs/CHANGELOG.md` descrevendo as alterações.

### 4.9 Testes e QA
1. Criar testes unitários e de integração em `turmas/tests.py` cobrindo:
   - Validação de `data_inicio` obrigatória.
   - Proibição de alterações após `data_fim`.
   - Criação automática de atividades.
2. Adicionar testes nos módulos impactados (`atividades/tests.py`, `presencas/tests/*.py`, `frequencias/tests.py`).
3. Atualizar suites de smoke tests e watchers (vide tarefas cadastradas em `.vscode/tasks.json`).

## 5. Checklist de Implementação
- [x] Migration adicionando `data_inicio`, `data_fim`, `encerrada_em`, `encerrada_por`.
- [x] Atualização do modelo `Turma` e propriedades auxiliares.
- [x] Ajuste do `TurmaForm` e templates.
- [x] Services para encerramento (mensagens, logging) e criação automática de atividades.
- [x] Bloqueios nos módulos `atividades`, `presencas` e `frequencias`.
- [x] View/processo para transferência em lote de alunos.
- [x] Documentação e changelog atualizados.
- [x] Suite de testes cobrindo regras novas.

## 6. Status Atual – 20/11/2025
- **Fluxos implementados:** encerramento com auditoria, criação automática de “Aula”/“Plenilúnio”, transferência em lote e mensagens contextuais nas telas (`turmas/views.py`, `turmas/templates/turmas/*`).
- **Integrações protegidas:** `atividades.forms.AtividadeForm`, `presencas.forms.RegistrarPresencaForm` e `frequencias.forms.FrequenciaMensalForm` bloqueiam turmas encerradas; `presencas/views_main.py` reforça o bloqueio em runtime.
- **Testes adicionados:** `turmas/tests_encerramento.py` concentra os cenários de confirmação de encerramento, chamadas aos services e o fluxo de transferência com mocks; recomenda-se executar `python manage.py test turmas.tests_encerramento` antes dos testes completos do app.
- **Próximos passos operacionais:** monitorar logs de encerramento (`turmas.services.encerrar_turma`), validar templates customizados nos ambientes legados e atualizar manuais do usuário com capturas de tela do novo fluxo quando disponíveis; homologar o bloqueio recém-incluído em `RegistrarPresencaForm.clean` com usuários-chave.

---
Este plano serve como guia para execução controlada das mudanças, garantindo rastreabilidade e aderência às premissas especificadas pelo usuário.
