#!/bin/bash

# Script de démarrage simple sans gestion d'erreurs complexes
echo "🚀 Démarrage Simple de l'Application RH"

# Aller dans le répertoire
cd "/Users/nikkoolagarnier/Downloads/app manus rh"

# Activer l'environnement virtuel
source venv/bin/activate

# Démarrer Flask en arrière-plan
echo "🐍 Démarrage de Flask..."
python3 main.py &
FLASK_PID=$!

# Attendre 3 secondes
sleep 3

# Démarrer Vite en arrière-plan
echo "⚛️ Démarrage de Vite..."
npm run dev &
VITE_PID=$!

# Attendre 5 secondes
sleep 5

echo ""
echo "🎉 Application démarrée !"
echo "🌐 Interface : http://localhost:5173"
echo "🔧 API : http://localhost:5001"
echo ""
echo "🔑 Connexion :"
echo "   Admin : admin@exemple.com / admin123"
echo ""
echo "🛑 Pour arrêter : kill $FLASK_PID $VITE_PID"
echo ""

# Attendre indéfiniment
wait