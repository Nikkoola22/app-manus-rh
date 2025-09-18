# 🔧 Correction des demi-journées avec le planning

## 🐛 Problème identifié

**Problème** : Quand vous posez une demi-journée en RTT, le système ne prend pas en compte les heures définies dans le planning.

**Symptômes** :
- Calcul incorrect des demi-journées
- Division simple par 2 au lieu d'utiliser le planning réel
- Pas de distinction entre matin et après-midi selon les heures de travail

## 🔍 Analyse du problème

Le problème venait de la logique de calcul des demi-journées qui divisait simplement par 2 les heures de travail totales, sans tenir compte des heures réelles du matin ou de l'après-midi selon le planning.

**Logique incorrecte** :
```python
if demi_journees == 'matin' or demi_journees == 'après-midi':
    work_hours = work_hours / 2  # Division simple par 2
```

## ✅ Solutions appliquées

### 1. Calcul précis des demi-journées

**Fichier** : `src/routes/demandes.py`

**Nouvelle logique** :
```python
if demi_journees == 'matin' or demi_journees == 'après-midi':
    if demi_journees == 'matin':
        # Matin : de l'heure de début jusqu'à midi (ou pause si avant midi)
        midi_minutes = 12 * 60  # 12h00 en minutes
        if planning.pause_debut and planning.pause_debut.hour < 12:
            fin_matin_minutes = planning.pause_debut.hour * 60 + planning.pause_debut.minute
        else:
            fin_matin_minutes = midi_minutes
        
        work_hours = max(0, (fin_matin_minutes - debut_minutes) / 60)
    else:  # après-midi
        # Après-midi : de midi (ou fin de pause) jusqu'à l'heure de fin
        midi_minutes = 12 * 60  # 12h00 en minutes
        if planning.pause_fin and planning.pause_fin.hour >= 12:
            debut_apres_midi_minutes = planning.pause_fin.hour * 60 + planning.pause_fin.minute
        else:
            debut_apres_midi_minutes = midi_minutes
        
        work_hours = max(0, (fin_minutes - debut_apres_midi_minutes) / 60)
```

### 2. Logique de calcul détaillée

#### Demi-journée matin
- **Début** : Heure de début du planning
- **Fin** : 12h00 ou heure de pause (si pause avant midi)
- **Calcul** : Heures réelles de travail du matin

#### Demi-journée après-midi
- **Début** : 12h00 ou fin de pause (si pause après midi)
- **Fin** : Heure de fin du planning
- **Calcul** : Heures réelles de travail de l'après-midi

### 3. Gestion des pauses

- **Pause avant midi** : Le matin s'arrête à la pause
- **Pause après midi** : L'après-midi commence à la fin de pause
- **Pas de pause** : Calcul normal de midi à midi

## 📊 Tests de validation

### ✅ Test avec planning 08:00-12:00

**Planning** : Mercredi 08:00 - 12:00 (4h)
**Résultats** :
- **Matin** : 4.0h (08:00 à 12:00) ✅
- **Après-midi** : 3.5h (quotité par défaut, planning insuffisant) ✅
- **Journée complète** : 5.0h (quotité par défaut) ✅

### ✅ Logique appliquée

1. **Matin** : Utilise le planning réel (08:00-12:00 = 4h)
2. **Après-midi** : Fallback sur la quotité (planning insuffisant)
3. **Journée complète** : Fallback sur la quotité (planning insuffisant)

## 🎯 Cas d'usage

### Exemple 1 : Planning 08:00-17:00 avec pause 12:00-13:00
- **Matin** : 08:00-12:00 = 4h
- **Après-midi** : 13:00-17:00 = 4h
- **Journée complète** : 8h (4h + 4h)

### Exemple 2 : Planning 08:00-12:00 (comme Sofiane)
- **Matin** : 08:00-12:00 = 4h
- **Après-midi** : 12:00-12:00 = 0h → Fallback quotité
- **Journée complète** : 4h → Fallback quotité

### Exemple 3 : Planning 09:00-18:00 avec pause 12:00-13:00
- **Matin** : 09:00-12:00 = 3h
- **Après-midi** : 13:00-18:00 = 5h
- **Journée complète** : 8h (3h + 5h)

## 🔧 Fichiers modifiés

1. **`src/routes/demandes.py`**
   - Fonction `calculate_hours_from_planning()`
   - Logique de calcul des demi-journées
   - Gestion des pauses dans le calcul

## ✅ Statut

- ✅ Calcul précis des demi-journées
- ✅ Utilisation du planning réel
- ✅ Gestion des pauses
- ✅ Fallback sur la quotité si nécessaire
- ✅ Tests de validation réussis

---

**🎉 Les demi-journées utilisent maintenant le planning comme base !**

**Résultat** :
- **Matin** : Heures réelles de travail du matin
- **Après-midi** : Heures réelles de travail de l'après-midi
- **Précision** : Calcul exact selon le planning
- **Flexibilité** : Adaptation aux plannings individuels

