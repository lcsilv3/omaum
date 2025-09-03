"""
Repositórios para o app Core.
Este módulo contém todas as operações de acesso a dados do core do sistema,
incluindo configurações e logs de atividade.
"""

from django.db.models import QuerySet, Q
from datetime import date, datetime
from typing import Optional, Dict
from .models import ConfiguracaoSistema, LogAtividade


class ConfiguracaoSistemaRepository:
    """Repository para operações de acesso a dados de ConfiguracaoSistema."""

    @staticmethod
    def get_all() -> QuerySet[ConfiguracaoSistema]:
        """Retorna todas as configurações."""
        return ConfiguracaoSistema.objects.all()

    @staticmethod
    def get_by_chave(chave: str) -> Optional[ConfiguracaoSistema]:
        """Retorna uma configuração por chave."""
        try:
            return ConfiguracaoSistema.objects.get(chave=chave)
        except ConfiguracaoSistema.DoesNotExist:
            return None

    @staticmethod
    def get_valor_por_chave(chave: str) -> Optional[str]:
        """Retorna o valor de uma configuração por chave."""
        config = ConfiguracaoSistemaRepository.get_by_chave(chave)
        return config.valor if config else None

    @staticmethod
    def create(chave: str, valor: str, descricao: str = None) -> ConfiguracaoSistema:
        """Cria uma nova configuração."""
        return ConfiguracaoSistema.objects.create(
            chave=chave, valor=valor, descricao=descricao
        )

    @staticmethod
    def update(
        config: ConfiguracaoSistema, valor: str = None, descricao: str = None
    ) -> ConfiguracaoSistema:
        """Atualiza uma configuração existente."""
        if valor is not None:
            config.valor = valor
        if descricao is not None:
            config.descricao = descricao
        config.save()
        return config

    @staticmethod
    def delete(config: ConfiguracaoSistema) -> bool:
        """Remove uma configuração."""
        try:
            config.delete()
            return True
        except Exception:
            return False

    @staticmethod
    def get_todas_como_dict() -> Dict[str, str]:
        """Retorna todas as configurações como dicionário."""
        return {
            config.chave: config.valor for config in ConfiguracaoSistema.objects.all()
        }

    @staticmethod
    def get_configuracao_atual() -> ConfiguracaoSistema:
        """Retorna a configuração atual do sistema (única instância)."""
        config, created = ConfiguracaoSistema.objects.get_or_create(
            pk=1,
            defaults={
                "nome_sistema": "OMAUM",
                "versao": "1.0",
                "em_manutencao": False,
                "mensagem_manutencao": "",
            },
        )
        return config

    @staticmethod
    def atualizar_configuracao(**dados) -> ConfiguracaoSistema:
        """Atualiza a configuração do sistema."""
        config = ConfiguracaoSistemaRepository.get_configuracao_atual()
        for campo, valor in dados.items():
            setattr(config, campo, valor)
        config.save()
        return config

    @staticmethod
    def ativar_manutencao(mensagem: str = "") -> ConfiguracaoSistema:
        """Ativa o modo de manutenção."""
        return ConfiguracaoSistemaRepository.atualizar_configuracao(
            manutencao_ativa=True, mensagem_manutencao=mensagem
        )

    @staticmethod
    def desativar_manutencao() -> ConfiguracaoSistema:
        """Desativa o modo de manutenção."""
        return ConfiguracaoSistemaRepository.atualizar_configuracao(
            manutencao_ativa=False, mensagem_manutencao=""
        )


class LogAtividadeRepository:
    """Repository para operações de acesso a dados de LogAtividade."""

    @staticmethod
    def get_all() -> QuerySet[LogAtividade]:
        """Retorna todos os logs ordenados por data
        (mais recentes primeiro)."""
        return LogAtividade.objects.all().order_by("-data")

    @staticmethod
    def get_by_usuario(usuario: str) -> QuerySet[LogAtividade]:
        """Retorna logs de um usuário específico."""
        return LogAtividade.objects.filter(usuario=usuario).order_by("-data")

    @staticmethod
    def get_by_tipo(tipo: str) -> QuerySet[LogAtividade]:
        """Retorna logs de um tipo específico."""
        return LogAtividade.objects.filter(tipo=tipo).order_by("-data")

    @staticmethod
    def get_by_periodo(
        data_inicio: datetime, data_fim: datetime
    ) -> QuerySet[LogAtividade]:
        """Retorna logs em um período específico."""
        return LogAtividade.objects.filter(
            data__gte=data_inicio, data__lte=data_fim
        ).order_by("-data")

    @staticmethod
    def get_recentes(limite: int = 50) -> QuerySet[LogAtividade]:
        """Retorna os logs mais recentes."""
        return LogAtividade.objects.all().order_by("-data")[:limite]

    @staticmethod
    def search(termo: str) -> QuerySet[LogAtividade]:
        """Busca logs por termo (ação ou detalhes)."""
        return LogAtividade.objects.filter(
            Q(acao__icontains=termo) | Q(detalhes__icontains=termo)
        ).order_by("-data")

    @staticmethod
    def create_log(
        usuario: str, acao: str, tipo: str = "INFO", detalhes: str = ""
    ) -> LogAtividade:
        """Cria um novo log de atividade."""
        return LogAtividade.objects.create(
            usuario=usuario, acao=acao, tipo=tipo, detalhes=detalhes
        )

    @staticmethod
    def delete_logs_antigos(dias: int = 90) -> int:
        """Remove logs antigos (padrão: 90 dias)."""
        from datetime import timedelta

        data_limite = datetime.now() - timedelta(days=dias)
        logs_antigos = LogAtividade.objects.filter(data__lt=data_limite)
        count = logs_antigos.count()
        logs_antigos.delete()
        return count

    @staticmethod
    def count_by_tipo() -> dict:
        """Retorna contagem de logs por tipo."""
        from django.db.models import Count

        return dict(
            LogAtividade.objects.values("tipo")
            .annotate(count=Count("tipo"))
            .values_list("tipo", "count")
        )

    @staticmethod
    def get_ultimos_erros(limite: int = 10) -> QuerySet[LogAtividade]:
        """Retorna os últimos logs de erro."""
        return LogAtividade.objects.filter(tipo="ERRO").order_by("-data")[:limite]

    @staticmethod
    def get_por_usuario(usuario_id: int) -> QuerySet[LogAtividade]:
        """Retorna logs de um usuário específico."""
        return LogAtividade.objects.filter(usuario_id=usuario_id).order_by("-data_hora")

    @staticmethod
    def get_por_acao(acao: str) -> QuerySet[LogAtividade]:
        """Retorna logs por ação."""
        return LogAtividade.objects.filter(acao__icontains=acao).order_by("-data_hora")

    @staticmethod
    def buscar(termo: str) -> QuerySet[LogAtividade]:
        """Busca logs por termo."""
        return LogAtividade.objects.filter(
            Q(acao__icontains=termo) | Q(detalhes__icontains=termo)
        ).order_by("-data_hora")

    @staticmethod
    def create(usuario_id: int, acao: str, detalhes: str = None) -> LogAtividade:
        """Cria um novo log de atividade."""
        return LogAtividade.objects.create(
            usuario_id=usuario_id, acao=acao, detalhes=detalhes
        )

    @staticmethod
    def count() -> int:
        """Retorna o número total de logs."""
        return LogAtividade.objects.count()

    @staticmethod
    def count_hoje() -> int:
        """Retorna o número de logs de hoje."""
        hoje = date.today()
        return LogAtividade.objects.filter(data_hora__date=hoje).count()

    @staticmethod
    def limpar_antigos(dias: int = 30) -> int:
        """Remove logs antigos."""
        from datetime import timedelta

        data_limite = datetime.now() - timedelta(days=dias)
        logs_antigos = LogAtividade.objects.filter(data_hora__lt=data_limite)
        count = logs_antigos.count()
        logs_antigos.delete()
        return count
