# Lista de arquivos de template para verificar
$templateFiles = @(
    "cursos/templates/cursos/detalhar_curso.html",
    "cursos/templates/cursos/listar_cursos.html",
    "cursos/templates/cursos/editar_curso.html",
    "cursos/templates/cursos/excluir_curso.html"
)

foreach ($file in $templateFiles) {
    if (Test-Path $file) {
        Write-Host "Processando arquivo: $file" -ForegroundColor Cyan
        
        # Ler o conteúdo do arquivo
        $content = Get-Content -Path $file -Raw
        
        # Substituir curso.id por curso.codigo_curso
        $newContent = $content -replace "curso\.id", "curso.codigo_curso"
        
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

Write-Host "`nProcesso concluído!" -ForegroundColor Green
