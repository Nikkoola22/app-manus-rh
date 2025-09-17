# 🚀 Guide de Démarrage - Application RH

## ✅ Corrections Apportées

### 1. **Page Personnelle de l'Agent**
- ✅ Ajout de la **quotité de travail hebdomadaire** (ex: 35h/semaine)
- ✅ Ajout de la **date d'arrivée** dans l'entreprise
- ✅ Ajout de l'**année d'entrée FP**
- ✅ Ajout de la **date de fin de contrat** (ou CDI)
- ✅ Informations personnelles complètes (nom, email, service, rôle)

### 2. **Menus Déroulants Fonctionnels**
- ✅ Correction du composant `Select` pour les formulaires
- ✅ Menus déroulants dans "Nouvelle demande de congés" maintenant fonctionnels
- ✅ Affichage correct des valeurs sélectionnées

### 3. **Configuration des Serveurs**
- ✅ Serveur Flask sur le port **5001** (au lieu de 5000)
- ✅ Configuration Vite mise à jour pour pointer vers le port 5001
- ✅ Script de démarrage automatique créé

## 🚀 Démarrage Rapide

### Option 1: Script Automatique
```bash
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
./start_servers.sh
```

### Option 2: Démarrage Manuel

**Terminal 1 - Backend (Flask):**
```bash
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend (Vite):**
```bash
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
npm run dev
```

## 🔗 URLs d'Accès

- **Application principale:** http://localhost:5173
- **Test de connexion:** http://localhost:5173/test_connection.html
- **API Backend:** http://localhost:5001

## 🔑 Identifiants de Test

**Admin:**
- Email: `admin@exemple.com`
- Mot de passe: `admin123`

**Responsable:**
- Email: `jean.martin@exemple.com`
- Mot de passe: `resp123`

**Agent:**
- Email: `sofiane.bendaoud@exemple.com`
- Mot de passe: `agent123`

## ✨ Nouvelles Fonctionnalités

### 📧 **Système de Notifications Email**
- **Nouvelle demande** : Email automatique au responsable
- **Validation/Refus** : Email automatique à l'agent
- **Templates HTML** : Design professionnel et responsive
- **Configuration flexible** : Support Gmail, Office 365, Yahoo

### 📅 **Calendrier de Présence avec Créneaux**
- **Cases séparées** : Matin et après-midi
- **Gestion des présences partielles** : Heures de début/fin
- **Intégration des congés** : Affichage des demandes validées
- **Navigation par semaines** : Calendrier perpétuel
- **Statistiques temps réel** : Présences, absences, congés

### 🏥 **Gestion des Arrêts Maladie**
- **Enregistrement** : Périodes et motifs
- **Calcul automatique** : Perte de RTT (1 RTT tous les 13 jours)
- **Intégration** : Historique des mouvements
- **Notifications** : Suivi des impacts sur les soldes

### ⏰ **Gestion des Heures Supplémentaires**
- **Ajout au solde RTT** : Conversion des HS en congés
- **Gestion des dates** : Traçabilité des réalisations
- **Intégration** : Historique des mouvements
- **Calculs automatiques** : Mise à jour des soldes

### Page Personnelle de l'Agent
Quand un agent se connecte, il voit maintenant :

1. **Mes Informations**
   - Nom complet
   - Email
   - Service
   - Rôle

2. **Informations de Travail**
   - **Date d'arrivée** (format français)
   - **Quotité de travail** (ex: 35h/semaine)
   - Année d'entrée FP
   - Fin de contrat (ou CDI)

3. **Soldes de Congés**
   - Congés Annuels
   - RTT
   - CET

4. **Actions**
   - Nouvelle demande de congé (avec menus déroulants fonctionnels)
   - Historique des demandes
   - Gestion des heures supplémentaires

## 📧 Configuration Email

### 1. **Variables d'Environnement**
Créez un fichier `.env` ou configurez :
```bash
# Gmail (recommandé)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=votre.email@gmail.com
MAIL_PASSWORD=mot_de_passe_application
MAIL_DEFAULT_SENDER=noreply@votre-entreprise.com
```

### 2. **Configuration Gmail**
1. Activez l'authentification à 2 facteurs
2. Générez un mot de passe d'application
3. Utilisez ce mot de passe dans `MAIL_PASSWORD`

### 3. **Test de Configuration**
```bash
# Script de test complet
python3 test_email_system.py

# Ou via l'API
POST /api/email/test
{
  "email": "test@exemple.com"
}
```

### 4. **Fonctionnement**
- **Agent fait une demande** → Email au responsable
- **Responsable valide/refuse** → Email à l'agent
- **Templates HTML** → Design professionnel
- **Configuration flexible** → Support multiple fournisseurs

## 🛠️ Dépannage

### Si les connexions ne fonctionnent pas :
1. Vérifiez que les deux serveurs sont démarrés
2. Utilisez le test de connexion : http://localhost:5173/test_connection.html
3. Vérifiez les ports (Flask: 5001, Vite: 5173)

### Si les menus déroulants ne fonctionnent pas :
1. Rechargez la page (Ctrl+F5)
2. Vérifiez la console du navigateur pour les erreurs

### Si les emails ne sont pas envoyés :
1. Vérifiez la configuration SMTP
2. Vérifiez les variables d'environnement
3. Testez avec l'email de test
4. Vérifiez le dossier spam

## 📝 Notes

- Le serveur Flask a été déplacé du port 5000 au port 5001 pour éviter les conflits
- Tous les composants Select ont été corrigés pour être fonctionnels
- La page personnelle de l'agent affiche maintenant toutes les informations demandées



