import functools


def api_exception_handler(view_func):
    """
    Decorator placeholder para tratar exceções da API.
    TODO: Implementar a lógica de tratamento de exceção.
    """

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # Por enquanto, apenas chama a view original sem tratamento.
        return view_func(*args, **kwargs)

    return wrapper
