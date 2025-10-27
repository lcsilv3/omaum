@echo off
chcp 65001 > nul
setlocal

REM Garante que o diretorio de logs exista
if not exist "c:\projetos\omaum\logs" mkdir "c:\projetos\omaum\logs"

REM Inicia o arquivo de log
echo. > "c:\projetos\omaum\logs\wsl_maintenance.log"
echo ================================================================= >> "c:\projetos\omaum\logs\wsl_maintenance.log"
echo      INICIO DA MANUTENCAO AUTOMATIZADA DO WSL - %date% %time% >> "c:\projetos\omaum\logs\wsl_maintenance.log"
echo ================================================================= >> "c:\projetos\omaum\logs\wsl_maintenance.log"
echo. >> "c:\projetos\omaum\logs\wsl_maintenance.log"

echo [PASSO 1/3] Definindo a versao padrao do WSL para 2... >> "c:\projetos\omaum\logs\wsl_maintenance.log"
wsl --set-default-version 2 >> "c:\projetos\omaum\logs\wsl_maintenance.log" 2>&1
echo. >> "c:\projetos\omaum\logs\wsl_maintenance.log"

echo [PASSO 2/3] Buscando atualizacoes do WSL... >> "c:\projetos\omaum\logs\wsl_maintenance.log"
wsl --update >> "c:\projetos\omaum\logs\wsl_maintenance.log" 2>&1
echo. >> "c:\projetos\omaum\logs\wsl_maintenance.log"

echo [PASSO 3/3] Verificando features do Windows... >> "c:\projetos\omaum\logs\wsl_maintenance.log"
dism /online /Get-FeatureInfo /FeatureName:VirtualMachinePlatform | findstr /i "Estado : Ativado" > nul
if %errorlevel% == 0 (
    echo   [OK] "Plataforma de Maquina Virtual" esta ativada. >> "c:\projetos\omaum\logs\wsl_maintenance.log"
) else (
    echo   [AVISO] "Plataforma de Maquina Virtual" NAO esta ativada. >> "c:\projetos\omaum\logs\wsl_maintenance.log"
)

dism /online /Get-FeatureInfo /FeatureName:Microsoft-Windows-Subsystem-Linux | findstr /i "Estado : Ativado" > nul
if %errorlevel% == 0 (
    echo   [OK] "Subsistema do Windows para Linux" esta ativado. >> "c:\projetos\omaum\logs\wsl_maintenance.log"
) else (
    echo   [AVISO] "Subsistema do Windows para Linux" NAO esta ativado. >> "c:\projetos\omaum\logs\wsl_maintenance.log"
)
echo. >> "c:\projetos\omaum\logs\wsl_maintenance.log"

echo ================================================================= >> "c:\projetos\omaum\logs\wsl_maintenance.log"
echo      FIM DA MANUTENCAO - %date% %time% >> "c:\projetos\omaum\logs\wsl_maintenance.log"
echo ================================================================= >> "c:\projetos\omaum\logs\wsl_maintenance.log"

endlocal
