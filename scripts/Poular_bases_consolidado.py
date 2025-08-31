
import os
import sys
import django
import random
import json
from datetime import date, time, timedelta

# Configuração do ambiente Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from django.core.files import File
from alunos.models import Aluno, Estado, Cidade, Bairro, RegistroHistorico, Codigo, TipoCodigo
from cursos.models import Curso
from turmas.models import Turma
from presencas.models import Presenca
from pagamentos.models import Pagamento
from notas.models import Nota
from matriculas.models import Matricula

# Listas de nomes, sobrenomes, sexos, tipos sanguíneos, fatores RH, convênios, hospitais
nomes = ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Juliana"]
sobrenomes = ["Silva", "Souza", "Oliveira", "Santos", "Lima", "Pereira", "Ferreira", "Almeida", "Costa", "Gomes"]
sexos = ["M", "F"]
tipos_sanguineos = ["A", "B", "AB", "O"]
fatores_rh = ["+", "-"]
convenios = ["Unimed", "Bradesco", "SulAmérica", "Amil", "Nenhum"]
hospitais = ["Hospital Central", "Santa Casa", "Hospital Municipal", "Nenhum"]

def gerar_cpf_unico():
	return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"

def gerar_email_unico(nome, sobrenome):
	return f"{nome.lower()}.{sobrenome.lower()}{random.randint(1,9999)}@exemplo.com"

def baixar_foto_aleatoria(sexo, nome, sobrenome):
	return None

def popular_turmas():
	turmas = list(Turma.objects.all())
	if not turmas:
		cursos = list(Curso.objects.all())
		for i in range(3):
			if cursos:
				turma = Turma.objects.create(
					nome=f"Turma Teste {i+1}",
					curso=random.choice(cursos)
				)
				turmas.append(turma)
	return turmas

def popular_alunos_e_matriculas(turmas):
		QUANTIDADE_ALUNOS = 50
		alunos_criados = 0
		matriculas_criadas = 0
		dados_export = []
		estados = list(Estado.objects.all())
		cidades = list(Cidade.objects.all())
		bairros = list(Bairro.objects.all())
		cursos = list(Curso.objects.all())
		# Buscar ou criar um TipoCodigo e um Codigo de teste para uso nos registros históricos
		tipo_codigo_teste, _ = TipoCodigo.objects.get_or_create(
			nome='Tipo Teste',
			defaults={'descricao': 'Tipo de Código para testes'}
		)
		codigo_teste, _ = Codigo.objects.get_or_create(
			nome='TESTE',
			defaults={
				'descricao': 'Código de Teste',
				'tipo_codigo': tipo_codigo_teste
			}
		)
		for i in range(QUANTIDADE_ALUNOS):
			try:
				nome_idx = random.randint(0, len(nomes) - 1)
				sobrenome_idx = random.randint(0, len(sobrenomes) - 1)
				nome_completo = f"{nomes[nome_idx]} {sobrenomes[sobrenome_idx]}"
				ano_nascimento = random.randint(1970, 2000)
				mes_nascimento = random.randint(1, 12)
				dia_nascimento = random.randint(1, 28)
				hora_nascimento = random.randint(0, 23)
				minuto_nascimento = random.randint(0, 59)
				sexo = random.choice(sexos)
				cidade_ref = random.choice(cidades) if cidades else None
				estado_ref = cidade_ref.estado if cidade_ref else (random.choice(estados) if estados else None)
				bairro_ref = random.choice(bairros) if bairros else None
				aluno_dados = {
					'cpf': gerar_cpf_unico(),
					'nome': nome_completo,
					'data_nascimento': date(ano_nascimento, mes_nascimento, dia_nascimento),
					'hora_nascimento': time(hora_nascimento, minuto_nascimento),
					'email': gerar_email_unico(nomes[nome_idx], sobrenomes[sobrenome_idx]),
					'sexo': sexo,
					'nacionalidade': 'Brasileira',
					'naturalidade': cidade_ref.nome if cidade_ref else 'Desconhecida',
					'rua': f"Rua {random.choice(sobrenomes)} {random.randint(1, 100)}",
					'numero_imovel': str(random.randint(1, 999)),
					'complemento': f"Apto {random.randint(1, 100)}" if random.random() > 0.5 else "",
					'bairro': bairro_ref.nome if bairro_ref else 'Centro',
					'cidade': cidade_ref.nome if cidade_ref else 'Desconhecida',
					'estado': estado_ref.codigo if estado_ref else 'SP',
					'cep': f"{random.randint(10000, 99999)}{random.randint(100, 999)}",
					'nome_primeiro_contato': f"{random.choice(nomes)} {random.choice(sobrenomes)}",
					'celular_primeiro_contato': f"{random.randint(10, 99)}9{random.randint(10000000, 99999999)}",
					'tipo_relacionamento_primeiro_contato': random.choice(['Pai', 'Mãe', 'Irmão', 'Irmã', 'Cônjuge']),
					'nome_segundo_contato': f"{random.choice(nomes)} {random.choice(sobrenomes)}",
					'celular_segundo_contato': f"{random.randint(10, 99)}9{random.randint(10000000, 99999999)}",
					'tipo_relacionamento_segundo_contato': random.choice(['Pai', 'Mãe', 'Irmão', 'Irmã', 'Amigo', 'Amiga']),
					'tipo_sanguineo': random.choice([a + b for a in tipos_sanguineos for b in fatores_rh]),
					'alergias': (
						'Nenhuma'
						if random.random() > 0.3
						else random.choice([
							'Poeira', 'Pólen', 'Penicilina', 'Frutos do mar', 'Amendoim'
						])
					),
					'condicoes_medicas_gerais': (
						'Nenhuma'
						if random.random() > 0.3
						else random.choice([
							'Asma', 'Hipertensão', 'Diabetes', 'Rinite alérgica'
						])
					),
					'convenio_medico': random.choice(convenios),
					'hospital': random.choice(hospitais)
				}
				aluno = Aluno.objects.create(**aluno_dados)
				for _ in range(random.randint(1, 3)):
					RegistroHistorico.objects.create(
						aluno=aluno,
						codigo=codigo_teste,
						ordem_servico=f"OS-{random.randint(1000, 9999)}",
						data_os=date.today() - timedelta(days=random.randint(0, 365*5)),
						observacoes="Registro automático."
					)
				matriculas = []
				if turmas and random.random() > 0.1:
					num_matriculas = random.randint(1, min(2, len(turmas)))
					turmas_selecionadas = random.sample(turmas, num_matriculas)
					for turma in turmas_selecionadas:
						if not Matricula.objects.filter(aluno=aluno, turma=turma).exists():
							Matricula.objects.create(
								aluno=aluno,
								turma=turma,
								data_matricula=date.today() - timedelta(days=random.randint(0, 365))
							)
							matriculas.append(turma.id)
							matriculas_criadas += 1
				presencas = []
				for turma in turmas:
					for _ in range(random.randint(1, 2)):
						data_presenca = date.today() - timedelta(days=random.randint(0, 180))
						presente = random.choice([True, False])
						pres = Presenca.objects.create(
							aluno=aluno,
							turma=turma,
							atividade=None,
							data=data_presenca,
							presente=presente,
							registrado_por="Script",
						)
						presencas.append(pres.id)
				pagamentos = []
				for _ in range(random.randint(1, 2)):
					valor = random.randint(100, 500)
					status = random.choice(["PENDENTE", "PAGO", "ATRASADO"])
					data_venc = date.today() - timedelta(days=random.randint(0, 90))
					pag = Pagamento.objects.create(
						aluno=aluno,
						valor=valor,
						data_vencimento=data_venc,
						status=status,
						metodo_pagamento=random.choice(["DINHEIRO", "PIX", "CARTAO_CREDITO"]),
					)
					pagamentos.append(pag.id)
				notas = []
				for _ in range(random.randint(1, 2)):
					if cursos and turmas:
						curso = random.choice(cursos)
						turma = random.choice(turmas)
						nota = Nota.objects.create(
							aluno=aluno,
							curso=curso,
							turma=turma,
							tipo_avaliacao=random.choice([
								'prova', 'trabalho', 'atividade', 'exame', 'outro'
							]),
							valor=random.uniform(0, 10),
							peso=random.choice([1.0, 2.0]),
							data=date.today() - timedelta(days=random.randint(0, 180)),
						)
						notas.append(nota.id)
				dados_export.append({
					'aluno': aluno.cpf,
					'matriculas': matriculas,
					'presencas': presencas,
					'pagamentos': pagamentos,
					'notas': notas
				})
				print(f'({i+1}/{QUANTIDADE_ALUNOS}) Aluno "{aluno.nome}" criado com sucesso!')
				alunos_criados += 1
			except Exception as e:
				print(f'Erro ao criar aluno {i+1}: {str(e)}')
		print(f'\nTotal de {alunos_criados} alunos criados com sucesso!')
		print(f'Total de {matriculas_criadas} matrículas criadas.')
		print(f'Total geral de alunos no banco: {Aluno.objects.count()}')
		print(f'Total geral de matrículas no banco: {Matricula.objects.count()}')
		with open("dados_teste_gerados.json", "w", encoding="utf-8") as f:
			json.dump(dados_export, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
	print("Iniciando população consolidada das bases de teste...")
	turmas = popular_turmas()
	if turmas:
		popular_alunos_e_matriculas(turmas)
	print("\nPopulação consolidada concluída!")

