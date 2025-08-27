from django.utils import timezone
from atividades.models import Atividade


class TestAtividadeModel:
    def test_criacao_atividade_valida(self, db):
        from cursos.models import Curso
        from turmas.models import Turma

        curso = Curso.objects.create(nome="Curso Teste")
        turma = Turma.objects.create(nome="Turma Teste", curso=curso, status="A")
        atividade = Atividade.objects.create(
            nome="Aula de Matemática",
            tipo_atividade="AULA",
            data_inicio=timezone.now().date(),
            hora_inicio=timezone.now().time(),
            status="PENDENTE",
        )
        atividade.turmas.add(turma)
        assert atividade.pk is not None
        assert atividade.nome == "Aula de Matemática"

    def test_nome_obrigatorio(self, db):
        atividade = Atividade(
            tipo_atividade="AULA",
            data_inicio=timezone.now().date(),
            hora_inicio=timezone.now().time(),
            status="PENDENTE",
        )
        try:
            atividade.full_clean()
            assert False, "Deveria falhar sem nome"
        except Exception as e:
            assert "nome" in str(e)

    def test_campos_obrigatorios(self, db):
        # Testa ausência de tipo_atividade
        atividade = Atividade(
            nome="Teste",
            data_inicio=timezone.now().date(),
            hora_inicio=timezone.now().time(),
            status="PENDENTE",
        )
        try:
            atividade.full_clean()
            assert False, "Deveria falhar sem tipo_atividade"
        except Exception as e:
            assert "tipo_atividade" in str(e)

        # Testa ausência de data_inicio
        atividade = Atividade(
            nome="Teste",
            tipo_atividade="AULA",
            hora_inicio=timezone.now().time(),
            status="PENDENTE",
        )
        try:
            atividade.full_clean()
            assert False, "Deveria falhar sem data_inicio"
        except Exception as e:
            assert "data_inicio" in str(e)

        # Testa ausência de hora_inicio
        atividade = Atividade(
            nome="Teste",
            tipo_atividade="AULA",
            data_inicio=timezone.now().date(),
            status="PENDENTE",
        )
        try:
            atividade.full_clean()
            assert False, "Deveria falhar sem hora_inicio"
        except Exception as e:
            assert "hora_inicio" in str(e)
