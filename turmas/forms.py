from django import forms
from core.utils import get_model_dynamically


class TurmaForm(forms.ModelForm):
    class Meta:
        model = get_model_dynamically("turmas", "Turma")
        fields = [
            "curso",
            "nome",
            "descricao",
            "num_livro",
            "perc_presenca_minima",
            "data_iniciacao",
            "data_inicio_ativ",
            "data_termino_atividades",
            "data_prim_aula",
            "dias_semana",
            "horario",
            "local",
            "vagas",
            "status",
            "instrutor",
            "instrutor_auxiliar",
            "auxiliar_instrucao",
            "alerta_instrutor",
            "alerta_mensagem",
        ]
        labels = {
            "curso": "Curso",
            "nome": "Nome da Turma",
            "data_inicio_ativ": "Data de Início das Atividades",
            "data_termino_atividades": "Data de Término das Atividades",
            "data_iniciacao": "Data de Iniciação",
            "data_prim_aula": "Data da Primeira Aula",
            "num_livro": "Nº do Livro de Presenças",
            "perc_presenca_minima": "Percentual de Presença Mínima (%)",
            "dias_semana": "Dia da Semana",
        }
        help_texts = {
            "perc_presenca_minima": "Percentual mínimo de presenças exigido para a turma (ex: 70%).",
            "horario": "Horário previsto de Aula (ex: 19:00 às 22:00)",
            "num_livro": "Número do livro de presenças usado na turma.",
            "data_iniciacao": "Data da cerimônia de iniciação dos alunos.",
            "data_inicio_ativ": "Data de início das atividades acadêmicas da turma.",
            "data_prim_aula": "Data da primeira aula ministrada.",
            "vagas": "Número máximo de alunos que podem ser matriculados.",
            "local": "Local onde as aulas serão ministradas.",
        }
        widgets = {
            "data_inicio_ativ": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "data_termino_atividades": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "data_iniciacao": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "data_prim_aula": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "curso": forms.Select(
                attrs={
                    "class": "form-select",
                    "placeholder": "Selecione o Curso desejado",
                }
            ),
            "nome": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex: Turma A - 2024"}
            ),
            "horario": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "__:__ às __:__", "id": "id_horario"}
            ),
            "num_livro": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "___", "min": "1"}
            ),
            "perc_presenca_minima": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "70", "min": "0", "max": "100"}
            ),
            "vagas": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "30", "min": "1"}
            ),
            "local": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex: Sala 101"}
            ),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Descrição detalhada da turma (opcional)"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "dias_semana": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar apenas alunos ativos para os campos de instrutor
        Aluno = get_model_dynamically("alunos", "Aluno")
        alunos_ativos = Aluno.objects.filter(situacao="ATIVO")

        self.fields["instrutor"].queryset = alunos_ativos
        self.fields["instrutor_auxiliar"].queryset = alunos_ativos
        self.fields["auxiliar_instrucao"].queryset = alunos_ativos

        # Tornar os campos de instrutor auxiliar e auxiliar de instrução opcionais
        self.fields["instrutor_auxiliar"].required = False
        self.fields["auxiliar_instrucao"].required = False

        # Torna os campos iniciáticos obrigatórios
        self.fields["num_livro"].required = True
        self.fields["perc_presenca_minima"].required = True
        self.fields["data_iniciacao"].required = True
        self.fields["data_inicio_ativ"].required = True
        self.fields["data_prim_aula"].required = True
        self.fields[
            "data_termino_atividades"
        ].required = False  # Alterado para não ser obrigatório

        # Configurar campo dias_semana como ChoiceField com as opções corretas
        DIA_SEMANA_CHOICES = [
            ("SEG", "Segunda-feira"),
            ("TER", "Terça-feira"),
            ("QUA", "Quarta-feira"),
            ("QUI", "Quinta-feira"),
            ("SEX", "Sexta-feira"),
            ("SAB", "Sábado"),
            ("DOM", "Domingo"),
        ]
        self.fields["dias_semana"] = forms.ChoiceField(
            choices=[("", "Selecione o dia")] + DIA_SEMANA_CHOICES,
            required=True,
            label="Dia da Semana",
            widget=forms.Select(attrs={"class": "form-select"}),
        )

        # Valor padrão para presença mínima: 70%
        if not self.initial.get("perc_presenca_minima"):
            if getattr(self.instance, "perc_presenca_minima", None):
                self.fields["perc_presenca_minima"].initial = (
                    self.instance.perc_presenca_minima
                )
            else:
                self.fields["perc_presenca_minima"].initial = 70

        # Troca o texto do option vazio para "Selecione"
        for field in self.fields.values():
            if isinstance(field, forms.models.ModelChoiceField):
                field.empty_label = "Selecione"

    def clean(self):
        """Validação adicional dos campos do formulário."""
        cleaned_data = super().clean()
        instrutor_auxiliar = cleaned_data.get("instrutor_auxiliar")
        auxiliar_instrucao = cleaned_data.get("auxiliar_instrucao")

        # Validar que instrutor auxiliar e auxiliar de instrução não sejam a mesma pessoa
        if (
            instrutor_auxiliar
            and auxiliar_instrucao
            and instrutor_auxiliar == auxiliar_instrucao
        ):
            self.add_error(
                "auxiliar_instrucao",
                "O auxiliar de instrução não pode ser o mesmo que o instrutor auxiliar.",
            )

        # Verificar se há vagas e se o número é positivo
        vagas = cleaned_data.get("vagas")
        if vagas is not None and vagas <= 0:
            self.add_error("vagas", "O número de vagas deve ser maior que zero.")

        # Validação extra para garantir que os campos obrigatórios não estejam vazios
        for field in [
            "num_livro",
            "perc_presenca_minima",
            "data_iniciacao",
            "data_inicio_ativ",
            "data_prim_aula",
        ]:
            if not cleaned_data.get(field):
                self.add_error(field, "Este campo é obrigatório.")

        # Validar que a data de término das atividades não seja anterior à de início
        data_inicio_ativ = cleaned_data.get("data_inicio_ativ")
        data_termino_atividades = cleaned_data.get("data_termino_atividades")
        data_iniciacao = cleaned_data.get("data_iniciacao")
        data_prim_aula = cleaned_data.get("data_prim_aula")
        
        if data_inicio_ativ and data_termino_atividades:
            if data_termino_atividades < data_inicio_ativ:
                self.add_error(
                    "data_termino_atividades",
                    "A data de término das atividades não pode ser anterior à data de início das atividades.",
                )
        
        # Validar que a data da primeira aula não seja anterior à data de início das atividades
        if data_inicio_ativ and data_prim_aula:
            if data_prim_aula < data_inicio_ativ:
                self.add_error(
                    "data_prim_aula",
                    "A data da primeira aula não pode ser anterior à data de início das atividades.",
                )
        
        # Validar que a data de iniciação seja coerente
        if data_iniciacao and data_inicio_ativ:
            if data_iniciacao > data_inicio_ativ:
                self.add_error(
                    "data_iniciacao",
                    "A data de iniciação geralmente ocorre antes ou no início das atividades.",
                )

        # NOVA VALIDAÇÃO: Impedir instrutor em múltiplas turmas ativas simultaneamente
        from turmas.models import Turma
        from django.db.models import Q
        
        campos_instrutor = [
            ('instrutor', 'Instrutor Principal'),
            ('instrutor_auxiliar', 'Instrutor Auxiliar'),
            ('auxiliar_instrucao', 'Auxiliar de Instrução')
        ]

        for campo_nome, _ in campos_instrutor:  # _ ignora o label não utilizado
            instrutor = cleaned_data.get(campo_nome)
            if instrutor:
                # Buscar turmas ativas onde este aluno já é instrutor
                turmas_ativas = Turma.objects.filter(
                    Q(instrutor=instrutor) |
                    Q(instrutor_auxiliar=instrutor) |
                    Q(auxiliar_instrucao=instrutor)
                ).filter(status="A")

                # Excluir a própria turma se estiver editando
                if self.instance.pk:
                    turmas_ativas = turmas_ativas.exclude(pk=self.instance.pk)

                # Se encontrou turmas ativas, adicionar erro
                if turmas_ativas.exists():
                    turma_existente = turmas_ativas.first()
                    papel_atual = "Instrutor Principal" if turma_existente.instrutor == instrutor else (
                        "Instrutor Auxiliar" if turma_existente.instrutor_auxiliar == instrutor else
                        "Auxiliar de Instrução"
                    )
                    mensagem = (
                        f"ATENÇÃO: {instrutor.nome} já está atuando como {papel_atual} "
                        f"na turma '{turma_existente.nome}' (Status: Ativa). "
                        f"Um aluno não pode ser instrutor em múltiplas turmas ativas simultaneamente."
                    )
                    self.add_error(campo_nome, mensagem)

        return cleaned_data
