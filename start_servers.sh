#!/bin/bash

echo "Démarrage des serveurs..."

# Démarrer Flask en arrière-plan
echo "Démarrage du serveur Flask (port 5001)..."
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
source venv/bin/activate
python main.py &
FLASK_PID=$!

# Attendre que Flask démarre
sleep 3

# Démarrer Vite en arrière-plan
echo "Démarrage du serveur Vite (port 5173)..."
npm run dev &
VITE_PID=$!

echo "Serveurs démarrés:"
echo "- Flask (Backend): http://localhost:5001 (PID: $FLASK_PID)"
echo "- Vite (Frontend): http://localhost:5173 (PID: $VITE_PID)"
echo ""
echo "Pour arrêter les serveurs, utilisez: kill $FLASK_PID $VITE_PID"
echo ""
echo "Test de connexion: http://localhost:5173/test_connection.html"

# Attendre que les processus se terminent
wait




