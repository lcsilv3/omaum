from django.core.management.base import BaseCommand
from importlib import import_module

class Command(BaseCommand):
    help = 'Atualiza o método de pagamento para pagamentos existentes'

    def handle(self, *args, **options):
        # Importar o modelo dinamicamente
        pagamentos_models = import_module("pagamentos.models")
        Pagamento = getattr(pagamentos_models, "Pagamento")
        
        # Verificar se o campo existe
        if not hasattr(Pagamento, 'metodo_pagamento'):
            self.stdout.write(
                self.style.ERROR('O campo metodo_pagamento não existe no modelo Pagamento')
            )
            return
        
        # Atualizar apenas pagamentos com status PAGO que não têm método de pagamento
        pagamentos_pagos = Pagamento.objects.filter(status='PAGO', metodo_pagamento__isnull=True)
        
        # Definir um valor padrão para o método de pagamento
        for pagamento in pagamentos_pagos:
            pagamento.metodo_pagamento = 'OUTRO'  # Ou outro valor padrão
            pagamento.save()
            
        self.stdout.write(
            self.style.SUCCESS(f'Atualizados {pagamentos_pagos.count()} pagamentos')
        )