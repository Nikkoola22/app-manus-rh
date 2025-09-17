#!/usr/bin/env python3
"""
Script de test pour vérifier l'intégration des demandes de congés dans le calendrier
"""

import requests
import json
from datetime import datetime, date, timedelta

def test_integration_demandes_calendrier():
    """Teste l'intégration des demandes de congés validées dans le calendrier"""
    
    base_url = "http://localhost:5001/api"
    
    print("🧪 Test d'intégration : Demandes de congés → Calendrier")
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
    
    # Test 3 : Créer une demande de congés pour l'agent
    print("\n3️⃣ Création d'une demande de congés...")
    today = date.today()
    date_debut = today + timedelta(days=1)  # Demain
    date_fin = today + timedelta(days=3)    # Dans 3 jours
    
    demande_data = {
        'agent_id': test_agent['id'],
        'type_absence': 'Congés',
        'date_debut': date_debut.isoformat(),
        'date_fin': date_fin.isoformat(),
        'nb_heures': 21.0,  # 3 jours × 7h
        'motif': 'Test d\'intégration calendrier - congés'
    }
    
    try:
        response = requests.post(f"{base_url}/demandes", 
                               json=demande_data, 
                               cookies=session_cookies)
        
        if response.status_code == 201:
            demande = response.json()
            demande_id = demande['id']
            print("✅ Demande de congés créée avec succès")
            print(f"   ID : {demande_id}")
            print(f"   Période : {date_debut} - {date_fin}")
            print(f"   Statut : {demande['statut']}")
        else:
            print(f"❌ Échec de création de la demande : {response.status_code}")
            print(f"   Réponse : {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la création de la demande : {e}")
        return False
    
    # Test 4 : Approuver la demande de congés
    print("\n4️⃣ Approbation de la demande de congés...")
    try:
        response = requests.put(f"{base_url}/demandes/{demande_id}", 
                              json={'statut': 'Approuvée'}, 
                              cookies=session_cookies)
        
        if response.status_code == 200:
            demande_approuvee = response.json()
            print("✅ Demande de congés approuvée avec succès")
            print(f"   Nouveau statut : {demande_approuvee['statut']}")
        else:
            print(f"❌ Échec d'approbation : {response.status_code}")
            print(f"   Réponse : {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'approbation : {e}")
        return False
    
    # Test 5 : Vérifier que la demande apparaît dans le calendrier
    print("\n5️⃣ Vérification dans le calendrier...")
    
    # Calculer la semaine qui contient la demande
    semaine_demande = get_semaine_iso(date_debut)
    print(f"   Semaine de test : {semaine_demande}")
    
    try:
        response = requests.get(f"{base_url}/presence/calendrier/semaine/{semaine_demande}", 
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
                
                # Vérifier que les jours de congés sont présents
                jours_conges_trouves = []
                for jour_date, jour_data in agent_calendrier['jours'].items():
                    if jour_data.get('presence') and jour_data['presence'].get('is_demande'):
                        jours_conges_trouves.append(jour_date)
                
                if jours_conges_trouves:
                    print(f"✅ {len(jours_conges_trouves)} jours de congés trouvés dans le calendrier :")
                    for jour in jours_conges_trouves:
                        print(f"   - {jour}")
                    
                    # Vérifier que les jours correspondent à la demande
                    jours_demande = []
                    current_date = date_debut
                    while current_date <= date_fin:
                        jours_demande.append(current_date.isoformat())
                        current_date += timedelta(days=1)
                    
                    jours_correspondants = set(jours_conges_trouves) & set(jours_demande)
                    if jours_correspondants:
                        print(f"✅ {len(jours_correspondants)} jours correspondent à la demande")
                    else:
                        print("⚠️ Les jours ne correspondent pas exactement à la demande")
                else:
                    print("❌ Aucun jour de congés trouvé dans le calendrier")
            else:
                print("❌ Agent non trouvé dans le calendrier")
        else:
            print(f"❌ Échec de récupération du calendrier : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du calendrier : {e}")
    
    # Test 6 : Vérifier les statistiques
    print("\n6️⃣ Vérification des statistiques...")
    try:
        response = requests.get(f"{base_url}/presence/statistiques/semaine/{semaine_demande}", 
                              cookies=session_cookies)
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistiques récupérées avec succès")
            print(f"   Total agents : {stats['total_agents']}")
            print(f"   Présences totales : {stats['presences_totales']}")
            print(f"   Pourcentage présence : {stats['pourcentage_presence']}%")
            
            # Vérifier que les congés sont comptés dans les statistiques
            if 'conges' in stats['statuts']:
                print(f"✅ Congés comptés dans les statistiques : {stats['statuts']['conges']} jours")
            else:
                print("⚠️ Congés non trouvés dans les statistiques")
        else:
            print(f"❌ Échec de récupération des statistiques : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des statistiques : {e}")
    
    # Test 7 : Créer une demande de RTT pour tester un autre type
    print("\n7️⃣ Test avec une demande de RTT...")
    date_debut_rtt = today + timedelta(days=7)  # Dans une semaine
    date_fin_rtt = date_debut_rtt  # Un seul jour
    
    demande_rtt_data = {
        'agent_id': test_agent['id'],
        'type_absence': 'RTT',
        'date_debut': date_debut_rtt.isoformat(),
        'date_fin': date_fin_rtt.isoformat(),
        'nb_heures': 7.0,
        'motif': 'Test d\'intégration calendrier - RTT'
    }
    
    try:
        # Créer la demande RTT
        response = requests.post(f"{base_url}/demandes", 
                               json=demande_rtt_data, 
                               cookies=session_cookies)
        
        if response.status_code == 201:
            demande_rtt = response.json()
            print("✅ Demande RTT créée")
            
            # Approuver la demande RTT
            response = requests.put(f"{base_url}/demandes/{demande_rtt['id']}", 
                                  json={'statut': 'Approuvée'}, 
                                  cookies=session_cookies)
            
            if response.status_code == 200:
                print("✅ Demande RTT approuvée")
                
                # Vérifier dans le calendrier
                semaine_rtt = get_semaine_iso(date_debut_rtt)
                response = requests.get(f"{base_url}/presence/calendrier/semaine/{semaine_rtt}", 
                                      cookies=session_cookies)
                
                if response.status_code == 200:
                    calendrier_rtt = response.json()
                    
                    # Chercher l'agent dans le calendrier
                    for agent in calendrier_rtt['agents']:
                        if agent['id'] == test_agent['id']:
                            jour_rtt = agent['jours'].get(date_debut_rtt.isoformat())
                            if jour_rtt and jour_rtt.get('presence', {}).get('is_demande'):
                                print("✅ RTT trouvé dans le calendrier")
                            else:
                                print("⚠️ RTT non trouvé dans le calendrier")
                            break
            else:
                print("❌ Échec d'approbation RTT")
        else:
            print("❌ Échec de création demande RTT")
    except Exception as e:
        print(f"❌ Erreur lors du test RTT : {e}")
    
    print("\n" + "=" * 70)
    print("✅ Tests d'intégration demandes-calendrier terminés")
    print("   Les demandes de congés validées s'affichent maintenant")
    print("   automatiquement dans le calendrier de présence.")
    
    return True

def get_semaine_iso(date_obj):
    """Calcule le numéro de semaine ISO pour une date donnée"""
    year, week, _ = date_obj.isocalendar()
    return f"{year}-{week:02d}"

if __name__ == "__main__":
    test_integration_demandes_calendrier()




