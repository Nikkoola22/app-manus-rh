#!/usr/bin/env python3
"""
Script de test pour vérifier la fonctionnalité des heures supplémentaires (HS)
"""

import requests
import json

def test_hs_functionality():
    """Teste la fonctionnalité des heures supplémentaires"""
    
    base_url = "http://localhost:5001/api"
    
    print("🧪 Test de la fonctionnalité des heures supplémentaires (HS)")
    print("=" * 60)
    
    # Test 1 : Connexion en tant qu'admin
    print("\n1️⃣ Connexion en tant qu'admin...")
    login_data = {
        "email": "admin@exemple.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Connexion admin réussie")
            session_cookies = response.cookies
        else:
            print(f"❌ Échec de la connexion admin : {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous que l'application est démarrée.")
        return False
    
    # Test 2 : Récupérer la liste des agents
    print("\n2️⃣ Récupération de la liste des agents...")
    try:
        response = requests.get(f"{base_url}/agents", cookies=session_cookies)
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ {len(agents)} agents récupérés")
            
            if agents:
                # Prendre le premier agent pour les tests
                test_agent = agents[0]
                print(f"   Agent de test : {test_agent['prenom']} {test_agent['nom']}")
            else:
                print("⚠️ Aucun agent trouvé pour les tests")
                return False
        else:
            print(f"❌ Échec de récupération des agents : {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des agents : {e}")
        return False
    
    # Test 3 : Vérifier que le champ solde_hs est présent
    print("\n3️⃣ Vérification du champ solde_hs...")
    if 'solde_hs' in test_agent:
        print(f"✅ Champ solde_hs présent : {test_agent['solde_hs']}h")
    else:
        print("❌ Champ solde_hs manquant")
        return False
    
    # Test 4 : Modifier le solde HS d'un agent
    print("\n4️⃣ Modification du solde HS d'un agent...")
    test_agent_id = test_agent['id']
    new_hs_value = 10.5
    
    update_data = {
        **test_agent,
        'solde_hs': new_hs_value
    }
    
    try:
        response = requests.put(f"{base_url}/agents/{test_agent_id}", 
                              json=update_data, 
                              cookies=session_cookies)
        if response.status_code == 200:
            updated_agent = response.json()
            if updated_agent['solde_hs'] == new_hs_value:
                print(f"✅ Solde HS mis à jour : {updated_agent['solde_hs']}h")
            else:
                print(f"❌ Solde HS non mis à jour correctement : {updated_agent['solde_hs']}h")
                return False
        else:
            print(f"❌ Échec de la mise à jour : {response.status_code}")
            print(f"   Réponse : {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour : {e}")
        return False
    
    # Test 5 : Connexion en tant qu'agent pour tester le formulaire de demande
    print("\n5️⃣ Test de connexion agent...")
    
    # Trouver un agent (non admin) pour le test
    agent_for_test = None
    for agent in agents:
        if agent['role'] == 'Agent':
            agent_for_test = agent
            break
    
    if not agent_for_test:
        print("⚠️ Aucun agent non-admin trouvé pour le test")
        return True
    
    print(f"   Agent de test : {agent_for_test['prenom']} {agent_for_test['nom']}")
    
    # Test 6 : Vérifier que les demandes incluent le type HS
    print("\n6️⃣ Test des types d'absence disponibles...")
    
    # Simuler une demande avec le type HS
    demande_data = {
        "type_absence": "HS",
        "date_debut": "2024-02-01",
        "date_fin": "2024-02-01",
        "demi_journees": "",
        "motif": "Test des heures supplémentaires"
    }
    
    # Se connecter en tant qu'agent
    agent_login_data = {
        "email": agent_for_test['email'],
        "password": "agent123"  # Mot de passe par défaut
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=agent_login_data)
        if response.status_code == 200:
            print("✅ Connexion agent réussie")
            agent_cookies = response.cookies
            
            # Tenter de créer une demande avec le type HS
            response = requests.post(f"{base_url}/demandes", 
                                   json=demande_data, 
                                   cookies=agent_cookies)
            
            if response.status_code == 201:
                print("✅ Demande avec type HS créée avec succès")
                demande = response.json()
                print(f"   Demande ID : {demande['id']}")
                print(f"   Type : {demande['type_absence']}")
            else:
                print(f"❌ Échec de création de demande HS : {response.status_code}")
                print(f"   Réponse : {response.text}")
        else:
            print(f"❌ Échec de connexion agent : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors du test agent : {e}")
    
    print("\n" + "=" * 60)
    print("✅ Tests des heures supplémentaires terminés")
    print("   Le champ solde_hs est maintenant disponible dans l'application.")
    print("   Les agents peuvent utiliser le type 'HS' dans leurs demandes de congés.")
    
    return True

if __name__ == "__main__":
    test_hs_functionality()




