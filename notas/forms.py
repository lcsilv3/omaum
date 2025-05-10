from django import forms
from .models import Nota
from alunos.models import Aluno
from cursos.models import Curso

class NotaForm(forms.ModelForm):
    """
    Formulário para criação e edição de notas.
    """
    
    class Meta:
        model = Nota
        fields = ['aluno', 'curso', 'valor', 'data', 'tipo_avaliacao', 'peso', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '10'
            }),
            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tipo_avaliacao': forms.Select(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1',
                'max': '5'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
        labels = {
            'aluno': 'Aluno',
            'curso': 'Curso',
            'valor': 'Nota',
            'data': 'Data da Avaliação',
            'tipo_avaliacao': 'Tipo de Avaliação',
            'peso': 'Peso da Avaliação',
            'observacoes': 'Observações'
        }
        help_texts = {
            'valor': 'Valor entre 0 e 10',
            'peso': 'Peso da avaliação (padrão: 1.0)',
            'tipo_avaliacao': 'Selecione o tipo de avaliação'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir valor padrão para o peso
        self.fields['peso'].initial = 1.0
        
        # Filtrar apenas alunos ativos
        self.fields['aluno'].queryset = Aluno.objects.filter(situacao='ATIVO')
        
        # Filtrar apenas cursos ativos
        self.fields['curso'].queryset = Curso.objects.filter(ativo=True)
        
        # Adicionar classes CSS para estilização
        for field_name, field in self.fields.items():
            if field_name not in ['aluno', 'curso', 'tipo_avaliacao']:
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean_valor(self):
        """Validação personalizada para o campo valor."""
        valor = self.cleaned_data.get('valor')
        if valor is not None:
            if valor < 0:
                raise forms.ValidationError("A nota não pode ser negativa.")
            if valor > 10:
                raise forms.ValidationError("A nota não pode ser maior que 10.")
        return valor
    
    def clean_peso(self):
        """Validação personalizada para o campo peso."""
        peso = self.cleaned_data.get('peso')
        if peso is not None:
            if peso <= 0:
                raise forms.ValidationError("O peso deve ser maior que zero.")
            if peso > 5:
                raise forms.ValidationError("O peso não pode ser maior que 5.")
        return peso
