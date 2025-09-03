#!/usr/bin/env python
"""
Script utilitário idempotente para criação / atualização de superusuário Django.

Características:
- Não altera nenhum arquivo existente: atua somente via ORM.
- Idempotente: executar várias vezes não duplica usuários.
- Suporta custom AUTH_USER_MODEL (usa get_user_model()).
- Detecta nome do campo de identificação (User.USERNAME_FIELD).
- Pode opcionalmente executar migrações (--migrar ou SUPERUSER_AUTO_MIGRATE=1).
- Pode forçar redefinição de senha existente (--forcar-troca-senha).
- Pode apenas listar superusuários (--apenas-exibir).
- Parametrização via argumentos ou variáveis de ambiente.

Variáveis de ambiente suportadas:
  SUPERUSER_USERNAME
  SUPERUSER_EMAIL
  SUPERUSER_PASSWORD   (atenção: usar somente em ambientes controlados/CI)
  SUPERUSER_AUTO_MIGRATE=1  (equivale a --migrar)

Exemplos de uso:
  python scripts/gerenciar_superusuario.py --username admin
  SUPERUSER_PASSWORD="SenhaForte123" python scripts/gerenciar_superusuario.py --username admin --email admin@exemplo.com
  python scripts/gerenciar_superusuario.py --apenas-exibir
  python scripts/gerenciar_superusuario.py --forcar-troca-senha --username admin
  python scripts/gerenciar_superusuario.py --migrar --username admin

Saídas (exit codes):
  0 = sucesso
  1 = erro genérico
  2 = migrações pendentes (quando não autorizado a migrar)
  3 = falha de validação de parâmetros

ATENÇÃO: Nunca faça commit de senhas reais. Use senhas temporárias e troque depois.
"""

from __future__ import annotations

import argparse
import getpass
import os
import sys
import traceback
import importlib
from typing import Any, Dict

# Configuração do Django -----------------------------------------------------
# Adicionar o diretório do projeto ao sys.path para permitir importação do módulo omaum
from pathlib import Path

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
try:
    django_module = importlib.import_module("django")  # evita import direto repetido
    django_module.setup()
except Exception as e:  # pragma: no cover
    print(f"[ERRO] Falha ao inicializar Django: {e}", file=sys.stderr)
    print(f"[DEBUG] Project root: {project_root}", file=sys.stderr)
    print(f"[DEBUG] sys.path: {sys.path}", file=sys.stderr)
    sys.exit(1)

from django.contrib.auth import get_user_model  # noqa: E402
from django.db import connections, DEFAULT_DB_ALIAS  # noqa: E402
from django.db.migrations.executor import MigrationExecutor  # noqa: E402
from django.core.management import call_command  # noqa: E402

# ---------------------------------------------------------------------------


def _tem_migracoes_pendentes() -> bool:
    """Verifica se há migrações pendentes na base padrão."""
    connection = connections[DEFAULT_DB_ALIAS]
    try:
        executor = MigrationExecutor(connection)
    except Exception:
        # Se as tabelas de migração não existem ainda, certamente há pendências
        return True
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    return bool(plan)


def _aplicar_migracoes_silencioso():
    """Aplica migrações sem interação (mostra saída mínima)."""
    print("[INFO] Aplicando migrações pendentes...")
    call_command("migrate", interactive=False, verbosity=1)


def obter_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gerencia (cria/atualiza) superusuário de forma idempotente.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--username",
        dest="username",
        default=os.getenv("SUPERUSER_USERNAME", "admin"),
        help="Username (ou campo USERNAME_FIELD se customizado)",
    )
    parser.add_argument(
        "--email",
        dest="email",
        default=os.getenv("SUPERUSER_EMAIL", "admin@example.com"),
        help="Email do superusuário",
    )
    parser.add_argument(
        "--password",
        dest="password",
        default=os.getenv("SUPERUSER_PASSWORD"),
        help="Senha (se omitida e necessário, será solicitada interativamente)",
    )
    parser.add_argument(
        "--migrar",
        action="store_true",
        help="Aplicar migrações pendentes automaticamente",
    )
    parser.add_argument(
        "--forcar-troca-senha",
        action="store_true",
        help="Reaplicar senha mesmo que o usuário já exista",
    )
    parser.add_argument(
        "--apenas-exibir",
        action="store_true",
        help="Somente listar superusuários existentes e sair",
    )
    parser.add_argument(
        "--inativar",
        action="store_true",
        help="Marcar usuário como inativo (para reversões)",
    )
    parser.add_argument(
        "--silencioso", action="store_true", help="Reduz logs (adequado a CI)"
    )
    return parser.parse_args()


def validar_parametros(args: argparse.Namespace) -> None:
    if not args.username:
        print("[ERRO] --username vazio.", file=sys.stderr)
        sys.exit(3)
    # Email opcional em alguns modelos, mas se informado validar formato simples
    if args.email and "@" not in args.email:
        print("[AVISO] Email sem '@' aparente: prosseguindo assim mesmo.")


def log(msg: str, *, silencioso: bool = False) -> None:
    if not silencioso:
        print(msg)


def listar_superusuarios(silencioso: bool = False) -> None:
    User = get_user_model()
    campo = User.USERNAME_FIELD
    dados = list(
        User.objects.filter(is_superuser=True).values(campo, "email", "is_active")
    )
    if not dados:
        log("[INFO] Nenhum superusuário encontrado.", silencioso=silencioso)
    else:
        log("[INFO] Superusuários:", silencioso=silencioso)
        for d in dados:
            log(
                f"  - {campo}={d[campo]!r} email={d.get('email')} ativo={d.get('is_active')}",
                silencioso=silencioso,
            )


def obter_senha_interativa(args: argparse.Namespace, created: bool) -> str:
    if args.password and (created or args.forcar_troca_senha):
        return args.password
    if not created and not args.forcar_troca_senha:
        return ""  # sem alteração
    # Solicitar
    while True:
        pwd1 = getpass.getpass("Digite a nova senha: ")
        pwd2 = getpass.getpass("Confirme a nova senha: ")
        if pwd1 != pwd2:
            print("[ERRO] Senhas não conferem. Tente novamente.")
            continue
        if not pwd1.strip():
            print("[ERRO] Senha vazia não permitida.")
            continue
        return pwd1


def criar_ou_atualizar_superusuario(args: argparse.Namespace) -> Dict[str, Any]:
    User = get_user_model()
    campo = User.USERNAME_FIELD

    # Monta kwargs dinâmico conforme o USERNAME_FIELD
    filtro = {campo: args.username}
    usuario, created = User.objects.get_or_create(**filtro)

    alteracoes = []

    # Flags administrativas
    if not usuario.is_superuser:
        usuario.is_superuser = True
        alteracoes.append("is_superuser=True")
    if not usuario.is_staff:
        usuario.is_staff = True
        alteracoes.append("is_staff=True")
    if args.inativar:
        if usuario.is_active:
            usuario.is_active = False
            alteracoes.append("is_active=False")
    else:
        if not usuario.is_active:
            usuario.is_active = True
            alteracoes.append("is_active=True")

    # Email (se o modelo possuir)
    if hasattr(usuario, "email") and args.email:
        if usuario.email != args.email:
            usuario.email = args.email
            alteracoes.append(f"email={args.email}")

    # Senha
    senha_para_definir = obter_senha_interativa(args, created)
    if senha_para_definir:
        usuario.set_password(senha_para_definir)
        alteracoes.append("<senha_atualizada>")

    if created or alteracoes:
        usuario.save()

    return {
        "created": created,
        "alteracoes": alteracoes,
        "username_field": campo,
        "identificador": getattr(usuario, campo),
        "id": usuario.id,
    }


def main():  # pragma: no cover - execução de script
    args = obter_args()
    validar_parametros(args)

    auto_migrate_env = os.getenv("SUPERUSER_AUTO_MIGRATE") == "1"
    executar_migrate = args.migrar or auto_migrate_env

    # Verificar migrações pendentes
    if _tem_migracoes_pendentes():
        if executar_migrate:
            _aplicar_migracoes_silencioso()
        else:
            print(
                "[AVISO] Há migrações pendentes. Use --migrar ou SUPERUSER_AUTO_MIGRATE=1 se necessário."
            )

    if args.apenas_exibir:
        listar_superusuarios(silencioso=args.silencioso)
        sys.exit(0)

    try:
        resultado = criar_ou_atualizar_superusuario(args)
    except Exception as e:  # pragma: no cover
        print(f"[ERRO] Falha ao criar/atualizar superusuário: {e}", file=sys.stderr)
        if not args.silencioso:
            traceback.print_exc()
        sys.exit(1)

    # Logs finais
    status_criacao = "CRIADO" if resultado["created"] else "ATUALIZADO"
    if not resultado["alteracoes"] and not resultado["created"]:
        status_criacao = "SEM ALTERAÇÕES"  # idempotente

    log(
        f"[RESULTADO] {status_criacao} id={resultado['id']} {resultado['username_field']}={resultado['identificador']} alteracoes={resultado['alteracoes']}",
        silencioso=args.silencioso,
    )

    if resultado["created"] and not args.password and not args.forcar_troca_senha:
        log(
            "[INFO] Usuário criado sem senha definida (ou senha não alterada). Execute changepassword depois.",
            silencioso=args.silencioso,
        )

    # Mostrar lista final (se não silencioso)
    if not args.silencioso:
        listar_superusuarios(silencioso=args.silencioso)

    sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    main()
