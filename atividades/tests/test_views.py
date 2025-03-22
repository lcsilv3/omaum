from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import AtividadeAcademica, Atividade

class AtividadeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.atividade = AtividadeAcademica.objects.create(
            codigo_atividade='ATV001',
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.'
        )

    def test_listar_atividades(self):
        response = self.client.get(reverse('listar_atividades_academicas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aula de Matemática')
        self.assertContains(response, 'ATV001')

    def test_detalhe_atividade(self):
        response = self.client.get(reverse('detalhe_atividade', args=[self.atividade.codigo_atividade]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.atividade.nome)
        self.assertContains(response, self.atividade.descricao)

class RitualisticaExcluirView(DeleteView):
    model = AtividadeRitualistica
    template_name = 'atividades/ritualistica_confirmar_exclusao.html'  # Change this line
    success_url = reverse_lazy('atividades:ritualistica_lista')
