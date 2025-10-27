@echo off
chcp 65001 > nul
setlocal

echo.
echo =================================================================
echo      SCRIPT DE MANUTENCAO E VERIFICACAO DE AMBIENTE WSL
echo =================================================================
echo.
echo Este script ira realizar as seguintes acoes:
echo 1. Definir a versao padrao do WSL para 2.
echo 2. Tentar atualizar o WSL.
echo 3. Verificar se as features do Windows necessarias estao ativadas.
echo 4. Exibir boas praticas e dicas para o uso do Docker com WSL.
echo.
pause

:wsl_version
echo.
echo --- 1. CONFIGURANDO A VERSAO PADRAO DO WSL ---
echo Definindo a versao padrao do WSL para 2...
wsl --set-default-version 2
echo.
echo Concluido. Se houver algum erro, ele sera exibido acima.
echo.
pause

:wsl_update
echo.
echo --- 2. ATUALIZANDO O WSL ---
echo Procurando por atualizacoes do WSL...
wsl --update
echo.
echo Concluido. O WSL foi atualizado se uma nova versao foi encontrada.
echo.
pause

:check_features
echo.
echo --- 3. VERIFICANDO FEATURES DO WINDOWS ---
echo Verificando "Plataforma de Maquina Virtual"...
dism /online /Get-FeatureInfo /FeatureName:VirtualMachinePlatform | findstr /i "Estado : Ativado" > nul
if %errorlevel% == 0 (
    echo   [OK] "Plataforma de Maquina Virtual" esta ativada.
) else (
    echo   [AVISO] "Plataforma de Maquina Virtual" NAO esta ativada.
    echo   Para ativar, execute o seguinte comando em um PowerShell como Administrador:
    echo   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
)
echo.

echo Verificando "Subsistema do Windows para Linux"...
dism /online /Get-FeatureInfo /FeatureName:Microsoft-Windows-Subsystem-Linux | findstr /i "Estado : Ativado" > nul
if %errorlevel% == 0 (
    echo   [OK] "Subsistema do Windows para Linux" esta ativado.
) else (
    echo   [AVISO] "Subsistema do Windows para Linux" NAO esta ativado.
    echo   Para ativar, execute o seguinte comando em um PowerShell como Administrador:
    echo   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
)
echo.
echo Apos ativar qualquer feature, e necessario reiniciar o computador.
echo.
pause

:best_practices
echo.
echo --- 4. BOAS PRATICAS E DICAS ADICIONAIS ---
echo.
echo Lembre-se das seguintes praticas para evitar problemas:
echo.
echo   [SHUTDOWN]
echo   - Feche o Docker Desktop pelo menu da bandeja (tray icon) ANTES de desligar o PC.
echo     Isso garante um encerramento limpo das VMs do WSL.
echo.
echo   [STARTUP]
echo   - Apos reiniciar o PC, espere alguns segundos antes de abrir o Docker Desktop.
echo   - Verifique o status do WSL com o comando: wsl --status
echo.
echo   [INICIALIZACAO AUTOMATICA (AVANCADO)]
echo   - Se precisar que uma distro WSL suba com o boot, crie uma Tarefa Agendada
echo     com um atraso de 1 a 2 minutos.
echo     Comando para a tarefa: wsl.exe -d <sua-distro>
echo     (Substitua <sua-distro> pelo nome da sua distribuicao, ex: Ubuntu).
echo.
echo   [TROUBLESHOOTING]
echo   - Se os problemas persistirem, verifique o Visualizador de Eventos do Windows em:
echo     Logs de Aplicativos e Servicos > Microsoft > Windows > WSL
echo   - Em casos de corrupcao, pode ser necessario recriar as distros do Docker:
echo     wsl --unregister docker-desktop
echo     wsl --unregister docker-desktop-data
echo     (AVISO: Isso apagara todas as suas imagens e containers Docker).
echo.
pause

echo.
echo =================================================================
echo      VERIFICACAO CONCLUIDA
echo =================================================================
echo.

endlocal