import os
import re
import chardet


def read_file_content(filepath):
    # Detectar a codificação do arquivo
    with open(filepath, "rb") as file:
        raw_data = file.read()
    detected = chardet.detect(raw_data)
    encoding = detected["encoding"]

    # Tentar ler o arquivo com a codificação detectada
    try:
        with open(filepath, "r", encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError:
        # Se falhar, tentar com outras codificações comuns
        for enc in ["utf-8", "latin-1", "iso-8859-1", "cp1252"]:
            try:
                with open(filepath, "r", encoding=enc) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue

    print(f"Não foi possível ler o arquivo: {filepath}")
    return ""


def check_views(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                content = read_file_content(filepath)

                # Procurar por render() com caminhos de template explícitos
                matches = re.findall(r'render\([^)]*,\s*[\'"]([^\'"]+)[\'"]', content)
                for match in matches:
                    if "/" in match or "\\" in match:
                        print(f"Possible template path to update in {filepath}:")
                        print(f"  {match}")


if __name__ == "__main__":
    project_root = "C:\\projetos\\omaum"
    check_views(project_root)
