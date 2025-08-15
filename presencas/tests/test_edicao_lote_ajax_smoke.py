import json
from datetime import date, time

import pytest
from django.urls import reverse
from django.contrib.auth.models import User

from alunos.models import Aluno
from cursos.models import Curso
from turmas.models import Turma
from atividades.models import Atividade
from presencas.models import Presenca, ConvocacaoPresenca


@pytest.mark.django_db(transaction=True)
def test_edicao_lote_ajax_create_update_delete(client):
    # Setup: usuário, curso, turma, aluno, atividade
    user = User.objects.create_user(username="tester", password="x")
    client.force_login(user)

    curso = Curso.objects.create(nome="Curso X")
    turma = Turma.objects.create(nome="T1", curso=curso, ativo=True)
    aluno = Aluno.objects.create(
        cpf="12345678901",
        nome="Fulano",
        data_nascimento=date(2000, 1, 1),
        email="f@x.com",
    )
    atividade = Atividade.objects.create(
        nome="Aula 1",
        data_inicio=date(2025, 8, 1),
        hora_inicio=time(19, 0),
        curso=curso,
        ativo=True,
        convocacao=True,
    )
    atividade.turmas.add(turma)

    # Sessão requerida pelo fluxo
    session = client.session
    session["edicao_lote_turma_id"] = turma.id
    session["edicao_lote_ano"] = 2025
    session["edicao_lote_mes"] = 8
    session.save()

    url = reverse("presencas:editar_lote_dias_atividades_ajax")

    # 1) CREATE presença + convocação
    payload = {
        "exclusoes": {},
        "presencas": {
            str(atividade.id): {
                "1": {
                    aluno.cpf: {
                        "presente": True,
                        "justificativa": "",
                        "convocado": True,
                    }
                }
            }
        },
    }
    resp = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200, resp.content
    data = resp.json()
    assert data["success"] is True
    assert data["alteracoes"] >= 1

    assert Presenca.objects.filter(
        aluno=aluno, turma=turma, atividade=atividade, data=date(2025, 8, 1)
    ).exists()
    conv = ConvocacaoPresenca.objects.get(
        aluno=aluno, turma=turma, atividade=atividade, data=date(2025, 8, 1)
    )
    assert conv.convocado is True

    # 2) UPDATE para ausente com justificativa e desconvocar
    payload["presencas"][str(atividade.id)]["1"][aluno.cpf] = {
        "presente": False,
        "justificativa": "Atestado",
        "convocado": False,
    }
    resp = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200
    p = Presenca.objects.get(
        aluno=aluno, turma=turma, atividade=atividade, data=date(2025, 8, 1)
    )
    assert p.presente is False
    assert p.justificativa == "Atestado"
    conv.refresh_from_db()
    assert conv.convocado is False

    # 3) DELETE presença e convocação
    payload = {"exclusoes": {str(atividade.id): {"1": [aluno.cpf]}}, "presencas": {}}
    resp = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200
    assert not Presenca.objects.filter(
        aluno=aluno, turma=turma, atividade=atividade, data=date(2025, 8, 1)
    ).exists()
    assert not ConvocacaoPresenca.objects.filter(
        aluno=aluno, turma=turma, atividade=atividade, data=date(2025, 8, 1)
    ).exists()
