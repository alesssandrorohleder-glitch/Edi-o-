# Prepara um PC Windows para editar videos com o Claude Code neste repositorio.
# Uso (PowerShell, dentro da pasta do repositorio):
#   powershell -ExecutionPolicy Bypass -File scripts\setup-windows.ps1
# Pode rodar de novo quando quiser: o que ja estiver instalado e mantido.

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot

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
    Refresh-Path
}

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    throw 'winget nao encontrado. Instale o "App Installer" pela Microsoft Store e rode de novo.'
}

Step 'Ferramentas do sistema (Git, Node.js, Python, FFmpeg, uv)'
Ensure-Winget 'Git.Git'             'git'
Ensure-Winget 'OpenJS.NodeJS.LTS'   'node'
Ensure-Winget 'Python.Python.3.12'  'python'
Ensure-Winget 'Gyan.FFmpeg'         'ffmpeg'
Ensure-Winget 'astral-sh.uv'        'uv'

Step 'Versoes'
node --version
python --version
(ffmpeg -version)[0]
uv --version

Step 'Pacotes do projeto (HyperFrames, Remotion, GSAP)'
Push-Location $repo
npm install --no-audit --no-fund

Step 'Transcricao local (faster-whisper)'
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Step 'Navegador do renderizador'
npx --yes hyperframes browser ensure

Step 'Modelo de transcricao (download unico, ~500 MB)'
python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8'); print('modelo pronto')"

Step 'Diagnostico do HyperFrames'
npx --yes hyperframes doctor
Pop-Location

Write-Host "`nTudo pronto. Abra o Claude Code nesta pasta e peca a edicao do seu video." -ForegroundColor Green
