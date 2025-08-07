# PLANO DE IMPLEMENTAÇÃO: MELHORIAS SISTEMA DE PRESENÇAS v2.0

**Data de Criação:** 06 de agosto de 2025  
**Responsável:** Desenvolvimento OMAUM  
**Branch de Trabalho:** `refatoracao-alunos-performance`  
**Status:** 📋 PLANEJAMENTO  

---

## 🎯 OBJETIVOS DO PLANO

Implementar melhorias prioritárias no sistema de marcação de presenças com foco em:
- ✅ **Auditoria e Compliance**
- 🔒 **Controle de Acesso Granular**
- ⏰ **Controle Temporal de Alterações**
- 💡 **Experiência do Usuário Melhorada**

---

## 📊 ESCOPO DO PROJETO

### 🔴 **ALTA PRIORIDADE** (Semanas 1-3)
1. Sistema de Auditoria Completo (PresencaHistorico)
2. Permissões Granulares para Alteração/Exclusão
3. Janela Temporal para Alterações
4. Feedback Visual Melhorado no Frontend

### 🟡 **MÉDIA PRIORIDADE** (Semanas 4-5)
5. Soft Delete em vez de Exclusão Física
6. Motivo Obrigatório para Alterações/Exclusões
7. Relatórios de Auditoria para Gestores

---

## 🗓️ CRONOGRAMA DETALHADO

### **SEMANA 1: Fundação - Sistema de Auditoria**

#### **Dia 1-2: Modelo de Auditoria**
```python
# 📁 presencas/models.py
class PresencaHistorico(models.Model):
    """Audit trail para mudanças de presença"""
    presenca_original = models.ForeignKey(Presenca, on_delete=models.CASCADE, related_name='historico')
    acao = models.CharField(max_length=10, choices=[
        ('CREATE', 'Criação'),
        ('UPDATE', 'Alteração'), 
        ('DELETE', 'Exclusão')
    ])
    dados_anteriores = models.JSONField(null=True, blank=True)
    dados_novos = models.JSONField(null=True, blank=True)
    usuario = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Histórico de Presença'
        verbose_name_plural = 'Históricos de Presenças'
```

**📋 Tarefas:**
- [ ] Criar modelo `PresencaHistorico`
- [ ] Gerar e executar migração
- [ ] Adicionar `related_name='historico'` ao modelo `Presenca`
- [ ] Criar testes unitários para o modelo
- [ ] Documentar estrutura de dados

#### **Dia 3-4: Signals para Auditoria Automática**
```python
# 📁 presencas/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.serializers import serialize
import json

@receiver(post_save, sender=Presenca)
def presenca_post_save(sender, instance, created, **kwargs):
    """Signal para capturar criação/atualização de presença"""
    acao = 'CREATE' if created else 'UPDATE'
    
    # Obter dados anteriores do cache se for UPDATE
    dados_anteriores = getattr(instance, '_dados_anteriores', None)
    
    PresencaHistorico.objects.create(
        presenca_original=instance,
        acao=acao,
        dados_anteriores=dados_anteriores,
        dados_novos=model_to_dict(instance),
        usuario=getattr(instance, '_usuario_atual', 'sistema'),
        motivo=getattr(instance, '_motivo_alteracao', ''),
        ip_address=getattr(instance, '_ip_address', None),
        user_agent=getattr(instance, '_user_agent', '')
    )
```

**📋 Tarefas:**
- [ ] Criar arquivo `presencas/signals.py`
- [ ] Implementar signals para CREATE/UPDATE/DELETE
- [ ] Conectar signals no `apps.py`
- [ ] Implementar sistema de cache para dados anteriores
- [ ] Criar middleware para capturar IP/User-Agent
- [ ] Testes de integração para signals

#### **Dia 5: Middleware de Contexto**
```python
# 📁 presencas/middleware.py
class AuditoriaMiddleware:
    """Middleware para capturar contexto de auditoria"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Armazenar contexto no thread local
        _audit_context.usuario = getattr(request.user, 'username', 'anonimo')
        _audit_context.ip_address = self.get_client_ip(request)
        _audit_context.user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        response = self.get_response(request)
        return response
```

**📋 Tarefas:**
- [ ] Criar middleware de auditoria
- [ ] Implementar thread-local storage
- [ ] Configurar middleware no settings
- [ ] Testes do middleware

---

### **SEMANA 2: Controle de Acesso e Permissões Granulares**

#### **Dia 1-2: Sistema de Permissões Customizadas**

##### **📊 MATRIZ DE PERMISSÕES DETALHADA**

```python
# 📁 presencas/models.py - Adicionar ao modelo Presenca
class Meta:
    permissions = [
        # === PERMISSÕES DE VISUALIZAÇÃO ===
        ('can_view_own_presenca', 'Pode visualizar próprias presenças'),
        ('can_view_turma_presenca', 'Pode visualizar presenças da turma'),
        ('can_view_any_presenca', 'Pode visualizar qualquer presença'),
        ('can_view_presenca_details', 'Pode ver detalhes completos de presença'),
        
        # === PERMISSÕES DE CRIAÇÃO ===
        ('can_create_presenca_turma', 'Pode criar presenças para sua turma'),
        ('can_create_presenca_any', 'Pode criar presenças para qualquer turma'),
        ('can_bulk_create_presenca', 'Pode criar presenças em lote'),
        
        # === PERMISSÕES DE EDIÇÃO ===
        ('can_edit_own_presenca', 'Pode editar próprias presenças'),
        ('can_edit_recent_presenca', 'Pode editar presenças recentes (7 dias)'),
        ('can_edit_any_presenca', 'Pode editar qualquer presença'),
        ('can_edit_presenca_beyond_deadline', 'Pode editar após prazo normal'),
        ('can_bulk_edit_presenca', 'Pode editar presenças em lote'),
        
        # === PERMISSÕES DE EXCLUSÃO ===
        ('can_delete_own_presenca', 'Pode excluir próprias presenças'),
        ('can_delete_recent_presenca', 'Pode excluir presenças recentes (24h)'),
        ('can_delete_any_presenca', 'Pode excluir qualquer presença'),
        ('can_restore_deleted_presenca', 'Pode restaurar presenças excluídas'),
        
        # === PERMISSÕES DE AUDITORIA ===
        ('can_view_audit_trail', 'Pode visualizar trilha de auditoria'),
        ('can_view_full_audit_details', 'Pode ver detalhes completos de auditoria'),
        ('can_export_audit_reports', 'Pode exportar relatórios de auditoria'),
        
        # === PERMISSÕES ADMINISTRATIVAS ===
        ('can_override_business_rules', 'Pode ignorar regras de negócio'),
        ('can_manage_presenca_settings', 'Pode gerenciar configurações do sistema'),
        ('can_access_admin_dashboard', 'Pode acessar dashboard administrativo'),
    ]

# 📁 presencas/models.py - Modelo de Configuração de Permissões
class PresencaConfiguracao(models.Model):
    """Configurações globais para controle de presenças"""
    
    # Janelas temporais
    dias_limite_edicao = models.PositiveIntegerField(
        default=7, 
        help_text="Dias após criação que presença pode ser editada"
    )
    horas_limite_exclusao = models.PositiveIntegerField(
        default=24,
        help_text="Horas após criação que presença pode ser excluída"
    )
    
    # Regras de validação
    motivo_obrigatorio_edicao = models.BooleanField(
        default=True,
        help_text="Exigir motivo para editar presença"
    )
    motivo_obrigatorio_exclusao = models.BooleanField(
        default=True,
        help_text="Exigir motivo para excluir presença"
    )
    
    # Configurações de segurança
    max_alteracoes_por_dia = models.PositiveIntegerField(
        default=50,
        help_text="Máximo de alterações por usuário por dia"
    )
    bloquear_edicao_finalizadas = models.BooleanField(
        default=True,
        help_text="Bloquear edição de presenças finalizadas"
    )
    
    # Configurações de auditoria
    manter_historico_dias = models.PositiveIntegerField(
        default=365,
        help_text="Dias para manter histórico de auditoria"
    )
    
    class Meta:
        verbose_name = 'Configuração de Presença'
        verbose_name_plural = 'Configurações de Presenças'
```

##### **👥 GRUPOS DE USUÁRIOS E PERFIS**

```python
# 📁 presencas/management/commands/setup_permissions.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from presencas.models import Presenca

class Command(BaseCommand):
    help = 'Configura grupos e permissões padrão para o sistema de presenças'
    
    def handle(self, *args, **options):
        self.create_permission_groups()
        self.stdout.write(
            self.style.SUCCESS('Grupos e permissões configurados com sucesso!')
        )
    
    def create_permission_groups(self):
        """Cria grupos padrão com suas respectivas permissões"""
        
        # === GRUPO: ALUNO ===
        aluno_group, created = Group.objects.get_or_create(name='Aluno')
        aluno_permissions = [
            'can_view_own_presenca',
            'can_view_presenca_details',
        ]
        self.assign_permissions(aluno_group, aluno_permissions)
        
        # === GRUPO: MONITOR ===
        monitor_group, created = Group.objects.get_or_create(name='Monitor')
        monitor_permissions = [
            'can_view_own_presenca',
            'can_view_turma_presenca',
            'can_view_presenca_details',
            'can_create_presenca_turma',
            'can_edit_own_presenca',
            'can_edit_recent_presenca',
        ]
        self.assign_permissions(monitor_group, monitor_permissions)
        
        # === GRUPO: PROFESSOR ===
        professor_group, created = Group.objects.get_or_create(name='Professor')
        professor_permissions = [
            'can_view_turma_presenca',
            'can_view_presenca_details',
            'can_create_presenca_turma',
            'can_bulk_create_presenca',
            'can_edit_own_presenca',
            'can_edit_recent_presenca',
            'can_bulk_edit_presenca',
            'can_delete_own_presenca',
            'can_delete_recent_presenca',
            'can_view_audit_trail',
        ]
        self.assign_permissions(professor_group, professor_permissions)
        
        # === GRUPO: COORDENADOR ===
        coordenador_group, created = Group.objects.get_or_create(name='Coordenador')
        coordenador_permissions = [
            'can_view_any_presenca',
            'can_view_presenca_details',
            'can_create_presenca_any',
            'can_bulk_create_presenca',
            'can_edit_any_presenca',
            'can_edit_presenca_beyond_deadline',
            'can_bulk_edit_presenca',
            'can_delete_any_presenca',
            'can_restore_deleted_presenca',
            'can_view_audit_trail',
            'can_view_full_audit_details',
            'can_export_audit_reports',
        ]
        self.assign_permissions(coordenador_group, coordenador_permissions)
        
        # === GRUPO: ADMINISTRADOR ===
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        admin_permissions = [
            # Todas as permissões
            'can_view_any_presenca',
            'can_view_presenca_details',
            'can_create_presenca_any',
            'can_bulk_create_presenca',
            'can_edit_any_presenca',
            'can_edit_presenca_beyond_deadline',
            'can_bulk_edit_presenca',
            'can_delete_any_presenca',
            'can_restore_deleted_presenca',
            'can_view_audit_trail',
            'can_view_full_audit_details',
            'can_export_audit_reports',
            'can_override_business_rules',
            'can_manage_presenca_settings',
            'can_access_admin_dashboard',
        ]
        self.assign_permissions(admin_group, admin_permissions)
    
    def assign_permissions(self, group, permission_names):
        """Atribui permissões específicas a um grupo"""
        content_type = ContentType.objects.get_for_model(Presenca)
        
        for perm_name in permission_names:
            try:
                permission = Permission.objects.get(
                    codename=perm_name,
                    content_type=content_type
                )
                group.permissions.add(permission)
                self.stdout.write(f'✓ {perm_name} → {group.name}')
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Permissão não encontrada: {perm_name}')
                )
```

**📋 Tarefas Dia 1-2:**
- [ ] Adicionar 20+ permissões customizadas detalhadas
- [ ] Criar modelo `PresencaConfiguracao` para settings dinâmicos
- [ ] Implementar command para setup automático de grupos
- [ ] Gerar migração para as novas permissões
- [ ] Criar matriz de permissões por papel (documento)
- [ ] Configurar permissões no Django Admin
- [ ] Testes unitários para cada grupo de permissões

#### **Dia 3-4: Sistema Avançado de Regras de Negócio**

##### **🔒 ENGINE DE PERMISSÕES CONTEXTUAL**

```python
# 📁 presencas/permissions.py
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from typing import Tuple, Dict, List
import logging

logger = logging.getLogger(__name__)

class PresencaPermissionEngine:
    """
    Engine avançado para verificação de permissões contextuais.
    Considera múltiplos fatores: tempo, ownership, hierarquia, regras específicas.
    """
    
    @classmethod
    def pode_visualizar_presenca(cls, presenca, usuario) -> Tuple[bool, str]:
        """Verifica se usuário pode visualizar presença específica"""
        
        # REGRA 1: Superusuário sempre pode
        if usuario.is_superuser:
            return True, "Superusuário - acesso total"
        
        # REGRA 2: Própria presença (se for aluno)
        if hasattr(usuario, 'aluno') and presenca.aluno == usuario.aluno:
            if usuario.has_perm('presencas.can_view_own_presenca'):
                return True, "Visualizando própria presença"
            return False, "Sem permissão para visualizar próprias presenças"
        
        # REGRA 3: Professor da turma
        if cls._is_professor_da_turma(usuario, presenca.turma):
            if usuario.has_perm('presencas.can_view_turma_presenca'):
                return True, "Professor da turma"
            return False, "Professor sem permissão para visualizar presenças da turma"
        
        # REGRA 4: Permissão global
        if usuario.has_perm('presencas.can_view_any_presenca'):
            return True, "Permissão global de visualização"
        
        return False, "Sem permissão para visualizar esta presença"
    
    @classmethod
    def pode_alterar_presenca(cls, presenca, usuario) -> Tuple[bool, str]:
        """Verifica se usuário pode alterar presença específica"""
        
        # REGRA 1: Verificação básica de visualização
        pode_ver, motivo_ver = cls.pode_visualizar_presenca(presenca, usuario)
        if not pode_ver:
            return False, f"Sem acesso para visualizar: {motivo_ver}"
        
        # REGRA 2: Presença já excluída (soft delete)
        if hasattr(presenca, 'excluida') and presenca.excluida:
            if not usuario.has_perm('presencas.can_restore_deleted_presenca'):
                return False, "Presença excluída não pode ser alterada"
        
        # REGRA 3: Status finalizada
        if hasattr(presenca, 'status') and presenca.status == 'FINALIZADA':
            config = cls._get_configuracao()
            if config.bloquear_edicao_finalizadas:
                if not usuario.has_perm('presencas.can_override_business_rules'):
                    return False, "Presença finalizada não pode ser alterada"
        
        # REGRA 4: Janela temporal
        pode_por_tempo, motivo_tempo = cls._verificar_janela_temporal_edicao(presenca, usuario)
        if not pode_por_tempo:
            return False, motivo_tempo
        
        # REGRA 5: Ownership e permissões
        return cls._verificar_permissao_edicao(presenca, usuario)
    
    @classmethod
    def pode_excluir_presenca(cls, presenca, usuario) -> Tuple[bool, str]:
        """Verifica se usuário pode excluir presença específica"""
        
        # REGRA 1: Verificação básica de alteração
        pode_alterar, motivo_alterar = cls.pode_alterar_presenca(presenca, usuario)
        if not pode_alterar:
            return False, f"Não pode excluir: {motivo_alterar}"
        
        # REGRA 2: Janela temporal mais restrita para exclusão
        pode_por_tempo, motivo_tempo = cls._verificar_janela_temporal_exclusao(presenca, usuario)
        if not pode_por_tempo:
            return False, motivo_tempo
        
        # REGRA 3: Permissões específicas de exclusão
        return cls._verificar_permissao_exclusao(presenca, usuario)
    
    @classmethod
    def pode_criar_presenca_para_turma(cls, turma, usuario) -> Tuple[bool, str]:
        """Verifica se usuário pode criar presença para turma específica"""
        
        # REGRA 1: Superusuário
        if usuario.is_superuser:
            return True, "Superusuário - acesso total"
        
        # REGRA 2: Professor da turma
        if cls._is_professor_da_turma(usuario, turma):
            if usuario.has_perm('presencas.can_create_presenca_turma'):
                return True, "Professor da turma"
            return False, "Professor sem permissão para criar presenças"
        
        # REGRA 3: Permissão global
        if usuario.has_perm('presencas.can_create_presenca_any'):
            return True, "Permissão global de criação"
        
        return False, "Sem permissão para criar presenças nesta turma"
    
    @classmethod
    def verificar_limite_alteracoes_diarias(cls, usuario) -> Tuple[bool, str]:
        """Verifica se usuário não excedeu limite de alterações diárias"""
        
        if usuario.has_perm('presencas.can_override_business_rules'):
            return True, "Usuário pode ignorar regras de negócio"
        
        config = cls._get_configuracao()
        hoje = timezone.now().date()
        
        # Chave do cache para contagem
        cache_key = f"presenca_alteracoes_{usuario.id}_{hoje}"
        alteracoes_hoje = cache.get(cache_key, 0)
        
        if alteracoes_hoje >= config.max_alteracoes_por_dia:
            return False, f"Limite diário de {config.max_alteracoes_por_dia} alterações excedido"
        
        return True, f"Alterações hoje: {alteracoes_hoje}/{config.max_alteracoes_por_dia}"
    
    # === MÉTODOS AUXILIARES PRIVADOS ===
    
    @classmethod
    def _verificar_janela_temporal_edicao(cls, presenca, usuario) -> Tuple[bool, str]:
        """Verifica janela temporal para edição"""
        config = cls._get_configuracao()
        limite = timezone.now() - timedelta(days=config.dias_limite_edicao)
        
        if presenca.data_registro < limite:
            # Fora da janela normal
            if usuario.has_perm('presencas.can_edit_presenca_beyond_deadline'):
                return True, f"Edição após prazo (permitida para usuário privilegiado)"
            elif usuario.has_perm('presencas.can_edit_any_presenca'):
                return True, f"Edição após prazo (permissão global)"
            else:
                dias_passados = (timezone.now() - presenca.data_registro).days
                return False, f"Período de edição expirado ({dias_passados} dias). Limite: {config.dias_limite_edicao} dias"
        
        return True, "Dentro da janela temporal de edição"
    
    @classmethod
    def _verificar_janela_temporal_exclusao(cls, presenca, usuario) -> Tuple[bool, str]:
        """Verifica janela temporal para exclusão (mais restrita)"""
        config = cls._get_configuracao()
        limite = timezone.now() - timedelta(hours=config.horas_limite_exclusao)
        
        if presenca.data_registro < limite:
            # Fora da janela normal
            if usuario.has_perm('presencas.can_delete_any_presenca'):
                return True, f"Exclusão após prazo (permissão global)"
            else:
                horas_passadas = (timezone.now() - presenca.data_registro).total_seconds() / 3600
                return False, f"Período de exclusão expirado ({horas_passadas:.1f} horas). Limite: {config.horas_limite_exclusao} horas"
        
        return True, "Dentro da janela temporal de exclusão"
    
    @classmethod
    def _verificar_permissao_edicao(cls, presenca, usuario) -> Tuple[bool, str]:
        """Verifica permissões específicas de edição"""
        
        # Próprio registro
        if presenca.registrado_por == usuario.username:
            if usuario.has_perm('presencas.can_edit_own_presenca'):
                return True, "Editando próprio registro"
            return False, "Sem permissão para editar próprios registros"
        
        # Registro de outros
        if usuario.has_perm('presencas.can_edit_any_presenca'):
            return True, "Permissão para editar qualquer presença"
        
        # Professor da turma
        if cls._is_professor_da_turma(usuario, presenca.turma):
            if usuario.has_perm('presencas.can_edit_recent_presenca'):
                return True, "Professor editando presença da turma"
        
        return False, "Sem permissão para editar presenças de outros usuários"
    
    @classmethod
    def _verificar_permissao_exclusao(cls, presenca, usuario) -> Tuple[bool, str]:
        """Verifica permissões específicas de exclusão"""
        
        # Próprio registro
        if presenca.registrado_por == usuario.username:
            if usuario.has_perm('presencas.can_delete_own_presenca'):
                return True, "Excluindo próprio registro"
            return False, "Sem permissão para excluir próprios registros"
        
        # Registro de outros - só administradores
        if usuario.has_perm('presencas.can_delete_any_presenca'):
            return True, "Permissão para excluir qualquer presença"
        
        return False, "Apenas administradores podem excluir presenças de outros usuários"
    
    @classmethod
    def _is_professor_da_turma(cls, usuario, turma) -> bool:
        """Verifica se usuário é professor da turma"""
        # Implementar lógica específica do seu sistema
        # Exemplo: verificar se usuario.professor.turmas.filter(id=turma.id).exists()
        return hasattr(usuario, 'professor') and \
               usuario.professor.turmas.filter(id=turma.id).exists()
    
    @classmethod
    def _get_configuracao(cls):
        """Obtém configuração atual do sistema (com cache)"""
        config = cache.get('presenca_configuracao')
        if not config:
            from .models import PresencaConfiguracao
            config = PresencaConfiguracao.objects.first()
            if not config:
                # Criar configuração padrão
                config = PresencaConfiguracao.objects.create()
            cache.set('presenca_configuracao', config, 300)  # 5 minutos
        return config
    
    @classmethod
    def incrementar_contador_alteracoes(cls, usuario):
        """Incrementa contador de alterações diárias"""
        hoje = timezone.now().date()
        cache_key = f"presenca_alteracoes_{usuario.id}_{hoje}"
        
        alteracoes_hoje = cache.get(cache_key, 0)
        cache.set(cache_key, alteracoes_hoje + 1, 86400)  # 24 horas
        
        logger.info(f"Alteração registrada para {usuario.username}: {alteracoes_hoje + 1}")

# Alias para compatibilidade
PresencaPermissions = PresencaPermissionEngine
```

##### **🔧 DECORATORS AVANÇADOS**

```python
# 📁 presencas/decorators.py
from functools import wraps
from django.http import JsonResponse, Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from .permissions import PresencaPermissionEngine
from .models import Presenca, Turma

def require_presenca_permission(permission_type, lookup_field='pk'):
    """
    Decorator avançado para verificar permissões de presença.
    
    Args:
        permission_type: 'view', 'edit', 'delete', 'create'
        lookup_field: Campo para buscar a presença ('pk', 'id', etc.)
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            
            if permission_type == 'create':
                # Para criação, verificar permissão na turma
                turma_id = request.POST.get('turma') or request.GET.get('turma')
                if turma_id:
                    turma = get_object_or_404(Turma, id=turma_id)
                    pode, motivo = PresencaPermissionEngine.pode_criar_presenca_para_turma(
                        turma, request.user
                    )
                    if not pode:
                        return _handle_permission_denied(request, motivo)
            
            else:
                # Para outras operações, verificar na presença específica
                presenca_id = kwargs.get(lookup_field)
                if presenca_id:
                    presenca = get_object_or_404(Presenca, pk=presenca_id)
                    
                    # Verificar limite de alterações diárias
                    if permission_type in ['edit', 'delete']:
                        pode_alterar, motivo_limite = PresencaPermissionEngine.verificar_limite_alteracoes_diarias(
                            request.user
                        )
                        if not pode_alterar:
                            return _handle_permission_denied(request, motivo_limite)
                    
                    # Verificar permissão específica
                    if permission_type == 'view':
                        pode, motivo = PresencaPermissionEngine.pode_visualizar_presenca(
                            presenca, request.user
                        )
                    elif permission_type == 'edit':
                        pode, motivo = PresencaPermissionEngine.pode_alterar_presenca(
                            presenca, request.user
                        )
                    elif permission_type == 'delete':
                        pode, motivo = PresencaPermissionEngine.pode_excluir_presenca(
                            presenca, request.user
                        )
                    
                    if not pode:
                        return _handle_permission_denied(request, motivo)
                    
                    # Adicionar presença ao request para uso na view
                    request.presenca = presenca
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def _handle_permission_denied(request, motivo):
    """Trata negação de permissão de forma consistente"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'error': True,
            'message': motivo,
            'code': 'PERMISSION_DENIED'
        }, status=403)
    
    messages.error(request, f"Acesso negado: {motivo}")
    return redirect('presencas:listar_presencas_academicas')

# === DECORATORS ESPECÍFICOS ===

def require_view_presenca_permission(view_func):
    """Shortcut para verificar permissão de visualização"""
    return require_presenca_permission('view')(view_func)

def require_edit_presenca_permission(view_func):
    """Shortcut para verificar permissão de edição"""
    return require_presenca_permission('edit')(view_func)

def require_delete_presenca_permission(view_func):
    """Shortcut para verificar permissão de exclusão"""
    return require_presenca_permission('delete')(view_func)

def require_create_presenca_permission(view_func):
    """Shortcut para verificar permissão de criação"""
    return require_presenca_permission('create')(view_func)

def require_bulk_operation_permission(view_func):
    """Decorator para operações em lote"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.has_perm('presencas.can_bulk_edit_presenca'):
            return _handle_permission_denied(
                request, 
                "Sem permissão para operações em lote"
            )
        
        # Verificar limite de alterações diárias (multiplicado por 5 para lote)
        pode, motivo = PresencaPermissionEngine.verificar_limite_alteracoes_diarias(request.user)
        if not pode:
            return _handle_permission_denied(request, f"Operação em lote bloqueada: {motivo}")
        
        return view_func(request, *args, **kwargs)
    return wrapper
```

**📋 Tarefas Dia 3-4:**
- [ ] Implementar engine de permissões contextual completo
- [ ] Criar 15+ regras de negócio específicas
- [ ] Implementar verificação de janela temporal dinâmica
- [ ] Criar sistema de limite de alterações diárias
- [ ] Implementar decorators avançados para views
- [ ] Adicionar cache para performance das verificações
- [ ] Criar logs detalhados de verificações de permissão
- [ ] Testes unitários para cada regra de negócio
- [ ] Testes de edge cases e cenários complexos

#### **Dia 5: Integração Avançada com Views e Context Processors**

##### **🎯 VIEWS COM CONTROLE DE ACESSO INTEGRADO**

```python
# 📁 presencas/views_permissions.py
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import *
from .permissions import PresencaPermissionEngine

class PresencaListViewWithPermissions(LoginRequiredMixin, ListView):
    """ListView com filtros de permissão integrados"""
    model = Presenca
    template_name = 'presencas/listar_presencas.html'
    paginate_by = 25
    
    def get_queryset(self):
        """Filtra queryset baseado nas permissões do usuário"""
        user = self.request.user
        
        # Superusuário vê tudo
        if user.is_superuser:
            return Presenca.objects.all()
        
        # Filtrar baseado nas permissões
        if user.has_perm('presencas.can_view_any_presenca'):
            return Presenca.objects.all()
        
        elif user.has_perm('presencas.can_view_turma_presenca'):
            # Professor vê apenas suas turmas
            if hasattr(user, 'professor'):
                return Presenca.objects.filter(
                    turma__in=user.professor.turmas.all()
                )
        
        elif user.has_perm('presencas.can_view_own_presenca'):
            # Aluno vê apenas suas presenças
            if hasattr(user, 'aluno'):
                return Presenca.objects.filter(aluno=user.aluno)
        
        # Sem permissão, retorna queryset vazio
        return Presenca.objects.none()
    
    def get_context_data(self, **kwargs):
        """Adiciona informações de permissão ao contexto"""
        context = super().get_context_data(**kwargs)
        
        # Adicionar permissões do usuário atual
        context['user_permissions'] = {
            'can_create': self.request.user.has_perm('presencas.can_create_presenca_any'),
            'can_bulk_edit': self.request.user.has_perm('presencas.can_bulk_edit_presenca'),
            'can_export': self.request.user.has_perm('presencas.can_export_audit_reports'),
            'can_view_audit': self.request.user.has_perm('presencas.can_view_audit_trail'),
        }
        
        # Estatísticas baseadas no que o usuário pode ver
        queryset = self.get_queryset()
        context['stats'] = {
            'total_presencas': queryset.count(),
            'presencas_hoje': queryset.filter(data=timezone.now().date()).count(),
            'presencas_semana': queryset.filter(
                data__gte=timezone.now().date() - timedelta(days=7)
            ).count(),
        }
        
        return context

@login_required
@require_view_presenca_permission
def detalhar_presenca_com_permissoes(request, pk):
    """View de detalhamento com verificação de permissões"""
    # A presença já foi verificada e anexada ao request pelo decorator
    presenca = request.presenca
    
    # Verificar permissões específicas para esta presença
    pode_editar, motivo_edicao = PresencaPermissionEngine.pode_alterar_presenca(
        presenca, request.user
    )
    pode_excluir, motivo_exclusao = PresencaPermissionEngine.pode_excluir_presenca(
        presenca, request.user
    )
    pode_ver_audit, _ = (True, "") if request.user.has_perm('presencas.can_view_audit_trail') else (False, "")
    
    context = {
        'presenca': presenca,
        'pode_editar': pode_editar,
        'motivo_edicao': motivo_edicao if not pode_editar else None,
        'pode_excluir': pode_excluir,
        'motivo_exclusao': motivo_exclusao if not pode_excluir else None,
        'pode_ver_auditoria': pode_ver_audit,
        'historico': presenca.historico.all()[:10] if pode_ver_audit else [],
        'limite_alteracao': presenca.data_registro + timedelta(
            days=PresencaPermissionEngine._get_configuracao().dias_limite_edicao
        ),
        'limite_exclusao': presenca.data_registro + timedelta(
            hours=PresencaPermissionEngine._get_configuracao().horas_limite_exclusao
        ),
    }
    
    return render(request, 'presencas/detalhar_presenca.html', context)

@login_required
@require_edit_presenca_permission
def editar_presenca_com_permissoes(request, pk):
    """View de edição com todas as verificações de permissão"""
    presenca = request.presenca  # Já verificada pelo decorator
    
    if request.method == 'POST':
        form = EditarPresencaForm(
            request.POST, 
            instance=presenca, 
            usuario=request.user
        )
        
        if form.is_valid():
            # Incrementar contador de alterações
            PresencaPermissionEngine.incrementar_contador_alteracoes(request.user)
            
            # Salvar com contexto de auditoria
            presenca_atualizada = form.save(commit=False)
            presenca_atualizada._usuario_atual = request.user.username
            presenca_atualizada._motivo_alteracao = form.cleaned_data['motivo_alteracao']
            presenca_atualizada._ip_address = get_client_ip(request)
            presenca_atualizada._user_agent = request.META.get('HTTP_USER_AGENT', '')
            presenca_atualizada.save()
            
            messages.success(request, 'Presença alterada com sucesso!')
            return redirect('presencas:detalhar_presenca', pk=presenca.pk)
    
    else:
        form = EditarPresencaForm(instance=presenca, usuario=request.user)
    
    # Verificar se está próximo do limite de alterações
    pode_mais, info_limite = PresencaPermissionEngine.verificar_limite_alteracoes_diarias(request.user)
    
    context = {
        'form': form,
        'presenca': presenca,
        'info_limite': info_limite,
        'proximo_limite': not pode_mais,
    }
    
    return render(request, 'presencas/editar_presenca.html', context)

@login_required
@require_bulk_operation_permission
def bulk_edit_presencas(request):
    """View para edição em lote com permissões"""
    
    if request.method == 'POST':
        presenca_ids = request.POST.getlist('presenca_ids')
        acao = request.POST.get('acao')
        motivo = request.POST.get('motivo_bulk', '')
        
        if not motivo or len(motivo.strip()) < 15:
            messages.error(request, 'Motivo é obrigatório e deve ter pelo menos 15 caracteres')
            return redirect('presencas:listar_presencas_academicas')
        
        # Verificar permissões para cada presença
        presencas_permitidas = []
        presencas_negadas = []
        
        for pk in presenca_ids:
            try:
                presenca = Presenca.objects.get(pk=pk)
                
                if acao == 'edit':
                    pode, motivo_negacao = PresencaPermissionEngine.pode_alterar_presenca(
                        presenca, request.user
                    )
                elif acao == 'delete':
                    pode, motivo_negacao = PresencaPermissionEngine.pode_excluir_presenca(
                        presenca, request.user
                    )
                
                if pode:
                    presencas_permitidas.append(presenca)
                else:
                    presencas_negadas.append(f"{presenca.aluno.nome}: {motivo_negacao}")
                    
            except Presenca.DoesNotExist:
                presencas_negadas.append(f"Presença ID {pk}: não encontrada")
        
        # Executar ação apenas nas presenças permitidas
        if presencas_permitidas:
            if acao == 'edit':
                # Implementar lógica de edição em lote
                pass
            elif acao == 'delete':
                for presenca in presencas_permitidas:
                    presenca.soft_delete(request.user.username, motivo)
                    PresencaPermissionEngine.incrementar_contador_alteracoes(request.user)
        
        # Feedback ao usuário
        if presencas_permitidas:
            messages.success(
                request, 
                f'{len(presencas_permitidas)} presenças processadas com sucesso'
            )
        
        if presencas_negadas:
            messages.warning(
                request,
                f'{len(presencas_negadas)} presenças não puderam ser processadas'
            )
    
    return redirect('presencas:listar_presencas_academicas')
```

##### **🔧 CONTEXT PROCESSORS E MIDDLEWARE**

```python
# 📁 presencas/context_processors.py
from .permissions import PresencaPermissionEngine

def presenca_permissions(request):
    """Context processor que adiciona permissões de presença em todos os templates"""
    
    if not request.user.is_authenticated:
        return {}
    
    # Cache das permissões do usuário para evitar múltiplas verificações
    user_permissions = {
        # Visualização
        'can_view_own_presenca': request.user.has_perm('presencas.can_view_own_presenca'),
        'can_view_turma_presenca': request.user.has_perm('presencas.can_view_turma_presenca'),
        'can_view_any_presenca': request.user.has_perm('presencas.can_view_any_presenca'),
        'can_view_audit_trail': request.user.has_perm('presencas.can_view_audit_trail'),
        
        # Criação
        'can_create_presenca_turma': request.user.has_perm('presencas.can_create_presenca_turma'),
        'can_create_presenca_any': request.user.has_perm('presencas.can_create_presenca_any'),
        'can_bulk_create_presenca': request.user.has_perm('presencas.can_bulk_create_presenca'),
        
        # Edição
        'can_edit_own_presenca': request.user.has_perm('presencas.can_edit_own_presenca'),
        'can_edit_any_presenca': request.user.has_perm('presencas.can_edit_any_presenca'),
        'can_bulk_edit_presenca': request.user.has_perm('presencas.can_bulk_edit_presenca'),
        
        # Exclusão
        'can_delete_own_presenca': request.user.has_perm('presencas.can_delete_own_presenca'),
        'can_delete_any_presenca': request.user.has_perm('presencas.can_delete_any_presenca'),
        'can_restore_deleted_presenca': request.user.has_perm('presencas.can_restore_deleted_presenca'),
        
        # Administrativo
        'can_override_business_rules': request.user.has_perm('presencas.can_override_business_rules'),
        'can_export_audit_reports': request.user.has_perm('presencas.can_export_audit_reports'),
        'can_access_admin_dashboard': request.user.has_perm('presencas.can_access_admin_dashboard'),
    }
    
    # Informações de limite de alterações
    pode_alterar, info_limite = PresencaPermissionEngine.verificar_limite_alteracoes_diarias(request.user)
    
    # Configurações do sistema
    config = PresencaPermissionEngine._get_configuracao()
    
    return {
        'presenca_perms': user_permissions,
        'presenca_limite_info': {
            'pode_alterar': pode_alterar,
            'info': info_limite,
            'limite_edicao_dias': config.dias_limite_edicao,
            'limite_exclusao_horas': config.horas_limite_exclusao,
        },
        'is_presenca_admin': request.user.has_perm('presencas.can_access_admin_dashboard'),
    }

# 📁 presencas/middleware.py
class PresencaPermissionMiddleware:
    """Middleware para adicionar informações de permissão nas requisições"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Adicionar helper de permissões ao request
        if request.user.is_authenticated:
            request.can_presenca = PresencaPermissionHelper(request.user)
        
        response = self.get_response(request)
        return response

class PresencaPermissionHelper:
    """Helper para verificações rápidas de permissão"""
    
    def __init__(self, user):
        self.user = user
        self.engine = PresencaPermissionEngine
    
    def pode_ver(self, presenca):
        """Verifica se pode visualizar presença"""
        pode, _ = self.engine.pode_visualizar_presenca(presenca, self.user)
        return pode
    
    def pode_editar(self, presenca):
        """Verifica se pode editar presença"""
        pode, _ = self.engine.pode_alterar_presenca(presenca, self.user)
        return pode
    
    def pode_excluir(self, presenca):
        """Verifica se pode excluir presença"""
        pode, _ = self.engine.pode_excluir_presenca(presenca, self.user)
        return pode
    
    def pode_criar_em_turma(self, turma):
        """Verifica se pode criar presença na turma"""
        pode, _ = self.engine.pode_criar_presenca_para_turma(turma, self.user)
        return pode
```

##### **📱 TEMPLATE TAGS CUSTOMIZADOS**

```python
# 📁 presencas/templatetags/presenca_permissions.py
from django import template
from ..permissions import PresencaPermissionEngine

register = template.Library()

@register.simple_tag
def can_edit_presenca(user, presenca):
    """Template tag para verificar se pode editar presença"""
    pode, _ = PresencaPermissionEngine.pode_alterar_presenca(presenca, user)
    return pode

@register.simple_tag
def can_delete_presenca(user, presenca):
    """Template tag para verificar se pode excluir presença"""
    pode, _ = PresencaPermissionEngine.pode_excluir_presenca(presenca, user)
    return pode

@register.simple_tag
def permission_reason(user, presenca, action):
    """Retorna o motivo da permissão/negação"""
    if action == 'edit':
        _, motivo = PresencaPermissionEngine.pode_alterar_presenca(presenca, user)
    elif action == 'delete':
        _, motivo = PresencaPermissionEngine.pode_excluir_presenca(presenca, user)
    elif action == 'view':
        _, motivo = PresencaPermissionEngine.pode_visualizar_presenca(presenca, user)
    else:
        motivo = "Ação inválida"
    
    return motivo

@register.inclusion_tag('presencas/includes/permission_badge.html')
def permission_badge(user, presenca, action):
    """Renderiza badge de permissão"""
    
    if action == 'edit':
        pode, motivo = PresencaPermissionEngine.pode_alterar_presenca(presenca, user)
        icon = 'fa-edit'
        color = 'success' if pode else 'danger'
    elif action == 'delete':
        pode, motivo = PresencaPermissionEngine.pode_excluir_presenca(presenca, user)
        icon = 'fa-trash'
        color = 'success' if pode else 'danger'
    elif action == 'view':
        pode, motivo = PresencaPermissionEngine.pode_visualizar_presenca(presenca, user)
        icon = 'fa-eye'
        color = 'success' if pode else 'danger'
    
    return {
        'pode': pode,
        'motivo': motivo,
        'icon': icon,
        'color': color,
        'action': action
    }

@register.filter
def has_presenca_perm(user, permission):
    """Filter para verificar permissão específica"""
    return user.has_perm(f'presencas.{permission}')
```

**📋 Tarefas Dia 5:**
- [ ] Implementar views com controle de acesso integrado
- [ ] Criar context processor para permissões globais
- [ ] Implementar middleware de helper de permissões
- [ ] Criar template tags customizados para verificações
- [ ] Atualizar templates existentes com novas verificações
- [ ] Implementar sistema de badges de permissão
- [ ] Criar helper classes para uso em templates
- [ ] Testes de integração completos
- [ ] Documentação de uso das novas funcionalidades

---

### **SEMANA 3: Interface de Usuário e Feedback Visual**

#### **Dia 1-2: Templates com Histórico de Auditoria**
```html
<!-- 📁 presencas/templates/presencas/includes/historico_presenca.html -->
<div class="card mt-3" id="historico-presenca">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h6 class="mb-0">
            <i class="fas fa-history text-info"></i>
            Histórico de Alterações
        </h6>
        <span class="badge badge-info">{{ presenca.historico.count }} registro(s)</span>
    </div>
    
    {% if presenca.historico.exists %}
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-sm table-hover mb-0">
                <thead class="thead-light">
                    <tr>
                        <th width="15%">Data/Hora</th>
                        <th width="15%">Usuário</th>
                        <th width="10%">Ação</th>
                        <th width="30%">Motivo</th>
                        <th width="15%">IP</th>
                        <th width="15%">Ações</th>
                    </tr>
                </thead>
                <tbody>
                {% for evento in presenca.historico.all %}
                    <tr>
                        <td>
                            <small>{{ evento.timestamp|date:"d/m/Y H:i:s" }}</small>
                        </td>
                        <td>
                            <span class="badge badge-secondary">{{ evento.usuario }}</span>
                        </td>
                        <td>
                            {% if evento.acao == 'CREATE' %}
                                <span class="badge badge-success">Criação</span>
                            {% elif evento.acao == 'UPDATE' %}
                                <span class="badge badge-warning">Alteração</span>
                            {% elif evento.acao == 'DELETE' %}
                                <span class="badge badge-danger">Exclusão</span>
                            {% endif %}
                        </td>
                        <td>
                            <small>{{ evento.motivo|truncatewords:8|default:"—" }}</small>
                        </td>
                        <td>
                            <small class="text-muted">{{ evento.ip_address|default:"—" }}</small>
                        </td>
                        <td>
                            <button class="btn btn-sm btn-outline-info" 
                                    onclick="verDetalhesEvento({{ evento.id }})">
                                <i class="fas fa-eye"></i>
                            </button>
                        </td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% else %}
    <div class="card-body text-center text-muted">
        <i class="fas fa-info-circle"></i>
        Nenhum evento registrado ainda.
    </div>
    {% endif %}
</div>
```

**📋 Tarefas:**
- [ ] Criar template de histórico de auditoria
- [ ] Implementar modal de detalhes do evento
- [ ] Adicionar JavaScript para interações
- [ ] Integrar em templates de edição existentes
- [ ] Testes de interface

#### **Dia 3-4: Formulários com Validação Avançada**
```html
<!-- 📁 presencas/templates/presencas/forms/editar_presenca_form.html -->
<form id="form-editar-presenca" method="post" novalidate>
    {% csrf_token %}
    
    <!-- Campo obrigatório: Motivo da alteração -->
    <div class="form-group">
        <label for="motivo_alteracao" class="form-label required">
            <i class="fas fa-edit"></i>
            Motivo da Alteração *
        </label>
        <textarea 
            class="form-control" 
            id="motivo_alteracao" 
            name="motivo_alteracao" 
            rows="3" 
            required
            placeholder="Descreva o motivo desta alteração..."
            maxlength="500">{{ form.motivo_alteracao.value|default_if_none:"" }}</textarea>
        <div class="invalid-feedback">
            Este campo é obrigatório para alterações.
        </div>
        <small class="form-text text-muted">
            <span id="contador-caracteres">0</span>/500 caracteres
        </small>
    </div>
    
    <!-- Aviso de janela temporal -->
    {% if presenca.pode_ser_alterada %}
        <div class="alert alert-info">
            <i class="fas fa-clock"></i>
            <strong>Janela de alteração:</strong> 
            Esta presença pode ser alterada até {{ presenca.limite_alteracao|date:"d/m/Y H:i" }}
        </div>
    {% else %}
        <div class="alert alert-warning">
            <i class="fas fa-exclamation-triangle"></i>
            <strong>Alteração restrita:</strong> 
            O período normal de alteração expirou. Apenas administradores podem modificar.
        </div>
    {% endif %}
    
    <!-- Campos do formulário principal -->
    {{ form.as_p }}
    
    <!-- Botões de ação -->
    <div class="form-actions mt-4">
        <button type="submit" class="btn btn-primary" id="btn-salvar">
            <i class="fas fa-save"></i> Salvar Alterações
        </button>
        <a href="{% url 'presencas:listar_presencas_academicas' %}" class="btn btn-secondary">
            <i class="fas fa-times"></i> Cancelar
        </a>
    </div>
</form>
```

**📋 Tarefas:**
- [ ] Atualizar formulários de edição
- [ ] Implementar validação client-side
- [ ] Adicionar campo obrigatório "motivo_alteracao"
- [ ] Criar indicadores visuais de permissão
- [ ] Testes de usabilidade

#### **Dia 5: JavaScript de Interação**
```javascript
// 📁 presencas/static/presencas/js/presenca_auditoria.js
class PresencaAuditoria {
    constructor() {
        this.initEventListeners();
        this.initValidation();
    }
    
    initEventListeners() {
        // Validação em tempo real do motivo
        $('#motivo_alteracao').on('input', this.validateMotivo.bind(this));
        
        // Confirmação antes de excluir
        $('.btn-excluir-presenca').on('click', this.confirmarExclusao.bind(this));
        
        // Ver detalhes do evento de auditoria
        window.verDetalhesEvento = this.verDetalhesEvento.bind(this);
    }
    
    validateMotivo() {
        const motivo = $('#motivo_alteracao').val().trim();
        const contador = $('#contador-caracteres');
        
        contador.text(motivo.length);
        
        if (motivo.length < 10) {
            $('#motivo_alteracao').addClass('is-invalid');
            return false;
        } else {
            $('#motivo_alteracao').removeClass('is-invalid').addClass('is-valid');
            return true;
        }
    }
    
    async confirmarExclusao(event) {
        event.preventDefault();
        
        const result = await Swal.fire({
            title: 'Confirmar Exclusão',
            text: 'Esta ação será registrada no histórico. Tem certeza?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sim, excluir!',
            cancelButtonText: 'Cancelar',
            input: 'textarea',
            inputPlaceholder: 'Motivo da exclusão (obrigatório)',
            inputValidator: (value) => {
                if (!value || value.trim().length < 10) {
                    return 'O motivo deve ter pelo menos 10 caracteres!';
                }
            }
        });
        
        if (result.isConfirmed) {
            // Adicionar motivo ao formulário e submeter
            const form = $(event.target).closest('form');
            $('<input>').attr({
                type: 'hidden',
                name: 'motivo_exclusao',
                value: result.value
            }).appendTo(form);
            
            form.submit();
        }
    }
    
    async verDetalhesEvento(eventoId) {
        try {
            const response = await fetch(`/api/presencas/historico/${eventoId}/`);
            const evento = await response.json();
            
            // Mostrar modal com detalhes
            const modalHtml = this.buildDetalheModal(evento);
            $('#modal-detalhe-evento').html(modalHtml).modal('show');
            
        } catch (error) {
            console.error('Erro ao carregar detalhes:', error);
            alert('Erro ao carregar detalhes do evento');
        }
    }
    
    buildDetalheModal(evento) {
        return `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Detalhes do Evento</h5>
                        <button type="button" class="close" data-dismiss="modal">
                            <span>&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <!-- Conteúdo detalhado do evento -->
                        ${this.renderEventoDetalhes(evento)}
                    </div>
                </div>
            </div>
        `;
    }
}

// Inicializar quando documento estiver pronto
$(document).ready(() => {
    new PresencaAuditoria();
});
```

**📋 Tarefas:**
- [ ] Implementar JavaScript de interação
- [ ] Integrar SweetAlert2 para confirmações
- [ ] Criar modals de detalhes
- [ ] Implementar validação client-side
- [ ] Testes de interface JavaScript

---

### **SEMANA 4: Soft Delete e Motivos Obrigatórios**

#### **Dia 1-2: Implementar Soft Delete**
```python
# 📁 presencas/managers.py
class PresencaManager(models.Manager):
    """Manager customizado para presenças"""
    
    def get_queryset(self):
        """Filtrar apenas registros não excluídos por padrão"""
        return super().get_queryset().filter(excluida=False)

class PresencaComExcluidasManager(models.Manager):
    """Manager que inclui registros excluídos"""
    pass

# 📁 presencas/models.py - Adicionar ao modelo Presenca
class Presenca(models.Model):
    # ... campos existentes ...
    
    # Campos para soft delete
    excluida = models.BooleanField(default=False, verbose_name='Excluída')
    data_exclusao = models.DateTimeField(null=True, blank=True, verbose_name='Data de Exclusão')
    excluida_por = models.CharField(max_length=100, null=True, blank=True, verbose_name='Excluída por')
    motivo_exclusao = models.TextField(blank=True, verbose_name='Motivo da Exclusão')
    
    # Managers
    objects = PresencaManager()  # Manager padrão (sem excluídas)
    todas = PresencaComExcluidasManager()  # Inclui excluídas
    
    def soft_delete(self, usuario, motivo):
        """Marca registro como excluído sem deletar fisicamente"""
        self.excluida = True
        self.data_exclusao = timezone.now()
        self.excluida_por = usuario
        self.motivo_exclusao = motivo
        self.save(update_fields=['excluida', 'data_exclusao', 'excluida_por', 'motivo_exclusao'])
    
    def restore(self, usuario, motivo):
        """Restaura registro marcado como excluído"""
        self.excluida = False
        self.data_exclusao = None
        self.excluida_por = None
        self.motivo_exclusao = ''
        self.save(update_fields=['excluida', 'data_exclusao', 'excluida_por', 'motivo_exclusao'])
        
        # Registrar restauração no histórico
        PresencaHistorico.objects.create(
            presenca_original=self,
            acao='RESTORE',
            dados_anteriores={'excluida': True},
            dados_novos={'excluida': False},
            usuario=usuario,
            motivo=f'Restauração: {motivo}'
        )
```

**📋 Tarefas:**
- [ ] Adicionar campos de soft delete ao modelo
- [ ] Criar managers customizados
- [ ] Implementar métodos `soft_delete()` e `restore()`
- [ ] Gerar e executar migração
- [ ] Atualizar todas as views para usar soft delete
- [ ] Testes unitários para soft delete

#### **Dia 3-4: Formulários com Motivos Obrigatórios**
```python
# 📁 presencas/forms.py
class EditarPresencaForm(forms.ModelForm):
    """Formulário para editar presença com motivo obrigatório"""
    
    motivo_alteracao = forms.CharField(
        label='Motivo da Alteração',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Descreva o motivo desta alteração...',
            'maxlength': 500
        }),
        min_length=10,
        max_length=500,
        help_text='Mínimo 10 caracteres, máximo 500.'
    )
    
    class Meta:
        model = Presenca
        fields = ['presente', 'justificativa', 'motivo_alteracao']
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        # Verificar se pode editar
        if self.instance.pk:
            pode_editar, motivo = PresencaPermissions.pode_alterar_presenca(
                self.instance, self.usuario
            )
            if not pode_editar:
                # Desabilitar campos se não pode editar
                for field in self.fields:
                    if field != 'motivo_alteracao':
                        self.fields[field].disabled = True
    
    def clean_motivo_alteracao(self):
        motivo = self.cleaned_data.get('motivo_alteracao', '').strip()
        
        if len(motivo) < 10:
            raise forms.ValidationError(
                'O motivo deve ter pelo menos 10 caracteres.'
            )
        
        # Verificar palavras proibidas
        palavras_proibidas = ['teste', 'abc', '123']
        if any(palavra in motivo.lower() for palavra in palavras_proibidas):
            raise forms.ValidationError(
                'Por favor, forneça um motivo válido e descritivo.'
            )
        
        return motivo

class ExcluirPresencaForm(forms.Form):
    """Formulário para exclusão com motivo obrigatório"""
    
    motivo_exclusao = forms.CharField(
        label='Motivo da Exclusão',
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Explique por que esta presença está sendo excluída...',
            'maxlength': 1000
        }),
        min_length=15,
        max_length=1000,
        help_text='Mínimo 15 caracteres. Este motivo será registrado permanentemente.'
    )
    
    confirmar_exclusao = forms.BooleanField(
        label='Confirmo que desejo excluir esta presença',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
```

**📋 Tarefas:**
- [ ] Criar formulários com validação de motivo
- [ ] Implementar validação de palavras proibidas
- [ ] Adicionar campo de confirmação
- [ ] Atualizar views para usar novos formulários
- [ ] Testes de validação

#### **Dia 5: Views Atualizadas**
```python
# 📁 presencas/views_audit.py
@login_required
@require_presenca_permission('edit')
def editar_presenca_com_auditoria(request, pk):
    """View para editar presença com auditoria completa"""
    presenca = get_object_or_404(Presenca, pk=pk)
    
    # Verificar permissões
    pode_editar, motivo_negacao = PresencaPermissions.pode_alterar_presenca(
        presenca, request.user
    )
    
    if request.method == 'POST':
        form = EditarPresencaForm(
            request.POST, 
            instance=presenca, 
            usuario=request.user
        )
        
        if form.is_valid() and pode_editar:
            # Salvar dados anteriores para auditoria
            dados_anteriores = {
                'presente': presenca.presente,
                'justificativa': presenca.justificativa,
            }
            
            # Aplicar alterações
            presenca_atualizada = form.save(commit=False)
            presenca_atualizada._usuario_atual = request.user.username
            presenca_atualizada._motivo_alteracao = form.cleaned_data['motivo_alteracao']
            presenca_atualizada._dados_anteriores = dados_anteriores
            presenca_atualizada._ip_address = get_client_ip(request)
            presenca_atualizada._user_agent = request.META.get('HTTP_USER_AGENT', '')
            presenca_atualizada.save()
            
            messages.success(request, 'Presença alterada com sucesso!')
            return redirect('presencas:listar_presencas_academicas')
        
        elif not pode_editar:
            messages.error(request, f'Não é possível editar: {motivo_negacao}')
    
    else:
        form = EditarPresencaForm(instance=presenca, usuario=request.user)
    
    context = {
        'form': form,
        'presenca': presenca,
        'pode_editar': pode_editar,
        'motivo_negacao': motivo_negacao if not pode_editar else None,
        'historico': presenca.historico.all()[:10]  # Últimos 10 eventos
    }
    
    return render(request, 'presencas/editar_presenca_auditoria.html', context)

@login_required
@require_presenca_permission('delete')
def excluir_presenca_com_auditoria(request, pk):
    """View para excluir presença com soft delete"""
    presenca = get_object_or_404(Presenca, pk=pk)
    
    pode_excluir, motivo_negacao = PresencaPermissions.pode_excluir_presenca(
        presenca, request.user
    )
    
    if request.method == 'POST':
        form = ExcluirPresencaForm(request.POST)
        
        if form.is_valid() and pode_excluir:
            # Soft delete com motivo
            presenca.soft_delete(
                usuario=request.user.username,
                motivo=form.cleaned_data['motivo_exclusao']
            )
            
            messages.success(request, 'Presença excluída com sucesso!')
            return redirect('presencas:listar_presencas_academicas')
        
        elif not pode_excluir:
            messages.error(request, f'Não é possível excluir: {motivo_negacao}')
    
    else:
        form = ExcluirPresencaForm()
    
    context = {
        'form': form,
        'presenca': presenca,
        'pode_excluir': pode_excluir,
        'motivo_negacao': motivo_negacao if not pode_excluir else None
    }
    
    return render(request, 'presencas/excluir_presenca_auditoria.html', context)
```

**📋 Tarefas:**
- [ ] Criar views com auditoria completa
- [ ] Implementar soft delete nas views
- [ ] Adicionar tratamento de permissões
- [ ] Criar templates atualizados
- [ ] Testes de integração

---

### **SEMANA 5: Relatórios de Auditoria**

#### **Dia 1-2: Relatórios Administrativos**
```python
# 📁 presencas/views/relatorios_auditoria.py
@login_required
@permission_required('presencas.can_view_audit_trail')
def relatorio_auditoria_presencas(request):
    """Relatório completo de auditoria de presenças"""
    
    # Filtros
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    usuario = request.GET.get('usuario')
    acao = request.GET.get('acao')
    
    # Query base
    historico = PresencaHistorico.objects.all()
    
    # Aplicar filtros
    if data_inicio:
        historico = historico.filter(timestamp__gte=data_inicio)
    if data_fim:
        historico = historico.filter(timestamp__lte=data_fim)
    if usuario:
        historico = historico.filter(usuario__icontains=usuario)
    if acao:
        historico = historico.filter(acao=acao)
    
    # Paginação
    paginator = Paginator(historico, 50)
    page = request.GET.get('page')
    historico_paginado = paginator.get_page(page)
    
    # Estatísticas
    stats = {
        'total_eventos': historico.count(),
        'eventos_por_acao': historico.values('acao').annotate(count=Count('id')),
        'usuarios_mais_ativos': historico.values('usuario').annotate(
            count=Count('id')
        ).order_by('-count')[:10],
        'eventos_por_dia': historico.extra({
            'dia': "date(timestamp)"
        }).values('dia').annotate(count=Count('id')).order_by('-dia')[:7]
    }
    
    context = {
        'historico': historico_paginado,
        'stats': stats,
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'usuario': usuario,
            'acao': acao
        }
    }
    
    return render(request, 'presencas/relatorios/auditoria.html', context)

@login_required
@permission_required('presencas.can_view_audit_trail')
def exportar_auditoria_excel(request):
    """Exporta relatório de auditoria para Excel"""
    
    # Aplicar mesmos filtros do relatório
    historico = get_filtered_historico(request)
    
    # Criar workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Auditoria de Presenças"
    
    # Cabeçalhos
    headers = [
        'Data/Hora', 'Usuário', 'Ação', 'Aluno', 'Turma', 
        'Atividade', 'Data Presença', 'Motivo', 'IP'
    ]
    ws.append(headers)
    
    # Dados
    for evento in historico:
        ws.append([
            evento.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
            evento.usuario,
            evento.get_acao_display(),
            evento.presenca_original.aluno.nome,
            evento.presenca_original.turma.nome,
            evento.presenca_original.atividade.nome,
            evento.presenca_original.data.strftime('%d/%m/%Y'),
            evento.motivo[:100],  # Limitar tamanho
            evento.ip_address or ''
        ])
    
    # Configurar response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="auditoria_presencas_{timezone.now().strftime("%Y%m%d")}.xlsx"'
    
    wb.save(response)
    return response
```

**📋 Tarefas:**
- [ ] Criar views de relatórios
- [ ] Implementar filtros avançados
- [ ] Adicionar exportação Excel/PDF
- [ ] Criar dashboard de estatísticas
- [ ] Testes de relatórios

#### **Dia 3-4: Dashboard de Monitoramento**
```html
<!-- 📁 presencas/templates/presencas/dashboard/auditoria.html -->
<div class="row">
    <!-- Cards de Estatísticas -->
    <div class="col-md-3">
        <div class="card bg-primary text-white">
            <div class="card-body">
                <div class="d-flex align-items-center">
                    <div class="flex-grow-1">
                        <h5 class="card-title">Eventos Hoje</h5>
                        <h3 class="mb-0">{{ stats.eventos_hoje }}</h3>
                    </div>
                    <div class="flex-shrink-0">
                        <i class="fas fa-calendar-day fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-3">
        <div class="card bg-info text-white">
            <div class="card-body">
                <div class="d-flex align-items-center">
                    <div class="flex-grow-1">
                        <h5 class="card-title">Alterações</h5>
                        <h3 class="mb-0">{{ stats.alteracoes_semana }}</h3>
                        <small>Esta semana</small>
                    </div>
                    <div class="flex-shrink-0">
                        <i class="fas fa-edit fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-3">
        <div class="card bg-warning text-white">
            <div class="card-body">
                <div class="d-flex align-items-center">
                    <div class="flex-grow-1">
                        <h5 class="card-title">Exclusões</h5>
                        <h3 class="mb-0">{{ stats.exclusoes_semana }}</h3>
                        <small>Esta semana</small>
                    </div>
                    <div class="flex-shrink-0">
                        <i class="fas fa-trash fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-3">
        <div class="card bg-success text-white">
            <div class="card-body">
                <div class="d-flex align-items-center">
                    <div class="flex-grow-1">
                        <h5 class="card-title">Usuários Ativos</h5>
                        <h3 class="mb-0">{{ stats.usuarios_ativos }}</h3>
                        <small>Últimos 7 dias</small>
                    </div>
                    <div class="flex-shrink-0">
                        <i class="fas fa-users fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Gráficos -->
<div class="row mt-4">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h5>Eventos por Dia (Últimos 30 dias)</h5>
            </div>
            <div class="card-body">
                <canvas id="grafico-eventos-dia"></canvas>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5>Distribuição por Tipo</h5>
            </div>
            <div class="card-body">
                <canvas id="grafico-tipos-evento"></canvas>
            </div>
        </div>
    </div>
</div>

<!-- Eventos Recentes -->
<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header d-flex justify-content-between">
                <h5>Eventos Recentes</h5>
                <a href="{% url 'presencas:relatorio_auditoria' %}" class="btn btn-sm btn-primary">
                    Ver Relatório Completo
                </a>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <!-- Tabela de eventos recentes -->
                </div>
            </div>
        </div>
    </div>
</div>
```

**📋 Tarefas:**
- [ ] Criar dashboard visual
- [ ] Implementar gráficos com Chart.js
- [ ] Adicionar filtros em tempo real
- [ ] Criar alertas automáticos
- [ ] Testes de interface

#### **Dia 5: Finalização e Documentação**
**📋 Tarefas:**
- [ ] Revisar toda implementação
- [ ] Atualizar documentação
- [ ] Criar guia do usuário
- [ ] Executar testes completos
- [ ] Preparar para produção

---

## 🧪 ESTRATÉGIA DE TESTES

### **Testes Unitários**
```python
# 📁 presencas/tests/test_auditoria.py
class TestPresencaHistorico(TestCase):
    def test_criacao_historico_automatica(self):
        """Testa se histórico é criado automaticamente"""
        presenca = Presenca.objects.create(...)
        self.assertEqual(presenca.historico.count(), 1)
        self.assertEqual(presenca.historico.first().acao, 'CREATE')
    
    def test_soft_delete(self):
        """Testa exclusão lógica"""
        presenca = Presenca.objects.create(...)
        presenca.soft_delete('admin', 'Teste de exclusão')
        
        self.assertTrue(presenca.excluida)
        self.assertNotIn(presenca, Presenca.objects.all())
        self.assertIn(presenca, Presenca.todas.all())
```

### **Testes de Integração**
```python
# 📁 presencas/tests/test_permissions.py
class TestPresencaPermissions(TestCase):
    def test_janela_temporal_alteracao(self):
        """Testa regra de janela temporal"""
        # Criar presença antiga
        presenca = Presenca.objects.create(...)
        presenca.data_registro = timezone.now() - timedelta(days=8)
        presenca.save()
        
        # Usuário comum não deve conseguir alterar
        pode, motivo = PresencaPermissions.pode_alterar_presenca(presenca, self.user_comum)
        self.assertFalse(pode)
        self.assertIn("expirado", motivo)
```

### **Testes End-to-End**
```python
# 📁 presencas/tests/test_e2e_auditoria.py
class TestAuditoriaE2E(LiveServerTestCase):
    def test_fluxo_completo_alteracao(self):
        """Testa fluxo completo de alteração com auditoria"""
        # 1. Criar presença
        # 2. Tentar alterar sem motivo
        # 3. Alterar com motivo válido
        # 4. Verificar histórico
        # 5. Tentar alterar após prazo
```

---

## 📊 MÉTRICAS DE SUCESSO

### **Funcionalidade**
- [ ] 100% das alterações registradas no histórico
- [ ] 0 alterações sem motivo válido permitidas
- [ ] Permissões funcionando conforme regras de negócio
- [ ] Interface responsiva e intuitiva

### **Performance**
- [ ] Consultas de auditoria < 500ms
- [ ] Dashboard carrega em < 2s
- [ ] Exportação de relatórios < 5s

### **Qualidade**
- [ ] Cobertura de testes > 90%
- [ ] 0 bugs críticos
- [ ] Documentação completa

---

## 🚀 DEPLOY E ROLLOUT

### **Ambiente de Desenvolvimento**
1. Criar branch `feature/auditoria-presencas`
2. Implementar incrementalmente
3. Testes locais contínuos

### **Ambiente de Teste**
1. Deploy em staging
2. Testes de integração
3. Validação com usuários

### **Ambiente de Produção**
1. Backup completo antes do deploy
2. Migração de dados
3. Monitoramento pós-deploy
4. Rollback plan preparado

---

## 📝 CHECKLIST FINAL

### **Antes do Deploy**
- [ ] Todos os testes passando
- [ ] Migração testada em dados reais
- [ ] Backup de segurança criado
- [ ] Documentação atualizada
- [ ] Treinamento de usuários realizado

### **Pós-Deploy**
- [ ] Monitorar logs de erro
- [ ] Verificar performance
- [ ] Coletar feedback dos usuários
- [ ] Ajustes finos se necessário

---

## 👥 RESPONSABILIDADES

| Papel | Responsabilidade |
|-------|------------------|
| **Desenvolvedor Backend** | Modelos, Views, API, Testes |
| **Desenvolvedor Frontend** | Templates, JavaScript, CSS |
| **DBA** | Migrações, Performance, Backup |
| **QA** | Testes, Validação, Documentação |
| **DevOps** | Deploy, Monitoramento, Rollback |

---

## 📚 RECURSOS ADICIONAIS

### **Documentação Técnica**
- Guia de Desenvolvimento: `/docs/desenvolvimento.md`
- API Documentation: `/docs/api.md`
- Manual do Usuário: `/docs/usuario.md`

### **Ferramentas**
- **Monitoramento**: Sentry, DataDog
- **Testes**: Pytest, Selenium
- **CI/CD**: GitHub Actions
- **Documentação**: Sphinx, GitBook

---

**🎯 PRÓXIMOS PASSOS:** Aguardando aprovação para iniciar implementação da **SEMANA 1: Fundação - Sistema de Auditoria**.
