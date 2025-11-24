################################################################################
# Script auxiliar: executa 02_deploy_atualizar_producao.ps1 respondendo "sim"
# a todos os prompts, reproduzindo no ambiente de producao tudo que esta no
# desenvolvimento. Este utilitario serve para administradores que precisam
# rodar o fluxo completo sem interacao manual.
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

$deployScript = Join-Path $ProjectRoot "scripts/deploy/02_deploy_atualizar_producao.ps1"
if (!(Test-Path $deployScript)) {
    throw "Script base nao encontrado em: $deployScript"
}

# Sequencia de respostas fornecida ao script 02:
#  1) confirma execucao do fluxo completo
#  2) autoriza criar commit pendente
#  3) define mensagem do commit
#  4) autoriza git pull
#  5) confirma importacao dos dados de desenvolvimento
$responses = @(
    "y",
    "y",
    $CommitMessage,
    "y",
    "y"
)

# Arquivos temporarios para redirecionar entrada/saida/erros do processo filho
$inputFile = Join-Path ([System.IO.Path]::GetTempPath()) ("omaum-deploy-input-" + [guid]::NewGuid().ToString() + ".txt")
$outputFile = Join-Path ([System.IO.Path]::GetTempPath()) ("omaum-deploy-out-" + [guid]::NewGuid().ToString() + ".log")
$errorFile = Join-Path ([System.IO.Path]::GetTempPath()) ("omaum-deploy-err-" + [guid]::NewGuid().ToString() + ".log")

try {
    # Grava respostas para alimentar o Read-Host do script principal
    $responses | Set-Content -Path $inputFile -Encoding ASCII

    Write-Host "Executando script de deploy automatico utilizando respostas pre-definidas..." -ForegroundColor Cyan
    Write-Host "Log de saida: $outputFile" -ForegroundColor White
    Write-Host "Log de erro: $errorFile" -ForegroundColor White

    $arguments = @(
        "-NoLogo",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", $deployScript
    )

    # Roda o script 02 em um novo processo para que possamos enviar stdin
    $process = Start-Process -FilePath "powershell.exe" `
        -ArgumentList $arguments `
        -WorkingDirectory $ProjectRoot `
        -RedirectStandardInput $inputFile `
        -RedirectStandardOutput $outputFile `
        -RedirectStandardError $errorFile `
        -PassThru -Wait

    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "SAIDA COMPLETA DO SCRIPT 02:" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    if (Test-Path $outputFile) {
        Get-Content $outputFile | ForEach-Object { Write-Host $_ }
    }

    if ((Test-Path $errorFile) -and (Get-Item $errorFile).Length -gt 0) {
        Write-Host "============================================================" -ForegroundColor Yellow
        Write-Host "ERROS/ALERTAS:" -ForegroundColor Yellow
        Write-Host "============================================================" -ForegroundColor Yellow
        Get-Content $errorFile | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
    }

    if ($process.ExitCode -ne 0) {
        throw "Script retornou codigo de saida $($process.ExitCode). Consulte os logs acima."
    }

    Write-Host "Deploy automatizado concluido com sucesso." -ForegroundColor Green
} finally {
    Remove-Item -ErrorAction SilentlyContinue $inputFile, $outputFile, $errorFile
}
