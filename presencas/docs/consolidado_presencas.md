# Consolidado de Presenças - Documentação

## Visão Geral

O sistema de Consolidado de Presenças é uma interface estilo Excel que permite visualizar, filtrar e editar dados de presenças de forma consolidada. Implementa a funcionalidade de planilha do Excel no Django, permitindo edição in-line e navegação horizontal entre atividades.

## Funcionalidades

### 1. Visualização Consolidada
- **Tabela estilo Excel**: Exibe dados em formato de planilha
- **Colunas fixas**: Nome do aluno e turma permanecem visíveis durante rolagem horizontal
- **Paginação horizontal**: Navega entre atividades (10 por página)
- **Cores por performance**: Células coloridas baseadas no percentual de presença

### 2. Filtros Avançados
- **Curso**: Filtra por curso específico
- **Turma**: Filtra por turma específica
- **Atividade**: Filtra por atividade específica
- **Período**: Define intervalo de datas
- **Nome do Aluno**: Busca por nome do aluno
- **Ordenação**: Ordena por diferentes campos

### 3. Edição In-line
- **Campos editáveis**: C, P, F, V1, V2
- **Salvamento automático**: AJAX salva alterações automaticamente
- **Validação**: Impede valores inválidos
- **Feedback visual**: Células ficam verdes após salvamento

### 4. Estatísticas
- **Resumo geral**: Total de registros, alunos únicos, atividades únicas
- **Totais**: Soma de convocações, presenças, faltas e voluntários
- **Média**: Percentual médio de presença

### 5. Exportação
- **Excel**: Exporta dados para arquivo Excel (.xlsx)
- **CSV**: Fallback para CSV se Excel não disponível
- **Filtros aplicados**: Exporta apenas dados filtrados

## Estrutura de Arquivos

```
presencas/
├── views/
│   ├── __init__.py
│   └── consolidado.py              # Views principais
├── templates/presencas/consolidado/
│   ├── consolidado.html            # Template principal
│   ├── filtros.html               # Template de filtros
│   └── partials/                  # Templates parciais
│       ├── celula_editavel.html
│       ├── percentual_cell.html
│       └── pagination.html
├── templatetags/
│   └── consolidado_tags.py         # Template tags customizados
├── tests/
│   └── test_consolidado.py         # Testes automatizados
├── docs/
│   └── consolidado_presencas.md    # Esta documentação
└── forms.py                        # Formulários estendidos
```

## URLs

```python
# Principais
/presencas/consolidado/                    # Página principal
/presencas/consolidado/filtros/            # Filtros avançados
/presencas/consolidado/exportar/           # Exportação Excel

# AJAX
/presencas/consolidado/?acao=salvar_celula       # Salvar célula
/presencas/consolidado/?acao=carregar_filtros    # Carregar filtros dinâmicos
```

## Uso

### 1. Acessar o Consolidado

```python
# URL name
reverse('presencas:consolidado')

# Com filtros
reverse('presencas:consolidado') + '?turma_id=1&periodo_inicio=2024-01-01'
```

### 2. Filtrar Dados

```python
# Via GET parameters
{
    'curso_id': 1,
    'turma_id': 2,
    'atividade_id': 3,
    'periodo_inicio': '2024-01-01',
    'periodo_fim': '2024-12-31',
    'aluno_nome': 'João',
    'ordenar_por': 'aluno__nome',
    'ordem': 'asc',
    'pagina_atividade': 1
}
```

### 3. Editar Dados via AJAX

```javascript
// Salvamento automático de célula
function salvarCelula(input) {
    const cell = input.closest('.celula-editavel');
    const presencaId = cell.getAttribute('data-presenca-id');
    const campo = cell.getAttribute('data-campo');
    const valor = input.value;
    
    fetch('/presencas/consolidado/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams({
            'acao': 'salvar_celula',
            'presenca_id': presencaId,
            'campo': campo,
            'valor': valor
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Sucesso
        } else {
            // Erro
        }
    });
}
```

### 4. Exportar Dados

```python
# View de exportação
class ExportarConsolidadoView(LoginRequiredMixin, View):
    def get(self, request):
        # Aplica mesmos filtros do consolidado
        # Gera arquivo Excel
        # Retorna response com arquivo
```

## Modelos de Dados

### PresencaDetalhada
```python
class PresencaDetalhada(models.Model):
    aluno = models.ForeignKey('alunos.Aluno', on_delete=models.CASCADE)
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE)
    atividade = models.ForeignKey('atividades.Atividade', on_delete=models.CASCADE)
    periodo = models.DateField()
    
    # Campos Excel
    convocacoes = models.PositiveIntegerField(default=0)      # C
    presencas = models.PositiveIntegerField(default=0)        # P
    faltas = models.PositiveIntegerField(default=0)           # F
    voluntario_extra = models.PositiveIntegerField(default=0)  # V1
    voluntario_simples = models.PositiveIntegerField(default=0) # V2
    
    # Calculados
    percentual_presenca = models.DecimalField(max_digits=5, decimal_places=2)
    total_voluntarios = models.PositiveIntegerField(default=0)
    carencias = models.PositiveIntegerField(default=0)
```

### ConfiguracaoPresenca
```python
class ConfiguracaoPresenca(models.Model):
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE)
    atividade = models.ForeignKey('atividades.Atividade', on_delete=models.CASCADE)
    
    # Limites de carência por faixa percentual
    limite_carencia_0_25 = models.PositiveIntegerField(default=0)
    limite_carencia_26_50 = models.PositiveIntegerField(default=0)
    limite_carencia_51_75 = models.PositiveIntegerField(default=0)
    limite_carencia_76_100 = models.PositiveIntegerField(default=0)
    
    obrigatoria = models.BooleanField(default=True)
    peso_calculo = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
```

## Personalização

### 1. CSS Customizado
```css
/* Cores dos percentuais */
.percentual-baixo { background-color: #ffe6e6; color: #d32f2f; }
.percentual-medio { background-color: #fff3cd; color: #856404; }
.percentual-alto { background-color: #d4edda; color: #155724; }

/* Colunas fixas */
.aluno-nome { position: sticky; left: 0; background-color: #f8f9fa; }
.turma-nome { position: sticky; left: 200px; background-color: #f8f9fa; }
```

### 2. Template Tags
```python
# Filtros customizados
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def percentage(value, total):
    return (value / total) * 100 if total > 0 else 0

@register.simple_tag
def get_percentual_class(percentual):
    if percentual < 50:
        return 'percentual-baixo'
    elif percentual < 75:
        return 'percentual-medio'
    else:
        return 'percentual-alto'
```

### 3. Configurações
```python
# settings.py
CONSOLIDADO_PRESENCAS = {
    'ATIVIDADES_POR_PAGINA': 10,
    'PERMITE_EDICAO_INLINE': True,
    'AUTOCOMPLETAMENTO_ATIVO': True,
    'SALVAR_AUTOMATICO': False,
    'CONFIRMAR_ANTES_SALVAR': True,
    'EXCEL_ENABLED': True,
    'CSV_FALLBACK': True,
}
```

## Segurança

### 1. Permissões
- **Visualização**: Usuários logados
- **Edição**: Usuários com permissão `presencas.change_presencadetalhada`
- **Exportação**: Usuários logados

### 2. Validações
- **Campos obrigatórios**: Validação no frontend e backend
- **Valores numéricos**: Apenas números inteiros positivos
- **Regras de negócio**: P + F ≤ C
- **CSRF**: Proteção contra ataques CSRF

### 3. Logs
```python
import logging
logger = logging.getLogger(__name__)

# Registra alterações
logger.info(f"Presença editada: {aluno.nome} - {atividade.nome} - {campo}: {valor}")
```

## Performance

### 1. Otimizações
- **Select Related**: Carrega relacionamentos em uma query
- **Paginação**: Limita atividades por página
- **Indexes**: Campos de filtro indexados
- **Cache**: Cache de consultas frequentes

### 2. Consultas Otimizadas
```python
# Carregamento eficiente
presencas = PresencaDetalhada.objects.select_related(
    'aluno', 'turma', 'atividade'
).filter(
    turma_id=turma_id
).order_by('aluno__nome')

# Paginação de atividades
paginator = Paginator(atividades, 10)
```

## Testes

### 1. Executar Testes
```bash
# Testes específicos do consolidado
python manage.py test presencas.tests.test_consolidado

# Todos os testes de presenças
python manage.py test presencas.tests
```

### 2. Cobertura de Testes
- **Views**: GET, POST, AJAX
- **Formulários**: Validação e limpeza
- **Models**: Cálculos e validações
- **Templates**: Renderização correta
- **Integração**: Workflow completo

### 3. Testes de Performance
```python
def test_consolidado_performance(self):
    """Testa performance com muitos dados."""
    import time
    start_time = time.time()
    
    response = self.client.get(reverse('presencas:consolidado'))
    
    end_time = time.time()
    load_time = end_time - start_time
    
    self.assertLess(load_time, 5.0)  # Deve carregar em menos de 5 segundos
```

## Manutenção

### 1. Logs de Erro
```python
# Verificar logs
tail -f /var/log/django/presencas.log

# Filtrar por consolidado
grep "consolidado" /var/log/django/presencas.log
```

### 2. Monitoramento
- **Tempo de resposta**: Consolidado deve carregar em < 3s
- **Erros AJAX**: Monitorar falhas de salvamento
- **Uso de memória**: Verificar com muitos dados

### 3. Backup
```bash
# Backup dos dados de presença
python manage.py dumpdata presencas.PresencaDetalhada > presencas_backup.json

# Restaurar
python manage.py loaddata presencas_backup.json
```

## Troubleshooting

### 1. Problemas Comuns

**Erro: "Sem permissão para editar"**
```python
# Verificar permissões do usuário
user.has_perm('presencas.change_presencadetalhada')

# Conceder permissão
user.user_permissions.add(permission)
```

**Erro: "Valor inválido"**
```python
# Validação no frontend
if (valor === '' || isNaN(valor) || valor < 0) {
    alert('Por favor, insira um valor válido.');
    return;
}
```

**Erro: "Carregamento lento"**
```python
# Otimizar queries
presencas = PresencaDetalhada.objects.select_related(
    'aluno', 'turma', 'atividade'
).prefetch_related(
    'turma__configuracoes_presenca'
)
```

### 2. Debug
```python
# Habilitar debug
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'presencas': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### 3. Ferramentas
- **Django Debug Toolbar**: Analisa queries SQL
- **django-extensions**: Comandos úteis de debug
- **django-silk**: Profiling de performance
