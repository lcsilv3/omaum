import os


def update_template_extends(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".html"):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()

                if '{% extends "core/base.html" %}' in content:
                    content = content.replace(
                        '{% extends "core/base.html" %}',
                        '{% extends "base.html" %}',
                    )
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(content)
                    print(f"Updated: {filepath}")


if __name__ == "__main__":
    project_root = "C:\\projetos\\omaum"
    update_template_extends(project_root)
