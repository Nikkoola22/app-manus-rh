#!/bin/bash

echo "🚀 Création de l'application RH portable"
echo "========================================"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "main.py" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis le répertoire de l'application"
    exit 1
fi

echo "📋 Étapes de création:"
echo "1. Configuration de l'environnement"
echo "2. Tests de l'application"
echo "3. Création du package portable"
echo "4. Génération du ZIP de distribution"
echo ""

# Étape 1: Configuration
echo "🔧 Étape 1: Configuration de l'environnement..."
python3 setup_portable.py
if [ $? -ne 0 ]; then
    echo "❌ Échec de la configuration"
    exit 1
fi

# Étape 2: Tests
echo ""
echo "🧪 Étape 2: Tests de l'application..."
./venv/bin/python test_portable.py
if [ $? -ne 0 ]; then
    echo "⚠️  Certains tests ont échoué, mais continuation..."
fi

# Étape 3: Build
echo ""
echo "🔨 Étape 3: Création du package portable..."
python3 build_portable.py
if [ $? -ne 0 ]; then
    echo "❌ Échec de la création du package"
    exit 1
fi

echo ""
echo "🎉 Application portable créée avec succès!"
echo ""
echo "📦 Fichiers générés:"
echo "   - Package ZIP: build/app-manus-rh-portable-*.zip"
echo "   - Dossier portable: build/app-manus-rh-portable/"
echo ""
echo "📝 Instructions de distribution:"
echo "   1. Partagez le fichier ZIP"
echo "   2. L'utilisateur extrait le ZIP"
echo "   3. L'utilisateur exécute: python3 install.py"
echo "   4. L'utilisateur lance: ./start.sh (ou start.bat sur Windows)"
echo ""
echo "🌐 Pour tester localement:"
echo "   ./start.sh"
echo ""
