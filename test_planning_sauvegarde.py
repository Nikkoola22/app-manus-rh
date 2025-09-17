#!/usr/bin/env python3
"""
Test de la sauvegarde du planning
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_planning_sauvegarde():
    """Test de la sauvegarde du planning"""
    print("📅 Test de la sauvegarde du planning")
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
        print("\n👤 Test de connexion Responsable...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'jean.martin@exemple.com', 'password': 'resp123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion Responsable réussie")
            print(f"   Nom: {data['user']['prenom']} {data['user']['nom']}")
            print(f"   Rôle: {data['user']['role']}")
            
            # Récupérer les cookies de session
            cookies = response.cookies
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test 2: Récupérer les agents
        print("\n👥 Test de récupération des agents...")
        response = requests.get('http://localhost:5001/api/agents', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ {len(agents)} agents récupérés")
            if agents:
                agent_id = agents[0]['id']
                print(f"   Agent test: {agents[0]['prenom']} {agents[0]['nom']} (ID: {agent_id})")
            else:
                print("❌ Aucun agent trouvé")
                return
        else:
            print(f"❌ Erreur récupération agents: {response.status_code}")
            return
        
        # Test 3: Récupérer le planning actuel
        print(f"\n📅 Test de récupération du planning de l'agent {agent_id}...")
        response = requests.get(f'http://localhost:5001/api/planning/agent/{agent_id}', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            planning_data = response.json()
            print(f"✅ Planning récupéré")
            print(f"   Jours configurés: {len([k for k, v in planning_data['planning'].items() if v['plannings']])}")
        else:
            print(f"⚠️ Planning non trouvé (normal si premier planning)")
        
        # Test 4: Créer un planning de test
        print(f"\n💾 Test de création d'un planning...")
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
                }
            ]
        }
        
        response = requests.post(f'http://localhost:5001/api/planning/agent/{agent_id}', 
                               json=planning_data, cookies=cookies, timeout=5)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Planning créé avec succès")
            print(f"   Plannings créés: {len(result['plannings'])}")
            for p in result['plannings']:
                print(f"   - {p['jour_semaine']}: {p['heure_debut']} - {p['heure_fin']}")
        else:
            error = response.json()
            print(f"❌ Erreur création planning: {error.get('error', 'Erreur inconnue')}")
            return
        
        # Test 5: Vérifier que le planning a été sauvegardé
        print(f"\n🔍 Test de vérification du planning sauvegardé...")
        response = requests.get(f'http://localhost:5001/api/planning/agent/{agent_id}', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            planning_data = response.json()
            jours_configures = [k for k, v in planning_data['planning'].items() if v['plannings']]
            print(f"✅ Planning vérifié")
            print(f"   Jours configurés: {len(jours_configures)}")
            for jour in jours_configures:
                planning = planning_data['planning'][jour]['plannings'][0]
                print(f"   - {planning_data['planning'][jour]['jour_nom']}: {planning['heure_debut']} - {planning['heure_fin']}")
        else:
            print(f"❌ Erreur vérification planning: {response.status_code}")
        
        print("\n✅ Tests de sauvegarde terminés")
        print("\n🔧 Corrections appliquées:")
        print("   - Ajout de logs de débogage")
        print("   - Gestion des valeurs null pour les pauses")
        print("   - Message de confirmation de sauvegarde")
        print("   - Rechargement automatique de la page")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_planning_sauvegarde()
