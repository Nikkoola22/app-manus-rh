@echo off
echo 🚀 Création de l'application RH portable
echo ========================================

REM Vérifier que nous sommes dans le bon répertoire
if not exist "main.py" (
    echo ❌ Erreur: Ce script doit être exécuté depuis le répertoire de l'application
    pause
    exit /b 1
)

echo 📋 Étapes de création:
echo 1. Configuration de l'environnement
echo 2. Tests de l'application
echo 3. Création du package portable
echo 4. Génération du ZIP de distribution
echo.

REM Étape 1: Configuration
echo 🔧 Étape 1: Configuration de l'environnement...
python setup_portable.py
if %errorlevel% neq 0 (
    echo ❌ Échec de la configuration
    pause
    exit /b 1
)

REM Étape 2: Tests
echo.
echo 🧪 Étape 2: Tests de l'application...
venv\Scripts\python test_portable.py
if %errorlevel% neq 0 (
    echo ⚠️  Certains tests ont échoué, mais continuation...
)

REM Étape 3: Build
echo.
echo 🔨 Étape 3: Création du package portable...
python build_portable.py
if %errorlevel% neq 0 (
    echo ❌ Échec de la création du package
    pause
    exit /b 1
)

echo.
echo 🎉 Application portable créée avec succès!
echo.
echo 📦 Fichiers générés:
echo    - Package ZIP: build\app-manus-rh-portable-*.zip
echo    - Dossier portable: build\app-manus-rh-portable\
echo.
echo 📝 Instructions de distribution:
echo    1. Partagez le fichier ZIP
echo    2. L'utilisateur extrait le ZIP
echo    3. L'utilisateur exécute: python install.py
echo    4. L'utilisateur lance: start.bat
echo.
echo 🌐 Pour tester localement:
echo    start.bat
echo.
pause

