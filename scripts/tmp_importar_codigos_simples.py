import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.production")
django.setup()

from alunos.models import TipoCodigo, Codigo

CSV_PATH = "/app/scripts/docs/Planilha de Códigos.csv"

tipos_cache = {}
created_tipos = 0
created_codigos = 0

with open(CSV_PATH, encoding='latin1') as f:
    reader = csv.DictReader(f, delimiter=';')
    
    for row in reader:
        tipo_id = row.get('código tipo', '').strip()
        tipo_nome = row.get('Descrição tipo', '').strip()
        codigo_id = row.get('código', '').strip()
        codigo_desc = row.get('Descrição código', '').strip()
        
        if not tipo_id or not tipo_nome or not codigo_id:
            continue
        
        # Criar tipo se não existir
        if tipo_id not in tipos_cache:
            tipo, criado = TipoCodigo.objects.get_or_create(
                id=int(tipo_id),
                defaults={'nome': tipo_nome, 'descricao': tipo_nome}
            )
            tipos_cache[tipo_id] = tipo
            if criado:
                created_tipos += 1
                print(f"Tipo criado: {tipo_id} - {tipo_nome}")
        
        tipo = tipos_cache[tipo_id]
        
        # Criar código
        codigo, criado = Codigo.objects.get_or_create(
            id=int(codigo_id),
            defaults={
                'tipo_codigo': tipo,
                'nome': codigo_desc,
                'descricao': codigo_desc
            }
        )
        if criado:
            created_codigos += 1
            if created_codigos <= 10:  # Mostrar apenas os primeiros 10
                print(f"Código criado: {codigo_id} - {codigo_desc} (Tipo: {tipo_nome})")

print(f"\n✅ Resumo:")
print(f"Tipos criados: {created_tipos}")
print(f"Códigos criados: {created_codigos}")
