class AlunoRepository:
    @staticmethod
    def buscar_por_cpf(cpf):
        return Aluno.objects.get(cpf=cpf)
        
    @staticmethod
    def buscar_instrutores_ativos():
        return Aluno.objects.filter(situacao="ATIVO")