from django import forms
from django.utils import timezone
from importlib import import_module

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_atividade_model():
    """Obtém o modelo Atividade."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "Atividade")

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

class PresencaForm(forms.ModelForm):
    """Formulário para registro e edição de presenças."""
    
    class Meta:
        model = get_model_dynamically("presencas", "Presenca")
        fields = ['aluno', 'atividade', 'data', 'presente', 'justificativa']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select select2'}),
            'atividade': forms.Select(attrs={'class': 'form-select select2'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'justificativa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalização adicional dos campos
        self.fields['justificativa'].required = False
        
        # Definir data padrão como hoje
        if not self.instance.pk:
            self.fields['data'].initial = timezone.now().date()
        
        # Adicionar classes CSS para validação
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = 'required'
    
    def clean(self):
        """Validação personalizada do formulário."""
        cleaned_data = super().clean()
        presente = cleaned_data.get('presente')
        justificativa = cleaned_data.get('justificativa')
        data = cleaned_data.get('data')
        
        # Verificar se a data não é futura
        if data and data > timezone.now().date():
            self.add_error('data', 'A data não pode ser futura.')
        
        # Verificar se há justificativa quando o aluno está ausente
        if presente is False and not justificativa:
            self.add_error('justificativa', 'É necessário fornecer uma justificativa para a ausência.')
        
        return cleaned_data

class PresencaMultiplaForm(forms.Form):
    """Formulário para registro de múltiplas presenças."""
    
    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.now().date()
    )
    
    turmas = forms.ModelMultipleChoiceField(
        label='Turmas',
        queryset=get_turma_model().objects.filter(status='A'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'size': '5'}),
        help_text='Selecione uma ou mais turmas'
    )
    
    atividades = forms.ModelMultipleChoiceField(
        label='Atividades',
        queryset=get_atividade_model().objects.all().order_by('-data_inicio'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'size': '5'}),
        help_text='Selecione uma ou mais atividades'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        turmas = cleaned_data.get('turmas')
        atividades = cleaned_data.get('atividades')
        
        if not turmas:
            self.add_error('turmas', 'Selecione pelo menos uma turma.')
        
        if not atividades:
            self.add_error('atividades', 'Selecione pelo menos uma atividade.')
        
        return cleaned_data

class FiltroPresencaForm(forms.Form):
    """Formulário para filtrar presenças."""
    
    aluno = forms.ModelChoiceField(
        label='Aluno',
        queryset=get_aluno_model().objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    atividade = forms.ModelChoiceField(
        label='Atividade',
        queryset=get_atividade_model().objects.all().order_by('-data_inicio'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    data_inicio = forms.DateField(
        label='Data Inicial',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    data_fim = forms.DateField(
        label='Data Final',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    situacao = forms.ChoiceField(
        label='Situação',
        choices=[('', '-- Todas --')] + list(get_models().SITUACAO_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
