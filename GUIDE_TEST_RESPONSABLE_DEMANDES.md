# Guide de Test - Demandes de Congés des Responsables

## 🎯 Objectif
Vérifier que les responsables de service peuvent faire des demandes de congés qui sont validées par l'admin, et non par eux-mêmes.

## 🔧 Fonctionnalités Implémentées

### ❌ Problème Identifié
Les responsables de service ne pouvaient pas faire leurs propres demandes de congés :
- **Pas d'interface** : Aucun moyen pour les responsables de créer des demandes
- **Pas de workflow** : Les demandes des responsables n'étaient pas gérées
- **Validation manquante** : Pas de processus de validation par l'admin

### ✅ Solution Implémentée

#### 1. Interface Responsable
```javascript
// Nouvel onglet "Mes Demandes" dans ResponsableDashboard
<TabsTrigger value="mes-demandes">
  Mes Demandes ({mesDemandes.length})
</TabsTrigger>

// Formulaire de création de demande
<Dialog open={showDemandeForm} onOpenChange={setShowDemandeForm}>
  <DialogTitle>Nouvelle Demande de Congé</DialogTitle>
  <DialogDescription>
    Créer une nouvelle demande de congé (sera validée par l'admin)
  </DialogDescription>
  // ... formulaire complet
</Dialog>
```

#### 2. API Endpoint
```python
@demandes_bp.route('/demandes/mes-demandes', methods=['GET'])
@login_required
def get_mes_demandes():
    """Récupère les demandes de congés du responsable connecté"""
    current_user = Agent.query.get(session['user_id'])
    
    if current_user.role != 'Responsable':
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    # Le responsable voit ses propres demandes
    demandes = DemandeConge.query.filter_by(agent_id=current_user.id).all()
    
    return jsonify([demande.to_dict() for demande in demandes])
```

#### 3. Workflow de Validation
```python
# Envoi d'email selon le rôle
if current_user.role == 'Responsable':
    # Les demandes des responsables sont envoyées à l'admin
    admin = Agent.query.filter_by(role='Admin').first()
    if admin:
        send_demande_conge_email(current_user, admin, demande)
else:
    # Les demandes des agents sont envoyées au responsable du service
    responsable = Agent.query.filter_by(
        service_id=current_user.service_id,
        role='Responsable'
    ).first()
    if responsable:
        send_demande_conge_email(current_user, responsable, demande)
```

#### 4. Permissions de Validation
```python
# Vérifier les permissions
if current_user.role == 'Responsable':
    # Les responsables ne peuvent valider que les demandes des agents de leur service
    if agent_demande.service_id != current_user.service_id:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    # Les responsables ne peuvent pas valider leurs propres demandes
    if agent_demande.id == current_user.id:
        return jsonify({'error': 'Vous ne pouvez pas valider vos propres demandes'}), 403
elif current_user.role == 'Admin':
    # L'admin peut valider toutes les demandes
    pass
```

## 🧪 Tests Effectués

### Test 1 : Création de Demande par Responsable
```python
# Connexion responsable
responsable_login_data = {
    'email': test_responsable['email'], 
    'password': 'resp123'
}
response = session.post(f'{BASE_URL}/auth/login', json=responsable_login_data)

# Création de demande
demande_data = {
    'type_absence': 'CA',
    'date_debut': today.isoformat(),
    'date_fin': (today + timedelta(days=2)).isoformat(),
    'nb_heures': 21.0,
    'motif': 'Vacances d\'été - Responsable'
}
response = session.post(f'{BASE_URL}/demandes', json=demande_data)
```

**Résultat :**
- ✅ Responsable connecté
- ✅ Demande créée avec succès
- ✅ Demande visible dans "Mes Demandes"

### Test 2 : Validation par Admin
```python
# Reconnexion admin
response = session.post(f'{BASE_URL}/auth/login', json=admin_login_data)

# Validation de la demande
validation_data = {
    'action': 'approuver',
    'commentaires': 'Demande approuvée par l\'admin'
}
response = session.post(f'{BASE_URL}/demandes/{demande_id}/valider', json=validation_data)
```

**Résultat :**
- ✅ Demande visible par l'admin
- ✅ Demande validée avec succès
- ✅ Statut final : "Approuvée"

## 🎨 Interface Utilisateur

### Onglet "Mes Demandes" du Responsable
```
┌─────────────────────────────────────────────────────────┐
│ Mes Demandes (1)                                       │
│                                                         │
│ [Nouvelle Demande]                                     │
│                                                         │
│ Type    │ Période        │ Durée │ Motif    │ Statut   │
│ CA      │ 17/09 - 19/09  │ 21h   │ Vacances │ Approuvée│
└─────────────────────────────────────────────────────────┘
```

### Formulaire de Création
```
┌─────────────────────────────────────────────────────────┐
│ Nouvelle Demande de Congé                              │
│                                                         │
│ Type d'absence: [CA ▼]                                 │
│ Date début: [2024-09-17] Date fin: [2024-09-19]       │
│ Nombre d'heures: [21.0]                                │
│ Motif: [Vacances d'été - Responsable]                  │
│                                                         │
│ [Annuler] [Créer la demande]                           │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Comment Tester

### 1. Démarrer l'Application
```bash
./start_simple.sh
```

### 2. Se Connecter en tant que Responsable
- URL: http://localhost:5173
- Email: `jean.martin@exemple.com` (ou autre responsable)
- Mot de passe: `resp123`

### 3. Aller dans l'Onglet "Mes Demandes"
1. **Cliquer sur "Mes Demandes"** : Dans le dashboard responsable
2. **Vérifier l'interface** : Doit afficher les demandes du responsable
3. **Cliquer sur "Nouvelle Demande"** : Pour créer une demande

### 4. Créer une Demande
1. **Remplir le formulaire** :
   - Type d'absence : CA, RTT, CET, etc.
   - Dates de début et fin
   - Nombre d'heures
   - Motif
2. **Cliquer sur "Créer la demande"**
3. **Vérifier** : La demande apparaît dans "Mes Demandes"

### 5. Valider en tant qu'Admin
1. **Se connecter en tant qu'admin** : `admin@exemple.com` / `admin123`
2. **Aller dans l'onglet "Demandes"** : Voir toutes les demandes
3. **Trouver la demande du responsable** : Statut "En attente"
4. **Cliquer sur "Valider"** : Approuver ou refuser
5. **Vérifier** : Le statut change dans "Mes Demandes" du responsable

## 📁 Fichiers Modifiés

- `src/components/ResponsableDashboard.jsx` : Ajout de l'onglet "Mes Demandes"
- `src/routes/demandes.py` : Ajout de l'endpoint `/demandes/mes-demandes`
- `test_responsable_demandes.py` : Test automatisé
- `GUIDE_TEST_RESPONSABLE_DEMANDES.md` : Guide complet

## ✅ Résultats Attendus

### Interface Responsable
- ✅ Onglet "Mes Demandes" visible
- ✅ Formulaire de création fonctionnel
- ✅ Liste des demandes du responsable
- ✅ Statuts mis à jour en temps réel

### Workflow de Validation
- ✅ Demandes des responsables → Admin
- ✅ Demandes des agents → Responsable
- ✅ Emails envoyés aux bons destinataires
- ✅ Permissions respectées

### API Fonctionnelle
- ✅ Endpoint `/demandes/mes-demandes` opérationnel
- ✅ Création de demandes par responsables
- ✅ Validation par admin uniquement
- ✅ Gestion des permissions correcte

## 🎉 Conclusion

Le système de demandes de congés pour les responsables a été implémenté avec succès :

1. **Interface complète** : Onglet "Mes Demandes" avec formulaire de création
2. **API fonctionnelle** : Endpoint dédié aux demandes du responsable
3. **Workflow correct** : Responsables → Admin (pas d'auto-validation)
4. **Permissions respectées** : Seuls les admins peuvent valider les demandes des responsables
5. **Emails automatiques** : Notifications envoyées aux bons destinataires

**Les responsables peuvent maintenant faire leurs demandes de congés qui sont validées par l'admin !** 🎉

