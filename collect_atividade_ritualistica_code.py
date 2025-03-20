import os
root_dir = "C:\\projetos\\omaum\\punicoes"
def collect_code(root_dir, output_file):
    files_to_check = [
        ('atividades/models.py', 'AtividadeRitualistica Model'),
        ('atividades/forms.py', 'AtividadeRitualisticaForm'),
        ('atividades/views.py', 'AtividadeRitualistica Views'),
        ('atividades/urls.py', 'AtividadeRitualistica URLs'),
        ('atividades/templates/atividades/criar_atividade_ritualistica.html', 'Create AtividadeRitualistica Template'),
        ('atividades/templates/atividades/editar_atividade_ritualistica.html', 'Edit AtividadeRitualistica Template'),
        ('atividades/templates/atividades/listar_atividades_ritualisticas.html', 'List AtividadeRitualistica Template'),
    ]

    with open(output_file, 'w', encoding='utf-8') as md_file:
        md_file.write("# AtividadeRitualistica Code Review\n\n")

        for file_path, section_title in files_to_check:
            full_path = os.path.join(root_dir, file_path)
            if os.path.exists(full_path):
                md_file.write(f"## {section_title}\n\n")
                md_file.write(f"**File: {file_path}**\n\n")
                md_file.write("```python\n")
                with open(full_path, 'r', encoding='utf-8') as code_file:
                    md_file.write(code_file.read())
                md_file.write("```\n\n")
            else:
                md_file.write(f"## {section_title}\n\n")
                md_file.write(f"**File: {file_path}**\n\n")
                md_file.write("File not found.\n\n")

if __name__ == "__main__":
    project_root = "C:/projetos/omaum"  # Update this to your project root
    output_file = "atividade_ritualistica_code_review.md"
    collect_code(project_root, output_file)
    print(f"Code review file generated: {output_file}")