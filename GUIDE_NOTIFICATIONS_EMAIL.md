# Guide des Notifications Email

## Vue d'ensemble

Le système de notifications email permet l'envoi automatique d'emails lors des actions importantes dans l'application RH. Les agents et responsables reçoivent des notifications en temps réel pour les demandes de congés et leurs validations.

## 🎯 Fonctionnalités

### 1. **Notifications Automatiques**
- ✅ **Nouvelle demande** : Email au responsable quand un agent fait une demande
- ✅ **Validation** : Email à l'agent quand sa demande est approuvée
- ✅ **Refus** : Email à l'agent quand sa demande est refusée
- ✅ **Templates HTML** : Emails avec design professionnel et responsive

### 2. **Types de Notifications**

#### **Email de Nouvelle Demande (Responsable)**
- Informations de l'agent (nom, email, service)
- Détails de la demande (type, période, durée, motif)
- Lien direct vers l'application pour validation
- Design avec gradient et icônes

#### **Email de Validation (Agent)**
- Détails de la demande validée/refusée
- Informations du validateur
- Impact sur les soldes (si approuvée)
- Lien vers l'espace personnel

#### **Email de Test (Admin)**
- Vérification de la configuration SMTP
- Confirmation du bon fonctionnement
- Instructions d'utilisation

## 🔧 Configuration

### 1. **Variables d'Environnement**

Créez un fichier `.env` ou configurez les variables suivantes :

```bash
# Serveur SMTP
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# Sécurité
MAIL_USE_TLS=True
MAIL_USE_SSL=False

# Identifiants
MAIL_USERNAME=votre.email@gmail.com
MAIL_PASSWORD=votre_mot_de_passe_application

# Expéditeur
MAIL_DEFAULT_SENDER=noreply@votre-entreprise.com
```

### 2. **Configuration par Fournisseur**

#### **Gmail**
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=votre.email@gmail.com
MAIL_PASSWORD=mot_de_passe_application  # Pas votre mot de passe normal !
```

**Étapes pour Gmail :**
1. Activez l'authentification à 2 facteurs
2. Générez un mot de passe d'application
3. Utilisez ce mot de passe dans `MAIL_PASSWORD`

#### **Office 365**
```bash
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=votre.email@entreprise.com
MAIL_PASSWORD=votre_mot_de_passe_normal
```

#### **Yahoo**
```bash
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=votre.email@yahoo.com
MAIL_PASSWORD=mot_de_passe_application
```

### 3. **Configuration via API**

Vous pouvez aussi configurer l'email via l'API :

```bash
# Récupérer la configuration actuelle
GET /api/email/config

# Mettre à jour la configuration
POST /api/email/config
{
  "mail_server": "smtp.gmail.com",
  "mail_port": 587,
  "mail_use_tls": true,
  "mail_username": "votre.email@gmail.com",
  "mail_password": "votre_mot_de_passe",
  "mail_default_sender": "noreply@entreprise.com"
}
```

## 📧 Templates d'Email

### 1. **Email de Nouvelle Demande**

#### **Design**
- **Header** : Gradient bleu avec icône calendrier
- **Contenu** : Informations structurées dans des boîtes
- **Actions** : Bouton d'accès à l'application
- **Footer** : Informations légales

#### **Contenu**
```
📅 Nouvelle demande de congé - Jean Dupont

👤 Informations de l'Agent
- Nom : Jean Dupont
- Email : jean.dupont@entreprise.com
- Service : Ressources Humaines

📋 Détails de la Demande
- Type d'absence : Congés Annuels
- Période : 15/04/2024 au 17/04/2024
- Durée : 21 heures
- Date de demande : 10/04/2024 à 14:30
- Statut : En attente
- Motif : Vacances familiales

⚡ Actions Requises
Veuillez vous connecter à l'application RH pour valider ou refuser cette demande.
[Accéder à l'application]
```

### 2. **Email de Validation**

#### **Design**
- **Header** : Gradient vert (approuvé) ou rouge (refusé)
- **Contenu** : Détails de la décision
- **Impact** : Information sur les soldes (si approuvé)
- **Actions** : Lien vers l'espace personnel

#### **Contenu (Approuvé)**
```
✅ Demande de Congé VALIDÉE - Congés Annuels

Votre demande de congé a été validée par Marie Dubois

📋 Détails de la Demande
- Type d'absence : Congés Annuels
- Période : 15/04/2024 au 17/04/2024
- Durée : 21 heures
- Statut : Approuvée

👤 Validé par
- Nom : Marie Dubois
- Rôle : Responsable
- Date de validation : 11/04/2024 à 09:15

💰 Impact sur vos soldes
Cette demande a été déduite de votre solde de congés annuels.
Vous pouvez consulter vos soldes actuels dans votre espace personnel.

[Accéder à mon espace]
```

#### **Contenu (Refusé)**
```
❌ Demande de Congé REFUSÉE - RTT

Votre demande de congé a été refusée par Marie Dubois

📋 Détails de la Demande
- Type d'absence : RTT
- Période : 20/04/2024 au 20/04/2024
- Durée : 7 heures
- Statut : Refusée

👤 Refusé par
- Nom : Marie Dubois
- Rôle : Responsable
- Date de validation : 11/04/2024 à 09:15
- Commentaires : Période trop chargée, veuillez reporter

[Accéder à mon espace]
```

## 🚀 Utilisation

### 1. **Pour les Administrateurs**

#### **Configuration**
1. Connectez-vous en tant qu'admin
2. Configurez les paramètres SMTP via l'API ou les variables d'environnement
3. Testez la configuration avec l'email de test

#### **Test de Configuration**
```bash
# Via l'API
POST /api/email/test
{
  "email": "test@exemple.com"
}

# Via le script de test
python3 test_email_system.py
```

### 2. **Pour les Responsables**

#### **Réception des Notifications**
- **Email automatique** lors de chaque nouvelle demande
- **Lien direct** vers l'application pour validation
- **Informations complètes** pour prendre une décision éclairée

#### **Actions**
1. Recevoir l'email de notification
2. Cliquer sur le lien vers l'application
3. Se connecter et valider/refuser la demande
4. L'agent recevra automatiquement un email de confirmation

### 3. **Pour les Agents**

#### **Réception des Notifications**
- **Email de confirmation** lors de la validation/refus
- **Détails complets** de la décision
- **Impact sur les soldes** (si approuvé)
- **Lien vers l'espace personnel**

#### **Actions**
1. Faire une demande de congé
2. Le responsable reçoit automatiquement un email
3. Recevoir un email de confirmation de la décision
4. Consulter les détails dans l'espace personnel

## 🧪 Tests et Validation

### 1. **Script de Test Complet**

Le script `test_email_system.py` teste :
- Configuration email
- Envoi d'email de test
- Création de demande avec notification
- Validation avec notification
- Refus avec notification

### 2. **Tests Manuels**

#### **Test de Configuration**
```bash
# 1. Vérifier la configuration
GET /api/email/config

# 2. Envoyer un email de test
POST /api/email/test
{
  "email": "votre.email@exemple.com"
}
```

#### **Test de Workflow Complet**
1. **Agent** : Créer une demande de congé
2. **Vérifier** : Email reçu par le responsable
3. **Responsable** : Valider ou refuser la demande
4. **Vérifier** : Email reçu par l'agent

### 3. **Dépannage**

#### **Emails non reçus**
1. Vérifiez la configuration SMTP
2. Vérifiez les logs de l'application
3. Vérifiez le dossier spam
4. Testez avec l'email de test

#### **Erreurs de configuration**
1. Vérifiez les variables d'environnement
2. Vérifiez les identifiants SMTP
3. Vérifiez les paramètres de sécurité (TLS/SSL)
4. Testez avec différents fournisseurs

## 📊 Monitoring et Logs

### 1. **Logs d'Envoi**
```python
# Les erreurs d'envoi sont loggées
current_app.logger.error(f"Erreur lors de l'envoi de l'email: {str(e)}")
```

### 2. **Statistiques**
- Nombre d'emails envoyés
- Taux de succès d'envoi
- Erreurs par type
- Performance des envois

### 3. **Monitoring**
- Vérification périodique de la configuration
- Alertes en cas d'échec d'envoi
- Dashboard de monitoring (futur)

## 🔒 Sécurité

### 1. **Protection des Données**
- **Mots de passe** : Stockés en variables d'environnement
- **Contenu** : Pas d'informations sensibles dans les emails
- **Expéditeur** : Adresse générique pour éviter le spam

### 2. **Authentification**
- **SMTP** : Authentification sécurisée
- **API** : Contrôle d'accès par rôle
- **Validation** : Vérification des permissions

### 3. **Conformité**
- **RGPD** : Respect de la vie privée
- **Audit** : Traçabilité des envois
- **Consentement** : Notifications légitimes uniquement

## 📈 Évolutions Futures

### 1. **Fonctionnalités Avancées**
- **Templates personnalisables** : Modification des designs
- **Notifications push** : Intégration mobile
- **Planification** : Envoi différé
- **Rapports** : Statistiques détaillées

### 2. **Intégrations**
- **Slack** : Notifications dans les canaux
- **Teams** : Intégration Microsoft
- **WhatsApp** : Notifications par SMS
- **Systèmes RH** : Synchronisation externe

### 3. **Améliorations UX**
- **Prévisualisation** : Aperçu des emails
- **Personnalisation** : Choix des notifications
- **Gestion** : Interface d'administration
- **Analytics** : Tableaux de bord

Le système de notifications email transforme l'application RH en offrant une communication automatique et professionnelle entre tous les acteurs. Les templates HTML modernes et la configuration flexible en font un outil de communication efficace et fiable.

