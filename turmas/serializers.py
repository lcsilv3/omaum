# c:/projetos/omaum/turmas/serializers.py
from rest_framework import serializers

from alunos.serializers import AlunoSerializer
from cursos.serializers import CursoSerializer
from matriculas.models import Matricula

from .models import Turma


class TurmaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Turma, otimizado para legibilidade e performance.
    """

    curso = CursoSerializer(read_only=True)
    vagas_preenchidas = serializers.IntegerField(
        source='matriculas.count', read_only=True
    )

    class Meta:
        model = Turma
        fields = [
            'id',
            'nome',
            'curso',
            'data_inicio_ativ',
            'data_termino_atividades',
            'vagas',
            'vagas_preenchidas',
            'status',
        ]
        read_only_fields = ['status']


class MatriculaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Matricula.
    """

    aluno = AlunoSerializer(read_only=True)
    turma = TurmaSerializer(read_only=True)

    class Meta:
        model = Matricula
        fields = ['id', 'aluno', 'turma', 'data_matricula']