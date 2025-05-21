'''
# Verificação de Diretórios de Templates

## Configurações de Templates no settings.py



### Arquivo: venv\Lib\site-packages\pyhanko\sign\validation\settings.py

python
from dataclasses import dataclass
from typing import Optional, Set

from asn1crypto import x509
from pyhanko_certvalidator.errors import InvalidCertificateError

from pyhanko.config.api import (
    ConfigurableMixin,
    process_bit_string_flags,
    process_oids,
)


def _match_usages(required: set, present: set, need_all: bool):
    if need_all:
        return not (required - present)
    else:
        # intersection must be non-empty
        return bool(required & present)


@dataclass(frozen=True)
class KeyUsageConstraints(ConfigurableMixin):
    """
    Convenience class to pass around key usage requirements and validate them.
    Intended to be flexible enough to handle both PKIX and ISO 32000 certificate
    seed value constraint semantics.

    .. versionchanged:: 0.6.0
        Bring extended key usage semantics in line with :rfc:`5280` (PKIX).
    """

    key_usage: Optional[Set[str]] = None
    """
    All or some (depending on :attr:`match_all_key_usage`) of these key usage
    extensions must be present in the signer's certificate.
    If not set or empty, all key usages are considered acceptable.
    """

    key_usage_forbidden: Optional[Set[str]] = None
    """
    These key usages must not be present in the signer's certificate.

    .. note::
        This behaviour is undefined in :rfc:`5280` (PKIX), but included for
        compatibility with certificate seed value settings in ISO 32000.
    """

    extd_key_usage: Optional[Set[str]] = None
    """
    List of acceptable key purposes that can appear in an extended key
    usage extension in the signer's certificate, if such an extension is at all
    present. If not set, all extended key usages are considered acceptable.

    If no extended key usage extension is present, or if the
    ``anyExtendedKeyUsage`` key purpose ID is present, the resulting behaviour
    depends on :attr:`explicit_extd_key_usage_required`.

    Setting this option to the empty set (as opposed to ``None``) effectively
    bans all (presumably unrecognised) extended key usages.

    .. warning::
        Note the difference in behaviour with :attr:`key_usage` for empty
        sets of valid usages.

    .. warning::
        Contrary to what some CAs seem to believe, the criticality of the
        extended key usage extension is irrelevant here.
        Even a non-critical EKU extension **must** be enforced according to
        :rfc:`5280` ยง 4.2.1.12.

        In practice, many certificate authorities issue non-repudiation certs
        that can also be used for TLS authentication by only including the
        TLS client authentication key purpose ID in the EKU extension.
        Interpreted strictly, :rfc:`5280` bans such certificates from being
        used to sign documents, and pyHanko will enforce these semantics
        if :attr:`extd_key_usage` is not ``None``.
    """

    explicit_extd_key_usage_required: bool = True
    """
    .. versionadded:: 0.6.0

    Require an extended key usage extension with the right key usages to be
    present if :attr:`extd_key_usage` is non-empty.

    If this flag is ``True``, at least one key purpose in :attr:`extd_key_usage`
    must appear in the certificate's extended key usage, and
    ``anyExtendedKeyUsage`` will be ignored.
    """

    match_all_key_usages: bool = False
    """
    .. versionadded:: 0.6.0

    If ``True``, all key usages indicated in :attr:`key_usage` must be present
    in the certificate. If ``False``, one match suffices.

    If :attr:`key_usage` is empty or ``None``, this option has no effect.
    """

    def validate(self, cert: x509.Certificate):
        self._validate_key_usage(cert.key_usage_value)
        self._validate_extd_key_usage(cert.extended_key_usage_value)

    def _validate_key_usage(self, key_usage_extension_value):
        if not self.key_usage:
            return
        key_usage = self.key_usage or set()
        key_usage_forbidden = self.key_usage_forbidden or set()

        # First, check the "regular" key usage extension
        cert_ku = (
            set(key_usage_extension_value.native)
            if key_usage_extension_value is not None
            else set()
        )

        # check blacklisted key usages (ISO 32k)
        forbidden_ku = cert_ku & key_usage_forbidden
        if forbidden_ku:
            rephrased = map(lambda s: s.replace('_', ' '), forbidden_ku)
            raise InvalidCertificateError(
                "The active key usage policy explicitly bans certificates "
                f"used for {', '.join(rephrased)}."
            )

        # check required key usage extension values
        need_all_ku = self.match_all_key_usages
        if not _match_usages(key_usage, cert_ku, need_all_ku):
            rephrased = map(lambda s: s.replace('_', ' '), key_usage)
            raise InvalidCertificateError(
                "The active key usage policy requires "
                f"{'' if need_all_ku else 'at least one of '}the key "
                f"usage extensions {', '.join(rephrased)} to be present."
            )

    def _validate_extd_key_usage(self, eku_extension_value):
        if self.extd_key_usage is None:
            return
        # check extended key usage
        has_extd_key_usage_ext = eku_extension_value is not None
        cert_eku = (
            set(eku_extension_value.native) if has_extd_key_usage_ext else set()
        )

        if (
            'any_extended_key_usage' in cert_eku
            and not self.explicit_extd_key_usage_required
        ):
            return  # early out, cert is valid for all EKUs

        extd_key_usage = self.extd_key_usage or set()
        if not has_extd_key_usage_ext:
            if self.explicit_extd_key_usage_required:
                raise InvalidCertificateError(
                    "The active key usage policy requires an extended "
                    "key usage extension."
                )
            return  # early out, cert is (presumably?) valid for all EKUs

        if not _match_usages(extd_key_usage, cert_eku, need_all=False):
            if extd_key_usage:
                rephrased = map(lambda s: s.replace('_', ' '), extd_key_usage)
                ok_list = f"Relevant key purposes are {', '.join(rephrased)}."
            else:
                ok_list = "There are no acceptable extended key usages."
            raise InvalidCertificateError(
                "The extended key usages for which this certificate is valid "
                f"do not match the active key usage policy. {ok_list}"
            )

    @classmethod
    def process_entries(cls, config_dict):
        super().process_entries(config_dict)

        # Deal with KeyUsage values first
        # might as well expose key_usage_forbidden while we're at it
        for key_usage_sett in ('key_usage', 'key_usage_forbidden'):
            affected_flags = config_dict.get(key_usage_sett, None)
            if affected_flags is not None:
                config_dict[key_usage_sett] = set(
                    process_bit_string_flags(
                        x509.KeyUsage,
                        affected_flags,
                        key_usage_sett.replace('_', '-'),
                    )
                )

        extd_key_usage = config_dict.get('extd_key_usage', None)
        if extd_key_usage is not None:
            config_dict['extd_key_usage'] = set(
                process_oids(
                    x509.KeyPurposeId, extd_key_usage, 'extd-key-usage'
                )
            )



## Diretórios de Templates Encontrados

- templates
  Arquivos:
- .venv\Lib\site-packages\debug_toolbar\templates
  Arquivos:
  - debug_toolbar\base.html
  - debug_toolbar\redirect.html
  - debug_toolbar\includes\panel_button.html
  - debug_toolbar\includes\panel_content.html
  - debug_toolbar\includes\theme_selector.html
  - debug_toolbar\panels\alerts.html
  - debug_toolbar\panels\cache.html
  - debug_toolbar\panels\headers.html
  - debug_toolbar\panels\history.html
  - debug_toolbar\panels\history_tr.html
  - debug_toolbar\panels\profiling.html
  - debug_toolbar\panels\request.html
  - debug_toolbar\panels\request_variables.html
  - debug_toolbar\panels\settings.html
  - debug_toolbar\panels\signals.html
  - debug_toolbar\panels\sql.html
  - debug_toolbar\panels\sql_explain.html
  - debug_toolbar\panels\sql_profile.html
  - debug_toolbar\panels\sql_select.html
  - debug_toolbar\panels\staticfiles.html
  - debug_toolbar\panels\templates.html
  - debug_toolbar\panels\template_source.html
  - debug_toolbar\panels\timer.html
  - debug_toolbar\panels\versions.html
- .venv\Lib\site-packages\debug_toolbar\panels\templates
  Arquivos:
  - jinja2.py
  - panel.py
  - views.py
  - __init__.py
  - __pycache__\jinja2.cpython-312.pyc
  - __pycache__\panel.cpython-312.pyc
  - __pycache__\views.cpython-312.pyc
  - __pycache__\__init__.cpython-312.pyc
- .venv\Lib\site-packages\django\contrib\admin\templates
  Arquivos:
  - admin\404.html
  - admin\500.html
  - admin\actions.html
  - admin\app_index.html
  - admin\app_list.html
  - admin\base.html
  - admin\base_site.html
  - admin\change_form.html
  - admin\change_form_object_tools.html
  - admin\change_list.html
  - admin\change_list_object_tools.html
  - admin\change_list_results.html
  - admin\color_theme_toggle.html
  - admin\date_hierarchy.html
  - admin\delete_confirmation.html
  - admin\delete_selected_confirmation.html
  - admin\filter.html
  - admin\index.html
  - admin\invalid_setup.html
  - admin\login.html
  - admin\nav_sidebar.html
  - admin\object_history.html
  - admin\pagination.html
  - admin\popup_response.html
  - admin\prepopulated_fields_js.html
  - admin\search_form.html
  - admin\submit_line.html
  - admin\auth\user\add_form.html
  - admin\auth\user\change_password.html
  - admin\edit_inline\stacked.html
  - admin\edit_inline\tabular.html
  - admin\includes\fieldset.html
  - admin\includes\object_delete_summary.html
  - admin\widgets\clearable_file_input.html
  - admin\widgets\date.html
  - admin\widgets\foreign_key_raw_id.html
  - admin\widgets\many_to_many_raw_id.html
  - admin\widgets\radio.html
  - admin\widgets\related_widget_wrapper.html
  - admin\widgets\split_datetime.html
  - admin\widgets\time.html
  - admin\widgets\url.html
  - registration\logged_out.html
  - registration\password_change_done.html
  - registration\password_change_form.html
  - registration\password_reset_complete.html
  - registration\password_reset_confirm.html
  - registration\password_reset_done.html
  - registration\password_reset_email.html
  - registration\password_reset_form.html
- .venv\Lib\site-packages\django\contrib\admindocs\templates
  Arquivos:
  - admin_doc\bookmarklets.html
  - admin_doc\index.html
  - admin_doc\missing_docutils.html
  - admin_doc\model_detail.html
  - admin_doc\model_index.html
  - admin_doc\template_detail.html
  - admin_doc\template_filter_index.html
  - admin_doc\template_tag_index.html
  - admin_doc\view_detail.html
  - admin_doc\view_index.html
- .venv\Lib\site-packages\django\contrib\auth\templates
  Arquivos:
  - auth\widgets\read_only_password_hash.html
  - registration\password_reset_subject.txt
- .venv\Lib\site-packages\django\contrib\gis\templates
  Arquivos:
  - gis\openlayers-osm.html
  - gis\openlayers.html
  - gis\kml\base.kml
  - gis\kml\placemarks.kml
- .venv\Lib\site-packages\django\contrib\postgres\templates
  Arquivos:
  - postgres\widgets\split_array.html
- .venv\Lib\site-packages\django\contrib\sitemaps\templates
  Arquivos:
  - sitemap.xml
  - sitemap_index.xml
- .venv\Lib\site-packages\django\forms\templates
  Arquivos:
  - django\forms\attrs.html
  - django\forms\div.html
  - django\forms\field.html
  - django\forms\label.html
  - django\forms\p.html
  - django\forms\table.html
  - django\forms\ul.html
  - django\forms\errors\dict\default.html
  - django\forms\errors\dict\text.txt
  - django\forms\errors\dict\ul.html
  - django\forms\errors\list\default.html
  - django\forms\errors\list\text.txt
  - django\forms\errors\list\ul.html
  - django\forms\formsets\div.html
  - django\forms\formsets\p.html
  - django\forms\formsets\table.html
  - django\forms\formsets\ul.html
  - django\forms\widgets\attrs.html
  - django\forms\widgets\checkbox.html
  - django\forms\widgets\checkbox_option.html
  - django\forms\widgets\checkbox_select.html
  - django\forms\widgets\clearable_file_input.html
  - django\forms\widgets\date.html
  - django\forms\widgets\datetime.html
  - django\forms\widgets\email.html
  - django\forms\widgets\file.html
  - django\forms\widgets\hidden.html
  - django\forms\widgets\input.html
  - django\forms\widgets\input_option.html
  - django\forms\widgets\multiple_hidden.html
  - django\forms\widgets\multiple_input.html
  - django\forms\widgets\multiwidget.html
  - django\forms\widgets\number.html
  - django\forms\widgets\password.html
  - django\forms\widgets\radio.html
  - django\forms\widgets\radio_option.html
  - django\forms\widgets\select.html
  - django\forms\widgets\select_date.html
  - django\forms\widgets\select_option.html
  - django\forms\widgets\splitdatetime.html
  - django\forms\widgets\splithiddendatetime.html
  - django\forms\widgets\text.html
  - django\forms\widgets\textarea.html
  - django\forms\widgets\time.html
  - django\forms\widgets\url.html
- .venv\Lib\site-packages\django\views\templates
  Arquivos:
  - csrf_403.html
  - default_urlconf.html
  - directory_index.html
  - i18n_catalog.js
  - technical_404.html
  - technical_500.html
  - technical_500.txt
- .venv\Lib\site-packages\django_extensions\templates
  Arquivos:
  - django_extensions\graph_models\django2018\digraph.dot
  - django_extensions\graph_models\django2018\label.dot
  - django_extensions\graph_models\django2018\relation.dot
  - django_extensions\graph_models\original\digraph.dot
  - django_extensions\graph_models\original\label.dot
  - django_extensions\graph_models\original\relation.dot
  - django_extensions\widgets\foreignkey_searchinput.html
- alunos\templates
  Arquivos:
  - alunos\confirmar_remocao_instrutoria.html
  - alunos\criar_aluno.html
  - alunos\dashboard.html
  - alunos\detalhar_aluno.html
  - alunos\diagnostico_instrutores.html
  - alunos\editar_aluno.html
  - alunos\excluir_aluno.html
  - alunos\formulario_aluno.html
  - alunos\importar_alunos.html
  - alunos\listar_alunos.html
  - alunos\registro.html
  - alunos\relatorio_alunos.html
- atividades\templates
  Arquivos:
  - atividades\calendario_atividades.html
  - atividades\confirmar_copia_academica.html
  - atividades\confirmar_copia_ritualistica.html
  - atividades\confirmar_exclusao_academica.html
  - atividades\confirmar_exclusao_ritualistica.html
  - atividades\copiar_atividade_academica.html
  - atividades\copiar_atividade_ritualistica.html
  - atividades\criar_atividade_academica.html
  - atividades\criar_atividade_ritualistica.html
  - atividades\dashboard.html
  - atividades\dashboard_atividades.html
  - atividades\detalhar_atividade_academica.html
  - atividades\detalhar_atividade_ritualistica.html
  - atividades\editar_atividade_academica.html
  - atividades\editar_atividade_ritualistica.html
  - atividades\excluir_atividade_academica.html
  - atividades\excluir_atividade_ritualistica.html
  - atividades\formulario_atividade_academica.html
  - atividades\formulario_atividade_ritualistica.html
  - atividades\importar_atividades.html
  - atividades\index.html
  - atividades\listar_atividades.html
  - atividades\listar_atividades_academicas.html
  - atividades\listar_atividades_ritualisticas.html
  - atividades\registrar_frequencia.html
  - atividades\relatorio_atividades.html
  - atividades\visualizar_frequencia.html
- cargos\templates
  Arquivos:
  - cargos\atribuir_cargo.html
  - cargos\confirmar_exclusao.html
  - cargos\criar_cargo.html
  - cargos\detalhar_cargo.html
  - cargos\detalhes_cargo.html
  - cargos\detalhe_cargo.html
  - cargos\editar_cargo.html
  - cargos\excluir_cargo.html
  - cargos\formulario_cargo.html
  - cargos\form_cargo.html
  - cargos\importar_cargos.html
  - cargos\listar_cargos.html
  - cargos\remover_atribuicao.html
- core\templates
  Arquivos:
- cursos\templates
  Arquivos:
  - cursos\criar_curso.html
  - cursos\detalhar_curso.html
  - cursos\editar_curso.html
  - cursos\excluir_curso.html
  - cursos\importar_cursos.html
  - cursos\listar_cursos.html
- frequencias\templates
  Arquivos:
  - frequencias\criar_notificacao.html
  - frequencias\dashboard.html
  - frequencias\detalhar_carencia.html
  - frequencias\detalhar_frequencia.html
  - frequencias\detalhar_frequencia_mensal.html
  - frequencias\detalhar_notificacao.html
  - frequencias\editar_carencia.html
  - frequencias\editar_frequencia.html
  - frequencias\editar_notificacao.html
  - frequencias\enviar_notificacao.html
  - frequencias\estatisticas_frequencia.html
  - frequencias\excluir_frequencia.html
  - frequencias\excluir_frequencia_mensal.html
  - frequencias\filtro_painel_frequencias.html
  - frequencias\formulario_frequencia_mensal.html
  - frequencias\gerar_frequencia_mensal.html
  - frequencias\gerenciar_carencias.html
  - frequencias\historico_frequencia.html
  - frequencias\importar_frequencias.html
  - frequencias\iniciar_acompanhamento.html
  - frequencias\listar_carencias.html
  - frequencias\listar_frequencias.html
  - frequencias\listar_notificacoes_carencia.html
  - frequencias\notificacoes_carencia.html
  - frequencias\painel_frequencias.html
  - frequencias\registrar_frequencia.html
  - frequencias\registrar_frequencia_turma.html
  - frequencias\relatorio_carencias.html
  - frequencias\relatorio_frequencias.html
  - frequencias\resolver_carencia.html
  - frequencias\responder_notificacao.html
  - frequencias\visualizar_resposta.html
- iniciacoes\templates
  Arquivos:
  - iniciacoes\criar_grau.html
  - iniciacoes\criar_iniciacao.html
  - iniciacoes\detalhar_iniciacao.html
  - iniciacoes\editar_grau.html
  - iniciacoes\editar_iniciacao.html
  - iniciacoes\excluir_grau.html
  - iniciacoes\excluir_iniciacao.html
  - iniciacoes\listar_graus.html
  - iniciacoes\listar_iniciacoes.html
- matriculas\templates
  Arquivos:
  - matriculas\cancelar_matricula.html
  - matriculas\detalhar_matricula.html
  - matriculas\detalhes_matricula.html
  - matriculas\importar_matriculas.html
  - matriculas\listar_matriculas.html
  - matriculas\realizar_matricula.html
- notas\templates
  Arquivos:
  - notas\dashboard.html
  - notas\dashboard_notas.html
  - notas\detalhar_nota.html
  - notas\excluir_nota.html
  - notas\formulario_nota.html
  - notas\listar_notas.html
  - notas\relatorio_notas_aluno.html
  - notas\pdf\notas_pdf.html
- omaum\templates
  Arquivos:
  - 403.html
  - 404.html
  - 500.html
  - atualizar_configuracao.html
  - base copy.html
  - base.html
  - csrf_test.html
  - home.html
  - home_old.html
  - listar_alunos.html
  - lista_categorias.html
  - manutencao.html
  - painel_controle.html
  - sidebar.html
  - includes\action_buttons.html
  - includes\form_error.html
  - includes\form_errors.html
  - includes\form_field.html
  - registration\login.html
  - registration\registro.html
- pagamentos\templates
  Arquivos:
  - __init__.py
  - pagamentos\criar_pagamento.html
  - pagamentos\dashboard.html
  - pagamentos\dashboard_financeiro.html
  - pagamentos\dashboard_pagamentos.html
  - pagamentos\detalhar_pagamento.html
  - pagamentos\editar_pagamento.html
  - pagamentos\excluir_pagamento.html
  - pagamentos\exportar_pagamentos.html
  - pagamentos\formulario_pagamento.html
  - pagamentos\importar_pagamentos.html
  - pagamentos\listar_pagamentos.html
  - pagamentos\pagamentos_aluno.html
  - pagamentos\pagamentos_por_turma.html
  - pagamentos\pagamento_rapido.html
  - pagamentos\registrar_pagamento.html
  - pagamentos\registrar_pagamento_rapido.html
  - pagamentos\relatorio_financeiro.html
  - pagamentos\__init__.py
  - pdf\pagamentos_pdf.html
- presencas\templates
  Arquivos:
  - presencas\detalhar_presenca.html
  - presencas\editar_presenca.html
  - presencas\excluir_presenca.html
  - presencas\filtro_presencas.html
  - presencas\formulario_presenca.html
  - presencas\formulario_presencas_multiplas.html
  - presencas\formulario_presencas_multiplas_passo1.html
  - presencas\formulario_presencas_multiplas_passo2.html
  - presencas\historico_presencas.html
  - presencas\importar_presencas.html
  - presencas\listar_presencas.html
  - presencas\registrar_presenca.html
  - presencas\registrar_presencas_multiplas.html
  - presencas\registrar_presenca_em_massa.html
  - presencas\relatorio_presencas.html
  - presencas\views\atividade.py
  - presencas\views\listagem.py
  - presencas\views\multiplas.py
  - presencas\views\__init__.py
  - presencas\views\__pycache__\atividade.cpython-312.pyc
  - presencas\views\__pycache__\listagem.cpython-312.pyc
  - presencas\views\__pycache__\multiplas.cpython-312.pyc
  - presencas\views\__pycache__\__init__.cpython-312.pyc
- punicoes\templates
  Arquivos:
  - punicoes\criar_punicao.html
  - punicoes\criar_tipo_punicao.html
  - punicoes\detalhar_punicao.html
  - punicoes\detalhe_punicao.html
  - punicoes\editar_punicao.html
  - punicoes\editar_tipo_punicao.html
  - punicoes\excluir_punicao.html
  - punicoes\excluir_tipo_punicao.html
  - punicoes\listar_punicoes.html
  - punicoes\listar_tipos_punicao.html
- relatorios\templates
  Arquivos:
  - relatorios\confirmar_exclusao.html
  - relatorios\detalhar_relatorio.html
  - relatorios\form_relatorio.html
  - relatorios\gerar_relatorio.html
  - relatorios\listar_relatorios.html
  - relatorios\relatorio_alunos.html
  - relatorios\relatorio_alunos_pdf.html
  - relatorios\relatorio_presencas.html
  - relatorios\relatorio_presencas_pdf.html
  - relatorios\relatorio_punicoes.html
  - relatorios\relatorio_punicoes_pdf.html
- turmas\templates
  Arquivos:
  - turmas\adicionar_aluno.html
  - turmas\cancelar_matricula.html
  - turmas\confirmar_cancelamento_matricula.html
  - turmas\criar_turma.html
  - turmas\dashboard.html
  - turmas\dashboard_turmas.html
  - turmas\detalhar_turma.html
  - turmas\editar_turma.html
  - turmas\excluir_turma.html
  - turmas\formulario_instrutoria.html
  - turmas\formulario_turma.html
  - turmas\importar_turmas.html
  - turmas\listar_alunos_matriculados.html
  - turmas\listar_turmas.html
  - turmas\matricular_aluno.html
  - turmas\registrar_frequencia_turma.html
  - turmas\relatorio_frequencia_turma.html
  - turmas\relatorio_turmas.html
  - turmas\turma_form.html
- venv\Lib\site-packages\debug_toolbar\templates
  Arquivos:
  - debug_toolbar\base.html
  - debug_toolbar\redirect.html
  - debug_toolbar\includes\panel_button.html
  - debug_toolbar\includes\panel_content.html
  - debug_toolbar\includes\theme_selector.html
  - debug_toolbar\panels\alerts.html
  - debug_toolbar\panels\cache.html
  - debug_toolbar\panels\headers.html
  - debug_toolbar\panels\history.html
  - debug_toolbar\panels\history_tr.html
  - debug_toolbar\panels\profiling.html
  - debug_toolbar\panels\request.html
  - debug_toolbar\panels\request_variables.html
  - debug_toolbar\panels\settings.html
  - debug_toolbar\panels\signals.html
  - debug_toolbar\panels\sql.html
  - debug_toolbar\panels\sql_explain.html
  - debug_toolbar\panels\sql_profile.html
  - debug_toolbar\panels\sql_select.html
  - debug_toolbar\panels\staticfiles.html
  - debug_toolbar\panels\templates.html
  - debug_toolbar\panels\template_source.html
  - debug_toolbar\panels\timer.html
  - debug_toolbar\panels\versions.html
- venv\Lib\site-packages\debug_toolbar\panels\templates
  Arquivos:
  - jinja2.py
  - panel.py
  - views.py
  - __init__.py
  - __pycache__\panel.cpython-312.pyc
  - __pycache__\views.cpython-312.pyc
  - __pycache__\__init__.cpython-312.pyc
- venv\Lib\site-packages\django\contrib\admin\templates
  Arquivos:
  - admin\404.html
  - admin\500.html
  - admin\actions.html
  - admin\app_index.html
  - admin\app_list.html
  - admin\base.html
  - admin\base_site.html
  - admin\change_form.html
  - admin\change_form_object_tools.html
  - admin\change_list.html
  - admin\change_list_object_tools.html
  - admin\change_list_results.html
  - admin\color_theme_toggle.html
  - admin\date_hierarchy.html
  - admin\delete_confirmation.html
  - admin\delete_selected_confirmation.html
  - admin\filter.html
  - admin\index.html
  - admin\invalid_setup.html
  - admin\login.html
  - admin\nav_sidebar.html
  - admin\object_history.html
  - admin\pagination.html
  - admin\popup_response.html
  - admin\prepopulated_fields_js.html
  - admin\search_form.html
  - admin\submit_line.html
  - admin\auth\user\add_form.html
  - admin\auth\user\change_password.html
  - admin\edit_inline\stacked.html
  - admin\edit_inline\tabular.html
  - admin\includes\fieldset.html
  - admin\includes\object_delete_summary.html
  - admin\widgets\clearable_file_input.html
  - admin\widgets\date.html
  - admin\widgets\foreign_key_raw_id.html
  - admin\widgets\many_to_many_raw_id.html
  - admin\widgets\radio.html
  - admin\widgets\related_widget_wrapper.html
  - admin\widgets\split_datetime.html
  - admin\widgets\time.html
  - admin\widgets\url.html
  - registration\logged_out.html
  - registration\password_change_done.html
  - registration\password_change_form.html
  - registration\password_reset_complete.html
  - registration\password_reset_confirm.html
  - registration\password_reset_done.html
  - registration\password_reset_email.html
  - registration\password_reset_form.html
- venv\Lib\site-packages\django\contrib\admindocs\templates
  Arquivos:
  - admin_doc\bookmarklets.html
  - admin_doc\index.html
  - admin_doc\missing_docutils.html
  - admin_doc\model_detail.html
  - admin_doc\model_index.html
  - admin_doc\template_detail.html
  - admin_doc\template_filter_index.html
  - admin_doc\template_tag_index.html
  - admin_doc\view_detail.html
  - admin_doc\view_index.html
- venv\Lib\site-packages\django\contrib\auth\templates
  Arquivos:
  - auth\widgets\read_only_password_hash.html
  - registration\password_reset_subject.txt
- venv\Lib\site-packages\django\contrib\gis\templates
  Arquivos:
  - gis\openlayers-osm.html
  - gis\openlayers.html
  - gis\kml\base.kml
  - gis\kml\placemarks.kml
- venv\Lib\site-packages\django\contrib\postgres\templates
  Arquivos:
  - postgres\widgets\split_array.html
- venv\Lib\site-packages\django\contrib\sitemaps\templates
  Arquivos:
  - sitemap.xml
  - sitemap_index.xml
- venv\Lib\site-packages\django\forms\templates
  Arquivos:
  - django\forms\attrs.html
  - django\forms\div.html
  - django\forms\field.html
  - django\forms\label.html
  - django\forms\p.html
  - django\forms\table.html
  - django\forms\ul.html
  - django\forms\errors\dict\default.html
  - django\forms\errors\dict\text.txt
  - django\forms\errors\dict\ul.html
  - django\forms\errors\list\default.html
  - django\forms\errors\list\text.txt
  - django\forms\errors\list\ul.html
  - django\forms\formsets\div.html
  - django\forms\formsets\p.html
  - django\forms\formsets\table.html
  - django\forms\formsets\ul.html
  - django\forms\widgets\attrs.html
  - django\forms\widgets\checkbox.html
  - django\forms\widgets\checkbox_option.html
  - django\forms\widgets\checkbox_select.html
  - django\forms\widgets\clearable_file_input.html
  - django\forms\widgets\date.html
  - django\forms\widgets\datetime.html
  - django\forms\widgets\email.html
  - django\forms\widgets\file.html
  - django\forms\widgets\hidden.html
  - django\forms\widgets\input.html
  - django\forms\widgets\input_option.html
  - django\forms\widgets\multiple_hidden.html
  - django\forms\widgets\multiple_input.html
  - django\forms\widgets\multiwidget.html
  - django\forms\widgets\number.html
  - django\forms\widgets\password.html
  - django\forms\widgets\radio.html
  - django\forms\widgets\radio_option.html
  - django\forms\widgets\select.html
  - django\forms\widgets\select_date.html
  - django\forms\widgets\select_option.html
  - django\forms\widgets\splitdatetime.html
  - django\forms\widgets\splithiddendatetime.html
  - django\forms\widgets\text.html
  - django\forms\widgets\textarea.html
  - django\forms\widgets\time.html
  - django\forms\widgets\url.html
- venv\Lib\site-packages\django\views\templates
  Arquivos:
  - csrf_403.html
  - default_urlconf.html
  - directory_index.html
  - i18n_catalog.js
  - technical_404.html
  - technical_500.html
  - technical_500.txt
- venv\Lib\site-packages\django_extensions\templates
  Arquivos:
  - django_extensions\graph_models\django2018\digraph.dot
  - django_extensions\graph_models\django2018\label.dot
  - django_extensions\graph_models\django2018\relation.dot
  - django_extensions\graph_models\original\digraph.dot
  - django_extensions\graph_models\original\label.dot
  - django_extensions\graph_models\original\relation.dot
  - django_extensions\widgets\foreignkey_searchinput.html
- venv\Lib\site-packages\pandas\io\formats\templates
  Arquivos:
  - html.tpl
  - html_style.tpl
  - html_table.tpl
  - latex.tpl
  - latex_longtable.tpl
  - latex_table.tpl
  - string.tpl

## Busca pelo template listar_alunos.html

Encontrado em: alunos\templates\alunos\listar_alunos.html
Encontrado em: omaum\templates\listar_alunos.html

'''