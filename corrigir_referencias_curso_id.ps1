# Lista de arquivos de template de alunos para verificar
$templateFiles = @(
    "alunos/templates/alunos/listar_alunos.html",
    "alunos/templates/alunos/detalhar_aluno.html",
    "alunos/templates/alunos/editar_aluno.html",
    "alunos/templates/alunos/criar_aluno.html",
    "alunos/templates/alunos/excluir_aluno.html"
)

foreach ($file in $templateFiles) {
    if (Test-Path $file) {
        Write-Host "Processando arquivo: $file" -ForegroundColor Cyan
        
        # Ler o conteúdo do arquivo
        $content = Get-Content -Path $file -Raw
        
        # Substituir curso.id por curso.codigo_curso
        $newContent = $content -replace "curso\.id", "curso.codigo_curso"
        
        # Também substituir em URLs relacionadas a cursos
        $newContent = $newContent -replace "{% url 'cursos:detalhar_curso' ([^\.]+)\.id %}", "{% url 'cursos:detalhar_curso' `$1.codigo_curso %}"
        $newContent = $newContent -replace "{% url 'cursos:editar_curso' ([^\.]+)\.id %}", "{% url 'cursos:editar_curso' `$1.codigo_curso %}"
        $newContent = $newContent -replace "{% url 'cursos:excluir_curso' ([^\.]+)\.id %}", "{% url 'cursos:excluir_curso' `$1.codigo_curso %}"
        
        # Verificar se houve alterações
        if ($content -ne $newContent) {
            # Salvar o arquivo com o novo conteúdo
            $newContent | Set-Content -Path $file
            Write-Host "  ✓ Substituições realizadas e arquivo salvo" -ForegroundColor Green
        } else {
            Write-Host "  ✓ Nenhuma substituição necessária" -ForegroundColor Yellow
        }
    } else {
        Write-Host "Arquivo não encontrado: $file" -ForegroundColor Red
    }
}

# Verificar também outros templates que podem referenciar cursos
$otherTemplates = @(
    "matriculas/templates/matriculas/realizar_matricula.html",
    "matriculas/templates/matriculas/listar_matriculas.html",
    "matriculas/templates/matriculas/detalhes_matricula.html",
    "turmas/templates/turmas/criar_turma.html",
    "turmas/templates/turmas/editar_turma.html",
    "turmas/templates/turmas/listar_turmas.html",
    "turmas/templates/turmas/detalhar_turma.html"
)

foreach ($file in $otherTemplates) {
    if (Test-Path $file) {
        Write-Host "Processando arquivo adicional: $file" -ForegroundColor Cyan
        
        # Ler o conteúdo do arquivo
        $content = Get-Content -Path $file -Raw
        
        # Substituir curso.id por curso.codigo_curso
        $newContent = $content -replace "curso\.id", "curso.codigo_curso"
        
        # Também substituir em URLs relacionadas a cursos
        $newContent = $newContent -replace "{% url 'cursos:detalhar_curso' ([^\.]+)\.id %}", "{% url 'cursos:detalhar_curso' `$1.codigo_curso %}"
        $newContent = $newContent -replace "{% url 'cursos:editar_curso' ([^\.]+)\.id %}", "{% url 'cursos:editar_curso' `$1.codigo_curso %}"
        $newContent = $newContent -replace "{% url 'cursos:excluir_curso' ([^\.]+)\.id %}", "{% url 'cursos:excluir_curso' `$1.codigo_curso %}"
        
        # Verificar se houve alterações
        if ($content -ne $newContent) {
            # Salvar o arquivo com o novo conteúdo
            $newContent | Set-Content -Path $file
            Write-Host "  ✓ Substituições realizadas e arquivo salvo" -ForegroundColor Green
        } else {
            Write-Host "  ✓ Nenhuma substituição necessária" -ForegroundColor Yellow
        }
    } else {
        Write-Host "Arquivo adicional não encontrado: $file" -ForegroundColor Red
    }
}

Write-Host "`nProcesso concluído!" -ForegroundColor Green
