from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Iniciacao, GrauIniciacao

class IniciacaoForm(forms.ModelForm):
    class Meta:
        model = Iniciacao
        # Remova 'nome' da lista de campos
        fields = ['aluno', 'curso', 'data_iniciacao', 'grau', 'observacoes']
        widgets = {
            'data_iniciacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'grau': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'aluno': 'Aluno',
            'curso': 'Curso',
            'data_iniciacao': 'Data de Iniciação',
            'grau': 'Grau',
            'observacoes': 'Observações'
        }
        help_texts = {
            'curso': 'Selecione o curso de iniciação',
            'data_iniciacao': 'Selecione a data em que o aluno foi iniciado no curso'
        }

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        curso = cleaned_data.get('curso')
        data_iniciacao = cleaned_data.get('data_iniciacao')

        # Verifica se já existe uma iniciação para este aluno neste curso
        if aluno and curso:
            # Exclui a instância atual em caso de edição
            instance_id = self.instance.id if self.instance else None

            # Verifica se já existe outra iniciação com o mesmo aluno e curso
            if Iniciacao.objects.filter(
                aluno=aluno, 
                curso=curso
            ).exclude(id=instance_id).exists():
                raise ValidationError(
                    f"O aluno {aluno.nome} já possui uma iniciação no curso {curso.nome}."
                )

        return cleaned_data

    def clean_data_iniciacao(self):
        data_iniciacao = self.cleaned_data.get('data_iniciacao')

        if data_iniciacao and data_iniciacao > date.today():
            raise ValidationError("A data de iniciação não pode ser no futuro.")

        return data_iniciacao

class GrauIniciacaoForm(forms.ModelForm):
    class Meta:
        model = GrauIniciacao
        fields = ['nome', 'descricao', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if ordem <= 0:
            raise ValidationError("A ordem deve ser um número positivo.")
        return ordem