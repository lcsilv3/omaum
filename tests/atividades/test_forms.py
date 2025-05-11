import pytest
from atividades.forms import AtividadeAcademicaForm, AtividadeRitualisticaForm
from turmas.models import Turma
from django.utils import timezone

@pytest.mark.django_db
class TestAtividadeAcademicaForm:
    """Testes para o formulário de AtividadeAcademica."""
    
    def test_form_valido(self):
        """Testa se o formulário é válido com dados corretos."""
        turma = Turma.objects.create(nome="Turma A", codigo="TA-001")
        
        form_data = {
            'nome': 'Aula de Filosofia',
            'descricao': 'Introdução à Filosofia',
            'data_inicio': timezone.now().strftime('%Y-%m-%d'),
            'data_fim': (timezone.now() + timezone.timedelta(hours=2)).strftime('%Y-%m-%d'),
            'responsavel': 'Prof. Silva',
            'local': 'Sala 101',
            'tipo_atividade': 'aula',
            'status': 'agendada',
            'turmas': [turma.id],
        }
        
        form = AtividadeAcademicaForm(data=form_data)
        assert form.is_valid(), f"Formulário inválido: {form.errors}"
    
    def test_form_invalido_campos_obrigatorios(self):
        """Testa se o formulário é inválido quando campos obrigatórios estão ausentes."""
        form_data = {
            'descricao': 'Introdução à Filosofia',
        }
        
        form = AtividadeAcademicaForm(data=form_data)
        assert not form.is_valid()
        assert 'nome' in form.errors
        assert 'data_inicio' in form.errors
    
    def test_form_data_fim_anterior_data_inicio(self):
        """Testa se o formulário rejeita data de fim anterior à data de início."""
        form_data = {
            'nome': 'Aula de Filosofia',
            'data_inicio': timezone.now().strftime('%Y-%m-%d'),
            'data_fim': (timezone.now() - timezone.timedelta(days=1)).strftime('%Y-%m-%d'),
            'tipo_atividade': 'aula',
            'status': 'agendada',
        }
        
        form = AtividadeAcademicaForm(data=form_data)
        assert not form.is_valid()
        assert 'data_fim' in form.errors

@pytest.mark.django_db
class TestAtividadeRitualisticaForm:
    """Testes para o formulário de AtividadeRitualistica."""
    
    def test_form_valido(self):
        """Testa se o formulário é válido com dados corretos."""
        turma = Turma.objects.create(nome="Turma A", codigo="TA-001")
        
        form_data = {
            'nome': 'Ritual de Iniciação',
            'descricao': 'Ritual para novos membros',
            'data': timezone.now().date().strftime('%Y-%m-%d'),
            'hora_inicio': '19:00',
            'hora_fim': '21:00',
            'local': 'Templo Principal',
            'turma': turma.id,
        }
        
        form = AtividadeRitualisticaForm(data=form_data)
        assert form.is_valid(), f"Formulário inválido: {form.errors}"
    
    def test_form_invalido_campos_obrigatorios(self):
        """Testa se o formulário é inválido quando campos obrigatórios estão ausentes."""
        form_data = {
            'descricao': 'Ritual para novos membros',
        }
        
        form = AtividadeRitualisticaForm(data=form_data)
        assert not form.is_valid()
        assert 'nome' in form.errors
        assert 'data' in form.errors
        assert 'hora_inicio' in form.errors
        assert 'hora_fim' in form.errors
        assert 'turma' in form.errors
    
    def test_form_hora_fim_anterior_hora_inicio(self):
        """Testa se o formulário rejeita hora de fim anterior à hora de início."""
        turma = Turma.objects.create(nome="Turma A", codigo="TA-001")
        
        form_data = {
            'nome': 'Ritual de Iniciação',
            'data': timezone.now().date().strftime('%Y-%m-%d'),
            'hora_inicio': '21:00',
            'hora_fim': '19:00',  # Hora de fim anterior à hora de início
            'local': 'Templo Principal',
            'turma': turma.id,
        }
        
        form = AtividadeRitualisticaForm(data=form_data)
        assert not form.is_valid()
        assert 'hora_fim' in form.errors or '__all__' in form.errors
            'data_fim': (timezone.