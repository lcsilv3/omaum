from pathlib import Path

def verify(path):
    """
    Verifica se um caminho existe e retorna o caminho absoluto.
    Se o caminho não existir, lança uma exceção ValueError.

    :param path: O caminho a ser verificado (pode ser uma string ou um objeto Path)
    :return: O caminho absoluto como um objeto Path
    :raises ValueError: Se o caminho não existir
    """
    path = Path(path)
    if path.exists():
        return path.resolve()
    else:
        raise ValueError(f"O caminho {path} não existe")

# Você pode adicionar outras funções utilitárias aqui, se necessário