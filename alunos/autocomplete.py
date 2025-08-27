from django_select2.views import AutoResponseView
from alunos.models import Cidade, Bairro, TipoCodigo, Codigo


class CidadeAutocomplete(AutoResponseView):
    def get_queryset(self):
        qs = Cidade.objects.all().order_by("nome")
        if self.q:
            qs = qs.filter(nome__icontains=self.q)
        return qs


class BairroAutocomplete(AutoResponseView):
    def get_queryset(self):
        qs = Bairro.objects.all().order_by("nome")
        if self.q:
            qs = qs.filter(nome__icontains=self.q)
        return qs


class TipoCodigoAutocomplete(AutoResponseView):
    def get_queryset(self):
        qs = TipoCodigo.objects.all().order_by("nome")
        if self.q:
            qs = qs.filter(nome__icontains=self.q)
        return qs


class CodigoAutocomplete(AutoResponseView):
    def get_queryset(self):
        qs = Codigo.objects.all().order_by("nome")
        tipo_id = self.forwarded.get("tipo_codigo", None)
        if tipo_id:
            qs = qs.filter(tipo_codigo_id=tipo_id)
        if self.q:
            qs = qs.filter(nome__icontains=self.q)
        return qs
