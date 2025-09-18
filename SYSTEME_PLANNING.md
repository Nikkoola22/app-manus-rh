# 🗓️ Système de Planning des Agents

## 📋 Fonctionnalités

### ✅ Modèles de données
- **PlanningAgent** : Planning individuel par agent et par jour
- **PlanningTemplate** : Modèles de planning réutilisables
- **Créneaux de 30 minutes** : De 8h00 à 19h00
- **Gestion des pauses** : Pauses déjeuner configurables

### ✅ API Backend
- **GET** `/api/planning/agent/{id}` : Récupérer le planning d'un agent
- **POST** `/api/planning/agent/{id}` : Créer/modifier le planning d'un agent
- **PUT** `/api/planning/agent/{id}/jour/{jour}` : Modifier un jour spécifique
- **GET** `/api/planning/service/{id}` : Récupérer tous les plannings d'un service
- **GET/POST** `/api/planning/templates` : Gestion des modèles

### ✅ Interface Frontend
- **PlanningAgent** : Affichage du planning avec créneaux de 30 minutes
- **PlanningEditor** : Édition des horaires par jour
- **Dashboard Responsable** : Onglet dédié au planning
- **Couleurs visuelles** : Travail (vert), Pause (orange), Libre (gris)

## 🎯 Utilisation

### Pour le Responsable
1. **Accéder au planning** : Onglet "Planning" dans le dashboard
2. **Voir les plannings** : Tous les agents du service avec leurs horaires
3. **Modifier un planning** : Bouton "Modifier le planning" pour chaque agent
4. **Configurer les horaires** : Par jour (Lundi à Samedi)
5. **Définir les pauses** : Pauses déjeuner optionnelles

### Pour l'Agent
1. **Consulter son planning** : Dans son profil ou dashboard
2. **Voir les créneaux** : Affichage détaillé par créneaux de 30 minutes
3. **Vérifier les horaires** : Heures de travail et pauses

## 📊 Structure des données

### PlanningAgent
```json
{
  "id": 1,
  "agent_id": 2,
  "jour_semaine": 0,
  "jour_nom": "Lundi",
  "heure_debut": "08:00",
  "heure_fin": "17:00",
  "pause_debut": "12:00",
  "pause_fin": "13:00",
  "actif": true,
  "duree_travail": 8.0
}
```

### Créneaux générés
```json
{
  "heure": "08:00",
  "en_pause": false,
  "travail": true
}
```

## 🎨 Interface utilisateur

### Affichage du planning
- **Grille de créneaux** : 6 colonnes par jour (créneaux de 30 min)
- **Couleurs** :
  - 🟢 Vert : Période de travail
  - 🟠 Orange : Pause déjeuner
  - ⚪ Gris : Temps libre
- **Informations** : Heure, statut, durée totale

### Édition du planning
- **Sélection des jours** : Lundi à Samedi
- **Horaires** : Début et fin de journée
- **Pauses** : Début et fin de pause (optionnel)
- **Calcul automatique** : Durée de travail en heures

## 🔧 Configuration

### Horaires par défaut
- **Début** : 8h00
- **Fin** : 17h00
- **Pause** : 12h00 - 13h00 (optionnel)
- **Durée** : 8h00 (7h00 avec pause)

### Créneaux disponibles
- **Période** : 8h00 à 19h00
- **Granularité** : 30 minutes
- **Total** : 22 créneaux par jour

## 📁 Fichiers créés

### Backend
- `src/models/planning.py` : Modèles de données
- `src/routes/planning.py` : Routes API
- `migrate_planning.py` : Script de migration

### Frontend
- `src/components/PlanningAgent.jsx` : Affichage du planning
- `src/components/PlanningEditor.jsx` : Édition du planning
- `src/components/ResponsableDashboard.jsx` : Intégration dans le dashboard

## ✅ Statut

- ✅ Modèles de données créés
- ✅ Routes API implémentées
- ✅ Composants frontend créés
- ✅ Intégration dans le dashboard responsable
- ✅ Migration de la base de données
- ✅ Tests de base effectués

---

**🎉 Le système de planning est maintenant opérationnel !**

Les responsables peuvent maintenant :
- Voir les plannings de tous leurs agents
- Modifier les horaires de travail par jour
- Configurer les pauses déjeuner
- Visualiser les créneaux de 30 minutes

Les agents peuvent :
- Consulter leur planning détaillé
- Voir leurs horaires de travail
- Identifier les périodes de pause


