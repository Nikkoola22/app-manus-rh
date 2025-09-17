# Guide de Test - Soldes Initiaux dans la Page Agent

## 🎯 Objectif
Vérifier que la page agent affiche correctement les **droits initiaux** dans la section "Informations de travail" sans faire de soustraction.

## 📋 Fonctionnalités Testées

### ✅ Section "Informations de travail"
- **Solde CA** : Affiche la valeur brute de `agent.solde_ca`
- **Solde RTT** : Calculé automatiquement selon la quotité (38h = 18 RTT, 36h = 6 RTT)
- **Solde CET** : Affiche la valeur brute de `agent.solde_cet`
- **Solde HS** : Affiche la valeur brute de `agent.solde_hs`
- **Solde Bonifications** : Affiche la valeur brute de `agent.solde_bonifications`
- **Solde Jours de sujétions** : Affiche la valeur brute de `agent.solde_jours_sujetions`
- **Solde Congés formations** : Affiche la valeur brute de `agent.solde_conges_formations`

### ✅ Section "Historique des soldes"
- **Droits totaux** : Affiche les droits initiaux
- **Congés pris** : Calcule les congés consommés
- **Solde restant** : Calcule les soldes restants après consommation

## 🧪 Tests Effectués

### Test 1 : Agent avec Quotité 35h
```
Agent: Super ADMIN
Quotité: 35h/semaine
RTT calculé: 0 jours (moins de 36h)
Soldes initiaux: 175.0 CA, 35.0 CET, 0.0 HS, etc.
```

### Test 2 : Agent avec Quotité 38h
```
Agent: Agent38h TEST
Quotité: 38h/semaine
RTT calculé: 18 jours (38h et plus)
Soldes initiaux: 72.5 CA, 0.0 CET, 0.0 HS, etc.
```

## 🔧 Corrections Appliquées

### 1. Affichage des Soldes Initiaux
```javascript
// Avant (avec soustraction)
<p className="text-sm">{agent.solde_ca - calculateCongesPris('CA')} jours</p>

// Après (droits initiaux)
<p className="text-sm font-semibold text-blue-600">{agent.solde_ca || 0} jours</p>
```

### 2. Calcul Automatique des RTT
```javascript
// RTT calculé selon la quotité
<p className="text-sm font-semibold text-blue-600">
  {calculateRttFromQuotite(agent.quotite_travail)} jours
</p>
```

### 3. Description Explicative
```javascript
<CardDescription>
  Droits initiaux accordés (les calculs de consommation sont dans l'historique)
</CardDescription>
```

## 📊 Règles de Calcul RTT

| Quotité | RTT Accordés |
|---------|--------------|
| 38h et plus | 18 jours |
| 36h | 6 jours |
| Moins de 36h | 0 jour |

## 🎨 Améliorations Visuelles

- **Couleur bleue** pour les soldes initiaux
- **Police en gras** pour mettre en évidence
- **Description explicative** pour clarifier le contenu
- **Séparation claire** entre droits initiaux et calculs

## ✅ Résultats Attendus

### Section "Informations de travail"
- ✅ Affiche les **droits initiaux** sans soustraction
- ✅ RTT calculé automatiquement selon la quotité
- ✅ Tous les types de soldes affichés
- ✅ Style visuel distinctif

### Section "Historique des soldes"
- ✅ Affiche les **droits totaux**
- ✅ Calcule les **congés pris**
- ✅ Calcule les **soldes restants**
- ✅ Historique détaillé des mouvements

## 🚀 Comment Tester

1. **Démarrer l'application** :
   ```bash
   ./start_simple.sh
   ```

2. **Se connecter en tant qu'admin** :
   - Email: `admin@exemple.com`
   - Mot de passe: `admin123`

3. **Naviguer vers un agent** :
   - Cliquer sur "Voir Agent" dans l'onglet "Demandes"
   - Ou utiliser le bouton "Voir" dans le tableau des agents

4. **Vérifier les soldes** :
   - Onglet "Informations" → Section "Informations de travail"
   - Onglet "Historique" → Section "Historique des soldes"

## 📝 Fichiers de Test

- `test_soldes_initiaux.html` : Test visuel des soldes
- `test_agent_soldes.py` : Test automatisé des API
- `test_navigation_agent.html` : Test de navigation

## 🎉 Conclusion

Les soldes initiaux sont maintenant correctement affichés dans la section "Informations de travail" sans aucune soustraction. Les calculs de consommation sont réservés à l'onglet "Historique des soldes" comme demandé.

