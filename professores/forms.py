from django import forms
from django.core.validators import RegexValidator
from .models import Professor

class ProfessorForm(forms.ModelForm):
    # Adiciona validação para o formato do telefone
    telefone = forms.CharField(
        max_length=15, 
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Formato inválido. Use (99) 99999-9999'
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': '(99) 99999-9999'
            }
        )
    )
    
    class Meta:
        model = Professor
        fields = ['nome', 'email', 'telefone', 'especialidade', 'observacoes', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do professor'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'especialidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Área de especialidade'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações adicionais sobre o professor'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica se o email já existe (exceto para o próprio professor em caso de edição)
        if Professor.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError('Este e-mail já está em uso por outro professor.')
        return email
