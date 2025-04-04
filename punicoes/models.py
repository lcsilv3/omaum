from django.db import models
from django.contrib.auth.models import User
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

class TipoPunicao(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Tipo de Punição'
        verbose_name_plural = 'Tipos de Punição'
        ordering = ['nome']

class Punicao(models.Model):
    aluno = models.ForeignKey(
        get_aluno_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Aluno',
        to_field='cpf'  # Especificar que estamos referenciando o campo cpf
    )
    tipo_punicao = models.ForeignKey(
        TipoPunicao, 
        on_delete=models.CASCADE, 
        verbose_name='Tipo de Punição'
    )
    data_aplicacao = models.DateField(verbose_name='Data de Aplicação')
    motivo = models.TextField(verbose_name='Motivo')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    aplicada_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='Aplicada por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f"{self.aluno.nome} - {self.tipo_punicao.nome} - {self.data_aplicacao}"

    class Meta:
        verbose_name = 'Punição'
        verbose_name_plural = 'Punições'
        ordering = ['-data_aplicacao', 'aluno__nome']
