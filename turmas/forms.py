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
            "perc_carencia",
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
            "perc_carencia": "Percentual de Carência (%)",
        }
        help_texts = {
            "perc_carencia": "Percentual mínimo de faltas permitido para a turma.",
            "horario": "Exemplo: 13:30 às 15:30",
        }
        widgets = {
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
            "horario": forms.TextInput(attrs={"placeholder": "13:30 às 15:30"}),
            "num_livro": forms.NumberInput(attrs={"placeholder": "999"}),
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
        self.fields["perc_carencia"].required = True
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
            "perc_carencia",
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