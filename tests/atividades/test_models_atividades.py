
from atividades.models import Atividade

class TestAtividadeModel:
	def test_criacao_atividade_valida(self, db):
		# Ajuste os nomes dos campos conforme o modelo real de Atividade
		atividade = Atividade.objects.create(nome="Aula de Matemática")
		assert atividade.pk is not None
		assert atividade.nome == "Aula de Matemática"

	def test_nome_obrigatorio(self, db):
		atividade = Atividade()
		try:
			atividade.full_clean()
			assert False, "Deveria falhar sem nome"
		except Exception as e:
			assert 'nome' in str(e)

	def test_outro_campo_obrigatorio(self, db):
		# Substitua 'outro_campo' pelo nome de um campo obrigatório real
		atividade = Atividade(nome="Teste")
		try:
			atividade.full_clean()
			assert False, "Deveria falhar sem outro campo obrigatório"
		except Exception as e:
			assert 'outro_campo' in str(e)
