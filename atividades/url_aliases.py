from django.urls import reverse

def listar_atividades_academicas(*args, **kwargs):
    return reverse('atividades:atividade_academica_list', args=args, kwargs=kwargs)

def criar_atividade_academica(*args, **kwargs):
    return reverse('atividades:atividade_academica_create', args=args, kwargs=kwargs)

def detalhar_atividade_academica(*args, **kwargs):
    return reverse('atividades:atividade_academica_detail', args=args, kwargs=kwargs)

def editar_atividade_academica(*args, **kwargs):
    return reverse('atividades:atividade_academica_update', args=args, kwargs=kwargs)

def excluir_atividade_academica(*args, **kwargs):
    return reverse('atividades:atividade_academica_delete', args=args, kwargs=kwargs)

def listar_atividades_ritualisticas(*args, **kwargs):
    return reverse('atividades:atividade_ritualistica_list', args=args, kwargs=kwargs)

def criar_atividade_ritualistica(*args, **kwargs):
    return reverse('atividades:atividade_ritualistica_create', args=args, kwargs=kwargs)

def detalhar_atividade_ritualistica(*args, **kwargs):
    return reverse('atividades:atividade_ritualistica_detail', args=args, kwargs=kwargs)

def editar_atividade_ritualistica(*args, **kwargs):
    return reverse('atividades:atividade_ritualistica_update', args=args, kwargs=kwargs)

def excluir_atividade_ritualistica(*args, **kwargs):
    return reverse('atividades:atividade_ritualistica_delete', args=args, kwargs=kwargs)
