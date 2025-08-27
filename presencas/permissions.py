class PresencaPermissionEngine:
    """
    Engine de permissões para presenças acadêmicas.
    """

    @staticmethod
    def pode_alterar_presenca(presenca, user):
        # Exemplo: só pode editar se for superuser ou criador
        if user.is_superuser:
            return True, None
        if (
            hasattr(presenca, "registrado_por")
            and presenca.registrado_por == user.username
        ):
            return True, None
        return False, "Usuário não tem permissão para editar esta presença."

    @staticmethod
    def pode_excluir_presenca(presenca, user):
        # Exemplo: só pode excluir se for superuser
        if user.is_superuser:
            return True, None
        return False, "Usuário não tem permissão para excluir esta presença."
