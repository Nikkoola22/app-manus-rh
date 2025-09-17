#!/usr/bin/env python3
"""
Test de la visualisation du planning sur la page de l'agent
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_planning_agent():
    """Test de la visualisation du planning sur la page de l'agent"""
    print("👤 Test de la visualisation du planning sur la page de l'agent")
    print("=" * 60)
    
    app_dir = Path(__file__).parent.absolute()
    python_cmd = str(app_dir / "venv" / "bin" / "python")
    
    # Démarrer Flask
    print("🐍 Démarrage de Flask...")
    flask_process = subprocess.Popen(
        [python_cmd, "main.py"],
        cwd=app_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Attendre que Flask démarre
    time.sleep(3)
    
    try:
        # Test 1: Connexion Agent
        print("\n👤 Test de connexion Agent...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'marie.dupont@exemple.com', 'password': 'agent123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion Agent réussie")
            print(f"   Nom: {data['user']['prenom']} {data['user']['nom']}")
            print(f"   Rôle: {data['user']['role']}")
            print(f"   ID: {data['user']['id']}")
            
            # Récupérer les cookies de session
            cookies = response.cookies
            agent_id = data['user']['id']
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test 2: Vérifier que l'agent peut accéder à son planning
        print(f"\n📅 Test d'accès au planning de l'agent {agent_id}...")
        response = requests.get(f'http://localhost:5001/api/planning/agent/{agent_id}', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            planning_data = response.json()
            print(f"✅ Planning accessible par l'agent")
            print(f"   Jours configurés: {len([k for k, v in planning_data['planning'].items() if v['plannings']])}")
            
            # Afficher les détails du planning
            for jour, data in planning_data['planning'].items():
                if data['plannings']:
                    planning = data['plannings'][0]
                    print(f"   - {data['jour_nom']}: {planning['heure_debut']} - {planning['heure_fin']}")
                    if planning.get('pause_debut') and planning.get('pause_fin'):
                        print(f"     Pause: {planning['pause_debut']} - {planning['pause_fin']}")
        else:
            print(f"⚠️ Planning non trouvé (normal si pas encore configuré)")
        
        # Test 3: Créer un planning pour l'agent via le responsable
        print(f"\n👨‍💼 Test de création de planning via le responsable...")
        
        # Connexion Responsable
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'jean.martin@exemple.com', 'password': 'resp123'},
                               timeout=5)
        
        if response.status_code == 200:
            resp_data = response.json()
            print(f"✅ Connexion Responsable réussie")
            resp_cookies = response.cookies
            
            # Créer un planning pour l'agent
            planning_data = {
                "plannings": [
                    {
                        "jour_semaine": 0,  # Lundi
                        "heure_debut": "08:00",
                        "heure_fin": "17:00",
                        "pause_debut": "12:00",
                        "pause_fin": "13:00"
                    },
                    {
                        "jour_semaine": 1,  # Mardi
                        "heure_debut": "08:30",
                        "heure_fin": "17:30",
                        "pause_debut": "12:30",
                        "pause_fin": "13:30"
                    },
                    {
                        "jour_semaine": 2,  # Mercredi
                        "heure_debut": "09:00",
                        "heure_fin": "18:00",
                        "pause_debut": "13:00",
                        "pause_fin": "14:00"
                    }
                ]
            }
            
            response = requests.post(f'http://localhost:5001/api/planning/agent/{agent_id}', 
                                   json=planning_data, cookies=resp_cookies, timeout=5)
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Planning créé par le responsable")
                print(f"   Plannings créés: {len(result['plannings'])}")
            else:
                error = response.json()
                print(f"❌ Erreur création planning: {error.get('error', 'Erreur inconnue')}")
                return
        
        # Test 4: Vérifier que l'agent peut voir son planning mis à jour
        print(f"\n👤 Test de visualisation du planning mis à jour par l'agent...")
        
        # Reconnexion Agent
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'marie.dupont@exemple.com', 'password': 'agent123'},
                               timeout=5)
        
        if response.status_code == 200:
            agent_cookies = response.cookies
            
            response = requests.get(f'http://localhost:5001/api/planning/agent/{agent_id}', 
                                  cookies=agent_cookies, timeout=5)
            
            if response.status_code == 200:
                planning_data = response.json()
                jours_configures = [k for k, v in planning_data['planning'].items() if v['plannings']]
                print(f"✅ Planning visible par l'agent")
                print(f"   Jours configurés: {len(jours_configures)}")
                
                for jour in sorted(jours_configures, key=int):
                    planning = planning_data['planning'][jour]['plannings'][0]
                    jour_nom = planning_data['planning'][jour]['jour_nom']
                    print(f"   - {jour_nom}: {planning['heure_debut']} - {planning['heure_fin']}")
                    if planning.get('pause_debut') and planning.get('pause_fin'):
                        print(f"     Pause: {planning['pause_debut']} - {planning['pause_fin']}")
                    print(f"     Durée: {planning.get('duree_travail', 'N/A')}h")
        
        print("\n✅ Tests de visualisation terminés")
        print("\n🔧 Fonctionnalités ajoutées:")
        print("   - Onglet 'Mon planning' dans AgentDashboard")
        print("   - Visualisation du planning par l'agent")
        print("   - Interface utilisateur avec onglets")
        print("   - Séparation dashboard/historique/planning")
        
        print("\n📝 Structure des onglets:")
        print("   1. Tableau de bord - Informations personnelles et soldes")
        print("   2. Mon planning - Planning hebdomadaire de travail")
        print("   3. Historique - Historique des demandes et mouvements")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_planning_agent()
