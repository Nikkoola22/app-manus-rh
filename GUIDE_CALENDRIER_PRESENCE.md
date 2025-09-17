# Guide du Calendrier de Présence

## Vue d'ensemble

Le calendrier de présence est une fonctionnalité dédiée aux responsables de service qui leur permet de visualiser et gérer la présence de tous les agents de leur service sur une base hebdomadaire. Il offre une vue d'ensemble claire et permet une gestion efficace des absences et présences.

## 🎯 Fonctionnalités Principales

### 1. **Calendrier Hebdomadaire**
- ✅ **Vue par semaine** : Affichage du lundi au dimanche
- ✅ **Navigation fluide** : Boutons semaine précédente/suivante
- ✅ **Retour à aujourd'hui** : Bouton pour revenir à la semaine courante
- ✅ **Vue claire** : Chaque agent avec sa présence/absence par jour

### 2. **Gestion des Présences**
- ✅ **Statuts multiples** : Présent, Absent, Congés, Maladie, RTT, Présence partielle
- ✅ **Création facile** : Clic sur une case vide pour ajouter une présence
- ✅ **Modification rapide** : Clic sur une présence existante pour la modifier
- ✅ **Suppression** : Possibilité de supprimer une entrée
- ✅ **Heures personnalisées** : Pour les présences partielles

### 3. **Statistiques en Temps Réel**
- ✅ **Métriques clés** : Nombre d'agents, pourcentage de présence, total d'entrées
- ✅ **Calculs automatiques** : Statistiques mises à jour en temps réel
- ✅ **Vue d'ensemble** : Indicateurs visuels avec couleurs

### 4. **Interface Moderne**
- ✅ **Design cohérent** : Style moderne avec glassmorphism
- ✅ **Responsive** : Adaptation mobile et desktop
- ✅ **Animations fluides** : Transitions et effets hover
- ✅ **Légende claire** : Codes couleur pour chaque statut

## 🏗️ Architecture Technique

### 1. **Modèle de Données**

#### Table `presence`
```sql
CREATE TABLE presence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL,
    date_presence DATE NOT NULL,
    statut VARCHAR(20) NOT NULL,
    motif TEXT,
    heure_debut TIME,
    heure_fin TIME,
    duree_heures REAL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    cree_par INTEGER NOT NULL,
    FOREIGN KEY (agent_id) REFERENCES agent (id),
    FOREIGN KEY (cree_par) REFERENCES agent (id),
    UNIQUE(agent_id, date_presence)
);
```

#### Champs principaux :
- **agent_id** : Référence vers l'agent
- **date_presence** : Date de la présence/absence
- **statut** : Type de présence (present, absent, conges, maladie, rtt, partiel)
- **motif** : Description optionnelle
- **heure_debut/heure_fin** : Pour les présences partielles
- **duree_heures** : Calculée automatiquement
- **cree_par** : Qui a créé l'entrée (audit trail)

### 2. **API REST**

#### Endpoints principaux :
```python
GET /api/presence/calendrier/semaine/{semaine}     # Calendrier hebdomadaire
GET /api/presence/statistiques/semaine/{semaine}   # Statistiques
POST /api/presence                                  # Créer une présence
PUT /api/presence/{id}                             # Modifier une présence
DELETE /api/presence/{id}                          # Supprimer une présence
```

#### Format de semaine :
- **Format** : `YYYY-WW` (ex: `2024-15`)
- **Calcul** : Semaine ISO (lundi = premier jour)
- **Navigation** : Gestion automatique des années

### 3. **Composant React**

#### Structure du composant Calendar :
```jsx
const Calendar = ({ user }) => {
  // États
  const [currentSemaine, setCurrentSemaine] = useState('')
  const [calendrierData, setCalendrierData] = useState(null)
  const [statistiques, setStatistiques] = useState(null)
  
  // Fonctions principales
  const fetchCalendrier = async (semaine) => { ... }
  const handleSemaineChange = (direction) => { ... }
  const handleAddPresence = (agentId, date) => { ... }
  const handleEditPresence = (presence) => { ... }
}
```

## 🎨 Interface Utilisateur

### 1. **Header avec Navigation**
```
┌─────────────────────────────────────────────────────────────┐
│ 📅 Calendrier de présence - Semaine 2024-15                │
│ lun 08 avr - dim 14 avr                                    │
│                                                             │
│ [← Semaine précédente] [Aujourd'hui] [Semaine suivante →]  │
└─────────────────────────────────────────────────────────────┘
```

### 2. **Statistiques**
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 👥 Agents   │ 📈 Présence │ 📅 Total    │ 🗓️ Jours    │
│      5      │      85%    │     23      │     35      │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### 3. **Tableau du Calendrier**
```
┌─────────────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ Agent       │ Lun │ Mar │ Mer │ Jeu │ Ven │ Sam │ Dim │
├─────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ Dupont Jean │ ✅  │ ✅  │ ❌  │ ✅  │ ✅  │     │     │
│ Martin Paul │ 🏥  │ 🏥  │ 🏥  │ ✅  │ ✅  │     │     │
│ Durand Anne │ ✅  │ ✅  │ ✅  │ ✅  │ ✅  │     │     │
└─────────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
```

### 4. **Légende des Statuts**
- 🟢 **Présent** : Agent présent toute la journée
- 🔴 **Absent** : Agent absent sans motif
- 🔵 **Congés** : Congés payés
- 🟠 **Maladie** : Arrêt maladie
- 🟣 **RTT** : Jour de RTT
- 🟡 **Partiel** : Présence partielle (avec heures)

## 📱 Utilisation

### Pour les Responsables :

#### 1. **Accéder au Calendrier**
1. Se connecter en tant que responsable
2. Aller dans l'onglet "Calendrier" du dashboard
3. Le calendrier affiche automatiquement la semaine courante

#### 2. **Naviguer dans le Temps**
- **Semaine précédente** : Bouton ←
- **Semaine suivante** : Bouton →
- **Retour à aujourd'hui** : Bouton "Aujourd'hui"

#### 3. **Ajouter une Présence**
1. Cliquer sur une case vide (bouton +)
2. Remplir le formulaire :
   - Date (pré-remplie)
   - Statut (présent, absent, congés, etc.)
   - Heures (pour présence partielle)
   - Motif (optionnel)
3. Sauvegarder

#### 4. **Modifier une Présence**
1. Cliquer sur une présence existante
2. Modifier les informations
3. Sauvegarder

#### 5. **Supprimer une Présence**
1. Cliquer sur une présence existante
2. Cliquer sur le bouton de suppression
3. Confirmer

### Pour les Administrateurs :

#### 1. **Accès Global**
- Les administrateurs voient tous les agents de tous les services
- Même interface que les responsables
- Permissions étendues

#### 2. **Gestion Multi-Services**
- Possibilité de gérer plusieurs services
- Vue d'ensemble globale
- Statistiques consolidées

## 🔧 Configuration et Personnalisation

### 1. **Statuts Personnalisés**
Les statuts sont définis dans le modèle `Presence` :
```python
def get_statut_color(self):
    colors = {
        'present': 'green',
        'absent': 'red', 
        'conges': 'blue',
        'maladie': 'orange',
        'rtt': 'purple',
        'partiel': 'yellow'
    }
    return colors.get(self.statut, 'gray')
```

### 2. **Couleurs et Thème**
Les couleurs sont définies dans le composant React :
```jsx
const getStatutColor = (statut) => {
  const colors = {
    present: 'bg-green-100 text-green-800 border-green-200',
    absent: 'bg-red-100 text-red-800 border-red-200',
    // ...
  }
  return colors[statut] || 'bg-gray-100 text-gray-800 border-gray-200'
}
```

### 3. **Calculs Automatiques**
- **Durée** : Calculée automatiquement pour les présences partielles
- **Statistiques** : Mises à jour en temps réel
- **Pourcentages** : Calculés selon le nombre d'agents et de jours

## 📊 Rapports et Statistiques

### 1. **Métriques Disponibles**
- **Total agents** : Nombre d'agents dans le service
- **Pourcentage présence** : Ratio présences / jours possibles
- **Présences totales** : Nombre total d'entrées
- **Jours possibles** : Agents × 7 jours

### 2. **Détail par Statut**
- Comptage automatique par type de présence
- Répartition visuelle avec codes couleur
- Historique par semaine

### 3. **Évolutions Futures**
- Export Excel/PDF
- Graphiques d'évolution
- Alertes d'absence
- Intégration avec planning

## 🚀 Avantages

### 1. **Pour les Responsables**
- ✅ **Vue d'ensemble** : Tous les agents en un coup d'œil
- ✅ **Gestion simple** : Interface intuitive
- ✅ **Temps réel** : Mise à jour instantanée
- ✅ **Mobile** : Accessible sur tous les appareils

### 2. **Pour l'Organisation**
- ✅ **Traçabilité** : Historique complet des présences
- ✅ **Conformité** : Respect des réglementations
- ✅ **Efficacité** : Réduction du temps de gestion
- ✅ **Données** : Base pour les analyses RH

### 3. **Pour les Agents**
- ✅ **Transparence** : Visibilité sur les absences
- ✅ **Planification** : Anticipation des congés
- ✅ **Équité** : Gestion uniforme des présences

## 🔒 Sécurité et Permissions

### 1. **Contrôle d'Accès**
- **Responsables** : Seulement leur service
- **Administrateurs** : Tous les services
- **Agents** : Lecture seule de leurs données

### 2. **Audit Trail**
- Traçabilité de qui a créé/modifié
- Horodatage des modifications
- Historique des changements

### 3. **Validation des Données**
- Contrôles de cohérence
- Prévention des doublons
- Validation des dates/heures

## 📈 Évolutions Futures

### 1. **Fonctionnalités Avancées**
- **Planification** : Gestion des plannings
- **Notifications** : Alertes automatiques
- **Intégration** : Systèmes RH externes
- **Rapports** : Exports personnalisés

### 2. **Améliorations UX**
- **Drag & Drop** : Modification par glisser-déposer
- **Recherche** : Filtres avancés
- **Thèmes** : Personnalisation visuelle
- **Mobile** : Application native

### 3. **Analytics**
- **Tableaux de bord** : KPIs avancés
- **Prédictions** : IA pour l'anticipation
- **Benchmarking** : Comparaisons inter-services
- **Optimisation** : Suggestions automatiques

Le calendrier de présence transforme la gestion RH en offrant une solution moderne, intuitive et complète pour le suivi des équipes. Il s'intègre parfaitement dans l'écosystème existant tout en apportant une valeur ajoutée significative aux responsables et à l'organisation.




