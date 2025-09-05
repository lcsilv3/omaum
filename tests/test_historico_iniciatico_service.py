import pytest

pytestmark = pytest.mark.django_db


def test_get_codigo_model_prioriza_alunos():
    from alunos.utils import get_codigo_model
    from alunos.models import Codigo as CodigoAlunos

    CodigoResolved = get_codigo_model()
    assert CodigoResolved is CodigoAlunos
