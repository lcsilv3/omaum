from django.db import migrations

def copiar_turma_para_turmas(apps, schema_editor):
    AtividadeAcademica = apps.get_model('atividades', 'AtividadeAcademica')
    
    # Percorrer todas as atividades acadêmicas
    for atividade in AtividadeAcademica.objects.all():
        if atividade.turma:
            # Adicionar a turma atual ao campo turmas
            atividade.turmas.add(atividade.turma)

def reverter_migracao(apps, schema_editor):
    # Não precisamos fazer nada aqui, pois não queremos perder dados
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('atividades', '0003_atividadeacademica_turmas_and_more'),  # Usando a dependência correta da segunda migração
    ]
    
    operations = [
        migrations.RunPython(copiar_turma_para_turmas, reverter_migracao),
    ]
