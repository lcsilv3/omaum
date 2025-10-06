"""Popula um aluno com histórico JSON legado para fins de teste da migração."""

from __future__ import annotations

from datetime import date

from django.db import transaction
from django.utils import timezone

from alunos.models import Aluno, Codigo, TipoCodigo


def run() -> None:
    """Cria (ou atualiza) registros de demonstração para o histórico legado."""

    with transaction.atomic():
        tipo, _ = TipoCodigo.objects.get_or_create(
            nome="Demo Legado",
            defaults={"descricao": "Tipo criado para demonstrar migração JSON."},
        )

        codigo, _ = Codigo.objects.get_or_create(
            tipo_codigo=tipo,
            nome="Evento Iniciático Demo",
            defaults={"descricao": "Código usado na migração de demonstração."},
        )

        aluno, created = Aluno.objects.get_or_create(
            cpf="99988877766",
            defaults={
                "nome": "Aluno Legado Demo",
                "data_nascimento": date(1990, 5, 20),
                "email": "aluno.legado.demo@example.com",
                "sexo": "M",
                "numero_iniciatico": "DEM0001",
            },
        )

        aluno.historico_iniciatico = [
            {
                "codigo_id": codigo.id,
                "descricao": codigo.nome,
                "data": "2018-03-12",
                "ordem_servico": "DEM/2018",
                "observacoes": "Registro legado importado via script.",
                "registrado_em": "2018-03-12T10:00:00",
            },
            {
                "codigo_id": codigo.id,
                "descricao": codigo.nome,
                "data": "2019-08-04",
                "ordem_servico": "DEM/2019",
                "observacoes": "Outro evento de demonstração criado pelo script.",
                "registrado_em": timezone.now().isoformat(),
            },
        ]
        aluno.historico_checksum = ""
        aluno.save(
            update_fields=["historico_iniciatico", "historico_checksum", "updated_at"]
        )

        acao = "criado" if created else "atualizado"
        print(f"Aluno demo {acao} com histórico JSON legado (CPF=99988877766).")
        print(
            "Pronto para executar: python manage.py migrar_historicos --cpf 99988877766"
        )


if __name__ == "__main__":
    run()
