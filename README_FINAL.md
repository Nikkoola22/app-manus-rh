# 🚀 Application RH - Version Portable

## 📋 Vue d'ensemble

Cette application de gestion des ressources humaines est maintenant **100% portable** et peut être déployée sur n'importe quel système (Windows, macOS, Linux) sans configuration complexe.

## 🎯 Fonctionnalités

- ✅ **Gestion des agents** : Création, modification, suppression
- ✅ **Gestion des services** : Organisation par services
- ✅ **Demandes de congés** : Workflow complet d'approbation
- ✅ **Gestion RTT** : Calcul automatique des RTT
- ✅ **Arrêts maladie** : Suivi et gestion
- ✅ **Gestion de présence** : Calendrier et suivi
- ✅ **Notifications email** : Alertes automatiques
- ✅ **Interface moderne** : Design responsive et intuitif
- ✅ **Base de données portable** : SQLite intégré

## 🚀 Démarrage Ultra-Rapide

### Option 1: Déploiement automatique (Recommandé)
```bash
python3 deploy_portable.py
```

### Option 2: Configuration manuelle
```bash
# 1. Configuration
python3 setup_portable.py

# 2. Lancement
python3 launcher.py
```

### Option 3: Scripts de lancement
- **Windows**: Double-cliquez sur `start.bat`
- **macOS/Linux**: Exécutez `./start.sh`

## 📦 Création d'un package portable

Pour créer un package ZIP portable à distribuer :

### Sur macOS/Linux
```bash
./MAKE_PORTABLE.sh
```

### Sur Windows
```cmd
MAKE_PORTABLE.bat
```

### Manuellement
```bash
python3 build_portable.py
```

## 🔧 Prérequis

- **Python 3.8+** (https://python.org)
- **Node.js 16+** (https://nodejs.org)

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

## 📁 Structure du projet

```
app-manus-rh/
├── 🚀 DÉMARRAGE RAPIDE
├── setup_portable.py      # Configuration automatique
├── deploy_portable.py     # Déploiement rapide
├── launcher.py            # Lanceur de l'application
├── start.bat              # Script Windows
├── start.sh               # Script Unix
├── MAKE_PORTABLE.sh       # Création package (Unix)
├── MAKE_PORTABLE.bat      # Création package (Windows)
│
├── 🧪 TESTS
├── test_portable.py       # Tests de l'application
│
├── 🔨 BUILD
├── build_portable.py      # Création du package portable
├── init_portable_data.py  # Initialisation des données
│
├── 📱 APPLICATION
├── main.py                # Application principale
├── requirements.txt       # Dépendances Python
├── package.json           # Dépendances Node.js
├── database/              # Base de données SQLite
├── static/                # Fichiers statiques
└── src/                   # Code source
```

## 🛠️ Scripts disponibles

### Configuration et déploiement
- `setup_portable.py` : Configuration automatique de l'environnement
- `deploy_portable.py` : Déploiement rapide avec options
- `launcher.py` : Lanceur de l'application

### Tests
- `test_portable.py` : Tests complets de l'application

### Build et distribution
- `build_portable.py` : Création du package portable
- `MAKE_PORTABLE.sh` : Script complet de création (Unix)
- `MAKE_PORTABLE.bat` : Script complet de création (Windows)

## 🔄 Workflow de déploiement

### 1. Développement local
```bash
# Configuration initiale
python3 setup_portable.py

# Test
python3 test_portable.py

# Lancement
python3 launcher.py
```

### 2. Création du package
```bash
# Création automatique
./MAKE_PORTABLE.sh

# Ou manuellement
python3 build_portable.py
```

### 3. Distribution
1. Partagez le fichier ZIP généré
2. L'utilisateur extrait le ZIP
3. L'utilisateur exécute `python3 install.py`
4. L'utilisateur lance `./start.sh` (ou `start.bat`)

## 🧪 Tests et validation

Le script `test_portable.py` vérifie :
- ✅ Environnement Python
- ✅ Dépendances installées
- ✅ Base de données
- ✅ Démarrage des serveurs
- ✅ Fonctionnement de l'API

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

## 🚨 Dépannage

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
chmod +x MAKE_PORTABLE.sh
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

## 🎉 Résumé

Votre application RH est maintenant **100% portable** ! 

**Pour démarrer rapidement :**
```bash
python3 deploy_portable.py
```

**Pour créer un package de distribution :**
```bash
./MAKE_PORTABLE.sh
```

**Pour tester :**
```bash
python3 test_portable.py
```

L'application fonctionne sur Windows, macOS et Linux sans configuration supplémentaire. Tous les chemins sont relatifs, la base de données est portable, et l'installation est entièrement automatisée.

---

**Version portable générée le** : $(date)  
**Compatible avec** : Python 3.8+, Node.js 16+  
**Base de données** : SQLite (portable)

