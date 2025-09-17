#!/bin/bash

echo "🚀 Push de l'application sur GitHub"
echo "=================================="

# Vérifier si on est dans le bon répertoire
if [ ! -f "main.py" ]; then
    echo "❌ Erreur: main.py non trouvé. Êtes-vous dans le bon répertoire ?"
    exit 1
fi

# Vérifier l'état Git
echo "📊 Vérification de l'état Git..."
git status --porcelain

# Ajouter tous les fichiers
echo "📁 Ajout des fichiers..."
git add .

# Commit si nécessaire
if ! git diff --staged --quiet; then
    echo "💾 Commit des changements..."
    git commit -m "Update: Améliorations et corrections finales"
fi

# Vérifier les remotes
echo "🔗 Vérification des remotes..."
if ! git remote | grep -q origin; then
    echo "📝 Aucun remote 'origin' trouvé."
    echo "Pour ajouter un remote, exécutez :"
    echo "git remote add origin https://github.com/VOTRE_USERNAME/app-rh.git"
    echo ""
    echo "Puis relancez ce script."
    exit 1
fi

# Afficher l'URL du remote
echo "🌐 Remote configuré :"
git remote -v

# Push vers GitHub
echo "🚀 Push vers GitHub..."
if git push -u origin main; then
    echo "✅ Push réussi !"
    echo "🎉 Application disponible sur GitHub"
    echo "🌐 URL: $(git remote get-url origin)"
else
    echo "❌ Erreur lors du push"
    echo "Vérifiez votre connexion et vos permissions GitHub"
    exit 1
fi
