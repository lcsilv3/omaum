# Controle de Andamento das Tarefas - Projeto Omaum

## Como usar
- Atualize este arquivo sempre que iniciar, pausar ou concluir uma tarefa importante.
- Registre decisões, pendências, dúvidas e próximos passos.
- Use datas para facilitar o acompanhamento.
- Preencha o campo "Solicitação de origem" com o texto do pedido, número do chamado, ou contexto que originou a tarefa.
- Utilize os campos de responsável, prioridade e datas para facilitar o acompanhamento e retomada.

---

## Modelo de registro detalhado

### [DATA] - [TÍTULO DA TAREFA]
- **Solicitação de origem:** [Descreva o pedido, contexto, número do chamado, ou cole o texto da solicitação]
- **Responsável:** [Nome ou equipe]
- **Prioridade:** [Alta/Média/Baixa]
- **Status:** [Em andamento/Concluída/Pendente/Em validação]
- **Progresso:** [0-100%]
- **Data de início:** [dd/mm/aaaa]
- **Data de conclusão:** [dd/mm/aaaa ou em aberto]
- **O que já foi feito:**
  - [Itens já realizados]
- **O que falta:**
  - [Itens pendentes]
- **Próximos passos:**
  - [Ações imediatas]
- **Comentários/Observações:**
  - [Dúvidas, bloqueios, decisões tomadas, etc.]
- **Links relacionados:**
  - [Links para issues, PRs, documentos, etc.]

---

## Pendências gerais
- [ ] Finalizar interface de relatórios do app Alunos
- [ ] Ajustes visuais/funcionais conforme novas demandas
- [ ] Confirmar e/ou sugerir pontos de integração para matrícula de alunos em turmas, se necessário

---

## Tarefas de Refatoração e Funcionalidades

### Concluídas

1.  **[PRIORIDADE CRÍTICA] Refatorar Cargos, Iniciações e Punições para App Alunos**
    -   **Descrição**: Centralizar as funcionalidades de Cargos, Iniciações e Punições no app `alunos`, utilizando uma tabela de códigos unificada. O objetivo é simplificar a arquitetura, facilitar a manutenção e preparar o sistema para futuras expansões.
    -   **Status**: Concluído.
    -   **Responsável**: @Copilot
    -   **Prazo**: N/A

2.  **Remover Apps Obsoletos (Cargos, Iniciacoes, Punicoes)**
    -   **Descrição**: Após a validação completa da nova seção "Dados Iniciáticos", remover os aplicativos `cargos`, `iniciacoes` e `punicoes` do projeto para eliminar código legado.
    -   **Status**: Concluído.
    -   **Responsável**: @Copilot
    -   **Prazo**: N/A

3.  **Evoluir Relatórios (Turmas, Atividades, Presenças)**
    -   **Descrição**: Aprimorar os relatórios existentes para os aplicativos `turmas`, `atividades` e `presencas`, adicionando mais filtros, exportação para PDF e melhorando a visualização dos dados.
    -   **Status**: Concluído.
    -   **Responsável**: @Copilot
    -   **Prazo**: N/A

4.  **Revisar Usabilidade dos Formulários (Alunos, Turmas, Atividades, Presenças)**
    -   **Descrição**: Revisar e aprimorar a usabilidade dos formulários de cadastro e edição dos principais aplicativos, utilizando bibliotecas como `django-widget-tweaks` e `django-select2` para uma melhor experiência do usuário.
    -   **Status**: Concluído.
    -   **Responsável**: @Copilot
    -   **Prazo**: N/A

---

> Mantenha este arquivo atualizado para facilitar a retomada das tarefas após reinicializações ou trocas de responsável.
