# Documentação dos Relatórios e Navegação Centralizada – OmAum

## 1. Visão Geral dos Relatórios
O sistema OmAum oferece um módulo robusto de relatórios para acompanhamento de frequência, presenças, faltas e carências dos alunos. Os principais relatórios disponíveis são:
- **Relatório Consolidado de Presença**: visão geral por turma e período.
- **Boletim de Frequência do Aluno**: detalhamento mensal individual.
- **Frequência por Atividade**: análise por atividade específica.
- **Relatório de Faltas**: lista alunos com mais faltas.
- **Alunos com Carência**: identifica alunos que atingiram o limite de carência.

Todos os relatórios podem ser acessados de forma centralizada pelo dashboard de relatórios.

## 2. Navegação Centralizada
- O menu "Relatórios" está disponível na barra de navegação principal.
- O menu é populado dinamicamente, listando todos os relatórios registrados nos arquivos `reports.py` de cada app.
- O dashboard centralizado apresenta cards para cada relatório, facilitando o acesso e a visualização.

## 3. Filtros e Exportações
- Cada relatório possui filtros específicos (curso, turma, aluno, período, etc.).
- Os filtros são dinâmicos e interdependentes, atualizados via AJAX para melhor experiência do usuário.
- Exportações disponíveis: CSV, Excel (quando aplicável) e PDF (renderizado via WeasyPrint).
- Os botões de exportação estão presentes nos templates dos relatórios.

## 4. AJAX e Experiência do Usuário
- A atualização dos dados dos relatórios é feita sem recarregar a página, utilizando JavaScript e endpoints AJAX.
- Mudanças em qualquer filtro atualizam automaticamente as opções dos demais e a tabela de resultados.

## 5. Testes Automatizados
- O módulo de relatórios possui cobertura de testes para:
  - Exportação de todos os formatos (CSV, Excel, PDF)
  - Views AJAX e respostas JSON/HTML
  - Cenários de erro (parâmetros inválidos/ausentes)
- Os testes garantem robustez e evitam regressões.

## 6. Expansão e Manutenção
- Para adicionar um novo relatório:
  1. Crie o arquivo `reports.py` (se não existir) no app desejado.
  2. Registre o novo relatório na lista `RELATORIOS` seguindo o padrão:
     ```python
     RELATORIOS = [
         {
             'nome': 'Nome do Relatório',
             'descricao': 'Descrição resumida',
             'url': 'app:rota_url',
             'exportacoes': ['csv', 'pdf', 'excel']
         },
         # ...
     ]
     ```
  3. Implemente a view, template e filtros conforme os exemplos existentes.
  4. O menu centralizado detectará automaticamente o novo relatório.

- Boas práticas:
  - Utilize sempre views baseadas em função.
  - Use `importlib.import_module` para evitar importações circulares.
  - Mantenha os filtros dinâmicos e a experiência AJAX.

## 7. Histórico de Alterações
- 2025-09-16: Documentação inicial criada, cobrindo todos os tópicos do módulo de relatórios e navegação centralizada.
- [Adicione aqui futuras alterações e melhorias.]

---

**Dúvidas ou sugestões:** Consulte o time de desenvolvimento ou a documentação técnica dos apps específicos.
