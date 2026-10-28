# Instala FFmpeg, Node.js e Git (winget), o whisper.cpp com o modelo large-v3-turbo
# e as skills do HyperFrames (globais); no fim testa tudo e lista o que faltou.
# Uso (PowerShell):
#   powershell -ExecutionPolicy Bypass -File scripts\setup-windows-whisper.ps1
# Pode rodar de novo: o que ja estiver instalado e mantido.

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'   # Invoke-WebRequest fica muito mais rapido
$whisperDir = Join-Path $env:USERPROFILE 'whisper.cpp'
$modelPath  = Join-Path $whisperDir 'models\ggml-large-v3-turbo.bin'
$modelUrl   = 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin'
$sampleUrl  = 'https://raw.githubusercontent.com/ggml-org/whisper.cpp/master/samples/jfk.wav'
$failures   = New-Object System.Collections.Generic.List[string]

function Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }

function Refresh-Path {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' +
                [Environment]::GetEnvironmentVariable('Path', 'User')
}

function Ensure-Winget($id, $command) {
    if (Get-Command $command -ErrorAction SilentlyContinue) {
        Write-Host "  ok: $command ja instalado"
        return
    }
    Write-Host "  instalando $id ..."
    winget install --id $id --exact --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { $failures.Add("winget nao instalou $id (codigo $LASTEXITCODE)") }
    Refresh-Path
}

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    throw 'winget nao encontrado. Instale o "App Installer" pela Microsoft Store e rode de novo.'
}

Step '1/4  FFmpeg, Node.js e Git pelo winget'
Ensure-Winget 'Gyan.FFmpeg'       'ffmpeg'
Ensure-Winget 'OpenJS.NodeJS.LTS' 'node'
Ensure-Winget 'Git.Git'           'git'

Step '2/4  whisper.cpp (binario oficial para Windows x64)'
New-Item -ItemType Directory -Force -Path (Join-Path $whisperDir 'models') | Out-Null
$cli = Get-ChildItem $whisperDir -Recurse -Filter 'whisper-cli.exe' -ErrorAction SilentlyContinue | Select-Object -First 1
if ($cli) {
    Write-Host "  ok: whisper.cpp ja em $($cli.DirectoryName)"
} else {
    $release = Invoke-RestMethod 'https://api.github.com/repos/ggml-org/whisper.cpp/releases/latest' -Headers @{ 'User-Agent' = 'setup-script' }
    $asset = $release.assets | Where-Object { $_.name -eq 'whisper-bin-x64.zip' } | Select-Object -First 1
    if (-not $asset) {
        $failures.Add("a release $($release.tag_name) do whisper.cpp nao tem whisper-bin-x64.zip")
    } else {
        $zip = Join-Path $env:TEMP $asset.name
        Write-Host "  baixando $($asset.name) ($($release.tag_name)) ..."
        Invoke-WebRequest $asset.browser_download_url -OutFile $zip
        Expand-Archive $zip -DestinationPath $whisperDir -Force
        Remove-Item $zip
        $cli = Get-ChildItem $whisperDir -Recurse -Filter 'whisper-cli.exe' | Select-Object -First 1
    }
}

Step '3/4  Modelo large-v3-turbo (~1,6 GB, download unico)'
if ((Test-Path $modelPath) -and ((Get-Item $modelPath).Length -gt 1GB)) {
    Write-Host "  ok: modelo ja em $modelPath"
} else {
    Write-Host '  baixando, pode demorar alguns minutos ...'
    Invoke-WebRequest $modelUrl -OutFile $modelPath
}
if ($cli) {
    # Deixa o whisper-cli disponivel em qualquer terminal novo.
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    if ($userPath -notlike "*$($cli.DirectoryName)*") {
        [Environment]::SetEnvironmentVariable('Path', "$userPath;$($cli.DirectoryName)", 'User')
        Refresh-Path
    }
}

Step '4/4  Skills do HyperFrames (globais, so para o Claude Code)'
npx --yes skills add heygen-com/hyperframes --all -g -a claude-code
if ($LASTEXITCODE -ne 0) { $failures.Add('npx skills add heygen-com/hyperframes --all -g -a claude-code falhou') }

Step 'Teste'
foreach ($tool in 'ffmpeg', 'node', 'npx', 'git') {
    if (Get-Command $tool -ErrorAction SilentlyContinue) {
        $version = if ($tool -eq 'ffmpeg') { (& ffmpeg -version)[0] } else { & $tool --version }
        Write-Host "  ok: $tool  $version"
    } else {
        $failures.Add("$tool nao encontrado no PATH (feche e abra o terminal e rode de novo)")
    }
}
$nodeMajor = [int]((node --version) -replace '^v(\d+).*', '$1')
if ($nodeMajor -lt 22) { $failures.Add("Node $nodeMajor e antigo demais: o HyperFrames pede 22 ou mais novo") }

if ($cli -and (Test-Path $modelPath)) {
    $sample = Join-Path $env:TEMP 'jfk.wav'
    Invoke-WebRequest $sampleUrl -OutFile $sample
    Write-Host '  transcrevendo um audio de teste com o large-v3-turbo ...'
    $ErrorActionPreference = 'Continue'   # o whisper escreve o progresso no stderr
    $text = & $cli.FullName -m $modelPath -f $sample -l en -nt 2>$null | Out-String
    $ErrorActionPreference = 'Stop'
    if ($text -match 'ask not what your country') {
        Write-Host "  ok: whisper.cpp + large-v3-turbo transcreveram: $($text.Trim())"
    } else {
        $failures.Add('o whisper.cpp nao transcreveu o audio de teste corretamente')
    }
} else {
    $failures.Add('whisper.cpp ou o modelo large-v3-turbo nao ficaram instalados')
}

$skillsDir = Join-Path $env:USERPROFILE '.claude\skills'
$expected = 'hyperframes', 'hyperframes-cli', 'hyperframes-registry', 'media-use', 'figma', 'remotion-to-hyperframes', 'slideshow'
$missing = $expected | Where-Object { -not (Test-Path (Join-Path $skillsDir "$_\SKILL.md")) }
if ($missing) { $failures.Add("skills ausentes em ${skillsDir}: $($missing -join ', ')") }
else { Write-Host "  ok: 7 skills do HyperFrames em $skillsDir" }

npx --yes hyperframes doctor

Write-Host ''
if ($failures.Count -eq 0) {
    Write-Host 'Tudo instalado e testado. Feche e abra o Claude Code para carregar as skills.' -ForegroundColor Green
} else {
    Write-Host 'Ficou faltando:' -ForegroundColor Yellow
    $failures | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
    exit 1
}
