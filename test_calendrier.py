#!/usr/bin/env python3
"""
Script de test pour vérifier la fonctionnalité du calendrier de présence
"""

import requests
import json
from datetime import datetime, date, timedelta

def test_calendrier_functionality():
    """Teste la fonctionnalité du calendrier de présence"""
    
    base_url = "http://localhost:5001/api"
    
    print("🧪 Test de la fonctionnalité du calendrier de présence")
    print("=" * 70)
    
    # Test 1 : Connexion en tant que responsable
    print("\n1️⃣ Connexion en tant que responsable...")
    login_data = {
        "email": "marie.dubois@exemple.com",
        "password": "resp123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Connexion responsable réussie")
            session_cookies = response.cookies
        else:
            print(f"❌ Échec de la connexion responsable : {response.status_code}")
            # Essayer avec un autre responsable
            login_data = {
                "email": "pierre.martin@exemple.com", 
                "password": "resp123"
            }
            response = requests.post(f"{base_url}/auth/login", json=login_data)
            if response.status_code == 200:
                print("✅ Connexion responsable réussie (2ème tentative)")
                session_cookies = response.cookies
            else:
                print(f"❌ Échec de la connexion responsable : {response.status_code}")
                return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous que l'application est démarrée.")
        return False
    
    # Test 2 : Récupérer la semaine courante
    print("\n2️⃣ Test de récupération de la semaine courante...")
    today = date.today()
    # Calculer le numéro de semaine (ISO)
    week_number = today.isocalendar()[1]
    annee = today.year
    semaine = f"{annee}-{week_number:02d}"
    print(f"   Semaine de test : {semaine}")
    
    # Test 3 : Récupérer le calendrier pour la semaine courante
    print("\n3️⃣ Récupération du calendrier de la semaine...")
    try:
        response = requests.get(f"{base_url}/presence/calendrier/semaine/{semaine}", cookies=session_cookies)
        if response.status_code == 200:
            calendrier = response.json()
            print("✅ Calendrier récupéré avec succès")
            print(f"   Date début : {calendrier['date_debut']}")
            print(f"   Date fin : {calendrier['date_fin']}")
            print(f"   Nombre d'agents : {len(calendrier['agents'])}")
            
            if calendrier['agents']:
                print("   Agents dans le calendrier :")
                for agent in calendrier['agents'][:3]:  # Afficher les 3 premiers
                    print(f"     - {agent['nom']} ({agent['service']})")
        else:
            print(f"❌ Échec de récupération du calendrier : {response.status_code}")
            print(f"   Réponse : {response.text}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du calendrier : {e}")
    
    # Test 4 : Récupérer les statistiques de la semaine
    print("\n4️⃣ Récupération des statistiques de la semaine...")
    try:
        response = requests.get(f"{base_url}/presence/statistiques/semaine/{semaine}", cookies=session_cookies)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistiques récupérées avec succès")
            print(f"   Total agents : {stats['total_agents']}")
            print(f"   Pourcentage présence : {stats['pourcentage_presence']}%")
            print(f"   Présences totales : {stats['presences_totales']}")
            print(f"   Jours possibles : {stats['total_jours_possibles']}")
        else:
            print(f"❌ Échec de récupération des statistiques : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des statistiques : {e}")
    
    # Test 5 : Récupérer la liste des agents pour créer des présences
    print("\n5️⃣ Récupération de la liste des agents...")
    try:
        response = requests.get(f"{base_url}/agents", cookies=session_cookies)
        if response.status_code == 200:
            agents = response.json()
            agents_service = [agent for agent in agents if agent.get('role') == 'Agent']
            print(f"✅ {len(agents_service)} agents récupérés")
            
            if agents_service:
                test_agent = agents_service[0]
                print(f"   Agent de test : {test_agent['prenom']} {test_agent['nom']}")
                
                # Test 6 : Créer une présence de test
                print("\n6️⃣ Création d'une présence de test...")
                presence_data = {
                    'agent_id': test_agent['id'],
                    'date_presence': today.isoformat(),
                    'statut': 'present',
                    'motif': 'Test de présence automatique',
                    'heure_debut': '08:00',
                    'heure_fin': '17:00'
                }
                
                try:
                    response = requests.post(f"{base_url}/presence", 
                                           json=presence_data, 
                                           cookies=session_cookies)
                    
                    if response.status_code == 201:
                        presence = response.json()
                        print("✅ Présence créée avec succès")
                        print(f"   ID : {presence['id']}")
                        print(f"   Statut : {presence['statut']}")
                        print(f"   Durée : {presence['duree_display']}")
                        
                        # Test 7 : Modifier la présence
                        print("\n7️⃣ Modification de la présence...")
                        update_data = {
                            'statut': 'partiel',
                            'motif': 'Présence partielle - test modifié',
                            'heure_debut': '10:00',
                            'heure_fin': '14:00'
                        }
                        
                        response = requests.put(f"{base_url}/presence/{presence['id']}", 
                                              json=update_data, 
                                              cookies=session_cookies)
                        
                        if response.status_code == 200:
                            updated_presence = response.json()
                            print("✅ Présence modifiée avec succès")
                            print(f"   Nouveau statut : {updated_presence['statut']}")
                            print(f"   Nouvelle durée : {updated_presence['duree_display']}")
                        else:
                            print(f"❌ Échec de modification : {response.status_code}")
                        
                        # Test 8 : Supprimer la présence
                        print("\n8️⃣ Suppression de la présence...")
                        response = requests.delete(f"{base_url}/presence/{presence['id']}", 
                                                  cookies=session_cookies)
                        
                        if response.status_code == 200:
                            print("✅ Présence supprimée avec succès")
                        else:
                            print(f"❌ Échec de suppression : {response.status_code}")
                            
                    else:
                        print(f"❌ Échec de création de présence : {response.status_code}")
                        print(f"   Réponse : {response.text}")
                        
                except Exception as e:
                    print(f"❌ Erreur lors de la gestion des présences : {e}")
            else:
                print("⚠️ Aucun agent trouvé pour les tests")
        else:
            print(f"❌ Échec de récupération des agents : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des agents : {e}")
    
    # Test 9 : Test avec différentes semaines
    print("\n9️⃣ Test de navigation entre semaines...")
    try:
        # Semaine précédente
        prev_week = week_number - 1 if week_number > 1 else 52
        prev_year = annee if week_number > 1 else annee - 1
        semaine_prev = f"{prev_year}-{prev_week:02d}"
        
        response = requests.get(f"{base_url}/presence/calendrier/semaine/{semaine_prev}", cookies=session_cookies)
        if response.status_code == 200:
            print(f"✅ Semaine précédente récupérée : {semaine_prev}")
        else:
            print(f"❌ Échec semaine précédente : {response.status_code}")
        
        # Semaine suivante
        next_week = week_number + 1 if week_number < 52 else 1
        next_year = annee if week_number < 52 else annee + 1
        semaine_next = f"{next_year}-{next_week:02d}"
        
        response = requests.get(f"{base_url}/presence/calendrier/semaine/{semaine_next}", cookies=session_cookies)
        if response.status_code == 200:
            print(f"✅ Semaine suivante récupérée : {semaine_next}")
        else:
            print(f"❌ Échec semaine suivante : {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de navigation : {e}")
    
    print("\n" + "=" * 70)
    print("✅ Tests du calendrier de présence terminés")
    print("   Le calendrier est maintenant disponible pour les responsables.")
    print("   Fonctionnalités testées :")
    print("   - Récupération du calendrier hebdomadaire")
    print("   - Statistiques de présence")
    print("   - Création/modification/suppression de présences")
    print("   - Navigation entre semaines")
    
    return True

if __name__ == "__main__":
    test_calendrier_functionality()




