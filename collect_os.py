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
