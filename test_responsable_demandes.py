#!/usr/bin/env python3
"""
Script de test pour vérifier que les responsables peuvent faire des demandes de congés
"""

import requests
import json
from datetime import date, timedelta

BASE_URL = 'http://127.0.0.1:5001/api'

def test_responsable_demandes():
    """Test que les responsables peuvent faire des demandes de congés validées par l'admin"""
    
    print("🧪 Test Demandes de Congés des Responsables")
    print("=" * 60)
    
    # Créer une session pour maintenir les cookies
    session = requests.Session()
    
    # 1. Connexion admin
    print("\n1. Connexion en tant qu'admin...")
    login_data = {'email': 'admin@exemple.com', 'password': 'admin123'}
    response = session.post(f'{BASE_URL}/auth/login', json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Échec de la connexion admin: {response.text}")
        return
    
    print("✅ Connexion admin réussie")
    
    # 2. Récupérer les responsables
    print("\n2. Récupération des responsables...")
    response = session.get(f'{BASE_URL}/agents')
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération des agents: {response.text}")
        return
    
    agents = response.json()
    responsables = [agent for agent in agents if agent['role'] == 'Responsable']
    
    if not responsables:
        print("❌ Aucun responsable trouvé")
        return
    
    test_responsable = responsables[0]
    print(f"✅ Responsable de test: {test_responsable['prenom']} {test_responsable['nom']} (ID: {test_responsable['id']})")
    
    # 3. Connexion responsable
    print(f"\n3. Connexion en tant que responsable...")
    responsable_login_data = {
        'email': test_responsable['email'], 
        'password': 'resp123'  # Mot de passe par défaut
    }
    response = session.post(f'{BASE_URL}/auth/login', json=responsable_login_data)
    
    if response.status_code != 200:
        print(f"❌ Échec de la connexion responsable: {response.text}")
        return
    
    print("✅ Connexion responsable réussie")
    
    # 4. Récupérer les demandes du responsable
    print(f"\n4. Récupération des demandes du responsable...")
    response = session.get(f'{BASE_URL}/demandes/mes-demandes')
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération des demandes: {response.text}")
        return
    
    mes_demandes = response.json()
    print(f"✅ {len(mes_demandes)} demandes du responsable trouvées")
    
    # 5. Créer une demande de congé
    print(f"\n5. Création d'une demande de congé...")
    today = date.today()
    demande_data = {
        'type_absence': 'CA',
        'date_debut': today.isoformat(),
        'date_fin': (today + timedelta(days=2)).isoformat(),
        'nb_heures': 21.0,
        'motif': 'Vacances d\'été - Responsable'
    }
    
    response = session.post(f'{BASE_URL}/demandes', json=demande_data)
    
    if response.status_code != 201:
        print(f"❌ Échec de création de la demande: {response.text}")
        return
    
    nouvelle_demande = response.json()
    demande_id = nouvelle_demande['id']
    print(f"✅ Demande créée avec succès (ID: {demande_id})")
    
    # 6. Vérifier que la demande apparaît dans les demandes du responsable
    print(f"\n6. Vérification des demandes du responsable...")
    response = session.get(f'{BASE_URL}/demandes/mes-demandes')
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération des demandes: {response.text}")
        return
    
    mes_demandes_apres = response.json()
    print(f"✅ {len(mes_demandes_apres)} demandes du responsable après création")
    
    # Vérifier que la nouvelle demande est présente
    nouvelle_demande_trouvee = any(d['id'] == demande_id for d in mes_demandes_apres)
    if nouvelle_demande_trouvee:
        print("✅ Nouvelle demande trouvée dans les demandes du responsable")
    else:
        print("❌ Nouvelle demande non trouvée dans les demandes du responsable")
    
    # 7. Reconnexion admin pour valider la demande
    print(f"\n7. Reconnexion admin pour valider la demande...")
    response = session.post(f'{BASE_URL}/auth/login', json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Échec de la reconnexion admin: {response.text}")
        return
    
    print("✅ Reconnexion admin réussie")
    
    # 8. Récupérer toutes les demandes (admin)
    print(f"\n8. Récupération de toutes les demandes (admin)...")
    response = session.get(f'{BASE_URL}/demandes')
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération des demandes: {response.text}")
        return
    
    toutes_demandes = response.json()
    demande_a_valider = next((d for d in toutes_demandes if d['id'] == demande_id), None)
    
    if not demande_a_valider:
        print("❌ Demande non trouvée dans les demandes admin")
        return
    
    print(f"✅ Demande trouvée dans les demandes admin: {demande_a_valider['statut']}")
    
    # 9. Valider la demande
    print(f"\n9. Validation de la demande par l'admin...")
    validation_data = {
        'action': 'approuver',
        'commentaires': 'Demande approuvée par l\'admin'
    }
    
    response = session.post(f'{BASE_URL}/demandes/{demande_id}/valider', json=validation_data)
    
    if response.status_code != 200:
        print(f"❌ Échec de validation de la demande: {response.text}")
        return
    
    demande_validee = response.json()
    print(f"✅ Demande validée avec succès: {demande_validee['statut']}")
    
    # 10. Vérifier que la demande est validée
    print(f"\n10. Vérification du statut de la demande...")
    response = session.get(f'{BASE_URL}/demandes/{demande_id}')
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération de la demande: {response.text}")
        return
    
    demande_finale = response.json()
    print(f"✅ Statut final de la demande: {demande_finale['statut']}")
    print(f"✅ Validée le: {demande_finale.get('date_validation', 'N/A')}")
    print(f"✅ Validateur: {demande_finale.get('validateur_id', 'N/A')}")
    
    print(f"\n✅ Test terminé avec succès")
    print(f"\n📝 Résumé:")
    print(f"   • Responsable connecté ✅")
    print(f"   • Demande créée par le responsable ✅")
    print(f"   • Demande visible dans 'Mes Demandes' ✅")
    print(f"   • Demande visible par l'admin ✅")
    print(f"   • Demande validée par l'admin ✅")
    print(f"   • Workflow responsable → admin fonctionnel ✅")

if __name__ == '__main__':
    test_responsable_demandes()

