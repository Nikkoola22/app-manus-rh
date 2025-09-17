# 📧 Guide de Configuration Email

## 🎯 Objectif

Configurer l'envoi d'emails pour recevoir les notifications de validation de congés à `nikkoola@gmail.com`.

## 🔧 Configuration Gmail

### 1. **Préparer votre compte Gmail**

1. **Aller sur** : https://myaccount.google.com/security
2. **Activer l'authentification à 2 facteurs** :
   - Cliquer sur "Authentification à 2 facteurs"
   - Suivre les instructions pour l'activer
3. **Générer un mot de passe d'application** :
   - Aller dans "Mots de passe des applications"
   - Sélectionner "Autre" et nommer "Application RH"
   - Copier le mot de passe généré (16 caractères)

### 2. **Configurer les variables d'environnement**

Créer un fichier `.env` dans le répertoire de l'application :

```bash
# Configuration Email Gmail
MAIL_USERNAME=nikkoola@gmail.com
MAIL_PASSWORD=votre-mot-de-passe-app-16-caracteres
MAIL_DEFAULT_SENDER=nikkoola@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
```

### 3. **Installer python-dotenv**

```bash
pip install python-dotenv
```

## 🧪 Test de l'envoi d'emails

### **Test 1 : Email de test**

```bash
python3 test_email_config.py
```

### **Test 2 : Demande de congé complète**

1. **Se connecter** comme responsable (jean.martin@exemple.com / resp123)
2. **Créer une demande** de congé pour un agent
3. **Valider la demande** 
4. **Vérifier l'email** reçu à nikkoola@gmail.com

## 📧 Types d'emails envoyés

### 1. **Email de notification de demande**
- **Quand** : Un agent crée une demande de congé
- **Destinataire** : Responsable du service
- **Contenu** : Détails de la demande

### 2. **Email de validation**
- **Quand** : Une demande est validée ou refusée
- **Destinataire** : Agent qui a fait la demande
- **Contenu** : Décision et commentaires

### 3. **Email de test**
- **Quand** : Test de configuration
- **Destinataire** : Email spécifié
- **Contenu** : Confirmation de configuration

## 🔍 Dépannage

### **Problème : "Authentication failed"**
- ✅ Vérifier que l'authentification à 2 facteurs est activée
- ✅ Vérifier que le mot de passe d'application est correct
- ✅ Vérifier que l'email est correct

### **Problème : "Connection refused"**
- ✅ Vérifier la connexion internet
- ✅ Vérifier les paramètres SMTP (smtp.gmail.com:587)

### **Problème : "No emails received"**
- ✅ Vérifier le dossier spam
- ✅ Vérifier que l'email de destination est correct
- ✅ Vérifier les logs de l'application

## 📁 Fichiers modifiés

1. **`src/services/email_service.py`**
   - Ajout du chargement du .env
   - Fonction `send_test_email()`

2. **`src/routes/test_email.py`**
   - Route de test pour l'envoi d'emails

3. **`main.py`**
   - Enregistrement de la route de test

4. **`.env`** (à créer)
   - Configuration des variables d'environnement

## ✅ Vérification

### **1. Configuration correcte**
```bash
# Vérifier que le fichier .env existe
ls -la .env

# Vérifier le contenu
cat .env
```

### **2. Test d'envoi**
```bash
# Tester l'envoi d'email
python3 test_email_config.py
```

### **3. Test complet**
1. Démarrer l'application
2. Se connecter comme responsable
3. Créer et valider une demande
4. Vérifier l'email reçu

---

**🎉 Une fois configuré, vous recevrez tous les emails de notification !**
