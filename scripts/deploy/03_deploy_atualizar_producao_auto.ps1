################################################################################
# Script auxiliar: executa 02_deploy_atualizar_producao.ps1 com interacao
# do usuario no terminal. Define a variavel OMAUM_DEPLOY_COMMIT_MESSAGE para
# usar a mensagem de commit fornecida via parametro.
#
# Uso sugerido:
#   powershell -ExecutionPolicy Bypass -File scripts/deploy/03_deploy_...
#     -ProjectRoot "c:\projetos\omaum" -CommitMessage "SYNC DEV -> PROD"
################################################################################
param(
    [string]$ProjectRoot = "c:\projetos\omaum",  # Raiz do repo no servidor
    [string]$CommitMessage = "ATUALIZACAO AUTOMATICA"  # Mensagem usada no git commit
)

$ErrorActionPreference = "Stop"

$originalCommitMessageEnv = $env:OMAUM_DEPLOY_COMMIT_MESSAGE
$env:OMAUM_DEPLOY_COMMIT_MESSAGE = $CommitMessage

$deployScript = Join-Path $ProjectRoot "scripts/deploy/02_deploy_atualizar_producao.ps1"
if (!(Test-Path $deployScript)) {
    throw "Script base nao encontrado em: $deployScript"
}

try {
    Write-Host "Executando script de deploy com interacao no terminal..." -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location $ProjectRoot
    & $deployScript
    
    Write-Host ""
    Write-Host "Deploy concluido." -ForegroundColor Green
} finally {
    if ($null -ne $originalCommitMessageEnv) {
        $env:OMAUM_DEPLOY_COMMIT_MESSAGE = $originalCommitMessageEnv
    } else {
        Remove-Item Env:OMAUM_DEPLOY_COMMIT_MESSAGE -ErrorAction SilentlyContinue
    }
}
