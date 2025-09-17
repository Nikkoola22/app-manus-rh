# 🚫 Fonctionnalité d'annulation des demandes

## 🎯 Objectif

Permettre aux agents d'annuler leurs propres demandes de congé tant qu'elles ne sont pas encore validées par leur responsable ou administrateur.

## ✅ Fonctionnalités implémentées

### 1. **API Backend** (`/api/demandes/<id>/annuler`)

**Fichier** : `src/routes/demandes.py`

**Fonctionnalités** :
- ✅ **POST** `/api/demandes/<demande_id>/annuler`
- ✅ **Authentification requise** : Seul l'agent connecté peut annuler
- ✅ **Vérification des permissions** : Seul le créateur de la demande peut l'annuler
- ✅ **Vérification du statut** : Seules les demandes "En attente" peuvent être annulées
- ✅ **Changement de statut** : "En attente" → "Annulée"
- ✅ **Enregistrement de la date** : `date_annulation` automatiquement remplie
- ✅ **Retour JSON** : Message de succès + données de la demande

**Code** :
```python
@demandes_bp.route('/demandes/<int:demande_id>/annuler', methods=['POST'])
@login_required
def annuler_demande(demande_id):
    # Vérifications de sécurité
    if demande.agent_id != current_user.id:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    
    if demande.statut != 'En attente':
        return jsonify({'error': 'Impossible d\'annuler une demande déjà traitée'}), 400
    
    # Annulation
    demande.statut = 'Annulée'
    demande.date_annulation = datetime.utcnow()
    db.session.commit()
```

### 2. **Modèle de données** (`DemandeConge`)

**Fichier** : `src/models/demande_conge.py`

**Nouveaux champs** :
- ✅ `date_annulation` : `DATETIME` nullable
- ✅ Statut "Annulée" ajouté aux commentaires
- ✅ Champ inclus dans `to_dict()` pour l'API

**Migration** :
- ✅ Script `migrate_annulation.py` pour ajouter la colonne
- ✅ Vérification d'existence avant ajout
- ✅ Compatible avec SQLAlchemy moderne

### 3. **Interface utilisateur** (`AgentDashboard`)

**Fichier** : `src/components/AgentDashboard.jsx`

**Fonctionnalités** :
- ✅ **Bouton d'annulation** : Visible uniquement pour les demandes "En attente"
- ✅ **Confirmation** : Dialog de confirmation avant annulation
- ✅ **Design** : Bouton rouge avec icône X
- ✅ **Feedback** : Messages de succès/erreur
- ✅ **Rafraîchissement** : Rechargement automatique de la liste
- ✅ **Colonne Actions** : Nouvelle colonne dans le tableau

**Code** :
```jsx
<TableCell>
  {demande.statut === 'En attente' && (
    <Button
      variant="outline"
      size="sm"
      onClick={() => annulerDemande(demande.id)}
      className="text-red-600 hover:text-red-700 hover:bg-red-50"
    >
      <X className="h-4 w-4 mr-1" />
      Annuler
    </Button>
  )}
</TableCell>
```

## 🔒 Sécurité et validations

### **Contrôles d'accès**
- ✅ **Authentification** : Utilisateur doit être connecté
- ✅ **Autorisation** : Seul le créateur peut annuler
- ✅ **Statut** : Seules les demandes "En attente" sont annulables
- ✅ **Protection CSRF** : Utilisation des cookies de session

### **Validations métier**
- ✅ **Demande existante** : Vérification de l'existence
- ✅ **Statut valide** : Impossible d'annuler une demande traitée
- ✅ **Propriétaire** : Impossible d'annuler la demande d'un autre
- ✅ **Confirmation** : Dialog de confirmation côté client

## 📊 Tests de validation

### **Tests automatisés** (`test_annulation_demande.py`)

**Scénarios testés** :
- ✅ **Création et annulation** : Cycle complet
- ✅ **Vérification du statut** : "En attente" → "Annulée"
- ✅ **Enregistrement de la date** : `date_annulation` correctement remplie
- ✅ **Protection contre double annulation** : Erreur si déjà annulée
- ✅ **Protection contre annulation d'autrui** : Erreur 403
- ✅ **Récupération des données** : API retourne les bonnes informations

**Résultats** :
```
✅ Demande annulée avec succès
✅ Nouveau statut: Annulée
✅ Date annulation: 2025-09-17T20:42:43.645271
✅ Erreur attendue: Impossible d'annuler une demande déjà traitée
✅ Erreur attendue: Permissions insuffisantes
```

## 🎨 Interface utilisateur

### **Tableau des demandes**
- ✅ **Nouvelle colonne "Actions"** : Bouton d'annulation
- ✅ **Affichage conditionnel** : Visible uniquement pour "En attente"
- ✅ **Design cohérent** : Style rouge pour l'action destructive
- ✅ **Icône intuitive** : X pour l'annulation
- ✅ **Hover effects** : Feedback visuel au survol

### **Expérience utilisateur**
- ✅ **Confirmation** : "Êtes-vous sûr de vouloir annuler cette demande ?"
- ✅ **Feedback immédiat** : Messages de succès/erreur
- ✅ **Mise à jour automatique** : Liste rechargée après annulation
- ✅ **Cohérence** : Même style que les autres boutons

## 🔄 Workflow complet

### **1. Agent crée une demande**
```
Demande créée → Statut: "En attente" → Bouton "Annuler" visible
```

### **2. Agent annule sa demande**
```
Clic "Annuler" → Confirmation → API appelée → Statut: "Annulée" → Bouton disparaît
```

### **3. Responsable valide une demande**
```
Demande validée → Statut: "Approuvée" → Bouton "Annuler" disparaît
```

## 📁 Fichiers modifiés

1. **`src/routes/demandes.py`**
   - Nouvelle route `annuler_demande()`
   - Logique de validation et sécurité

2. **`src/models/demande_conge.py`**
   - Champ `date_annulation` ajouté
   - Mise à jour de `to_dict()`

3. **`src/components/AgentDashboard.jsx`**
   - Fonction `annulerDemande()`
   - Bouton d'annulation dans le tableau
   - Colonne "Actions" ajoutée

4. **`migrate_annulation.py`**
   - Script de migration de la base de données

5. **`test_annulation_demande.py`**
   - Tests automatisés complets

## ✅ Statut

- ✅ **Backend** : API complète et sécurisée
- ✅ **Base de données** : Migration appliquée
- ✅ **Frontend** : Interface utilisateur intuitive
- ✅ **Tests** : Validation complète
- ✅ **Sécurité** : Contrôles d'accès stricts
- ✅ **UX** : Expérience utilisateur fluide

---

**🎉 Les agents peuvent maintenant annuler leurs demandes tant qu'elles ne sont pas validées !**

**Fonctionnalités clés** :
- **Sécurité** : Seul le créateur peut annuler
- **Validation** : Seules les demandes en attente sont annulables
- **Interface** : Bouton intuitif avec confirmation
- **Traçabilité** : Date d'annulation enregistrée
- **Protection** : Contrôles stricts contre les abus
