#!/usr/bin/env python
"""
Exemplo de uso do CalculadoraEstatisticas.
Execute: python manage.py shell < exemplo_uso_calculadora.py
"""

import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from presencas.services.calculadora_estatisticas import CalculadoraEstatisticas
from presencas.models import PresencaDetalhada, ConfiguracaoPresenca
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade


def exemplo_uso():
    """Demonstra o uso do CalculadoraEstatisticas."""

    print("*** Demonstracao do CalculadoraEstatisticas Service ***")
    print("=" * 50)

    # 1. Verificar se existem dados
    total_presencas = PresencaDetalhada.objects.count()
    total_alunos = Aluno.objects.count()
    total_turmas = Turma.objects.count()
    total_atividades = Atividade.objects.count()

    print("[INFO] Dados disponíveis:")
    print(f"   - Presenças detalhadas: {total_presencas}")
    print(f"   - Alunos: {total_alunos}")
    print(f"   - Turmas: {total_turmas}")
    print(f"   - Atividades: {total_atividades}")
    print()

    if total_presencas == 0:
        print("[AVISO] Nenhuma presença detalhada encontrada.")
        print("   Para testar completamente, crie alguns dados primeiro.")
        return

    # 2. Testar métodos principais
    print("[TESTE] Testando métodos da CalculadoraEstatisticas:")
    print()

    # Consolidado por aluno
    if total_alunos > 0:
        aluno = Aluno.objects.first()
        print(f"[TESTE] Consolidado do aluno: {aluno.nome}")
        try:
            consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
                aluno_id=aluno.id
            )
            print(
                f"   [OK] Sucesso! Percentual: {consolidado['percentuais']['presenca']}%"
            )
            print(
                f"   [INFO] Total convocações: {consolidado['totais']['convocacoes']}"
            )
            print(f"   [INFO] Total presenças: {consolidado['totais']['presencas']}")
            print(f"   [INFO] Status: {consolidado['status']}")
        except Exception as e:
            print(f"   [ERRO] Erro: {e}")
        print()

    # Tabela consolidada
    if total_turmas > 0:
        turma = Turma.objects.first()
        print(f"[TESTE] Tabela consolidada da turma: {turma.nome}")
        try:
            tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(turma_id=turma.id)
            print(f"   [OK] Sucesso! Total de alunos: {tabela['total_alunos']}")
            print(
                f"   [INFO] Percentual médio: {tabela['estatisticas_gerais']['percentual_medio']}%"
            )
        except Exception as e:
            print(f"   [ERRO] Erro: {e}")
        print()

    # Estatísticas da turma
    if total_turmas > 0:
        print(f"[TESTE] Estatísticas da turma: {turma.nome}")
        try:
            estatisticas = CalculadoraEstatisticas.calcular_estatisticas_turma(
                turma_id=turma.id
            )
            print(
                f"   [OK] Sucesso! Alunos na turma: {estatisticas['totais']['alunos']}"
            )
            print(f"   [INFO] Atividades: {estatisticas['totais']['atividades']}")
            print(
                f"   [INFO] Presença média: {estatisticas['percentuais']['presenca_media']}%"
            )
        except Exception as e:
            print(f"   [ERRO] Erro: {e}")
        print()

    # Configurações de presença
    total_configs = ConfiguracaoPresenca.objects.count()
    print(f"[INFO] Configurações de presença: {total_configs}")

    if total_configs > 0:
        config = ConfiguracaoPresenca.objects.first()
        print(f"   [INFO] Configuração: {config.turma} - {config.atividade}")
        print("   [INFO] Limites de carência:")
        print(f"      0-25%: {config.limite_carencia_0_25}")
        print(f"      26-50%: {config.limite_carencia_26_50}")
        print(f"      51-75%: {config.limite_carencia_51_75}")
        print(f"      76-100%: {config.limite_carencia_76_100}")
    print()

    # Recálculo de carências
    if total_presencas > 0:
        print("[TESTE] Testando recálculo de carências...")
        try:
            if total_turmas > 0:
                resultado = CalculadoraEstatisticas.recalcular_todas_carencias(
                    turma_id=turma.id
                )
                print("   [OK] Recálculo concluído!")
                print(f"   [INFO] Total processadas: {resultado['total_presencas']}")
                print(f"   [INFO] Atualizadas: {resultado['presencas_atualizadas']}")
                print(f"   [INFO] Erros: {resultado['total_erros']}")
            else:
                resultado = CalculadoraEstatisticas.recalcular_todas_carencias()
                print("   [OK] Recálculo geral concluído!")
                print(f"   [INFO] Total processadas: {resultado['total_presencas']}")
        except Exception as e:
            print(f"   [ERRO] Erro no recálculo: {e}")
        print()

    print("[SUCESSO] Demonstração concluída!")
    print("[INFO] Para usar em produção:")
    print(
        "   1. Importe: from presencas.services.calculadora_estatisticas import CalculadoraEstatisticas"
    )
    print(
        "   2. Use os métodos estáticos: CalculadoraEstatisticas.calcular_consolidado_aluno(aluno_id)"
    )
    print("   3. Veja a documentação em: presencas/services/README.md")


if __name__ == "__main__":
    exemplo_uso()
