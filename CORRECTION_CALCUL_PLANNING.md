# 🔧 Correction du calcul des heures basé sur le planning

## 🐛 Problème identifié

**Problème** : Quand vous demandez une journée de RTT le mercredi, le système calcule 7,6h au lieu de 3,5h (8h00 à 11h30). Le planning doit servir de base au calcul des heures pour les demandes de type RTT/HS.

**Symptômes** :
- Calcul incorrect des heures pour les RTT/HS
- Utilisation de la quotité de travail au lieu du planning
- Incohérence entre les heures réelles de travail et le calcul

## 🔍 Analyse du problème

Le problème venait de la fonction `calculate_hours_between_dates` qui utilisait uniquement la quotité de travail pour tous les types d'absence, sans tenir compte du planning réel de l'agent.

**Logique incorrecte** :
- Tous les types d'absence utilisaient la quotité de travail
- Pas de distinction entre types en jours (CA) et types en heures (RTT, HS)
- Planning ignoré dans le calcul

## ✅ Solutions appliquées

### 1. Création d'une nouvelle fonction de calcul

**Fichier** : `src/routes/demandes.py`

**Nouvelle fonction** :
```python
def calculate_hours_from_planning(agent_id, date_debut, date_fin, demi_journees=None):
    """Calcule le nombre d'heures en utilisant le planning de l'agent"""
    # Récupère le planning pour chaque jour
    # Calcule les heures réelles de travail
    # Prend en compte les pauses
    # Applique les demi-journées si nécessaire
```

**Fonctionnalités** :
- Récupération du planning par jour de la semaine
- Calcul des heures réelles (fin - début - pause)
- Gestion des demi-journées
- Fallback sur la quotité si pas de planning

### 2. Modification de la logique de calcul

**Fichier** : `src/routes/demandes.py`

**Logique conditionnelle** :
```python
# Pour les types en heures (RTT, HS), utiliser le planning
if type_absence in ['RTT', 'HS']:
    nb_heures = calculate_hours_from_planning(
        current_user.id,
        date_debut, 
        date_fin, 
        data.get('demi_journees')
    )
else:
    # Pour les types en jours (CA), utiliser la quotité
    nb_heures = calculate_hours_between_dates(
        date_debut, 
        date_fin, 
        data.get('demi_journees'),
        current_user.quotite_travail or 35
    )
```

### 3. Calcul détaillé des heures

**Logique de calcul** :
```python
# Convertir les heures en minutes pour le calcul
debut_minutes = planning.heure_debut.hour * 60 + planning.heure_debut.minute
fin_minutes = planning.heure_fin.hour * 60 + planning.heure_fin.minute

# Soustraire la pause si elle existe
if planning.pause_debut and planning.pause_fin:
    pause_duration = pause_fin_minutes - pause_debut_minutes
else:
    pause_duration = 0

# Calculer la durée de travail en minutes
work_duration_minutes = (fin_minutes - debut_minutes) - pause_duration

# Convertir en heures
work_hours = work_duration_minutes / 60
```

## 📊 Règles de calcul appliquées

### Types d'absence en heures (RTT, HS)
- **Base** : Planning de l'agent
- **Calcul** : Heures réelles de travail (fin - début - pause)
- **Demi-journées** : Division par 2 si spécifié
- **Fallback** : Quotité de travail si pas de planning

### Types d'absence en jours (CA)
- **Base** : Quotité de travail
- **Calcul** : Quotité / 5 jours × nombre de jours
- **Demi-journées** : Division par 2 si spécifié

## ✅ Tests de validation

### ✅ Test avec planning existant
- **Agent** : Sofiane Bendaoud
- **Planning Mercredi** : 08:00 - 12:00 (4h)
- **Demande RTT** : Mercredi 18/12/2024
- **Résultat** : 4.0h (au lieu de 7.6h)
- **Statut** : ✅ Calcul correct basé sur le planning

### ✅ Comparaison avant/après
- **Avant** : 7.6h (quotité 38h / 5 jours)
- **Après** : 4.0h (planning réel 08:00-12:00)
- **Amélioration** : Précision du calcul

## 🔧 Fichiers modifiés

1. **`src/routes/demandes.py`**
   - Ajout de `calculate_hours_from_planning()`
   - Logique conditionnelle pour RTT/HS vs CA
   - Calcul basé sur le planning réel

## 📝 Exemples de calcul

### Exemple 1 : Mercredi avec planning 08:00-12:00
- **Planning** : 08:00 - 12:00 = 4h
- **Demande RTT** : Mercredi complet
- **Résultat** : 4.0h

### Exemple 2 : Mercredi avec planning 08:00-11:30
- **Planning** : 08:00 - 11:30 = 3.5h
- **Demande RTT** : Mercredi complet
- **Résultat** : 3.5h

### Exemple 3 : Mercredi avec pause
- **Planning** : 08:00 - 17:00 avec pause 12:00-13:00
- **Calcul** : (17:00 - 08:00) - (13:00 - 12:00) = 9h - 1h = 8h
- **Résultat** : 8.0h

## ✅ Statut

- ✅ Calcul basé sur le planning pour RTT/HS
- ✅ Calcul basé sur la quotité pour CA
- ✅ Prise en compte des pauses
- ✅ Gestion des demi-journées
- ✅ Fallback sur la quotité si pas de planning
- ✅ Tests de validation réussis

---

**🎉 Le calcul des heures utilise maintenant le planning comme base !**

**Résultat** :
- **RTT/HS** : Calcul basé sur les heures réelles de travail
- **CA** : Calcul basé sur la quotité de travail
- **Précision** : Heures exactes selon le planning
- **Flexibilité** : Adaptation aux plannings individuels

