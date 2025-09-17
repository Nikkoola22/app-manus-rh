# 🔧 Guide de Résolution des Erreurs - Application RH

## 🚨 Problèmes Identifiés

### **1. Erreur "zsh:1: command not found: dump_zsh_state"**
Cette erreur est liée à la configuration du shell zsh et n'affecte pas le fonctionnement de l'application.

### **2. Ports Occupés**
Parfois, les ports 5001 ou 5173 peuvent être occupés par d'autres processus.

### **3. Problèmes de Démarrage**
L'application peut ne pas démarrer correctement à cause de conflits de ports ou de processus.

## ✅ Solutions

### **Solution 1 : Nettoyage des Ports**

```bash
# Arrêter tous les processus sur les ports utilisés
lsof -ti:5001 | xargs kill -9
lsof -ti:5173 | xargs kill -9

# Vérifier que les ports sont libres
lsof -i:5001
lsof -i:5173
```

### **Solution 2 : Démarrage Manuel**

```bash
# Terminal 1 - Backend Flask
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
source venv/bin/activate
python3 main.py

# Terminal 2 - Frontend Vite
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
npm run dev
```

### **Solution 3 : Script de Démarrage Automatique**

```bash
# Utiliser le script de démarrage
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
./start_app.sh
```

### **Solution 4 : Diagnostic Complet**

```bash
# Exécuter le diagnostic
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
./diagnose_errors.sh
```

## 🔍 Vérifications

### **1. Vérifier que l'Application Fonctionne**

```bash
# Test de l'API Flask
curl http://localhost:5001/api/agents

# Test de l'interface Vite
curl http://localhost:5173
```

### **2. Vérifier les Logs**

```bash
# Vérifier les logs Flask
tail -f /tmp/flask.log

# Vérifier les logs Vite
npm run dev --verbose
```

### **3. Vérifier les Processus**

```bash
# Vérifier les processus Python
ps aux | grep python

# Vérifier les processus Node
ps aux | grep node
```

## 🛠️ Dépannage Avancé

### **Problème : Port 5001 Occupé**

```bash
# Trouver le processus qui utilise le port
lsof -i:5001

# Arrêter le processus
kill -9 $(lsof -ti:5001)

# Ou utiliser un port différent
PORT=5002 python3 main.py
```

### **Problème : Port 5173 Occupé**

```bash
# Trouver le processus qui utilise le port
lsof -i:5173

# Arrêter le processus
kill -9 $(lsof -ti:5173)

# Ou utiliser un port différent
npm run dev -- --port 5174
```

### **Problème : Base de Données Corrompue**

```bash
# Supprimer la base de données
rm -rf database/

# Recréer la base de données
mkdir database
python3 -c "from main import app, db; app.app_context().push(); db.create_all()"
```

### **Problème : Dépendances Manquantes**

```bash
# Réinstaller les dépendances Python
source venv/bin/activate
pip install -r requirements.txt

# Réinstaller les dépendances Node
npm install
```

## 📋 Checklist de Résolution

### **Étape 1 : Nettoyage**
- [ ] Arrêter tous les processus existants
- [ ] Vérifier que les ports sont libres
- [ ] Nettoyer les caches si nécessaire

### **Étape 2 : Vérification**
- [ ] Vérifier que Python 3 est installé
- [ ] Vérifier que l'environnement virtuel existe
- [ ] Vérifier que les dépendances sont installées
- [ ] Vérifier que la base de données existe

### **Étape 3 : Démarrage**
- [ ] Démarrer Flask sur le port 5001
- [ ] Démarrer Vite sur le port 5173
- [ ] Vérifier que les deux services répondent

### **Étape 4 : Test**
- [ ] Tester l'API : `curl http://localhost:5001/api/agents`
- [ ] Tester l'interface : `curl http://localhost:5173`
- [ ] Se connecter avec les identifiants de test

## 🚀 Commandes de Démarrage Rapide

### **Option 1 : Script Automatique**
```bash
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
./start_app.sh
```

### **Option 2 : Manuel (2 Terminaux)**
```bash
# Terminal 1
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
source venv/bin/activate
python3 main.py

# Terminal 2
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
npm run dev
```

### **Option 3 : Ports Alternatifs**
```bash
# Terminal 1 - Flask sur port 5002
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
source venv/bin/activate
PORT=5002 python3 main.py

# Terminal 2 - Vite sur port 5174
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
npm run dev -- --port 5174
```

## 🔑 Identifiants de Test

Une fois l'application démarrée :

- **Admin** : `admin@exemple.com` / `admin123`
- **Responsable** : `marie.dubois@exemple.com` / `resp123`
- **Agent** : `jean.martin@exemple.com` / `agent123`

## 📞 Support

Si les problèmes persistent :

1. **Exécuter le diagnostic** : `./diagnose_errors.sh`
2. **Vérifier les logs** : Regarder les messages d'erreur dans les terminaux
3. **Redémarrer complètement** : Fermer tous les terminaux et redémarrer
4. **Vérifier les permissions** : S'assurer que les scripts sont exécutables

## ✅ Résolution des Erreurs Courantes

### **"Address already in use"**
- Solution : Arrêter le processus qui utilise le port
- Commande : `lsof -ti:5001 | xargs kill -9`

### **"Module not found"**
- Solution : Réinstaller les dépendances
- Commande : `pip install -r requirements.txt`

### **"Permission denied"**
- Solution : Rendre les scripts exécutables
- Commande : `chmod +x *.sh`

### **"Database locked"**
- Solution : Arrêter l'application et redémarrer
- Commande : `killall python3` puis redémarrer

L'application devrait maintenant fonctionner correctement ! 🎉

