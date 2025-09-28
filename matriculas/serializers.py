"""Serializers para o aplicativo Matriculas."""

from rest_framework import serializers
from .models import Matricula


class MatriculaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Matricula."""

    aluno = serializers.SerializerMethodField()
    turma = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = ["id", "aluno", "turma", "data_matricula"]

    def get_aluno(self, obj):
        """Carrega dinamicamente o AlunoSerializer para evitar importação circular."""
        from alunos.serializers import AlunoSerializer
        return AlunoSerializer(obj.aluno).data

    def get_turma(self, obj):
        """Carrega dinamicamente o TurmaSerializer para evitar importação circular."""
        from turmas.serializers import TurmaSerializer
        return TurmaSerializer(obj.turma).data