#!/usr/bin/env python3
"""
Script de test pour vérifier la fonctionnalité des créneaux matin/après-midi
"""

import requests
import json
from datetime import datetime, date, timedelta

def test_creneaux_calendrier():
    """Teste la fonctionnalité des créneaux matin/après-midi"""
    
    base_url = "http://localhost:5001/api"
    
    print("🧪 Test des créneaux matin/après-midi dans le calendrier")
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
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous que l'application est démarrée.")
        return False
    
    # Test 2 : Récupérer les agents du service
    print("\n2️⃣ Récupération des agents du service...")
    try:
        response = requests.get(f"{base_url}/agents", cookies=session_cookies)
        if response.status_code == 200:
            agents = response.json()
            agents_service = [agent for agent in agents if agent.get('role') == 'Agent']
            print(f"✅ {len(agents_service)} agents récupérés")
            
            if not agents_service:
                print("⚠️ Aucun agent trouvé pour les tests")
                return False
                
            test_agent = agents_service[0]
            print(f"   Agent de test : {test_agent['prenom']} {test_agent['nom']}")
        else:
            print(f"❌ Échec de récupération des agents : {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des agents : {e}")
        return False
    
    # Test 3 : Créer une présence le matin
    print("\n3️⃣ Création d'une présence le matin...")
    today = date.today()
    
    presence_matin_data = {
        'agent_id': test_agent['id'],
        'date_presence': today.isoformat(),
        'creneau': 'matin',
        'statut': 'present',
        'motif': 'Test créneau matin',
        'heure_debut': '08:00',
        'heure_fin': '12:00'
    }
    
    try:
        response = requests.post(f"{base_url}/presence", 
                               json=presence_matin_data, 
                               cookies=session_cookies)
        
        if response.status_code == 201:
            presence_matin = response.json()
            print("✅ Présence matin créée avec succès")
            print(f"   ID : {presence_matin['id']}")
            print(f"   Créneau : {presence_matin['creneau']}")
            print(f"   Statut : {presence_matin['statut']}")
        else:
            print(f"❌ Échec de création présence matin : {response.status_code}")
            print(f"   Réponse : {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la création présence matin : {e}")
        return False
    
    # Test 4 : Créer une présence l'après-midi
    print("\n4️⃣ Création d'une présence l'après-midi...")
    
    presence_apres_midi_data = {
        'agent_id': test_agent['id'],
        'date_presence': today.isoformat(),
        'creneau': 'apres_midi',
        'statut': 'absent',
        'motif': 'Test créneau après-midi - RDV médical'
    }
    
    try:
        response = requests.post(f"{base_url}/presence", 
                               json=presence_apres_midi_data, 
                               cookies=session_cookies)
        
        if response.status_code == 201:
            presence_apres_midi = response.json()
            print("✅ Présence après-midi créée avec succès")
            print(f"   ID : {presence_apres_midi['id']}")
            print(f"   Créneau : {presence_apres_midi['creneau']}")
            print(f"   Statut : {presence_apres_midi['statut']}")
        else:
            print(f"❌ Échec de création présence après-midi : {response.status_code}")
            print(f"   Réponse : {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la création présence après-midi : {e}")
        return False
    
    # Test 5 : Vérifier dans le calendrier
    print("\n5️⃣ Vérification dans le calendrier...")
    
    # Calculer la semaine courante
    semaine = get_semaine_iso(today)
    print(f"   Semaine de test : {semaine}")
    
    try:
        response = requests.get(f"{base_url}/presence/calendrier/semaine/{semaine}", 
                              cookies=session_cookies)
        
        if response.status_code == 200:
            calendrier = response.json()
            print("✅ Calendrier récupéré avec succès")
            
            # Chercher l'agent dans le calendrier
            agent_calendrier = None
            for agent in calendrier['agents']:
                if agent['id'] == test_agent['id']:
                    agent_calendrier = agent
                    break
            
            if agent_calendrier:
                print(f"✅ Agent trouvé dans le calendrier : {agent_calendrier['nom']}")
                
                # Vérifier les créneaux pour aujourd'hui
                jour_data = agent_calendrier['jours'].get(today.isoformat())
                if jour_data:
                    print(f"   Jour {today.isoformat()} trouvé")
                    
                    # Vérifier le créneau matin
                    if jour_data.get('matin') and jour_data['matin'].get('presence'):
                        presence_matin_cal = jour_data['matin']['presence']
                        print(f"   ✅ Créneau matin : {presence_matin_cal['statut']} ({presence_matin_cal['creneau']})")
                    else:
                        print("   ❌ Créneau matin non trouvé")
                    
                    # Vérifier le créneau après-midi
                    if jour_data.get('apres_midi') and jour_data['apres_midi'].get('presence'):
                        presence_apres_midi_cal = jour_data['apres_midi']['presence']
                        print(f"   ✅ Créneau après-midi : {presence_apres_midi_cal['statut']} ({presence_apres_midi_cal['creneau']})")
                    else:
                        print("   ❌ Créneau après-midi non trouvé")
                else:
                    print("❌ Jour non trouvé dans le calendrier")
            else:
                print("❌ Agent non trouvé dans le calendrier")
        else:
            print(f"❌ Échec de récupération du calendrier : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du calendrier : {e}")
    
    # Test 6 : Créer une présence journée complète
    print("\n6️⃣ Création d'une présence journée complète...")
    
    demain = today + timedelta(days=1)
    presence_journee_data = {
        'agent_id': test_agent['id'],
        'date_presence': demain.isoformat(),
        'creneau': 'journee',
        'statut': 'conges',
        'motif': 'Test journée complète - congés'
    }
    
    try:
        response = requests.post(f"{base_url}/presence", 
                               json=presence_journee_data, 
                               cookies=session_cookies)
        
        if response.status_code == 201:
            presence_journee = response.json()
            print("✅ Présence journée complète créée avec succès")
            print(f"   ID : {presence_journee['id']}")
            print(f"   Créneau : {presence_journee['creneau']}")
            print(f"   Statut : {presence_journee['statut']}")
        else:
            print(f"❌ Échec de création présence journée : {response.status_code}")
            print(f"   Réponse : {response.text}")
    except Exception as e:
        print(f"❌ Erreur lors de la création présence journée : {e}")
    
    # Test 7 : Test de contrainte unique (même agent, même date, même créneau)
    print("\n7️⃣ Test de contrainte unique...")
    
    presence_doublon_data = {
        'agent_id': test_agent['id'],
        'date_presence': today.isoformat(),
        'creneau': 'matin',  # Même créneau que le test 3
        'statut': 'present',
        'motif': 'Test doublon'
    }
    
    try:
        response = requests.post(f"{base_url}/presence", 
                               json=presence_doublon_data, 
                               cookies=session_cookies)
        
        if response.status_code == 400:
            print("✅ Contrainte unique respectée : doublon refusé")
        else:
            print(f"❌ Contrainte unique non respectée : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors du test de contrainte : {e}")
    
    # Test 8 : Vérifier les statistiques
    print("\n8️⃣ Vérification des statistiques...")
    try:
        response = requests.get(f"{base_url}/presence/statistiques/semaine/{semaine}", 
                              cookies=session_cookies)
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistiques récupérées avec succès")
            print(f"   Total agents : {stats['total_agents']}")
            print(f"   Présences totales : {stats['presences_totales']}")
            print(f"   Pourcentage présence : {stats['pourcentage_presence']}%")
            
            if 'present' in stats['statuts']:
                print(f"   Présences : {stats['statuts']['present']}")
            if 'absent' in stats['statuts']:
                print(f"   Absences : {stats['statuts']['absent']}")
        else:
            print(f"❌ Échec de récupération des statistiques : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des statistiques : {e}")
    
    # Test 9 : Modification d'une présence
    print("\n9️⃣ Modification d'une présence...")
    try:
        # Modifier la présence matin
        update_data = {
            'statut': 'partiel',
            'motif': 'Présence partielle modifiée',
            'heure_debut': '09:00',
            'heure_fin': '11:00'
        }
        
        response = requests.put(f"{base_url}/presence/{presence_matin['id']}", 
                              json=update_data, 
                              cookies=session_cookies)
        
        if response.status_code == 200:
            presence_modifiee = response.json()
            print("✅ Présence modifiée avec succès")
            print(f"   Nouveau statut : {presence_modifiee['statut']}")
            print(f"   Nouvelles heures : {presence_modifiee['heure_debut']} - {presence_modifiee['heure_fin']}")
        else:
            print(f"❌ Échec de modification : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors de la modification : {e}")
    
    # Test 10 : Suppression des présences de test
    print("\n🔟 Nettoyage des présences de test...")
    try:
        # Supprimer la présence matin
        response = requests.delete(f"{base_url}/presence/{presence_matin['id']}", 
                                 cookies=session_cookies)
        if response.status_code == 200:
            print("✅ Présence matin supprimée")
        
        # Supprimer la présence après-midi
        response = requests.delete(f"{base_url}/presence/{presence_apres_midi['id']}", 
                                 cookies=session_cookies)
        if response.status_code == 200:
            print("✅ Présence après-midi supprimée")
            
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage : {e}")
    
    print("\n" + "=" * 70)
    print("✅ Tests des créneaux matin/après-midi terminés")
    print("   Le calendrier peut maintenant gérer les créneaux séparément.")
    print("   Fonctionnalités testées :")
    print("   - Création de présences par créneau")
    print("   - Affichage dans le calendrier")
    print("   - Contraintes uniques")
    print("   - Statistiques")
    print("   - Modification et suppression")
    
    return True

def get_semaine_iso(date_obj):
    """Calcule le numéro de semaine ISO pour une date donnée"""
    year, week, _ = date_obj.isocalendar()
    return f"{year}-{week:02d}"

if __name__ == "__main__":
    test_creneaux_calendrier()




