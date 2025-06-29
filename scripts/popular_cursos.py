from django.core.management.base import BaseCommand
from cursos.models import Curso


class Command(BaseCommand):
    help = "Popula o banco de dados com cursos iniciais"

    def handle(self, *args, **kwargs):
        cursos_dados = [
            {
                "nome": "Introdução à Meditação",
                "descricao": (
                    "Curso básico para iniciantes em meditação"
                ),
            },
            {
                "nome": "Meditação Avançada",
                "descricao": (
                    "Técnicas avançadas de meditação para praticantes "
                    "experientes"
                ),
            },
            {
                "nome": "Yoga para Iniciantes",
                "descricao": (
                    "Fundamentos de yoga para quem está começando"
                ),
            },
            {
                "nome": "Filosofia Oriental",
                "descricao": (
                    "Estudo dos princípios filosóficos orientais"
                ),
            },
            {
                "nome": "Práticas de Mindfulness",
                "descricao": (
                    "Técnicas de atenção plena para o dia a dia"
                ),
            },
        ]

        for curso_dados in cursos_dados:
            curso, criado = Curso.objects.get_or_create(
                nome=curso_dados["nome"],
                defaults={
                    "descricao": curso_dados["descricao"],
                },
            )

            if criado:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Curso "{curso.nome}" criado com sucesso!'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Curso "{curso.nome}" já existe.')
                )
