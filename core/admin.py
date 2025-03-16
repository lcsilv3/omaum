from django.contrib import admin
from .models import Aluno, Curso, Turma, AtividadeAcademica, AtividadeRitualistica
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
admin.site.site_header = mark_safe(_("Painel de Administração - <b><u> SISTEMA DE GESTÃO DE INICIADOS </u></b>"))
admin.site.site_title = mark_safe(_("<b><u>Administração da Gestão de Iniciados</u></b>"))
admin.site.index_title = mark_safe(_("<b><u>Bem-vindo ao painel de administração</u></b>"))

from .models import Aluno, Curso, Turma, AtividadeAcademica, AtividadeRitualistica

admin.site.register(Aluno)
admin.site.register(Curso)
admin.site.register(Turma)
admin.site.register(AtividadeAcademica)
admin.site.register(AtividadeRitualistica)