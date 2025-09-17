# Guide de Test - Création d'Agent avec Soldes et Service

## 🎯 Objectif
Vérifier que la création d'agent affiche tous les soldes et que le service assigné est correctement affiché dans la fiche agent.

## 🔧 Corrections Appliquées

### 1. Formulaire de Création d'Agent
- ✅ **Ajout de tous les champs de soldes** dans le formulaire
- ✅ **Organisation en section "Soldes initiaux"** avec titre explicite
- ✅ **Champs avec unité "(jours)"** pour clarifier
- ✅ **Support des décimales** avec `step="0.5"`
- ✅ **Calcul automatique des RTT** selon la quotité

### 2. Affichage du Service dans la Fiche Agent
- ✅ **Modification de `Agent.to_dict()`** pour inclure la relation `service`
- ✅ **Chargement de la relation** avec `joinedload(Agent.service)`
- ✅ **Affichage correct** du nom du service assigné

### 3. API des Agents
- ✅ **Chargement de la relation service** dans `get_agent()`
- ✅ **Import de `joinedload`** pour les relations SQLAlchemy
- ✅ **Retour des données complètes** avec service inclus

## 📋 Champs de Soldes Ajoutés

| Champ | Description | Unité |
|-------|-------------|-------|
| Solde CA | Congés Annuels | jours |
| Solde RTT | RTT (calculé automatiquement) | jours |
| Solde CET | Compte Épargne Temps | jours |
| Solde HS | Heures Supplémentaires | jours |
| Solde Bonifications | Bonifications | jours |
| Solde Jours de sujétions | Jours de sujétions | jours |
| Solde Congés formations | Congés formations | jours |

## 🧪 Tests Effectués

### Test 1 : Création d'Agent avec Tous les Soldes
```python
agent_data = {
    'nom': 'TEST_SOLDES',
    'prenom': 'Agent',
    'email': 'agent.soldes@test.com',
    'password': 'test123',
    'role': 'Agent',
    'service_id': 1,
    'quotite_travail': 38,
    'solde_ca': 80.0,
    'solde_rtt': 0.0,  # Calculé automatiquement
    'solde_cet': 0.0,
    'solde_hs': 0.0,
    'solde_bonifications': 34.4,
    'solde_jours_sujetions': 0.0,
    'solde_conges_formations': 1.0
}
```

**Résultat :**
- ✅ Agent créé avec succès
- ✅ Tous les soldes sauvegardés
- ✅ RTT calculé automatiquement (18 jours pour 38h)
- ✅ Service assigné et affiché

### Test 2 : Vérification de l'Affichage du Service
```python
# Récupération de l'agent complet
agent = session.get(f"{BASE_URL}/agents/{agent_id}")

# Vérification du service
if 'service' in agent and agent['service']:
    print(f"Service: {agent['service']['nom_service']}")
```

**Résultat :**
- ✅ Service correctement chargé
- ✅ Nom du service affiché
- ✅ Relation service fonctionnelle

## 🎨 Interface Utilisateur

### Formulaire de Création
- **Section "Soldes initiaux"** avec titre explicite
- **Grille 3 colonnes** pour organiser les champs
- **Labels avec unité** "(jours)" pour clarifier
- **Support des décimales** avec `step="0.5"`
- **Calcul automatique des RTT** affiché

### Fiche Agent
- **Service assigné** affiché dans "Informations personnelles"
- **Tous les soldes** affichés dans "Informations de travail"
- **Calcul automatique des RTT** selon la quotité
- **Relation service** correctement chargée

## 🔄 Règles de Calcul RTT

| Quotité | RTT Accordés | Calcul |
|---------|--------------|--------|
| 38h et plus | 18 jours | Automatique |
| 36h | 6 jours | Automatique |
| Moins de 36h | 0 jour | Automatique |

## 🚀 Comment Tester

### 1. Démarrer l'Application
```bash
./start_simple.sh
```

### 2. Se Connecter en tant qu'Admin
- Email: `admin@exemple.com`
- Mot de passe: `admin123`

### 3. Créer un Nouvel Agent
1. Aller dans l'onglet "Agents"
2. Cliquer sur "Nouvel Agent"
3. Remplir les informations de base
4. **Vérifier que tous les soldes sont affichés**
5. Remplir les soldes (ex: CA=80, Bonifications=34.4, etc.)
6. Sélectionner un service
7. Cliquer sur "Créer"

### 4. Vérifier la Fiche Agent
1. Cliquer sur "Voir" pour l'agent créé
2. **Vérifier que le service est affiché** dans "Informations personnelles"
3. **Vérifier que tous les soldes sont affichés** dans "Informations de travail"
4. **Vérifier que les RTT sont calculés automatiquement**

## 📁 Fichiers de Test

- `test_agent_creation_service.py` : Test automatisé des API
- `test_creation_agent_ui.html` : Test visuel de l'interface
- `GUIDE_TEST_CREATION_AGENT.md` : Guide complet de test

## ✅ Résultats Attendus

### Formulaire de Création
- ✅ Tous les champs de soldes visibles
- ✅ Section "Soldes initiaux" bien organisée
- ✅ Calcul automatique des RTT
- ✅ Validation et sauvegarde des données

### Fiche Agent
- ✅ Service assigné affiché correctement
- ✅ Tous les soldes initiaux affichés
- ✅ Calcul automatique des RTT
- ✅ Relation service fonctionnelle

## 🎉 Conclusion

Les corrections ont été appliquées avec succès :

1. **Formulaire de création** affiche maintenant tous les soldes
2. **Service assigné** est correctement affiché dans la fiche agent
3. **Calcul automatique des RTT** fonctionne selon la quotité
4. **API** retourne les données complètes avec la relation service

**L'interface de création d'agent est maintenant complète et fonctionnelle !** 🎉

