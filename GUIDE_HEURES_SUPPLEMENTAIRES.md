# Guide des Heures Supplémentaires (HS)

## Vue d'ensemble

Les heures supplémentaires (HS) sont maintenant disponibles dans l'application de gestion des congés. Cette fonctionnalité permet aux agents d'utiliser leurs heures supplémentaires comme un type de congé supplémentaire.

## Nouvelles fonctionnalités

### 1. Champ solde_hs dans le modèle Agent

- **Nouveau champ** : `solde_hs` (Float, défaut 0.0)
- **Description** : Stocke le nombre d'heures supplémentaires disponibles pour l'agent
- **Migration** : Le champ a été ajouté automatiquement à la base de données

### 2. Menu déroulant des types d'absence

Dans le formulaire de demande de congés, les agents peuvent maintenant sélectionner :
- **"Heures Supplémentaires"** comme type d'absence
- Le solde HS disponible s'affiche automatiquement

### 3. Administration des HS

#### Dans l'AdminDashboard :
- **Nouveau champ** : "Solde HS (heures)" dans le formulaire de création/modification d'agent
- **Tableau des agents** : Nouvelle colonne "HS" affichant le solde
- **Informations complètes** : Date d'entrée, année d'entrée FP, date de fin de contrat

#### Champs ajoutés au formulaire admin :
- Date d'entrée
- Année d'entrée FP  
- Date de fin de contrat
- Solde Bonifications
- Solde Jours de sujétions
- Solde Congés formations
- **Solde HS (nouveau)**

### 4. Affichage dans les dashboards

#### AgentDashboard :
- **Nouvelle carte** : "Heures Supplémentaires" avec le solde disponible
- **Historique des mouvements** : Les demandes HS apparaissent dans l'historique
- **Calculs automatiques** : Solde avant/après pour les HS

#### AgentProfile :
- **Section "Informations de travail"** : Affichage du solde HS
- **Tableau "Droits totaux accordés"** : Ligne dédiée aux HS
- **Historique des mouvements** : Suivi des demandes HS

## Utilisation

### Pour les agents :

1. **Voir le solde HS** :
   - Dans le dashboard personnel, carte "Heures Supplémentaires"
   - Dans l'historique des mouvements

2. **Faire une demande avec des HS** :
   - Cliquer sur "Nouvelle demande de congé"
   - Sélectionner "Heures Supplémentaires" dans le menu déroulant
   - Le solde disponible s'affiche automatiquement
   - Remplir les dates et motifs comme pour les autres types

### Pour les administrateurs :

1. **Modifier le solde HS d'un agent** :
   - Aller dans l'onglet "Agents"
   - Cliquer sur l'icône "Modifier" (crayon)
   - Remplir le champ "Solde HS (heures)"
   - Sauvegarder

2. **Créer un nouvel agent avec des HS** :
   - Cliquer sur "Nouvel agent"
   - Remplir tous les champs, y compris "Solde HS"
   - Sauvegarder

## Calculs automatiques

Les heures supplémentaires sont prises en compte dans :
- **Solde disponible** : Affiché en temps réel
- **Historique des mouvements** : Calcul du solde avant/après chaque demande
- **Tableau des droits totaux** : Récapitulatif complet

## API

### Endpoints mis à jour :

- `GET /api/agents` : Inclut maintenant le champ `solde_hs`
- `POST /api/agents` : Accepte le paramètre `solde_hs`
- `PUT /api/agents/{id}` : Permet de modifier le `solde_hs`

### Structure JSON :

```json
{
  "id": 1,
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@exemple.com",
  "solde_ca": 107.5,
  "solde_rtt": 18.0,
  "solde_cet": 0.0,
  "solde_hs": 10.5,
  // ... autres champs
}
```

## Migration

La migration a été effectuée automatiquement :
- ✅ Ajout de la colonne `solde_hs` à la table `agent`
- ✅ Initialisation à 0.0 pour tous les agents existants
- ✅ Compatibilité avec les données existantes

## Tests

Pour tester la fonctionnalité :

```bash
python3 test_hs_functionality.py
```

Ce script vérifie :
- La présence du champ `solde_hs` dans l'API
- La possibilité de modifier le solde HS
- La création de demandes avec le type HS

## Notes techniques

- **Type de données** : Float (permet les demi-heures)
- **Valeur par défaut** : 0.0
- **Calculs** : Intégrés dans les fonctions existantes
- **Compatibilité** : Rétrocompatible avec les versions précédentes

## Résolution de problèmes

### Si le champ HS n'apparaît pas :
1. Vérifier que la migration a été exécutée
2. Redémarrer l'application Flask
3. Vider le cache du navigateur

### Si les calculs sont incorrects :
1. Vérifier que les demandes HS ont le bon statut
2. S'assurer que le type_absence = "HS" dans la base de données

### Si l'admin ne peut pas modifier :
1. Vérifier les permissions d'admin
2. S'assurer que tous les champs du formulaire sont remplis
3. Contrôler les logs du serveur pour les erreurs

## Support

Pour toute question ou problème avec les heures supplémentaires, vérifier :
1. Les logs de l'application
2. La structure de la base de données
3. Les permissions utilisateur
4. La configuration CORS si nécessaire




