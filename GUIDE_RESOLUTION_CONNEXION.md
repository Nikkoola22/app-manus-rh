# 🔧 Guide de Résolution des Problèmes de Connexion

## ❌ Problème Identifié

Les erreurs récurrentes `cursor_snap_ENV_VARS` et `dump_zsh_state` proviennent de la configuration du terminal et empêchent le démarrage correct des serveurs.

## ✅ Solutions Disponibles

### 🚀 **Solution 1 : Script Python Direct (Recommandé)**

```bash
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
python3 start_app_direct.py
```

**Avantages :**
- Évite complètement les problèmes de terminal
- Démarre automatiquement les deux serveurs
- Ouvre l'application dans le navigateur
- Gestion propre de l'arrêt (Ctrl+C)

### 🚀 **Solution 2 : Démarrage Manuel (Si nécessaire)**

**Terminal 1 - Backend Flask:**
```bash
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend Vite:**
```bash
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
npm run dev
```

### 🚀 **Solution 3 : Script de Diagnostic**

```bash
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
python3 test_server.py
```

## 🔍 Diagnostic des Problèmes

### **Vérifier l'état des serveurs :**
```bash
# Vérifier les processus
ps aux | grep -E "(python|node)" | grep -v grep

# Vérifier les ports
lsof -i :5001 -i :5173
```

### **Tester la connexion :**
```bash
# Test Flask
curl http://localhost:5001/api/auth/check-session

# Test Vite
curl http://localhost:5173/
```

## 🌐 URLs d'Accès

- **Application principale :** http://localhost:5173
- **API Backend :** http://localhost:5001
- **Test de connexion :** http://localhost:5173/test_connection.html
- **Test historique :** http://localhost:5173/test_historique.html

## 🔑 Identifiants de Test

- **Admin :** admin@exemple.com / admin123
- **Responsable :** jean.martin@exemple.com / resp123
- **Agent :** sofiane.bendaoud@exemple.com / agent123

## 🛠️ Résolution des Erreurs Courantes

### **Erreur : "Failed to connect to localhost port 5001"**
- **Cause :** Serveur Flask non démarré
- **Solution :** Utiliser `python3 start_app_direct.py`

### **Erreur : "Failed to connect to localhost port 5173"**
- **Cause :** Serveur Vite non démarré
- **Solution :** Vérifier que `npm run dev` fonctionne

### **Erreur : "cursor_snap_ENV_VARS"**
- **Cause :** Problème de configuration du terminal
- **Solution :** Utiliser les scripts Python au lieu des commandes bash

### **Erreur : "dump_zsh_state"**
- **Cause :** Configuration zsh corrompue
- **Solution :** Utiliser les scripts Python qui évitent le terminal

## 📝 Scripts Disponibles

1. **`start_app_direct.py`** - Démarrage simple et fiable
2. **`test_server.py`** - Diagnostic des serveurs
3. **`start_simple.sh`** - Wrapper bash pour Python
4. **`demarrer_app.sh`** - Script bash complet (peut avoir des problèmes)

## 🎯 Recommandation

**Utilisez toujours `python3 start_app_direct.py`** pour éviter les problèmes de terminal récurrents.

## 🆘 En Cas de Problème Persistant

1. **Redémarrer complètement :**
   ```bash
   pkill -f "python main.py"
   pkill -f "vite"
   python3 start_app_direct.py
   ```

2. **Vérifier les dépendances :**
   ```bash
   cd "/Users/nikkoolagarnier/Downloads/app manus rh"
   source venv/bin/activate
   pip install -r requirements.txt
   npm install
   ```

3. **Nettoyer et redémarrer :**
   ```bash
   rm -rf node_modules
   npm install
   python3 start_app_direct.py
   ```

---

**L'application RH est maintenant robuste contre les problèmes de connexion !** 🎉




