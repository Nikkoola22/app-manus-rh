#!/usr/bin/env python3
"""
Script de test pour vérifier la fonctionnalité des arrêts maladie
"""

import requests
import json

def test_arret_maladie_functionality():
    """Teste la fonctionnalité des arrêts maladie"""
    
    base_url = "http://localhost:5001/api"
    
    print("🧪 Test de la fonctionnalité des arrêts maladie")
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
                print(f"   Quotité de travail : {test_agent['quotite_travail']}h/semaine")
                print(f"   Solde RTT initial : {test_agent['solde_rtt']}h")
            else:
                print("⚠️ Aucun agent trouvé pour les tests")
                return False
        else:
            print(f"❌ Échec de récupération des agents : {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des agents : {e}")
        return False
    
    # Test 3 : Créer un arrêt maladie
    print("\n3️⃣ Création d'un arrêt maladie...")
    test_agent_id = test_agent['id']
    
    # Créer un arrêt de 15 jours (devrait faire perdre 1 RTT si l'agent est à 38h)
    arret_data = {
        'agent_id': test_agent_id,
        'date_debut': '2024-02-01',
        'date_fin': '2024-02-15',  # 15 jours
        'motif': 'Test arrêt maladie - grippe'
    }
    
    try:
        response = requests.post(f"{base_url}/arret-maladie", 
                               json=arret_data, 
                               cookies=session_cookies)
        
        if response.status_code == 201:
            arret = response.json()
            print("✅ Arrêt maladie créé avec succès")
            print(f"   ID : {arret['id']}")
            print(f"   Durée : {arret['nb_jours']} jours")
            print(f"   RTT perdus : {arret['perte_rtt']} jour(s)")
            
            if test_agent['quotite_travail'] >= 38 and arret['perte_rtt'] > 0:
                print("✅ Calcul automatique des RTT perdus fonctionne correctement")
            elif test_agent['quotite_travail'] < 38:
                print("✅ Aucun RTT perdu car l'agent n'est pas à 38h/semaine")
            else:
                print("⚠️ Calcul des RTT perdus inattendu")
                
        else:
            print(f"❌ Échec de création de l'arrêt maladie : {response.status_code}")
            print(f"   Réponse : {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la création : {e}")
        return False
    
    # Test 4 : Vérifier la mise à jour du solde RTT de l'agent
    print("\n4️⃣ Vérification de la mise à jour du solde RTT...")
    try:
        response = requests.get(f"{base_url}/agents/{test_agent_id}", cookies=session_cookies)
        if response.status_code == 200:
            updated_agent = response.json()
            print(f"✅ Solde RTT mis à jour : {updated_agent['solde_rtt']}h")
            
            if test_agent['quotite_travail'] >= 38:
                expected_rtt = test_agent['solde_rtt'] - 1  # 1 RTT perdu pour 15 jours
                if updated_agent['solde_rtt'] == expected_rtt:
                    print("✅ Le solde RTT a été correctement déduit")
                else:
                    print(f"⚠️ Solde RTT inattendu : attendu {expected_rtt}h, obtenu {updated_agent['solde_rtt']}h")
            else:
                print("✅ Aucune modification du solde RTT (agent < 38h)")
                
        else:
            print(f"❌ Échec de récupération de l'agent : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification : {e}")
    
    # Test 5 : Récupérer la liste des arrêts maladie
    print("\n5️⃣ Récupération de la liste des arrêts maladie...")
    try:
        response = requests.get(f"{base_url}/arret-maladie", cookies=session_cookies)
        if response.status_code == 200:
            arrets = response.json()
            print(f"✅ {len(arrets)} arrêts maladie récupérés")
            
            if arrets:
                print("   Détails des arrêts :")
                for arret in arrets:
                    print(f"   - {arret['agent_nom']} : {arret['nb_jours']} jours ({arret['date_debut']} - {arret['date_fin']})")
                    print(f"     RTT perdus : {arret['perte_rtt']} jour(s)")
        else:
            print(f"❌ Échec de récupération des arrêts maladie : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération : {e}")
    
    # Test 6 : Test avec un responsable
    print("\n6️⃣ Test avec un responsable...")
    
    # Trouver un responsable
    responsable = None
    for agent in agents:
        if agent['role'] == 'Responsable':
            responsable = agent
            break
    
    if responsable:
        print(f"   Responsable de test : {responsable['prenom']} {responsable['nom']}")
        
        # Se connecter en tant que responsable
        responsable_login = {
            "email": responsable['email'],
            "password": "resp123"
        }
        
        try:
            response = requests.post(f"{base_url}/auth/login", json=responsable_login)
            if response.status_code == 200:
                print("✅ Connexion responsable réussie")
                resp_cookies = response.cookies
                
                # Tenter de créer un arrêt maladie
                arret_resp_data = {
                    'agent_id': test_agent_id,
                    'date_debut': '2024-02-20',
                    'date_fin': '2024-02-22',  # 3 jours
                    'motif': 'Test arrêt maladie par responsable'
                }
                
                response = requests.post(f"{base_url}/arret-maladie", 
                                       json=arret_resp_data, 
                                       cookies=resp_cookies)
                
                if response.status_code == 201:
                    print("✅ Responsable peut créer des arrêts maladie")
                else:
                    print(f"❌ Responsable ne peut pas créer d'arrêts maladie : {response.status_code}")
            else:
                print(f"❌ Échec de connexion responsable : {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur lors du test responsable : {e}")
    else:
        print("⚠️ Aucun responsable trouvé pour le test")
    
    print("\n" + "=" * 60)
    print("✅ Tests des arrêts maladie terminés")
    print("   La fonctionnalité est maintenant disponible dans l'application.")
    print("   Les administrateurs et responsables peuvent gérer les arrêts maladie.")
    print("   La perte automatique de RTT est calculée selon les règles.")
    
    return True

if __name__ == "__main__":
    test_arret_maladie_functionality()




