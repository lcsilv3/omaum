# Código da Funcionalidade: presencas - Parte 2/2
*Gerado automaticamente*



## presencas\templates\presencas\listar_presencas.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Lista de Presenças</h1>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="aluno" class="form-label">Aluno</label>
                    <select name="aluno" id="aluno" class="form-select">
                        <option value="">Todos</option>
                        {% for aluno in alunos %}
                            <option value="{{ aluno.id }}" {% if aluno_id == aluno.id|stringformat:"s" %}selected{% endif %}>{{ aluno.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select name="turma" id="turma" class="form-select">
                        <option value="">Todas</option>
                        {% for turma in turmas %}
                            <option value="{{ turma.id }}" {% if turma_id == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.codigo_turma }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ data_fim }}">
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                    <a href="{% url 'lista_presencas' %}" class="btn btn-secondary">Limpar Filtros</a>
                </div>
            </form>
        </div>
    </div>
    
    <table class="table">
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Turma</th>
                <th>Data</th>
                <th>Presente</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for presenca in presencas %}
            <tr>
                <td>{{ presenca.aluno.nome }}</td>
                <td>{{ presenca.turma.nome }}</td>
                <td>{{ presenca.data|date:"d/m/Y" }}</td>
                <td>{% if presenca.presente %}Sim{% else %}Não{% endif %}</td>
                <td>
                    <a href="{% url 'presencas:editar_presenca' presenca.id %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'presencas:excluir_presenca' presenca.id %}" class="btn btn-sm btn-danger">Excluir</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5">Nenhuma presença registrada.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <!-- Paginação -->
    {% if presencas.paginator.num_pages > 1 %}
    <nav aria-label="Navegação de página">
        <ul class="pagination justify-content-center">
            {% if presencas.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Primeira">
                        <span aria-hidden="true">««</span>
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ presencas.previous_page_number }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Anterior">
                        <span aria-hidden="true">«</span>
                    </a>
                </li>
            {% else %}
                <li class="page-item disabled">
                    <a class="page-link" href="#" aria-label="Primeira">
                        <span aria-hidden="true">««</span>
                    </a>
                </li>
                <li class="page-item disabled">
                    <a class="page-link" href="#" aria-label="Anterior">
                        <span aria-hidden="true">«</span>
                    </a>
                </li>
            {% endif %}
            
            {% for i in presencas.paginator.page_range %}
                {% if presencas.number == i %}
                    <li class="page-item active"><a class="page-link" href="#">{{ i }}</a></li>
                {% elif i > presencas.number|add:'-3' and i < presencas.number|add:'3' %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ i }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}">{{ i }}</a>
                    </li>
                {% endif %}
            {% endfor %}
            
            {% if presencas.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ presencas.next_page_number }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Próxima">
                        <span aria-hidden="true">»</span>
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ presencas.paginator.num_pages }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Última">
                        <span aria-hidden="true">»»</span>
                    </a>
                </li>
            {% else %}
                <li class="page-item disabled">
                    <a class="page-link" href="#" aria-label="Próxima">
                        <span aria-hidden="true">»</span>
                    </a>
                </li>
                <li class="page-item disabled">
                    <a class="page-link" href="#" aria-label="Última">
                        <span aria-hidden="true">»»</span>
                    </a>
                </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
    
    <a href="{% url 'registrar_presenca' %}" class="btn btn-primary">Nova Presença</a>
</div>
{% endblock %}





## presencas\templates\presencas\registrar_presenca.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Registrar Presença</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Registrar</button>
    </form>
    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary mt-2">Voltar</a>
</div>
{% endblock %}





## presencas\tests\test_forms.py

python
from django.test import TestCase
from presencas.forms import PresencaForm
from alunos.models import Aluno
from turmas.models import Turma
from datetime import date, time, timedelta

class PresencaFormTest(TestCase):
    def setUp(self):
        self.turma = Turma.objects.create(codigo_turma='TURMA001')
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def test_form_valido(self):
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today(),
            'presente': True
        }
        form = PresencaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_data_futura(self):
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today() + timedelta(days=1),
            'presente': True
        }
        form = PresencaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('data', form.errors)

    def test_form_duplicado(self):
        # Criar uma presença inicial
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today(),
            'presente': True
        }
        form = PresencaForm(data=data)
        form.is_valid()





## presencas\tests\test_models.py

python
from django.test import TestCase
from presencas.models import PresencaAcademica
from turmas.models import Turma
from alunos.models import Aluno
from datetime import date, time

class PresencaAcademicaModelTest(TestCase):
    def setUp(self):
        self.turma = Turma.objects.create(codigo_turma='TURMA001')
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def test_criar_presenca(self):
        presenca = PresencaAcademica.objects.create(
            turma=self.turma,
            aluno=self.aluno,
            data=date(2023, 10, 1),
            presente=True
        )
        self.assertEqual(presenca.presente, True)
        self.assertEqual(presenca.aluno, self.aluno)





## presencas\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from presencas.models import PresencaAcademica
from turmas.models import Turma
from alunos.models import Aluno
from datetime import date, time

class PresencaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.turma = Turma.objects.create(codigo_turma='TURMA001')
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        self.presenca = PresencaAcademica.objects.create(
            turma=self.turma,
            aluno=self.aluno,
            data=date(2023, 10, 1),
            presente=True
        )

    def test_listar_presencas(self):
        response = self.client.get(reverse('lista_presencas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Silva')



