"""
Script de auto-correção de dados inconsistentes no módulo de presenças.
Baseado nos padrões aplicados em atividades, turmas e matrículas.
"""

import os
import django

# Configurar Django
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
    django.setup()

    import logging
    from presencas.models import RegistroPresenca
    from django.db import transaction

    logger = logging.getLogger(__name__)

    print("🔍 Iniciando auto-correção do módulo Presenças...")

    # 1. Verificar registros de presença sem turma definida quando há atividade
    with transaction.atomic():
        print("\n📋 Verificando registros de presença sem turma quando há atividade...")
        presencas_sem_turma = RegistroPresenca.objects.filter(
            turma__isnull=True, atividade__isnull=False
        ).select_related("atividade")

        corrigidas_turma = 0
        for presenca in presencas_sem_turma:
            if (
                hasattr(presenca.atividade, "turmas")
                and presenca.atividade.turmas.exists()
            ):
                primeira_turma = presenca.atividade.turmas.first()
                presenca.turma = primeira_turma
                presenca.save()
                corrigidas_turma += 1
                print(
                    f"  ✓ Presença ID {presenca.id} - turma definida: {primeira_turma.nome}"
                )

        print(f"📊 {corrigidas_turma} registros de presença tiveram turmas corrigidas")

    # 2. Verificar registros de presença sem relacionamentos consistentes
    with transaction.atomic():
        print(
            "\n📋 Verificando registros de presença com relacionamentos inconsistentes..."
        )
        presencas_academicas = RegistroPresenca.objects.select_related(
            "aluno", "atividade", "turma"
        ).all()

        corrigidas_academicas = 0
        for presenca in presencas_academicas:
            mudou = False

            # Se tem atividade mas não tem turma, usar turma da atividade
            if presenca.atividade and not presenca.turma:
                if (
                    hasattr(presenca.atividade, "turmas")
                    and presenca.atividade.turmas.exists()
                ):
                    presenca.turma = presenca.atividade.turmas.first()
                    mudou = True

            # Se tem turma mas não tem atividade, e aluno tem matrícula ativa
            if presenca.turma and not presenca.atividade:
                # Buscar atividade recente da turma na data da presença
                from atividades.models import Atividade

                atividade_proxima = Atividade.objects.filter(
                    turmas=presenca.turma, data_inicio=presenca.data
                ).first()

                if atividade_proxima:
                    presenca.atividade = atividade_proxima
                    mudou = True

            if mudou:
                presenca.save()
                corrigidas_academicas += 1
                print(
                    f"  ✓ PresencaAcademica ID {presenca.id} - relacionamentos corrigidos"
                )

        print(
            f"📊 {corrigidas_academicas} presenças acadêmicas tiveram relacionamentos corrigidos"
        )

    # 3. Verificar dados órfãos (sem aluno ou sem referência válida)
    print("\n📋 Verificando dados órfãos...")
    presencas_orfas = RegistroPresenca.objects.filter(aluno__isnull=True)
    if presencas_orfas.exists():
        print(f"⚠️  Encontrados {presencas_orfas.count()} registros órfãos (sem aluno)")
        print("   Recomenda-se revisão manual destes registros")

    # 4. Verificar inconsistências de datas
    print("\n📋 Verificando inconsistências de datas...")
    from datetime import date

    presencas_futuras = RegistroPresenca.objects.filter(data__gt=date.today())
    if presencas_futuras.exists():
        print(f"⚠️  Encontrados {presencas_futuras.count()} registros com datas futuras")
        print("   Verifique se estas datas estão corretas")

    # 5. Relatório final
    total_presencas = RegistroPresenca.objects.count()

    print("\n✅ Auto-correção concluída!")
    print("📊 Estatísticas finais:")
    print(f"   • Total de registros de presença: {total_presencas}")
    print(f"   • Registros corrigidos (turmas): {corrigidas_turma}")
    print(f"   • Registros corrigidos (relacionamentos): {corrigidas_academicas}")

    print("\n🎯 Módulo Presenças (RegistroPresenca) otimizado com sucesso!")
