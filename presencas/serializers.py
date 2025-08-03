from rest_framework import serializers
from .models import Presenca, PresencaDetalhada, ConfiguracaoPresenca, TotalAtividadeMes, ObservacaoPresenca
# Serializer para ObservacaoPresenca
class ObservacaoPresencaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    atividade_nome = serializers.CharField(source='atividade.nome', read_only=True)

    class Meta:
        model = ObservacaoPresenca
        fields = [
            'id', 'aluno', 'aluno_nome', 'turma', 'turma_nome',
            'atividade', 'atividade_nome', 'data', 'texto',
            'registrado_por', 'data_registro'
        ]


class PresencaSerializer(serializers.ModelSerializer):
    """Serializer para modelo Presenca básico."""
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    atividade_nome = serializers.CharField(source='atividade.nome', read_only=True)
    
    class Meta:
        model = Presenca
        fields = '__all__'


class PresencaDetalhadaSerializer(serializers.ModelSerializer):
    """Serializer para PresencaDetalhada com campos calculados."""
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    atividade_nome = serializers.CharField(source='atividade.nome', read_only=True)
    periodo_display = serializers.SerializerMethodField()
    
    class Meta:
        model = PresencaDetalhada
        fields = [
            'id', 'aluno', 'aluno_nome', 'turma', 'turma_nome', 
            'atividade', 'atividade_nome', 'periodo', 'periodo_display',
            'convocacoes', 'presencas', 'faltas', 'voluntario_extra', 
            'voluntario_simples', 'percentual_presenca', 'total_voluntarios',
            'carencias', 'registrado_por', 'data_registro', 'data_atualizacao'
        ]
        read_only_fields = ['percentual_presenca', 'total_voluntarios', 'carencias']
    
    def get_periodo_display(self, obj):
        """Retorna período formatado."""
        if obj.periodo:
            return obj.periodo.strftime('%m/%Y')
        return None
    
    def validate(self, data):
        """Validações customizadas."""
        # Validar que P + F <= C
        if data.get('presencas', 0) + data.get('faltas', 0) > data.get('convocacoes', 0):
            raise serializers.ValidationError(
                "A soma de presenças e faltas não pode ser maior que convocações"
            )
        
        # Validar período (primeiro dia do mês)
        periodo = data.get('periodo')
        if periodo and periodo.day != 1:
            raise serializers.ValidationError({
                'periodo': "O período deve ser o primeiro dia do mês"
            })
        
        return data


class ConfiguracaoPresencaSerializer(serializers.ModelSerializer):
    """Serializer para ConfiguracaoPresenca."""
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    atividade_nome = serializers.CharField(source='atividade.nome', read_only=True)
    
    class Meta:
        model = ConfiguracaoPresenca
        fields = [
            'id', 'turma', 'turma_nome', 'atividade', 'atividade_nome',
            'limite_carencia_0_25', 'limite_carencia_26_50', 
            'limite_carencia_51_75', 'limite_carencia_76_100',
            'obrigatoria', 'peso_calculo', 'ativo', 'registrado_por',
            'data_registro', 'data_atualizacao'
        ]


class PresencaLoteSerializer(serializers.Serializer):
    """Serializer para atualização em lote."""
    aluno_id = serializers.IntegerField()
    turma_id = serializers.IntegerField()
    atividade_id = serializers.IntegerField()
    periodo = serializers.DateField()
    convocacoes = serializers.IntegerField(min_value=0, default=0)
    presencas = serializers.IntegerField(min_value=0, default=0)
    faltas = serializers.IntegerField(min_value=0, default=0)
    voluntario_extra = serializers.IntegerField(min_value=0, default=0)
    voluntario_simples = serializers.IntegerField(min_value=0, default=0)
    
    def validate(self, data):
        """Validações para lote."""
        # Validar soma P + F <= C
        if data['presencas'] + data['faltas'] > data['convocacoes']:
            raise serializers.ValidationError(
                "A soma de presenças e faltas não pode ser maior que convocações"
            )
        
        # Validar período
        if data['periodo'].day != 1:
            raise serializers.ValidationError({
                'periodo': "O período deve ser o primeiro dia do mês"
            })
        
        return data


class BuscaAlunoSerializer(serializers.Serializer):
    """Serializer para busca de alunos."""
    q = serializers.CharField(max_length=255)
    turma_id = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(default=20, max_value=100)
    
    def validate_q(self, value):
        """Validar termo de busca."""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Termo de busca deve ter pelo menos 2 caracteres")
        return value.strip()



# Serializer para TotalAtividadeMes
class TotalAtividadeMesSerializer(serializers.ModelSerializer):
    atividade_nome = serializers.CharField(source='atividade.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)

    class Meta:
        model = TotalAtividadeMes
        fields = [
            'id', 'atividade', 'atividade_nome', 'turma', 'turma_nome',
            'ano', 'mes', 'qtd_ativ_mes', 'registrado_por', 'data_registro'
        ]
