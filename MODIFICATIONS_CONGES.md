# ✅ Modifications des Calculs de Congés

## 🎯 Objectif

Modifier l'application pour que :
- **Congés Annuels (CA)** : Calculés en **jours** (journée complète ou demi-journée)
- **RTT et Heures Supplémentaires** : Calculés en **heures**

## 🔧 Modifications apportées

### 1. Modèle `DemandeConge` (`src/models/demande_conge.py`)

#### Nouveaux champs
```python
nb_jours = db.Column(db.Float, nullable=False, default=0.0)  # Nombre de jours (pour CA)
nb_heures = db.Column(db.Float, nullable=False, default=0.0)  # Nombre d'heures (pour RTT, HS)
```

#### Nouvelles méthodes
- `calculate_duration()` : Calcule automatiquement la durée selon le type
- `get_duration_display()` : Retourne l'affichage avec les bonnes unités

#### Logique de calcul
```python
# CA : calcul en jours
if type_absence == 'CA':
    if demi_journees == 'matin' or demi_journees == 'après-midi':
        nb_jours = total_days * 0.5  # Demi-journée
    else:
        nb_jours = total_days  # Journée complète
    nb_heures = 0.0

# RTT/HS : calcul en heures  
elif type_absence in ['RTT', 'HS']:
    if demi_journees == 'matin' or demi_journees == 'après-midi':
        nb_heures = total_days * 4.0  # 4h par demi-journée
    else:
        nb_heures = total_days * 8.0  # 8h par journée complète
    nb_jours = 0.0
```

### 2. Modèle `Agent` (`src/models/agent.py`)

#### Commentaires mis à jour
```python
solde_ca = db.Column(db.Float, default=0.0)  # Congés annuels en jours
solde_rtt = db.Column(db.Float, default=0.0)  # RTT en heures
solde_hs = db.Column(db.Float, default=0.0)   # Heures supplémentaires en heures
```

#### Calcul RTT modifié
```python
def calculate_rtt_from_quotite(self):
    # Règles de calcul des RTT selon la quotité (en heures)
    if quotite >= 38:
        return 18 * 8  # 18 RTT * 8h = 144h pour 38h et plus
    elif quotite >= 36:
        return 6 * 8   # 6 RTT * 8h = 48h pour 36h
    # ...
```

#### Nouvelles méthodes
- `get_solde_by_type(type_absence)` : Retourne le solde selon le type
- `get_solde_display(type_absence)` : Retourne l'affichage avec unités

### 3. Script d'initialisation (`init_portable_data.py`)

#### Agents mis à jour
```python
{
    'solde_ca': 25,  # 25 jours de CA
    'solde_hs': 0,   # 0 heures supplémentaires
    'quotite_travail': 38.0  # RTT calculé automatiquement
}
```

#### Demandes d'exemple
```python
# CA : calcul automatique en jours
demande_ca = DemandeConge(
    type_absence='CA',
    demi_journees='journée complète'
)
demande_ca.calculate_duration()  # Calcule automatiquement

# RTT : calcul automatique en heures
demande_rtt = DemandeConge(
    type_absence='RTT', 
    demi_journees='matin'
)
demande_rtt.calculate_duration()  # Calcule automatiquement
```

## 🧪 Tests et validation

### Script de test (`test_calculs_conges.py`)
- Test des calculs CA en jours
- Test des calculs RTT/HS en heures
- Test des demi-journées
- Vérification des affichages

### Script de migration (`migrate_database.py`)
- Recréation des tables avec nouveaux champs
- Réinitialisation des données
- Vérification des calculs

## 📊 Résultats des tests

### Soldes des agents
```
CA: 25.0 jours
RTT: 144 heures (18 RTT × 8h)
HS: 0.0 heures
```

### Exemples de calculs
```
CA 3 jours complets : 3.0 jours, 0.0 heures
CA 1 demi-journée : 0.5 jour, 0.0 heures
RTT 1 jour complet : 0.0 jour, 8.0 heures
RTT 1 demi-journée : 0.0 jour, 4.0 heures
HS 1 demi-journée : 0.0 jour, 4.0 heures
```

## 🎯 Avantages

1. **Conformité RH** : Respect des conventions françaises
2. **Clarté** : Distinction claire jours/heures
3. **Précision** : Calculs exacts selon le type
4. **Automatisation** : Calculs automatiques
5. **Flexibilité** : Gestion des demi-journées

## 📱 Impact sur l'interface

### Affichage des soldes
- **Avant** : "25 heures" (confus)
- **Après** : "25 jours" pour CA, "144 heures" pour RTT

### Création de demandes
- **Calcul automatique** selon le type
- **Affichage adapté** aux unités
- **Validation** des durées

### Liste des demandes
- **Colonne durée** : Unités appropriées
- **Filtres** : Par type d'absence
- **Tri** : Par date, type, durée

## ✅ Statut

- ✅ Modèles modifiés
- ✅ Calculs implémentés
- ✅ Tests validés
- ✅ Migration effectuée
- ✅ Documentation créée
- ✅ Application fonctionnelle

---

**🎉 Les calculs de congés sont maintenant conformes aux standards RH français !**
