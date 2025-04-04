# Código da Funcionalidade: iniciacoes - Parte 2/3
*Gerado automaticamente*



## iniciacoes\templates\iniciacoes\detalhar_iniciacao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes da Iniciação</h1>
  
  <div class="card">
    <div class="card-header">
      <h2>Iniciação de {{ iniciacao.aluno.nome }}</h2>
    </div>
    <div class="card-body">
      <p><strong>Aluno:</strong> {{ iniciacao.aluno.nome }}</p>
      <p><strong>Grau:</strong> {{ iniciacao.grau.nome }}</p>
      <p><strong>Data:</strong> {{ iniciacao.data|date:"d/m/Y" }}</p>
      <p><strong>Local:</strong> {{ iniciacao.local }}</p>
      <p>
        <strong>Status:</strong> 
        {% if iniciacao.concluida %}
          <span class="badge bg-success">Concluída</span>
        {% else %}
          <span class="badge bg-warning">Pendente</span>
        {% endif %}
      </p>
      {% if iniciacao.observacoes %}
        <p><strong>Observações:</strong> {{ iniciacao.observacoes }}</p>
      {% endif %}
      <p><strong>Registrado por:</strong> {{ iniciacao.registrado_por.username }}</p>
      <p><strong>Data de registro:</strong> {{ iniciacao.data_registro|date:"d/m/Y H:i" }}</p>
      {% if iniciacao.atualizado_por %}
        <p><strong>Atualizado por:</strong> {{ iniciacao.atualizado_por.username }}</p>
        <p><strong>Data de atualização:</strong> {{ iniciacao.data_atualizacao|date:"d/m/Y H:i" }}</p>
      {% endif %}
    </div>
    <div class="card-footer">
      <a href="{% url 'iniciacoes:editar_iniciacao' iniciacao.id %}" class="btn btn-warning">Editar</a>
      <a href="{% url 'iniciacoes:excluir_iniciacao' iniciacao.id %}" class="btn btn-danger">Excluir</a>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Voltar</a>
    </div>
  </div>
</div>
{% endblock %}





## iniciacoes\templates\iniciacoes\editar_grau.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Editar Grau de Iniciação</h1>
  
  <form method="post">
    {% csrf_token %}
    {% include 'includes/form_errors.html' %}
    
    {% for field in form %}
      {% include 'includes/form_field.html' %}
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Atualizar Grau</button>
    <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}





## iniciacoes\templates\iniciacoes\editar_iniciacao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Iniciação</h1>
  
    <form method="post">
      {% csrf_token %}
      {% include 'includes/form_errors.html' %}
    
      {% for field in form %}
        {% include 'includes/form_field.html' %}
      {% endfor %}
    
      <button type="submit" class="btn btn-primary">Atualizar Iniciação</button>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




## iniciacoes\templates\iniciacoes\excluir_grau.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Excluir Grau de Iniciação</h1>
  
  <div class="alert alert-danger">
    <p>Tem certeza que deseja excluir o grau <strong>{{ grau.nome }}</strong>?</p>
    {% if iniciacoes_associadas %}
      <div class="mt-3">
        <p><strong>Atenção:</strong> Existem {{ iniciacoes_associadas }} iniciações associadas a este grau. A exclusão deste grau pode afetar esses registros.</p>
      </div>
    {% endif %}
  </div>
  
  <form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Sim, excluir</button>
    <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}





## iniciacoes\templates\iniciacoes\excluir_iniciacao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Iniciação</h1>
  
    <div class="alert alert-danger">
      <p>Tem certeza que deseja excluir a iniciação de <strong>{{ iniciacao.aluno.nome }}</strong> no grau <strong>{{ iniciacao.grau.nome }}</strong> realizada em <strong>{{ iniciacao.data|date:"d/m/Y" }}</strong>?</p>
    </div>
  
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Sim, excluir</button>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




## iniciacoes\templates\iniciacoes\listar_graus.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Graus de Iniciação</h1>
  
  <div class="d-flex justify-content-between mb-3">
    <a href="{% url 'iniciacoes:criar_grau' %}" class="btn btn-primary">Novo Grau</a>
    <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Voltar para Iniciações</a>
  </div>
  
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Nome</th>
        <th>Número</th>
        <th>Descrição</th>
        <th>Requisitos</th>
        <th>Ações</th>
      </tr>
    </thead>
    <tbody>
      {% for grau in graus %}
      <tr>
        <td>{{ grau.nome }}</td>
        <td>{{ grau.numero }}</td>
        <td>{{ grau.descricao|truncatechars:50 }}</td>
        <td>{{ grau.requisitos|truncatechars:50 }}</td>
        <td>
          <a href="{% url 'iniciacoes:editar_grau' grau.id %}" class="btn btn-sm btn-warning">Editar</a>
          <a href="{% url 'iniciacoes:excluir_grau' grau.id %}" class="btn btn-sm btn-danger">Excluir</a>
        </td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="5">Nenhum grau cadastrado.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}





## iniciacoes\templates\iniciacoes\listar_iniciacoes.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Iniciações</h1>
  
    <div class="d-flex justify-content-between mb-3">
      <a href="{% url 'iniciacoes:criar_iniciacao' %}" class="btn btn-primary">Nova Iniciação</a>
      <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-info">Gerenciar Graus</a>
    </div>
  
    <div class="card mb-4">
      <div class="card-header">
        <h5>Filtros</h5>
      </div>
      <div class="card-body">
        <form method="get" class="row g-3">
          <div class="col-md-4">
            <label for="aluno" class="form-label">Aluno</label>
            <select name="aluno" id="aluno" class="form-select">
              <option value="">Todos</option>
              {% for aluno in alunos %}
                <option value="{{ aluno.id }}" {% if request.GET.aluno == aluno.id|stringformat:"i" %}selected{% endif %}>
                  {{ aluno.nome }}
                </option>
              {% endfor %}
            </select>
          </div>
          <div class="col-md-4">
            <label for="grau" class="form-label">Grau</label>
            <select name="grau" id="grau" class="form-select">
              <option value="">Todos</option>
              {% for grau in graus %}
                <option value="{{ grau.id }}" {% if request.GET.grau == grau.id|stringformat:"i" %}selected{% endif %}>
                  {{ grau.nome }}
                </option>
              {% endfor %}
            </select>
          </div>
          <div class="col-md-4">
            <label for="data" class="form-label">Data</label>
            <input type="date" name="data" id="data" class="form-control" value="{{ request.GET.data }}">
          </div>
          <div class="col-12 mt-3">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Limpar Filtros</a>
          </div>
        </form>
      </div>
    </div>
  
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Aluno</th>
          <th>Grau</th>
          <th>Data</th>
          <th>Local</th>
          <th>Status</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {% for iniciacao in iniciacoes %}
        <tr>
          <td>{{ iniciacao.aluno.nome }}</td>
          <td>{{ iniciacao.grau.nome }}</td>
          <td>{{ iniciacao.data|date:"d/m/Y" }}</td>
          <td>{{ iniciacao.local }}</td>
          <td>
            {% if iniciacao.concluida %}
              <span class="badge bg-success">Concluída</span>
            {% else %}
              <span class="badge bg-warning">Pendente</span>
            {% endif %}
          </td>
          <td>
            <a href="{% url 'iniciacoes:detalhar_iniciacao' iniciacao.id %}" class="btn btn-sm btn-info">Detalhes</a>
            <a href="{% url 'iniciacoes:editar_iniciacao' iniciacao.id %}" class="btn btn-sm btn-warning">Editar</a>
            <a href="{% url 'iniciacoes:excluir_iniciacao' iniciacao.id %}" class="btn btn-sm btn-danger">Excluir</a>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="6">Nenhuma iniciação encontrada.</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  
    {% if iniciacoes.has_other_pages %}
    <nav aria-label="Paginação">
      <ul class="pagination justify-content-center">
        {% if iniciacoes.has_previous %}
          <li class="page-item">
            <a class="page-link" href="?page=1{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Primeira">
              <span aria-hidden="true">««</span>
            </a>
          </li>
          <li class="page-item">
            <a class="page-link" href="?page={{ iniciacoes.previous_page_number }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Anterior">
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
      
        {% for i in iniciacoes.paginator.page_range %}
          {% if iniciacoes.number == i %}
            <li class="page-item active"><a class="page-link" href="#">{{ i }}</a></li>
          {% elif i > iniciacoes.number|add:'-3' and i < iniciacoes.number|add:'3' %}
            <li class="page-item">
              <a class="page-link" href="?page={{ i }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}">{{ i }}</a>
            </li>
          {% endif %}
        {% endfor %}
      
        {% if iniciacoes.has_next %}
          <li class="page-item">
            <a class="page-link" href="?page={{ iniciacoes.next_page_number }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Próxima">
              <span aria-hidden="true">»</span>
            </a>
          </li>
          <li class="page-item">
            <a class="page-link" href="?page={{ iniciacoes.paginator.num_pages }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Última">
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
</div>
{% endblock %}




## iniciacoes\tests\test_forms.py

python
from django.test import TestCase
from iniciacoes.forms import IniciacaoForm
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time

class IniciacaoFormTest(TestCase):
    def setUp(self):
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
        
        # Criar uma iniciação para testar a validação de duplicidade
        self.iniciacao = Iniciacao.objects.create(
            aluno=self.aluno,
            nome_curso='Curso de Iniciação',
            data_iniciacao=date(2023, 10, 1)
        )
    
    def test_form_valido(self):
        # Testando um formulário com dados válidos
        form_data = {
            'aluno': self.aluno.id,
            'nome_curso': 'Curso de Meditação',  # Curso diferente
            'data_iniciacao': date(2023, 11, 1),
            'observacoes': 'Teste de observação'
        }
        form = IniciacaoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalido_curso_duplicado(self):
        # Testando um formulário com curso duplicado para o mesmo aluno
        form_data = {
            'aluno': self.aluno.id,
            'nome_curso': 'Curso de Iniciação',  # Mesmo curso que já existe
            'data_iniciacao': date(2023, 11, 1),
            'observacoes': 'Teste de observação'
        }
        form = IniciacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
    
    def test_form_campos_obrigatorios(self):
        # Testando um formulário sem campos obrigatórios
        form_data = {
            'observacoes': 'Apenas observações'
        }
        form = IniciacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('aluno', form.errors)
        self.assertIn('nome_curso', form.errors)
        self.assertIn('data_iniciacao', form.errors)





## iniciacoes\tests\test_models.py

python
from django.test import TestCase
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time

class IniciacaoModelTest(TestCase):
    def setUp(self):
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

    def test_criar_iniciacao(self):
        iniciacao = Iniciacao.objects.create(
            aluno=self.aluno,
            nome_curso='Curso de Iniciação',
            data_iniciacao=date(2023, 10, 1)
        )
        self.assertEqual(iniciacao.nome_curso, 'Curso de Iniciação')
        self.assertEqual(iniciacao.aluno, self.aluno)





## iniciacoes\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time

class IniciacaoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Criar um usuário de teste e fazer login
        self.usuario = User.objects.create_user(username='usuarioteste', password='12345')
        self.client.login(username='usuarioteste', password='12345')
        
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
        self.iniciacao = Iniciacao.objects.create(
            aluno=self.aluno,
            nome_curso='Curso de Iniciação',
            data_iniciacao=date(2023, 10, 1)
        )

    def test_listar_iniciacoes(self):
        response = self.client.get(reverse('iniciacoes:listar_iniciacoes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Silva')
        self.assertContains(response, 'Curso de Iniciação')



