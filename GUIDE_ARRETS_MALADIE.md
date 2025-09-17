# Guide des Arrêts Maladie (AM)

## Vue d'ensemble

Les arrêts maladie (AM) sont maintenant disponibles dans l'application de gestion des congés. Cette fonctionnalité permet aux administrateurs et responsables de service d'enregistrer les arrêts maladie des agents avec calcul automatique de la perte de RTT selon les règles établies.

## Règles de perte de RTT

### Calcul automatique
- **Agents à 38h/semaine ou plus** : 1 jour de RTT perdu tous les 13 jours d'arrêt maladie
- **Agents à moins de 38h/semaine** : Aucune perte de RTT
- **Calcul par multiple** : 26 jours = 2 RTT perdus, 39 jours = 3 RTT perdus, etc.

### Exemples
- Agent 38h avec 13 jours d'arrêt → **1 RTT perdu**
- Agent 38h avec 25 jours d'arrêt → **1 RTT perdu** (pas encore 26)
- Agent 38h avec 26 jours d'arrêt → **2 RTT perdus**
- Agent 35h avec 20 jours d'arrêt → **0 RTT perdu** (pas 38h)

## Nouvelles fonctionnalités

### 1. Modèle ArretMaladie
- **Champs** : agent_id, date_debut, date_fin, nb_jours, motif, date_creation, cree_par
- **Calculs automatiques** : perte_rtt, jours_restants_prochain_rtt
- **Relations** : liaison avec Agent et historique des créateurs

### 2. API REST complète
- `GET /api/arret-maladie` : Liste des arrêts selon les permissions
- `POST /api/arret-maladie` : Création d'un arrêt maladie
- `PUT /api/arret-maladie/{id}` : Modification d'un arrêt
- `DELETE /api/arret-maladie/{id}` : Suppression d'un arrêt
- `GET /api/arret-maladie/agent/{id}/statistiques` : Statistiques par agent

### 3. Permissions et accès
- **Administrateurs** : Accès complet à tous les arrêts maladie
- **Responsables** : Accès aux arrêts maladie de leur service uniquement
- **Agents** : Consultation de leurs propres arrêts maladie

### 4. Interface utilisateur

#### AdminDashboard
- **Nouvel onglet** : "Arrêts maladie" avec compteur
- **Formulaire de création** : Agent, dates, motif avec prévisualisation des RTT perdus
- **Tableau de gestion** : Liste complète avec actions (modifier, supprimer)
- **Indicateurs visuels** : Badges rouges pour les RTT perdus

#### ResponsableDashboard
- **Nouvel onglet** : "Arrêts maladie du service"
- **Accès restreint** : Seulement aux agents de son service
- **Même fonctionnalités** : Création, modification, suppression

#### AgentProfile et AgentDashboard
- **Historique unifié** : Arrêts maladie intégrés dans l'historique des mouvements
- **Colonne supplémentaire** : "RTT perdus" avec badges visuels
- **Statut spécial** : "Enregistré" pour les arrêts maladie

## Utilisation

### Pour les administrateurs :

1. **Enregistrer un arrêt maladie** :
   - Aller dans l'onglet "Arrêts maladie"
   - Cliquer sur "Nouvel arrêt maladie"
   - Sélectionner l'agent concerné
   - Remplir les dates de début et fin
   - Optionnel : ajouter un motif
   - Sauvegarder

2. **Modifier un arrêt existant** :
   - Cliquer sur l'icône "Modifier" (crayon)
   - Modifier les informations nécessaires
   - Le calcul des RTT perdus se met à jour automatiquement

3. **Supprimer un arrêt** :
   - Cliquer sur l'icône "Supprimer" (poubelle)
   - Confirmer la suppression
   - Les RTT perdus sont automatiquement restaurés

### Pour les responsables :

1. **Accès restreint** :
   - Seuls les agents de leur service sont visibles
   - Mêmes fonctionnalités que l'admin mais avec restriction

2. **Suivi des équipes** :
   - Vue d'ensemble des arrêts maladie du service
   - Impact sur les soldes RTT des agents

### Pour les agents :

1. **Consultation** :
   - Historique complet dans leur dashboard personnel
   - Visibilité sur les RTT perdus
   - Intégration dans l'historique des mouvements

## Calculs et impacts

### Mise à jour automatique des soldes
- **Création d'arrêt** : Déduction immédiate des RTT perdus
- **Modification d'arrêt** : Recalcul et ajustement du solde
- **Suppression d'arrêt** : Restauration automatique des RTT

### Historique des mouvements
- **Chronologie** : Arrêts maladie intégrés avec les demandes de congés
- **Tri chronologique** : Affichage par date de création
- **Informations complètes** : Durée, RTT perdus, statut

### Statistiques disponibles
- **Total des arrêts** : Nombre et durée cumulée
- **RTT perdus** : Total des jours de RTT perdus
- **Année en cours** : Statistiques séparées par année

## Interface utilisateur

### Formulaire de création
```
┌─────────────────────────────────────┐
│ Nouvel arrêt maladie                │
├─────────────────────────────────────┤
│ Agent * : [Sélectionner agent]      │
│ Date début * : [Date picker]        │
│ Date fin * : [Date picker]          │
│ Motif : [Zone de texte]             │
│                                     │
│ ℹ️ Information : Si l'agent est à   │
│    38h/semaine ou plus, il perdra   │
│    1 jour de RTT tous les 13 jours  │
│    d'arrêt maladie.                 │
│                                     │
│ [Annuler] [Enregistrer]             │
└─────────────────────────────────────┘
```

### Tableau de gestion
```
┌─────────┬──────────┬─────────────┬────────┬──────────┬──────────┬─────────┐
│ Agent   │ Période  │ Durée       │ RTT    │ Créé par │ Actions  │         │
├─────────┼──────────┼─────────────┼────────┼──────────┼──────────┼─────────┤
│ Dupont  │ 01/02 -  │ 15 jours    │ 1 jour │ Admin    │ [✏️] [🗑] │         │
│ Jean    │ 15/02    │             │ (rouge)│          │          │         │
└─────────┴──────────┴─────────────┴────────┴──────────┴──────────┴─────────┘
```

### Historique des mouvements
```
┌─────────┬─────────────┬─────────────┬────────┬──────────┬──────────┬──────────┐
│ Date    │ Type        │ Période     │ Durée  │ Statut   │ RTT      │ Solde... │
├─────────┼─────────────┼─────────────┼────────┼──────────┼──────────┼──────────┤
│ 01/02   │ Arrêt       │ 01/02 -     │ 15     │ Enregistré│ 1 jour   │ -        │
│         │ maladie     │ 15/02       │ jours  │ (bleu)   │ (rouge)  │          │
└─────────┴─────────────┴─────────────┴────────┴──────────┴──────────┴──────────┘
```

## Tests et validation

### Script de test
```bash
python3 test_arret_maladie.py
```

Le script teste :
- ✅ Création d'arrêts maladie
- ✅ Calcul automatique des RTT perdus
- ✅ Mise à jour des soldes d'agents
- ✅ Permissions par rôle
- ✅ API et base de données

### Scénarios de test
1. **Agent 38h + 13 jours** → 1 RTT perdu
2. **Agent 38h + 25 jours** → 1 RTT perdu
3. **Agent 38h + 26 jours** → 2 RTT perdus
4. **Agent 35h + 20 jours** → 0 RTT perdu
5. **Modification d'arrêt** → Recalcul des RTT
6. **Suppression d'arrêt** → Restauration des RTT

## Migration et déploiement

### Base de données
- **Table créée** : `arret_maladie` avec toutes les relations
- **Migration automatique** : Flask-SQLAlchemy crée la table
- **Compatibilité** : Rétrocompatible avec les données existantes

### Déploiement
1. ✅ Modèles ajoutés
2. ✅ Routes API créées
3. ✅ Interfaces utilisateur intégrées
4. ✅ Calculs automatiques implémentés
5. ✅ Tests de validation

## Résolution de problèmes

### Si les RTT ne sont pas déduits :
1. Vérifier que l'agent est à 38h/semaine ou plus
2. Vérifier que l'arrêt fait au moins 13 jours
3. Contrôler les logs du serveur pour les erreurs

### Si les permissions ne fonctionnent pas :
1. Vérifier le rôle de l'utilisateur connecté
2. Pour les responsables : s'assurer que l'agent appartient à leur service
3. Contrôler les sessions utilisateur

### Si l'historique ne s'affiche pas :
1. Vérifier que les données sont chargées
2. Contrôler les appels API dans la console du navigateur
3. Vérifier les permissions d'accès aux arrêts maladie

## Support et maintenance

### Logs à surveiller
- Création/modification/suppression d'arrêts maladie
- Calculs de RTT perdus
- Erreurs de permissions

### Métriques importantes
- Nombre d'arrêts maladie par agent
- Total des RTT perdus par service
- Fréquence des arrêts maladie

### Évolutions futures possibles
- Notifications automatiques
- Rapports détaillés
- Intégration avec des systèmes externes
- Calculs plus complexes selon la législation




