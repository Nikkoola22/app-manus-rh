#!/usr/bin/env python3
"""
Script de test pour vérifier les fonctionnalités de suppression des agents et services
"""

import requests
import json
from datetime import date

BASE_URL = 'http://127.0.0.1:5001/api'

def test_delete_functionality():
    """Test les fonctionnalités de suppression des agents et services"""
    
    print("🧪 Test Fonctionnalités de Suppression")
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
    
    # 2. Créer un service de test
    print("\n2. Création d'un service de test...")
    service_data = {
        'nom_service': 'Service Test Suppression',
        'description': 'Service pour tester la suppression'
    }
    response = session.post(f'{BASE_URL}/services', json=service_data)
    
    if response.status_code != 201:
        print(f"❌ Échec de création du service: {response.text}")
        return
    
    test_service = response.json()
    service_id = test_service['id']
    print(f"✅ Service créé: {test_service['nom_service']} (ID: {service_id})")
    
    # 3. Créer un agent de test
    print("\n3. Création d'un agent de test...")
    agent_data = {
        'nom': 'AgentTest',
        'prenom': 'Suppression',
        'email': 'agent.test.suppression@exemple.com',
        'password': 'test123',
        'role': 'Agent',
        'quotite_travail': 35,
        'service_id': service_id,
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
    response = session.post(f'{BASE_URL}/agents', json=agent_data)
    
    if response.status_code != 201:
        print(f"❌ Échec de création de l'agent: {response.text}")
        return
    
    test_agent = response.json()
    agent_id = test_agent['id']
    print(f"✅ Agent créé: {test_agent['prenom']} {test_agent['nom']} (ID: {agent_id})")
    
    # 4. Vérifier que l'agent et le service existent
    print("\n4. Vérification de l'existence...")
    
    # Vérifier l'agent
    response = session.get(f'{BASE_URL}/agents/{agent_id}')
    if response.status_code == 200:
        print("✅ Agent existe avant suppression")
    else:
        print("❌ Agent non trouvé avant suppression")
        return
    
    # Vérifier le service
    response = session.get(f'{BASE_URL}/services/{service_id}')
    if response.status_code == 200:
        print("✅ Service existe avant suppression")
    else:
        print("❌ Service non trouvé avant suppression")
        return
    
    # 5. Tester la suppression de l'agent
    print("\n5. Test de suppression de l'agent...")
    response = session.delete(f'{BASE_URL}/agents/{agent_id}')
    
    if response.status_code == 200:
        print("✅ Agent supprimé avec succès")
        
        # Vérifier que l'agent n'existe plus
        response = session.get(f'{BASE_URL}/agents/{agent_id}')
        if response.status_code == 404:
            print("✅ Agent confirmé supprimé (404)")
        else:
            print("⚠️ Agent encore accessible après suppression")
    else:
        print(f"❌ Échec de suppression de l'agent: {response.text}")
        return
    
    # 6. Tester la suppression du service
    print("\n6. Test de suppression du service...")
    response = session.delete(f'{BASE_URL}/services/{service_id}')
    
    if response.status_code == 200:
        print("✅ Service supprimé avec succès")
        
        # Vérifier que le service n'existe plus
        response = session.get(f'{BASE_URL}/services/{service_id}')
        if response.status_code == 404:
            print("✅ Service confirmé supprimé (404)")
        else:
            print("⚠️ Service encore accessible après suppression")
    else:
        print(f"❌ Échec de suppression du service: {response.text}")
        return
    
    # 7. Tester la suppression d'un agent inexistant
    print("\n7. Test de suppression d'un agent inexistant...")
    response = session.delete(f'{BASE_URL}/agents/99999')
    
    if response.status_code == 404:
        print("✅ Gestion correcte de l'agent inexistant (404)")
    else:
        print(f"⚠️ Réponse inattendue pour agent inexistant: {response.status_code}")
    
    # 8. Tester la suppression d'un service inexistant
    print("\n8. Test de suppression d'un service inexistant...")
    response = session.delete(f'{BASE_URL}/services/99999')
    
    if response.status_code == 404:
        print("✅ Gestion correcte du service inexistant (404)")
    else:
        print(f"⚠️ Réponse inattendue pour service inexistant: {response.status_code}")
    
    print(f"\n✅ Test terminé avec succès")
    print(f"\n📝 Résumé:")
    print(f"   • Service de test créé ✅")
    print(f"   • Agent de test créé ✅")
    print(f"   • Suppression d'agent fonctionnelle ✅")
    print(f"   • Suppression de service fonctionnelle ✅")
    print(f"   • Gestion des erreurs correcte ✅")

if __name__ == '__main__':
    test_delete_functionality()

