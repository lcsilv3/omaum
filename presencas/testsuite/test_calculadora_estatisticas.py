from django.test import TestCase
from presencas.services.calculadora_estatisticas import CalculadoraEstatisticas


class CalculadoraEstatisticasTest(TestCase):
    def test_calcular_totais_vazio(self):
        resultado = CalculadoraEstatisticas.calcular_totais_consolidado([])
        self.assertIsNotNone(resultado)
        # Adapte conforme a implementação real
        # self.assertEqual(resultado, esperado)
