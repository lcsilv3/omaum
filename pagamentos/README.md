# Módulo de Pagamentos

Este módulo gerencia os pagamentos dos alunos, permitindo o registro, acompanhamento e relatórios financeiros.

## Funcionalidades

- Registro de pagamentos
- Acompanhamento de status (pendente, pago, cancelado)
- Relatórios financeiros
- Exportação de dados
- Notificações de pagamentos atrasados

## Modelos de Dados

### Pagamento
- **aluno**: Referência ao aluno
- **valor**: Valor do pagamento
- **data_pagamento**: Data em que o pagamento foi realizado
- **status**: Status do pagamento (pendente, pago, cancelado)
- **data_vencimento**: Data de vencimento
- **matricula**: Referência à matrícula (opcional)
- **metodo_pagamento**: Método utilizado para pagamento
- **comprovante**: Arquivo de comprovante (opcional)

## Fluxo de Trabalho

1. Criação de pagamento (manual ou automático via matrícula)
2. Acompanhamento de status
3. Registro de pagamento quando efetuado
4. Geração de relatórios e análises
```

**Restam 14 alterações**

### 2. Criar documentação para o módulo de Notas
**Caminho:** `notas/README.md`
```markdown
# Módulo de Notas

Este módulo gerencia as notas dos alunos, permitindo o registro, acompanhamento e relatórios acadêmicos.

## Funcionalidades

- Registro de notas por aluno, curso e turma
- Diferentes tipos de avaliação
- Cálculo de médias
- Relatórios acadêmicos
- Exportação de dados

## Modelos de Dados

### Nota
- **aluno**: Referência ao aluno
- **curso**: Referência ao curso
- **turma**: Referência à turma
- **valor**: Valor da nota
- **data**: Data da avaliação
- **tipo_avaliacao**: Tipo de avaliação
- **peso**: Peso da nota no cálculo da média
- **observacoes**: Observações adicionais

## Fluxo de Trabalho

1. Registro de avaliação
2. Lançamento de notas
3. Cálculo automático de médias
4. Geração de relatórios acadêmicos