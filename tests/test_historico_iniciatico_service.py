import pytest
from datetime import date
from alunos.models import Aluno
from alunos.utils import get_tipo_codigo_model, get_codigo_model
from alunos.services import criar_evento_iniciatico, sincronizar_historico_iniciatico

pytestmark = pytest.mark.django_db


def criar_aluno_basico():
    return Aluno.objects.create(
        nome="Teste",
        cpf="12345678901",
        email="t@example.com",
        situacao_iniciatica="ATIVO",
    data_nascimento=date(2000, 1, 1),
    )


def criar_codigo_basico():
    TipoCodigo = get_tipo_codigo_model()
    Codigo = get_codigo_model()
    tipo = TipoCodigo.objects.create(nome="CARGO")
    return Codigo.objects.create(tipo_codigo=tipo, nome="Instrutor")


def test_criar_evento_iniciatico_incremental():
    aluno = criar_aluno_basico()
    codigo = criar_codigo_basico()
    resultado = criar_evento_iniciatico(
        aluno=aluno,
        codigo=codigo,
        tipo_evento="CARGO",
        data_os=date.today(),
        data_evento=date.today(),
        observacoes="Primeiro evento",
    )
    assert resultado["registro"].id is not None
    assert len(aluno.historico_iniciatico) == 1
    evento_json = resultado["evento_json"]
    assert evento_json["tipo"] == "CARGO"


def test_sincronizar_reconstroi_json():
    aluno = criar_aluno_basico()
    codigo = criar_codigo_basico()
    # cria dois eventos
    criar_evento_iniciatico(
        aluno=aluno,
        codigo=codigo,
        tipo_evento="CARGO",
        data_os=date.today(),
        data_evento=date.today(),
        observacoes="E1",
    )
    criar_evento_iniciatico(
        aluno=aluno,
        codigo=codigo,
        tipo_evento="CARGO",
        data_os=date.today(),
        data_evento=date.today(),
        observacoes="E2",
    )
    # corrompe manualmente JSON
    aluno.historico_iniciatico = []
    aluno.save(update_fields=["historico_iniciatico"])
    eventos = sincronizar_historico_iniciatico(aluno)
    assert len(eventos) == 2
    assert aluno.historico_iniciatico[0]["data"] >= aluno.historico_iniciatico[-1]["data"]


def test_reconciliar_detecta_divergencia(monkeypatch):
    from alunos.services import reconciliar_historico_if_divergente

    aluno = criar_aluno_basico()
    codigo = criar_codigo_basico()
    criar_evento_iniciatico(
        aluno=aluno,
        codigo=codigo,
        tipo_evento="CARGO",
        data_os=date.today(),
        data_evento=date.today(),
        observacoes="X",
    )
    # remove JSON para simular divergência
    aluno.historico_iniciatico = []
    aluno.save(update_fields=["historico_iniciatico"])
    reconciliar_historico_if_divergente(aluno)
    assert len(aluno.historico_iniciatico) == 1


def test_checksum_atualizado_incremental():
    """Verifica que o checksum é calculado e muda após novo evento."""
    from alunos.models import Aluno
    from alunos.utils import get_tipo_codigo_model, get_codigo_model
    from alunos.services import criar_evento_iniciatico
    import hashlib, json
    from datetime import date

    aluno = criar_aluno_basico()
    TipoCodigo = get_tipo_codigo_model()
    Codigo = get_codigo_model()
    tipo = TipoCodigo.objects.create(nome="GRAU")
    codigo = Codigo.objects.create(tipo_codigo=tipo, nome="Aprendiz")
    resultado1 = criar_evento_iniciatico(
        aluno=aluno,
        codigo=codigo,
        tipo_evento="GRAU",
        data_os=date.today(),
        data_evento=date.today(),
        observacoes="Primeiro",
    )
    assert aluno.historico_checksum is not None
    checksum1 = aluno.historico_checksum
    # Recalcula manualmente
    manual1 = hashlib.sha256(json.dumps(aluno.historico_iniciatico, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    assert checksum1 == manual1

    # Segundo evento
    criar_evento_iniciatico(
        aluno=aluno,
        codigo=codigo,
        tipo_evento="GRAU",
        data_os=date.today(),
        data_evento=date.today(),
        observacoes="Segundo",
    )
    aluno.refresh_from_db()
    assert aluno.historico_checksum is not None
    checksum2 = aluno.historico_checksum
    assert checksum2 != checksum1
    manual2 = hashlib.sha256(json.dumps(aluno.historico_iniciatico, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    assert checksum2 == manual2


def test_checksum_reconstruido_em_sincronizar():
    from alunos.services import sincronizar_historico_iniciatico
    import hashlib, json
    from datetime import date

    aluno = criar_aluno_basico()
    codigo = criar_codigo_basico()
    criar_evento_iniciatico(
        aluno=aluno,
        codigo=codigo,
        tipo_evento="CARGO",
        data_os=date.today(),
        data_evento=date.today(),
        observacoes="E1",
    )
    checksum_original = aluno.historico_checksum
    # corrompe JSON
    aluno.historico_iniciatico.append({"tipo": "X", "descricao": "Y", "data": "1900-01-01"})
    aluno.save(update_fields=["historico_iniciatico"])
    sincronizar_historico_iniciatico(aluno)
    aluno.refresh_from_db()
    # Deve recomputar e diferente do corrompido, mas possivelmente igual ao original se reconstrução fiel
    manual = hashlib.sha256(json.dumps(aluno.historico_iniciatico, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    assert aluno.historico_checksum == manual


def test_verificar_integridade_historico_sem_divergencia():
    from alunos.services import verificar_integridade_historico
    from datetime import date
    aluno = criar_aluno_basico()
    codigo = criar_codigo_basico()
    criar_evento_iniciatico(
        aluno=aluno,
        codigo=codigo,
        tipo_evento="CARGO",
        data_os=date.today(),
        data_evento=date.today(),
        observacoes="E1",
    )
    resultado = verificar_integridade_historico(aluno)
    assert resultado["integro"] is True
    assert resultado["checksum_atual"] == resultado["checksum_recomputado"]


def test_verificar_integridade_historico_com_reparo():
    from alunos.services import verificar_integridade_historico
    from datetime import date
    aluno = criar_aluno_basico()
    codigo = criar_codigo_basico()
    criar_evento_iniciatico(
        aluno=aluno,
        codigo=codigo,
        tipo_evento="CARGO",
        data_os=date.today(),
        data_evento=date.today(),
        observacoes="E1",
    )
    # Corrompe checksum
    aluno.historico_checksum = "xxx"
    aluno.save(update_fields=["historico_checksum"])
    resultado = verificar_integridade_historico(aluno, reparar=True)
    assert resultado["integro"] is True
    assert resultado["reparado"] is True


def test_get_codigo_model_prioriza_alunos():
    from alunos.utils import get_codigo_model
    from alunos.models import Codigo as CodigoAlunos
    CodigoResolved = get_codigo_model()
    assert CodigoResolved is CodigoAlunos
