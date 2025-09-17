# 🧮 Guide du Calcul Automatique des RTT

## ✅ Fonctionnalité Implémentée

Le système calcule maintenant automatiquement les RTT en fonction de la quotité de travail hebdomadaire de l'agent.

## 📊 Règles de Calcul

| Quotité de travail | RTT accordés | Description |
|-------------------|--------------|-------------|
| **38h et plus** | **18 RTT** | Temps plein avec RTT |
| **36h-37h** | **6 RTT** | Temps partiel avec RTT |
| **35h et moins** | **0 RTT** | Pas de RTT |

## 🔧 Modifications Techniques

### **1. Modèle Agent (`src/models/agent.py`)**

**Nouvelles méthodes ajoutées :**
```python
def calculate_rtt_from_quotite(self):
    """Calcule le nombre de RTT en fonction de la quotité de travail"""
    if not self.quotite_travail:
        return 0
    
    quotite = self.quotite_travail
    
    if quotite >= 38:
        return 18  # 18 RTT pour 38h et plus
    elif quotite >= 36:
        return 6   # 6 RTT pour 36h
    else:
        return 0   # Pas de RTT pour moins de 36h

def get_effective_rtt_solde(self):
    """Retourne le solde RTT effectif (calculé automatiquement)"""
    return self.calculate_rtt_from_quotite()
```

**Modification de `to_dict()` :**
```python
'solde_rtt': self.get_effective_rtt_solde(),  # Utilise le calcul automatique
```

### **2. Composants React**

**AgentDashboard et AgentProfile :**
- Ajout de la fonction `calculateRttFromQuotite()`
- Modification de `getSoldeInitial()` pour utiliser le calcul automatique des RTT

## 🎯 Exemples Concrets

### **Agent à 38h/semaine :**
- Quotité : 38h
- RTT calculés : **18 RTT**
- Affichage : "18h" dans les soldes

### **Agent à 36h/semaine :**
- Quotité : 36h
- RTT calculés : **6 RTT**
- Affichage : "6h" dans les soldes

### **Agent à 35h/semaine :**
- Quotité : 35h
- RTT calculés : **0 RTT**
- Affichage : "0h" dans les soldes

## 📍 Où Voir les RTT Calculés

### **1. Page Personnelle de l'Agent**
- Section "Soldes de congés" → Carte RTT
- Section "Historique des mouvements" → Calculs des soldes

### **2. Profil d'Agent (Responsables/Admins)**
- Onglet "Informations" → Solde RTT
- Onglet "Historique" → Tableau des droits totaux

### **3. API Backend**
- Endpoint `/api/agents/{id}` → `solde_rtt` calculé automatiquement
- Endpoint `/api/auth/login` → `solde_rtt` dans les données utilisateur

## 🔄 Mise à Jour Automatique

Les RTT sont recalculés automatiquement :
- ✅ À chaque connexion de l'agent
- ✅ À chaque affichage du profil
- ✅ À chaque calcul d'historique
- ✅ Lors de la récupération des données via l'API

## 🧪 Test de la Fonctionnalité

### **Script de Test :**
```bash
cd "/Users/nikkoolagarnier/Downloads/app manus rh"
source venv/bin/activate
python test_rtt_calculation.py
```

### **Test Manuel :**
1. Connectez-vous en tant qu'agent
2. Vérifiez la quotité de travail dans "Mes informations"
3. Vérifiez le solde RTT dans "Soldes de congés"
4. Le solde doit correspondre au calcul automatique

## 📝 Avantages

1. **Automatique** : Plus besoin de saisir manuellement les RTT
2. **Cohérent** : Calcul uniforme selon les règles établies
3. **Temps réel** : Mise à jour automatique des soldes
4. **Fiable** : Élimine les erreurs de saisie manuelle

## 🎨 Interface Utilisateur

### **Avant :**
- RTT saisis manuellement dans la base de données
- Risque d'incohérence entre quotité et RTT

### **Après :**
- RTT calculés automatiquement selon la quotité
- Affichage cohérent partout dans l'application
- Historique des mouvements avec calculs corrects

## ✅ Résultat

**Les RTT sont maintenant calculés automatiquement selon la quotité de travail !**

- 38h+ → 18 RTT
- 36h-37h → 6 RTT  
- 35h et moins → 0 RTT

L'application est maintenant plus intelligente et cohérente ! 🎉




