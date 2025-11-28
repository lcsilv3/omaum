# Script de Deploy - Signals de Atualização Automática de grau_atual
# Data: 27/11/2025
# Commit: 475e4b84

Write-Host "`n=== DEPLOY: Atualização Automática de grau_atual ===" -ForegroundColor Cyan
Write-Host "Commit: 475e4b84" -ForegroundColor Yellow
Write-Host "Arquivos: signals.py, apps.py, forms.py, templates`n" -ForegroundColor Yellow

# Verificar se Docker está rodando
Write-Host "1. Verificando containers Docker..." -ForegroundColor Green
docker ps --filter "name=omaum-web-prod" --format "{{.Names}} - {{.Status}}" | Out-Host

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Container omaum-web-prod não encontrado!" -ForegroundColor Red
    exit 1
}

# Backup antes do deploy
Write-Host "`n2. Criando backup do banco de dados..." -ForegroundColor Green
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "backup_pre_deploy_signals_$timestamp.dump"

docker exec omaum-db-prod pg_dump -U postgres -d omaum_db -Fc -f "/backups/$backupFile"
Write-Host "✅ Backup criado: /backups/$backupFile" -ForegroundColor Green

# Copiar arquivos para o container
Write-Host "`n3. Copiando arquivos modificados para produção..." -ForegroundColor Green

$files = @(
    @{Source="matriculas/signals.py"; Dest="/app/matriculas/signals.py"},
    @{Source="matriculas/apps.py"; Dest="/app/matriculas/apps.py"},
    @{Source="alunos/forms.py"; Dest="/app/alunos/forms.py"},
    @{Source="alunos/templates/alunos/formulario_aluno.html"; Dest="/app/alunos/templates/alunos/formulario_aluno.html"},
    @{Source="matriculas/README_SIGNALS_GRAU_ATUAL.md"; Dest="/app/matriculas/README_SIGNALS_GRAU_ATUAL.md"}
)

foreach ($file in $files) {
    Write-Host "   Copiando $($file.Source)..." -ForegroundColor Yellow
    docker cp $file.Source "omaum-web-prod:$($file.Dest)"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ $($file.Source)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Erro ao copiar $($file.Source)" -ForegroundColor Red
        exit 1
    }
}

# Verificar arquivos copiados
Write-Host "`n4. Verificando arquivos em produção..." -ForegroundColor Green
docker exec omaum-web-prod ls -lh /app/matriculas/signals.py /app/matriculas/apps.py | Out-Host

# Restart do container para carregar signals
Write-Host "`n5. Reiniciando container para carregar signals..." -ForegroundColor Green
docker restart omaum-web-prod

Write-Host "   Aguardando container inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verificar saúde do container
Write-Host "`n6. Verificando saúde do container..." -ForegroundColor Green
$health = docker inspect omaum-web-prod --format='{{.State.Health.Status}}'
Write-Host "   Status: $health" -ForegroundColor $(if ($health -eq "healthy") { "Green" } else { "Red" })

# Verificar logs para erros
Write-Host "`n7. Verificando logs (últimas 30 linhas)..." -ForegroundColor Green
docker logs omaum-web-prod --tail 30 | Out-Host

# Testar se signals estão funcionando
Write-Host "`n8. Testando import dos signals..." -ForegroundColor Green
docker exec omaum-web-prod python -c "from matriculas import signals; print('✅ Signals carregados com sucesso!')" | Out-Host

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ DEPLOY CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
    Write-Host "`nPróximos passos:" -ForegroundColor Cyan
    Write-Host "1. Acesse http://192.168.15.4/admin/" -ForegroundColor White
    Write-Host "2. Matricule um aluno em uma turma" -ForegroundColor White
    Write-Host "3. Verifique se o campo grau_atual foi atualizado automaticamente" -ForegroundColor White
    Write-Host "4. Confira os logs: docker logs omaum-web-prod --tail 50 -f`n" -ForegroundColor White
} else {
    Write-Host "`n❌ DEPLOY FALHOU! Verifique os logs acima." -ForegroundColor Red
    Write-Host "Para rollback, restaure o backup: $backupFile`n" -ForegroundColor Yellow
}
