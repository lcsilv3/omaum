# Manual do Usuário - Sistema de Presenças OMAUM

## Índice
1. [Introdução](#introdução)
2. [Acesso ao Sistema](#acesso-ao-sistema)
3. [Navegação Básica](#navegação-básica)
4. [Registro de Presenças](#registro-de-presenças)
5. [Consulta e Relatórios](#consulta-e-relatórios)
6. [Exportação de Dados](#exportação-de-dados)
7. [Configurações](#configurações)
8. [Resolução de Problemas](#resolução-de-problemas)
9. [FAQ](#faq)

## Introdução

O Sistema de Presenças OMAUM é uma ferramenta completa para controle de frequência de alunos em atividades acadêmicas e ritualísticas. Este manual guiará você através de todas as funcionalidades disponíveis.

### Principais Funcionalidades
- ✅ **Registro Multi-etapas**: Processo guiado para registro de presenças
- ⚡ **Registro Rápido**: Interface otimizada para registros em lote
- 📊 **Relatórios Consolidados**: Visão geral de presenças por período
- 📈 **Painel de Estatísticas**: Métricas e gráficos em tempo real
- 📄 **Exportação Avançada**: Múltiplos formatos (Excel, PDF, CSV)
- ⏰ **Agendamento Automático**: Relatórios periódicos por email

## Acesso ao Sistema

### 1. Login
1. Acesse a URL do sistema fornecida pelo administrador
2. Digite seu usuário e senha
3. Clique em "Entrar"

### 2. Perfis de Usuário
- **Administrador**: Acesso completo ao sistema
- **Coordenador**: Gestão de presenças e relatórios
- **Professor**: Registro de presenças das suas turmas
- **Visualizador**: Apenas consulta de dados

## Navegação Básica

### Menu Principal
O sistema possui navegação intuitiva através do menu lateral:

```
📋 Presenças
├── 📝 Registrar Presença
├── ⚡ Registro Rápido
├── 📊 Consolidado
├── 📈 Painel Estatísticas
├── 📄 Exportação
└── 📋 Listar Presenças
```

### Filtros e Busca
Todas as telas de listagem possuem:
- **Filtro por período**: Data início e fim
- **Filtro por turma**: Seleção de turma específica
- **Filtro por curso**: Filtragem por curso
- **Busca textual**: Por nome do aluno

## Registro de Presenças

### Método 1: Registro Multi-etapas (Recomendado para registros mensais)

#### Etapa 1: Dados Básicos
1. Acesse **"Presenças" → "Registrar Presença"**
2. Selecione o **Curso**
3. Escolha a **Turma**
4. Defina o **Período** (mês/ano)
5. Clique em **"Próximo"**

![Dados Básicos](screenshots/dados_basicos.png)

#### Etapa 2: Totais por Atividades
1. Para cada atividade da turma, informe:
   - **Quantidade no mês**: Total de atividades realizadas
   - **Observações**: Informações adicionais (opcional)
2. O sistema calculará automaticamente os limites baseados na configuração
3. Clique em **"Próximo"**

![Totais Atividades](screenshots/totais_atividades.png)

#### Etapa 3: Distribuição por Dias
1. Distribua as atividades pelos dias do mês
2. Use o calendário interativo para marcar os dias
3. O sistema validará se a distribuição está correta
4. Clique em **"Próximo"**

![Dias Atividades](screenshots/dias_atividades.png)

#### Etapa 4: Dados dos Alunos
1. Para cada aluno, informe:
   - **C (Convocações)**: Número de convocações
   - **P (Presenças)**: Número de presenças
   - **F (Faltas)**: Número de faltas
   - **V1 (Voluntário Extra)**: Atividades voluntárias extras
   - **V2 (Voluntário Simples)**: Atividades voluntárias simples
2. O sistema calculará automaticamente:
   - Percentual de presença
   - Total de voluntários
   - Carências
3. Clique em **"Confirmar"**

![Dados Alunos](screenshots/dados_alunos.png)

#### Etapa 5: Confirmação
1. Revise todos os dados informados
2. Confirme as informações calculadas
3. Clique em **"Salvar"** para finalizar

### Método 2: Registro Rápido (Para registros pontuais)

1. Acesse **"Presenças" → "Registro Rápido"**
2. Selecione a **Turma** e **Data**
3. A lista de alunos será carregada automaticamente
4. Marque **Presente/Ausente** para cada aluno
5. Adicione **Justificativas** para ausências
6. Clique em **"Salvar em Lote"**

#### Avisos de turma encerrada

- Um banner amarelo com ícone de cadeado é exibido quando a turma escolhida está encerrada administrativamente.
- Caso o formulário rejeite a turma, selecione outra turma ativa utilizando o campo de busca.
- Se precisar seguir com aquela turma, solicite aos administradores a reabertura no módulo **Turmas** antes de tentar novamente.


### Validações Automáticas

O sistema realiza as seguintes validações:
- ✅ **P + F ≤ C**: Presenças + Faltas não podem superar Convocações
- ✅ **Data futura**: Não permite registros em datas futuras
- ✅ **Justificativa**: Obrigatória para ausências
- ✅ **Duplicação**: Previne registros duplicados
- ✅ **Limites**: Respeita configurações de carência da turma
- ✅ **Turma ativa obrigatória**: Turmas encerradas exibem alerta e não aceitam novos lançamentos até serem reabertas em **Turmas**.

## Consulta e Relatórios

### 1. Listar Presenças

- Acesse **"Presenças" → "Listar Presenças"**
- Use os filtros para refinar a busca
- Visualize dados individuais ou em lote
- Ações disponíveis: Editar, Excluir, Detalhar

### 2. Consolidado de Presenças

- Acesse **"Presenças" → "Consolidado"**
- Aplique filtros de período, turma ou curso
- Visualize estatísticas agregadas:
  - Total de presenças por período
  - Percentuais por aluno
  - Ranking de frequência
  - Alunos com carência

### 3. Painel de Estatísticas

- Acesse **"Presenças" → "Painel Estatísticas"**
- Visualize gráficos interativos:
  - **Gráfico de Pizza**: Distribuição presença/ausência
  - **Gráfico de Barras**: Comparação entre turmas
  - **Gráfico de Linha**: Evolução temporal
  - **Indicadores**: KPIs principais

#### Principais Indicadores

- 📊 **Taxa de Presença Geral**: Percentual geral de presenças
- 👥 **Total de Alunos**: Quantidade de alunos no período
- 📚 **Atividades Registradas**: Total de atividades
- ⚠️ **Alunos com Carência**: Alunos abaixo do percentual mínimo

## Exportação de Dados

### Exportação Simples

1. Em qualquer listagem, clique em **"Exportar"**
2. Escolha o formato:
   - **Excel (.xlsx)**: Formato padrão para análise
   - **CSV (.csv)**: Para importação em outros sistemas
   - **PDF (.pdf)**: Para impressão e arquivamento

### Exportação Avançada

1. Acesse **"Presenças" → "Exportação"**
2. Configure as opções:
   - **Formato**: Excel Básico/Profissional, PDF, CSV
   - **Template**: Tipo de relatório
   - **Período**: Intervalo de datas
   - **Filtros**: Turma, curso, atividade
   - **Opções**: Gráficos, estatísticas, detalhamento
3. Clique em **"Gerar Relatório"**

### Formatos Disponíveis

#### Excel Profissional

- 📊 Gráficos automáticos
- 🎨 Formatação profissional
- 📈 Tabelas dinâmicas
- 🧮 Fórmulas e cálculos

#### PDF Completo

- 📄 Layout profissional
- 📊 Gráficos incorporados
- 📋 Sumário executivo
- 🖼️ Logotipo institucional

#### CSV Estruturado

- 📝 Dados tabulares limpos
- 🔗 Compatível com sistemas externos
- ⚡ Processamento rápido
- 📊 Ideal para análises

### Agendamento de Relatórios

1. Na tela de **Exportação Avançada**, clique em **"Agendar"**
2. Configure:
   - **Nome**: Identificação do agendamento
   - **Frequência**: Diário, semanal, mensal, etc.
   - **Formato**: Tipo de relatório desejado
   - **Destinatários**: Emails para envio
   - **Horário**: Hora de execução
3. O sistema enviará automaticamente os relatórios

## Configurações

### Configuração de Presença por Turma/Atividade
1. Acesse **Admin → Configurações de Presença**
2. Crie uma nova configuração para:
   - **Turma específica**
   - **Atividade específica**
3. Defina limites de carência por faixa percentual:
   - **0-25%**: Limite máximo para baixa frequência
   - **26-50%**: Limite para frequência regular
   - **51-75%**: Limite para boa frequência
   - **76-100%**: Limite para excelente frequência
4. Configure o **peso no cálculo** para a atividade

### Configuração de Turmas

- Acesse **Turmas** para configurar:
   - **Percentual mínimo de presença**
   - **Atividades obrigatórias**
   - **Período letivo**
- Utilize o mesmo cadastro para encerrar ou reabrir uma turma. Quando marcada como encerrada, o status "Encerrada" aparece no topo da tela e bloqueia registros de presenças, criação de atividades e lançamentos de frequência.
- Antes de tentar novos registros, confirme se o status está como "Ativa". Se precisar reabrir, use a ação apropriada no cadastro ou acione o administrador responsável.

### Bloqueios em Atividades e Frequências

- Em **Atividades → Nova Atividade Acadêmica**, um alerta amarelo informa que turmas encerradas não podem ser associadas no multi-selecionador.
- Em **Frequências → Registrar Frequência Mensal**, o formulário mostra mensagem equivalente e impede o salvamento quando a turma não está ativa.
- Os serviços internos utilizam a validação `turma_services.validar_turma_para_registro`, portanto a API também recusa operações com turmas encerradas.
- Verifique com a coordenação se a turma deve continuar encerrada antes de solicitar reabertura.

## Resolução de Problemas

### Problemas Comuns

#### ❌ "Erro ao salvar presença"

**Causa**: Dados inválidos ou conflitantes

**Solução**:

1. Verifique se P + F ≤ C
2. Confirme se a data não é futura
3. Adicione justificativa para ausências

#### ❌ "Presença já registrada"

**Causa**: Tentativa de duplicar registro

**Solução**:

1. Use a função "Editar" ao invés de criar novo registro
2. Verifique se o registro já existe na listagem

#### ❌ "Erro na exportação"

**Causa**: Volume muito grande de dados

**Solução**:

1. Aplique filtros para reduzir o volume
2. Use exportação por partes (períodos menores)
3. Tente em horário de menor uso do sistema

#### ❌ "Gráficos não carregam"

**Causa**: Problemas de navegador ou cache

**Solução**:

1. Atualize a página (F5)
2. Limpe o cache do navegador
3. Tente em modo anônimo/privado

#### ❌ "Turma encerrada não aceita novos lançamentos"

**Causa**: A turma foi encerrada administrativamente e está bloqueada para registros.

**Solução**:

1. Confirme se selecionou a turma correta e se ela deveria continuar encerrada.
2. Solicite a reabertura no módulo **Turmas** ou peça acesso a uma turma ativa.
3. Recarregue o formulário após a reabertura para que o alerta desapareça.

### Contato para Suporte

- **Email**: [suporte@omaum.edu.br](mailto:suporte@omaum.edu.br)
- **Telefone**: (11) 1234-5678
- **Horário**: Segunda a sexta, 8h às 18h

## FAQ

### 📋 Registro de Presenças

**P: Posso editar uma presença já registrada?**
R: Sim, use a opção "Editar" na listagem de presenças. Alterações são registradas no log do sistema.

**P: Como registro presenças para atividades extras?**
R: Use os campos V1 (Voluntário Extra) e V2 (Voluntário Simples) no registro multi-etapas.

**P: O que significa "carência"?**
R: Carência indica quantas presenças faltam para o aluno atingir o percentual mínimo da turma.

### 📊 Relatórios e Estatísticas

**P: Como interpretar o percentual de presença?**
R: É calculado como (Presenças ÷ Convocações) × 100. Considera apenas atividades obrigatórias.

**P: Por que alguns alunos não aparecem no relatório?**
R: Verifique se têm registros no período selecionado e se estão matriculados na turma.

**P: Posso personalizar os relatórios?**
R: Sim, use a Exportação Avançada para configurar formato, conteúdo e layout.

### 🔧 Configurações

**P: Como alterar o percentual mínimo de presença?**
R: Acesse Turmas → Editar → Configure o campo "Percentual de Carência".

**P: Posso ter configurações diferentes por atividade?**
R: Sim, crie configurações específicas em "Configurações de Presença".

### 📧 Agendamentos

**P: Como configurar relatórios automáticos?**
R: Use a função "Agendar" na Exportação Avançada. Configure frequência e destinatários.

**P: Posso parar um agendamento?**
R: Sim, acesse "Gerenciar Agendamentos" e desative ou exclua o agendamento desejado.

### 🔐 Permissões

**P: Não consigo acessar certas funcionalidades**
R: Verifique suas permissões com o administrador. Diferentes perfis têm acessos específicos.

**P: Como solicitar novas permissões?**
R: Entre em contato com o administrador do sistema informando sua função e necessidades.

### 📱 Acesso e Navegação

**P: O sistema funciona no celular?**
R: Sim, o sistema é responsivo e se adapta a dispositivos móveis.

**P: Posso usar o sistema offline?**
R: Não, é necessária conexão com internet para todas as funcionalidades.

---

*Este manual é atualizado periodicamente. Para a versão mais recente, acesse a seção de documentação do sistema.*
