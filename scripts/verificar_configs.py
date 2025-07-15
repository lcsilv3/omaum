import os


def check_config_files(root_dir):
    config_files = ["settings.py", "tests.py", "conftest.py"]
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename in config_files:
                filepath = os.path.join(dirpath, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()

                # Procurar por referências a templates ou DIRS
                if "TEMPLATES" in content or "DIRS" in content:
                    print(f"Possible template configuration in {filepath}")
                    print("Please review this file manually.")


if __name__ == "__main__":
    project_root = "C:\\projetos\\omaum"
    check_config_files(project_root)
