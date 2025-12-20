# Análise Inicial da Estrutura do Projeto OmAum

## Visão Geral do Projeto

O Sistema OMAUM é uma aplicação Django 4.2+ especializada em gestão acadêmica com foco no controle de presenças e frequência de alunos em atividades acadêmicas e ritualísticas.

## Estrutura de Apps Django

### Apps Principais Identificados:
1. **presencas/** - Sistema principal de controle de frequência ⭐
2. **alunos/** - Gestão de estudantes
3. **turmas/** - Organização de turmas e períodos
4. **atividades/** - Controle de atividades acadêmicas/ritualísticas
5. **cursos/** - Estrutura de cursos oferecidos
6. **core/** - Utilitários e configurações comuns
7. **matriculas/** - Gestão de matrículas
8. **notas/** - Sistema de notas
9. **pagamentos/** - Controle financeiro
10. **relatorios/** - Sistema de relatórios

## Análise do Sistema de Presenças (Módulo Principal)

### Modelos Identificados:

#### 1. ConvocacaoPresenca
- Representa convocação individual de aluno para atividade
- Campos: aluno, turma, atividade, data, convocado, registrado_por
- Unique constraint: aluno + turma + atividade + data

#### 2. Presenca (Modelo Base)
- Registro básico de presença/ausência
- Campos: aluno, atividade, turma, data, presente, justificativa
- Validações: data não pode ser futura

#### 3. PresencaDetalhada (Modelo Principal)
- Modelo expandido replicando funcionalidade Excel
- Campos Excel: C (Convocações), P (Presenças), F (Faltas), V1 (Voluntário Extra), V2 (Voluntário Simples)
- Campos calculados: percentual_presenca, total_voluntarios, carencias
- Unique constraint: aluno + turma + atividade + periodo

#### 4. ConfiguracaoPresenca
- Configurações específicas por turma/atividade
- Limites de carência por faixas percentuais (0-25%, 26-50%, 51-75%, 76-100%)
- Campos: obrigatoria, peso_calculo

#### 5. TotalAtividadeMes
- Totalização de atividades por mês/turma
- Campos: atividade, turma, ano, mes, qtd_ativ_mes

#### 6. ObservacaoPresenca
- Observações relacionadas à presença
- Campos: aluno, turma, data, atividade, texto

#### 7. AgendamentoRelatorio
- Sistema de agendamento automático de relatórios
- Múltiplos formatos: Excel, PDF, CSV
- Frequências: diário, semanal, mensal, etc.

### Estrutura de Views:
- **views/consolidado.py** - Relatórios consolidados
- **views/painel.py** - Dashboard estatísticas
- **views/registro_rapido.py** - Interface otimizada
- **views/exportacao_simplificada.py** - Exportações avançadas

## Análise do Modelo Aluno

### Estrutura Geográfica:
- **Pais** - Países com código ISO
- **Estado** - Estados brasileiros com regiões
- **Cidade** - Cidades com código IBGE

### Campos Identificados (parcial):
- Informações pessoais básicas
- Relacionamento com localização geográfica
- Sistema de validações

## Análise do Modelo Turma

### Campos Principais:
- **Informações básicas**: nome, curso, descrição
- **Campos específicos**: num_livro, perc_carencia, data_iniciacao
- **Datas importantes**: data_inicio_ativ, data_prim_aula, data_termino_atividades
- **Agendamento**: dias_semana, horario, local
- **Capacidade**: vagas, status (A/I/C/F)
- **Instrutores**: instrutor, instrutor_auxiliar, auxiliar_instrucao

### Propriedades Calculadas:
- vagas_disponiveis
- esta_ativa
- esta_em_andamento

## Tecnologias e Configurações

### Backend:
- Django 4.2+
- Django REST Framework
- PostgreSQL (produção) / SQLite (desenvolvimento)

### Frontend:
- Bootstrap 5
- jQuery
- Chart.js para gráficos
- Select2 para componentes avançados

### Configurações de Segurança:
- HSTS configurado
- SSL/HTTPS redirect
- Cookies seguros
- XSS e Content-Type protection

## Features Implementadas (v2.0)

### ✅ Sistema de Presenças:
- Registro Multi-etapas (5 etapas guiadas)
- Registro Rápido (interface AJAX)
- Cálculos automáticos (percentuais, carências)
- Configurações flexíveis por turma/atividade
- Validações robustas

### ✅ Relatórios e Análises:
- Painel de Estatísticas (Chart.js)
- Exportação avançada (Excel, PDF, CSV)
- Agendamento automático
- Relatórios consolidados

### ✅ API REST:
- Endpoints documentados
- Autenticação por token
- Rate limiting
- Versionamento

## Problemas Identificados Inicialmente

### 1. Nomenclatura Inconsistente:
- Campo `perc_carencia` deveria ser `perc_presenca` (conforme diretrizes)
- Falta campo "Número Iniciático" no modelo Aluno
- Falta mapeamento de situação do aluno (f/a/d/e)

### 2. Complexidade do Sistema:
- Múltiplos modelos para presença podem causar confusão
- Lógica de cálculo distribuída entre modelos
- Falta documentação clara das regras de negócio

### 3. Estrutura de Relatórios:
- Sistema atual não replica visualmente os relatórios Excel
- Falta interpretação clara das sheets (grau, mod, mes01-99, pcg)

### 4. Performance:
- Queries podem não estar otimizadas
- Cache pode não estar sendo usado eficientemente

## Próximos Passos

1. Análise detalhada dos cálculos de presença
2. Revisão da arquitetura de relatórios
3. Identificação de melhorias de performance
4. Proposta de nova implementação
5. Desenvolvimento de relatórios aprimorados

