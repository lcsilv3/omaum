# Arquivos da Raiz do Projeto Django


### Arquivo: collect_code.py

python
import os
import chardet
import shutil


def collect_files_by_app(project_root):
    # Dicionário para armazenar arquivos por app/funcionalidade
    apps_files = {}
    for root, dirs, files in os.walk(project_root):
        # Ignorar diretórios de ambiente virtual e cache
        if "venv" in root or "__pycache__" in root:
            continue
        # Identificar o app/funcionalidade com base no caminho
        relative_path = os.path.relpath(root, project_root)
        app_name = (
            relative_path.split(os.path.sep)[0]
            if relative_path != "."
            else "core"
        )
        # Inicializar a estrutura para o app se ainda não existir
        if app_name not in apps_files:
            apps_files[app_name] = {
                "forms.py": [],
                "views.py": [],
                "urls.py": [],
                "models.py": [],
                "templates": [],
            }
        for file in files:
            if file in ["forms.py", "views.py", "urls.py", "models.py"]:
                apps_files[app_name][file].append(os.path.join(root, file))
            elif file.endswith(".html"):
                apps_files[app_name]["templates"].append(
                    os.path.join(root, file)
                )
    return apps_files


def write_file_contents(output_file, filepath):
    # Detectar codificação do arquivo
    with open(filepath, "rb") as raw_file:
        raw_data = raw_file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"] or "utf-8"  # Fallback para utf-8
    try:
        with open(filepath, "r", encoding=encoding) as file:
            relative_path = os.path.relpath(filepath)
            output_file.write(f"\n\n### Arquivo: {relative_path}\n\n")
            # Determinar o tipo de linguagem para o bloco de código
            if filepath.endswith(".html"):
                language = "html"
            elif filepath.endswith(".py"):
                language = "python"
            else:
                language = "text"
            output_file.write(f"{language}\n")
            output_file.write(file.read())
            output_file.write("\n\n")
    except Exception as e:
        output_file.write(f"\n\n### Arquivo: {filepath}\n\n")
        output_file.write(f"\nErro ao ler o arquivo: {str(e)}\n\n")


def collect_root_files(project_root, output_dir):
    """Coleta arquivos da raiz do projeto Django."""
    output_filename = os.path.join(output_dir, "root_files_revisao.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Arquivos da Raiz do Projeto Django\n")

        # Listar arquivos na raiz do projeto
        root_files = [
            f
            for f in os.listdir(project_root)
            if os.path.isfile(os.path.join(project_root, f))
            and not f.startswith(".")
            and f != "db.sqlite3"  # Excluir o arquivo db.sqlite3
        ]

        for file in root_files:
            filepath = os.path.join(project_root, file)
            write_file_contents(output_file, filepath)

        # Verificar e incluir arquivos estáticos
        static_dir = os.path.join(project_root, "static")
        if os.path.exists(static_dir) and os.path.isdir(static_dir):
            output_file.write("\n## Arquivos Estáticos\n")
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    write_file_contents(output_file, filepath)

    print(f"Arquivos da raiz do projeto foram escritos em {output_filename}")


def generate_project_structure(project_root, output_dir):
    """Gera um arquivo com a estrutura completa do projeto."""
    output_filename = os.path.join(output_dir, "project_structure.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Estrutura do Projeto Django\n\n")
        output_file.write("\n")

        for root, dirs, files in os.walk(project_root):
            # Ignorar diretórios de ambiente virtual e cache
            if "venv" in root or "__pycache__" in root:
                continue

            level = root.replace(project_root, "").count(os.sep)
            indent = " " * 4 * level
            output_file.write(f"{indent}{os.path.basename(root)}/\n")

            sub_indent = " " * 4 * (level + 1)
            for file in files:
                output_file.write(f"{sub_indent}{file}\n")

        output_file.write("\n")

    print(f"Estrutura do projeto foi escrita em {output_filename}")


def check_template_dirs(project_root, output_dir):
    """Verifica e documenta as configurações de diretórios de templates."""
    output_filename = os.path.join(output_dir, "template_dirs_check.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Verificação de Diretórios de Templates\n\n")

        # Verificar settings.py para configurações de TEMPLATES
        settings_files = []
        for root, dirs, files in os.walk(project_root):
            if "settings.py" in files:
                settings_files.append(os.path.join(root, "settings.py"))

        if settings_files:
            output_file.write(
                "## Configurações de Templates no settings.py\n\n"
            )
            for settings_file in settings_files:
                write_file_contents(output_file, settings_file)

        # Listar todos os diretórios de templates encontrados
        output_file.write("\n## Diretórios de Templates Encontrados\n\n")
        template_dirs = []
        for root, dirs, files in os.walk(project_root):
            if "templates" in dirs:
                template_dir = os.path.join(root, "templates")
                template_dirs.append(template_dir)
                output_file.write(
                    f"- {os.path.relpath(template_dir, project_root)}\n"
                )

                # Listar arquivos de template neste diretório
                output_file.write("  Arquivos:\n")
                for template_root, template_dirs, template_files in os.walk(
                    template_dir
                ):
                    for file in template_files:
                        output_file.write(
                            f"  - {os.path.relpath(os.path.join(template_root, file), template_dir)}\n"
                        )

        # Verificar especificamente o template listar_alunos.html
        output_file.write("\n## Busca pelo template listar_alunos.html\n\n")
        found = False
        for root, dirs, files in os.walk(project_root):
            for file in files:
                if file == "listar_alunos.html":
                    found = True
                    output_file.write(
                        f"Encontrado em: {os.path.relpath(os.path.join(root, file), project_root)}\n"
                    )

        if not found:
            output_file.write(
                "O arquivo listar_alunos.html não foi encontrado no projeto.\n"
            )

    print(
        f"Verificação de diretórios de templates foi escrita em {output_filename}"
    )


def main():
    project_root = input("Digite o diretório raiz do seu projeto Django: ")
    output_dir = "revisao_projeto"
    # Criar diretório de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Coletar arquivos por app
    apps_files = collect_files_by_app(project_root)
    for app_name, file_types in apps_files.items():
        # Verificar se há arquivos para este app
        has_files = any(files for files in file_types.values())
        if not has_files:
            continue
        output_filename = os.path.join(output_dir, f"{app_name}_revisao.md")
        with open(output_filename, "w", encoding="utf-8") as output_file:
            output_file.write(f"# Revisão da Funcionalidade: {app_name}\n")
            for file_type, file_paths in file_types.items():
                if not file_paths:
                    continue
                if file_type == "templates":
                    output_file.write(f"\n## Arquivos de Template:\n")
                else:
                    output_file.write(f"\n## Arquivos {file_type}:\n")
                for filepath in sorted(file_paths):
                    write_file_contents(output_file, filepath)
        print(
            f"Conteúdo da funcionalidade '{app_name}' foi escrito em {output_filename}"
        )

    # Coletar arquivos da raiz e arquivos estáticos
    collect_root_files(project_root, output_dir)

    # Gerar estrutura do projeto
    generate_project_structure(project_root, output_dir)

    # Verificar diretórios de templates
    check_template_dirs(project_root, output_dir)

    print(f"Revisão completa! Arquivos gerados no diretório '{output_dir}'")


if __name__ == "__main__":
    main()




### Arquivo: collect_django_files.py

python
import os
import chardet


def collect_files(project_root):
    relevant_files = {
        "forms.py": [],
        "views.py": [],
        "urls.py": [],
        "models.py": [],
        "templates": [],
    }

    for root, dirs, files in os.walk(project_root):
        # Ignorar diretórios de ambiente virtual e cache
        if "venv" in root or "__pycache__" in root:
            continue

        for file in files:
            if file in relevant_files:
                relevant_files[file].append(os.path.join(root, file))
            elif file.endswith(".html"):
                relevant_files["templates"].append(os.path.join(root, file))

    return relevant_files


def write_file_contents(output_file, filepath):
    # Detectar codificação do arquivo
    with open(filepath, "rb") as raw_file:
        raw_data = raw_file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"] or "utf-8"  # Fallback para utf-8

    try:
        with open(filepath, "r", encoding=encoding) as file:
            relative_path = os.path.relpath(filepath)
            output_file.write(f"\n\n### Arquivo: {relative_path}\n")

            # Determinar o tipo de linguagem para o bloco de código
            if filepath.endswith(".html"):
                language = "html"
            elif filepath.endswith(".py"):
                language = "python"
            else:
                language = "text"

            output_file.write(f"{language}\n")
            output_file.write(file.read())
            output_file.write("\n\n")
    except Exception as e:
        output_file.write(f"\n\n### Arquivo: {filepath}\n")
        output_file.write(f"\nErro ao ler o arquivo: {str(e)}\n\n")


def main():
    project_root = input("Digite o diretório raiz do seu projeto Django: ")
    output_filename = "arquivos_projeto_para_revisao.md"

    relevant_files = collect_files(project_root)

    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Arquivos do Projeto Django para Revisão\n")

        for file_type, file_paths in relevant_files.items():
            if file_type == "templates":
                output_file.write(f"\n## Arquivos de Template:\n")
            else:
                output_file.write(f"\n## Arquivos {file_type}:\n")

            for filepath in sorted(file_paths):
                write_file_contents(output_file, filepath)

    print(f"Conteúdo dos arquivos foi escrito em {output_filename}")


if __name__ == "__main__":
    main()




### Arquivo: collect_os.py

python
import os


def collect_files(project_root):
    relevant_files = {
        "forms.py": [],
        "views.py": [],
        "urls.py": [],
        "models.py": [],
        "templates": [],
    }

    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file in relevant_files:
                relevant_files[file].append(os.path.join(root, file))
            elif file.endswith(".html"):
                relevant_files["templates"].append(os.path.join(root, file))

    return relevant_files


def write_file_contents(output_file, filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        output_file.write(f"\n\nFile: {filepath}\n")
        output_file.write("```python\n")
        output_file.write(file.read())
        output_file.write("\n```\n")


def main():
    project_root = input("Enter the root directory of your Django project: ")
    output_filename = "project_files_for_review.md"

    relevant_files = collect_files(project_root)

    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Django Project Files for Review\n")

        for file_type, file_paths in relevant_files.items():
            output_file.write(f"\n## {file_type.capitalize()} Files:\n")
            for filepath in file_paths:
                write_file_contents(output_file, filepath)

    print(f"File contents have been written to {output_filename}")


if __name__ == "__main__":
    main()




### Arquivo: cspell.json

text
{
    "version": "0.2",
    "language": "en,pt,pt-BR",
    "words": [
      "OMAUM",
      "academica",
      "academicas",
      "ritualistica",
      "ritualisticas",
      "alunos",
      "turmas",
      "cadastrar",
      "listar",
      "excluir",
      "editar",
      "criar",
      "todos",
      "direitos",
      "reservados",
      "sair",
      "fechar"
    ],
    "ignorePaths": [
      "node_modules/**",
      "venv/**",
      "*.min.*",
      "static/**",
      "media/**",
      "migrations/**"
    ],
    "ignoreRegExpList": [
      "{% [\\s\\S]*? %}",
      "{{ [\\s\\S]*? }}"
    ],
    "allowCompoundWords": true
  }
  



### Arquivo: Cursos.JPG

text


### Arquivo: c:\projetos\omaum\Cursos.JPG


Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte



### Arquivo: Erros na edição de alunos.docx

text


### Arquivo: c:\projetos\omaum\Erros na edição de alunos.docx


Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xbd in position 11: invalid start byte



### Arquivo: Erros na edição de alunos.txt

text
Tela editar_alunos antes da alteração no nome iniciatico:
<body>
    <!-- Cabeçalho -->
    <header class="bg-dark text-white p-3">
        <div class="container">
            <nav class="navbar navbar-expand-lg navbar-dark">
                <a class="navbar-brand" href="/">OMAUM</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" title="Menu de navegação">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        
                            <li class="nav-item"><a class="nav-link" href="/alunos/">Alunos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/cursos/">Cursos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/atividades/academicas/">Atividades Acadêmicas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/atividades/ritualisticas/">Atividades Ritualísticas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/turmas/">Turmas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/iniciacoes/">Iniciações</a></li>
                            <li class="nav-item"><a class="nav-link" href="/cargos/">Cargos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/frequencias/">Frequências</a></li>
                            <li class="nav-item"><a class="nav-link" href="/presencas/">Presenças</a></li>
                            <li class="nav-item"><a class="nav-link" href="/punicoes/">Punições</a></li>
                            
                                <li class="nav-item"><a class="nav-link" href="/painel-controle/">Painel de Controle</a></li>
                            
                        
                    </ul>
                    <div class="navbar-nav">
                        
                            <span class="nav-item nav-link">Olá, lcsilv3</span>
                            <a class="nav-link" href="/sair/">Sair</a>
                        
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <!-- Mensagens -->
    <div class="container mt-3">
        
    </div>

    <!-- Conteúdo Principal -->
    <main class="container py-4">
        
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Aluno: Aline Souza</h1>
        <a href="/alunos/" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    
    
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="csrfmiddlewaretoken" value="cl0Q7D6AF014XUqrqst8xs6j7BERAR1MkCsZRXNR2JMNB8D3NtsY9itJWQz1gvah">
        
        
        <div class="card mb-4 border-primary">
            <div class="card-header bg-primary text-white">
                <h5>Dados Pessoais</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
    <label for="id_cpf" class="form-label">Cpf</label>
    <input type="text" name="cpf" value="18027737038" class="form-control" placeholder="Somente números" required="" id="id_cpf" maxlength="14">
    
    
</div>

                                <div class="mb-3">
    <label for="id_nome" class="form-label">Nome Completo</label>
    <input type="text" name="nome" value="Aline Souza" class="form-control" maxlength="100" required="" id="id_nome">
    
    
</div>

                                <div class="mb-3">
    <label for="id_data_nascimento" class="form-label">Data de Nascimento</label>
    <input type="date" name="data_nascimento" value="22/12/2000" class="form-control" required="" aria-describedby="id_data_nascimento_helptext" id="id_data_nascimento">
    
    
        <small class="form-text text-muted">Formato: DD/MM/AAAA</small>
    
</div>

                                <div class="mb-3">
    <label for="id_hora_nascimento" class="form-label">Hora de Nascimento</label>
    <input type="time" name="hora_nascimento" value="15:02:00" class="form-control" aria-describedby="id_hora_nascimento_helptext" id="id_hora_nascimento">
    
    
        <small class="form-text text-muted">Formato: HH:MM</small>
    
</div>

                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
    <label for="id_email" class="form-label">E-mail</label>
    <input type="email" name="email" value="aline.souza@exemplo.com" class="form-control" maxlength="254" required="" id="id_email" style="background-size: auto, 25px; background-image: none, url(&quot;data:image/svg+xml;utf8,<svg width='26' height='28' viewBox='0 0 26 28' fill='none' xmlns='http://www.w3.org/2000/svg'><path d='M23.8958 6.1084L13.7365 0.299712C13.3797 0.103027 12.98 0 12.5739 0C12.1678 0 11.7682 0.103027 11.4113 0.299712L1.21632 6.1084C0.848276 6.31893 0.54181 6.62473 0.328154 6.99462C0.114498 7.36452 0.00129162 7.78529 7.13608e-05 8.21405V19.7951C-0.00323007 20.2248 0.108078 20.6474 0.322199 21.0181C0.53632 21.3888 0.845275 21.6938 1.21632 21.9008L11.3756 27.6732C11.7318 27.8907 12.1404 28.0037 12.556 27.9999C12.9711 27.9989 13.3784 27.8861 13.7365 27.6732L23.8958 21.9008C24.2638 21.6903 24.5703 21.3845 24.7839 21.0146C24.9976 20.6447 25.1108 20.2239 25.112 19.7951V8.21405C25.1225 7.78296 25.0142 7.35746 24.7994 6.98545C24.5845 6.61343 24.2715 6.30969 23.8958 6.1084Z' fill='url(%23paint0_linear_714_179)'/><path d='M5.47328 17.037L4.86515 17.4001C4.75634 17.4613 4.66062 17.5439 4.58357 17.643C4.50652 17.7421 4.4497 17.8558 4.4164 17.9775C4.3831 18.0991 4.374 18.2263 4.38963 18.3516C4.40526 18.4768 4.44531 18.5977 4.50743 18.707C4.58732 18.8586 4.70577 18.9857 4.85046 19.0751C4.99516 19.1645 5.16081 19.2129 5.33019 19.2153C5.49118 19.2139 5.64992 19.1767 5.79522 19.1064L6.40335 18.7434C6.51216 18.6822 6.60789 18.5996 6.68493 18.5004C6.76198 18.4013 6.8188 18.2876 6.8521 18.166C6.8854 18.0443 6.8945 17.9171 6.87887 17.7919C6.86324 17.6666 6.82319 17.5458 6.76107 17.4364C6.70583 17.3211 6.62775 17.2185 6.53171 17.1352C6.43567 17.0518 6.32374 16.9895 6.20289 16.952C6.08205 16.9145 5.95489 16.9027 5.82935 16.9174C5.70382 16.932 5.5826 16.9727 5.47328 17.037ZM9.19357 14.8951L7.94155 15.6212C7.83273 15.6824 7.73701 15.7649 7.65996 15.8641C7.58292 15.9632 7.52609 16.0769 7.49279 16.1986C7.4595 16.3202 7.4504 16.4474 7.46603 16.5726C7.48166 16.6979 7.5217 16.8187 7.58383 16.9281C7.66371 17.0797 7.78216 17.2068 7.92686 17.2962C8.07155 17.3856 8.23721 17.434 8.40658 17.4364C8.56757 17.435 8.72631 17.3978 8.87162 17.3275L10.1236 16.6014C10.2325 16.5402 10.3282 16.4576 10.4052 16.3585C10.4823 16.2594 10.5391 16.1457 10.5724 16.024C10.6057 15.9024 10.6148 15.7752 10.5992 15.6499C10.5835 15.5247 10.5435 15.4038 10.4814 15.2944C10.4261 15.1791 10.348 15.0766 10.252 14.9932C10.156 14.9099 10.044 14.8475 9.92318 14.8101C9.80234 14.7726 9.67518 14.7608 9.54964 14.7754C9.42411 14.7901 9.30289 14.8308 9.19357 14.8951ZM14.2374 13.1198C14.187 13.0168 14.1167 12.9251 14.0307 12.8503C13.9446 12.7754 13.8446 12.7189 13.7366 12.6842V5.38336C13.7371 5.2545 13.7124 5.12682 13.6641 5.00768C13.6157 4.88854 13.5446 4.78029 13.4548 4.68917C13.365 4.59806 13.2583 4.52587 13.1409 4.47678C13.0235 4.42769 12.8977 4.40266 12.7708 4.40314C12.6457 4.40355 12.522 4.42946 12.407 4.47933C12.292 4.52919 12.188 4.602 12.1013 4.69343C12.0145 4.78485 11.9467 4.89304 11.902 5.01156C11.8572 5.13007 11.8364 5.25651 11.8407 5.38336V12.7168C11.7327 12.7516 11.6327 12.8081 11.5466 12.883C11.4606 12.9578 11.3903 13.0495 11.3399 13.1525C11.2727 13.2801 11.2346 13.4213 11.2284 13.5659C11.2222 13.7104 11.2481 13.8545 11.3041 13.9875C11.2481 14.1205 11.2222 14.2646 11.2284 14.4091C11.2346 14.5536 11.2727 14.6949 11.3399 14.8225C11.3903 14.9255 11.4606 15.0172 11.5466 15.092C11.6327 15.1669 11.7327 15.2233 11.8407 15.2581V22.5916C11.8407 22.8516 11.9425 23.1009 12.1236 23.2847C12.3047 23.4686 12.5504 23.5718 12.8065 23.5718C13.0627 23.5718 13.3084 23.4686 13.4895 23.2847C13.6706 23.1009 13.7724 22.8516 13.7724 22.5916V15.2218C13.8804 15.187 13.9804 15.1305 14.0664 15.0557C14.1525 14.9809 14.2228 14.8892 14.2732 14.7862C14.3404 14.6586 14.3785 14.5173 14.3847 14.3728C14.3909 14.2283 14.365 14.0842 14.309 13.9512C14.3917 13.6751 14.3661 13.3772 14.2374 13.1198ZM16.6735 10.6112L15.4215 11.3373C15.3127 11.3985 15.2169 11.481 15.1399 11.5802C15.0628 11.6793 15.006 11.793 14.9727 11.9147C14.9394 12.0363 14.9303 12.1635 14.946 12.2887C14.9616 12.414 15.0016 12.5348 15.0638 12.6442C15.1436 12.7958 15.2621 12.9229 15.4068 13.0123C15.5515 13.1017 15.7171 13.1501 15.8865 13.1525C16.0475 13.1511 16.2062 13.1139 16.3515 13.0436L17.6036 12.3175C17.7124 12.2563 17.8081 12.1737 17.8851 12.0746C17.9622 11.9755 18.019 11.8617 18.0523 11.7401C18.0856 11.6184 18.0947 11.4913 18.0791 11.366C18.0635 11.2408 18.0234 11.1199 17.9613 11.0105C17.906 10.8952 17.828 10.7927 17.7319 10.7093C17.6359 10.626 17.524 10.5636 17.4031 10.5261C17.2823 10.4887 17.1551 10.4769 17.0296 10.4915C16.904 10.5061 16.7828 10.5469 16.6735 10.6112ZM19.639 10.9742C19.8 10.9728 19.9587 10.9357 20.104 10.8653L20.7122 10.5023C20.8208 10.4406 20.9164 10.3578 20.9935 10.2586C21.0705 10.1593 21.1275 10.0456 21.1611 9.92394C21.1947 9.80228 21.2043 9.67508 21.1893 9.54965C21.1744 9.42421 21.1351 9.30302 21.0739 9.19302C21.0126 9.08303 20.9305 8.9864 20.8324 8.90869C20.7342 8.83098 20.6219 8.77372 20.5019 8.7402C20.3818 8.70667 20.2564 8.69755 20.1329 8.71335C20.0094 8.72915 19.8902 8.76957 19.7821 8.83227L19.174 9.19531C19.0651 9.25651 18.9694 9.33909 18.8924 9.43822C18.8153 9.53735 18.7585 9.65106 18.7252 9.77271C18.6919 9.89436 18.6828 10.0215 18.6984 10.1468C18.7141 10.272 18.7541 10.3929 18.8162 10.5023C18.8981 10.6494 19.018 10.7711 19.163 10.8543C19.308 10.9374 19.4725 10.9789 19.639 10.9742ZM20.7122 17.4001L20.104 17.037C19.8859 16.9133 19.6284 16.8823 19.3878 16.9508C19.1472 17.0193 18.9432 17.1816 18.8202 17.4024C18.6973 17.6231 18.6655 17.8843 18.7318 18.1288C18.798 18.3733 18.957 18.5812 19.174 18.707L19.7821 19.0701C19.9274 19.1404 20.0861 19.1776 20.2471 19.179C20.4165 19.1766 20.5821 19.1282 20.7268 19.0388C20.8715 18.9494 20.99 18.8223 21.0699 18.6707C21.1339 18.5648 21.1755 18.4466 21.1921 18.3235C21.2087 18.2003 21.1999 18.0751 21.1662 17.9556C21.1326 17.8361 21.0749 17.7251 20.9967 17.6294C20.9185 17.5338 20.8216 17.4557 20.7122 17.4001ZM17.6 15.6212L16.348 14.8951C16.2399 14.8324 16.1207 14.792 15.9971 14.7762C15.8736 14.7604 15.7482 14.7695 15.6282 14.803C15.5082 14.8365 15.3958 14.8938 15.2977 14.9715C15.1995 15.0492 15.1174 15.1458 15.0562 15.2558C14.9949 15.3658 14.9557 15.487 14.9407 15.6125C14.9257 15.7379 14.9353 15.8651 14.9689 15.9868C15.0026 16.1084 15.0595 16.2221 15.1366 16.3214C15.2136 16.4206 15.3092 16.5035 15.4179 16.5651L16.6699 17.2912C16.8152 17.3615 16.974 17.3987 17.135 17.4001C17.3043 17.3977 17.47 17.3493 17.6147 17.2599C17.7594 17.1705 17.8778 17.0434 17.9577 16.8918C18.0228 16.7862 18.0653 16.6679 18.0825 16.5445C18.0997 16.4212 18.0911 16.2955 18.0574 16.1757C18.0237 16.0559 17.9655 15.9447 17.8867 15.8491C17.8079 15.7536 17.7103 15.6759 17.6 15.6212ZM7.94155 12.2812L9.19357 13.0073C9.33888 13.0776 9.49761 13.1148 9.6586 13.1162C9.82798 13.1138 9.99363 13.0654 10.1383 12.976C10.283 12.8866 10.4015 12.7595 10.4814 12.6079C10.5435 12.4985 10.5835 12.3777 10.5992 12.2524C10.6148 12.1272 10.6057 12 10.5724 11.8784C10.5391 11.7567 10.4823 11.643 10.4052 11.5439C10.3282 11.4447 10.2325 11.3622 10.1236 11.301L8.87162 10.5749C8.76383 10.5118 8.64476 10.4712 8.52134 10.4553C8.39792 10.4395 8.27262 10.4487 8.15275 10.4825C8.03288 10.5163 7.92084 10.574 7.82317 10.6521C7.72549 10.7303 7.64413 10.8275 7.58383 10.9379C7.46399 11.166 7.43428 11.4319 7.50073 11.6814C7.56719 11.9309 7.72481 12.1454 7.94155 12.2812ZM6.40335 9.19531L5.79522 8.83227C5.68714 8.76957 5.56791 8.72915 5.44439 8.71335C5.32087 8.69755 5.19549 8.70667 5.07546 8.7402C4.95542 8.77372 4.8431 8.83098 4.74493 8.90869C4.64676 8.9864 4.56469 9.08303 4.50343 9.19302C4.44217 9.30302 4.40293 9.42421 4.38796 9.54965C4.37299 9.67508 4.38259 9.80228 4.4162 9.92394C4.44981 10.0456 4.50677 10.1593 4.58382 10.2586C4.66087 10.3578 4.75647 10.4406 4.86515 10.5023L5.47328 10.8653C5.61859 10.9357 5.77732 10.9728 5.93831 10.9742C6.10769 10.9718 6.27334 10.9234 6.41804 10.834C6.56273 10.7447 6.68118 10.6176 6.76107 10.466C6.82193 10.3592 6.861 10.2411 6.87592 10.1187C6.89085 9.99635 6.88134 9.87216 6.84796 9.75358C6.81457 9.635 6.758 9.52446 6.68161 9.42854C6.60523 9.33263 6.51059 9.25331 6.40335 9.19531Z' fill='%2320133A'/><defs><linearGradient id='paint0_linear_714_179' x1='7.13608e-05' y1='14.001' x2='25.1156' y2='14.001' gradientUnits='userSpaceOnUse'><stop stop-color='%239059FF'/><stop offset='1' stop-color='%23F770FF'/></linearGradient></defs></svg>&quot;); background-repeat: repeat, no-repeat; background-position: 0% 0%, right calc(50% - 0px); background-origin: padding-box, content-box;">
    
    
<button type="button" style="border: 0px; clip: rect(0px, 0px, 0px, 0px); clip-path: inset(50%); height: 1px; margin: 0px -1px -1px 0px; overflow: hidden; padding: 0px; position: absolute; width: 1px; white-space: nowrap;">Gerar nova máscara</button></div>

                                <div class="mb-3">
    <label for="id_sexo" class="form-label">Sexo</label>
    <select name="sexo" class="form-control" id="id_sexo">
  <option value="M" selected="">Masculino</option>

  <option value="F">Feminino</option>

  <option value="O">Outro</option>

</select>
    
    
</div>

                                <div class="mb-3">
    <label for="id_situacao" class="form-label">Situação</label>
    <select name="situacao" class="form-control" aria-describedby="id_situacao_helptext" id="id_situacao">
  <option value="ATIVO" selected="">Ativo</option>

  <option value="AFASTADO">Afastado</option>

  <option value="ESPECIAIS">Especiais</option>

  <option value="EXCLUIDO">Excluído</option>

  <option value="FALECIDO">Falecido</option>

  <option value="LOI">LOI</option>

</select>
    
    
        <small class="form-text text-muted">Selecione a situação atual do aluno.</small>
    
</div>

                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <!-- Moldura tracejada azul brilhante sem cabeçalho -->
                        <div class="border rounded p-3 mb-3 text-center" style="border-style: dashed !important; 
                                    border-color: #007bff !important; 
                                    border-width: 2px !important;
                                    height: 200px; 
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: center;">
                            
                                <div class="text-muted">Sem foto</div>
                            
                        </div>
                        
                        <!-- Campo de upload separado da moldura -->
                        <div class="form-group">
                            <input type="file" name="foto" class="form-control" accept="image/*" id="id_foto">
                            
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-success">
            <div class="card-header bg-success text-white">
                <h5>Dados Iniciáticos</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_numero_iniciatico" class="form-label">Número Iniciático</label>
    <input type="text" name="numero_iniciatico" value="608N" class="form-control" maxlength="10" aria-describedby="id_numero_iniciatico_helptext" id="id_numero_iniciatico">
    
    
        <small class="form-text text-muted">Número único de identificação do iniciado.</small>
    
</div>

                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_nome_iniciatico" class="form-label">Nome Iniciático</label>
    <input type="text" name="nome_iniciatico" value="Moksha" class="form-control" maxlength="100" id="id_nome_iniciatico">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-info">
            <div class="card-header bg-info text-white">
                <h5>Nacionalidade e Naturalidade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_nacionalidade" class="form-label">Nacionalidade</label>
    <input type="text" name="nacionalidade" value="Brasileira" class="form-control" maxlength="50" required="" id="id_nacionalidade">
    
    
</div>

                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_naturalidade" class="form-label">Naturalidade</label>
    <input type="text" name="naturalidade" value="Belo Horizonte" class="form-control" maxlength="50" required="" id="id_naturalidade">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-secondary">
            <div class="card-header bg-secondary text-white">
                <h5>Endereço</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="mb-3">
    <label for="id_rua" class="form-label">Rua</label>
    <input type="text" name="rua" value="Rua Costa 76" class="form-control" maxlength="100" required="" id="id_rua">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_numero_imovel" class="form-label">Número</label>
    <input type="text" name="numero_imovel" value="389" class="form-control" maxlength="10" required="" id="id_numero_imovel">
    
    
</div>

                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_complemento" class="form-label">Complemento</label>
    <input type="text" name="complemento" class="form-control" maxlength="100" id="id_complemento">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_bairro" class="form-label">Bairro</label>
    <input type="text" name="bairro" value="Copacabana" class="form-control" maxlength="50" required="" id="id_bairro">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_cep" class="form-label">CEP</label>
    <input type="text" name="cep" value="10183466" class="form-control" placeholder="Somente números" maxlength="9" required="" aria-describedby="id_cep_helptext" id="id_cep">
    
    
        <small class="form-text text-muted">Digite apenas os 8 números do CEP, sem hífen.</small>
    
</div>

                    </div>
                </div>
                <div class="row">
                    <div class="col-md-8">
                        <div class="mb-3">
    <label for="id_cidade" class="form-label">Cidade</label>
    <input type="text" name="cidade" value="Belo Horizonte" class="form-control" maxlength="50" required="" id="id_cidade">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_estado" class="form-label">Estado</label>
    <input type="text" name="estado" value="MG" class="form-control" maxlength="2" required="" id="id_estado">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-warning">
            <div class="card-header bg-warning text-dark">
                <h5>Contatos de Emergência</h5>
            </div>
            <div class="card-body">
                <h6>Primeiro Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_nome_primeiro_contato" class="form-label">Nome do Primeiro Contato</label>
    <input type="text" name="nome_primeiro_contato" value="Aline Souza" class="form-control" maxlength="100" required="" id="id_nome_primeiro_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_celular_primeiro_contato" class="form-label">Celular do Primeiro Contato</label>
    <input type="text" name="celular_primeiro_contato" value="44913707770" class="form-control" maxlength="15" required="" id="id_celular_primeiro_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_tipo_relacionamento_primeiro_contato" class="form-label">Relacionamento</label>
    <input type="text" name="tipo_relacionamento_primeiro_contato" value="Irmão" class="form-control" maxlength="50" required="" id="id_tipo_relacionamento_primeiro_contato">
    
    
</div>

                    </div>
                </div>
                
                <h6 class="mt-3">Segundo Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_nome_segundo_contato" class="form-label">Nome do Segundo Contato</label>
    <input type="text" name="nome_segundo_contato" value="Lucas Barbosa" class="form-control" maxlength="100" id="id_nome_segundo_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_celular_segundo_contato" class="form-label">Celular do Segundo Contato</label>
    <input type="text" name="celular_segundo_contato" value="16915231124" class="form-control" maxlength="15" id="id_celular_segundo_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_tipo_relacionamento_segundo_contato" class="form-label">Relacionamento</label>
    <input type="text" name="tipo_relacionamento_segundo_contato" value="Irmã" class="form-control" maxlength="50" id="id_tipo_relacionamento_segundo_contato">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-danger">
            <div class="card-header bg-danger text-white">
                <h5>Informações Médicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_tipo_sanguineo" class="form-label">Tipo Sanguíneo</label>
    <input type="text" name="tipo_sanguineo" value="A" class="form-control" maxlength="1" required="" aria-describedby="id_tipo_sanguineo_helptext" id="id_tipo_sanguineo">
    
    
        <small class="form-text text-muted">Ex: A, B, AB, O</small>
    
</div>

                    </div>
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_fator_rh" class="form-label">Fator RH</label>
    <select name="fator_rh" class="form-control" required="" aria-describedby="id_fator_rh_helptext" id="id_fator_rh">
  <option value="">---------</option>

  <option value="+">Positivo</option>

  <option value="-" selected="">Negativo</option>

</select>
    
    
        <small class="form-text text-muted">Positivo (+) ou Negativo (-)</small>
    
</div>

                    </div>
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_convenio_medico" class="form-label">Convênio Médico</label>
    <input type="text" name="convenio_medico" value="Medial Saúde" class="form-control" maxlength="100" id="id_convenio_medico">
    
    
</div>

                    </div>
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_hospital" class="form-label">Hospital de Preferência</label>
    <input type="text" name="hospital" value="Hospital Samaritano" class="form-control" maxlength="100" id="id_hospital">
    
    
</div>

                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_alergias" class="form-label">Alergias</label>
    <textarea name="alergias" cols="40" rows="3" class="form-control" aria-describedby="id_alergias_helptext" id="id_alergias">Nenhuma</textarea>
    
    
        <small class="form-text text-muted">Liste todas as alergias conhecidas. Deixe em branco se não houver.</small>
    
</div>

                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_condicoes_medicas_gerais" class="form-label">Condições Médicas</label>
    <textarea name="condicoes_medicas_gerais" cols="40" rows="3" class="form-control" aria-describedby="id_condicoes_medicas_gerais_helptext" id="id_condicoes_medicas_gerais">Rinite alérgica</textarea>
    
    
        <small class="form-text text-muted">Descreva condições médicas relevantes. Deixe em branco se não houver.</small>
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="/alunos/" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                Atualizar Aluno
            </button>
        </div>    </form>
</div>

    </main>

    <!-- Rodapé -->
    <footer class="bg-dark text-white p-3 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <p>© 2025 OMAUM - Todos os direitos reservados</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p>Versão 1.0</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- JavaScript Bootstrap -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <!-- jQuery e jQuery Mask -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
    <!-- Select2 para melhorar campos de seleção -->
    <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
    <!-- JavaScript Personalizado -->
    <script src="/static/js/alunos/mascaras.js"></script>
    <script src="/static/js/csrf_refresh.js"></script>
    <!-- Inicialização do Select2 -->
    <script>
        $(document).ready(function() {
            // Inicializar Select2 em todos os selects com a classe form-select
            $('.form-select').select2({
                theme: 'bootstrap4',
                width: '100%'
            });
            
            // Inicializar tooltips do Bootstrap
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            });
        });
    </script>
    
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
<script>
    // Script para pré-visualização da imagem quando o usuário seleciona uma foto
    document.addEventListener('DOMContentLoaded', function() {
        const fotoInput = document.getElementById('id_foto');
        if (fotoInput) {
            fotoInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const preview = document.createElement('img');
                    preview.className = 'img-fluid mt-2 rounded';
                    preview.style.maxHeight = '200px';
                    
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                    
                    // Remove qualquer preview anterior
                    const previewContainer = fotoInput.parentNode;
                    const existingPreview = previewContainer.querySelector('img');
                    if (existingPreview) {
                        previewContainer.removeChild(existingPreview);
                    }
                    
                    // Adiciona o novo preview
                    previewContainer.appendChild(preview);
                }
            });
        }
        
        // Aplicar máscaras aos campos
        $('#id_cpf').mask('000.000.000-00', {reverse: true});
        $('#id_cep').mask('00000-000');
        $('#id_celular_primeiro_contato').mask('(00) 00000-0000');
        $('#id_celular_segundo_contato').mask('(00) 00000-0000');
        $('#id_tipo_sanguineo').mask('A', {
            translation: {
                'A': { pattern: /[ABO]/ }
            }
        });
    });
</script>



</body>
Tela de editar_aluno depois da Alteração do nome iniciatico e antes de clicar no botão "Atualizar Aluno":
<body>
    <!-- Cabeçalho -->
    <header class="bg-dark text-white p-3">
        <div class="container">
            <nav class="navbar navbar-expand-lg navbar-dark">
                <a class="navbar-brand" href="/">OMAUM</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" title="Menu de navegação">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        
                            <li class="nav-item"><a class="nav-link" href="/alunos/">Alunos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/cursos/">Cursos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/atividades/academicas/">Atividades Acadêmicas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/atividades/ritualisticas/">Atividades Ritualísticas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/turmas/">Turmas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/iniciacoes/">Iniciações</a></li>
                            <li class="nav-item"><a class="nav-link" href="/cargos/">Cargos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/frequencias/">Frequências</a></li>
                            <li class="nav-item"><a class="nav-link" href="/presencas/">Presenças</a></li>
                            <li class="nav-item"><a class="nav-link" href="/punicoes/">Punições</a></li>
                            
                                <li class="nav-item"><a class="nav-link" href="/painel-controle/">Painel de Controle</a></li>
                            
                        
                    </ul>
                    <div class="navbar-nav">
                        
                            <span class="nav-item nav-link">Olá, lcsilv3</span>
                            <a class="nav-link" href="/sair/">Sair</a>
                        
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <!-- Mensagens -->
    <div class="container mt-3">
        
    </div>

    <!-- Conteúdo Principal -->
    <main class="container py-4">
        
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Aluno: Aline Souza</h1>
        <a href="/alunos/" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    
    
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="csrfmiddlewaretoken" value="cl0Q7D6AF014XUqrqst8xs6j7BERAR1MkCsZRXNR2JMNB8D3NtsY9itJWQz1gvah">
        
        
        <div class="card mb-4 border-primary">
            <div class="card-header bg-primary text-white">
                <h5>Dados Pessoais</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
    <label for="id_cpf" class="form-label">Cpf</label>
    <input type="text" name="cpf" value="18027737038" class="form-control" placeholder="Somente números" required="" id="id_cpf" maxlength="14">
    
    
</div>

                                <div class="mb-3">
    <label for="id_nome" class="form-label">Nome Completo</label>
    <input type="text" name="nome" value="Aline Souza" class="form-control" maxlength="100" required="" id="id_nome">
    
    
</div>

                                <div class="mb-3">
    <label for="id_data_nascimento" class="form-label">Data de Nascimento</label>
    <input type="date" name="data_nascimento" value="22/12/2000" class="form-control" required="" aria-describedby="id_data_nascimento_helptext" id="id_data_nascimento">
    
    
        <small class="form-text text-muted">Formato: DD/MM/AAAA</small>
    
</div>

                                <div class="mb-3">
    <label for="id_hora_nascimento" class="form-label">Hora de Nascimento</label>
    <input type="time" name="hora_nascimento" value="15:02:00" class="form-control" aria-describedby="id_hora_nascimento_helptext" id="id_hora_nascimento">
    
    
        <small class="form-text text-muted">Formato: HH:MM</small>
    
</div>

                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
    <label for="id_email" class="form-label">E-mail</label>
    <input type="email" name="email" value="aline.souza@exemplo.com" class="form-control" maxlength="254" required="" id="id_email" style="background-size: auto, 25px; background-image: none, url(&quot;data:image/svg+xml;utf8,<svg width='26' height='28' viewBox='0 0 26 28' fill='none' xmlns='http://www.w3.org/2000/svg'><path d='M23.8958 6.1084L13.7365 0.299712C13.3797 0.103027 12.98 0 12.5739 0C12.1678 0 11.7682 0.103027 11.4113 0.299712L1.21632 6.1084C0.848276 6.31893 0.54181 6.62473 0.328154 6.99462C0.114498 7.36452 0.00129162 7.78529 7.13608e-05 8.21405V19.7951C-0.00323007 20.2248 0.108078 20.6474 0.322199 21.0181C0.53632 21.3888 0.845275 21.6938 1.21632 21.9008L11.3756 27.6732C11.7318 27.8907 12.1404 28.0037 12.556 27.9999C12.9711 27.9989 13.3784 27.8861 13.7365 27.6732L23.8958 21.9008C24.2638 21.6903 24.5703 21.3845 24.7839 21.0146C24.9976 20.6447 25.1108 20.2239 25.112 19.7951V8.21405C25.1225 7.78296 25.0142 7.35746 24.7994 6.98545C24.5845 6.61343 24.2715 6.30969 23.8958 6.1084Z' fill='url(%23paint0_linear_714_179)'/><path d='M5.47328 17.037L4.86515 17.4001C4.75634 17.4613 4.66062 17.5439 4.58357 17.643C4.50652 17.7421 4.4497 17.8558 4.4164 17.9775C4.3831 18.0991 4.374 18.2263 4.38963 18.3516C4.40526 18.4768 4.44531 18.5977 4.50743 18.707C4.58732 18.8586 4.70577 18.9857 4.85046 19.0751C4.99516 19.1645 5.16081 19.2129 5.33019 19.2153C5.49118 19.2139 5.64992 19.1767 5.79522 19.1064L6.40335 18.7434C6.51216 18.6822 6.60789 18.5996 6.68493 18.5004C6.76198 18.4013 6.8188 18.2876 6.8521 18.166C6.8854 18.0443 6.8945 17.9171 6.87887 17.7919C6.86324 17.6666 6.82319 17.5458 6.76107 17.4364C6.70583 17.3211 6.62775 17.2185 6.53171 17.1352C6.43567 17.0518 6.32374 16.9895 6.20289 16.952C6.08205 16.9145 5.95489 16.9027 5.82935 16.9174C5.70382 16.932 5.5826 16.9727 5.47328 17.037ZM9.19357 14.8951L7.94155 15.6212C7.83273 15.6824 7.73701 15.7649 7.65996 15.8641C7.58292 15.9632 7.52609 16.0769 7.49279 16.1986C7.4595 16.3202 7.4504 16.4474 7.46603 16.5726C7.48166 16.6979 7.5217 16.8187 7.58383 16.9281C7.66371 17.0797 7.78216 17.2068 7.92686 17.2962C8.07155 17.3856 8.23721 17.434 8.40658 17.4364C8.56757 17.435 8.72631 17.3978 8.87162 17.3275L10.1236 16.6014C10.2325 16.5402 10.3282 16.4576 10.4052 16.3585C10.4823 16.2594 10.5391 16.1457 10.5724 16.024C10.6057 15.9024 10.6148 15.7752 10.5992 15.6499C10.5835 15.5247 10.5435 15.4038 10.4814 15.2944C10.4261 15.1791 10.348 15.0766 10.252 14.9932C10.156 14.9099 10.044 14.8475 9.92318 14.8101C9.80234 14.7726 9.67518 14.7608 9.54964 14.7754C9.42411 14.7901 9.30289 14.8308 9.19357 14.8951ZM14.2374 13.1198C14.187 13.0168 14.1167 12.9251 14.0307 12.8503C13.9446 12.7754 13.8446 12.7189 13.7366 12.6842V5.38336C13.7371 5.2545 13.7124 5.12682 13.6641 5.00768C13.6157 4.88854 13.5446 4.78029 13.4548 4.68917C13.365 4.59806 13.2583 4.52587 13.1409 4.47678C13.0235 4.42769 12.8977 4.40266 12.7708 4.40314C12.6457 4.40355 12.522 4.42946 12.407 4.47933C12.292 4.52919 12.188 4.602 12.1013 4.69343C12.0145 4.78485 11.9467 4.89304 11.902 5.01156C11.8572 5.13007 11.8364 5.25651 11.8407 5.38336V12.7168C11.7327 12.7516 11.6327 12.8081 11.5466 12.883C11.4606 12.9578 11.3903 13.0495 11.3399 13.1525C11.2727 13.2801 11.2346 13.4213 11.2284 13.5659C11.2222 13.7104 11.2481 13.8545 11.3041 13.9875C11.2481 14.1205 11.2222 14.2646 11.2284 14.4091C11.2346 14.5536 11.2727 14.6949 11.3399 14.8225C11.3903 14.9255 11.4606 15.0172 11.5466 15.092C11.6327 15.1669 11.7327 15.2233 11.8407 15.2581V22.5916C11.8407 22.8516 11.9425 23.1009 12.1236 23.2847C12.3047 23.4686 12.5504 23.5718 12.8065 23.5718C13.0627 23.5718 13.3084 23.4686 13.4895 23.2847C13.6706 23.1009 13.7724 22.8516 13.7724 22.5916V15.2218C13.8804 15.187 13.9804 15.1305 14.0664 15.0557C14.1525 14.9809 14.2228 14.8892 14.2732 14.7862C14.3404 14.6586 14.3785 14.5173 14.3847 14.3728C14.3909 14.2283 14.365 14.0842 14.309 13.9512C14.3917 13.6751 14.3661 13.3772 14.2374 13.1198ZM16.6735 10.6112L15.4215 11.3373C15.3127 11.3985 15.2169 11.481 15.1399 11.5802C15.0628 11.6793 15.006 11.793 14.9727 11.9147C14.9394 12.0363 14.9303 12.1635 14.946 12.2887C14.9616 12.414 15.0016 12.5348 15.0638 12.6442C15.1436 12.7958 15.2621 12.9229 15.4068 13.0123C15.5515 13.1017 15.7171 13.1501 15.8865 13.1525C16.0475 13.1511 16.2062 13.1139 16.3515 13.0436L17.6036 12.3175C17.7124 12.2563 17.8081 12.1737 17.8851 12.0746C17.9622 11.9755 18.019 11.8617 18.0523 11.7401C18.0856 11.6184 18.0947 11.4913 18.0791 11.366C18.0635 11.2408 18.0234 11.1199 17.9613 11.0105C17.906 10.8952 17.828 10.7927 17.7319 10.7093C17.6359 10.626 17.524 10.5636 17.4031 10.5261C17.2823 10.4887 17.1551 10.4769 17.0296 10.4915C16.904 10.5061 16.7828 10.5469 16.6735 10.6112ZM19.639 10.9742C19.8 10.9728 19.9587 10.9357 20.104 10.8653L20.7122 10.5023C20.8208 10.4406 20.9164 10.3578 20.9935 10.2586C21.0705 10.1593 21.1275 10.0456 21.1611 9.92394C21.1947 9.80228 21.2043 9.67508 21.1893 9.54965C21.1744 9.42421 21.1351 9.30302 21.0739 9.19302C21.0126 9.08303 20.9305 8.9864 20.8324 8.90869C20.7342 8.83098 20.6219 8.77372 20.5019 8.7402C20.3818 8.70667 20.2564 8.69755 20.1329 8.71335C20.0094 8.72915 19.8902 8.76957 19.7821 8.83227L19.174 9.19531C19.0651 9.25651 18.9694 9.33909 18.8924 9.43822C18.8153 9.53735 18.7585 9.65106 18.7252 9.77271C18.6919 9.89436 18.6828 10.0215 18.6984 10.1468C18.7141 10.272 18.7541 10.3929 18.8162 10.5023C18.8981 10.6494 19.018 10.7711 19.163 10.8543C19.308 10.9374 19.4725 10.9789 19.639 10.9742ZM20.7122 17.4001L20.104 17.037C19.8859 16.9133 19.6284 16.8823 19.3878 16.9508C19.1472 17.0193 18.9432 17.1816 18.8202 17.4024C18.6973 17.6231 18.6655 17.8843 18.7318 18.1288C18.798 18.3733 18.957 18.5812 19.174 18.707L19.7821 19.0701C19.9274 19.1404 20.0861 19.1776 20.2471 19.179C20.4165 19.1766 20.5821 19.1282 20.7268 19.0388C20.8715 18.9494 20.99 18.8223 21.0699 18.6707C21.1339 18.5648 21.1755 18.4466 21.1921 18.3235C21.2087 18.2003 21.1999 18.0751 21.1662 17.9556C21.1326 17.8361 21.0749 17.7251 20.9967 17.6294C20.9185 17.5338 20.8216 17.4557 20.7122 17.4001ZM17.6 15.6212L16.348 14.8951C16.2399 14.8324 16.1207 14.792 15.9971 14.7762C15.8736 14.7604 15.7482 14.7695 15.6282 14.803C15.5082 14.8365 15.3958 14.8938 15.2977 14.9715C15.1995 15.0492 15.1174 15.1458 15.0562 15.2558C14.9949 15.3658 14.9557 15.487 14.9407 15.6125C14.9257 15.7379 14.9353 15.8651 14.9689 15.9868C15.0026 16.1084 15.0595 16.2221 15.1366 16.3214C15.2136 16.4206 15.3092 16.5035 15.4179 16.5651L16.6699 17.2912C16.8152 17.3615 16.974 17.3987 17.135 17.4001C17.3043 17.3977 17.47 17.3493 17.6147 17.2599C17.7594 17.1705 17.8778 17.0434 17.9577 16.8918C18.0228 16.7862 18.0653 16.6679 18.0825 16.5445C18.0997 16.4212 18.0911 16.2955 18.0574 16.1757C18.0237 16.0559 17.9655 15.9447 17.8867 15.8491C17.8079 15.7536 17.7103 15.6759 17.6 15.6212ZM7.94155 12.2812L9.19357 13.0073C9.33888 13.0776 9.49761 13.1148 9.6586 13.1162C9.82798 13.1138 9.99363 13.0654 10.1383 12.976C10.283 12.8866 10.4015 12.7595 10.4814 12.6079C10.5435 12.4985 10.5835 12.3777 10.5992 12.2524C10.6148 12.1272 10.6057 12 10.5724 11.8784C10.5391 11.7567 10.4823 11.643 10.4052 11.5439C10.3282 11.4447 10.2325 11.3622 10.1236 11.301L8.87162 10.5749C8.76383 10.5118 8.64476 10.4712 8.52134 10.4553C8.39792 10.4395 8.27262 10.4487 8.15275 10.4825C8.03288 10.5163 7.92084 10.574 7.82317 10.6521C7.72549 10.7303 7.64413 10.8275 7.58383 10.9379C7.46399 11.166 7.43428 11.4319 7.50073 11.6814C7.56719 11.9309 7.72481 12.1454 7.94155 12.2812ZM6.40335 9.19531L5.79522 8.83227C5.68714 8.76957 5.56791 8.72915 5.44439 8.71335C5.32087 8.69755 5.19549 8.70667 5.07546 8.7402C4.95542 8.77372 4.8431 8.83098 4.74493 8.90869C4.64676 8.9864 4.56469 9.08303 4.50343 9.19302C4.44217 9.30302 4.40293 9.42421 4.38796 9.54965C4.37299 9.67508 4.38259 9.80228 4.4162 9.92394C4.44981 10.0456 4.50677 10.1593 4.58382 10.2586C4.66087 10.3578 4.75647 10.4406 4.86515 10.5023L5.47328 10.8653C5.61859 10.9357 5.77732 10.9728 5.93831 10.9742C6.10769 10.9718 6.27334 10.9234 6.41804 10.834C6.56273 10.7447 6.68118 10.6176 6.76107 10.466C6.82193 10.3592 6.861 10.2411 6.87592 10.1187C6.89085 9.99635 6.88134 9.87216 6.84796 9.75358C6.81457 9.635 6.758 9.52446 6.68161 9.42854C6.60523 9.33263 6.51059 9.25331 6.40335 9.19531Z' fill='%2320133A'/><defs><linearGradient id='paint0_linear_714_179' x1='7.13608e-05' y1='14.001' x2='25.1156' y2='14.001' gradientUnits='userSpaceOnUse'><stop stop-color='%239059FF'/><stop offset='1' stop-color='%23F770FF'/></linearGradient></defs></svg>&quot;); background-repeat: repeat, no-repeat; background-position: 0% 0%, right calc(50% - 0px); background-origin: padding-box, content-box;">
    
    
<button type="button" style="border: 0px; clip: rect(0px, 0px, 0px, 0px); clip-path: inset(50%); height: 1px; margin: 0px -1px -1px 0px; overflow: hidden; padding: 0px; position: absolute; width: 1px; white-space: nowrap;">Gerar nova máscara</button></div>

                                <div class="mb-3">
    <label for="id_sexo" class="form-label">Sexo</label>
    <select name="sexo" class="form-control" id="id_sexo">
  <option value="M" selected="">Masculino</option>

  <option value="F">Feminino</option>

  <option value="O">Outro</option>

</select>
    
    
</div>

                                <div class="mb-3">
    <label for="id_situacao" class="form-label">Situação</label>
    <select name="situacao" class="form-control" aria-describedby="id_situacao_helptext" id="id_situacao">
  <option value="ATIVO" selected="">Ativo</option>

  <option value="AFASTADO">Afastado</option>

  <option value="ESPECIAIS">Especiais</option>

  <option value="EXCLUIDO">Excluído</option>

  <option value="FALECIDO">Falecido</option>

  <option value="LOI">LOI</option>

</select>
    
    
        <small class="form-text text-muted">Selecione a situação atual do aluno.</small>
    
</div>

                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <!-- Moldura tracejada azul brilhante sem cabeçalho -->
                        <div class="border rounded p-3 mb-3 text-center" style="border-style: dashed !important; 
                                    border-color: #007bff !important; 
                                    border-width: 2px !important;
                                    height: 200px; 
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: center;">
                            
                                <div class="text-muted">Sem foto</div>
                            
                        </div>
                        
                        <!-- Campo de upload separado da moldura -->
                        <div class="form-group">
                            <input type="file" name="foto" class="form-control" accept="image/*" id="id_foto">
                            
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-success">
            <div class="card-header bg-success text-white">
                <h5>Dados Iniciáticos</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_numero_iniciatico" class="form-label">Número Iniciático</label>
    <input type="text" name="numero_iniciatico" value="608N" class="form-control" maxlength="10" aria-describedby="id_numero_iniciatico_helptext" id="id_numero_iniciatico">
    
    
        <small class="form-text text-muted">Número único de identificação do iniciado.</small>
    
</div>

                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_nome_iniciatico" class="form-label">Nome Iniciático</label>
    <input type="text" name="nome_iniciatico" value="Moksha" class="form-control" maxlength="100" id="id_nome_iniciatico">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-info">
            <div class="card-header bg-info text-white">
                <h5>Nacionalidade e Naturalidade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_nacionalidade" class="form-label">Nacionalidade</label>
    <input type="text" name="nacionalidade" value="Brasileira" class="form-control" maxlength="50" required="" id="id_nacionalidade">
    
    
</div>

                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_naturalidade" class="form-label">Naturalidade</label>
    <input type="text" name="naturalidade" value="Belo Horizonte" class="form-control" maxlength="50" required="" id="id_naturalidade">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-secondary">
            <div class="card-header bg-secondary text-white">
                <h5>Endereço</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="mb-3">
    <label for="id_rua" class="form-label">Rua</label>
    <input type="text" name="rua" value="Rua Costa 76" class="form-control" maxlength="100" required="" id="id_rua">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_numero_imovel" class="form-label">Número</label>
    <input type="text" name="numero_imovel" value="389" class="form-control" maxlength="10" required="" id="id_numero_imovel">
    
    
</div>

                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_complemento" class="form-label">Complemento</label>
    <input type="text" name="complemento" class="form-control" maxlength="100" id="id_complemento">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_bairro" class="form-label">Bairro</label>
    <input type="text" name="bairro" value="Copacabana" class="form-control" maxlength="50" required="" id="id_bairro">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_cep" class="form-label">CEP</label>
    <input type="text" name="cep" value="10183466" class="form-control" placeholder="Somente números" maxlength="9" required="" aria-describedby="id_cep_helptext" id="id_cep">
    
    
        <small class="form-text text-muted">Digite apenas os 8 números do CEP, sem hífen.</small>
    
</div>

                    </div>
                </div>
                <div class="row">
                    <div class="col-md-8">
                        <div class="mb-3">
    <label for="id_cidade" class="form-label">Cidade</label>
    <input type="text" name="cidade" value="Belo Horizonte" class="form-control" maxlength="50" required="" id="id_cidade">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_estado" class="form-label">Estado</label>
    <input type="text" name="estado" value="MG" class="form-control" maxlength="2" required="" id="id_estado">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-warning">
            <div class="card-header bg-warning text-dark">
                <h5>Contatos de Emergência</h5>
            </div>
            <div class="card-body">
                <h6>Primeiro Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_nome_primeiro_contato" class="form-label">Nome do Primeiro Contato</label>
    <input type="text" name="nome_primeiro_contato" value="Aline Souza" class="form-control" maxlength="100" required="" id="id_nome_primeiro_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_celular_primeiro_contato" class="form-label">Celular do Primeiro Contato</label>
    <input type="text" name="celular_primeiro_contato" value="44913707770" class="form-control" maxlength="15" required="" id="id_celular_primeiro_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_tipo_relacionamento_primeiro_contato" class="form-label">Relacionamento</label>
    <input type="text" name="tipo_relacionamento_primeiro_contato" value="Irmão" class="form-control" maxlength="50" required="" id="id_tipo_relacionamento_primeiro_contato">
    
    
</div>

                    </div>
                </div>
                
                <h6 class="mt-3">Segundo Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_nome_segundo_contato" class="form-label">Nome do Segundo Contato</label>
    <input type="text" name="nome_segundo_contato" value="Lucas Barbosa" class="form-control" maxlength="100" id="id_nome_segundo_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_celular_segundo_contato" class="form-label">Celular do Segundo Contato</label>
    <input type="text" name="celular_segundo_contato" value="16915231124" class="form-control" maxlength="15" id="id_celular_segundo_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_tipo_relacionamento_segundo_contato" class="form-label">Relacionamento</label>
    <input type="text" name="tipo_relacionamento_segundo_contato" value="Irmã" class="form-control" maxlength="50" id="id_tipo_relacionamento_segundo_contato">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-danger">
            <div class="card-header bg-danger text-white">
                <h5>Informações Médicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_tipo_sanguineo" class="form-label">Tipo Sanguíneo</label>
    <input type="text" name="tipo_sanguineo" value="A" class="form-control" maxlength="1" required="" aria-describedby="id_tipo_sanguineo_helptext" id="id_tipo_sanguineo">
    
    
        <small class="form-text text-muted">Ex: A, B, AB, O</small>
    
</div>

                    </div>
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_fator_rh" class="form-label">Fator RH</label>
    <select name="fator_rh" class="form-control" required="" aria-describedby="id_fator_rh_helptext" id="id_fator_rh">
  <option value="">---------</option>

  <option value="+">Positivo</option>

  <option value="-" selected="">Negativo</option>

</select>
    
    
        <small class="form-text text-muted">Positivo (+) ou Negativo (-)</small>
    
</div>

                    </div>
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_convenio_medico" class="form-label">Convênio Médico</label>
    <input type="text" name="convenio_medico" value="Medial Saúde" class="form-control" maxlength="100" id="id_convenio_medico">
    
    
</div>

                    </div>
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_hospital" class="form-label">Hospital de Preferência</label>
    <input type="text" name="hospital" value="Hospital Samaritano" class="form-control" maxlength="100" id="id_hospital">
    
    
</div>

                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_alergias" class="form-label">Alergias</label>
    <textarea name="alergias" cols="40" rows="3" class="form-control" aria-describedby="id_alergias_helptext" id="id_alergias">Nenhuma</textarea>
    
    
        <small class="form-text text-muted">Liste todas as alergias conhecidas. Deixe em branco se não houver.</small>
    
</div>

                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_condicoes_medicas_gerais" class="form-label">Condições Médicas</label>
    <textarea name="condicoes_medicas_gerais" cols="40" rows="3" class="form-control" aria-describedby="id_condicoes_medicas_gerais_helptext" id="id_condicoes_medicas_gerais">Rinite alérgica</textarea>
    
    
        <small class="form-text text-muted">Descreva condições médicas relevantes. Deixe em branco se não houver.</small>
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="/alunos/" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                Atualizar Aluno
            </button>
        </div>    </form>
</div>

    </main>

    <!-- Rodapé -->
    <footer class="bg-dark text-white p-3 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <p>© 2025 OMAUM - Todos os direitos reservados</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p>Versão 1.0</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- JavaScript Bootstrap -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <!-- jQuery e jQuery Mask -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
    <!-- Select2 para melhorar campos de seleção -->
    <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
    <!-- JavaScript Personalizado -->
    <script src="/static/js/alunos/mascaras.js"></script>
    <script src="/static/js/csrf_refresh.js"></script>
    <!-- Inicialização do Select2 -->
    <script>
        $(document).ready(function() {
            // Inicializar Select2 em todos os selects com a classe form-select
            $('.form-select').select2({
                theme: 'bootstrap4',
                width: '100%'
            });
            
            // Inicializar tooltips do Bootstrap
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            });
        });
    </script>
    
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
<script>
    // Script para pré-visualização da imagem quando o usuário seleciona uma foto
    document.addEventListener('DOMContentLoaded', function() {
        const fotoInput = document.getElementById('id_foto');
        if (fotoInput) {
            fotoInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const preview = document.createElement('img');
                    preview.className = 'img-fluid mt-2 rounded';
                    preview.style.maxHeight = '200px';
                    
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                    
                    // Remove qualquer preview anterior
                    const previewContainer = fotoInput.parentNode;
                    const existingPreview = previewContainer.querySelector('img');
                    if (existingPreview) {
                        previewContainer.removeChild(existingPreview);
                    }
                    
                    // Adiciona o novo preview
                    previewContainer.appendChild(preview);
                }
            });
        }
        
        // Aplicar máscaras aos campos
        $('#id_cpf').mask('000.000.000-00', {reverse: true});
        $('#id_cep').mask('00000-000');
        $('#id_celular_primeiro_contato').mask('(00) 00000-0000');
        $('#id_celular_segundo_contato').mask('(00) 00000-0000');
        $('#id_tipo_sanguineo').mask('A', {
            translation: {
                'A': { pattern: /[ABO]/ }
            }
        });
    });
</script>



</body>
Tela editar_aluno depois de clickar no botão "Atualizar aluno":
<body>
    <!-- Cabeçalho -->
    <header class="bg-dark text-white p-3">
        <div class="container">
            <nav class="navbar navbar-expand-lg navbar-dark">
                <a class="navbar-brand" href="/">OMAUM</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" title="Menu de navegação">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        
                            <li class="nav-item"><a class="nav-link" href="/alunos/">Alunos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/cursos/">Cursos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/atividades/academicas/">Atividades Acadêmicas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/atividades/ritualisticas/">Atividades Ritualísticas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/turmas/">Turmas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/iniciacoes/">Iniciações</a></li>
                            <li class="nav-item"><a class="nav-link" href="/cargos/">Cargos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/frequencias/">Frequências</a></li>
                            <li class="nav-item"><a class="nav-link" href="/presencas/">Presenças</a></li>
                            <li class="nav-item"><a class="nav-link" href="/punicoes/">Punições</a></li>
                            
                                <li class="nav-item"><a class="nav-link" href="/painel-controle/">Painel de Controle</a></li>
                            
                        
                    </ul>
                    <div class="navbar-nav">
                        
                            <span class="nav-item nav-link">Olá, lcsilv3</span>
                            <a class="nav-link" href="/sair/">Sair</a>
                        
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <!-- Mensagens -->
    <div class="container mt-3">
        
    </div>

    <!-- Conteúdo Principal -->
    <main class="container py-4">
        
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Aluno: Aline Souza</h1>
        <a href="/alunos/" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    
    
    <form method="post" enctype="multipart/form-data">
        <input type="hidden" name="csrfmiddlewaretoken" value="cl0Q7D6AF014XUqrqst8xs6j7BERAR1MkCsZRXNR2JMNB8D3NtsY9itJWQz1gvah">
        
        
        <div class="card mb-4 border-primary">
            <div class="card-header bg-primary text-white">
                <h5>Dados Pessoais</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
    <label for="id_cpf" class="form-label">Cpf</label>
    <input type="text" name="cpf" value="18027737038" class="form-control" placeholder="Somente números" required="" id="id_cpf" maxlength="14">
    
    
</div>

                                <div class="mb-3">
    <label for="id_nome" class="form-label">Nome Completo</label>
    <input type="text" name="nome" value="Aline Souza" class="form-control" maxlength="100" required="" id="id_nome">
    
    
</div>

                                <div class="mb-3">
    <label for="id_data_nascimento" class="form-label">Data de Nascimento</label>
    <input type="date" name="data_nascimento" value="22/12/2000" class="form-control" required="" aria-describedby="id_data_nascimento_helptext" id="id_data_nascimento">
    
    
        <small class="form-text text-muted">Formato: DD/MM/AAAA</small>
    
</div>

                                <div class="mb-3">
    <label for="id_hora_nascimento" class="form-label">Hora de Nascimento</label>
    <input type="time" name="hora_nascimento" value="15:02:00" class="form-control" aria-describedby="id_hora_nascimento_helptext" id="id_hora_nascimento">
    
    
        <small class="form-text text-muted">Formato: HH:MM</small>
    
</div>

                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
    <label for="id_email" class="form-label">E-mail</label>
    <input type="email" name="email" value="aline.souza@exemplo.com" class="form-control" maxlength="254" required="" id="id_email" style="background-size: auto, 25px; background-image: none, url(&quot;data:image/svg+xml;utf8,<svg width='26' height='28' viewBox='0 0 26 28' fill='none' xmlns='http://www.w3.org/2000/svg'><path d='M23.8958 6.1084L13.7365 0.299712C13.3797 0.103027 12.98 0 12.5739 0C12.1678 0 11.7682 0.103027 11.4113 0.299712L1.21632 6.1084C0.848276 6.31893 0.54181 6.62473 0.328154 6.99462C0.114498 7.36452 0.00129162 7.78529 7.13608e-05 8.21405V19.7951C-0.00323007 20.2248 0.108078 20.6474 0.322199 21.0181C0.53632 21.3888 0.845275 21.6938 1.21632 21.9008L11.3756 27.6732C11.7318 27.8907 12.1404 28.0037 12.556 27.9999C12.9711 27.9989 13.3784 27.8861 13.7365 27.6732L23.8958 21.9008C24.2638 21.6903 24.5703 21.3845 24.7839 21.0146C24.9976 20.6447 25.1108 20.2239 25.112 19.7951V8.21405C25.1225 7.78296 25.0142 7.35746 24.7994 6.98545C24.5845 6.61343 24.2715 6.30969 23.8958 6.1084Z' fill='url(%23paint0_linear_714_179)'/><path d='M5.47328 17.037L4.86515 17.4001C4.75634 17.4613 4.66062 17.5439 4.58357 17.643C4.50652 17.7421 4.4497 17.8558 4.4164 17.9775C4.3831 18.0991 4.374 18.2263 4.38963 18.3516C4.40526 18.4768 4.44531 18.5977 4.50743 18.707C4.58732 18.8586 4.70577 18.9857 4.85046 19.0751C4.99516 19.1645 5.16081 19.2129 5.33019 19.2153C5.49118 19.2139 5.64992 19.1767 5.79522 19.1064L6.40335 18.7434C6.51216 18.6822 6.60789 18.5996 6.68493 18.5004C6.76198 18.4013 6.8188 18.2876 6.8521 18.166C6.8854 18.0443 6.8945 17.9171 6.87887 17.7919C6.86324 17.6666 6.82319 17.5458 6.76107 17.4364C6.70583 17.3211 6.62775 17.2185 6.53171 17.1352C6.43567 17.0518 6.32374 16.9895 6.20289 16.952C6.08205 16.9145 5.95489 16.9027 5.82935 16.9174C5.70382 16.932 5.5826 16.9727 5.47328 17.037ZM9.19357 14.8951L7.94155 15.6212C7.83273 15.6824 7.73701 15.7649 7.65996 15.8641C7.58292 15.9632 7.52609 16.0769 7.49279 16.1986C7.4595 16.3202 7.4504 16.4474 7.46603 16.5726C7.48166 16.6979 7.5217 16.8187 7.58383 16.9281C7.66371 17.0797 7.78216 17.2068 7.92686 17.2962C8.07155 17.3856 8.23721 17.434 8.40658 17.4364C8.56757 17.435 8.72631 17.3978 8.87162 17.3275L10.1236 16.6014C10.2325 16.5402 10.3282 16.4576 10.4052 16.3585C10.4823 16.2594 10.5391 16.1457 10.5724 16.024C10.6057 15.9024 10.6148 15.7752 10.5992 15.6499C10.5835 15.5247 10.5435 15.4038 10.4814 15.2944C10.4261 15.1791 10.348 15.0766 10.252 14.9932C10.156 14.9099 10.044 14.8475 9.92318 14.8101C9.80234 14.7726 9.67518 14.7608 9.54964 14.7754C9.42411 14.7901 9.30289 14.8308 9.19357 14.8951ZM14.2374 13.1198C14.187 13.0168 14.1167 12.9251 14.0307 12.8503C13.9446 12.7754 13.8446 12.7189 13.7366 12.6842V5.38336C13.7371 5.2545 13.7124 5.12682 13.6641 5.00768C13.6157 4.88854 13.5446 4.78029 13.4548 4.68917C13.365 4.59806 13.2583 4.52587 13.1409 4.47678C13.0235 4.42769 12.8977 4.40266 12.7708 4.40314C12.6457 4.40355 12.522 4.42946 12.407 4.47933C12.292 4.52919 12.188 4.602 12.1013 4.69343C12.0145 4.78485 11.9467 4.89304 11.902 5.01156C11.8572 5.13007 11.8364 5.25651 11.8407 5.38336V12.7168C11.7327 12.7516 11.6327 12.8081 11.5466 12.883C11.4606 12.9578 11.3903 13.0495 11.3399 13.1525C11.2727 13.2801 11.2346 13.4213 11.2284 13.5659C11.2222 13.7104 11.2481 13.8545 11.3041 13.9875C11.2481 14.1205 11.2222 14.2646 11.2284 14.4091C11.2346 14.5536 11.2727 14.6949 11.3399 14.8225C11.3903 14.9255 11.4606 15.0172 11.5466 15.092C11.6327 15.1669 11.7327 15.2233 11.8407 15.2581V22.5916C11.8407 22.8516 11.9425 23.1009 12.1236 23.2847C12.3047 23.4686 12.5504 23.5718 12.8065 23.5718C13.0627 23.5718 13.3084 23.4686 13.4895 23.2847C13.6706 23.1009 13.7724 22.8516 13.7724 22.5916V15.2218C13.8804 15.187 13.9804 15.1305 14.0664 15.0557C14.1525 14.9809 14.2228 14.8892 14.2732 14.7862C14.3404 14.6586 14.3785 14.5173 14.3847 14.3728C14.3909 14.2283 14.365 14.0842 14.309 13.9512C14.3917 13.6751 14.3661 13.3772 14.2374 13.1198ZM16.6735 10.6112L15.4215 11.3373C15.3127 11.3985 15.2169 11.481 15.1399 11.5802C15.0628 11.6793 15.006 11.793 14.9727 11.9147C14.9394 12.0363 14.9303 12.1635 14.946 12.2887C14.9616 12.414 15.0016 12.5348 15.0638 12.6442C15.1436 12.7958 15.2621 12.9229 15.4068 13.0123C15.5515 13.1017 15.7171 13.1501 15.8865 13.1525C16.0475 13.1511 16.2062 13.1139 16.3515 13.0436L17.6036 12.3175C17.7124 12.2563 17.8081 12.1737 17.8851 12.0746C17.9622 11.9755 18.019 11.8617 18.0523 11.7401C18.0856 11.6184 18.0947 11.4913 18.0791 11.366C18.0635 11.2408 18.0234 11.1199 17.9613 11.0105C17.906 10.8952 17.828 10.7927 17.7319 10.7093C17.6359 10.626 17.524 10.5636 17.4031 10.5261C17.2823 10.4887 17.1551 10.4769 17.0296 10.4915C16.904 10.5061 16.7828 10.5469 16.6735 10.6112ZM19.639 10.9742C19.8 10.9728 19.9587 10.9357 20.104 10.8653L20.7122 10.5023C20.8208 10.4406 20.9164 10.3578 20.9935 10.2586C21.0705 10.1593 21.1275 10.0456 21.1611 9.92394C21.1947 9.80228 21.2043 9.67508 21.1893 9.54965C21.1744 9.42421 21.1351 9.30302 21.0739 9.19302C21.0126 9.08303 20.9305 8.9864 20.8324 8.90869C20.7342 8.83098 20.6219 8.77372 20.5019 8.7402C20.3818 8.70667 20.2564 8.69755 20.1329 8.71335C20.0094 8.72915 19.8902 8.76957 19.7821 8.83227L19.174 9.19531C19.0651 9.25651 18.9694 9.33909 18.8924 9.43822C18.8153 9.53735 18.7585 9.65106 18.7252 9.77271C18.6919 9.89436 18.6828 10.0215 18.6984 10.1468C18.7141 10.272 18.7541 10.3929 18.8162 10.5023C18.8981 10.6494 19.018 10.7711 19.163 10.8543C19.308 10.9374 19.4725 10.9789 19.639 10.9742ZM20.7122 17.4001L20.104 17.037C19.8859 16.9133 19.6284 16.8823 19.3878 16.9508C19.1472 17.0193 18.9432 17.1816 18.8202 17.4024C18.6973 17.6231 18.6655 17.8843 18.7318 18.1288C18.798 18.3733 18.957 18.5812 19.174 18.707L19.7821 19.0701C19.9274 19.1404 20.0861 19.1776 20.2471 19.179C20.4165 19.1766 20.5821 19.1282 20.7268 19.0388C20.8715 18.9494 20.99 18.8223 21.0699 18.6707C21.1339 18.5648 21.1755 18.4466 21.1921 18.3235C21.2087 18.2003 21.1999 18.0751 21.1662 17.9556C21.1326 17.8361 21.0749 17.7251 20.9967 17.6294C20.9185 17.5338 20.8216 17.4557 20.7122 17.4001ZM17.6 15.6212L16.348 14.8951C16.2399 14.8324 16.1207 14.792 15.9971 14.7762C15.8736 14.7604 15.7482 14.7695 15.6282 14.803C15.5082 14.8365 15.3958 14.8938 15.2977 14.9715C15.1995 15.0492 15.1174 15.1458 15.0562 15.2558C14.9949 15.3658 14.9557 15.487 14.9407 15.6125C14.9257 15.7379 14.9353 15.8651 14.9689 15.9868C15.0026 16.1084 15.0595 16.2221 15.1366 16.3214C15.2136 16.4206 15.3092 16.5035 15.4179 16.5651L16.6699 17.2912C16.8152 17.3615 16.974 17.3987 17.135 17.4001C17.3043 17.3977 17.47 17.3493 17.6147 17.2599C17.7594 17.1705 17.8778 17.0434 17.9577 16.8918C18.0228 16.7862 18.0653 16.6679 18.0825 16.5445C18.0997 16.4212 18.0911 16.2955 18.0574 16.1757C18.0237 16.0559 17.9655 15.9447 17.8867 15.8491C17.8079 15.7536 17.7103 15.6759 17.6 15.6212ZM7.94155 12.2812L9.19357 13.0073C9.33888 13.0776 9.49761 13.1148 9.6586 13.1162C9.82798 13.1138 9.99363 13.0654 10.1383 12.976C10.283 12.8866 10.4015 12.7595 10.4814 12.6079C10.5435 12.4985 10.5835 12.3777 10.5992 12.2524C10.6148 12.1272 10.6057 12 10.5724 11.8784C10.5391 11.7567 10.4823 11.643 10.4052 11.5439C10.3282 11.4447 10.2325 11.3622 10.1236 11.301L8.87162 10.5749C8.76383 10.5118 8.64476 10.4712 8.52134 10.4553C8.39792 10.4395 8.27262 10.4487 8.15275 10.4825C8.03288 10.5163 7.92084 10.574 7.82317 10.6521C7.72549 10.7303 7.64413 10.8275 7.58383 10.9379C7.46399 11.166 7.43428 11.4319 7.50073 11.6814C7.56719 11.9309 7.72481 12.1454 7.94155 12.2812ZM6.40335 9.19531L5.79522 8.83227C5.68714 8.76957 5.56791 8.72915 5.44439 8.71335C5.32087 8.69755 5.19549 8.70667 5.07546 8.7402C4.95542 8.77372 4.8431 8.83098 4.74493 8.90869C4.64676 8.9864 4.56469 9.08303 4.50343 9.19302C4.44217 9.30302 4.40293 9.42421 4.38796 9.54965C4.37299 9.67508 4.38259 9.80228 4.4162 9.92394C4.44981 10.0456 4.50677 10.1593 4.58382 10.2586C4.66087 10.3578 4.75647 10.4406 4.86515 10.5023L5.47328 10.8653C5.61859 10.9357 5.77732 10.9728 5.93831 10.9742C6.10769 10.9718 6.27334 10.9234 6.41804 10.834C6.56273 10.7447 6.68118 10.6176 6.76107 10.466C6.82193 10.3592 6.861 10.2411 6.87592 10.1187C6.89085 9.99635 6.88134 9.87216 6.84796 9.75358C6.81457 9.635 6.758 9.52446 6.68161 9.42854C6.60523 9.33263 6.51059 9.25331 6.40335 9.19531Z' fill='%2320133A'/><defs><linearGradient id='paint0_linear_714_179' x1='7.13608e-05' y1='14.001' x2='25.1156' y2='14.001' gradientUnits='userSpaceOnUse'><stop stop-color='%239059FF'/><stop offset='1' stop-color='%23F770FF'/></linearGradient></defs></svg>&quot;); background-repeat: repeat, no-repeat; background-position: 0% 0%, right calc(50% - 0px); background-origin: padding-box, content-box;">
    
    
<button type="button" style="border: 0px; clip: rect(0px, 0px, 0px, 0px); clip-path: inset(50%); height: 1px; margin: 0px -1px -1px 0px; overflow: hidden; padding: 0px; position: absolute; width: 1px; white-space: nowrap;">Gerar nova máscara</button></div>

                                <div class="mb-3">
    <label for="id_sexo" class="form-label">Sexo</label>
    <select name="sexo" class="form-control" id="id_sexo">
  <option value="M" selected="">Masculino</option>

  <option value="F">Feminino</option>

  <option value="O">Outro</option>

</select>
    
    
</div>

                                <div class="mb-3">
    <label for="id_situacao" class="form-label">Situação</label>
    <select name="situacao" class="form-control" aria-describedby="id_situacao_helptext" id="id_situacao">
  <option value="ATIVO" selected="">Ativo</option>

  <option value="AFASTADO">Afastado</option>

  <option value="ESPECIAIS">Especiais</option>

  <option value="EXCLUIDO">Excluído</option>

  <option value="FALECIDO">Falecido</option>

  <option value="LOI">LOI</option>

</select>
    
    
        <small class="form-text text-muted">Selecione a situação atual do aluno.</small>
    
</div>

                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <!-- Moldura tracejada azul brilhante sem cabeçalho -->
                        <div class="border rounded p-3 mb-3 text-center" style="border-style: dashed !important; 
                                    border-color: #007bff !important; 
                                    border-width: 2px !important;
                                    height: 200px; 
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: center;">
                            
                                <div class="text-muted">Sem foto</div>
                            
                        </div>
                        
                        <!-- Campo de upload separado da moldura -->
                        <div class="form-group">
                            <input type="file" name="foto" class="form-control" accept="image/*" id="id_foto">
                            
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-success">
            <div class="card-header bg-success text-white">
                <h5>Dados Iniciáticos</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_numero_iniciatico" class="form-label">Número Iniciático</label>
    <input type="text" name="numero_iniciatico" value="608N" class="form-control" maxlength="10" aria-describedby="id_numero_iniciatico_helptext" id="id_numero_iniciatico">
    
    
        <small class="form-text text-muted">Número único de identificação do iniciado.</small>
    
</div>

                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_nome_iniciatico" class="form-label">Nome Iniciático</label>
    <input type="text" name="nome_iniciatico" value="Moksha" class="form-control" maxlength="100" id="id_nome_iniciatico">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-info">
            <div class="card-header bg-info text-white">
                <h5>Nacionalidade e Naturalidade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_nacionalidade" class="form-label">Nacionalidade</label>
    <input type="text" name="nacionalidade" value="Brasileira" class="form-control" maxlength="50" required="" id="id_nacionalidade">
    
    
</div>

                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_naturalidade" class="form-label">Naturalidade</label>
    <input type="text" name="naturalidade" value="Belo Horizonte" class="form-control" maxlength="50" required="" id="id_naturalidade">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-secondary">
            <div class="card-header bg-secondary text-white">
                <h5>Endereço</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="mb-3">
    <label for="id_rua" class="form-label">Rua</label>
    <input type="text" name="rua" value="Rua Costa 76" class="form-control" maxlength="100" required="" id="id_rua">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_numero_imovel" class="form-label">Número</label>
    <input type="text" name="numero_imovel" value="389" class="form-control" maxlength="10" required="" id="id_numero_imovel">
    
    
</div>

                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_complemento" class="form-label">Complemento</label>
    <input type="text" name="complemento" class="form-control" maxlength="100" id="id_complemento">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_bairro" class="form-label">Bairro</label>
    <input type="text" name="bairro" value="Copacabana" class="form-control" maxlength="50" required="" id="id_bairro">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_cep" class="form-label">CEP</label>
    <input type="text" name="cep" value="10183466" class="form-control" placeholder="Somente números" maxlength="9" required="" aria-describedby="id_cep_helptext" id="id_cep">
    
    
        <small class="form-text text-muted">Digite apenas os 8 números do CEP, sem hífen.</small>
    
</div>

                    </div>
                </div>
                <div class="row">
                    <div class="col-md-8">
                        <div class="mb-3">
    <label for="id_cidade" class="form-label">Cidade</label>
    <input type="text" name="cidade" value="Belo Horizonte" class="form-control" maxlength="50" required="" id="id_cidade">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_estado" class="form-label">Estado</label>
    <input type="text" name="estado" value="MG" class="form-control" maxlength="2" required="" id="id_estado">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-warning">
            <div class="card-header bg-warning text-dark">
                <h5>Contatos de Emergência</h5>
            </div>
            <div class="card-body">
                <h6>Primeiro Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_nome_primeiro_contato" class="form-label">Nome do Primeiro Contato</label>
    <input type="text" name="nome_primeiro_contato" value="Aline Souza" class="form-control" maxlength="100" required="" id="id_nome_primeiro_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_celular_primeiro_contato" class="form-label">Celular do Primeiro Contato</label>
    <input type="text" name="celular_primeiro_contato" value="44913707770" class="form-control" maxlength="15" required="" id="id_celular_primeiro_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_tipo_relacionamento_primeiro_contato" class="form-label">Relacionamento</label>
    <input type="text" name="tipo_relacionamento_primeiro_contato" value="Irmão" class="form-control" maxlength="50" required="" id="id_tipo_relacionamento_primeiro_contato">
    
    
</div>

                    </div>
                </div>
                
                <h6 class="mt-3">Segundo Contato</h6>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_nome_segundo_contato" class="form-label">Nome do Segundo Contato</label>
    <input type="text" name="nome_segundo_contato" value="Lucas Barbosa" class="form-control" maxlength="100" id="id_nome_segundo_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_celular_segundo_contato" class="form-label">Celular do Segundo Contato</label>
    <input type="text" name="celular_segundo_contato" value="16915231124" class="form-control" maxlength="15" id="id_celular_segundo_contato">
    
    
</div>

                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
    <label for="id_tipo_relacionamento_segundo_contato" class="form-label">Relacionamento</label>
    <input type="text" name="tipo_relacionamento_segundo_contato" value="Irmã" class="form-control" maxlength="50" id="id_tipo_relacionamento_segundo_contato">
    
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4 border-danger">
            <div class="card-header bg-danger text-white">
                <h5>Informações Médicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_tipo_sanguineo" class="form-label">Tipo Sanguíneo</label>
    <input type="text" name="tipo_sanguineo" value="A" class="form-control" maxlength="1" required="" aria-describedby="id_tipo_sanguineo_helptext" id="id_tipo_sanguineo">
    
    
        <small class="form-text text-muted">Ex: A, B, AB, O</small>
    
</div>

                    </div>
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_fator_rh" class="form-label">Fator RH</label>
    <select name="fator_rh" class="form-control" required="" aria-describedby="id_fator_rh_helptext" id="id_fator_rh">
  <option value="">---------</option>

  <option value="+">Positivo</option>

  <option value="-" selected="">Negativo</option>

</select>
    
    
        <small class="form-text text-muted">Positivo (+) ou Negativo (-)</small>
    
</div>

                    </div>
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_convenio_medico" class="form-label">Convênio Médico</label>
    <input type="text" name="convenio_medico" value="Medial Saúde" class="form-control" maxlength="100" id="id_convenio_medico">
    
    
</div>

                    </div>
                    <div class="col-md-3">
                        <div class="mb-3">
    <label for="id_hospital" class="form-label">Hospital de Preferência</label>
    <input type="text" name="hospital" value="Hospital Samaritano" class="form-control" maxlength="100" id="id_hospital">
    
    
</div>

                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_alergias" class="form-label">Alergias</label>
    <textarea name="alergias" cols="40" rows="3" class="form-control" aria-describedby="id_alergias_helptext" id="id_alergias">Nenhuma</textarea>
    
    
        <small class="form-text text-muted">Liste todas as alergias conhecidas. Deixe em branco se não houver.</small>
    
</div>

                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
    <label for="id_condicoes_medicas_gerais" class="form-label">Condições Médicas</label>
    <textarea name="condicoes_medicas_gerais" cols="40" rows="3" class="form-control" aria-describedby="id_condicoes_medicas_gerais_helptext" id="id_condicoes_medicas_gerais">Rinite alérgica</textarea>
    
    
        <small class="form-text text-muted">Descreva condições médicas relevantes. Deixe em branco se não houver.</small>
    
</div>

                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="/alunos/" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                Atualizar Aluno
            </button>
        </div>    </form>
</div>

    </main>

    <!-- Rodapé -->
    <footer class="bg-dark text-white p-3 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <p>© 2025 OMAUM - Todos os direitos reservados</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p>Versão 1.0</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- JavaScript Bootstrap -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <!-- jQuery e jQuery Mask -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
    <!-- Select2 para melhorar campos de seleção -->
    <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
    <!-- JavaScript Personalizado -->
    <script src="/static/js/alunos/mascaras.js"></script>
    <script src="/static/js/csrf_refresh.js"></script>
    <!-- Inicialização do Select2 -->
    <script>
        $(document).ready(function() {
            // Inicializar Select2 em todos os selects com a classe form-select
            $('.form-select').select2({
                theme: 'bootstrap4',
                width: '100%'
            });
            
            // Inicializar tooltips do Bootstrap
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            });
        });
    </script>
    
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
<script>
    // Script para pré-visualização da imagem quando o usuário seleciona uma foto
    document.addEventListener('DOMContentLoaded', function() {
        const fotoInput = document.getElementById('id_foto');
        if (fotoInput) {
            fotoInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const preview = document.createElement('img');
                    preview.className = 'img-fluid mt-2 rounded';
                    preview.style.maxHeight = '200px';
                    
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                    
                    // Remove qualquer preview anterior
                    const previewContainer = fotoInput.parentNode;
                    const existingPreview = previewContainer.querySelector('img');
                    if (existingPreview) {
                        previewContainer.removeChild(existingPreview);
                    }
                    
                    // Adiciona o novo preview
                    previewContainer.appendChild(preview);
                }
            });
        }
        
        // Aplicar máscaras aos campos
        $('#id_cpf').mask('000.000.000-00', {reverse: true});
        $('#id_cep').mask('00000-000');
        $('#id_celular_primeiro_contato').mask('(00) 00000-0000');
        $('#id_celular_segundo_contato').mask('(00) 00000-0000');
        $('#id_tipo_sanguineo').mask('A', {
            translation: {
                'A': { pattern: /[ABO]/ }
            }
        });
    });
</script>



</body>
não voltou para listar_aluno e aparentemente as alterações embora ainda na tela não foram atualizadas no banco de datos. Vou voltar manualmente na listagem de alunos e entrar novamente na detalhar_aluno e a alteração no nome iniciatico não foi alterada:
<body>
    <!-- Cabeçalho -->
    <header class="bg-dark text-white p-3">
        <div class="container">
            <nav class="navbar navbar-expand-lg navbar-dark">
                <a class="navbar-brand" href="/">OMAUM</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" title="Menu de navegação">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        
                            <li class="nav-item"><a class="nav-link" href="/alunos/">Alunos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/cursos/">Cursos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/atividades/academicas/">Atividades Acadêmicas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/atividades/ritualisticas/">Atividades Ritualísticas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/turmas/">Turmas</a></li>
                            <li class="nav-item"><a class="nav-link" href="/iniciacoes/">Iniciações</a></li>
                            <li class="nav-item"><a class="nav-link" href="/cargos/">Cargos</a></li>
                            <li class="nav-item"><a class="nav-link" href="/frequencias/">Frequências</a></li>
                            <li class="nav-item"><a class="nav-link" href="/presencas/">Presenças</a></li>
                            <li class="nav-item"><a class="nav-link" href="/punicoes/">Punições</a></li>
                            
                                <li class="nav-item"><a class="nav-link" href="/painel-controle/">Painel de Controle</a></li>
                            
                        
                    </ul>
                    <div class="navbar-nav">
                        
                            <span class="nav-item nav-link">Olá, lcsilv3</span>
                            <a class="nav-link" href="/sair/">Sair</a>
                        
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <!-- Mensagens -->
    <div class="container mt-3">
        
    </div>

    <!-- Conteúdo Principal -->
    <main class="container py-4">
        
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes do Aluno</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="/alunos/18027737038/editar/" class="btn btn-warning me-2">Editar</a>
            <a href="/alunos/18027737038/excluir/" class="btn btn-danger">Excluir</a>
        </div>
    </div>
    
    
    
    <div class="card mb-4 border-primary">
        <div class="card-header bg-primary text-white">
            <h5>Dados Pessoais</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-8">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>CPF:</strong> <span class="cpf-mask">180.277.370-38</span></p>
                            <p><strong>Nome:</strong> Aline Souza</p>
                            <p><strong>Data de Nascimento:</strong> 22/12/2000</p>
                            <p><strong>Hora de Nascimento:</strong> 15:02</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Email:</strong> aline.souza@exemplo.com</p>
                            <p><strong>Sexo:</strong> Masculino</p>
                            <p><strong>Situação:</strong> 
                                
                                    <span class="badge bg-success">Ativo</span>
                                
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <!-- Moldura tracejada azul brilhante sem cabeçalho -->
                    <div class="border rounded p-3 text-center" style="border-style: dashed !important; 
                                border-color: #007bff !important; 
                                border-width: 2px !important;
                                height: 200px; 
                                display: flex; 
                                align-items: center; 
                                justify-content: center;">
                        
                            <div class="text-muted">Sem foto</div>
                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    
    <div class="card mb-4 border-success">
        <div class="card-header bg-success text-white">
            <h5>Instrutoria</h5>
        </div>
        <div class="card-body">
            
                <p class="text-muted">Este aluno não é instrutor em nenhuma turma ativa.</p>
            
        </div>
    </div>
    
    
    <div class="card mb-4 border-info">
        <div class="card-header bg-info text-white">
            <h5>Dados Iniciáticos</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Número Iniciático:</strong> 608N</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Nome Iniciático:</strong> Moksha</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mb-4 border-secondary">
        <div class="card-header bg-secondary text-white">
            <h5>Nacionalidade e Naturalidade</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Nacionalidade:</strong> Brasileira</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Naturalidade:</strong> Belo Horizonte</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mb-4 border-secondary">
        <div class="card-header bg-secondary text-white">
            <h5>Endereço</h5>
        </div>
        <div class="card-body">
            <p><strong>Endereço Completo:</strong> Rua Costa 76, 389
                
                - Copacabana, Belo Horizonte/MG - CEP: <span class="cep-mask">10183-466</span></p>
        </div>
    </div>
    
    <div class="card mb-4 border-warning">
        <div class="card-header bg-warning text-dark">
            <h5>Contatos de Emergência</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <h6>Primeiro Contato</h6>
                    <p><strong>Nome:</strong> Aline Souza</p>
                    <p><strong>Celular:</strong> <span class="celular-mask">(44) 91370-7770</span></p>
                    <p><strong>Relacionamento:</strong> Irmão</p>
                </div>
                
                
                <div class="col-md-6">
                    <h6>Segundo Contato</h6>
                    <p><strong>Nome:</strong> Lucas Barbosa</p>
                    <p><strong>Celular:</strong> <span class="celular-mask">(16) 91523-1124</span></p>
                    <p><strong>Relacionamento:</strong> Irmã</p>
                </div>
                
            </div>
        </div>
    </div>
    
    <div class="card mb-4 border-danger">
        <div class="card-header bg-danger text-white">
            <h5>Informações Médicas</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-3">
                    <p><strong>Tipo Sanguíneo:</strong> A</p>
                </div>
                <div class="col-md-3">
                    <p><strong>Fator RH:</strong> Negativo</p>
                </div>
                <div class="col-md-3">
                    <p><strong>Convênio Médico:</strong> Medial Saúde</p>
                </div>
                <div class="col-md-3">
                    <p><strong>Hospital:</strong> Hospital Samaritano</p>
                </div>
            </div>
            
            <div class="row mt-3">
                <div class="col-md-6">
                    <h6>Alergias:</h6>
                    <div class="p-2 bg-light rounded">
                        <p>Nenhuma</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <h6>Condições Médicas:</h6>
                    <div class="p-2 bg-light rounded">
                        <p>Rinite alérgica</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="d-flex justify-content-between mb-5">
        <a href="/alunos/" class="btn btn-secondary">Voltar para a lista</a>
        <div>
            <a href="/alunos/18027737038/editar/" class="btn btn-warning me-2">Editar</a>
            <a href="/alunos/18027737038/excluir/" class="btn btn-danger">Excluir</a>
        </div>
    </div>
</div>

    </main>

    <!-- Rodapé -->
    <footer class="bg-dark text-white p-3 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <p>© 2025 OMAUM - Todos os direitos reservados</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p>Versão 1.0</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- JavaScript Bootstrap -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <!-- jQuery e jQuery Mask -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
    <!-- Select2 para melhorar campos de seleção -->
    <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
    <!-- JavaScript Personalizado -->
    <script src="/static/js/alunos/mascaras.js"></script>
    <script src="/static/js/csrf_refresh.js"></script>
    <!-- Inicialização do Select2 -->
    <script>
        $(document).ready(function() {
            // Inicializar Select2 em todos os selects com a classe form-select
            $('.form-select').select2({
                theme: 'bootstrap4',
                width: '100%'
            });
            
            // Inicializar tooltips do Bootstrap
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            });
        });
    </script>
    
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
<script>
    $(document).ready(function(){
        // Aplicar máscaras para exibição
        $('.cpf-mask').each(function(){
            var cpf = $(this).text().trim();
            if(cpf.length === 11) {
                $(this).text(cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4"));
            }
        });
        
        $('.cep-mask').each(function(){
            var cep = $(this).text().trim();
            if(cep.length === 8) {
                $(this).text(cep.replace(/(\d{5})(\d{3})/, "$1-$2"));
            }
        });
        
        $('.celular-mask').each(function(){
            var celular = $(this).text().trim();
            if(celular.length === 11) {
                $(this).text(celular.replace(/(\d{2})(\d{5})(\d{4})/, "($1) $2-$3"));
            } else if(celular.length === 10) {
                $(this).text(celular.replace(/(\d{2})(\d{4})(\d{4})/, "($1) $2-$3"));
            }
        });
    });
</script>



</body>



### Arquivo: manage.py

python
#!/usr/bin/env python
"""Utilitário de linha de comando do Django para tarefas administrativas."""
import os
import sys


def main():
    """Executa tarefas administrativas."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django."
            "Tem certeza de que ele está instalado e disponível"
            "Na sua variável de ambiente PYTHONPATH? "
            "Você esqueceu de ativar um ambiente virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()




### Arquivo: pyproject.toml

text
[tool.black]
line-length = 79
include = '\.pyi?



### Arquivo: README.md

text
# Sistema OMAUM

Sistema de gestão acadêmica desenvolvido para [descrição da instituição/propósito].

## Funcionalidades

- Gestão de alunos
- Controle de atividades acadêmicas e ritualísticas
- Gerenciamento de cursos e turmas
- Controle de presenças e notas
- Relatórios acadêmicos
- [outras funcionalidades]

## Tecnologias Utilizadas

- Django
- Python
- SQLite (desenvolvimento)
- [outras tecnologias]

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute as migrações: `python manage.py migrate`
6. Inicie o servidor: `python manage.py runserver`

## Estrutura do Projeto

O projeto está organizado em módulos funcionais, cada um responsável por uma área específica do sistema:

- **alunos**: Gerenciamento de estudantes
- **atividades**: Controle de atividades acadêmicas e ritualísticas
- **cursos**: Administração de cursos oferecidos
- **turmas**: Gerenciamento de turmas e períodos letivos
- [outros módulos]

## Desenvolvimento

### Linting e Formatação de Código

Este projeto usa Pylint e Flake8 para garantir a qualidade do código. Para executar os linters:

```bash
python scripts/lint.py
```

Recomendamos configurar seu editor para executar o linter automaticamente ao salvar os arquivos.

Para o VS Code, instale as extensões:
- Python (Microsoft)
- Pylint
- Flake8

As configurações recomendadas já estão no arquivo `.vscode/settings.json`.
```

## 7. Corrigindo o Arquivo verificar_arquivos_importantes_duplicados.py

Agora, vamos corrigir o problema específico que você encontrou no arquivo `scripts/verificar_arquivos_importantes_duplicados.py`:

```python:scripts/verificar_arquivos_importantes_duplicados.py
# Nas linhas 61-62, substitua:
("base.html", "omaum\\templates\\base.html"),
("home.html", "omaum\templates\home.html"),

# Por:
("base.html", r"omaum\templates\base.html"),
("home.html", r"omaum\templates\home.html"),



### Arquivo: requirements-dev.txt

text
asgiref==3.8.1
astroid==3.3.9
black==25.1.0
chardet==5.2.0
click==8.1.8
colorama==0.4.6
dill==0.3.9
Django==5.1.7
django-crispy-forms==2.3
django-debug-toolbar==5.1.0
django-extensions==3.2.3
django-widget-tweaks==1.5.0
Faker==37.1.0
flake8==7.2.0
isort==6.0.1
mccabe==0.7.0
mypy-extensions==1.0.0
packaging==24.2
pathspec==0.12.1
pillow==11.1.0
platformdirs==4.3.7
pycodestyle==2.13.0
pyflakes==3.3.2
pylint==3.3.6
reportlab==4.3.1
sqlparse==0.5.3
tomlkit==0.13.2
tzdata==2025.1
XlsxWriter==3.2.2




### Arquivo: requirements.txt

text
asgiref==3.8.1
chardet==5.2.0
Django==5.1.7
django-crispy-forms==2.3
django-debug-toolbar==5.1.0
django-extensions==3.2.3
django-widget-tweaks==1.5.0
pillow==11.1.0
reportlab==4.3.1
sqlparse==0.5.3
tzdata==2025.1




### Arquivo: script_revisao_projeto.py

python
import os
import chardet
import shutil


def collect_files_by_app(project_root):
    # Dicionário para armazenar arquivos por app/funcionalidade
    apps_files = {}
    for root, dirs, files in os.walk(project_root):
        # Ignorar diretórios de ambiente virtual e cache
        if "venv" in root or "__pycache__" in root:
            continue
        # Identificar o app/funcionalidade com base no caminho
        relative_path = os.path.relpath(root, project_root)
        app_name = (
            relative_path.split(os.path.sep)[0]
            if relative_path != "."
            else "core"
        )
        # Inicializar a estrutura para o app se ainda não existir
        if app_name not in apps_files:
            apps_files[app_name] = {
                "forms.py": [],
                "views.py": [],
                "urls.py": [],
                "models.py": [],
                "templates": [],
            }
        for file in files:
            if file in ["forms.py", "views.py", "urls.py", "models.py"]:
                apps_files[app_name][file].append(os.path.join(root, file))
            elif file.endswith(".html"):
                apps_files[app_name]["templates"].append(
                    os.path.join(root, file)
                )
    return apps_files


def write_file_contents(output_file, filepath):
    # Detectar codificação do arquivo
    with open(filepath, "rb") as raw_file:
        raw_data = raw_file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"] or "utf-8"  # Fallback para utf-8
    try:
        with open(filepath, "r", encoding=encoding) as file:
            relative_path = os.path.relpath(filepath)
            output_file.write(f"\n\n### Arquivo: {relative_path}\n\n")
            # Determinar o tipo de linguagem para o bloco de código
            if filepath.endswith(".html"):
                language = "html"
            elif filepath.endswith(".py"):
                language = "python"
            else:
                language = "text"
            output_file.write(f"{language}\n")
            output_file.write(file.read())
            output_file.write("\n\n")
    except Exception as e:
        output_file.write(f"\n\n### Arquivo: {filepath}\n\n")
        output_file.write(f"\nErro ao ler o arquivo: {str(e)}\n\n")


def collect_root_files(project_root, output_dir):
    """Coleta arquivos da raiz do projeto Django."""
    output_filename = os.path.join(output_dir, "root_files_revisao.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Arquivos da Raiz do Projeto Django\n")

        # Listar arquivos na raiz do projeto
        root_files = [
            f
            for f in os.listdir(project_root)
            if os.path.isfile(os.path.join(project_root, f))
            and not f.startswith(".")
        ]

        for file in root_files:
            filepath = os.path.join(project_root, file)
            write_file_contents(output_file, filepath)

        # Verificar e incluir arquivos estáticos
        static_dir = os.path.join(project_root, "static")
        if os.path.exists(static_dir) and os.path.isdir(static_dir):
            output_file.write("\n## Arquivos Estáticos\n")
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    write_file_contents(output_file, filepath)

    print(f"Arquivos da raiz do projeto foram escritos em {output_filename}")


def generate_project_structure(project_root, output_dir):
    """Gera um arquivo com a estrutura completa do projeto."""
    output_filename = os.path.join(output_dir, "project_structure.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Estrutura do Projeto Django\n\n")
        output_file.write("\n")

        for root, dirs, files in os.walk(project_root):
            # Ignorar diretórios de ambiente virtual e cache
            if "venv" in root or "__pycache__" in root:
                continue

            level = root.replace(project_root, "").count(os.sep)
            indent = " " * 4 * level
            output_file.write(f"{indent}{os.path.basename(root)}/\n")

            sub_indent = " " * 4 * (level + 1)
            for file in files:
                output_file.write(f"{sub_indent}{file}\n")

        output_file.write("\n")

    print(f"Estrutura do projeto foi escrita em {output_filename}")


def check_template_dirs(project_root, output_dir):
    """Verifica e documenta as configurações de diretórios de templates."""
    output_filename = os.path.join(output_dir, "template_dirs_check.md")
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("# Verificação de Diretórios de Templates\n\n")

        # Verificar settings.py para configurações de TEMPLATES
        settings_files = []
        for root, dirs, files in os.walk(project_root):
            if "settings.py" in files:
                settings_files.append(os.path.join(root, "settings.py"))

        if settings_files:
            output_file.write(
                "## Configurações de Templates no settings.py\n\n"
            )
            for settings_file in settings_files:
                write_file_contents(output_file, settings_file)

        # Listar todos os diretórios de templates encontrados
        output_file.write("\n## Diretórios de Templates Encontrados\n\n")
        template_dirs = []
        for root, dirs, files in os.walk(project_root):
            if "templates" in dirs:
                template_dir = os.path.join(root, "templates")
                template_dirs.append(template_dir)
                output_file.write(
                    f"- {os.path.relpath(template_dir, project_root)}\n"
                )

                # Listar arquivos de template neste diretório
                output_file.write("  Arquivos:\n")
                for template_root, template_dirs, template_files in os.walk(
                    template_dir
                ):
                    for file in template_files:
                        output_file.write(
                            f"  - {os.path.relpath(os.path.join(template_root, file), template_dir)}\n"
                        )

        # Verificar especificamente o template listar_alunos.html
        output_file.write("\n## Busca pelo template listar_alunos.html\n\n")
        found = False
        for root, dirs, files in os.walk(project_root):
            for file in files:
                if file == "listar_alunos.html":
                    found = True
                    output_file.write(
                        f"Encontrado em: {os.path.relpath(os.path.join(root, file), project_root)}\n"
                    )

        if not found:
            output_file.write(
                "O arquivo listar_alunos.html não foi encontrado no projeto.\n"
            )

    print(
        f"Verificação de diretórios de templates foi escrita em {output_filename}"
    )


def main():
    project_root = input("Digite o diretório raiz do seu projeto Django: ")
    output_dir = "revisao_projeto"
    # Criar diretório de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Coletar arquivos por app
    apps_files = collect_files_by_app(project_root)
    for app_name, file_types in apps_files.items():
        # Verificar se há arquivos para este app
        has_files = any(files for files in file_types.values())
        if not has_files:
            continue
        output_filename = os.path.join(output_dir, f"{app_name}_revisao.md")
        with open(output_filename, "w", encoding="utf-8") as output_file:
            output_file.write(f"# Revisão da Funcionalidade: {app_name}\n")
            for file_type, file_paths in file_types.items():
                if not file_paths:
                    continue
                if file_type == "templates":
                    output_file.write(f"\n## Arquivos de Template:\n")
                else:
                    output_file.write(f"\n## Arquivos {file_type}:\n")
                for filepath in sorted(file_paths):
                    write_file_contents(output_file, filepath)
        print(
            f"Conteúdo da funcionalidade '{app_name}' foi escrito em {output_filename}"
        )

    # Coletar arquivos da raiz e arquivos estáticos
    collect_root_files(project_root, output_dir)

    # Gerar estrutura do projeto
    generate_project_structure(project_root, output_dir)

    # Verificar diretórios de templates
    check_template_dirs(project_root, output_dir)

    print(f"Revisão completa! Arquivos gerados no diretório '{output_dir}'")


if __name__ == "__main__":
    main()




### Arquivo: settings.py

python




### Arquivo: urls.py

python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static  # Adicione esta importação

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("alunos/", include("alunos.urls")),
    path("atividades/", include("atividades.urls")),
    path("cargos/", include("cargos.urls")),
    path("cursos/", include("cursos.urls")),
    path("frequencias/", include("frequencias.urls")),
    path("iniciacoes/", include("iniciacoes.urls")),
    path("presencas/", include("presencas.urls")),
    path("punicoes/", include("punicoes.urls")),
    path("relatorios/", include("relatorios.urls", namespace="relatorios")),
    path("turmas/", include("turmas.urls")),
]

from django.contrib.auth import views as auth_views

urlpatterns += [
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="/"),
        name="logout",
    ),
]

# Adicione este bloco no final do arquivo
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    # Adicione esta linha para servir arquivos de mídia durante o desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


## Arquivos Estáticos


### Arquivo: static\favicon.ico

text


### Arquivo: c:\projetos\omaum\static\favicon.ico


Erro ao ler o arquivo: 'charmap' codec can't decode byte 0x98 in position 615: character maps to <undefined>



### Arquivo: static\css\accessibility_fixes.css

text
/* Fix for list structure accessibility issues */
ul, ol {
  font-size: 0;  /* Collapse whitespace between list items */
  list-style-position: inside;  /* Ensure bullets/numbers are within the list item's text flow */
}

li {
  font-size: 1rem;  /* Restore font size for list items */
  margin-bottom: 0.5em;  /* Add some vertical spacing between list items for better readability */
}

ul *, ol * {
  font-size: 1rem;  /* Restore font size for nested elements */
}

/* Fix for Bootstrap components */
.navbar-nav, .dropdown-menu {
  font-size: 0;  /* Collapse whitespace between nav items */
}

.navbar-nav *, .dropdown-menu * {
  font-size: 1rem;  /* Restore font size for nav items and dropdowns */
}

/* Additional accessibility improvements */
:focus {
  outline: 2px solid #007bff;  /* Add a visible focus indicator */
  outline-offset: 2px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Improve color contrast for better readability */
body {
  color: #333;  /* Darker text color for better contrast */
}

a {
  color: #0056b3;  /* Darker link color for better contrast */
}

/* Ensure sufficient line height for readability */
p, li {
  line-height: 1.5;
}




### Arquivo: static\css\alunos.css

text
/* Estilos para o módulo de alunos */

/* Cores para os cards */
.card.border-primary {
    border-color: #007bff !important;
}

.card.border-success {
    border-color: #28a745 !important;
}

.card.border-info {
    border-color: #17a2b8 !important;
}

.card.border-warning {
    border-color: #ffc107 !important;
}

.card.border-danger {
    border-color: #dc3545 !important;
}

.card.border-secondary {
    border-color: #6c757d !important;
}

/* Estilos para campos de formulário */
.form-control:focus {
    border-color: #80bdff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Estilos para a foto do aluno */
.foto-container {
    border-style: dashed !important;
    border-color: #007bff !important;
    border-width: 2px !important;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Estilos para informações médicas */
.info-medica {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
}

/* Estilos para badges de situação */
.badge-situacao {
    font-size: 0.9em;
    padding: 5px 8px;
}

/* Estilos para listas de turmas */
.lista-turmas {
    max-height: 300px;
    overflow-y: auto;
}

/* Estilos responsivos */
@media (max-width: 768px) {
    .d-flex.justify-content-between {
        flex-direction: column;
        gap: 10px;
    }
    
    .d-flex.justify-content-between div {
        display: flex;
        gap: 10px;
    }
}



### Arquivo: static\css\extra_styles.css

text
.list-group {
    position: absolute;
    z-index: 1000;
    width: 100%;
    max-height: 300px;
    overflow-y: auto;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.list-group-item-action:hover {
    background-color: #f8f9fa;
}

/* Garantir que o container do instrutor selecionado tenha a mesma largura do campo de pesquisa */
.selected-instructor-container {
    background-color: #f8f9fa;
    border-radius: 4px;
    padding: 10px;
    margin-top: 10px;
    width: 100%; /* Garante que ocupe toda a largura disponível */
    box-sizing: border-box; /* Inclui padding e border na largura total */
}

/* Estilo para a informação do instrutor selecionado */
.selected-instructor-info {
    font-size: 0.9rem;
    word-break: break-word; /* Evita que textos longos quebrem o layout */
}
/* Estilos para itens não elegíveis na busca de instrutores */
.list-group-item.ineligible {
    opacity: 0.7;
    background-color: #fff0f0;
    cursor: not-allowed;
}

.list-group-item.ineligible:hover {
    background-color: #ffe0e0;
}

/* Estilo para o ícone X vermelho */
.list-group-item .text-danger i {
    font-size: 1.1em;
}
.list-group {
    position: absolute;
    z-index: 1000;
    width: 100%;
    max-height: 300px;
    overflow-y: auto;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Garantir que o container pai tenha posição relativa */
.col-md-4 {
    position: relative;
}



### Arquivo: static\css\Piscar.css

text
<!-- No bloco head ou em um arquivo CSS separado -->
<style>
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .blink {
        animation: blink 1s linear infinite;
    }
</style>




### Arquivo: static\css\style.css

text
/* Estilos personalizados para o sistema OMAUM */




### Arquivo: static\js\aluno-search.js

text
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-aluno');
    const searchResults = document.getElementById('search-results');
    
    if (!searchInput || !searchResults) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        
        const query = this.value.trim();
        
        // Clear results if query is too short
        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }
        
        // Set a timeout to avoid making too many requests
        searchTimeout = setTimeout(function() {
            // Show loading indicator
            searchResults.innerHTML = '<div class="list-group-item text-muted">Buscando...</div>';
            searchResults.style.display = 'block';
            
            // Get CSRF token
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(`/alunos/search/?q=${encodeURIComponent(query)}`, {
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                searchResults.innerHTML = '';
                
                if (data.error) {
                    // Handle error response
                    searchResults.innerHTML = `<div class="list-group-item text-danger">Erro ao buscar alunos: ${data.error}</div>`;
                    return;
                }
                
                if (data.length === 0) {
                    searchResults.innerHTML = '<div class="list-group-item">Nenhum aluno encontrado</div>';
                    return;
                }
                
                // Display results
                data.forEach(aluno => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.className = 'list-group-item list-group-item-action';
                    item.innerHTML = `
                        <div class="d-flex justify-content-between">
                            <div>${aluno.nome}</div>
                            <div class="text-muted">
                                <small>CPF: ${aluno.cpf}</small>
                                ${aluno.numero_iniciatico !== "N/A" ? `<small class="ms-2">NÂº: ${aluno.numero_iniciatico}</small>` : ''}
                            </div>
                        </div>
                    `;
                    
                    // Add click event to select this aluno
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        selectAluno(aluno);
                    });
                    
                    searchResults.appendChild(item);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                searchResults.innerHTML = '<div class="list-group-item text-danger">Erro ao buscar alunos</div>';
            });
        }, 300);
    });
    
    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
    
    // Function to select an aluno
    function selectAluno(aluno) {
        // Get the hidden input field for the aluno ID
        const alunoIdField = document.getElementById('id_aluno');
        if (alunoIdField) {
            alunoIdField.value = aluno.cpf;
        }
        
        // Update the search input with the selected aluno's name
        searchInput.value = aluno.nome;
        
        // Hide the search results
        searchResults.style.display = 'none';
        
        // Trigger any additional actions needed when an aluno is selected
        const event = new CustomEvent('alunoSelected', { detail: aluno });
        document.dispatchEvent(event);
    }
});




### Arquivo: static\js\csrf_refresh.js

text
// Variáveis para controle de inatividade
let inactivityTimer;
const inactivityTimeout = 30 * 60 * 1000; // 30 minutos em milissegundos

// Função para verificar o status da sessão e do token CSRF
function checkSessionStatus() {
    // Fazer uma requisição AJAX para verificar o status da sessão
    fetch('/core/csrf_check/', {  // Corrigir o caminho para incluir 'core/'
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            // Se a resposta não for OK, mostrar alerta de sessão expirada
            showSessionExpiredAlert();
        }
    })
    .catch(error => {
        console.error('Erro ao verificar status da sessão:', error);
        // Em caso de erro, também mostrar o alerta
        showSessionExpiredAlert();
    });
}

// Função para mostrar alerta de sessão expirada
function showSessionExpiredAlert() {
    // Verificar se o alerta já existe para não duplicar
    if (!document.getElementById('session-expired-alert')) {
        const alertDiv = document.createElement('div');
        alertDiv.id = 'session-expired-alert';
        alertDiv.className = 'alert alert-warning alert-dismissible fade show session-alert';
        alertDiv.innerHTML = `
            <strong>Atenção!</strong> Sua sessão pode ter expirado devido à inatividade. 
            <button type="button" class="btn btn-sm btn-primary mx-2" onclick="refreshPage()">Recarregar Página</button>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
        `;
        
        // Estilo para o alerta fixo no topo da página
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '10px';
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
        
        document.body.appendChild(alertDiv);
    }
}

// Função para recarregar a página
function refreshPage() {
    window.location.reload();
}

// Função para reiniciar o timer de inatividade
function resetInactivityTimer() {
    // Limpar o timer existente
    clearTimeout(inactivityTimer);
    
    // Iniciar um novo timer
    inactivityTimer = setTimeout(() => {
        // Após 30 minutos de inatividade, verificar a sessão
        checkSessionStatus();
    }, inactivityTimeout);
}

// Lista de eventos que indicam atividade do usuário
const userActivityEvents = [
    'mousedown', 'mousemove', 'keypress', 
    'scroll', 'touchstart', 'click', 'keydown'
];

// Inicializar o monitoramento de atividade do usuário
function initInactivityMonitoring() {
    // Adicionar listeners para todos os eventos de atividade
    userActivityEvents.forEach(eventType => {
        document.addEventListener(eventType, resetInactivityTimer, { passive: true });
    });
    
    // Iniciar o timer pela primeira vez
    resetInactivityTimer();
}

// Também verificar quando o usuário retorna à aba
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        // Reiniciar o timer quando o usuário volta para a aba
        resetInactivityTimer();
    }
});

// Inicializar o monitoramento de inatividade quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    // Iniciar o monitoramento de inatividade
    initInactivityMonitoring();
});



### Arquivo: static\js\instrutor_search.js

text
/**
 * Módulo para busca e seleção de instrutores
 */
const InstrutorSearch = (function() {
    let csrfToken = '';
    let showAllStudents = false;
    let ignoreEligibility = false;
    
    // Função para verificar elegibilidade
    function verificarElegibilidade(cpf, tipoInstrutor) {
        console.log(`Verificando elegibilidade do instrutor ${tipoInstrutor} com CPF: ${cpf}`);
        
        const errorElement = document.getElementById(`${tipoInstrutor}-error`);
        if (!errorElement) {
            console.error(`Elemento de erro não encontrado para ${tipoInstrutor}`);
            return;
        }
        
        // Limpar mensagem de erro anterior
        errorElement.textContent = '';
        errorElement.classList.add('d-none');
        
        // Se estamos ignorando verificações de elegibilidade, não fazer a verificação
        if (ignoreEligibility) {
            console.log('Ignorando verificação de elegibilidade (modo de depuração ativo)');
            return;
        }
        
        // Fazer requisição para verificar elegibilidade
        fetch(`/alunos/api/verificar-elegibilidade/${cpf}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(`Resposta da verificação de elegibilidade:`, data);
                
                if (!data.elegivel) {
                    // Mostrar mensagem de erro específica
                    errorElement.textContent = data.motivo || "Este aluno não pode ser instrutor.";
                    errorElement.classList.remove('d-none');
                    
                    // Se estamos mostrando todos os alunos, não bloqueamos a seleção
                    if (!showAllStudents) {
                        // Limpar seleção
                        const selectElement = document.getElementById(`id_${tipoInstrutor}`);
                        if (selectElement) {
                            selectElement.value = '';
                        }
                    }
                }
            })
            .catch(error => {
                console.error(`Erro ao verificar elegibilidade: ${error.message}`);
                errorElement.textContent = `Erro na busca: ${error.message}`;
                errorElement.classList.remove('d-none');
            });
    }
    
    // Função para selecionar um instrutor
    function selectInstructor(cpf, nome, numero, situacao, turmas, tipoInstrutor) {
        console.log(`Selecionando ${tipoInstrutor}: ${nome} (${cpf})`);
        
        // Atualizar o select oculto
        const selectElement = document.getElementById(`id_${tipoInstrutor}`);
        if (selectElement) {
            selectElement.value = cpf;
        }
        
        // Atualizar a exibição
        const containerElement = document.getElementById(`selected-${tipoInstrutor}-container`);
        const infoElement = document.getElementById(`selected-${tipoInstrutor}-info`);
        
        if (containerElement && infoElement) {
            // Criar HTML para turmas, se disponível
            let turmasHtml = '';
            if (turmas && turmas.length > 0) {
                turmasHtml = `
                    <div class="mt-2">
                        <strong>Turmas:</strong>
                        <ul class="mb-0 ps-3">
                            ${turmas.map(turma => `<li>${turma}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            infoElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <strong>${nome}</strong><br>
                        CPF: ${cpf} | Nº Iniciático: ${numero || 'N/A'}<br>
                        <span class="badge ${situacao === 'ATIVO' ? 'bg-success' : 'bg-danger'}">${situacao || 'Não informado'}</span>
                        ${turmasHtml}
                    </div>
                    <button type="button" class="btn btn-sm btn-danger remove-instructor">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            
            containerElement.classList.remove('d-none');
            
            // Adicionar evento para remover instrutor
            const removeButton = infoElement.querySelector('.remove-instructor');
            if (removeButton) {
                removeButton.addEventListener('click', function() {
                    selectElement.value = '';
                    containerElement.classList.add('d-none');
                    infoElement.innerHTML = '';
                    
                    // Limpar mensagem de erro
                    const errorElement = document.getElementById(`${tipoInstrutor}-error`);
                    if (errorElement) {
                        errorElement.textContent = '';
                        errorElement.classList.add('d-none');
                    }
                });
            }
        }
        
        // Verificar elegibilidade
        verificarElegibilidade(cpf, tipoInstrutor);
    }
    
    // Função para configurar a busca de instrutores
    function setupInstructorSearch(tipoInstrutor) {
        console.log(`Configurando busca para ${tipoInstrutor}`);
        
        const searchInput = document.getElementById(`search-${tipoInstrutor}`);
        const searchResults = document.getElementById(`search-results-${tipoInstrutor}`);
        
        if (!searchInput || !searchResults) {
            console.error(`Elementos de busca não encontrados para ${tipoInstrutor}`);
            return;
        }
        
        // Evento de digitação
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            // Fazer requisição para buscar alunos
            const url = showAllStudents || ignoreEligibility ? 
                `/alunos/search/?q=${encodeURIComponent(query)}` : 
                `/alunos/api/search-instrutores/?q=${encodeURIComponent(query)}`;
            
            fetch(url, {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(`Resultados da busca para ${tipoInstrutor}:`, data);
                
                // Limpar resultados anteriores
                searchResults.innerHTML = '';
                
                // Verificar se há erro na resposta
                if (data && data.error) {
                    searchResults.innerHTML = `<div class="list-group-item text-danger">Erro na busca: ${data.error}</div>`;
                    searchResults.style.display = 'block';
                    return;
                }
                
                // Garantir que data seja um array
                const alunos = Array.isArray(data) ? data : [];
                
                if (alunos.length === 0) {
                    searchResults.innerHTML = '<div class="list-group-item">Nenhum resultado encontrado</div>';
                    searchResults.style.display = 'block';
                    return;
                }
                
                // Adicionar resultados
                alunos.forEach(aluno => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.className = 'list-group-item list-group-item-action';
                    item.dataset.cpf = aluno.cpf;
                    item.dataset.nome = aluno.nome;
                    item.dataset.numero = aluno.numero_iniciatico;
                    item.dataset.situacao = aluno.situacao || 'Não informado';
                    
                    // Preparar informações de turmas
                    let turmasHtml = '';
                    let turmasArray = [];
                    
                    if (aluno.turmas_como_instrutor && aluno.turmas_como_instrutor.length > 0) {
                        turmasArray = turmasArray.concat(aluno.turmas_como_instrutor.map(t => `${t} (Instrutor)`));
                    }
                    
                    if (aluno.turmas_como_aluno && aluno.turmas_como_aluno.length > 0) {
                        turmasArray = turmasArray.concat(aluno.turmas_como_aluno.map(t => `${t} (Aluno)`));
                    }
                    
                    if (turmasArray.length > 0) {
                        turmasHtml = `
                            <div class="small mt-1">
                                <strong>Turmas:</strong>
                                <ul class="mb-0 ps-3">
                                    ${turmasArray.map(turma => `<li>${turma}</li>`).join('')}
                                </ul>
                            </div>
                        `;
                    }
                    
                    item.innerHTML = `
                        <div>
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>${aluno.nome}</strong>
                                    <span class="badge ${aluno.situacao === 'ATIVO' ? 'bg-success' : 'bg-danger'} ms-2">${aluno.situacao || 'Não informado'}</span>
                                </div>
                                <div class="text-muted">
                                    <small>CPF: ${aluno.cpf}</small>
                                    <small class="ms-2">Nº: ${aluno.numero_iniciatico || 'N/A'}</small>
                                </div>
                            </div>
                            ${turmasHtml}
                        </div>
                    `;                    
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        selectInstructor(
                            this.dataset.cpf,
                            this.dataset.nome,
                            this.dataset.numero,
                            this.dataset.situacao,
                            turmasArray,
                            tipoInstrutor
                        );
                        searchResults.style.display = 'none';
                        searchInput.value = '';
                    });
                    
                    searchResults.appendChild(item);
                });
                
                searchResults.style.display = 'block';
            })
            .catch(error => {
                console.error(`Erro na busca de ${tipoInstrutor}:`, error);
                searchResults.innerHTML = `<div class="list-group-item text-danger">Erro na busca: ${error.message}</div>`;
                searchResults.style.display = 'block';
            });        });
        
        // Esconder resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
    
    return {
        init: function(token, allowAllStudents = false) {
            console.log('Inicializando módulo de busca de instrutores');
            csrfToken = token;
            showAllStudents = allowAllStudents;
            
            // Configurar busca para cada tipo de instrutor
            setupInstructorSearch('instrutor');
            setupInstructorSearch('instrutor-auxiliar');
            setupInstructorSearch('auxiliar-instrucao');
            
            console.log(`Modo de exibição: ${showAllStudents ? 'todos os alunos' : 'apenas elegíveis'}`);
            
            // Verificar se o modo de depuração está ativo
            const debugSwitch = document.getElementById('ignore-eligibility');
            if (debugSwitch) {
                ignoreEligibility = debugSwitch.checked;
                console.log(`Modo de depuração: ${ignoreEligibility ? 'ativo' : 'inativo'}`);
            }
        },
        
        setIgnoreEligibility: function(value) {
            ignoreEligibility = value;
            console.log(`Modo de depuração ${ignoreEligibility ? 'ativado' : 'desativado'}`);
        }
    };
})();



### Arquivo: static\js\alunos\mascaras.js

text
/**
 * Funções para aplicar máscaras e validações nos formulários de alunos
 */

$(document).ready(function() {
    // Aplicar máscaras
    $('#id_cpf').mask('000.000.000-00');
    $('#id_cep').mask('00000-000');
    $('#id_celular_primeiro_contato').mask('(00) 00000-0000');
    $('#id_celular_segundo_contato').mask('(00) 00000-0000');
    
    // Remover máscaras antes do envio do formulário
    $('form').on('submit', function() {
        console.log("Formulário sendo enviado - removendo máscaras");
        
        // Remover máscaras dos campos
        var cpf = $('#id_cpf').val().replace(/\D/g, '');
        var cep = $('#id_cep').val().replace(/\D/g, '');
        var celular1 = $('#id_celular_primeiro_contato').val().replace(/\D/g, '');
        var celular2 = $('#id_celular_segundo_contato').val().replace(/\D/g, '');
        
        // Atualizar os campos com valores sem máscara
        $('#id_cpf').val(cpf);
        $('#id_cep').val(cep);
        $('#id_celular_primeiro_contato').val(celular1);
        $('#id_celular_segundo_contato').val(celular2);
        
        // Não usar preventDefault() para permitir o envio normal do formulário
        return true;
    });
});



### Arquivo: static\js\turmas\instrutor_search.js

text
/**
 * Módulo para busca e seleção de instrutores
 */
const InstrutorSearch = (function() {
    let csrfToken = '';
    let showAllStudents = false;
    let ignoreEligibility = false;
    
    // Função para verificar elegibilidade
    function verificarElegibilidade(cpf, tipoInstrutor) {
        console.log(`Verificando elegibilidade do instrutor ${tipoInstrutor} com CPF: ${cpf}`);
        
        const errorElement = document.getElementById(`${tipoInstrutor}-error`);
        if (!errorElement) {
            console.error(`Elemento de erro não encontrado para ${tipoInstrutor}`);
            return;
        }
        
        // Limpar mensagem de erro anterior
        errorElement.textContent = '';
        errorElement.classList.add('d-none');
        
        // Se estamos ignorando verificações de elegibilidade, não fazer a verificação
        if (ignoreEligibility) {
            console.log('Ignorando verificação de elegibilidade (modo de depuração ativo)');
            return;
        }
        
        // Fazer requisição para verificar elegibilidade
        fetch(`/alunos/api/verificar-elegibilidade/${cpf}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(`Resposta da verificação de elegibilidade:`, data);
                
                if (!data.elegivel) {
                    // Mostrar mensagem de erro específica
                    errorElement.textContent = data.motivo || "Este aluno não pode ser instrutor.";
                    errorElement.classList.remove('d-none');
                    
                    // Se estamos mostrando todos os alunos, não bloqueamos a seleção
                    if (!showAllStudents) {
                        // Limpar seleção
                        const selectElement = document.getElementById(`id_${tipoInstrutor}`);
                        if (selectElement) {
                            selectElement.value = '';
                        }
                    }
                }
            })
            .catch(error => {
                console.error(`Erro ao verificar elegibilidade: ${error.message}`);
                errorElement.textContent = `Erro na busca: ${error.message}`;
                errorElement.classList.remove('d-none');
            });
    }
    
    // Função para selecionar um instrutor
    function selectInstructor(cpf, nome, numero, tipoInstrutor) {
        console.log(`Selecionando ${tipoInstrutor}: ${nome} (${cpf})`);
        
        // Atualizar o select oculto
        const selectElement = document.getElementById(`id_${tipoInstrutor}`);
        if (selectElement) {
            selectElement.value = cpf;
        }
        
        // Atualizar a exibição
        const containerElement = document.getElementById(`selected-${tipoInstrutor}-container`);
        const infoElement = document.getElementById(`selected-${tipoInstrutor}-info`);
        
        if (containerElement && infoElement) {
            infoElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${nome}</strong><br>
                        CPF: ${cpf} | Nº Iniciático: ${numero || 'N/A'}
                    </div>
                    <button type="button" class="btn btn-sm btn-danger remove-instructor">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            
            containerElement.classList.remove('d-none');
            
            // Adicionar evento para remover instrutor
            const removeButton = infoElement.querySelector('.remove-instructor');
            if (removeButton) {
                removeButton.addEventListener('click', function() {
                    selectElement.value = '';
                    containerElement.classList.add('d-none');
                    infoElement.innerHTML = '';
                    
                    // Limpar mensagem de erro
                    const errorElement = document.getElementById(`${tipoInstrutor}-error`);
                    if (errorElement) {
                        errorElement.textContent = '';
                        errorElement.classList.add('d-none');
                    }
                });
            }
        }
        
        // Verificar elegibilidade
        verificarElegibilidade(cpf, tipoInstrutor);
    }
    
    // Função para configurar a busca de instrutores
    function setupInstructorSearch(tipoInstrutor) {
        console.log(`Configurando busca para ${tipoInstrutor}`);
        
        const searchInput = document.getElementById(`search-${tipoInstrutor}`);
        const searchResults = document.getElementById(`search-results-${tipoInstrutor}`);
        
        if (!searchInput || !searchResults) {
            console.error(`Elementos de busca não encontrados para ${tipoInstrutor}`);
            return;
        }
        
        // Evento de digitação
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            // Fazer requisição para buscar alunos
            const url = showAllStudents || ignoreEligibility ? 
                `/alunos/search/?q=${encodeURIComponent(query)}` : 
                `/alunos/api/search-instrutores/?q=${encodeURIComponent(query)}`;
            
            fetch(url, {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(`Resultados da busca para ${tipoInstrutor}:`, data);
                
                // Limpar resultados anteriores
                searchResults.innerHTML = '';
                
                // Verificar se há erro na resposta
                if (data && data.error) {
                    searchResults.innerHTML = `<div class="list-group-item text-danger">Erro na busca: ${data.error}</div>`;
                    searchResults.style.display = 'block';
                    return;
                }
                
                // Garantir que data seja um array
                const alunos = Array.isArray(data) ? data : [];
                
                if (alunos.length === 0) {
                    searchResults.innerHTML = '<div class="list-group-item">Nenhum resultado encontrado</div>';
                    searchResults.style.display = 'block';
                    return;
                }
                
                // Adicionar resultados
                alunos.forEach(aluno => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.className = 'list-group-item list-group-item-action';
                    item.dataset.cpf = aluno.cpf;
                    item.dataset.nome = aluno.nome;
                    item.dataset.numero = aluno.numero_iniciatico;
                    
                    // Incluir informações de situação se disponíveis
                    const situacaoHtml = aluno.situacao ? 
                        `<small class="badge bg-secondary ms-2">${aluno.situacao}</small>` : '';
                    
                    item.innerHTML = `
                        <div>
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <strong>${aluno.nome}</strong> ${situacaoHtml}
                                </div>
                                <div class="text-muted">
                                    <small>CPF: ${aluno.cpf}</small>
                                    <small class="ms-2">Nº: ${aluno.numero_iniciatico || 'N/A'}</small>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        selectInstructor(
                            this.dataset.cpf,
                            this.dataset.nome,
                            this.dataset.numero,
                            tipoInstrutor
                        );
                        searchResults.style.display = 'none';
                        searchInput.value = '';
                    });
                    
                    searchResults.appendChild(item);
                });
                
                searchResults.style.display = 'block';
            })
            .catch(error => {
                console.error(`Erro na busca de ${tipoInstrutor}:`, error);
                searchResults.innerHTML = `<div class="list-group-item text-danger">Erro na busca: ${error.message}</div>`;
                searchResults.style.display = 'block';
            });        });
        
        // Esconder resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
    
    return {
        init: function(token, allowAllStudents = false) {
            console.log('Inicializando módulo de busca de instrutores');
            csrfToken = token;
            showAllStudents = allowAllStudents;
            
            // Configurar busca para cada tipo de instrutor
            setupInstructorSearch('instrutor');
            setupInstructorSearch('instrutor-auxiliar');
            setupInstructorSearch('auxiliar-instrucao');
            
            console.log(`Modo de exibição: ${showAllStudents ? 'todos os alunos' : 'apenas elegíveis'}`);
            
            // Verificar se o modo de depuração está ativo
            const debugSwitch = document.getElementById('ignore-eligibility');
            if (debugSwitch) {
                ignoreEligibility = debugSwitch.checked;
                console.log(`Modo de depuração: ${ignoreEligibility ? 'ativo' : 'inativo'}`);
            }
        },
        
        setIgnoreEligibility: function(value) {
            ignoreEligibility = value;
            console.log(`Modo de depuração ${ignoreEligibility ? 'ativado' : 'desativado'}`);
        }
    };
})();

