# Código da Funcionalidade: cargos - Parte 3/3
*Gerado automaticamente*



## cargos\templates\cargos\listar_cargos.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Cargos</h1>
  
  <div class="d-flex justify-content-between mb-3">
    <a href="{% url 'cargos:criar_cargo' %}" class="btn btn-primary">Novo Cargo</a>
    <a href="{% url 'cargos:atribuir_cargo' %}" class="btn btn-success">Atribuir Cargo</a>
  </div>
  
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Nome</th>
        <th>Descrição</th>
        <th>Nível</th>
        <th>Ações</th>
      </tr>
    </thead>
    <tbody>
      {% for cargo in cargos %}
      <tr>
        <td>{{ cargo.nome }}</td>
        <td>{{ cargo.descricao|truncatechars:50 }}</td>
        <td>{{ cargo.get_nivel_display }}</td>
        <td>
          <a href="{% url 'cargos:detalhar_cargo' cargo.id %}" class="btn btn-sm btn-info">Detalhes</a>
          <a href="{% url 'cargos:editar_cargo' cargo.id %}" class="btn btn-sm btn-warning">Editar</a>
          <a href="{% url 'cargos:excluir_cargo' cargo.id %}" class="btn btn-sm btn-danger">Excluir</a>
        </td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="4">Nenhum cargo cadastrado.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  
  <h2 class="mt-5">Atribuições de Cargos</h2>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Aluno</th>
        <th>Cargo</th>
        <th>Data de Início</th>
        <th>Data de Término</th>
        <th>Ações</th>
      </tr>
    </thead>
    <tbody>
      {% for atribuicao in atribuicoes %}
      <tr>
        <td>{{ atribuicao.aluno.nome }}</td>
        <td>{{ atribuicao.cargo.nome }}</td>
        <td>{{ atribuicao.data_inicio|date:"d/m/Y" }}</td>
        <td>{{ atribuicao.data_fim|date:"d/m/Y"|default:"Atual" }}</td>
        <td>
          <a href="{% url 'cargos:remover_atribuicao_cargo' atribuicao.id %}" class="btn btn-sm btn-danger">Remover</a>
        </td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="5">Nenhuma atribuição de cargo cadastrada.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}




## cargos\templates\cargos\remover_atribuicao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Remover Atribuição de Cargo</h1>
  
  <div class="alert alert-danger">
    <p>Tem certeza que deseja remover a atribuição do cargo "{{ atribuicao.cargo.nome }}" para o aluno "{{ atribuicao.aluno.nome }}"?</p>
  </div>
  
  <form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Sim, remover</button>
    <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}





## cargos\tests\test_models.py

python
from django.test import TestCase
from cargos.models import CargoAdministrativo

class CargoAdministrativoTest(TestCase):
    def test_criar_cargo(self):
        cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )
        self.assertEqual(cargo.nome, 'Coordenador')
        self.assertEqual(cargo.codigo_cargo, 'CARGO001')





## cargos\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from cargos.models import CargoAdministrativo

class CargoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )

    def test_listar_cargos(self):
        response = self.client.get(reverse('cargos:listar_cargos_administrativos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Coordenador')

    def test_detalhe_cargo(self):
        response = self.client.get(reverse('cargos:detalhe_cargo', args=[self.cargo.codigo_cargo]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Coordenador')
        
    def test_criar_cargo(self):
        response = self.client.post(
            reverse('cargos:criar_cargo'),
            {
                'codigo_cargo': 'CARGO002',
                'nome': 'diretor',
                'descricao': 'Responsável pela direção do departamento.'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verifica se o cargo foi criado e se o nome foi capitalizado corretamente
        cargo = CargoAdministrativo.objects.get(codigo_cargo='CARGO002')
        self.assertEqual(cargo.nome, 'Diretor')

    def test_editar_cargo(self):
        response = self.client.post(
            reverse('cargos:editar_cargo', args=[self.cargo.codigo_cargo]),
            {
                'codigo_cargo': 'CARGO001',
                'nome': 'coordenador sênior',
                'descricao': 'Coordenador com experiência avançada.'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verifica se o cargo foi atualizado
        cargo = CargoAdministrativo.objects.get(codigo_cargo='CARGO001')
        self.assertEqual(cargo.nome, 'Coordenador Sênior')
        self.assertEqual(cargo.descricao, 'Coordenador com experiência avançada.')

    def test_excluir_cargo(self):
        response = self.client.post(
            reverse('cargos:excluir_cargo', args=[self.cargo.codigo_cargo])
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verifica se o cargo foi excluído
        with self.assertRaises(CargoAdministrativo.DoesNotExist):
            CargoAdministrativo.objects.get(codigo_cargo='CARGO001')



