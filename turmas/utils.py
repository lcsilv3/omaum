# turmas/utils.py
from core.utils import get_model_dynamically

def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    return get_model_dynamically("turmas", "Turma")
