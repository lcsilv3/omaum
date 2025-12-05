param(
    [string]$ShortcutName = "OMAUM - Iniciar",
    [ValidateSet('dev','prod')]
    [string]$Environment,
    [string]$AppUrl
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Get-Item -LiteralPath $PSScriptRoot).Parent.FullName
$runner = Join-Path $PSScriptRoot 'run_omaum.ps1'
if (-not (Test-Path $runner)) {
    throw "Script run_omaum.ps1 não foi encontrado em $runner"
}

$desktop = [Environment]::GetFolderPath('Desktop')
if (-not (Test-Path $desktop)) {
    throw 'Não foi possível localizar a área de trabalho do usuário.'
}

$shortcutPath = Join-Path $desktop "$ShortcutName.lnk"

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
$arguments = "-ExecutionPolicy Bypass -NoLogo -File `"$runner`""
if (-not [string]::IsNullOrWhiteSpace($Environment)) {
    $arguments += " -Environment $Environment"
}
if (-not [string]::IsNullOrWhiteSpace($AppUrl)) {
    $arguments += " -AppUrl `"$AppUrl`""
}
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = $repoRoot
$shortcut.Save()

Write-Host "Atalho criado em: $shortcutPath" -ForegroundColor Cyan
