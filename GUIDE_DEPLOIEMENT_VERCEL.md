# 🚀 Guide de déploiement sur Vercel

## ✅ Configuration Vercel

Votre application est maintenant configurée pour être déployée sur Vercel !

### **Fichier `vercel.json` corrigé :**

```json
{
  "build": {
    "env": {
      "VITE_API_URL": "/api"
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/$1"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "functions": {
    "main.py": {
      "runtime": "python3.9"
    }
  }
}
```

## 🌐 Déploiement sur Vercel

### **Étape 1 : Préparer l'application**

```bash
# 1. Construire le frontend
npm run build

# 2. Vérifier que le dossier dist/ est créé
ls -la dist/

# 3. Commiter les changements
git add .
git commit -m "Add: Configuration Vercel pour déploiement"
git push origin main
```

### **Étape 2 : Déployer sur Vercel**

#### **Option A : Via l'interface web Vercel**

1. **Aller sur** : https://vercel.com
2. **Se connecter** avec GitHub
3. **Cliquer** sur "New Project"
4. **Sélectionner** le dépôt `app-manus-rh`
5. **Configurer** :
   - Framework Preset : `Other`
   - Build Command : `npm run build`
   - Output Directory : `dist`
   - Install Command : `npm install`
6. **Cliquer** sur "Deploy"

#### **Option B : Via Vercel CLI**

```bash
# 1. Installer Vercel CLI
npm install -g vercel

# 2. Se connecter
vercel login

# 3. Déployer
vercel

# 4. Suivre les instructions
```

### **Étape 3 : Configuration des variables d'environnement**

Dans le dashboard Vercel :

1. **Aller** dans Settings > Environment Variables
2. **Ajouter** :
   ```
   MAIL_USERNAME=votre-email@gmail.com
   MAIL_PASSWORD=votre-mot-de-passe-app
   MAIL_DEFAULT_SENDER=votre-email@gmail.com
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   ```

## 🔧 Modifications nécessaires pour Vercel

### **1. Modifier `main.py` pour la production :**

```python
import os
from pathlib import Path

# Configuration pour Vercel
if os.environ.get('VERCEL'):
    # Mode production Vercel
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/app.db'
    app.config['DEBUG'] = False
else:
    # Mode développement local
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
    app.config['DEBUG'] = True

# Démarrer l'application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### **2. Créer un fichier `requirements.txt` optimisé :**

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Mail==0.9.1
python-dotenv==1.0.0
Werkzeug==2.3.7
```

### **3. Créer un fichier `package.json` optimisé :**

```json
{
  "name": "app-manus-rh",
  "version": "1.0.0",
  "scripts": {
    "build": "vite build",
    "dev": "vite",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.263.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.3",
    "vite": "^4.4.5",
    "tailwindcss": "^3.3.3",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.27"
  }
}
```

## 📱 Accès à l'application déployée

### **URL de production :**
- **Vercel** : `https://app-manus-rh.vercel.app`
- **Domaine personnalisé** : Possible avec Vercel Pro

### **Comptes par défaut :**
- **Admin** : admin@exemple.com / admin123
- **Responsable** : jean.martin@exemple.com / resp123
- **Agent** : sofiane.bendaoud@exemple.com / agent123

## 🧪 Tests de déploiement

### **Test 1 : Vérifier l'URL**
```bash
# Tester l'URL de production
curl https://app-manus-rh.vercel.app
```

### **Test 2 : Tester l'API**
```bash
# Tester l'endpoint API
curl https://app-manus-rh.vercel.app/api/auth/login
```

### **Test 3 : Interface utilisateur**
1. **Ouvrir** l'URL dans un navigateur
2. **Se connecter** avec un compte par défaut
3. **Tester** les fonctionnalités principales

## 🔍 Dépannage Vercel

### **Problème : "Build failed"**
```bash
# Vérifier les logs de build
vercel logs

# Vérifier la configuration
vercel inspect
```

### **Problème : "Function timeout"**
```bash
# Vérifier la configuration des fonctions
# Augmenter le timeout dans vercel.json
```

### **Problème : "Database not found"**
```bash
# Vérifier que la base de données est incluse
# Ou configurer une base de données externe
```

## 🎯 Avantages de Vercel

### **✅ Gratuit :**
- **Bande passante** : 100 GB/mois
- **Fonctions** : 100 GB-heures/mois
- **Builds** : Illimités
- **Domaine** : Sous-domaine .vercel.app

### **✅ Fonctionnalités :**
- **Déploiement automatique** depuis GitHub
- **HTTPS** automatique
- **CDN** global
- **Mise à jour** automatique à chaque push
- **Logs** en temps réel

## 📚 Documentation Vercel

- **Documentation** : https://vercel.com/docs
- **Guide Python** : https://vercel.com/docs/functions/serverless-functions/runtimes/python
- **Variables d'environnement** : https://vercel.com/docs/environment-variables

## 🚀 Déploiement final

### **Commande de déploiement :**

```bash
# 1. Construire et commiter
npm run build
git add .
git commit -m "Ready for Vercel deployment"
git push origin main

# 2. Déployer sur Vercel
vercel --prod
```

---

**🎉 Votre application de gestion RH est maintenant prête pour Vercel !**

**Prochaine étape** : Déployer sur Vercel et tester l'application en production !
