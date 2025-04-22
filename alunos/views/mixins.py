class AlunoQuerysetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        # Lógica comum de filtragem
        return queryset