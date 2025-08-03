from django import forms

class RegistroRapidoForm(forms.Form):
    pass

class ExportacaoForm(forms.Form):
    pass

class PresencaDetalhadaForm(forms.Form):
    pass

import logging
from cursos.models import Curso
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from django.utils import timezone
from django_select2.forms import Select2Widget


logger = logging.getLogger(__name__)

class RegistrarPresencaForm(forms.Form):
    """
    Formulário para o primeiro passo do registro de presença,
    com seleção de curso, turma, ano e mês.
    """
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.filter(ativo=True),
        label="Curso",
        widget=Select2Widget(attrs={'data-placeholder': 'Selecione um curso'}),
        required=True
    )
    turma = forms.ModelChoiceField(
        queryset=Turma.objects.none(),  # Populado via AJAX
        label="Turma",
        widget=Select2Widget(attrs={'data-placeholder': 'Selecione uma turma'}),
        required=True
    )

    ANO_CHOICES = [(ano, str(ano)) for ano in range(timezone.now().year, timezone.now().year - 5, -1)]
    MES_CHOICES = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ]

    ano = forms.ChoiceField(
        choices=ANO_CHOICES,
        label="Ano",
        required=True,
        initial=timezone.now().year
    )
    mes = forms.ChoiceField(
        choices=MES_CHOICES,
        label="Mês",
        required=True,
        initial=timezone.now().month
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                self.fields['turma'].queryset = Turma.objects.filter(
                    curso_id=curso_id,
                    status='A'
                ).order_by('nome')
            except (ValueError, TypeError):
                pass  # O queryset permanecerá como none()
        elif self.initial.get('curso'):
            curso_id = self.initial['curso'].pk
            self.fields['turma'].queryset = Turma.objects.filter(
                curso_id=curso_id,
                status='A'
            ).order_by('nome')

class TotaisAtividadesPresencaForm(forms.Form):
    """
    Formulário dinâmico para informar o total de atividades por mês.
    """
    def __init__(self, *args, atividades=None, **kwargs):
        super().__init__(*args, **kwargs)
        if atividades is not None:
            for atividade in atividades:
                self.fields[f'qtd_ativ_{atividade.id}'] = forms.IntegerField(
                    label=atividade.nome,
                    min_value=0,
                    max_value=999,
                    required=True,
                    widget=forms.NumberInput(
                        attrs={
                            'class': 'form-control',
                            'placeholder': 'Qtd. dias',
                            'aria-label': atividade.nome
                        }
                    )
                )
        self.atividades = atividades

    def clean(self):
        cleaned_data = super().clean()
        curso = cleaned_data.get('curso')
        turma = cleaned_data.get('turma')
        
        # Validação cruzada curso-turma
        if curso and turma and turma.curso != curso:
            raise forms.ValidationError(
                'A turma selecionada não pertence ao curso escolhido.'
            )
        
        # Auto-preenchimento: se não há curso mas há turma, usar curso da turma
        if turma and not curso:
            cleaned_data['curso'] = turma.curso
        
        return cleaned_data

class AlunosPresencaForm(forms.Form):
    """
    Formulário para seleção de presença/falta dos alunos convocados.
    """
    def __init__(self, *args, alunos=None, **kwargs):
        super().__init__(*args, **kwargs)
        if alunos:
            for aluno in alunos:
                self.fields[f'aluno_{aluno.cpf}_status'] = forms.ChoiceField(
                    choices=[('presente', 'Presente'), ('ausente', 'Ausente')],
                    initial='presente',
                    label=aluno.nome,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input', 'aria-label': aluno.nome})
                )
                self.fields[f'aluno_{aluno.cpf}_justificativa'] = forms.CharField(
                    required=False,
                    label='Justificativa',
                    widget=forms.TextInput(attrs={'placeholder': 'Justificativa da falta', 'class': 'form-control', 'aria-label': f'Justificativa {aluno.nome}'})
                )

# class PresencaAcademicaForm(forms.ModelForm):
#     """
#     Formulário para criação/edição de PresencaAcademica.
#     """
#     class Meta:
#         model = PresencaAcademica
#         fields = [
#             'aluno', 'turma', 'atividade', 'data', 'presente',
#             'registrado_por', 'data_registro'
#         ]


class FiltroConsolidadoForm(forms.Form):
    """
    Formulário para filtros do consolidado de presenças.
    """
    
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.filter(ativo=True),
        label="Curso",
        widget=Select2Widget(attrs={'data-placeholder': 'Todos os cursos'}),
        required=False
    )
    
    turma = forms.ModelChoiceField(
        queryset=Turma.objects.filter(status='A'),
        label="Turma",
        widget=Select2Widget(attrs={'data-placeholder': 'Todas as turmas'}),
        required=False
    )
    
    atividade = forms.ModelChoiceField(
        queryset=AtividadeAcademica.objects.filter(ativo=True),
        label="Atividade",
        widget=Select2Widget(attrs={'data-placeholder': 'Todas as atividades'}),
        required=False
    )
    
    periodo_inicio = forms.DateField(
        label="Período Início",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            },
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        required=False
    )
    
    periodo_fim = forms.DateField(
        label="Período Fim",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            },
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        required=False
    )
    
    aluno_nome = forms.CharField(
        label="Nome do Aluno",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome do aluno'
        }),
        required=False
    )
    
    ORDENACAO_CHOICES = [
        ('aluno__nome', 'Nome do Aluno'),
        ('turma__nome', 'Nome da Turma'),
        ('atividade__nome', 'Nome da Atividade'),
        ('periodo', 'Período'),
        ('percentual_presenca', 'Percentual de Presença'),
    ]
    
    ordenar_por = forms.ChoiceField(
        choices=ORDENACAO_CHOICES,
        label="Ordenar por",
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='aluno__nome',
        required=False
    )
    
    ORDEM_CHOICES = [
        ('asc', 'Crescente'),
        ('desc', 'Decrescente'),
    ]
    
    ordem = forms.ChoiceField(
        choices=ORDEM_CHOICES,
        label="Ordem",
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='asc',
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Atualizar queryset de turmas baseado no curso
        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                self.fields['turma'].queryset = Turma.objects.filter(
                    curso_id=curso_id,
                    status='A'
                ).order_by('nome')
            except (ValueError, TypeError):
                pass
        
        # Atualizar queryset de atividades baseado na turma
        if 'turma' in self.data:
            try:
                turma_id = int(self.data.get('turma'))
                self.fields['atividade'].queryset = AtividadeAcademica.objects.filter(
                    presencas_detalhadas_expandidas__turma_id=turma_id
                ).distinct().order_by('nome')
            except (ValueError, TypeError):
                pass
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar período
        periodo_inicio = cleaned_data.get('periodo_inicio')
        periodo_fim = cleaned_data.get('periodo_fim')
        
        if periodo_inicio and periodo_fim:
            if periodo_inicio > periodo_fim:
                raise forms.ValidationError(
                    "A data de início deve ser anterior à data de fim."
                )
        
        return cleaned_data


class EditarPresencaDetalhadaForm(forms.Form):
    """
    Formulário para edição inline de presença detalhada.
    """
    
    presenca_id = forms.IntegerField(widget=forms.HiddenInput())
    
    convocacoes = forms.IntegerField(
        label="Convocações (C)",
        min_value=0,
        max_value=999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'style': 'width: 60px;'
        })
    )
    
    presencas = forms.IntegerField(
        label="Presenças (P)",
        min_value=0,
        max_value=999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'style': 'width: 60px;'
        })
    )
    
    faltas = forms.IntegerField(
        label="Faltas (F)",
        min_value=0,
        max_value=999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'style': 'width: 60px;'
        })
    )
    
    voluntario_extra = forms.IntegerField(
        label="Voluntário Extra (V1)",
        min_value=0,
        max_value=999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'style': 'width: 60px;'
        })
    )
    
    voluntario_simples = forms.IntegerField(
        label="Voluntário Simples (V2)",
        min_value=0,
        max_value=999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'style': 'width: 60px;'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        convocacoes = cleaned_data.get('convocacoes', 0)
        presencas = cleaned_data.get('presencas', 0)
        faltas = cleaned_data.get('faltas', 0)
        
        # Validar: P + F deve ser <= C
        if presencas + faltas > convocacoes:
            raise forms.ValidationError(
                "A soma de presenças e faltas não pode ser maior que convocações."
            )
        
        return cleaned_data
