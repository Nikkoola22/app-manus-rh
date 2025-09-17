#!/bin/bash

# Script de démarrage avec configuration email
# Application RH - Système de Notifications Email

echo "🚀 Démarrage de l'Application RH avec Notifications Email"
echo "=================================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si npm est installé
if ! command -v npm &> /dev/null; then
    echo "❌ npm n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Aller dans le répertoire de l'application
cd "$(dirname "$0")"

echo "📁 Répertoire de travail : $(pwd)"

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "🔧 Création de l'environnement virtuel Python..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Installer les dépendances Node.js
echo "📦 Installation des dépendances Node.js..."
npm install

# Vérifier la configuration email
echo "📧 Vérification de la configuration email..."
if [ -f ".env" ]; then
    echo "✅ Fichier .env trouvé"
    echo "📋 Configuration email :"
    grep -E "MAIL_" .env | sed 's/=.*/=***/' || echo "   Aucune configuration email trouvée"
else
    echo "⚠️  Fichier .env non trouvé"
    echo "📝 Créez un fichier .env avec la configuration email :"
    echo "   MAIL_SERVER=smtp.gmail.com"
    echo "   MAIL_PORT=587"
    echo "   MAIL_USE_TLS=True"
    echo "   MAIL_USERNAME=votre.email@gmail.com"
    echo "   MAIL_PASSWORD=mot_de_passe_application"
    echo "   MAIL_DEFAULT_SENDER=noreply@votre-entreprise.com"
    echo ""
    echo "📖 Consultez email_config_example.txt pour plus de détails"
fi

# Créer le répertoire database s'il n'existe pas
mkdir -p database

# Démarrer le serveur Flask en arrière-plan
echo "🐍 Démarrage du serveur Flask (Backend)..."
python3 main.py &
FLASK_PID=$!

# Attendre que Flask démarre
echo "⏳ Attente du démarrage de Flask..."
sleep 3

# Vérifier que Flask fonctionne
if curl -s http://localhost:5001/api/agents > /dev/null 2>&1; then
    echo "✅ Serveur Flask démarré avec succès (PID: $FLASK_PID)"
else
    echo "❌ Erreur lors du démarrage de Flask"
    kill $FLASK_PID 2>/dev/null
    exit 1
fi

# Démarrer le serveur Vite en arrière-plan
echo "⚛️  Démarrage du serveur Vite (Frontend)..."
npm run dev &
VITE_PID=$!

# Attendre que Vite démarre
echo "⏳ Attente du démarrage de Vite..."
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
echo "=================================================="
echo "🌐 Application : http://localhost:5173"
echo "🔧 API Backend : http://localhost:5001"
echo "📧 Notifications : Configurées et actives"
echo ""
echo "🔑 Identifiants de test :"
echo "   Admin : admin@exemple.com / admin123"
echo "   Responsable : marie.dubois@exemple.com / resp123"
echo "   Agent : jean.martin@exemple.com / agent123"
echo ""
echo "📧 Test des notifications :"
echo "   python3 test_email_system.py"
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

