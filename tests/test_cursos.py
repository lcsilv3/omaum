import pytest
from django.test import TestCase
from cursos.models import Curso
from tests.factories import CursoFactory


@pytest.mark.django_db
class CursoModelTest(TestCase):
    def test_crud_basico(self):
        # Criação
        curso = Curso.objects.create(nome="Curso Teste", descricao="Desc", ativo=True)
        assert Curso.objects.filter(nome="Curso Teste").exists()

        # Leitura
        curso_lido = Curso.objects.get(nome="Curso Teste")
        assert curso_lido.descricao == "Desc"

        # Atualização
        curso_lido.nome = "Curso Atualizado"
        curso_lido.save()
        assert Curso.objects.filter(nome="Curso Atualizado").exists()

        # Exclusão lógica
        curso_lido.ativo = False
        curso_lido.save()
        assert not Curso.objects.get(id=curso_lido.id).ativo

    def test_str(self):
        curso = Curso.objects.create(nome="Curso Teste", descricao="Desc")
        assert str(curso) == "Curso Teste"


@pytest.mark.django_db
class CursoFactoryTest(TestCase):
    def test_factory_cria_curso_valido(self):
        curso = CursoFactory()
        assert isinstance(curso, Curso)
        assert Curso.objects.filter(id=curso.id).exists()
        assert len(cursos) == 100
