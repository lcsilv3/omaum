# Script para copiar fotos de teste para o container
# Uso: .\scripts\copiar_fotos_teste.ps1 <caminho_origem_fotos>

param(
    [Parameter(Mandatory=$true)]
    [string]$OrigemFotos
)

if (-not (Test-Path $OrigemFotos)) {
    Write-Host "❌ Diretório não encontrado: $OrigemFotos" -ForegroundColor Red
    exit 1
}

Write-Host "📁 Listando fotos em: $OrigemFotos" -ForegroundColor Cyan
Get-ChildItem $OrigemFotos -File | Select-Object Name, Length | Format-Table

Write-Host "`n📤 Copiando fotos para o container..." -ForegroundColor Cyan

# Cria diretório no container
docker exec omaum-web-prod mkdir -p /app/media/alunos/fotos

# Copia todas as fotos
Get-ChildItem $OrigemFotos -File | ForEach-Object {
    Write-Host "  Copiando: $($_.Name)" -ForegroundColor Gray
    docker cp $_.FullName "omaum-web-prod:/app/media/alunos/fotos/$($_.Name)"
}

Write-Host "`n✅ Fotos copiadas com sucesso!" -ForegroundColor Green
Write-Host "`n📋 Verificando fotos no container:" -ForegroundColor Cyan
docker exec omaum-web-prod ls -lh /app/media/alunos/fotos/
