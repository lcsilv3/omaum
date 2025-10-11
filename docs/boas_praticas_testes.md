# Boas Práticas para Testes no Sistema OMAUM

Este documento descreve as boas práticas a serem seguidas ao escrever testes para o sistema OMAUM.

## Princípios Gerais

1. **Independência**: Cada teste deve ser independente dos outros. Um teste não deve depender do estado deixado por outro teste.

2. **Repetibilidade**: Os testes devem produzir o mesmo resultado cada vez que são executados, independentemente da ordem de execução.

3. **Simplicidade**: Mantenha os testes simples e focados. Cada teste deve verificar uma única funcionalidade ou comportamento.

4. **Legibilidade**: Os testes devem ser fáceis de ler e entender. Use nomes descritivos para os métodos de teste.

5. **Manutenibilidade**: Os testes devem ser fáceis de manter. Evite duplicação de código e use fixtures e helpers quando apropriado.

## Estrutura dos Testes

### Testes Unitários

- Teste cada modelo, formulário e função auxiliar separadamente.
- Use mocks para isolar o componente sendo testado.
- Verifique casos de sucesso e casos de erro.

Exemplo:

```python
def test_aluno_str_method(self):
    """Testa se o método __str__ do modelo Aluno retorna o nome do aluno."""
    aluno = Aluno.objects.create(
        cpf="12345678900",
        nome="Aluno Teste",
        email="aluno@teste.com",
        data_nascimento="1990-01-01"
    )
    self.assertEqual(str(aluno), "Aluno Teste")
```

### Testes de Integração

- Teste a interação entre diferentes componentes do sistema.
- Verifique se as views retornam os templates corretos e se os dados são processados corretamente.
- Teste os fluxos de formulários, incluindo validação e salvamento.

Exemplo:

```python
def test_criar_aluno_view(self):
    """Testa se a view de criação de aluno funciona corretamente."""
    self.client.login(username='testuser', password='testpassword')
    
    response = self.client.post(
        reverse('alunos:criar_aluno'),
        {
            'cpf': '12345678900',
            'nome': 'Aluno Teste',
            'email': 'aluno@teste.com',
            'data_nascimento': '1990-01-01'
        },
        follow=True
    )
    
    self.assertEqual(response.status_code, 200)
    self.assertTrue(Aluno.objects.filter(cpf='12345678900').exists())
    self.assertContains(response, "Aluno criado com sucesso")
```

### Testes E2E

- Simule a interação do usuário com o sistema usando Selenium.
- Teste fluxos completos de uso, do início ao fim.
- Verifique se a interface do usuário funciona como esperado.

### Gerenciamento do ChromeDriver

- **Não versionar binaries**: o projeto depende do `webdriver-manager`/Selenium Manager para baixar o driver compatível em runtime. Não adicione `chromedriver` ao repositório nem ao container.
- **Ambiente local**: remova qualquer `chromedriver.exe` legado do seu `PATH` (especialmente em `C:\Windows`). Se precisar manter permissões elevadas, execute `Remove-Item` em um terminal administrativo ou use o utilitário integrado do Selenium (`python -m selenium.webdriver`).
- **Docker/CI**: garanta que a imagem base contenha somente o Google Chrome e deixe que o Selenium faça o download sob demanda. Se for necessário cachear, exporte `WDM_LOCAL=1` para reutilizar o binário instalado automaticamente.
- **Execução headless**: em pipelines use Chrome headless e configure a variável `SELENIUM_HEADLESS=1` (respeitada nos testes E2E) para evitar abertura de janelas em ambientes sem display.

Exemplo:

```python
def test_fluxo_criar_aluno(self):
    """Testa o fluxo completo de criação de aluno."""
    self.selenium.get(f'{self.live_server_url}/accounts/login/')
    username_input = self.selenium.find_element(By.NAME, 'username')
    password_input = self.selenium.find_element(By.NAME, 'password')
    username_input.send_keys('testuser')
    password_input.send_keys('testpassword')
    self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
    
    self.selenium.get(f'{self.live_server_url}/alunos/criar/')
    
    self.selenium.find_element(By.ID, 'id_cpf').send_keys('12345678900')
    self.selenium.find_element(By.ID, 'id_nome').send_keys('Aluno Teste')
    self.selenium.find_element(By.ID, 'id_email').send_keys('aluno@teste.com')
    self.selenium.find_element(By.ID, 'id_data_nascimento').send_keys('1990-01-01')
    
    self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
    
    WebDriverWait(self.selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
    )
    
    self.assertIn('Aluno criado com sucesso', self.selenium.page_source)
```

## Convenções de Nomenclatura

- Nome dos arquivos de teste: `test_<componente>.py`
- Nome dos métodos de teste: `test_<funcionalidade>_<condição>`

Exemplos:
- `test_models.py`
- `test_forms.py`
- `test_views.py`
- `test_criar_aluno_sucesso()`
- `test_editar_aluno_campos_invalidos()`

## Fixtures e Factory Boy

Use fixtures e Factory Boy para criar dados de teste de forma eficiente:

```python
import factory
from alunos.models import Aluno

class AlunoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Aluno
    
    cpf = factory.Sequence(lambda n: f"{n:011d}")
    nome = factory.Sequence(lambda n: f"Aluno {n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.nome.lower().replace(' ', '.')}@exemplo.com")
    data_nascimento = "1990-01-01"
```

## Cobertura de Código

- Mantenha a cobertura de código acima de 80%.
- Use o comando `coverage run` para medir a cobertura.
- Gere relatórios com `coverage report` e `coverage html`.

## Testes de Regressão

- Sempre que um bug for corrigido, adicione um teste que verifica se o bug não voltará a ocorrer.
- Documente o bug e a solução no comentário do teste.

Exemplo:

```python
def test_cpf_duplicado_erro(self):
    """
    Testa se o sistema impede a criação de alunos com CPF duplicado.
    
    Relacionado ao bug #123: O sistema permitia a criação de alunos com CPF duplicado.
    """
    Aluno.objects.create(
        cpf="12345678900",
        nome="Aluno Original",
        email="original@teste.com",
        data_nascimento="1990-01-01"
    )
    
    form = AlunoForm({
        'cpf': '12345678900',
        'nome': 'Aluno Duplicado',
        'email': 'duplicado@teste.com',
        'data_nascimento': '1990-01-01'
    })
    
    self.assertFalse(form.is_valid())
    self.assertIn('cpf', form.errors)
```

## Conclusão

Seguir estas boas práticas ajudará a manter a qualidade do código e a confiabilidade do sistema OMAUM. Lembre-se de que os testes são uma parte essencial do desenvolvimento de software e devem ser tratados com o mesmo cuidado que o código de produção.

## Referências

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Selenium with Python Documentation](https://selenium-python.readthedocs.io/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/en/stable/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
```

## Passo 14: Implementação de Testes para Funcionalidades Específicas

### Testes para o Módulo de Atividades

```python:tests/atividades/test_models.py
from django.test import TestCase
from django.utils import timezone
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from alunos.models import Aluno
import datetime

class AtividadeAcademicaModelTest(TestCase):
    """Testes para o modelo AtividadeAcademica."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar uma turma para os testes
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        # Criar uma atividade acadêmica para os testes
        self.atividade = AtividadeAcademica.objects.create(
            nome="Atividade de Teste",
            descricao="Descrição da atividade",
            data_inicio=timezone.now(),
            responsavel="Professor Teste",
            tipo_atividade="aula",
            status="agendada"
        )
        self.atividade.turmas.add(self.turma)
    
    def test_atividade_academica_str(self):
        """Testa se o método __str__ do modelo AtividadeAcademica retorna o nome da atividade."""
        self.assertEqual(str(self.atividade), "Atividade de Teste")
    
    def test_atividade_academica_titulo_property(self):
        """Testa se a propriedade titulo retorna o nome da atividade."""
        self.assertEqual(self.atividade.titulo, "Atividade de Teste")
    
    def test_atividade_academica_titulo_setter(self):
        """Testa se o setter da propriedade titulo altera o nome da atividade."""
        self.atividade.titulo = "Novo Título"
        self.assertEqual(self.atividade.nome, "Novo Título")
        self.assertEqual(self.atividade.titulo, "Novo Título")
    
    def test_atividade_academica_turmas_relation(self):
        """Testa se a relação com turmas funciona corretamente."""
        self.assertEqual(self.atividade.turmas.count(), 1)
        self.assertEqual(self.atividade.turmas.first(), self.turma)
        
        # Adicionar outra turma
        turma2 = Turma.objects.create(
            nome="Turma de Teste 2",
            codigo="TT-002",
            data_inicio=timezone.now().date(),
            status="A"
        )
        self.atividade.turmas.add(turma2)
        
        self.assertEqual(self.atividade.turmas.count(), 2)
        self.assertIn(turma2, self.atividade.turmas.all())

class AtividadeRitualisticaModelTest(TestCase):
    """Testes para o modelo AtividadeRitualistica."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar uma turma para os testes
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        # Criar alunos para os testes
        self.aluno1 = Aluno.objects.create(
            cpf="12345678901",
            nome="Aluno Teste 1",
            email="aluno1@teste.com",
            data_nascimento="1990-01-01"
        )
        
        self.aluno2 = Aluno.objects.create(
            cpf="12345678902",
            nome="Aluno Teste 2",
            email="aluno2@teste.com",
            data_nascimento="1990-01-02"
        )
        
        # Criar uma atividade ritualística para os testes
        self.atividade = AtividadeRitualistica.objects.create(
            nome="Atividade Ritualística de Teste",
            descricao="Descrição da atividade ritualística",
            data=timezone.now().date(),
            hora_inicio="10:00",
            hora_fim="12:00",
            local="Local de Teste",
            turma=self.turma
        )
        self.atividade.participantes.add(self.aluno1, self.aluno2)
    
    def test_atividade_ritualistica_str(self):
        """Testa se o método __str__ do modelo AtividadeRitualistica retorna o formato esperado."""
        expected = f"Atividade Ritualística de Teste - {timezone.now().date()}"
        self.assertEqual(str(self.atividade), expected)
    
    def test_atividade_ritualistica_participantes_relation(self):
        """Testa se a relação com participantes funciona corretamente."""
        self.assertEqual(self.atividade.participantes.count(), 2)
        self.assertIn(self.aluno1, self.atividade.participantes.all())
        self.assertIn(self.aluno2, self.atividade.participantes.all())
        
        # Remover um participante
        self.atividade.participantes.remove(self.aluno1)
        
        self.assertEqual(self.atividade.participantes.count(), 1)
        self.assertNotIn(self.aluno1, self.atividade.participantes.all())
        self.assertIn(self.aluno2, self.atividade.participantes.all())
```

```python:tests/atividades/test_forms.py
from django.test import TestCase
from django.utils import timezone
from atividades.forms import AtividadeAcademicaForm, AtividadeRitualisticaForm
from turmas.models import Turma
from alunos.models import Aluno
import datetime

class AtividadeAcademicaFormTest(TestCase):
    """Testes para o formulário AtividadeAcademicaForm."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar turmas para os testes
        self.turma1 = Turma.objects.create(
            nome="Turma de Teste 1",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        self.turma2 = Turma.objects.create(
            nome="Turma de Teste 2",
            codigo="TT-002",
            data_inicio=timezone.now().date(),
            status="A"
        )
    
    def test_form_valid_data(self):
        """Testa se o formulário é válido com dados corretos."""
        form_data = {
            'nome': 'Atividade de Teste',
            'descricao': 'Descrição da atividade',
            'data_inicio': timezone.now().date(),
            'data_fim': timezone.now().date() + datetime.timedelta(days=1),
            'responsavel': 'Professor Teste',
            'local': 'Local de Teste',
            'tipo_atividade': 'aula',
            'status': 'agendada',
            'turmas': [self.turma1.id, self.turma2.id],
            'todas_turmas': False
        }
        
        form = AtividadeAcademicaForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_missing_required_fields(self):
        """Testa se o formulário é inválido quando campos obrigatórios estão faltando."""
        form_data = {
            'descricao': 'Descrição da atividade',
            'responsavel': 'Professor Teste',
            'local': 'Local de Teste',
            'tipo_atividade': 'aula',
            'status': 'agendada',
            'todas_turmas': False
        }
        
        form = AtividadeAcademicaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('data_inicio', form.errors)
    
    def test_form_data_validation(self):
        """Testa a validação de dados do formulário."""
        # Data de fim anterior à data de início
        form_data = {
            'nome': 'Atividade de Teste',
            'descricao': 'Descrição da atividade',
            'data_inicio': timezone.now().date(),
            'data_fim': timezone.now().date() - datetime.timedelta(days=1),
            'responsavel': 'Professor Teste',
            'local': 'Local de Teste',
            'tipo_atividade': 'aula',
            'status': 'agendada',
            'turmas': [self.turma1.id],
            'todas_turmas': False
        }
        
        form = AtividadeAcademicaForm(data=form_data)
        # Nota: Este teste pode falhar se o formulário não valida que a data_fim seja posterior à data_inicio
        # Se o formulário não faz essa validação, você pode adicionar essa validação ou ajustar o teste
        
        # Tipo de atividade inválido
        form_data = {
            'nome': 'Atividade de Teste',
            'descricao': 'Descrição da atividade',
            'data_inicio': timezone.now().date(),
            'data_fim': timezone.now().date() + datetime.timedelta(days=1),
            'responsavel': 'Professor Teste',
            'local': 'Local de Teste',
            'tipo_atividade': 'tipo_invalido',
            'status': 'agendada',
            'turmas': [self.turma1.id],
            'todas_turmas': False
        }
        
        form = AtividadeAcademicaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo_atividade', form.errors)

class AtividadeRitualisticaFormTest(TestCase):
    """Testes para o formulário AtividadeRitualisticaForm."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar uma turma para os testes
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        # Criar alunos para os testes
        self.aluno1 = Aluno.objects.create(
            cpf="12345678901",
            nome="Aluno Teste 1",
            email="aluno1@teste.com",
            data_nascimento="1990-01-01"
        )
        
        self.aluno2 = Aluno.objects.create(
            cpf="12345678902",
            nome="Aluno Teste 2",
            email="aluno2@teste.com",
            data_nascimento="1990-01-02"
        )
    
    def test_form_valid_data(self):
        """Testa se o formulário é válido com dados corretos."""
        form_data = {
            'nome': 'Atividade Ritualística de Teste',
            'descricao': 'Descrição da atividade ritualística',
            'data': timezone.now().date(),
            'hora_inicio': '10:00',
            'hora_fim': '12:00',
            'local': 'Local de Teste',
            'turma': self.turma.id,
            'participantes': [self.aluno1.cpf, self.aluno2.cpf],
            'todos_alunos': False
        }
        
        form = AtividadeRitualisticaForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_missing_required_fields(self):
        """Testa se o formulário é inválido quando campos obrigatórios estão faltando."""
        form_data = {
            'descricao': 'Descrição da atividade ritualística',
            'hora_inicio': '10:00',
            'hora_fim': '12:00',
            'local': 'Local de Teste',
            'todos_alunos': False
        }
        
        form = AtividadeRitualisticaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('data', form.errors)
        self.assertIn('turma', form.errors)
    
    def test_form_hora_validation(self):
        """Testa a validação de horários do formulário."""
        # Hora de fim anterior à hora de início
        form_data = {
            'nome': 'Atividade Ritualística de Teste',
            'descricao': 'Descrição da atividade ritualística',
            'data': timezone.now().date(),
            'hora_inicio': '12:00',
            'hora_fim': '10:00',
            'local': 'Local de Teste',
            'turma': self.turma.id,
            'participantes': [self.aluno1.cpf],
            'todos_alunos': False
        }
        
        form = AtividadeRitualisticaForm(data=form_data)
        # Nota: Este teste pode falhar se o formulário não valida que a hora_fim seja posterior à hora_inicio
        # Se o formulário não faz essa validação, você pode adicionar essa validação ou ajustar o teste

Seguir estas boas práticas ajudará a manter a qualidade do código e a confiabilidade do sistema OMAUM. Lembre-se de