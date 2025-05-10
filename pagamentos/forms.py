from django import forms
from .models import Pagamento
from alunos.models import Aluno

class PagamentoForm(forms.ModelForm):
    """
    Formulário para criação e edição de pagamentos.
    """
    
    class Meta:
        model = Pagamento
        fields = ['aluno', 'valor', 'data_pagamento', 'status']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'data_pagamento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'aluno': 'Aluno',
            'valor': 'Valor (R$)',
            'data_pagamento': 'Data do Pagamento',
            'status': 'Status'
        }
        help_texts = {
            'valor': 'Valor em reais',
            'data_pagamento': 'Data em que o pagamento foi realizado ou está previsto',
            'status': 'Situação atual do pagamento'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas alunos ativos
        self.fields['aluno'].queryset = Aluno.objects.filter(situacao='ATIVO')
        
        # Adicionar classes CSS para estilização
        for field_name, field in self.fields.items():
            if field_name not in ['aluno', 'status']:
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean_valor(self):
        """Validação personalizada para o campo valor."""
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise forms.ValidationError("O valor do pagamento deve ser maior que zero.")
        return valor
        return cleaned_data