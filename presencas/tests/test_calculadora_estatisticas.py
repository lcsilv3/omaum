"""Testes para o serviço CalculadoraEstatisticas."""

from django.test import TestCase
from presencas.services.calculadora_estatisticas import CalculadoraEstatisticas


class CalculadoraEstatisticasTest(TestCase):
    """Testes básicos para a calculadora de estatísticas."""

    def test_calcular_totais_vazio(self):
        """Verifica que a calculadora retorna resultado válido para lista vazia."""
        resultado = CalculadoraEstatisticas.calcular_totais_consolidado([])
        self.assertIsNotNone(resultado)
        # TODO: Expandir com cenários específicos conforme evolução da implementação
