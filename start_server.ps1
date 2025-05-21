# Activar el entorno virtual si existe, si no, crear uno nuevo
if (Test-Path "venv") {
    .\venv\Scripts\Activate.ps1
} else {
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
}

# Iniciar el servidor Django
python manage.py runserver
