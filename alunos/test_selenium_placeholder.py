from django.test import TestCase


class SeleniumTestCase(TestCase):
    """Placeholder para cenários Selenium ainda não suportados."""

    def setUp(self):
        self.skipTest("Ignorando temporariamente os testes Selenium.")
