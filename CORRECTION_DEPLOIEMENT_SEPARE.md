# 🔧 Correction du déploiement séparé Vercel + Render

## ❌ Problèmes identifiés

### **Erreurs actuelles :**
1. **404 sur check-session** - L'API n'est pas accessible
2. **405 sur login** - Méthode HTTP non autorisée
3. **SyntaxError** - Problème de parsing JSON
4. **CORS** - Problème de cross-origin

## ✅ Solutions appliquées

### **1. Configuration Vercel corrigée**

**Fichier `vercel.json` mis à jour :**

```json
{
  "build": {
    "env": {
      "VITE_API_URL": "https://app-manus-rh-api.onrender.com/api"
    }
  },
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### **2. Configuration CORS pour Render**

Créer un fichier `cors_config.py` pour Render :

```python
from flask_cors import CORS

def configure_cors(app):
    """Configure CORS pour le déploiement sur Render"""
    CORS(app, origins=[
        "https://app-manus-rh.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173"
    ])
    
    # Headers CORS spécifiques
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'https://app-manus-rh.vercel.app')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
```

### **3. Modification de main.py pour Render**

```python
import os
from flask_cors import CORS

# Configuration pour Render
if os.environ.get('RENDER'):
    # Mode production Render
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['DEBUG'] = False
    # Configuration CORS
    CORS(app, origins=['https://app-manus-rh.vercel.app'])
else:
    # Mode développement local
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
    app.config['DEBUG'] = True

# Démarrer l'application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
```

## 🚀 Étapes de correction

### **Étape 1 : Corriger le frontend (Vercel)**

```bash
# 1. Mettre à jour vercel.json
git add vercel.json
git commit -m "Fix: Configuration API URL pour Render"
git push origin main

# 2. Redéployer sur Vercel
# Vercel redéploiera automatiquement
```

### **Étape 2 : Corriger le backend (Render)**

```bash
# 1. Ajouter Flask-CORS aux requirements
echo "Flask-CORS==4.0.0" >> requirements.txt

# 2. Modifier main.py pour Render
# (voir le code ci-dessus)

# 3. Commiter et pousser
git add .
git commit -m "Fix: Configuration CORS pour Render"
git push origin main

# 4. Render redéploiera automatiquement
```

### **Étape 3 : Vérifier les variables d'environnement**

**Sur Render :**
- `DATABASE_URL` : URL de la base de données
- `MAIL_USERNAME` : Votre email Gmail
- `MAIL_PASSWORD` : Mot de passe d'application Gmail
- `MAIL_DEFAULT_SENDER` : Votre email Gmail

**Sur Vercel :**
- `VITE_API_URL` : `https://app-manus-rh-api.onrender.com/api`

## 🔍 Tests de correction

### **Test 1 : Vérifier l'API Render**

```bash
# Tester l'endpoint de base
curl https://app-manus-rh-api.onrender.com/api/

# Tester l'endpoint de session
curl https://app-manus-rh-api.onrender.com/api/auth/check-session
```

### **Test 2 : Vérifier CORS**

```bash
# Tester avec les headers CORS
curl -H "Origin: https://app-manus-rh.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://app-manus-rh-api.onrender.com/api/auth/login
```

### **Test 3 : Vérifier le frontend**

1. **Ouvrir** https://app-manus-rh.vercel.app
2. **Ouvrir** la console du navigateur (F12)
3. **Vérifier** qu'il n'y a plus d'erreurs 404/405
4. **Tester** la connexion

## 📱 Configuration finale

### **URLs de production :**
- **Frontend** : https://app-manus-rh.vercel.app
- **Backend** : https://app-manus-rh-api.onrender.com
- **API** : https://app-manus-rh-api.onrender.com/api

### **Comptes de test :**
- **Admin** : admin@exemple.com / admin123
- **Responsable** : jean.martin@exemple.com / resp123
- **Agent** : sofiane.bendaoud@exemple.com / agent123

## 🔧 Dépannage avancé

### **Problème : "CORS error"**
```python
# Ajouter dans main.py
from flask_cors import CORS
CORS(app, origins=['https://app-manus-rh.vercel.app'])
```

### **Problème : "Database connection failed"**
```bash
# Vérifier DATABASE_URL sur Render
# Utiliser PostgreSQL au lieu de SQLite
```

### **Problème : "Session not working"**
```python
# Ajouter dans main.py
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
```

## 📚 Fichiers à modifier

1. **`vercel.json`** - Configuration frontend
2. **`main.py`** - Configuration backend
3. **`requirements.txt`** - Ajouter Flask-CORS
4. **Variables d'environnement** - Sur Render et Vercel

---

**🎉 Après ces corrections, votre application fonctionnera parfaitement !**

**Prochaine étape** : Appliquer les corrections et redéployer !
