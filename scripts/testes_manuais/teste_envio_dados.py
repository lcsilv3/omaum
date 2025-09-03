#!/usr/bin/env python
"""
Script para simular exatamente o envio de dados do frontend para testar o backend
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

import json
from datetime import date
from django.utils import timezone
from presencas.models import PresencaAcademica
from alunos.models import Aluno
from turmas.models import Turma
from django.apps import apps


def get_model_class(model_name):
    """Obtém classe de modelo dinamicamente para evitar imports circulares."""
    return apps.get_model("atividades", model_name)


def simular_envio_dados():
    """
    Simula exatamente os dados que estão sendo enviados pelo frontend
    """
    print("🔍 SIMULAÇÃO DO ENVIO DE DADOS DO FRONTEND")
    print("=" * 60)

    # Dados exatos do console do frontend
    presencas_json = '{"1":{"1":{"81991045700":{"presente":true,"justificativa":"","convocado":true}}},"2":{"2":{"81991045700":{"presente":false,"justificativa":"","convocado":true}}},"3":{"3":{"81991045700":{"presente":true,"justificativa":"","convocado":false}},"4":{"81991045700":{"presente":false,"justificativa":"","convocado":false}}}}'

    # Simular dados da sessão (você pode ajustar conforme necessário)
    turma_id = 1
    ano = 2025
    mes = 8

    try:
        turma = Turma.objects.get(id=turma_id)
        print(f"🏫 Turma encontrada: {turma.nome}")

        presencas_processadas = 0
        print(f"🎯 presencas_json recebido: {bool(presencas_json)}")
        print(f"🎯 presencas_json conteúdo: {presencas_json}")

        if presencas_json:
            try:
                presencas_data = json.loads(presencas_json)
                print(
                    f"✅ JSON parsed com sucesso: {json.dumps(presencas_data, indent=2)}"
                )

                for atividade_id, dias_data in presencas_data.items():
                    print(f"🔄 Processando atividade {atividade_id}: {dias_data}")
                    for dia, alunos_data in dias_data.items():
                        print(f"🔄 Processando dia {dia}: {alunos_data}")
                        for cpf_aluno, presenca_info in alunos_data.items():
                            print(f"🔄 Processando aluno {cpf_aluno}: {presenca_info}")
                            try:
                                aluno = Aluno.objects.get(cpf=cpf_aluno)
                                Atividade = get_model_class("Atividade")
                                atividade = Atividade.objects.get(id=atividade_id)
                                data_presenca = date(int(ano), int(mes), int(dia))

                                print(
                                    f"✅ Criando presença: Aluno={aluno.nome}, Atividade={atividade.nome}, Data={data_presenca}"
                                )

                                # Simula exatamente o que o view faz
                                presenca_obj, created = (
                                    PresencaAcademica.objects.update_or_create(
                                        aluno=aluno,
                                        turma=turma,
                                        data=data_presenca,
                                        atividade=atividade,
                                        defaults={
                                            "presente": presenca_info.get(
                                                "presente", True
                                            ),
                                            "justificativa": presenca_info.get(
                                                "justificativa", ""
                                            )
                                            if not presenca_info.get("presente", True)
                                            else None,
                                            "registrado_por": "TESTE_SCRIPT",
                                            "data_registro": timezone.now(),
                                        },
                                    )
                                )
                                presencas_processadas += 1
                                print(
                                    f"✅ Presença {'criada' if created else 'atualizada'}: {presenca_obj.id}"
                                )

                            except Exception as e:
                                print(f"❌ Erro ao processar presença {cpf_aluno}: {e}")
                                import traceback

                                traceback.print_exc()
                                continue

            except json.JSONDecodeError as e:
                print(f"❌ Erro ao decodificar JSON de presenças: {e}")

        print(f"📊 RESULTADO FINAL: {presencas_processadas} presenças processadas")

        if presencas_processadas > 0:
            print("✅ SUCESSO - Dados processados com sucesso!")
        else:
            print("❌ FALHA - Nenhuma presença foi processada")

        # Verificar se as presenças foram realmente salvas
        print("\n🔍 VERIFICAÇÃO FINAL:")
        total_presencas = PresencaAcademica.objects.filter(
            registrado_por="TESTE_SCRIPT"
        ).count()
        print(f"📊 Total de presenças criadas pelo script: {total_presencas}")

        if total_presencas > 0:
            print("📋 PRESENÇAS CRIADAS:")
            for p in PresencaAcademica.objects.filter(registrado_por="TESTE_SCRIPT"):
                print(
                    f"   ID: {p.id} | Aluno: {p.aluno.nome} | Atividade: {p.atividade.nome}"
                )
                print(
                    f"      Data: {p.data} | Presente: {p.presente} | Criado: {p.data_registro}"
                )
                print("   ---")

    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    simular_envio_dados()
