#!/bin/bash

# Script de diagnostic pour l'application RH
echo "🔍 Diagnostic de l'Application RH"
echo "================================="

# Aller dans le répertoire de l'application
cd "/Users/nikkoolagarnier/Downloads/app manus rh"

echo ""
echo "1. 📁 Vérification du répertoire de travail :"
echo "   $(pwd)"

echo ""
echo "2. 🐍 Vérification de Python :"
if command -v python3 &> /dev/null; then
    echo "   ✅ Python3 installé : $(python3 --version)"
else
    echo "   ❌ Python3 non trouvé"
fi

echo ""
echo "3. 📦 Vérification de l'environnement virtuel :"
if [ -d "venv" ]; then
    echo "   ✅ Environnement virtuel trouvé"
    if [ -f "venv/bin/activate" ]; then
        echo "   ✅ Script d'activation trouvé"
    else
        echo "   ❌ Script d'activation manquant"
    fi
else
    echo "   ❌ Environnement virtuel non trouvé"
fi

echo ""
echo "4. 🔧 Vérification des dépendances Python :"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "   ✅ Environnement virtuel activé"
    
    echo "   📋 Dépendances installées :"
    pip list | grep -E "(Flask|Flask-Mail|Flask-SQLAlchemy|Flask-CORS)" | while read line; do
        echo "      $line"
    done
else
    echo "   ❌ Impossible d'activer l'environnement virtuel"
fi

echo ""
echo "5. 📄 Vérification des fichiers principaux :"
files=("main.py" "src/App.jsx" "package.json" "requirements.txt")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file manquant"
    fi
done

echo ""
echo "6. 🌐 Vérification des ports :"
echo "   Port 5001 (Flask) :"
if lsof -i:5001 &> /dev/null; then
    echo "      ❌ Port 5001 occupé par : $(lsof -ti:5001 | xargs ps -p 2>/dev/null | tail -n +2 | awk '{print $4}' | head -1)"
else
    echo "      ✅ Port 5001 libre"
fi

echo "   Port 5173 (Vite) :"
if lsof -i:5173 &> /dev/null; then
    echo "      ❌ Port 5173 occupé par : $(lsof -ti:5173 | xargs ps -p 2>/dev/null | tail -n +2 | awk '{print $4}' | head -1)"
else
    echo "      ✅ Port 5173 libre"
fi

echo ""
echo "7. 🔍 Vérification des erreurs de syntaxe :"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "   Python (main.py) :"
    if python3 -m py_compile main.py 2>/dev/null; then
        echo "      ✅ Syntaxe Python correcte"
    else
        echo "      ❌ Erreur de syntaxe Python"
        python3 -m py_compile main.py
    fi
fi

echo ""
echo "8. 📊 Vérification de la base de données :"
if [ -d "database" ]; then
    echo "   ✅ Répertoire database trouvé"
    if [ -f "database/app.db" ]; then
        echo "   ✅ Base de données trouvée"
        echo "   📏 Taille : $(du -h database/app.db | cut -f1)"
    else
        echo "   ❌ Base de données manquante"
    fi
else
    echo "   ❌ Répertoire database manquant"
fi

echo ""
echo "9. 🚀 Test de démarrage Flask :"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "   Test de démarrage Flask (5 secondes) :"
    timeout 5s python3 main.py &
    FLASK_PID=$!
    sleep 2
    if curl -s http://localhost:5001/api/agents > /dev/null 2>&1; then
        echo "      ✅ Flask démarre correctement"
    else
        echo "      ❌ Flask ne démarre pas ou ne répond pas"
    fi
    kill $FLASK_PID 2>/dev/null
    sleep 1
fi

echo ""
echo "10. 📋 Recommandations :"
echo "   - Si des ports sont occupés : lsof -ti:PORT | xargs kill -9"
echo "   - Si l'environnement virtuel est manquant : python3 -m venv venv"
echo "   - Si les dépendances manquent : pip install -r requirements.txt"
echo "   - Si la base de données manque : l'application la créera automatiquement"

echo ""
echo "🔍 Diagnostic terminé"

