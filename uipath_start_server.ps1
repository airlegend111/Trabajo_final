# Script para iniciar el servidor Django para UiPath
param(
    [string]$ConfigPath = "uipath_config.json",
    [switch]$WaitForServer = $true
)

function Test-ServerConnection {
    param([string]$Url)
    try {
        $response = Invoke-WebRequest -Uri $Url -Method Head -UseBasicParsing
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

# Activar el entorno virtual
if (Test-Path "venv") {
    Write-Host "Activando entorno virtual..."
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Creando nuevo entorno virtual..."
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
}

# Leer la configuración
$config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$baseUrl = $config.application.baseUrl

# Iniciar el servidor Django
Write-Host "Iniciando servidor Django..."
Start-Process python -ArgumentList "manage.py", "runserver" -NoNewWindow

if ($WaitForServer) {
    Write-Host "Esperando que el servidor esté listo..."
    $attempts = 0
    $maxAttempts = 10
    
    while ($attempts -lt $maxAttempts) {
        if (Test-ServerConnection -Url $baseUrl) {
            Write-Host "¡Servidor listo! Accesible en $baseUrl"
            break
        }
        $attempts++
        Start-Sleep -Seconds 2
    }
    
    if ($attempts -eq $maxAttempts) {
        Write-Error "El servidor no respondió después de $($maxAttempts * 2) segundos"
        exit 1
    }
}
