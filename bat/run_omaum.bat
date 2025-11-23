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
%SHELL% -ExecutionPolicy Bypass -NoLogo -File "scripts\run_omaum.ps1"

popd
pause