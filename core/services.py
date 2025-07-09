"""
Serviços para o app core.
"""
from typing import Optional, Dict, Any
from django.db.models import QuerySet
from .models import ConfiguracaoSistema, LogAtividade
from .repositories import ConfiguracaoSistemaRepository, LogAtividadeRepository


class ConfiguracaoService:
    """Serviço para lógica de negócio relacionada a ConfiguracaoSistema."""
    
    def __init__(self):
        self.repository = ConfiguracaoSistemaRepository()
    
    def obter_configuracao(self, chave: str) -> Optional[str]:
        """Obtém uma configuração por chave."""
        return self.repository.get_valor_por_chave(chave)
    
    def definir_configuracao(self, chave: str, valor: str,
                             descricao: str = None) -> ConfiguracaoSistema:
        """Define uma configuração."""
        if not chave or not chave.strip():
            raise ValueError("A chave da configuração é obrigatória")
        
        if not valor or not valor.strip():
            raise ValueError("O valor da configuração é obrigatório")
        
        config = self.repository.get_by_chave(chave.strip())
        if config:
            return self.repository.update(
                config,
                valor=valor.strip(),
                descricao=descricao.strip() if descricao else None
            )
        else:
            return self.repository.create(
                chave=chave.strip(),
                valor=valor.strip(),
                descricao=descricao.strip() if descricao else None
            )
    
    def listar_configuracoes(self) -> QuerySet[ConfiguracaoSistema]:
        """Lista todas as configurações."""
        return self.repository.get_all()
    
    def remover_configuracao(self, chave: str) -> bool:
        """Remove uma configuração."""
        config = self.repository.get_by_chave(chave)
        if config:
            return self.repository.delete(config)
        return False
    
    def obter_configuracoes_como_dict(self) -> Dict[str, str]:
        """Obtém todas as configurações como dicionário."""
        return self.repository.get_todas_como_dict()


class LogAtividadeService:
    """Serviço para lógica de negócio relacionada a LogAtividade."""
    
    def __init__(self):
        self.repository = LogAtividadeRepository()
    
    def registrar_atividade(self, usuario_id: int, acao: str,
                            detalhes: str = None) -> LogAtividade:
        """Registra uma nova atividade no log."""
        if not usuario_id:
            raise ValueError("O ID do usuário é obrigatório")
        
        if not acao or not acao.strip():
            raise ValueError("A ação é obrigatória")
        
        return self.repository.create(
            usuario_id=usuario_id,
            acao=acao.strip(),
            detalhes=detalhes.strip() if detalhes else None
        )
    
    def obter_logs_do_usuario(self, usuario_id: int) -> QuerySet[LogAtividade]:
        """Obtém logs de um usuário específico."""
        return self.repository.get_por_usuario(usuario_id)
    
    def obter_logs_recentes(self, limit: int = 50) -> QuerySet[LogAtividade]:
        """Obtém logs mais recentes."""
        return self.repository.get_recentes(limit)
    
    def obter_logs_por_acao(self, acao: str) -> QuerySet[LogAtividade]:
        """Obtém logs por tipo de ação."""
        return self.repository.get_por_acao(acao)
    
    def buscar_logs(self, termo: str) -> QuerySet[LogAtividade]:
        """Busca logs por termo."""
        return self.repository.buscar(termo)
    
    def limpar_logs_antigos(self, dias: int = 30) -> int:
        """Remove logs antigos."""
        return self.repository.limpar_antigos(dias)
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas dos logs."""
        return {
            'total_logs': self.repository.count(),
            'logs_hoje': self.repository.count_hoje(),
            'logs_recentes': self.repository.get_recentes(10)
        }
