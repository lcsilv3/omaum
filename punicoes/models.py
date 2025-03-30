from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import importlib

# Importando modelos usando importlib para evitar importações circulares
def get_model(app_name, model_name):
    module = importlib.import_module(f"{app_name}.models")
    return getattr(module, model_name)

class TipoPunicao(models.Model):
    GRAVIDADE_CHOICES = [
        ('leve', 'Leve'),
        ('media', 'Média'),
        ('grave', 'Grave'),
        ('gravissima', 'Gravíssima'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    gravidade = models.CharField(max_length=20, choices=GRAVIDADE_CHOICES, default='media')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Tipo de Punição'
        verbose_name_plural = 'Tipos de Punição'
        ordering = ['nome']

class Punicao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    aluno = models.ForeignKey('alunos.Aluno', on_delete=models.CASCADE, related_name='punicoes')
    tipo_punicao = models.ForeignKey(TipoPunicao, on_delete=models.PROTECT, related_name='punicoes')
    descricao = models.TextField()
    data_aplicacao = models.DateField()
    data_termino = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True, null=True)
    
    # Campos de auditoria
    registrado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='punicoes_registradas')
    data_registro = models.DateTimeField(default=timezone.now)
    atualizado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='punicoes_atualizadas', null=True, blank=True)
    data_atualizacao = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Atualiza a data de atualização quando o objeto é modificado
        if self.pk:
            self.data_atualizacao = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Punição de {self.aluno.nome} - {self.tipo_punicao.nome}"
    
    class Meta:
        verbose_name = 'Punição'
        verbose_name_plural = 'Punições'
        ordering = ['-data_aplicacao']
