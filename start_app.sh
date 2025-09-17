#!/bin/bash

# Script de démarrage simple pour l'application RH
echo "🚀 Démarrage de l'Application RH"

# Aller dans le répertoire de l'application
cd "/Users/nikkoolagarnier/Downloads/app manus rh"

# Activer l'environnement virtuel
source venv/bin/activate

# Tuer les processus existants
echo "🔄 Arrêt des processus existants..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

# Attendre un peu
sleep 2

# Démarrer Flask
echo "🐍 Démarrage du serveur Flask..."
python3 main.py &
FLASK_PID=$!

# Attendre que Flask démarre
sleep 3

# Vérifier que Flask fonctionne
if curl -s http://localhost:5001/api/agents > /dev/null 2>&1; then
    echo "✅ Serveur Flask démarré avec succès (PID: $FLASK_PID)"
else
    echo "❌ Erreur lors du démarrage de Flask"
    kill $FLASK_PID 2>/dev/null
    exit 1
fi

# Démarrer Vite
echo "⚛️ Démarrage du serveur Vite..."
npm run dev &
VITE_PID=$!

# Attendre que Vite démarre
sleep 5

# Vérifier que Vite fonctionne
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "✅ Serveur Vite démarré avec succès (PID: $VITE_PID)"
else
    echo "❌ Erreur lors du démarrage de Vite"
    kill $FLASK_PID $VITE_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Application RH démarrée avec succès !"
echo "🌐 Application : http://localhost:5173"
echo "🔧 API Backend : http://localhost:5001"
echo ""
echo "🔑 Identifiants de test :"
echo "   Admin : admin@exemple.com / admin123"
echo "   Responsable : marie.dubois@exemple.com / resp123"
echo "   Agent : jean.martin@exemple.com / agent123"
echo ""
echo "🛑 Pour arrêter l'application :"
echo "   kill $FLASK_PID $VITE_PID"
echo "   ou Ctrl+C dans ce terminal"
echo ""

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🛑 Arrêt de l'application..."
    kill $FLASK_PID $VITE_PID 2>/dev/null
    echo "✅ Application arrêtée"
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Attendre indéfiniment
echo "📱 L'application est en cours d'exécution..."
echo "   Appuyez sur Ctrl+C pour arrêter"
wait

