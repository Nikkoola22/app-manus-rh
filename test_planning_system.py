#!/usr/bin/env python3
"""
Test du système de planning complet
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_planning_system():
    """Test du système de planning"""
    print("🗓️ Test du système de planning")
    print("=" * 50)
    
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
        # Test 1: Connexion Responsable
        print("\n👤 Connexion Responsable...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'jean.martin@exemple.com', 'password': 'resp123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            user = data['user']
            print(f"✅ Connexion réussie")
            print(f"   Nom: {user['prenom']} {user['nom']}")
            print(f"   Rôle: {user['role']}")
            print(f"   Service: {user.get('service_id', 'N/A')}")
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test 2: Récupérer les agents du service
        print(f"\n👥 Récupération des agents du service...")
        response = requests.get('http://localhost:5001/api/agents', 
                              headers={'Authorization': f"Bearer {data.get('token', '')}"},
                              timeout=5)
        
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ {len(agents)} agents trouvés")
            
            # Prendre le premier agent pour les tests
            if agents:
                test_agent = agents[0]
                print(f"   Agent de test: {test_agent['prenom']} {test_agent['nom']} (ID: {test_agent['id']})")
                
                # Test 3: Récupérer le planning de l'agent
                print(f"\n📅 Récupération du planning de l'agent...")
                response = requests.get(f'http://localhost:5001/api/planning/agent/{test_agent["id"]}', 
                                      headers={'Authorization': f"Bearer {data.get('token', '')}"},
                                      timeout=5)
                
                if response.status_code == 200:
                    planning_data = response.json()
                    print(f"✅ Planning récupéré")
                    print(f"   Agent ID: {planning_data['agent_id']}")
                    print(f"   Jours configurés: {len(planning_data['planning'])}")
                    
                    # Afficher les détails du planning
                    for jour, data in planning_data['planning'].items():
                        if data['plannings']:
                            planning = data['plannings'][0]
                            print(f"   {data['jour_nom']}: {planning['heure_debut']} - {planning['heure_fin']} ({planning['duree_travail']}h)")
                        else:
                            print(f"   {data['jour_nom']}: Aucun planning")
                else:
                    print(f"❌ Erreur planning: {response.status_code}")
                    print(f"   Réponse: {response.text}")
                
                # Test 4: Créer un planning de test
                print(f"\n📝 Création d'un planning de test...")
                planning_test = {
                    'plannings': [
                        {
                            'jour_semaine': 0,  # Lundi
                            'heure_debut': '08:00',
                            'heure_fin': '17:00',
                            'pause_debut': '12:00',
                            'pause_fin': '13:00'
                        },
                        {
                            'jour_semaine': 1,  # Mardi
                            'heure_debut': '08:00',
                            'heure_fin': '17:00',
                            'pause_debut': '12:00',
                            'pause_fin': '13:00'
                        }
                    ]
                }
                
                response = requests.post(f'http://localhost:5001/api/planning/agent/{test_agent["id"]}', 
                                       json=planning_test,
                                       headers={'Authorization': f"Bearer {data.get('token', '')}"},
                                       timeout=5)
                
                if response.status_code == 201:
                    print(f"✅ Planning créé avec succès")
                    planning_created = response.json()
                    print(f"   Plannings créés: {len(planning_created['plannings'])}")
                    
                    for planning in planning_created['plannings']:
                        print(f"   {planning['jour_nom']}: {planning['heure_debut']} - {planning['heure_fin']} ({planning['duree_travail']}h)")
                else:
                    print(f"❌ Erreur création planning: {response.status_code}")
                    print(f"   Réponse: {response.text}")
            else:
                print("❌ Aucun agent trouvé pour les tests")
        else:
            print(f"❌ Erreur agents: {response.status_code}")
        
        print("\n✅ Tests du système de planning terminés")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_planning_system()


