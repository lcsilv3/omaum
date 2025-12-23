$ErrorActionPreference = 'Stop'
$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop 'OMAUM - Launcher.lnk'
$target = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
$arguments = '-ExecutionPolicy Bypass -NoLogo -File "E:\projetos\omaum\scripts\docker\launcher.ps1"'
$working = 'E:\projetos\omaum'
$icon = 'E:\projetos\omaum\static\img\logo.png,0'
$w = New-Object -ComObject WScript.Shell
$s = $w.CreateShortcut($shortcutPath)
$s.TargetPath = $target
$s.Arguments = $arguments
$s.WorkingDirectory = $working
$s.IconLocation = $icon
$s.Save()
Write-Host "Criado: $shortcutPath"