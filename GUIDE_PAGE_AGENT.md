# Guide d'utilisation - Page Agent

## 🎯 Fonctionnalité créée

Une page personnelle détaillée pour chaque agent a été ajoutée à l'application. Cette page permet de consulter toutes les informations d'un agent de manière organisée.

## 🔑 Identifiants de connexion

**Admin :**
- Email: `admin@exemple.com`
- Mot de passe: `admin123`

**Responsable :**
- Email: `jean.martin@exemple.com`
- Mot de passe: `resp123`

**Agent :**
- Email: `sofiane.bendaoud@exemple.com`
- Mot de passe: `agent123`

## 📋 Comment utiliser la page agent

### 1. Se connecter
1. Ouvrir l'application : http://localhost:5173
2. Se connecter avec un des identifiants ci-dessus

### 2. Accéder à la page agent
**En tant qu'Admin :**
1. Aller dans l'onglet "Agents" du dashboard
2. Cliquer sur l'icône "œil" (👁️) à côté d'un agent
3. La page agent s'ouvre

**En tant que Responsable :**
1. Aller dans l'onglet "Agents" du dashboard
2. Cliquer sur l'icône "œil" (👁️) à côté d'un agent de votre service
3. La page agent s'ouvre

### 3. Explorer la page agent

La page agent contient 3 onglets :

#### 📊 Onglet "Informations"
- **Informations personnelles** : nom, prénom, email, rôle, service
- **Informations de travail** : quotité, soldes CA/RTT/CET

#### 📅 Onglet "Congés"
- **Historique des demandes** : toutes les demandes de congé de l'agent
- **Statuts** : En attente, Approuvée, Refusée
- **Détails** : type, période, durée, date de demande

#### 📈 Onglet "Historique"
- **Section réservée** pour les futures fonctionnalités
- **Journal des activités** (à venir)

### 4. Navigation
- **Bouton "Retour"** : retourne au dashboard principal
- **Bouton "Modifier"** : pour modifier les informations (à implémenter)

## 🛠️ Fonctionnalités techniques

### APIs utilisées
- `GET /api/agents/{id}` : récupère les données d'un agent
- `GET /api/demandes/agent/{id}` : récupère les demandes d'un agent

### Sécurité
- **Contrôle des permissions** selon le rôle
- **Agent** : peut voir uniquement son propre profil
- **Responsable** : peut voir les agents de son service
- **Admin** : peut voir tous les agents

### Interface
- **Responsive** : s'adapte aux différentes tailles d'écran
- **Moderne** : design cohérent avec le reste de l'application
- **Accessible** : boutons avec tooltips et labels

## 🧪 Test de l'application

### Test automatique
1. Ouvrir : http://localhost:5173/test_agent_profile.html
2. Cliquer sur "Admin (admin@exemple.com)" ou "Responsable (jean.martin@exemple.com)"
3. Cliquer sur "Tester l'API Agent"
4. Cliquer sur "Tester l'API Demandes Agent"

### Test manuel
1. Se connecter avec `admin@exemple.com` / `admin123` ou `jean.martin@exemple.com` / `resp123`
2. Aller dans "Agents"
3. Cliquer sur l'icône "œil" à côté de "SOFIANE BENDAOUD"
4. Explorer les 3 onglets de la page agent

## ✅ Statut

- ✅ Composant AgentProfile créé
- ✅ API backend implémentée
- ✅ Intégration dans le Dashboard
- ✅ Navigation depuis les listes d'agents
- ✅ Tests fonctionnels validés

## 🚀 Prochaines étapes possibles

1. **Modification des informations** : bouton "Modifier" fonctionnel
2. **Historique des activités** : journal des actions
3. **Export des données** : PDF des informations agent
4. **Notifications** : alertes pour les agents
5. **Statistiques** : graphiques des congés pris

---

*Page agent créée avec succès ! 🎉*
