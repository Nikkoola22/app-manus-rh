# Guide des Créneaux Matin/Après-midi

## Vue d'ensemble

Le calendrier de présence a été enrichi pour supporter la gestion des créneaux matin et après-midi, permettant une granularité plus fine dans le suivi des présences et absences des agents. Cette fonctionnalité offre une flexibilité maximale pour la gestion des équipes.

## 🎯 Fonctionnalités

### 1. **Gestion Granulaire des Présences**
- ✅ **Créneaux séparés** : Matin et après-midi indépendants
- ✅ **Journée complète** : Option pour les absences sur toute la journée
- ✅ **Flexibilité maximale** : Gestion fine des présences partielles
- ✅ **Cohérence** : Intégration avec les demandes de congés validées

### 2. **Interface Utilisateur Optimisée**
- ✅ **Affichage clair** : Cases séparées pour chaque créneau
- ✅ **Navigation intuitive** : Clic direct sur le créneau souhaité
- ✅ **Indicateurs visuels** : Distinction claire entre les créneaux
- ✅ **Responsive** : Adaptation mobile et desktop

### 3. **Gestion des Données**
- ✅ **Contraintes uniques** : Agent + Date + Créneau
- ✅ **Validation** : Prévention des conflits
- ✅ **Audit trail** : Traçabilité complète
- ✅ **Statistiques** : Métriques détaillées par créneau

## 🏗️ Architecture Technique

### 1. **Modèle de Données Enrichi**

#### **Table `presence` mise à jour**
```sql
CREATE TABLE presence (
    id INTEGER PRIMARY KEY,
    agent_id INTEGER NOT NULL,
    date_presence DATE NOT NULL,
    creneau VARCHAR(10) NOT NULL DEFAULT 'journee',  -- NOUVEAU
    statut VARCHAR(20) NOT NULL,
    motif TEXT,
    heure_debut TIME,
    heure_fin TIME,
    duree_heures REAL,
    date_creation DATETIME,
    cree_par INTEGER NOT NULL,
    UNIQUE(agent_id, date_presence, creneau)  -- MISE À JOUR
);
```

#### **Types de créneaux**
- **`matin`** : Créneau matinal (ex: 8h-12h)
- **`apres_midi`** : Créneau après-midi (ex: 13h-17h)
- **`journee`** : Journée complète (pour les demandes de congés)

### 2. **API REST Adaptée**

#### **Endpoints modifiés**
```python
POST /api/presence
# Nouveau champ requis : creneau

PUT /api/presence/{id}
# Support de la modification du créneau

GET /api/presence/calendrier/semaine/{semaine}
# Structure de réponse adaptée pour les créneaux
```

#### **Structure de réponse du calendrier**
```json
{
  "agents": [
    {
      "id": 1,
      "nom": "Dupont Jean",
      "jours": {
        "2024-04-15": {
          "matin": {
            "presence": { "statut": "present", "creneau": "matin" },
            "statut": "present"
          },
          "apres_midi": {
            "presence": { "statut": "absent", "creneau": "apres_midi" },
            "statut": "absent"
          }
        }
      }
    }
  ]
}
```

### 3. **Composant React Redesigné**

#### **Structure du tableau**
```jsx
<thead>
  <tr>
    <th>Agent</th>
    <th>Lun 15</th>  {/* Matin / Après-midi */}
    <th>Mar 16</th>
    {/* ... */}
  </tr>
</thead>
<tbody>
  {agents.map(agent => (
    <tr>
      <td>{agent.nom}</td>
      <td>
        <div className="space-y-1">
          {/* Créneau Matin */}
          <div className="h-8">
            {presence.matin ? <Badge>Présent</Badge> : <Button>+</Button>}
          </div>
          {/* Créneau Après-midi */}
          <div className="h-8">
            {presence.apres_midi ? <Badge>Absent</Badge> : <Button>+</Button>}
          </div>
        </div>
      </td>
    </tr>
  ))}
</tbody>
```

## 🎨 Interface Utilisateur

### 1. **Affichage du Calendrier**

#### **Structure du tableau**
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Agent       │ Lun 15      │ Mar 16      │ Mer 17      │
├─────────────┼─────────────┼─────────────┼─────────────┤
│             │ Matin       │ Matin       │ Matin       │
│ Dupont Jean │ Après-midi  │ Après-midi  │ Après-midi  │
├─────────────┼─────────────┼─────────────┼─────────────┤
│             │ [Présent]   │ [Absent]    │ [Congés ✓]  │
│ Martin Paul │ [Absent]    │ [Présent]   │ [Congés ✓]  │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

#### **Cases interactives**
- **Case vide** : Bouton "+" pour ajouter une présence
- **Case remplie** : Badge avec statut et bouton d'édition
- **Demandes validées** : Affichage automatique sur les deux créneaux

### 2. **Formulaire de Présence**

#### **Champs du formulaire**
```
┌─────────────────────────────────────────────────────────┐
│ Date          │ Créneau        │ Statut                 │
├─────────────────────────────────────────────────────────┤
│ 2024-04-15    │ Matin          │ Présent                │
│               │ Après-midi     │ Absent                 │
│               │ Journée        │ Congés                 │
└─────────────────────────────────────────────────────────┘
```

#### **Heures automatiques**
- **Matin** : 08:00 - 12:00 (par défaut)
- **Après-midi** : 13:00 - 17:00 (par défaut)
- **Journée** : 08:00 - 17:00 (par défaut)

### 3. **Indicateurs Visuels**

#### **Couleurs par créneau**
- **Matin** : Bleu clair (`bg-blue-50`)
- **Après-midi** : Vert clair (`bg-green-50`)
- **Journée** : Gris clair (`bg-gray-50`)

#### **Badges de statut**
- **Présent** : Vert
- **Absent** : Rouge
- **Congés** : Bleu
- **Maladie** : Orange
- **RTT** : Violet
- **Partiel** : Jaune

## 📱 Utilisation

### Pour les Responsables :

#### 1. **Ajouter une Présence**
1. Cliquer sur le bouton "+" dans le créneau souhaité
2. Remplir le formulaire :
   - **Date** : Automatiquement remplie
   - **Créneau** : Matin/Après-midi/Journée
   - **Statut** : Présent/Absent/Congés/etc.
   - **Heures** : Pour les présences partielles
   - **Motif** : Description optionnelle
3. Sauvegarder

#### 2. **Modifier une Présence**
1. Cliquer sur le badge de présence existant
2. Modifier les informations souhaitées
3. Sauvegarder

#### 3. **Gérer les Demandes de Congés**
- Les demandes validées s'affichent automatiquement sur les deux créneaux
- Impossible de les modifier directement (lecture seule)
- Distinction visuelle avec la marque ✓

### Scénarios d'Usage :

#### **Scénario 1 : Présence partielle**
```
Agent présent le matin, absent l'après-midi (RDV médical)
- Matin : Présent ✓
- Après-midi : Absent (RDV médical)
```

#### **Scénario 2 : Congés validés**
```
Demande de congés approuvée pour toute la journée
- Matin : Congés ✓ (automatique)
- Après-midi : Congés ✓ (automatique)
```

#### **Scénario 3 : Présence normale**
```
Agent présent toute la journée
- Matin : Présent
- Après-midi : Présent
```

## 🔧 Configuration et Personnalisation

### 1. **Horaires par Défaut**
```javascript
const horaires_par_defaut = {
  matin: { debut: '08:00', fin: '12:00' },
  apres_midi: { debut: '13:00', fin: '17:00' },
  journee: { debut: '08:00', fin: '17:00' }
}
```

### 2. **Couleurs Personnalisables**
```css
/* Créneaux */
.creneau-matin { @apply bg-blue-50 border-blue-200; }
.creneau-apres-midi { @apply bg-green-50 border-green-200; }
.creneau-journee { @apply bg-gray-50 border-gray-200; }

/* Statuts */
.statut-present { @apply bg-green-100 text-green-800; }
.statut-absent { @apply bg-red-100 text-red-800; }
/* ... */
```

### 3. **Validation des Données**
```python
def validate_presence(data):
    # Vérifier que le créneau est valide
    if data['creneau'] not in ['matin', 'apres_midi', 'journee']:
        raise ValueError('Créneau invalide')
    
    # Vérifier la cohérence des heures
    if data['heure_debut'] and data['heure_fin']:
        if data['heure_debut'] >= data['heure_fin']:
            raise ValueError('Heure de début doit être avant heure de fin')
```

## 📊 Statistiques et Rapports

### 1. **Métriques par Créneau**
- **Présences matin** : Nombre d'agents présents le matin
- **Présences après-midi** : Nombre d'agents présents l'après-midi
- **Présences complètes** : Agents présents toute la journée
- **Absences partielles** : Agents présents seulement un créneau

### 2. **Calculs Automatiques**
```python
def calculer_statistiques_creneaux(agents, semaine):
    stats = {
        'matin': {'present': 0, 'absent': 0},
        'apres_midi': {'present': 0, 'absent': 0},
        'journee_complete': 0,
        'presence_partielle': 0
    }
    
    for agent in agents:
        for jour in semaine:
            matin = agent.jours[jour]['matin']
            apres_midi = agent.jours[jour]['apres_midi']
            
            # Compter les présences par créneau
            if matin['statut'] == 'present':
                stats['matin']['present'] += 1
            if apres_midi['statut'] == 'present':
                stats['apres_midi']['present'] += 1
            
            # Journée complète
            if matin['statut'] == 'present' and apres_midi['statut'] == 'present':
                stats['journee_complete'] += 1
            
            # Présence partielle
            if (matin['statut'] == 'present' and apres_midi['statut'] == 'absent') or \
               (matin['statut'] == 'absent' and apres_midi['statut'] == 'present'):
                stats['presence_partielle'] += 1
    
    return stats
```

### 3. **Rapports Détaillés**
- **Par agent** : Historique des créneaux
- **Par service** : Statistiques consolidées
- **Par période** : Évolution dans le temps
- **Par type d'absence** : Répartition des absences

## 🔒 Sécurité et Intégrité

### 1. **Contraintes de Données**
- **Unicité** : Agent + Date + Créneau unique
- **Cohérence** : Validation des heures
- **Intégrité** : Contrôles de référence

### 2. **Permissions**
- **Responsables** : Création/modification pour leur service
- **Administrateurs** : Accès global
- **Agents** : Lecture seule de leurs données

### 3. **Audit Trail**
- **Création** : Qui a créé, quand
- **Modification** : Historique des changements
- **Suppression** : Traçabilité des suppressions

## 🚀 Avantages

### 1. **Pour les Responsables**
- ✅ **Précision** : Gestion fine des présences
- ✅ **Flexibilité** : Adaptation aux besoins réels
- ✅ **Visibilité** : Vue claire des créneaux
- ✅ **Efficacité** : Saisie rapide et intuitive

### 2. **Pour l'Organisation**
- ✅ **Données précises** : Informations détaillées
- ✅ **Conformité** : Respect des réglementations
- ✅ **Optimisation** : Meilleure gestion des ressources
- ✅ **Reporting** : Analyses approfondies

### 3. **Pour les Agents**
- ✅ **Transparence** : Visibilité sur leurs créneaux
- ✅ **Flexibilité** : Gestion des présences partielles
- ✅ **Planification** : Anticipation des absences
- ✅ **Équité** : Gestion uniforme et juste

## 📈 Évolutions Futures

### 1. **Fonctionnalités Avancées**
- **Créneaux personnalisés** : Définition d'horaires spécifiques
- **Notifications** : Alertes pour les changements
- **Planification** : Gestion des plannings
- **Intégration** : Synchronisation avec d'autres systèmes

### 2. **Améliorations UX**
- **Drag & Drop** : Modification par glisser-déposer
- **Raccourcis** : Saisie rapide avec touches
- **Thèmes** : Personnalisation visuelle
- **Mobile** : Application native

### 3. **Analytics Avancés**
- **Prédictions** : IA pour l'anticipation
- **Optimisation** : Suggestions automatiques
- **Benchmarking** : Comparaisons inter-services
- **Tableaux de bord** : KPIs en temps réel

La gestion des créneaux matin/après-midi transforme le calendrier de présence en un outil de gestion RH de nouvelle génération, offrant la précision et la flexibilité nécessaires pour une gestion moderne des équipes.




