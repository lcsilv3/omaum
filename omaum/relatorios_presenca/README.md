# App Relatórios de Presença e Frequência

Sistema completo para geração de relatórios de presença e frequência no projeto OmAum, implementado seguindo as premissas estabelecidas e mantendo fidelidade visual aos formatos Excel existentes.

## 📋 Visão Geral

Este app substitui o sistema de relatórios anterior, oferecendo:

- **Modelo Unificado**: `RegistroPresenca` centraliza toda a lógica de presença
- **Fidelidade Visual**: Relatórios Excel idênticos aos formatos originais
- **Filtros Dinâmicos**: Interface AJAX responsiva e interdependente
- **Arquitetura Robusta**: Services, generators e views bem estruturados

## 🏗️ Arquitetura

### Modelos

#### `RegistroPresenca`
Modelo unificado que substitui `Presenca`, `PresencaDetalhada` e `ConvocacaoPresenca`:

```python
class RegistroPresenca(models.Model):
    aluno = models.ForeignKey("alunos.Aluno", ...)
    turma = models.ForeignKey("turmas.Turma", ...)
    atividade = models.ForeignKey("atividades.Atividade", ...)
    data = models.DateField(...)
    status = models.CharField(choices=[
        ('P', 'Presente'),
        ('F', 'Falta'),
        ('J', 'Falta Justificada'),
        ('V1', 'Voluntário Extra'),
        ('V2', 'Voluntário Simples'),
    ])
    # ... outros campos
```

#### Modelos de Configuração
- `ConfiguracaoRelatorio`: Templates e configurações
- `HistoricoRelatorio`: Rastreamento de relatórios gerados
- `AgendamentoRelatorio`: Relatórios automáticos
- `TemplatePersonalizado`: Templates customizados

### Services

#### `RelatorioPresencaService`
Centraliza toda a lógica de negócio para geração de dados:

```python
service = RelatorioPresencaService()

# Relatório consolidado
dados = service.obter_dados_consolidado_periodo(turma_id, data_inicio, data_fim)

# Relatório mensal
dados = service.obter_dados_apuracao_mensal(turma_id, ano, mes)

# Formulário de coleta
dados = service.obter_dados_formulario_coleta(turma_id, ano, mes)

# Controle geral
dados = service.obter_dados_controle_geral(turma_id)
```

### Generators

#### `ExcelRelatorioGenerator`
Gera relatórios Excel com fidelidade visual:

```python
generator = ExcelRelatorioGenerator()

# Gerar consolidado
arquivo = generator.gerar_consolidado_periodo(dados)

# Gerar mensal
arquivo = generator.gerar_apuracao_mensal(dados)

# Gerar formulário
arquivo = generator.gerar_formulario_coleta(dados)

# Gerar controle geral
arquivo = generator.gerar_controle_geral(dados)
```

## 📊 Tipos de Relatórios

### 1. Consolidado por Período (`grau`)
- **Objetivo**: Visão consolidada da presença por período
- **Formato**: Alunos (linhas) × Meses (colunas)
- **Dados**: P, F, J, V1, V2 por mês + totais + percentual

### 2. Apuração Mensal (`mes01-99`)
- **Objetivo**: Detalhamento de presença por mês
- **Formato**: Alunos (linhas) × Dias do mês (colunas)
- **Dados**: Status por dia + totais mensais

### 3. Formulário de Coleta (`mod`)
- **Objetivo**: Template para coleta manual
- **Formato**: Planilha em branco para preenchimento
- **Dados**: Estrutura de alunos e dias para input manual

### 4. Controle Geral da Turma (`pcg`)
- **Objetivo**: Informações completas da turma
- **Formato**: Relatório estruturado
- **Dados**: Dados da turma, estatísticas, lista de alunos

## 🔧 Instalação e Configuração

### 1. Adicionar ao INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    # ... outros apps
    'relatorios_presenca',
]
```

### 2. Incluir URLs

```python
# urls.py principal
urlpatterns = [
    # ... outras URLs
    path('relatorios-presenca/', include('relatorios_presenca.urls')),
]
```

### 3. Executar Migrações

```bash
# Criar migrações
python manage.py makemigrations relatorios_presenca

# Aplicar migrações
python manage.py migrate

# Migrar dados existentes
python manage.py migrar_dados_presenca --dry-run  # Simulação
python manage.py migrar_dados_presenca             # Execução real
```

### 4. Configurar Permissões

```python
# Adicionar permissões no admin ou via código
from django.contrib.auth.models import Permission

# Permissões específicas do app
permissions = [
    'relatorios_presenca.add_configuracaorelatorio',
    'relatorios_presenca.change_configuracaorelatorio',
    'relatorios_presenca.view_historico_relatorio',
    # ... outras permissões
]
```

## 🎯 Uso

### Interface Web

1. **Acessar**: `/relatorios-presenca/`
2. **Selecionar**: Tipo de relatório desejado
3. **Configurar**: Filtros dinâmicos (turma, período, atividade)
4. **Gerar**: Download automático do arquivo Excel

### Programático

```python
from relatorios_presenca.services.relatorio_service import RelatorioPresencaService
from relatorios_presenca.generators.excel_generator import ExcelRelatorioGenerator

# Obter dados
service = RelatorioPresencaService()
dados = service.obter_dados_consolidado_periodo(
    turma_id=1,
    data_inicio=date(2023, 1, 1),
    data_fim=date(2023, 12, 31)
)

# Gerar relatório
generator = ExcelRelatorioGenerator()
arquivo = generator.gerar_consolidado_periodo(dados)

# Salvar ou retornar
with open('relatorio.xlsx', 'wb') as f:
    f.write(arquivo.getvalue())
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes do app
python manage.py test relatorios_presenca

# Testes específicos
python manage.py test relatorios_presenca.tests.test_models
python manage.py test relatorios_presenca.tests.test_services
python manage.py test relatorios_presenca.tests.test_views

# Com cobertura
coverage run --source='.' manage.py test relatorios_presenca
coverage report
```

### Estrutura de Testes

```
tests/
├── __init__.py
├── test_models.py      # Testes dos modelos
├── test_services.py    # Testes dos services
├── test_views.py       # Testes das views
├── test_generators.py  # Testes dos generators
└── test_commands.py    # Testes dos comandos
```

## 📁 Estrutura de Arquivos

```
relatorios_presenca/
├── __init__.py
├── admin.py                    # Configurações do admin
├── apps.py                     # Configuração do app
├── models.py                   # Modelos do sistema
├── urls.py                     # URLs do app
├── views.py                    # Views function-based
├── generators/                 # Geradores de relatório
│   ├── __init__.py
│   ├── excel_generator.py      # Gerador Excel
│   ├── pdf_generator.py        # Gerador PDF (futuro)
│   └── csv_generator.py        # Gerador CSV (futuro)
├── services/                   # Lógica de negócio
│   ├── __init__.py
│   └── relatorio_service.py    # Service principal
├── management/                 # Comandos Django
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── migrar_dados_presenca.py
├── templates/                  # Templates HTML
│   └── relatorios_presenca/
│       ├── listar_relatorios.html
│       ├── gerar_relatorio.html
│       ├── detalhar_relatorio.html
│       └── confirmar_exclusao_relatorio.html
├── static/                     # Arquivos estáticos
│   └── relatorios_presenca/
│       ├── css/
│       │   └── relatorios.css
│       └── js/
│           └── relatorios.js
├── tests/                      # Testes automatizados
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_views.py
├── migrations/                 # Migrações do banco
└── README.md                   # Esta documentação
```

## 🔄 Migração de Dados

### Comando de Migração

```bash
# Simulação (recomendado primeiro)
python manage.py migrar_dados_presenca --dry-run --verbose

# Execução real
python manage.py migrar_dados_presenca --verbose

# Com tamanho de lote personalizado
python manage.py migrar_dados_presenca --batch-size=500
```

### Mapeamento de Dados

| Modelo Antigo | Campo Antigo | Modelo Novo | Campo Novo |
|---------------|--------------|-------------|------------|
| `Presenca` | `presente` | `RegistroPresenca` | `status` (P/F) |
| `PresencaDetalhada` | `status` | `RegistroPresenca` | `status` |
| `ConvocacaoPresenca` | `convocado` | `RegistroPresenca` | `convocado` |

### Rastreabilidade

O modelo `HistoricoMigracao` mantém registro de todos os dados migrados:

```python
# Verificar migração
from relatorios_presenca.models import HistoricoMigracao

# Total migrado
total = HistoricoMigracao.objects.count()

# Por tipo
por_tipo = HistoricoMigracao.objects.values('tipo_origem').annotate(
    total=Count('id')
)
```

## 🎨 Personalização

### Templates Excel

1. **Upload**: Via admin ou interface web
2. **Formato**: Arquivo .xlsx com placeholders
3. **Uso**: Automático na geração de relatórios

### Estilos CSS

Personalizar em `static/relatorios_presenca/css/relatorios.css`:

```css
:root {
    --primary-color: #366092;  /* Cor principal */
    --secondary-color: #f8f9fa; /* Cor secundária */
    /* ... outras variáveis */
}
```

### JavaScript

Estender funcionalidades em `static/relatorios_presenca/js/relatorios.js`:

```javascript
// Adicionar validações customizadas
function validacaoCustomizada() {
    // Sua lógica aqui
}

// Integrar com sistema existente
$(document).ready(function() {
    initFiltrosDinamicos();
    validacaoCustomizada();
});
```

## 🚀 Performance

### Otimizações Implementadas

1. **Índices de Banco**: Campos frequentemente consultados
2. **Select Related**: Redução de queries N+1
3. **Batch Processing**: Processamento em lotes
4. **Caching**: Cache de configurações e templates
5. **AJAX Debounce**: Redução de chamadas desnecessárias

### Monitoramento

```python
# Logs de performance
import logging
logger = logging.getLogger('relatorios_presenca.performance')

# Métricas de geração
from django.db import connection
print(f"Queries executadas: {len(connection.queries)}")
```

## 🔒 Segurança

### Validações Implementadas

1. **Autenticação**: `@login_required` em todas as views
2. **Autorização**: Verificação de permissões por tipo de relatório
3. **CSRF**: Proteção em formulários AJAX
4. **Sanitização**: Validação de parâmetros de entrada
5. **Rate Limiting**: Controle de frequência de geração

### Auditoria

```python
# Histórico completo
from relatorios_presenca.models import HistoricoRelatorio

# Relatórios por usuário
relatorios_usuario = HistoricoRelatorio.objects.filter(
    usuario=request.user
).order_by('-data_geracao')

# Relatórios com erro
relatorios_erro = HistoricoRelatorio.objects.filter(
    status='erro'
)
```

## 📈 Métricas e Analytics

### Estatísticas Disponíveis

1. **Uso por Tipo**: Relatórios mais gerados
2. **Performance**: Tempo médio de geração
3. **Erros**: Taxa de falha por tipo
4. **Usuários**: Usuários mais ativos

### Dashboard (Futuro)

```python
# Métricas para dashboard
def obter_metricas_dashboard():
    return {
        'total_relatorios': HistoricoRelatorio.objects.count(),
        'relatorios_hoje': HistoricoRelatorio.objects.filter(
            data_geracao__date=timezone.now().date()
        ).count(),
        'taxa_sucesso': calcular_taxa_sucesso(),
        'tipos_populares': obter_tipos_populares(),
    }
```

## 🤝 Contribuição

### Padrões de Código

1. **PEP 8**: Seguir padrões Python
2. **Docstrings**: Documentar todas as funções
3. **Type Hints**: Usar anotações de tipo
4. **Testes**: Cobertura mínima de 80%

### Processo de Desenvolvimento

1. **Branch**: Criar branch para feature
2. **Testes**: Executar suite completa
3. **Documentação**: Atualizar README se necessário
4. **Pull Request**: Submeter para revisão

## 📞 Suporte

### Logs

```bash
# Logs do app
tail -f logs/relatorios_presenca.log

# Logs de erro
grep ERROR logs/relatorios_presenca.log
```

### Troubleshooting

| Problema | Solução |
|----------|---------|
| Erro de importação | Verificar `INSTALLED_APPS` |
| Relatório vazio | Verificar filtros e dados |
| Erro de template | Verificar arquivo Excel |
| Performance lenta | Verificar índices e queries |

### Contato

- **Documentação**: Este README
- **Issues**: Sistema de tickets interno
- **Suporte**: Equipe de desenvolvimento

---

**Versão**: 1.0  
**Data**: Setembro 2025  
**Autor**: Manus AI  
**Status**: Implementação Completa

