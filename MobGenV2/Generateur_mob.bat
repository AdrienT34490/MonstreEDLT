@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0"

echo [CONSOLE] : Détection dynamique de Python...

set "PYTHON_EXE="

:: Cherche python.exe ou py.exe hors WindowsApps
for %%P in (python.exe py.exe) do (
    for /F "delims=" %%I in ('where %%P 2^>nul') do (
        echo [CONSOLE] : Test de %%I
        call :test_python "%%I"
        if defined PYTHON_EXE goto python_found
    )
)

echo [CONSOLE] : Aucun Python valide trouvé (hors WindowsApps)
pause
exit /b 1

:python_found
echo [CONSOLE] : Python trouvé : %PYTHON_EXE%

:: Création du venv si besoin
if not exist "%~dp0venv\Scripts\activate.bat" (
    echo [CONSOLE] : Création du venv...
    "%PYTHON_EXE%" -m venv venv
    if errorlevel 1 (
        echo [CONSOLE] : Impossible de créer le venv
        pause
        exit /b 1
    )
) else (
    echo [CONSOLE] : venv déjà existant, activation...
)

:: activate venv
call "%~dp0venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [CONSOLE] : Impossible d'activer le venv
    pause
    exit /b 1
)

:: Vérification si le package est installé
python -c "import pkg_resources; pkg_resources.get_distribution('MonstreEDLT')" 2>nul
if errorlevel 1 (
    echo [CONSOLE] : Installation du package MonstreEDLT depuis GitHub...
    pip install git+https://github.com/AdrienT34490/MonstreEDLT.git
) else (
    echo [CONSOLE] : Package MonstreEDLT déjà installé.
)

:: Lancement de MobGenEDLT.exe
echo [CONSOLE] : Lancement de MobGenEDLT.exe...
if exist "%~dp0venv\Scripts\MobGenEDLT.exe" (
    "%~dp0venv\Scripts\MobGenEDLT.exe"
) else (
    echo [CONSOLE] : ERREUR : MobGenEDLT.exe introuvable dans le venv
)

echo [CONSOLE] : Script terminé.
pause
exit /b 0

:test_python
set "CANDIDATE=%~1"
echo %CANDIDATE% | findstr /i WindowsApps >nul
if errorlevel 1 set "PYTHON_EXE=%CANDIDATE%"
exit /b
