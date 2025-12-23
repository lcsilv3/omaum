$ErrorActionPreference = 'Stop'
$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop 'OMAUM - Launcher.lnk'
$target = 'E:\projetos\omaum\OMAUM-Launcher.bat'
$working = 'E:\projetos\omaum'
$icon = 'E:\projetos\omaum\static\img\logo.png,0'

# Remove atalho antigo se existir
if (Test-Path $shortcutPath) { Remove-Item $shortcutPath -Force }

$w = New-Object -ComObject WScript.Shell
$s = $w.CreateShortcut($shortcutPath)
$s.TargetPath = $target
$s.WorkingDirectory = $working
$s.IconLocation = $icon
$s.Save()

Write-Host "✅ Criado: $shortcutPath"
Write-Host "Agora clique direito no atalho → 'Fixar na barra de tarefas'"