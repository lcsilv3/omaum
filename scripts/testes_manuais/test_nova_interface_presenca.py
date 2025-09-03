"""
Teste da nova interface de confirmação de presenças por atividade individual.
Este script testa a lógica de processamento dos dados enviados pelo novo formulário.
"""


def test_form_data_processing():
    """Simula o processamento dos dados do novo formulário."""

    # Dados simulados que viriam do request.POST
    mock_post_data = {
        # Atividade 0 - aluno 12345678901 presente
        "atividade_0_aluno_12345678901": "presente",
        # Atividade 0 - aluno 98765432100 ausente com justificativa
        "atividade_0_justificativa_98765432100": "Consulta médica",
        # Atividade 1 - aluno 12345678901 ausente com justificativa
        "atividade_1_justificativa_12345678901": "Viagem a trabalho",
        # Atividade 1 - aluno 98765432100 presente
        "atividade_1_aluno_98765432100": "presente",
    }

    # Simular processamento das atividades
    atividades_processadas = [
        (0, {"id": 101, "nome": "Palestra sobre Iniciação"}, range(1, 3)),  # 2 dias
        (1, {"id": 102, "nome": "Exercícios Práticos"}, range(1, 4)),  # 3 dias
    ]

    # Alunos da turma
    alunos_ids = ["12345678901", "98765432100"]

    print("=== Teste de Processamento dos Dados ===\n")

    # Processar cada atividade
    for atividade_index, atividade, dias in atividades_processadas:
        print(
            f"ATIVIDADE {atividade_index}: {atividade['nome']} (ID: {atividade['id']})"
        )
        print(f"Dias: {list(dias)}")
        print()

        for aluno_cpf in alunos_ids:
            # Verificar presença
            campo_presenca = f"atividade_{atividade_index}_aluno_{aluno_cpf}"
            presente = campo_presenca in mock_post_data

            # Verificar justificativa
            justificativa = ""
            if not presente:
                campo_justificativa = (
                    f"atividade_{atividade_index}_justificativa_{aluno_cpf}"
                )
                justificativa = mock_post_data.get(campo_justificativa, "").strip()

            print(f"  Aluno {aluno_cpf}:")
            print(f"    Campo presença: {campo_presenca}")
            print(f"    Presente: {'SIM' if presente else 'NÃO'}")
            if not presente and justificativa:
                print(f"    Justificativa: {justificativa}")

            # Simular criação dos registros
            print("    Registros a criar:")
            for dia in dias:
                data_simulada = f"2024-01-{dia:02d}"
                print(
                    f"      - Data: {data_simulada}, Presente: {presente}, Justificativa: '{justificativa}'"
                )
            print()

        print("-" * 50)
        print()

    print("=== Teste Concluído ===")


if __name__ == "__main__":
    test_form_data_processing()
