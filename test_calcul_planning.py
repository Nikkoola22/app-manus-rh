#!/usr/bin/env python3
"""
Test du calcul des heures basé sur le planning
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_calcul_planning():
    """Test du calcul des heures basé sur le planning"""
    print("📅 Test du calcul des heures basé sur le planning")
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
        # Test 1: Connexion Responsable
        print("\n👨‍💼 Test de connexion Responsable...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'jean.martin@exemple.com', 'password': 'resp123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion Responsable réussie")
            resp_cookies = response.cookies
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test 2: Créer un planning spécifique pour Sofiane (Mercredi 8h00-11h30)
        print(f"\n📅 Test de création d'un planning spécifique...")
        
        # Connexion Sofiane pour obtenir son ID
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'sofiane.bendaoud@exemple.com', 'password': 'agent123'},
                               timeout=5)
        
        if response.status_code == 200:
            sofiane_data = response.json()
            sofiane_id = sofiane_data['user']['id']
            print(f"✅ Sofiane ID: {sofiane_id}")
        else:
            print(f"❌ Erreur connexion Sofiane: {response.status_code}")
            return
        
        # Créer le planning directement en base de données
        print(f"   Création du planning en base...")
        
        # Importer les modèles
        import sys
        sys.path.append(str(app_dir))
        from src.models.planning import PlanningAgent
        from src.models.agent import Agent
        from src.database import db
        from datetime import time as dt_time
        
        # Créer le planning pour Sofiane (Mercredi = jour 2)
        planning = PlanningAgent(
            agent_id=sofiane_id,
            jour_semaine=2,  # Mercredi
            heure_debut=dt_time(8, 0),   # 08:00
            heure_fin=dt_time(11, 30),   # 11:30
            pause_debut=None,
            pause_fin=None,
            actif=True
        )
        
        # Ajouter en base
        db.session.add(planning)
        db.session.commit()
        
        print(f"✅ Planning créé pour Sofiane")
        print(f"   Mercredi: 08:00 - 11:30 (3.5h)")
        
        # Test 3: Tester le calcul avec le planning
        print(f"\n🧮 Test du calcul des heures avec planning...")
        
        # Reconnexion Sofiane
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'sofiane.bendaoud@exemple.com', 'password': 'agent123'},
                               timeout=5)
        
        if response.status_code == 200:
            sofiane_cookies = response.cookies
            
            # Créer une demande RTT pour le mercredi
            demande_rtt = {
                'type_absence': 'RTT',
                'date_debut': '2024-12-18',  # Mercredi
                'date_fin': '2024-12-18',    # Mercredi
                'motif': 'Test calcul avec planning'
            }
            
            response = requests.post('http://localhost:5001/api/demandes', 
                                   json=demande_rtt, cookies=sofiane_cookies, timeout=5)
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Demande RTT créée avec succès")
                print(f"   Date: Mercredi 18/12/2024")
                print(f"   Heures calculées: {result['nb_heures']}h")
                print(f"   Attendu: 3.5h (08:00-11:30)")
                
                if result['nb_heures'] == 3.5:
                    print(f"✅ Calcul correct ! Le planning est utilisé.")
                else:
                    print(f"❌ Calcul incorrect. Attendu: 3.5h, Obtenu: {result['nb_heures']}h")
            else:
                error = response.json()
                print(f"❌ Erreur création demande: {error.get('error', 'Erreur inconnue')}")
                print(f"   Détails: {error}")
        else:
            print(f"❌ Erreur reconnexion Sofiane: {response.status_code}")
        
        print("\n✅ Tests de calcul terminés")
        print("\n🔧 Corrections appliquées:")
        print("   - Fonction calculate_hours_from_planning() créée")
        print("   - Utilisation du planning pour RTT et HS")
        print("   - Calcul basé sur les heures réelles de travail")
        print("   - Prise en compte des pauses")
        
        print("\n📝 Logique appliquée:")
        print("   - RTT/HS: Calcul basé sur le planning")
        print("   - CA: Calcul basé sur la quotité")
        print("   - Mercredi 08:00-11:30 = 3.5h")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_calcul_planning()
