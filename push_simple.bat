@echo off
echo 🚀 Push de l'application sur GitHub
echo ==================================

REM Vérifier si on est dans le bon répertoire
if not exist "main.py" (
    echo ❌ Erreur: main.py non trouvé. Êtes-vous dans le bon répertoire ?
    pause
    exit /b 1
)

REM Vérifier l'état Git
echo 📊 Vérification de l'état Git...
git status --porcelain

REM Ajouter tous les fichiers
echo 📁 Ajout des fichiers...
git add .

REM Commit si nécessaire
git diff --staged --quiet
if %errorlevel% neq 0 (
    echo 💾 Commit des changements...
    git commit -m "Update: Améliorations et corrections finales"
)

REM Vérifier les remotes
echo 🔗 Vérification des remotes...
git remote | findstr origin >nul
if %errorlevel% neq 0 (
    echo 📝 Aucun remote 'origin' trouvé.
    echo Pour ajouter un remote, exécutez :
    echo git remote add origin https://github.com/VOTRE_USERNAME/app-rh.git
    echo.
    echo Puis relancez ce script.
    pause
    exit /b 1
)

REM Afficher l'URL du remote
echo 🌐 Remote configuré :
git remote -v

REM Push vers GitHub
echo 🚀 Push vers GitHub...
git push -u origin main
if %errorlevel% equ 0 (
    echo ✅ Push réussi !
    echo 🎉 Application disponible sur GitHub
    echo 🌐 URL: 
    git remote get-url origin
) else (
    echo ❌ Erreur lors du push
    echo Vérifiez votre connexion et vos permissions GitHub
    pause
    exit /b 1
)

pause


