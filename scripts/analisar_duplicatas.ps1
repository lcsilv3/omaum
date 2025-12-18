# Script de Análise de Arquivos Duplicados
# Compara tamanho, hash e data de modificação

$rootPath = "E:\projetos\omaum"
Set-Location $rootPath

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  ANÁLISE SISTEMÁTICA DE ARQUIVOS DUPLICADOS - PROJETO OMAUM  ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Definir todos os pares de arquivos duplicados
$jsFiles = @(
    # Módulo alunos
    @{Name="detalhar_aluno.js"; App="alunos\static\alunos\js"; Root="static\alunos\js"},
    @{Name="diagnostico_instrutores.js"; App="alunos\static\alunos\js"; Root="static\alunos\js"},
    @{Name="formulario_aluno.js"; App="alunos\static\alunos\js"; Root="static\alunos\js"},
    @{Name="listar_alunos.js"; App="alunos\static\alunos\js"; Root="static\alunos\js"},
    @{Name="painel_alunos.js"; App="alunos\static\alunos\js"; Root="static\alunos\js"},
    
    # Módulo presencas
    @{Name="convocacao.js"; App="presencas\static\presencas\js"; Root="static\presencas\js"},
    @{Name="registro_rapido.js"; App="presencas\static\presencas\js"; Root="static\presencas\js"},
    @{Name="tabela-consolidada.js"; App="presencas\static\presencas\js"; Root="static\presencas\js"},
    @{Name="presenca_app.js"; App="presencas\static\presencas"; Root="static\presencas"},
    @{Name="presenca_app_fixed.js"; App="presencas\static\presencas"; Root="static\presencas"},
    
    # Módulo relatorios_presenca
    @{Name="filtros_dinamicos.js"; App="relatorios_presenca\static\relatorios_presenca\js"; Root="static\relatorios_presenca\js"},
    
    # Outros módulos
    @{Name="pagamento_form.js"; App="pagamentos\static\pagamentos\js"; Root="static\pagamentos\js"},
    @{Name="frequencia_form.js"; App="frequencias\static\js"; Root="static\js"}
)

$cssFiles = @(
    # Módulo alunos
    @{Name="timeline.css"; App="alunos\static\alunos\css"; Root="static\alunos\css"},
    
    # Módulo presencas
    @{Name="presenca_estilos.css"; App="presencas\static\presencas"; Root="static\presencas"},
    @{Name="registro_rapido.css"; App="presencas\static\presencas\css"; Root="static\presencas\css"},
    @{Name="tabela-consolidada.css"; App="presencas\static\presencas\css"; Root="static\presencas\css"},
    @{Name="tabela-interativa.css"; App="presencas\static\presencas\css"; Root="static\presencas\css"}
)

$identicos = 0
$diferentes = 0
$totalSize = 0

function Analyze-FilePair {
    param($FileInfo)
    
    $path1 = Join-Path $rootPath "$($FileInfo.App)\$($FileInfo.Name)"
    $path2 = Join-Path $rootPath "$($FileInfo.Root)\$($FileInfo.Name)"
    
    if (-not (Test-Path $path1)) {
        Write-Host "⚠ AVISO: Arquivo não encontrado: $path1" -ForegroundColor Yellow
        return $null
    }
    
    if (-not (Test-Path $path2)) {
        Write-Host "⚠ AVISO: Arquivo não encontrado: $path2" -ForegroundColor Yellow
        return $null
    }
    
    $file1 = Get-Item $path1
    $file2 = Get-Item $path2
    
    $hash1 = (Get-FileHash $path1 -Algorithm MD5).Hash
    $hash2 = (Get-FileHash $path2 -Algorithm MD5).Hash
    
    $identical = ($hash1 -eq $hash2)
    
    Write-Host "`n┌─────────────────────────────────────────────────────────────┐" -ForegroundColor Gray
    Write-Host "│ $($FileInfo.Name)" -ForegroundColor White
    Write-Host "└─────────────────────────────────────────────────────────────┘" -ForegroundColor Gray
    
    Write-Host "  📁 App/static:  $($file1.Length.ToString().PadLeft(8)) bytes | Modificado: $($file1.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"
    Write-Host "  📁 static/   :  $($file2.Length.ToString().PadLeft(8)) bytes | Modificado: $($file2.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))"
    
    if ($identical) {
        Write-Host "  ✓ STATUS: IDÊNTICOS (hash MD5 igual)" -ForegroundColor Green
        $script:identicos++
        $script:totalSize += $file2.Length
    } else {
        Write-Host "  ⚠ STATUS: DIFERENTES (conteúdo divergente)" -ForegroundColor Red
        Write-Host "  Δ Diferença de tamanho: $($file1.Length - $file2.Length) bytes"
        $script:diferentes++
        
        # Verificar qual é mais recente
        if ($file1.LastWriteTime -gt $file2.LastWriteTime) {
            Write-Host "  ⏰ App/static/ é MAIS RECENTE" -ForegroundColor Yellow
        } elseif ($file2.LastWriteTime -gt $file1.LastWriteTime) {
            Write-Host "  ⏰ static/ é MAIS RECENTE" -ForegroundColor Yellow
        } else {
            Write-Host "  ⏰ Mesma data de modificação" -ForegroundColor Cyan
        }
    }
    
    return @{
        Name = $FileInfo.Name
        Identical = $identical
        Size1 = $file1.Length
        Size2 = $file2.Length
        Date1 = $file1.LastWriteTime
        Date2 = $file2.LastWriteTime
        Hash1 = $hash1
        Hash2 = $hash2
    }
}

# Analisar JavaScript
Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    ARQUIVOS JAVASCRIPT                        ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green

$jsResults = @()
foreach ($file in $jsFiles) {
    $result = Analyze-FilePair -FileInfo $file
    if ($result) { $jsResults += $result }
}

# Analisar CSS
Write-Host "`n`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║                       ARQUIVOS CSS                            ║" -ForegroundColor Blue
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Blue

$cssResults = @()
foreach ($file in $cssFiles) {
    $result = Analyze-FilePair -FileInfo $file
    if ($result) { $cssResults += $result }
}

# Resumo final
Write-Host "`n`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║                      RESUMO DA ANÁLISE                        ║" -ForegroundColor Magenta
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta

Write-Host "`n  Total de pares analisados: $($identicos + $diferentes)"
Write-Host "  ✓ Arquivos IDÊNTICOS (seguro deletar da raiz): $identicos" -ForegroundColor Green
Write-Host "  ⚠ Arquivos DIFERENTES (requer análise manual): $diferentes" -ForegroundColor Yellow
Write-Host "  💾 Espaço liberado (se deletar idênticos): $([math]::Round($totalSize/1KB, 2)) KB`n"

# Arquivos com diferenças críticas
$criticos = ($jsResults + $cssResults) | Where-Object { -not $_.Identical }
if ($criticos.Count -gt 0) {
    Write-Host "`n  ⚠ ATENÇÃO: $($criticos.Count) arquivo(s) com DIFERENÇAS detectadas:" -ForegroundColor Red
    foreach ($file in $criticos) {
        Write-Host "     - $($file.Name)" -ForegroundColor Yellow
    }
    Write-Host "`n  👉 Estes arquivos precisam de revisão manual antes de qualquer ação!`n" -ForegroundColor Red
}

Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan
