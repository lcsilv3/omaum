# Nova Proposta de Implementação e Relatórios de Presença e Frequência no Projeto OmAum

## Sumário Executivo

Este documento apresenta uma nova proposta de implementação para o sistema de presença e frequência do projeto OmAum, baseada em uma análise detalhada da estrutura atual. A proposta visa simplificar a arquitetura, melhorar a performance e criar um sistema de relatórios que replique fielmente os formatos Excel existentes.

## 1. Problemas Identificados na Implementação Atual

### 1.1. Complexidade Excessiva nos Modelos
O sistema atual utiliza múltiplos modelos para controlar presença (`Presenca`, `PresencaDetalhada`, `ConvocacaoPresenca`), criando redundância e dificultando a manutenção.

### 1.2. Nomenclatura Inconsistente
- Campo `perc_carencia` deveria ser `perc_presenca`
- Ausência do campo "Número Iniciático" no modelo Aluno
- Falta de campo para situação do aluno (ativo/desligado/falecido/excluído)

### 1.3. Sistema de Relatórios Inadequado
- Relatórios não replicam visualmente os formatos Excel existentes
- App `relatorios` atual é disfuncional e não atende aos requisitos
- Falta interpretação correta das planilhas Excel (grau, mod, mes01-99, pcg)

## 2. Nova Arquitetura Proposta

### 2.1. Unificação dos Modelos de Presença

**Modelo Único: `RegistroPresenca`**

```python
class RegistroPresenca(models.Model):
    """Modelo unificado para registro de presença."""
    
    # Relacionamentos
    aluno = models.ForeignKey("alunos.Aluno", on_delete=models.CASCADE)
    turma = models.ForeignKey("turmas.Turma", on_delete=models.CASCADE)
    atividade = models.ForeignKey("atividades.Atividade", on_delete=models.CASCADE)
    data = models.DateField()

    # Status da presença
    STATUS_CHOICES = [
        ('P', 'Presente'),
        ('F', 'Falta'),
        ('J', 'Falta Justificada'),
        ('V1', 'Voluntário Extra'),
        ('V2', 'Voluntário Simples'),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')

    # Informações adicionais
    justificativa = models.TextField(blank=True, null=True)
    convocado = models.BooleanField(default=True)

    # Campos de controle
    registrado_por = models.CharField(max_length=100, default="Sistema")
    data_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["aluno", "turma", "atividade", "data"]
        verbose_name = "Registro de Presença"
        verbose_name_plural = "Registros de Presença"
        ordering = ["-data", "aluno__nome"]

    def __str__(self):
        return f"{self.aluno.nome} - {self.data} - {self.get_status_display()}"
```

### 2.2. Ajustes nos Modelos Existentes

**Modelo Aluno - Campos Adicionais:**

```python
class Aluno(models.Model):
    # ... campos existentes ...
    
    # Novos campos obrigatórios
    numero_iniciatico = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name="Número Iniciático",
        help_text="Número único de identificação iniciática"
    )
    
    SITUACAO_CHOICES = [
        ('a', 'Ativo'),
        ('d', 'Desligado'),
        ('f', 'Falecido'),
        ('e', 'Excluído'),
    ]
    situacao = models.CharField(
        max_length=1,
        choices=SITUACAO_CHOICES,
        default='a',
        verbose_name="Situação do Aluno"
    )
```

**Modelo Turma - Ajuste de Nomenclatura:**

```python
class Turma(models.Model):
    # ... campos existentes ...
    
    # Campo renomeado
    perc_presenca_minima = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Percentual Mínimo de Presença (%)",
        help_text="Percentual mínimo de presenças permitido para a turma"
    )
```

### 2.3. Novo App: `relatorios_presenca`

Substituição completa do app `relatorios` atual por um novo app especializado.

**Estrutura do App:**

```
relatorios_presenca/
├── __init__.py
├── admin.py
├── apps.py
├── models.py          # Configurações e histórico de relatórios
├── services.py        # Lógica de negócio para geração de dados
├── generators/        # Geradores por formato
│   ├── __init__.py
│   ├── excel.py       # Geração de arquivos Excel
│   ├── pdf.py         # Geração de arquivos PDF
│   └── csv.py         # Geração de arquivos CSV
├── views.py           # Views para interface web
├── urls.py
├── forms.py
├── templates/         # Templates HTML
│   └── relatorios_presenca/
├── static/            # CSS/JS específicos
├── tests/             # Testes automatizados
└── migrations/
```

## 3. Especificação dos Relatórios

### 3.1. Relatório Consolidado por Período (`grau`)

**Objetivo:** Apresentar visão consolidada da presença por período com agregação mensal.

**Estrutura:**
- Cabeçalho com título, período e turma
- Tabela com alunos (linhas) e meses (colunas)
- Subtotais por mês: P, F, J, V1, V2
- Totais do período e percentual de presença
- Formatação condicional para baixa presença

**Implementação:**

```python
class ConsolidadoPeriodoGenerator:
    def gerar(self, turma_id, data_inicio, data_fim):
        # Obter dados do service
        service = RelatorioPresencaService()
        dados = service.obter_dados_consolidado(turma_id, data_inicio, data_fim)
        
        # Gerar Excel com template
        wb = self.carregar_template('consolidado_periodo.xlsx')
        ws = wb.active
        
        # Preencher cabeçalho
        ws['A1'] = f"Relatório Consolidado - {dados['turma'].nome}"
        ws['A2'] = f"Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"
        
        # Preencher dados dos alunos
        row = 5
        for aluno_dados in dados['alunos']:
            self.preencher_linha_aluno(ws, row, aluno_dados)
            row += 1
        
        return wb
```

### 3.2. Relatório de Coleta Mensal (`mod`)

**Objetivo:** Formulário para coleta manual de dados mensais.

**Estrutura:**
- Cabeçalho com mês e turma
- Tabela com alunos e dias do mês
- Células editáveis para preenchimento manual
- Coluna para observações

### 3.3. Relatório de Apuração Mensal (`mes01..mes99`)

**Objetivo:** Detalhar apuração de presença por mês.

**Estrutura:**
- Cabeçalho com mês e turma
- Tabela com alunos e dias de atividade
- Status de presença por dia
- Subtotais mensais

### 3.4. Relatório de Controle Geral (`pcg`)

**Objetivo:** Apresentar dados gerais da turma.

**Estrutura:**
- Informações completas da turma
- Dados dos instrutores
- Configurações de presença
- Formato PDF profissional

## 4. Implementação Técnica

### 4.1. Service Layer

```python
class RelatorioPresencaService:
    """Serviço centralizado para geração de dados de relatórios."""
    
    def obter_dados_consolidado(self, turma_id, data_inicio, data_fim):
        """Obtém dados para relatório consolidado."""
        registros = RegistroPresenca.objects.filter(
            turma_id=turma_id,
            data__range=[data_inicio, data_fim]
        ).select_related('aluno', 'atividade')
        
        # Processar dados por aluno e mês
        dados_processados = self._processar_dados_consolidado(registros)
        
        return {
            'turma': Turma.objects.get(id=turma_id),
            'periodo': {'inicio': data_inicio, 'fim': data_fim},
            'alunos': dados_processados
        }
    
    def _processar_dados_consolidado(self, registros):
        """Processa registros para formato consolidado."""
        dados_alunos = {}
        
        for registro in registros:
            aluno_id = registro.aluno.id
            mes_ano = f"{registro.data.month:02d}/{registro.data.year}"
            
            if aluno_id not in dados_alunos:
                dados_alunos[aluno_id] = {
                    'aluno': registro.aluno,
                    'meses': {},
                    'totais': {'P': 0, 'F': 0, 'J': 0, 'V1': 0, 'V2': 0}
                }
            
            if mes_ano not in dados_alunos[aluno_id]['meses']:
                dados_alunos[aluno_id]['meses'][mes_ano] = {
                    'P': 0, 'F': 0, 'J': 0, 'V1': 0, 'V2': 0
                }
            
            # Contabilizar por status
            status = registro.status
            dados_alunos[aluno_id]['meses'][mes_ano][status] += 1
            dados_alunos[aluno_id]['totais'][status] += 1
        
        return list(dados_alunos.values())
```

### 4.2. Gerador Excel

```python
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side

class ExcelGenerator:
    """Gerador de relatórios Excel com fidelidade visual."""
    
    def __init__(self, template_path):
        self.template_path = template_path
    
    def gerar_consolidado(self, dados):
        """Gera relatório consolidado em Excel."""
        wb = load_workbook(self.template_path)
        ws = wb.active
        
        # Aplicar estilos padrão
        self._aplicar_estilos_cabecalho(ws)
        
        # Preencher dados
        self._preencher_dados_consolidado(ws, dados)
        
        # Aplicar formatação condicional
        self._aplicar_formatacao_condicional(ws, dados)
        
        return wb
    
    def _aplicar_estilos_cabecalho(self, ws):
        """Aplica estilos ao cabeçalho."""
        header_font = Font(bold=True, color="FFFFFF", size=12)
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        # Aplicar aos cabeçalhos das colunas
        for col in range(1, 10):  # Ajustar conforme necessário
            cell = ws.cell(row=4, column=col)
            cell.font = header_font
            cell.fill = header_fill
    
    def _aplicar_formatacao_condicional(self, ws, dados):
        """Aplica formatação condicional para baixa presença."""
        for row_idx, aluno_dados in enumerate(dados['alunos'], start=5):
            percentual = self._calcular_percentual_presenca(aluno_dados)
            
            if percentual < 75:  # Critério de baixa presença
                fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
                for col in range(1, 10):
                    ws.cell(row=row_idx, column=col).fill = fill
```

### 4.3. Interface Web

```python
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

class GerarRelatorioView(LoginRequiredMixin, TemplateView):
    """View para interface de geração de relatórios."""
    template_name = 'relatorios_presenca/gerar_relatorio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turmas'] = Turma.objects.filter(ativo=True)
        context['tipos_relatorio'] = [
            ('consolidado', 'Consolidado por Período'),
            ('mensal', 'Apuração Mensal'),
            ('coleta', 'Formulário de Coleta'),
            ('controle_geral', 'Controle Geral da Turma'),
        ]
        return context
    
    def post(self, request, *args, **kwargs):
        """Processa solicitação de geração de relatório."""
        tipo = request.POST.get('tipo_relatorio')
        turma_id = request.POST.get('turma_id')
        formato = request.POST.get('formato', 'excel')
        
        # Gerar relatório conforme tipo
        if tipo == 'consolidado':
            return self._gerar_consolidado(turma_id, formato, request.POST)
        elif tipo == 'mensal':
            return self._gerar_mensal(turma_id, formato, request.POST)
        # ... outros tipos
    
    def _gerar_consolidado(self, turma_id, formato, params):
        """Gera relatório consolidado."""
        service = RelatorioPresencaService()
        dados = service.obter_dados_consolidado(
            turma_id, 
            params.get('data_inicio'),
            params.get('data_fim')
        )
        
        if formato == 'excel':
            generator = ExcelGenerator('templates/consolidado.xlsx')
            wb = generator.gerar_consolidado(dados)
            
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=consolidado.xlsx'
            wb.save(response)
            return response
```

## 5. Plano de Migração

### 5.1. Estratégia de Migração

**Fase 1: Preparação**
- Backup completo do banco de dados
- Criação do ambiente de teste
- Implementação dos novos modelos em paralelo

**Fase 2: Migração de Dados**
- Script de migração dos dados existentes
- Validação da integridade dos dados migrados
- Testes de performance

**Fase 3: Implementação Gradual**
- Deploy do novo app de relatórios
- Migração gradual das funcionalidades
- Treinamento dos usuários

**Fase 4: Finalização**
- Remoção dos modelos antigos
- Limpeza do código legado
- Documentação final

### 5.2. Script de Migração

```python
from django.core.management.base import BaseCommand
from presencas.models import Presenca, PresencaDetalhada, ConvocacaoPresenca
from presencas.models import RegistroPresenca  # Novo modelo

class Command(BaseCommand):
    help = 'Migra dados dos modelos antigos para o novo RegistroPresenca'
    
    def handle(self, *args, **options):
        self.stdout.write('Iniciando migração de dados...')
        
        # Migrar dados de Presenca
        self._migrar_presencas()
        
        # Migrar dados de PresencaDetalhada
        self._migrar_presencas_detalhadas()
        
        # Migrar dados de ConvocacaoPresenca
        self._migrar_convocacoes()
        
        self.stdout.write(self.style.SUCCESS('Migração concluída com sucesso!'))
    
    def _migrar_presencas(self):
        """Migra dados do modelo Presenca."""
        presencas = Presenca.objects.all()
        
        for presenca in presencas:
            RegistroPresenca.objects.get_or_create(
                aluno=presenca.aluno,
                turma=presenca.turma,
                atividade=presenca.atividade,
                data=presenca.data,
                defaults={
                    'status': 'P' if presenca.presente else 'F',
                    'justificativa': presenca.justificativa,
                    'registrado_por': presenca.registrado_por,
                    'data_registro': presenca.data_registro,
                }
            )
```

## 6. Benefícios da Nova Implementação

### 6.1. Simplificação da Arquitetura
- Redução de 3 modelos para 1 modelo unificado
- Eliminação de redundâncias e inconsistências
- Facilidade de manutenção e evolução

### 6.2. Melhoria na Performance
- Consultas mais eficientes com menos JOINs
- Redução do número de queries para relatórios
- Otimização do uso de memória

### 6.3. Fidelidade aos Relatórios Excel
- Replicação exata do layout visual
- Manutenção da familiaridade dos usuários
- Formatação condicional automática

### 6.4. Facilidade de Manutenção
- Código mais limpo e organizado
- Documentação completa
- Testes automatizados abrangentes

## 7. Cronograma de Implementação

| Fase | Atividade | Duração | Responsável |
|------|-----------|---------|-------------|
| 1 | Análise e Planejamento | 1 semana | Equipe Técnica |
| 2 | Implementação dos Novos Modelos | 2 semanas | Desenvolvedor Backend |
| 3 | Desenvolvimento do App de Relatórios | 3 semanas | Equipe Completa |
| 4 | Criação dos Geradores de Relatório | 2 semanas | Desenvolvedor Backend |
| 5 | Interface Web | 1 semana | Desenvolvedor Frontend |
| 6 | Testes e Validação | 2 semanas | QA + Equipe |
| 7 | Migração de Dados | 1 semana | DBA + Backend |
| 8 | Deploy e Monitoramento | 1 semana | DevOps + Equipe |

**Total: 13 semanas (aproximadamente 3 meses)**

## 8. Conclusão

A nova proposta de implementação apresentada neste documento oferece uma solução robusta, eficiente e alinhada com os requisitos específicos do projeto OmAum. A unificação dos modelos de presença, combinada com um sistema de relatórios dedicado e visualmente fiel aos formatos Excel existentes, resultará em um sistema mais simples de manter, mais performático e mais satisfatório para os usuários finais.

A implementação gradual proposta minimiza os riscos e garante a continuidade das operações durante a transição, enquanto os testes automatizados e a documentação detalhada asseguram a qualidade e facilitam futuras evoluções do sistema.

---

**Documento elaborado por:** Manus AI  
**Data:** Setembro 2025  
**Versão:** 1.0  
**Status:** Proposta para Aprovação

