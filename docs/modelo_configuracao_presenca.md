# Modelo ConfiguracaoPresenca

## Descrição

O modelo `ConfiguracaoPresenca` foi criado para gerenciar configurações específicas de presença por turma/atividade, replicando a lógica de carências do sistema Excel. Permite definir limites de carência baseados em faixas percentuais de presença.

## Estrutura do Modelo

### Relacionamentos

- **turma**: ForeignKey para `turmas.Turma`
- **atividade**: ForeignKey para `atividades.Atividade`
- **Unique constraint**: Combinação turma + atividade

### Campos de Configuração de Carências

#### Limites por Faixa Percentual

- **limite_carencia_0_25**: Limite máximo de carências para presença entre 0-25%
- **limite_carencia_26_50**: Limite máximo de carências para presença entre 26-50%
- **limite_carencia_51_75**: Limite máximo de carências para presença entre 51-75%
- **limite_carencia_76_100**: Limite máximo de carências para presença entre 76-100%

#### Configurações Gerais

- **obrigatoria**: Boolean indicando se a atividade é obrigatória
- **peso_calculo**: Decimal para ponderar o cálculo de carências
- **ativo**: Boolean para controle de status

### Campos de Controle

- **registrado_por**: Usuário que registrou a configuração
- **data_registro**: Data/hora de criação
- **data_atualizacao**: Data/hora de última atualização

## Métodos Principais

### `get_limite_carencia_por_percentual(percentual)`

Retorna o limite de carência apropriado baseado no percentual de presença.

**Parâmetros:**
- `percentual` (Decimal): Percentual de presença (0-100)

**Retorno:**
- `int`: Limite de carência correspondente

**Exemplo:**
```python
config = ConfiguracaoPresenca.objects.get(turma=turma, atividade=atividade)
limite = config.get_limite_carencia_por_percentual(Decimal('45.5'))
# Retorna limite_carencia_26_50
```

### `calcular_carencia_permitida(presenca_detalhada)`

Calcula a carência permitida para uma presença detalhada específica, aplicando o peso configurado.

**Parâmetros:**
- `presenca_detalhada` (PresencaDetalhada): Instância de presença detalhada

**Retorno:**
- `int`: Número de carências permitidas

**Exemplo:**
```python
config = ConfiguracaoPresenca.objects.get(turma=turma, atividade=atividade)
carencia_permitida = config.calcular_carencia_permitida(presenca_detalhada)
```

## Integração com PresencaDetalhada

O modelo `PresencaDetalhada` foi atualizado para usar as configurações do `ConfiguracaoPresenca`:

### Método `calcular_carencias()` Atualizado

1. **Prioridade**: Verifica se existe configuração específica para turma/atividade
2. **Configuração específica**: Usa limites e peso definidos em `ConfiguracaoPresenca`
3. **Fallback**: Usa lógica original baseada no percentual da turma

**Lógica de Cálculo:**
```python
def calcular_carencias(self):
    try:
        configuracao = ConfiguracaoPresenca.objects.get(
            turma=self.turma,
            atividade=self.atividade,
            ativo=True
        )
        
        percentual_atual = self.calcular_percentual()
        limite_carencia = configuracao.get_limite_carencia_por_percentual(percentual_atual)
        carencia_permitida = int(limite_carencia * float(configuracao.peso_calculo))
        
        if self.convocacoes > 0:
            presencas_necessarias = self.convocacoes - carencia_permitida
            carencias = max(0, presencas_necessarias - self.presencas)
            return carencias
        
        return 0
        
    except ConfiguracaoPresenca.DoesNotExist:
        # Fallback para lógica original
        # ...
```

## Validações

### Validação de Peso

- O peso no cálculo deve ser maior que zero
- Validação aplicada no método `clean()`

### Validação de Limites

- Todos os limites de carência devem ser não-negativos
- Validação aplicada no método `clean()`

### Unique Constraint

- Combinação turma + atividade deve ser única
- Previne configurações duplicadas

## Exemplos de Uso

### Criação de Configuração

```python
from presencas.models import ConfiguracaoPresenca
from decimal import Decimal

# Criar configuração para turma/atividade específica
config = ConfiguracaoPresenca.objects.create(
    turma=turma,
    atividade=atividade,
    limite_carencia_0_25=5,
    limite_carencia_26_50=3,
    limite_carencia_51_75=2,
    limite_carencia_76_100=1,
    obrigatoria=True,
    peso_calculo=Decimal('1.5'),
    registrado_por="Admin"
)
```

### Consulta de Configuração

```python
# Buscar configuração específica
config = ConfiguracaoPresenca.objects.get(
    turma=turma,
    atividade=atividade,
    ativo=True
)

# Listar configurações de uma turma
configs = ConfiguracaoPresenca.objects.filter(
    turma=turma,
    ativo=True
)
```

### Cálculo de Carências

```python
# Calcular carências para presença detalhada
presenca = PresencaDetalhada.objects.get(
    aluno=aluno,
    turma=turma,
    atividade=atividade,
    periodo=periodo
)

# O cálculo usa automaticamente a configuração se existir
carencias = presenca.calcular_carencias()
```

## Benefícios

1. **Flexibilidade**: Configurações específicas por turma/atividade
2. **Compatibilidade**: Mantém lógica original como fallback
3. **Escalabilidade**: Fácil expansão para novas regras
4. **Rastreabilidade**: Logs e controle de auditoria
5. **Validação**: Garantia de integridade dos dados

## Considerações de Migração

- Modelo compatível com estrutura existente
- Não afeta funcionalidade atual
- Adiciona funcionalidade opcional
- Permite migração gradual das configurações

## Próximos Passos

1. Criar migration para o novo modelo
2. Implementar interface administrativa
3. Criar formulários para configuração
4. Adicionar testes unitários
5. Documentar casos de uso específicos
