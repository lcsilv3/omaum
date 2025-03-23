from django.db import models
from django.utils import timezone

class Professor(models.Model):
    """Modelo para armazenar informações dos professores"""
    nome = models.CharField(max_length=100, verbose_name="Nome completo")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")
    especialidade = models.CharField(max_length=100, verbose_name="Especialidade")
    data_cadastro = models.DateTimeField(default=timezone.now, verbose_name="Data de cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    def __str__(self):
        return self.nome
    
    @property
    def turmas(self):
        """Retorna as turmas associadas ao professor"""
        return self.turma_set.all()
    
    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ['nome']

class HistoricoAlteracaoProfessor(models.Model):
    """Modelo para rastrear alterações nos dados dos professores"""
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='historico')
    campo = models.CharField(max_length=50)
    valor_antigo = models.TextField(blank=True, null=True)
    valor_novo = models.TextField(blank=True, null=True)
    usuario = models.CharField(max_length=100)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Histórico de Alteração"
        verbose_name_plural = "Histórico de Alterações"
        ordering = ['-data_alteracao']
