from django import forms

from core.utils import get_model_dynamically


class TurmaForm(forms.ModelForm):
    confirmar_encerramento = forms.BooleanField(
        required=False,
        label="Confirmo o encerramento desta turma",
        help_text=(
            "Marque esta opção quando informar a data de fim para registrar o encerramento."
        ),
    )

    class Meta:
        model = get_model_dynamically("turmas", "Turma")
        fields = [
            "curso",
            "nome",
            "descricao",
            "data_inicio",
            "data_fim",
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
            "confirmar_encerramento",
        ]
        labels = {
            "curso": "Curso",
            "nome": "Nome da Turma",
            "data_inicio": "Data de Início",
            "data_fim": "Data de Fim",
            "data_inicio_ativ": "Data de Início das Atividades",
            "data_termino_atividades": "Data de Término das Atividades",
            "data_iniciacao": "Data de Iniciação",
            "data_prim_aula": "Data da Primeira Aula",
            "num_livro": "Nº do Livro de Presenças",
            "perc_presenca_minima": "Percentual Mínimo de Presença (%)",
        }
        help_texts = {
            "perc_presenca_minima": "Percentual mínimo de presença exigido para a turma.",
            "horario": 'Exemplo: 13:30 "às" 15:30',
            "data_inicio": "Obrigatória para todas as turmas.",
            "data_fim": "Informe apenas ao encerrar administrativamente a turma.",
        }
        widgets = {
            "data_inicio": forms.DateInput(attrs={"type": "date"}),
            "data_fim": forms.DateInput(attrs={"type": "date"}),
            "data_inicio_ativ": forms.DateInput(attrs={"type": "date"}),
            "data_termino_atividades": forms.DateInput(attrs={"type": "date"}),
            "data_iniciacao": forms.DateInput(attrs={"type": "date"}),
            "data_prim_aula": forms.DateInput(attrs={"type": "date"}),
            "curso": forms.Select(
                attrs={
                    "class": "curso-select",
                    "placeholder": "Selecione o Curso desejado",
                }
            ),
            # Placeholder segue a máscara exigida para orientar o preenchimento inicial
            "horario": forms.TextInput(attrs={"placeholder": '__:__ "às" __:__'}),
            "num_livro": forms.NumberInput(attrs={"placeholder": "999"}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
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

        self.fields["data_inicio"].required = True
        self.fields["data_fim"].required = False
        self.fields["confirmar_encerramento"].required = False
        self.fields["confirmar_encerramento"].initial = bool(
            getattr(self.instance, "data_fim", None)
        )

        # Torna os campos iniciáticos obrigatórios
        self.fields["num_livro"].required = True
        self.fields["perc_presenca_minima"].required = True
        self.fields["data_iniciacao"].required = True
        self.fields["data_inicio_ativ"].required = True
        self.fields["data_prim_aula"].required = True
        self.fields[
            "data_termino_atividades"
        ].required = False  # Alterado para não ser obrigatório

        # Troca o texto do option vazio para "Selecione"
        for field_name, field in self.fields.items():
            if isinstance(field, forms.models.ModelChoiceField):
                field.empty_label = "Selecione"

        # Flag padrão para a validação do modelo
        setattr(self.instance, "_encerramento_previsto", False)

    def clean(self):
        """Validação adicional dos campos do formulário."""
        cleaned_data = super().clean()
        instrutor_auxiliar = cleaned_data.get("instrutor_auxiliar")
        auxiliar_instrucao = cleaned_data.get("auxiliar_instrucao")
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")
        confirmar_encerramento = cleaned_data.get("confirmar_encerramento")

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

        if not data_inicio:
            self.add_error("data_inicio", "A data de início é obrigatória.")

        if data_fim:
            if data_inicio and data_fim < data_inicio:
                self.add_error(
                    "data_fim",
                    "A data de fim não pode ser anterior à data de início.",
                )
            if not confirmar_encerramento:
                self.add_error(
                    "confirmar_encerramento",
                    "Confirme o encerramento para salvar a data de fim.",
                )
            cleaned_data["_encerrar"] = True
            setattr(self.instance, "_encerramento_previsto", True)
        else:
            cleaned_data["_encerrar"] = False
            setattr(self.instance, "_encerramento_previsto", False)

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
        if data_inicio_ativ and data_termino_atividades:
            if data_termino_atividades < data_inicio_ativ:
                self.add_error(
                    "data_termino_atividades",
                    "A data de término das atividades não pode ser anterior à data de início das atividades.",
                )

        return cleaned_data


class TransferenciaTurmaForm(forms.Form):
    turma_destino = forms.ModelChoiceField(
        label="Turma de destino",
        queryset=get_model_dynamically("turmas", "Turma").objects.none(),
    )
    confirmacao = forms.BooleanField(
        label="Confirmo a transferência de todos os alunos",
        required=True,
    )

    def __init__(self, turma_origem, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Turma = get_model_dynamically("turmas", "Turma")
        self.turma_origem = turma_origem
        self.fields["turma_destino"].queryset = Turma.objects.filter(
            ativo=True,
            status="A",
        ).exclude(pk=turma_origem.pk)

    def clean_turma_destino(self):
        turma_destino = self.cleaned_data["turma_destino"]
        if getattr(turma_destino, "esta_encerrada", False):
            raise forms.ValidationError(
                "A turma de destino não pode estar encerrada."
            )
        return turma_destino
