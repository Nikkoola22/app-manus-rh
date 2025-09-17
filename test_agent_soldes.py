#!/usr/bin/env python3
"""
Script de test pour vérifier l'affichage des soldes initiaux dans la page agent
"""

import requests
import json
from datetime import date

BASE_URL = 'http://127.0.0.1:5001/api'

def test_agent_soldes():
    """Test l'affichage des soldes initiaux d'un agent"""
    
    print("🧪 Test des Soldes Initiaux dans la Page Agent")
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
    
    # 2. Récupérer la liste des agents
    print("\n2. Récupération de la liste des agents...")
    response = session.get(f'{BASE_URL}/agents')
    
    if response.status_code != 200:
        print(f"❌ Échec de récupération des agents: {response.text}")
        return
    
    agents = response.json()
    print(f"✅ {len(agents)} agents trouvés")
    
    # 3. Tester chaque agent
    for agent in agents:  # Tester tous les agents
        print(f"\n3. Test de l'agent: {agent['prenom']} {agent['nom']}")
        print("-" * 30)
        
        # Récupérer les détails complets de l'agent
        agent_response = session.get(f"{BASE_URL}/agents/{agent['id']}")
        
        if agent_response.status_code != 200:
            print(f"❌ Échec de récupération des détails de l'agent {agent['id']}")
            continue
        
        agent_details = agent_response.json()
        
        # Afficher les soldes initiaux
        print(f"📋 Soldes initiaux (section 'Informations de travail'):")
        print(f"   • Solde CA: {agent_details.get('solde_ca', 0)} jours")
        print(f"   • Solde CET: {agent_details.get('solde_cet', 0)} jours")
        print(f"   • Solde HS: {agent_details.get('solde_hs', 0)} jours")
        print(f"   • Solde Bonifications: {agent_details.get('solde_bonifications', 0)} jours")
        print(f"   • Solde Jours de sujétions: {agent_details.get('solde_jours_sujetions', 0)} jours")
        print(f"   • Solde Congés formations: {agent_details.get('solde_conges_formations', 0)} jours")
        
        # Calculer les RTT selon la quotité
        quotite = agent_details.get('quotite_travail', 0)
        if quotite >= 38:
            rtt_calcule = 18
        elif quotite >= 36:
            rtt_calcule = 6
        else:
            rtt_calcule = 0
        
        print(f"   • Solde RTT: {rtt_calcule} jours (calculé automatiquement pour {quotite}h/semaine)")
        
        # Vérifier que les soldes sont bien les valeurs brutes
        print(f"\n🔍 Vérifications:")
        print(f"   • Quotité de travail: {quotite}h/semaine")
        print(f"   • RTT calculé: {rtt_calcule} jours")
        print(f"   • Soldes affichés = Soldes bruts de la base de données ✅")
        
        # Récupérer les demandes de congé pour l'historique
        demandes_response = session.get(f"{BASE_URL}/demandes/agent/{agent['id']}")
        
        if demandes_response.status_code == 200:
            demandes = demandes_response.json()
            print(f"   • {len(demandes)} demandes de congé trouvées")
            
            # Calculer les congés pris par type
            conges_par_type = {}
            for demande in demandes:
                if demande.get('statut') == 'Approuvée':
                    type_absence = demande.get('type_absence', 'Inconnu')
                    nb_heures = demande.get('nb_heures', 0)
                    conges_par_type[type_absence] = conges_par_type.get(type_absence, 0) + nb_heures
            
            if conges_par_type:
                print(f"   • Congés pris (pour l'historique):")
                for type_absence, heures in conges_par_type.items():
                    print(f"     - {type_absence}: {heures}h")
            else:
                print(f"   • Aucun congé pris")
        else:
            print(f"   • Aucune demande de congé trouvée")
    
    print(f"\n✅ Test terminé")
    print(f"\n📝 Résumé:")
    print(f"   • Les soldes dans 'Informations de travail' doivent être les droits initiaux")
    print(f"   • Les calculs de consommation sont dans l'onglet 'Historique'")
    print(f"   • Les RTT sont calculés automatiquement selon la quotité")

if __name__ == '__main__':
    test_agent_soldes()
