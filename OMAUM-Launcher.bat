@echo off
REM Launcher do OMAUM - Desenvolvimento e Produção
REM Arquivo .bat que permite fixar na barra de tarefas

setlocal enabledelayedexpansion

powershell -NoLogo -ExecutionPolicy Bypass -File "%~dp0scripts\docker\launcher.ps1"
pause
