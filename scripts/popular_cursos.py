from django.core.management.base import BaseCommand
from cursos.models import Curso


class Command(BaseCommand):
    help = "Popula o banco de dados com cursos iniciais"

    def handle(self, *args, **kwargs):
        cursos_dados = [
            {
                "codigo_curso": 101,
                "nome": "Introdução à Meditação",
                "descricao": "Curso básico para iniciantes em meditação",
                "duracao": 3,
            },
            {
                "codigo_curso": 102,
                "nome": "Meditação Avançada",
                "descricao": "Técnicas avançadas de meditação para praticantes experientes",
                "duracao": 6,
            },
            {
                "codigo_curso": 103,
                "nome": "Yoga para Iniciantes",
                "descricao": "Fundamentos de yoga para quem está começando",
                "duracao": 4,
            },
            {
                "codigo_curso": 104,
                "nome": "Filosofia Oriental",
                "descricao": "Estudo dos princípios filosóficos orientais",
                "duracao": 8,
            },
            {
                "codigo_curso": 105,
                "nome": "Práticas de Mindfulness",
                "descricao": "Técnicas de atenção plena para o dia a dia",
                "duracao": 5,
            },
        ]

        for curso_dados in cursos_dados:
            curso, criado = Curso.objects.get_or_create(
                codigo_curso=curso_dados["codigo_curso"],
                defaults={
                    "nome": curso_dados["nome"],
                    "descricao": curso_dados["descricao"],
                    "duracao": curso_dados["duracao"],
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
