"""
Serializers para o app core.
"""
from rest_framework import serializers
from .models import ConfiguracaoSistema, LogAtividade


class ConfiguracaoSistemaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo ConfiguracaoSistema."""
    
    class Meta:
        model = ConfiguracaoSistema
        fields = ['id', 'chave', 'valor', 'descricao', 'data_criacao',
                  'data_atualizacao']
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao']
    
    def validate_chave(self, value):
        """Valida a chave da configuração."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "A chave da configuração é obrigatória"
            )
        return value.strip()
    
    def validate_valor(self, value):
        """Valida o valor da configuração."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "O valor da configuração é obrigatório"
            )
        return value.strip()


class ConfiguracaoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de configuração."""
    
    class Meta:
        model = ConfiguracaoSistema
        fields = ['chave', 'valor', 'descricao']
    
    def validate_chave(self, value):
        """Valida a chave da configuração."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "A chave da configuração é obrigatória"
            )
        
        # Verifica se já existe uma configuração com a mesma chave
        if ConfiguracaoSistema.objects.filter(chave=value.strip()).exists():
            raise serializers.ValidationError(
                "Já existe uma configuração com esta chave"
            )
        
        return value.strip()
    
    def validate_valor(self, value):
        """Valida o valor da configuração."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "O valor da configuração é obrigatório"
            )
        return value.strip()


class ConfiguracaoUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de configuração."""
    
    class Meta:
        model = ConfiguracaoSistema
        fields = ['valor', 'descricao']
    
    def validate_valor(self, value):
        """Valida o valor da configuração."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "O valor da configuração é obrigatório"
            )
        return value.strip()


class LogAtividadeSerializer(serializers.ModelSerializer):
    """Serializer para o modelo LogAtividade."""
    
    class Meta:
        model = LogAtividade
        fields = ['id', 'usuario', 'acao', 'detalhes', 'data_hora']
        read_only_fields = ['id', 'data_hora']
    
    def validate_acao(self, value):
        """Valida a ação do log."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "A ação é obrigatória"
            )
        return value.strip()


class LogAtividadeCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de log de atividade."""
    
    class Meta:
        model = LogAtividade
        fields = ['usuario', 'acao', 'detalhes']
    
    def validate_acao(self, value):
        """Valida a ação do log."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "A ação é obrigatória"
            )
        return value.strip()
