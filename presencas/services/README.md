# Serviços de Presença

Este módulo contém os serviços especializados para o sistema de presenças, implementando a lógica de negócios complexa separada das views.

## CalculadoraEstatisticas

O serviço `CalculadoraEstatisticas` replica a funcionalidade das planilhas Excel, oferecendo cálculos estatísticos otimizados para o sistema de presenças.

### Principais Funcionalidades

#### 1. Cálculo Consolidado por Aluno
```python
from presencas.services.calculadora_estatisticas import CalculadoraEstatisticas

# Consolidado completo de um aluno
consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
    aluno_id=1,
    turma_id=1,  # opcional
    atividade_id=1,  # opcional
    periodo_inicio=date(2024, 1, 1),  # opcional
    periodo_fim=date(2024, 12, 31)  # opcional
)

# Resultado inclui:
# - Dados do aluno
# - Totais (C, P, F, V1, V2, carências)
# - Percentuais
# - Status (excelente, bom, regular, atenção, crítico)
# - Estatísticas por atividade
```

#### 2. Tabela Consolidada (Excel-like)
```python
# Gerar tabela consolidada completa
tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
    turma_id=1,  # opcional
    atividade_id=1,  # opcional
    periodo_inicio=date(2024, 1, 1),  # opcional
    periodo_fim=date(2024, 12, 31),  # opcional
    ordenar_por='nome'  # 'nome', 'percentual', 'carencias'
)

# Resultado inclui:
# - Array de linhas (alunos)
# - Estatísticas gerais
# - Filtros aplicados
# - Total de alunos
```

#### 3. Estatísticas da Turma
```python
# Estatísticas consolidadas da turma
estatisticas = CalculadoraEstatisticas.calcular_estatisticas_turma(
    turma_id=1,
    periodo_inicio=date(2024, 1, 1),  # opcional
    periodo_fim=date(2024, 12, 31)  # opcional
)

# Resultado inclui:
# - Dados da turma
# - Totais consolidados
# - Percentuais médios
# - Estatísticas por atividade
# - Estatísticas por aluno
# - Distribuição de carências
```

#### 4. Cálculo de Carências
```python
# Calcular carências para presença específica
resultado = CalculadoraEstatisticas.calcular_carencias(
    presenca_detalhada_id=1,
    forcar_recalculo=True  # opcional
)

# Recalcular todas as carências
resultado = CalculadoraEstatisticas.recalcular_todas_carencias(
    turma_id=1,  # opcional
    atividade_id=1,  # opcional
    periodo_inicio=date(2024, 1, 1),  # opcional
    periodo_fim=date(2024, 12, 31)  # opcional
)
```

### Estrutura dos Dados Retornados

#### Consolidado do Aluno
```python
{
    'aluno': {
        'id': 1,
        'nome': 'João Silva',
        'cpf': '12345678901'
    },
    'periodo': {
        'inicio': date(2024, 1, 1),
        'fim': date(2024, 12, 31)
    },
    'totais': {
        'convocacoes': 100,
        'presencas': 80,
        'faltas': 20,
        'voluntario_extra': 5,
        'voluntario_simples': 3,
        'total_voluntarios': 8,
        'carencias': 2,
        'registros': 12
    },
    'percentuais': {
        'presenca': 80.0,
        'faltas': 20.0
    },
    'status': 'bom',
    'atividades': [
        {
            'id': 1,
            'nome': 'Atividade A',
            'convocacoes': 50,
            'presencas': 40,
            'faltas': 10,
            'percentual': 80.0
            # ... outros campos
        }
    ],
    'data_calculo': datetime(2024, 1, 15, 10, 30, 0)
}
```

#### Tabela Consolidada
```python
{
    'linhas': [
        {
            'aluno': { 'id': 1, 'nome': 'João Silva', 'cpf': '12345678901' },
            'turma': { 'id': 1, 'nome': 'Turma A' },
            'totais': { 'convocacoes': 100, 'presencas': 80, ... },
            'percentual_geral': 80.0,
            'total_voluntarios': 8,
            'status': 'bom',
            'atividades': [...]
        }
    ],
    'estatisticas_gerais': {
        'total_alunos': 25,
        'percentual_medio': 78.5,
        'total_convocacoes': 2500,
        'total_presencas': 1962,
        'total_carencias': 45
    },
    'filtros_aplicados': {
        'turma_id': 1,
        'atividade_id': null,
        'periodo_inicio': date(2024, 1, 1),
        'periodo_fim': date(2024, 12, 31),
        'ordenar_por': 'nome'
    },
    'total_alunos': 25,
    'data_geracao': datetime(2024, 1, 15, 10, 30, 0)
}
```

### Status dos Alunos

O sistema classifica automaticamente os alunos em:

- **Excelente**: ≥90% presença e 0 carências
- **Bom**: ≥80% presença e ≤2 carências
- **Regular**: ≥70% presença e ≤5 carências
- **Atenção**: ≥60% presença
- **Crítico**: <60% presença

### Integração com ConfiguracaoPresenca

O serviço utiliza automaticamente as configurações específicas de presença:

1. **Prioridade**: Configuração específica turma/atividade
2. **Fallback**: Percentual de carência da turma
3. **Padrão**: Sem carência se não houver configuração

### Otimizações de Performance

- **Select Related**: Carrega relacionamentos em uma única query
- **Prefetch Related**: Otimiza queries para relacionamentos N:N
- **Agregações**: Usa agregações do Django ORM para cálculos
- **Caching**: Calcula campos automáticos apenas quando necessário

### Exemplo de Uso em Views

```python
# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .services.calculadora_estatisticas import CalculadoraEstatisticas

def relatorio_turma(request, turma_id):
    try:
        # Obter parâmetros da requisição
        periodo_inicio = request.GET.get('periodo_inicio')
        periodo_fim = request.GET.get('periodo_fim')
        ordenar_por = request.GET.get('ordenar_por', 'nome')
        
        # Converter datas se fornecidas
        if periodo_inicio:
            periodo_inicio = datetime.strptime(periodo_inicio, '%Y-%m-%d').date()
        if periodo_fim:
            periodo_fim = datetime.strptime(periodo_fim, '%Y-%m-%d').date()
        
        # Gerar tabela consolidada
        tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
            turma_id=turma_id,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
            ordenar_por=ordenar_por
        )
        
        # Para requisições AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(tabela)
        
        # Para renderização HTML
        return render(request, 'presencas/relatorio_turma.html', {
            'tabela': tabela,
            'turma_id': turma_id
        })
        
    except ValidationError as e:
        return JsonResponse({'erro': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'erro': 'Erro interno do servidor'}, status=500)

def consolidado_aluno(request, aluno_id):
    try:
        consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
            aluno_id=aluno_id,
            turma_id=request.GET.get('turma_id'),
            atividade_id=request.GET.get('atividade_id')
        )
        
        return JsonResponse(consolidado)
        
    except ValidationError as e:
        return JsonResponse({'erro': str(e)}, status=400)
```

### Logs e Monitoramento

O serviço registra logs detalhados para:
- Cálculos realizados
- Erros e exceções
- Performance de queries
- Atualizações de carências

### Tratamento de Erros

- **ValidationError**: Para erros de validação e dados inválidos
- **Logging**: Registra erros para debug
- **Fallbacks**: Retorna estruturas vazias quando não há dados
- **Transações**: Garante consistência em operações críticas

### Testes

Execute os testes com:
```bash
python manage.py test presencas.tests.test_calculadora_estatisticas
```

Os testes cobrem:
- Cálculos com e sem dados
- Diferentes cenários de carências
- Filtros e ordenação
- Performance e otimização
- Tratamento de erros
