# Caminho para o arquivo
$filePath = "cursos/templates/cursos/detalhar_curso.html"

# Verificar se o arquivo existe
if (Test-Path $filePath) {
    # Ler o conteúdo do arquivo
    $content = Get-Content -Path $filePath -Raw
    
    # Substituir todas as ocorrências de curso.id por curso.codigo_curso
    $newContent = $content -replace "curso\.id", "curso.codigo_curso"
    
    # Salvar o arquivo com o novo conteúdo
    $newContent | Set-Content -Path $filePath
    
    Write-Host "Substituição concluída com sucesso no arquivo $filePath" -ForegroundColor Green
    Write-Host "Ocorrências de 'curso.id' foram substituídas por 'curso.codigo_curso'"
} else {
    Write-Host "Erro: O arquivo $filePath não foi encontrado!" -ForegroundColor Red
}