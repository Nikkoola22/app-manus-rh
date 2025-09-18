# 📊 Guide des Unités de Calcul des Congés

## 🎯 Principe général

L'application distingue maintenant clairement les **congés en jours** et les **congés en heures** selon leur nature :

### 📅 Congés calculés en JOURS
- **Congés Annuels (CA)** : 1 jour = 1 journée complète ou 0.5 jour = 1 demi-journée
- **Jours de Sujétions** : 1 jour = 1 journée complète ou 0.5 jour = 1 demi-journée  
- **Congés Formations** : 1 jour = 1 journée complète ou 0.5 jour = 1 demi-journée

### ⏰ Congés calculés en HEURES
- **RTT (Récupération du Temps de Travail)** : 1 journée = 8h, 1 demi-journée = 4h
- **Heures Supplémentaires (HS)** : 1 journée = 8h, 1 demi-journée = 4h
- **CET (Compte Épargne Temps)** : 1 journée = 8h, 1 demi-journée = 4h
- **Bonifications** : 1 journée = 8h, 1 demi-journée = 4h

## 🔢 Calculs automatiques

### Pour les Congés Annuels (CA)
```
Journée complète : 1 jour
Demi-journée (matin) : 0.5 jour
Demi-journée (après-midi) : 0.5 jour
Période de 3 jours complètes : 3 jours
Période de 2 jours + 1 demi-journée : 2.5 jours
```

### Pour les RTT et Heures Supplémentaires
```
Journée complète : 8 heures
Demi-journée (matin) : 4 heures
Demi-journée (après-midi) : 4 heures
Période de 2 jours complètes : 16 heures
Période de 1 jour + 1 demi-journée : 12 heures
```

## 📋 Exemples concrets

### Exemple 1 : Demande de CA
- **Type** : Congés Annuels (CA)
- **Période** : 15 au 17 janvier (3 jours)
- **Demi-journées** : Journée complète
- **Résultat** : 3 jours de CA

### Exemple 2 : Demande de CA demi-journée
- **Type** : Congés Annuels (CA)
- **Période** : 20 janvier (1 jour)
- **Demi-journées** : Matin
- **Résultat** : 0.5 jour de CA

### Exemple 3 : Demande de RTT
- **Type** : RTT
- **Période** : 25 janvier (1 jour)
- **Demi-journées** : Journée complète
- **Résultat** : 8 heures de RTT

### Exemple 4 : Demande de RTT demi-journée
- **Type** : RTT
- **Période** : 30 janvier (1 jour)
- **Demi-journées** : Après-midi
- **Résultat** : 4 heures de RTT

### Exemple 5 : Heures supplémentaires
- **Type** : Heures Supplémentaires (HS)
- **Période** : 5 février (1 jour)
- **Demi-journées** : Matin
- **Résultat** : 4 heures de HS

## 🏢 Soldes des agents

### Affichage des soldes
- **CA** : "25 jours" (au lieu de "25 heures")
- **RTT** : "144 heures" (18 RTT × 8h = 144h)
- **HS** : "0 heures"

### Calcul automatique des RTT
Les RTT sont calculés automatiquement selon la quotité de travail :
- **38h et plus** : 18 RTT = 144 heures
- **36h** : 6 RTT = 48 heures  
- **35h** : 0 RTT = 0 heures
- **Moins de 35h** : 0 RTT = 0 heures

## 🔄 Migration des données

### Changements apportés
1. **Nouveau champ** : `nb_jours` dans la table `demande_conge`
2. **Modification** : `nb_heures` maintenant spécifique aux RTT/HS
3. **Calcul automatique** : Durée calculée selon le type d'absence
4. **Affichage** : Unités adaptées au type de congé

### Compatibilité
- Les anciennes données sont automatiquement migrées
- Les calculs sont rétrocompatibles
- L'interface s'adapte automatiquement

## 🧪 Tests et validation

### Script de test
```bash
python3 test_calculs_conges.py
```

### Vérifications
- ✅ CA calculé en jours
- ✅ RTT calculé en heures  
- ✅ HS calculé en heures
- ✅ Demi-journées correctement gérées
- ✅ Affichage des unités appropriées

## 📱 Interface utilisateur

### Création de demande
- **Type CA** : Affichage en jours
- **Type RTT/HS** : Affichage en heures
- **Calcul automatique** : Selon la période et demi-journées

### Liste des demandes
- **Colonne durée** : Unités adaptées au type
- **Filtres** : Par type d'absence
- **Tri** : Par date, type, durée

### Soldes des agents
- **CA** : "X jours"
- **RTT** : "X heures" 
- **HS** : "X heures"

## 🎯 Avantages

1. **Clarté** : Distinction claire entre jours et heures
2. **Conformité** : Respect des conventions RH
3. **Précision** : Calculs exacts selon le type
4. **Flexibilité** : Gestion des demi-journées
5. **Automatisation** : Calculs automatiques

---

**📝 Note** : Cette modification améliore la précision et la conformité de l'application avec les standards RH français.

