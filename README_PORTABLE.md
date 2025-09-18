# Application RH - Version Portable

## 🚀 Démarrage Rapide

### Option 1: Déploiement automatique (Recommandé)
```bash
python3 deploy_portable.py
```

### Option 2: Configuration manuelle
```bash
# 1. Configuration
python3 setup_portable.py

# 2. Tests (optionnel)
python3 test_portable.py

# 3. Lancement
python3 launcher.py
```

### Option 3: Scripts de lancement
- **Windows**: Double-cliquez sur `start.bat`
- **macOS/Linux**: Exécutez `./start.sh`

## 📋 Prérequis

- **Python 3.8+** (https://python.org)
- **Node.js 16+** (https://nodejs.org)

## 🔧 Configuration

Le script `setup_portable.py` configure automatiquement :
- ✅ Environnement virtuel Python
- ✅ Installation des dépendances Python
- ✅ Installation des dépendances Node.js
- ✅ Création de la base de données SQLite
- ✅ Initialisation des données de test
- ✅ Création des scripts de lancement

## 🧪 Tests

Le script `test_portable.py` vérifie :
- ✅ Environnement Python
- ✅ Dépendances installées
- ✅ Base de données
- ✅ Démarrage des serveurs
- ✅ Fonctionnement de l'API

## 🌐 Accès à l'application

Une fois lancée, l'application est accessible à :
- **Interface utilisateur**: http://localhost:5173
- **API Backend**: http://localhost:5001

## 🔑 Comptes de test

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Admin | admin@exemple.com | admin123 |
| Responsable | jean.martin@exemple.com | resp123 |
| Agent | sofiane.bendaoud@exemple.com | agent123 |
| Agent | marie.dupont@exemple.com | agent123 |
| Agent | pierre.leroy@exemple.com | agent123 |

## 📦 Création d'un package portable

Pour créer un package ZIP portable :

```bash
python3 build_portable.py
```

Cela génère un fichier `app-manus-rh-portable-YYYYMMDD_HHMMSS.zip` dans le dossier `build/`.

## 🗂️ Structure du projet

```
app-manus-rh/
├── setup_portable.py      # Configuration automatique
├── deploy_portable.py     # Déploiement rapide
├── test_portable.py       # Tests de l'application
├── build_portable.py      # Création du package portable
├── init_portable_data.py  # Initialisation des données
├── launcher.py            # Lanceur de l'application
├── main.py                # Application principale
├── start.bat              # Script Windows
├── start.sh               # Script Unix
├── requirements.txt       # Dépendances Python
├── package.json           # Dépendances Node.js
├── database/              # Base de données SQLite
├── static/                # Fichiers statiques
└── src/                   # Code source
```

## 🛠️ Dépannage

### Problème de Python
```bash
# Vérifier la version
python3 --version

# Si Python n'est pas trouvé, installer depuis python.org
```

### Problème de Node.js
```bash
# Vérifier la version
node --version

# Si Node.js n'est pas trouvé, installer depuis nodejs.org
```

### Problème de ports
Si les ports 5001 ou 5173 sont occupés :
1. Arrêter les autres applications utilisant ces ports
2. Ou modifier les ports dans `main.py` et `vite.config.js`

### Problème de permissions (macOS/Linux)
```bash
# Rendre les scripts exécutables
chmod +x start.sh
chmod +x launcher.py
```

### Réinitialisation complète
```bash
# Supprimer l'environnement virtuel et la base de données
rm -rf venv/
rm -rf database/
rm -rf node_modules/

# Reconfigurer
python3 setup_portable.py
```

## 📱 Fonctionnalités

- ✅ **Gestion des agents** : Création, modification, suppression
- ✅ **Gestion des services** : Organisation par services
- ✅ **Demandes de congés** : Workflow complet d'approbation
- ✅ **Gestion RTT** : Calcul automatique des RTT
- ✅ **Arrêts maladie** : Suivi et gestion
- ✅ **Gestion de présence** : Calendrier et suivi
- ✅ **Notifications email** : Alertes automatiques
- ✅ **Interface moderne** : Design responsive et intuitif
- ✅ **Base de données portable** : SQLite intégré

## 🔒 Sécurité

- Authentification par email/mot de passe
- Sessions sécurisées
- Rôles utilisateurs (Admin, Responsable, Agent)
- Validation des données côté serveur
- Protection CORS configurée

## 📊 Base de données

L'application utilise SQLite pour la portabilité :
- Fichier : `database/app.db`
- Tables créées automatiquement
- Données d'exemple incluses
- Sauvegarde simple (copier le fichier .db)

## 🌍 Compatibilité

- ✅ **Windows** 10/11
- ✅ **macOS** 10.15+
- ✅ **Linux** (Ubuntu, Debian, CentOS, etc.)

## 📞 Support

Pour toute question ou problème :
1. Consultez les guides dans le dossier
2. Vérifiez les logs d'erreur
3. Exécutez `python3 test_portable.py` pour diagnostiquer

## 🔄 Mise à jour

Pour mettre à jour l'application :
1. Sauvegardez `database/app.db`
2. Téléchargez la nouvelle version
3. Restaurez `database/app.db`
4. Exécutez `python3 setup_portable.py`

---

**Version portable générée le** : $(date)
**Compatible avec** : Python 3.8+, Node.js 16+


