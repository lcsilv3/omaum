from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Iniciacao

class IniciacaoForm(forms.ModelForm):
    class Meta:
        model = Iniciacao
        fields = ['aluno', 'nome_curso', 'data_iniciacao', 'observacoes']
        widgets = {
            'data_iniciacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'nome_curso': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'aluno': 'Aluno',
            'nome_curso': 'Nome do Curso',
            'data_iniciacao': 'Data de Iniciação',
            'observacoes': 'Observações'
        }
        help_texts = {
            'nome_curso': 'Digite o nome completo do curso de iniciação',
            'data_iniciacao': 'Selecione a data em que o aluno foi iniciado no curso'
        }

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        nome_curso = cleaned_data.get('nome_curso')
        data_iniciacao = cleaned_data.get('data_iniciacao')
        
        # Verifica se já existe uma iniciação para este aluno neste curso
        if aluno and nome_curso:
            # Exclui a instância atual em caso de edição
            instance_id = self.instance.id if self.instance else None
            
            # Verifica se já existe outra iniciação com o mesmo aluno e curso
            if Iniciacao.objects.filter(aluno=aluno, nome_curso=nome_curso).exclude(id=instance_id).exists():
                raise ValidationError(
                    f"O aluno {aluno.nome} já possui uma iniciação no curso {nome_curso}."
                )
        
        return cleaned_data

    def clean_data_iniciacao(self):
        data_iniciacao = self.cleaned_data.get('data_iniciacao')
        
        if data_iniciacao and data_iniciacao > date.today():
            raise ValidationError("A data de iniciação não pode ser no futuro.")
        
        return data_iniciacao