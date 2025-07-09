"""
Serializers para o app relatorios.
"""
from rest_framework import serializers
from .models import Relatorio


class RelatorioSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Relatorio."""
    
    class Meta:
        model = Relatorio
        fields = ['id', 'titulo', 'conteudo', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']
    
    def validate_titulo(self, value):
        """Valida o título do relatório."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "O título do relatório é obrigatório"
            )
        return value.strip()
    
    def validate_conteudo(self, value):
        """Valida o conteúdo do relatório."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "O conteúdo do relatório é obrigatório"
            )
        return value.strip()


class RelatorioCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de relatório."""
    
    class Meta:
        model = Relatorio
        fields = ['titulo', 'conteudo']
    
    def validate_titulo(self, value):
        """Valida o título do relatório."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "O título do relatório é obrigatório"
            )
        
        # Verifica se já existe um relatório com o mesmo título
        if Relatorio.objects.filter(titulo=value.strip()).exists():
            raise serializers.ValidationError(
                "Já existe um relatório com este título"
            )
        
        return value.strip()
    
    def validate_conteudo(self, value):
        """Valida o conteúdo do relatório."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "O conteúdo do relatório é obrigatório"
            )
        return value.strip()


class RelatorioUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de relatório."""
    
    class Meta:
        model = Relatorio
        fields = ['titulo', 'conteudo']
        extra_kwargs = {
            'titulo': {'required': False},
            'conteudo': {'required': False}
        }
    
    def validate_titulo(self, value):
        """Valida o título do relatório."""
        if value is not None:
            if not value or not value.strip():
                raise serializers.ValidationError(
                    "O título do relatório não pode estar vazio"
                )
            
            # Verifica se já existe outro relatório com o mesmo título
            instance = self.instance
            if (instance and
                    Relatorio.objects.filter(titulo=value.strip())
                    .exclude(id=instance.id).exists()):
                raise serializers.ValidationError(
                    "Já existe um relatório com este título"
                )
            
            return value.strip()
        return value
    
    def validate_conteudo(self, value):
        """Valida o conteúdo do relatório."""
        if value is not None:
            if not value or not value.strip():
                raise serializers.ValidationError(
                    "O conteúdo do relatório não pode estar vazio"
                )
            return value.strip()
        return value
