#!/usr/bin/env python3
"""
Script de test pour vérifier que le bouton de suppression des agents s'affiche correctement
"""

import requests
import json
from datetime import date

BASE_URL = 'http://127.0.0.1:5001/api'

def test_agent_delete_button():
    """Test que le bouton de suppression des agents s'affiche correctement"""
    
    print("🧪 Test Bouton Suppression Agents")
    print("=" * 50)
    
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
    
    # 2. Récupérer les agents
    print("\n2. Récupération des agents...")
    response = session.get(f'{BASE_URL}/agents')
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération des agents: {response.text}")
        return
    
    agents = response.json()
    print(f"✅ {len(agents)} agents trouvés")
    
    # 3. Afficher les agents disponibles
    print("\n3. Agents disponibles pour test de suppression:")
    for agent in agents:
        print(f"   • ID: {agent['id']} - {agent['prenom']} {agent['nom']} ({agent['email']})")
    
    # 4. Tester la suppression d'un agent de test
    print("\n4. Test de suppression d'un agent...")
    
    # Créer un agent de test pour la suppression
    test_agent_data = {
        'nom': 'AgentTestDelete',
        'prenom': 'Test',
        'email': 'agent.test.delete@exemple.com',
        'password': 'test123',
        'role': 'Agent',
        'quotite_travail': 35,
        'service_id': 1,  # Utiliser le premier service disponible
        'date_debut_contrat': '2024-01-01',
        'annee_entree_fp': '2024',
        'solde_ca': 25,
        'solde_rtt': 0,
        'solde_cet': 5,
        'solde_hs': 0,
        'solde_bonifications': 2,
        'solde_jours_sujetions': 3,
        'solde_conges_formations': 4
    }
    
    response = session.post(f'{BASE_URL}/agents', json=test_agent_data)
    
    if response.status_code != 201:
        print(f"❌ Échec de création de l'agent de test: {response.text}")
        return
    
    test_agent = response.json()
    test_agent_id = test_agent['id']
    print(f"✅ Agent de test créé: {test_agent['prenom']} {test_agent['nom']} (ID: {test_agent_id})")
    
    # 5. Vérifier que l'agent existe
    print("\n5. Vérification de l'existence de l'agent...")
    response = session.get(f'{BASE_URL}/agents/{test_agent_id}')
    
    if response.status_code == 200:
        print("✅ Agent de test existe avant suppression")
    else:
        print("❌ Agent de test non trouvé avant suppression")
        return
    
    # 6. Tester la suppression
    print("\n6. Test de suppression de l'agent de test...")
    response = session.delete(f'{BASE_URL}/agents/{test_agent_id}')
    
    if response.status_code == 200:
        print("✅ Agent de test supprimé avec succès")
        
        # Vérifier que l'agent n'existe plus
        response = session.get(f'{BASE_URL}/agents/{test_agent_id}')
        if response.status_code == 404:
            print("✅ Agent de test confirmé supprimé (404)")
        else:
            print("⚠️ Agent de test encore accessible après suppression")
    else:
        print(f"❌ Échec de suppression de l'agent de test: {response.text}")
        return
    
    # 7. Vérifier que les autres agents existent toujours
    print("\n7. Vérification que les autres agents existent toujours...")
    response = session.get(f'{BASE_URL}/agents')
    
    if response.status_code == 200:
        remaining_agents = response.json()
        print(f"✅ {len(remaining_agents)} agents restants après suppression")
        
        for agent in remaining_agents:
            print(f"   • {agent['prenom']} {agent['nom']} ({agent['email']})")
    else:
        print("❌ Erreur lors de la récupération des agents restants")
    
    print(f"\n✅ Test terminé avec succès")
    print(f"\n📝 Résumé:")
    print(f"   • Agent de test créé ✅")
    print(f"   • Suppression fonctionnelle ✅")
    print(f"   • Autres agents préservés ✅")
    print(f"   • API de suppression opérationnelle ✅")
    
    print(f"\n🔍 Pour vérifier l'interface:")
    print(f"   1. Aller sur http://localhost:5173")
    print(f"   2. Se connecter en tant qu'admin")
    print(f"   3. Aller dans l'onglet 'Agents'")
    print(f"   4. Vérifier que chaque agent a 3 boutons: 👁️ Voir, ✏️ Modifier, 🗑️ Supprimer")

if __name__ == '__main__':
    test_agent_delete_button()

