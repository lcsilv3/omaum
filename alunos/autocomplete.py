from django.http import JsonResponse
from django.views import View
from alunos.models import Estado, Cidade, Bairro, TipoCodigo, Codigo


class BaseAutocompleteView(View):
    """View base para autocomplete sem validação de field_id."""
    
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '').strip()
        
        # O ModelSelect2Widget envia os forwards como parâmetros individuais
        # Por exemplo: ?forward=14 ou ?estado_ref=14
        forward_data = {}
        for key, value in request.GET.items():
            if key not in ['q', 'term', 'page', '_']:
                forward_data[key] = value
        
        # Também tenta parse JSON se vier como JSON
        import json
        forward_json = request.GET.get('forward', '')
        if forward_json:
            try:
                parsed = json.loads(forward_json)
                if isinstance(parsed, dict):
                    forward_data.update(parsed)
            except:
                pass
        
        results = self.get_results(q, forward_data)
        
        return JsonResponse({
            'results': results,
            'pagination': {'more': False}
        })
    
    def get_results(self, q, forward_data):
        """Override este método nas subclasses."""
        return []


class EstadoAutocomplete(BaseAutocompleteView):
    def get_results(self, q, forward_data):
        qs = Estado.objects.all().order_by("nome")
        
        if q:
            qs = qs.filter(nome__icontains=q) | qs.filter(codigo__icontains=q)
        
        return [{'id': obj.id, 'text': f"{obj.codigo} - {obj.nome}"} for obj in qs[:20]]


class CidadeAutocomplete(BaseAutocompleteView):
    def get_results(self, q, forward_data):
        import logging
        logger = logging.getLogger(__name__)
        
        qs = Cidade.objects.all().order_by("nome")
        
        # Filtrar por estado se fornecido
        estado_id = forward_data.get("estado_ref") or forward_data.get("forward")
        logger.info(f"CidadeAutocomplete - forward_data: {forward_data}, q: {q}, estado_id: {estado_id}")
        
        if estado_id:
            qs = qs.filter(estado_id=estado_id)
            logger.info(f"CidadeAutocomplete - Filtrando por estado {estado_id}, total: {qs.count()}")
        
        if q:
            qs = qs.filter(nome__icontains=q)
            logger.info(f"CidadeAutocomplete - Filtrando por nome '{q}', total: {qs.count()}")
        
        return [{'id': obj.id, 'text': f"{obj.nome} - {obj.estado.codigo}"} for obj in qs[:20]]


class BairroAutocomplete(BaseAutocompleteView):
    def get_results(self, q, forward_data):
        qs = Bairro.objects.all().order_by("nome")
        
        # Filtrar por cidade se fornecida
        cidade_id = forward_data.get("cidade_ref") or forward_data.get("forward")
        if cidade_id:
            qs = qs.filter(cidade_id=cidade_id)
        
        if q:
            qs = qs.filter(nome__icontains=q)
        
        return [{'id': obj.id, 'text': f"{obj.nome} - {obj.cidade.nome}"} for obj in qs[:20]]


class TipoCodigoAutocomplete(BaseAutocompleteView):
    def get_results(self, q, forward_data):
        qs = TipoCodigo.objects.all().order_by("nome")
        if q:
            qs = qs.filter(nome__icontains=q)
        return [{'id': obj.id, 'text': obj.nome} for obj in qs[:20]]


class CodigoAutocomplete(BaseAutocompleteView):
    def get_results(self, q, forward_data):
        qs = Codigo.objects.all().order_by("nome")
        tipo_id = forward_data.get("tipo_codigo") or forward_data.get("forward")
        if tipo_id:
            qs = qs.filter(tipo_codigo_id=tipo_id)
        if q:
            qs = qs.filter(nome__icontains=q)
        return [{'id': obj.id, 'text': obj.nome} for obj in qs[:20]]
