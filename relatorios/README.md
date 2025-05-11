# Scripts de Gerenciamento do Plano de Testes OMAUM

Este diretório contém scripts para gerenciar automaticamente o plano de testes do sistema OMAUM.

## Visão Geral

Os scripts disponíveis são:

1. `update_test
# Scripts de Gerenciamento do Plano de Testes OMAUM

Este diretório contém scripts para gerenciar automaticamente o plano de testes do sistema OMAUM.

## Visão Geral

Os scripts disponíveis são:

1. `update_test_plan.py` - Script principal para atualizar o plano de testes
2. `manage_test_plan.py` - Interface interativa de linha de comando para gerenciar o plano de testes
3. `watch_changes.py` - Monitora mudanças nos arquivos do projeto e atualiza o plano automaticamente
4. `notify_update.py` - Envia notificações sobre atualizações do plano de testes
5. `web_dashboard.py` - Painel de controle web para gerenciar o plano de testes

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python: (instale com `pip install -r requirements.txt`)
  - win10toast (opcional, para notificações no Windows 10)

## Como Usar

### Atualização Manual do Plano de Testes

Para atualizar manualmente o plano de testes, execute:

```bash
python scripts/update_test_plan.py
```

Ou use o arquivo batch:

```bash
update_test_plan.bat
```

### Interface Interativa

Para usar a interface interativa de linha de comando:

```bash
python scripts/manage_test_plan.py
```

Ou use o arquivo batch:

```bash
manage_test_plan.bat
```

### Monitoramento Automático

Para iniciar o monitoramento automático de mudanças:

```bash
python scripts/watch_changes.py [intervalo_em_segundos]
```

Ou use o arquivo batch:

```bash
watch_changes.bat
```

O intervalo padrão é de 10 segundos.

### Painel de Controle Web

Para iniciar o painel de controle web:

```bash
python scripts/web_dashboard.py [porta]
```

Ou use o arquivo batch:

```bash
web_dashboard.bat
```

A porta padrão é 8000. O navegador será aberto automaticamente.

## Configuração de Execução Automática

### Tarefa Agendada no Windows

1. Execute `manage_test_plan.py` e selecione a opção "Configurar atualização automática"
2. Escolha "Criar tarefa agendada no Windows"
3. Siga as instruções na tela

### Git Hook (pre-commit)

1. Execute `manage_test_plan.py` e selecione a opção "Configurar atualização automática"
2. Escolha "Configurar Git Hook (pre-commit)"
3. O hook será configurado automaticamente

## Solução de Problemas

### O plano de testes não está sendo atualizado

- Verifique se o diretório `docs` existe na raiz do projeto
- Verifique as permissões de escrita no diretório `docs`
- Execute o script com privilégios de administrador, se necessário

### Erro ao executar os scripts

- Verifique se o Python está instalado corretamente
- Verifique se todas as dependências estão instaladas
- Verifique o log de erros para mais detalhes

## Contribuição

Para contribuir com melhorias nos scripts:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um novo Pull Request
```

## Passo 13: Criar um Arquivo de Requisitos

Para garantir que todas as dependências necessárias estejam instaladas, vamos criar um arquivo `requirements.txt`:

```text:C:\projetos\omaum\scripts\requirements.txt
# Requisitos para os scripts de gerenciamento do plano de testes
win10toast>=0.9; platform_system=="Windows"  # Para notificações no Windows
```

## Passo 14: Criar um Script de Instalação

Para facilitar a configuração inicial, vamos criar um script de instalação:

```python:C:\projetos\omaum\scripts\setup.py
#!/usr/bin/env python
"""
Script de instalação para configurar o ambiente de gerenciamento do plano de testes.
"""

import os
import sys
import subprocess
import platform

def clear_screen():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Imprime o cabeçalho do instalador."""
    clear_screen()
    print("=" * 60)
    print("      INSTALAÇÃO DO GERENCIADOR DE PLANO DE TESTES OMAUM")
    print("=" * 60)
    print()

def check_python_version():
    """Verifica se a versão do Python é compatível."""
    print("Verificando versão do Python...")
    
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 6):
        print(f"Versão do Python incompatível: {major}.{minor}")
        print("Este script requer Python 3.6 ou superior.")
        return False
    
    print(f"Versão do Python: {major}.{minor} (OK)")
    return True

def install_dependencies():
    """Instala as dependências necessárias."""
    print("\nInstalando dependências...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(script_dir, 'requirements.txt')
    
    if not os.path.exists(requirements_path):
        print(f"Arquivo de requisitos não encontrado: {requirements_path}")
        return False
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print("Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar dependências: {e}")
        return False

def create_batch_files():
    """Cria os arquivos batch para facilitar a execução dos scripts."""
    print("\nCriando arquivos batch...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    batch_files = {
        'update_test_plan.bat': '@echo off\necho Atualizando o plano de testes...\npython scripts\\update_test_plan.py\nif %ERRORLEVEL% EQU 0 (\n    echo Plano de testes atualizado com sucesso!\n) else (\n    echo Erro ao atualizar o plano de testes.\n)\npause\n',
        'manage_test_plan.bat': '@echo off\npython scripts\\manage_test_plan.py\n',
        'watch_changes.bat': '@echo off\necho Iniciando monitoramento de mudanças no projeto...\npython scripts\\watch_changes.py 10\n',
        'web_dashboard.bat': '@echo off\necho Iniciando o painel de controle web...\npython scripts\\web_dashboard.py\n'
    }
    
    for filename, content in batch_files.items():
        file_path = os.path.join(project_root, filename)
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Arquivo criado: {filename}")
        except Exception as e:
            print(f"Erro ao criar {filename}: {e}")
    
    return True

def create_docs_directory():
    """Cria o diretório docs se não existir."""
    print("\nVerificando diretório docs...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    docs_dir = os.path.join(project_root, 'docs')
    
    if not os.path.exists(docs_dir):
        try:
            os.makedirs(docs_dir)
            print(f"Diretório criado: {docs_dir}")
        except Exception as e:
            print(f"Erro ao criar diretório docs: {e}")
            return False
    else:
        print(f"Diretório docs já existe: {docs_dir}")
    
    return True

def main():
    """Função principal do instalador."""
    print_header()
    
    print("Este script irá configurar o ambiente para o gerenciamento do plano de testes OMAUM.")
    print("Serão realizadas as seguintes ações:")
    print("1. Verificar a versão do Python")
    print("2. Instalar dependências necessárias")
    print("3. Criar arquivos batch para facilitar a execução")
    print("4. Criar o diretório docs (se não existir)")
    print()
    
    confirm = input("Deseja continuar? (s/n): ")
    if confirm.lower() != 's':
        print("\nInstalação cancelada pelo usuário.")
        return
    
    # Verificar versão do Python
    if not check_python_version():
        input("\nPressione Enter para sair...")
        return
    
    # Instalar dependências
    install_dependencies()
    
    # Criar arquivos batch
    create_batch_files()
    
    # Criar diretório docs
    create_docs_directory()
    
    print("\nInstalação concluída com sucesso!")
    print("\nVocê pode agora:")
    print("- Executar update_test_plan.bat para atualizar o plano de testes")
    print("- Executar manage_test_plan.bat para usar a interface interativa")
    print("- Executar watch_changes.bat para iniciar o monitoramento automático")
    print("- Executar web_dashboard.bat para iniciar o painel de controle web")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
```

## Conclusão

Com esses scripts, você tem um sistema completo para gerenciar automaticamente o plano de testes do projeto OMAUM. Os principais recursos incluem:

1. **Atualização automática** do plano de testes com base no código-fonte
2. **Interface interativa** para gerenciar o plano de testes
3. **Monitoramento automático** de mudanças nos arquivos do projeto
4. **Notificações** sobre atualizações do plano de testes
5. **Painel de controle web** para gerenciamento visual
6. **Integração com Git** para atualização automática antes de commits
7. **Agendamento de tarefas** para atualização periódica

Para começar a usar o sistema, execute o script de instalação:

```bash
python scripts/setup.py
