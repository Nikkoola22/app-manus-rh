# 🏢 Application de Gestion RH

Une application web complète de gestion des ressources humaines avec système de congés, plannings et notifications email.

## ✨ Fonctionnalités

### 👥 Gestion des utilisateurs
- **3 rôles** : Agent, Responsable, Admin
- **Authentification** sécurisée
- **Profils** personnalisés avec soldes de congés

### 📅 Gestion des congés
- **Types de congés** : CA (jours), RTT/HS (heures)
- **Demandes** avec validation par les responsables
- **Calcul automatique** basé sur les plannings
- **Historique** complet des demandes

### 📊 Planning des agents
- **Planning hebdomadaire** du lundi au samedi
- **Créneaux de 30 minutes** de 8h00 à 19h00
- **Modification** par les responsables
- **Visualisation** par les agents

### 📧 Notifications email
- **Notifications** de nouvelles demandes
- **Confirmations** de validation/refus
- **Configuration Gmail** intégrée

### 🎨 Interface moderne
- **Design responsive** avec Tailwind CSS
- **Onglets interactifs** avec scroll automatique
- **Animations fluides** et UX optimisée

## 🚀 Installation

### Prérequis
- Python 3.8+
- Node.js 16+
- Git

### Installation rapide
```bash
# Cloner le dépôt
git clone https://github.com/Nikkoola22/app-rh.git
cd app-rh

# Configuration automatique
python3 setup_portable.py

# Démarrage
python3 start_app.py
```

### Installation manuelle
```bash
# Backend Python
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Frontend Node.js
npm install
npm run build

# Base de données
python3 init_portable_data.py

# Configuration email (optionnel)
python3 setup_email.py
# Modifier le fichier .env avec vos paramètres Gmail
```

## 🔧 Configuration

### Variables d'environnement
Créer un fichier `.env` :
```env
MAIL_USERNAME=votre-email@gmail.com
MAIL_PASSWORD=votre-mot-de-passe-app
MAIL_DEFAULT_SENDER=votre-email@gmail.com
```

### Configuration Gmail
1. Activer l'authentification à 2 facteurs
2. Générer un mot de passe d'application
3. Configurer les variables d'environnement

## 📱 Utilisation

### Accès à l'application
- **URL** : http://localhost:5001
- **Port** : 5001 (Flask) + 5173 (Vite)

### Comptes par défaut
- **Admin** : admin@exemple.com / admin123
- **Responsable** : jean.martin@exemple.com / resp123
- **Agent** : sofiane.bendaoud@exemple.com / agent123

### Workflow principal
1. **Agent** : Créer une demande de congé
2. **Responsable** : Valider/refuser la demande
3. **Système** : Envoyer email de notification
4. **Agent** : Consulter l'historique et le planning

## 🏗️ Architecture

### Backend (Flask)
- **API REST** avec authentification
- **Base de données** SQLite portable
- **Services** : Email, calculs, validation
- **Modèles** : Agent, DemandeConge, Planning

### Frontend (React + Vite)
- **Composants** modulaires avec Tailwind CSS
- **Routage** conditionnel par rôle
- **État** géré avec React hooks
- **API** intégrée avec fetch

### Base de données
- **SQLite** pour la portabilité
- **Migrations** automatiques
- **Données** d'exemple incluses

## 📁 Structure du projet

```
app-rh/
├── src/                    # Code source
│   ├── components/         # Composants React
│   ├── models/            # Modèles de données
│   ├── routes/            # Routes API Flask
│   └── services/          # Services (email, etc.)
├── static/                # Fichiers statiques
├── database/              # Base de données SQLite
├── dist/                  # Build frontend
├── venv/                  # Environnement Python
├── node_modules/          # Dépendances Node.js
├── main.py               # Point d'entrée Flask
├── requirements.txt       # Dépendances Python
├── package.json          # Dépendances Node.js
└── README.md             # Documentation
```

## 🧪 Tests

### Tests automatisés
```bash
# Test de l'application
python3 test_portable.py

# Test des onglets
python3 test_onglets_final.py

# Test de l'email
python3 test_email_config.py
```

### Tests manuels
1. **Interface** : Navigation et fonctionnalités
2. **Rôles** : Permissions et accès
3. **Email** : Envoi et réception
4. **Planning** : Création et modification

## 🚀 Déploiement

### Version portable
```bash
# Créer un package portable
python3 build_portable.py

# Déployer
python3 deploy_portable.py
```

### Production
1. **Serveur** : Configurer un serveur web
2. **Base de données** : Migrer vers PostgreSQL/MySQL
3. **Email** : Configurer SMTP de production
4. **SSL** : Ajouter certificat HTTPS

## 📚 Documentation

- **Guides** : Voir les fichiers GUIDE_*.md
- **Corrections** : Voir les fichiers CORRECTION_*.md
- **Fonctionnalités** : Voir les fichiers FONCTIONNALITE_*.md

## 🤝 Contribution

1. **Fork** le projet
2. **Créer** une branche feature
3. **Commit** vos changements
4. **Push** vers la branche
5. **Ouvrir** une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 👨‍💻 Auteur

**Nikkoola22** - [GitHub](https://github.com/Nikkoola22)

## 🙏 Remerciements

- **Flask** pour le backend Python
- **React** pour le frontend
- **Tailwind CSS** pour le design
- **SQLite** pour la base de données
- **Gmail** pour les notifications email

---

**🎉 Application de gestion RH complète et moderne !**