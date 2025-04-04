# Código da Funcionalidade: turmas - Parte 2/3
*Gerado automaticamente*



## turmas\templates\turmas\criar_turma.html

html
{% extends 'base.html' %}

{% block title %}Criar Nova Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Criar Nova Turma</h1>

    <form method="post">
        {% csrf_token %}

        {% for field in form %}
            <div class="form-group">
                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
                {% if field.help_text %}
                    <small class="form-text text-muted">{{ field.help_text }}</small>
                {% endif %}
                {% for error in field.errors %}
                    <div class="alert alert-danger">{{ error }}</div>
                {% endfor %}
            </div>
        {% endfor %}

        <button type="submit" class="btn btn-primary">Salvar</button>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}






## turmas\templates\turmas\detalhar_turma.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Detalhes da Turma: {{ turma.nome }}</h1>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <div class="card mb-4">
        <div class="card-body">
            <h5 class="card-title">Informações da Turma</h5>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Data de Início:</strong> {{ turma.data_inicio|date:"d/m/Y" }}</p>
            <p><strong>Data de Fim:</strong> {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Status:</strong> {{ turma.get_status_display }}</p>
            <p><strong>Capacidade:</strong> {{ turma.capacidade }}</p>
            <p><strong>Alunos Matriculados:</strong> {{ total_matriculas }}</p>
            <p><strong>Vagas Disponíveis:</strong> {{ vagas_disponiveis }}</p>
            <p><strong>Descrição:</strong> {{ turma.descricao|default:"Não informada" }}</p>
        </div>
    </div>

    <h2>Alunos Matriculados</h2>
    <div class="table-responsive">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Matrícula</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for matricula in matriculas %}
                <tr>
                    <td>{{ matricula.aluno.nome }}</td>
                    <td>{{ matricula.aluno.matricula }}</td>
                    <td>
                        <a href="{% url 'turmas:cancelar_matricula' turma.id matricula.aluno.id %}" class="btn btn-sm btn-danger">Cancelar Matrícula</a>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="3" class="text-center">Nenhum aluno matriculado nesta turma.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="mt-4">
        <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary">Matricular Novo Aluno</a>
        <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-warning">Editar Turma</a>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Voltar para Lista de Turmas</a>
    </div>
</div>
{% endblock %}






## turmas\templates\turmas\detalhes_turma.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}





## turmas\templates\turmas\editar_turma.html

html
{% extends 'base.html' %}

{% block title %}Editar Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Turma: {{ turma.nome }}</h1>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <form method="post">
        {% csrf_token %}

        {% for field in form %}
            <div class="form-group">
                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
                {% if field.help_text %}
                    <small class="form-text text-muted">{{ field.help_text }}</small>
                {% endif %}
                {% for error in field.errors %}
                    <div class="alert alert-danger">{{ error }}</div>
                {% endfor %}
            </div>
        {% endfor %}

        <div class="mt-4">
            <button type="submit" class="btn btn-primary">Salvar Alterações</button>
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}






## turmas\templates\turmas\excluir_turma.html

html
{% extends 'base.html' %}

{% block title %}Excluir Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Turma: {{ turma.nome }}</h1>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <div class="alert alert-danger">
        <p>Você tem certeza que deseja excluir esta turma?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>

    <form method="post">
        {% csrf_token %}
        <div class="mt-4">
            <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}






## turmas\templates\turmas\listar_alunos_matriculados.html

html
{% extends 'core/base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>{{ titulo }}</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome da Turma:</strong> {{ turma.nome }}</p>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Período:</strong> {{ turma.data_inicio|date:"d/m/Y" }} a {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Total de Alunos:</strong> {{ turma.total_alunos }} de {{ turma.vagas }}</p>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Alunos Matriculados</h5>
            <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary btn-sm">
                <i class="fas fa-plus"></i> Matricular Aluno
            </a>
        </div>
        <div class="card-body">
            {% if alunos %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Nome</th>
                                <th>Matrícula</th>
                                <th>Curso</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for aluno in alunos %}
                                <tr>
                                    <td>{{ aluno.nome }}</td>
                                    <td>{{ aluno.matricula }}</td>
                                    <td>{{ aluno.curso.nome }}</td>
                                    <td>
                                        <a href="{% url 'alunos:detalhar_aluno' aluno.id %}" class="btn btn-info btn-sm">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        <a href="{% url 'turmas:cancelar_matricula' turma.id aluno.id %}" class="btn btn-danger btn-sm">
                                            <i class="fas fa-times"></i> Cancelar Matrícula
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p>Nenhum aluno matriculado nesta turma.</p>
            {% endif %}
        </div>
    </div>
    
    <a href="{% url 'turmas:detalhes_turma' turma.id %}" class="btn btn-secondary mt-3">Voltar para Detalhes da Turma</a>
</div>
{% endblock %}





## turmas\templates\turmas\listar_turmas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Turmas{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Lista de Turmas</h1>

    <form method="get" class="mb-3">
        <div class="row">
            <div class="col-md-4">
                <input type="text" name="q" class="form-control" placeholder="Buscar turmas..." value="{{ query }}">
            </div>
            <div class="col-md-3">
                <select name="curso" class="form-control">
                    <option value="">Todos os cursos</option>
                    {% for curso in cursos %}
                        <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == curso_selecionado %}selected{% endif %}>
                            {{ curso.nome }}
                        </option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-3">
                <select name="status" class="form-control">
                    <option value="">Todos os status</option>
                    {% for status_value, status_label in opcoes_status %}
                        <option value="{{ status_value }}" {% if status_value == status_selecionado %}selected{% endif %}>
                            {{ status_label }}
                        </option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-2">
                <button type="submit" class="btn btn-primary">Filtrar</button>
            </div>
        </div>
    </form>

    <table class="table table-striped">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Curso</th>
                <th>Data de Início</th>
                <th>Data de Fim</th>
                <th>Status</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for turma in turmas %}
            <tr>
                <td>{{ turma.nome }}</td>
                <td>{{ turma.curso.nome }}</td>
                <td>{{ turma.data_inicio|date:"d/m/Y" }}</td>
                <td>{{ turma.data_fim|date:"d/m/Y" }}</td>
                <td>{{ turma.get_status_display }}</td>
                <td>
                    <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-sm btn-info">Detalhes</a>
                    <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-sm btn-danger">Excluir</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="6">Nenhuma turma encontrada.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    {% if turmas.has_other_pages %}
    <nav>
        <ul class="pagination">
            {% if turmas.has_previous %}
                <li class="page-item"><a class="page-link" href="?page={{ turmas.previous_page_number }}">Anterior</a></li>
            {% endif %}

            {% for i in turmas.paginator.page_range %}
                {% if turmas.number == i %}
                    <li class="page-item active"><span class="page-link">{{ i }}</span></li>
                {% else %}
                    <li class="page-item"><a class="page-link" href="?page={{ i }}">{{ i }}</a></li>
                {% endif %}
            {% endfor %}

            {% if turmas.has_next %}
                <li class="page-item"><a class="page-link" href="?page={{ turmas.next_page_number }}">Próxima</a></li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}

    <a href="{% url 'turmas:criar_turma' %}" class="btn btn-primary">Criar Nova Turma</a>
</div>
{% endblock %}






## turmas\templates\turmas\matricular_aluno.html

html
{% extends 'core/base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>{{ titulo }}</h1>
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome da Turma:</strong> {{ turma.nome }}</p>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Período:</strong> {{ turma.data_inicio|date:"d/m/Y" }} a {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Vagas Disponíveis:</strong> {{ turma.vagas_disponiveis }} de {{ turma.vagas }}</p>
        </div>
    </div>
    
    <div class="card mt-4">
        <div class="card-header">
            <h5 class="mb-0">Selecionar Aluno</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="{{ form.aluno.id_for_label }}" class="form-label">Aluno</label>
                    {{ form.aluno }}
                    {% if form.aluno.errors %}
                        <div class="text-danger">{{ form.aluno.errors }}</div>
                    {% endif %}
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'turmas:detalhes_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Matricular</button>
                </div>
            </form>
        </div>
    </div>
    
    <a href="javascript:history.back()" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}





## turmas\templates\turmas\turma_form.html

html
{% extends 'base.html' %}

{% block content %}
  <h1>Criar Turma</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Criar</button>
  </form>
{% endblock %}




## turmas\tests\test_models.py

python
from django.test import TestCase
from turmas.models import Turma
from cursos.models import Curso
from datetime import date

class TurmaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )

    def test_criar_turma(self):
        turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 10, 1),
            data_fim=date(2023, 12, 31)
        )

        self.assertEqual(turma.nome, 'Turma de Teste')
        self.assertEqual(turma.curso, self.curso)
        self.assertEqual(str(turma), 'Turma de Teste - Curso de Teste')

class CargoAdministrativoTest(TestCase):
    def test_criar_cargo(self):
        cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )
        self.assertEqual(cargo.nome, 'Coordenador')
        self.assertEqual(cargo.codigo_cargo, 'CARGO001')


