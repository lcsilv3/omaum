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