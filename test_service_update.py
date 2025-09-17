#!/usr/bin/env python3
"""
Script de test pour vérifier la mise à jour du service d'un agent
"""

import requests
import json
from datetime import date

BASE_URL = 'http://127.0.0.1:5001/api'

def test_service_update():
    """Test la mise à jour du service d'un agent"""
    
    print("🧪 Test Mise à Jour du Service d'un Agent")
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
    
    # 3. Récupérer les services
    print("\n3. Récupération des services...")
    response = session.get(f'{BASE_URL}/services')
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération des services: {response.text}")
        return
    
    services = response.json()
    print(f"✅ {len(services)} services trouvés")
    
    if len(services) < 2:
        print("❌ Besoin d'au moins 2 services pour le test")
        return
    
    # 4. Trouver un agent et un service différent
    agent = agents[0]  # Premier agent
    current_service_id = agent.get('service_id')
    
    # Trouver un service différent
    new_service = None
    for service in services:
        if service['id'] != current_service_id:
            new_service = service
            break
    
    if not new_service:
        print("❌ Aucun service différent trouvé")
        return
    
    print(f"\n4. Test de mise à jour du service:")
    print(f"   • Agent: {agent['prenom']} {agent['nom']} (ID: {agent['id']})")
    print(f"   • Service actuel: {current_service_id}")
    print(f"   • Nouveau service: {new_service['nom_service']} (ID: {new_service['id']})")
    
    # 5. Mettre à jour le service
    print(f"\n5. Mise à jour du service...")
    update_data = {'service_id': new_service['id']}
    response = session.put(f"{BASE_URL}/agents/{agent['id']}", json=update_data)
    
    if response.status_code != 200:
        print(f"❌ Échec de la mise à jour: {response.text}")
        return
    
    updated_agent = response.json()
    print(f"✅ Service mis à jour avec succès")
    print(f"   • Nouveau service_id: {updated_agent.get('service_id')}")
    
    # 6. Vérifier la mise à jour
    print(f"\n6. Vérification de la mise à jour...")
    response = session.get(f"{BASE_URL}/agents/{agent['id']}")
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération de l'agent: {response.text}")
        return
    
    final_agent = response.json()
    final_service_id = final_agent.get('service_id')
    
    if final_service_id == new_service['id']:
        print(f"✅ Service correctement mis à jour")
        print(f"   • Service final: {final_service_id}")
    else:
        print(f"❌ Service non mis à jour correctement")
        print(f"   • Attendu: {new_service['id']}")
        print(f"   • Obtenu: {final_service_id}")
        return
    
    # 7. Restaurer le service original
    print(f"\n7. Restauration du service original...")
    if current_service_id:
        restore_data = {'service_id': current_service_id}
        response = session.put(f"{BASE_URL}/agents/{agent['id']}", json=restore_data)
        
        if response.status_code == 200:
            print(f"✅ Service original restauré")
        else:
            print(f"⚠️ Échec de restauration du service original")
    else:
        print(f"ℹ️ Aucun service original à restaurer")
    
    print(f"\n✅ Test terminé avec succès")
    print(f"\n📝 Résumé:")
    print(f"   • Mise à jour du service via API PUT ✅")
    print(f"   • Vérification de la mise à jour ✅")
    print(f"   • Restauration du service original ✅")

if __name__ == '__main__':
    test_service_update()

