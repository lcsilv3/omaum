@echo off
setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
pushd "%SCRIPT_DIR%.."

for %%I in (pwsh.exe powershell.exe) do (
	where %%I >nul 2>nul
	if not errorlevel 1 (
		set SHELL=%%I
		goto :found
	)
)

echo [ERRO] Não foi possível localizar o PowerShell.
pause
goto :eof

:found
set TARGET_ENV=
echo Selecione o ambiente alvo:
echo   [D] Desenvolvimento
echo   [P] Producao
choice /C DP /M "Escolha uma opcao"
if errorlevel 2 (
	set TARGET_ENV=prod
) else (
	set TARGET_ENV=dev
)
%SHELL% -ExecutionPolicy Bypass -NoLogo -File "scripts\run_omaum.ps1" -Environment %TARGET_ENV%

popd
pause