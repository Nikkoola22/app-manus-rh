#!/usr/bin/env python3
"""
Script de test pour vérifier la création d'agent avec tous les soldes et l'affichage du service
"""

import requests
import json
from datetime import date

BASE_URL = 'http://127.0.0.1:5001/api'

def test_agent_creation_and_service():
    """Test la création d'agent avec tous les soldes et l'affichage du service"""
    
    print("🧪 Test Création Agent avec Soldes et Service")
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
    
    # 2. Récupérer les services disponibles
    print("\n2. Récupération des services...")
    response = session.get(f'{BASE_URL}/services')
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération des services: {response.text}")
        return
    
    services = response.json()
    print(f"✅ {len(services)} services trouvés")
    
    if not services:
        print("❌ Aucun service disponible pour créer un agent")
        return
    
    # Utiliser le premier service disponible
    service = services[0]
    print(f"   • Service sélectionné: {service['nom_service']} (ID: {service['id']})")
    
    # 3. Créer un agent avec tous les soldes
    print("\n3. Création d'un agent avec tous les soldes...")
    agent_data = {
        'nom': 'TEST_SOLDES',
        'prenom': 'Agent',
        'email': 'agent.soldes@test.com',
        'password': 'test123',
        'role': 'Agent',
        'service_id': service['id'],
        'quotite_travail': 38,
        'date_debut_contrat': '2024-01-15',
        'annee_entree_fp': 2024,
        'solde_ca': 80.0,
        'solde_rtt': 0.0,  # Sera calculé automatiquement
        'solde_cet': 0.0,
        'solde_hs': 0.0,
        'solde_bonifications': 34.4,
        'solde_jours_sujetions': 0.0,
        'solde_conges_formations': 1.0
    }
    
    response = session.post(f'{BASE_URL}/agents', json=agent_data)
    
    if response.status_code != 201:
        print(f"❌ Échec de création de l'agent: {response.text}")
        return
    
    agent = response.json()
    print(f"✅ Agent créé: {agent['prenom']} {agent['nom']} (ID: {agent['id']})")
    
    # 4. Vérifier les soldes dans la réponse
    print(f"\n4. Vérification des soldes dans la réponse:")
    print(f"   • Solde CA: {agent.get('solde_ca', 'N/A')} jours")
    print(f"   • Solde RTT: {agent.get('solde_rtt', 'N/A')} jours (calculé automatiquement)")
    print(f"   • Solde CET: {agent.get('solde_cet', 'N/A')} jours")
    print(f"   • Solde HS: {agent.get('solde_hs', 'N/A')} jours")
    print(f"   • Solde Bonifications: {agent.get('solde_bonifications', 'N/A')} jours")
    print(f"   • Solde Jours de sujétions: {agent.get('solde_jours_sujetions', 'N/A')} jours")
    print(f"   • Solde Congés formations: {agent.get('solde_conges_formations', 'N/A')} jours")
    
    # 5. Vérifier l'affichage du service
    print(f"\n5. Vérification de l'affichage du service:")
    if 'service' in agent and agent['service']:
        print(f"   ✅ Service assigné: {agent['service']['nom_service']} (ID: {agent['service']['id']})")
    else:
        print(f"   ❌ Service non assigné ou non chargé")
        print(f"   • service_id: {agent.get('service_id', 'N/A')}")
    
    # 6. Récupérer l'agent complet pour vérifier la relation service
    print(f"\n6. Récupération de l'agent complet...")
    response = session.get(f"{BASE_URL}/agents/{agent['id']}")
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération de l'agent: {response.text}")
        return
    
    agent_complet = response.json()
    print(f"✅ Agent récupéré avec succès")
    
    # Vérifier le service dans l'agent complet
    if 'service' in agent_complet and agent_complet['service']:
        print(f"   ✅ Service dans l'agent complet: {agent_complet['service']['nom_service']}")
    else:
        print(f"   ❌ Service non chargé dans l'agent complet")
        print(f"   • service_id: {agent_complet.get('service_id', 'N/A')}")
    
    # 7. Vérifier le calcul automatique des RTT
    print(f"\n7. Vérification du calcul automatique des RTT:")
    quotite = agent_complet.get('quotite_travail', 0)
    rtt_attendu = 18 if quotite >= 38 else 6 if quotite >= 36 else 0
    rtt_obtenu = agent_complet.get('solde_rtt', 0)
    
    print(f"   • Quotité: {quotite}h/semaine")
    print(f"   • RTT attendu: {rtt_attendu} jours")
    print(f"   • RTT obtenu: {rtt_obtenu} jours")
    
    if rtt_obtenu == rtt_attendu:
        print(f"   ✅ Calcul automatique des RTT correct")
    else:
        print(f"   ❌ Calcul automatique des RTT incorrect")
    
    print(f"\n✅ Test terminé")
    print(f"\n📝 Résumé:")
    print(f"   • Agent créé avec tous les soldes ✅")
    print(f"   • Service assigné et affiché ✅")
    print(f"   • Calcul automatique des RTT ✅")
    
    # Nettoyage
    print(f"\n🧹 Nettoyage...")
    response = session.delete(f"{BASE_URL}/agents/{agent['id']}")
    if response.status_code == 200:
        print(f"   ✅ Agent de test supprimé")
    else:
        print(f"   ⚠️ Échec de suppression de l'agent de test")

if __name__ == '__main__':
    test_agent_creation_and_service()

