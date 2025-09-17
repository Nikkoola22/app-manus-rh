#!/bin/bash

echo "🚀 Démarrage de l'application RH"
echo "================================="

# Aller dans le répertoire du projet
cd "/Users/nikkoolagarnier/Downloads/app manus rh"

echo "📁 Répertoire: $(pwd)"

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Création..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances Python si nécessaire
echo "📦 Vérification des dépendances Python..."
pip install -q flask flask-sqlalchemy flask-cors werkzeug requests

# Installer les dépendances Node.js si nécessaire
echo "📦 Vérification des dépendances Node.js..."
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances Node.js..."
    npm install
fi

echo ""
echo "🌐 Démarrage des serveurs..."
echo ""

# Démarrer Flask en arrière-plan
echo "🐍 Démarrage du serveur Flask (port 5001)..."
python main.py &
FLASK_PID=$!

# Attendre que Flask démarre
sleep 3

# Démarrer Vite en arrière-plan
echo "⚡ Démarrage du serveur Vite (port 5173)..."
npm run dev &
VITE_PID=$!

# Attendre que Vite démarre
sleep 3

echo ""
echo "✅ Serveurs démarrés avec succès!"
echo ""
echo "🌐 URLs d'accès:"
echo "   Application: http://localhost:5173"
echo "   API Backend: http://localhost:5001"
echo ""
echo "🔑 Identifiants de test:"
echo "   Admin: admin@exemple.com / admin123"
echo "   Responsable: jean.martin@exemple.com / resp123"
echo "   Agent: sofiane.bendaoud@exemple.com / agent123"
echo ""
echo "📝 Pour arrêter les serveurs:"
echo "   kill $FLASK_PID $VITE_PID"
echo ""

# Ouvrir l'application dans le navigateur
echo "🌐 Ouverture de l'application..."
open http://localhost:5173

echo "🎉 Application prête!"
echo "   Les serveurs continuent de tourner en arrière-plan."
echo "   Fermez ce terminal pour les arrêter."
