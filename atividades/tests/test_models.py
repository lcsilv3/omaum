from django.test import TestCase
from atividades.models import AtividadeAcademica

class AtividadeAcademicaModelTest(TestCase):
    def test_criar_atividade(self):
        atividade = AtividadeAcademica.objects.create(
            codigo_atividade='ATV001',
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.'
        )
        
        self.assertEqual(atividade.codigo_atividade, 'ATV001')
        self.assertEqual(atividade.nome, 'Aula de Matemática')
        self.assertEqual(atividade.descricao, 'Aula introdutória sobre álgebra.')
