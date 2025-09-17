#!/usr/bin/env python3
"""
Test simple du calcul des heures basé sur le planning
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_calcul_simple():
    """Test simple du calcul des heures basé sur le planning"""
    print("📅 Test simple du calcul basé sur le planning")
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
        # Test 1: Connexion Sofiane
        print("\n👤 Test de connexion Sofiane...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'sofiane.bendaoud@exemple.com', 'password': 'agent123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion Sofiane réussie")
            print(f"   Nom: {data['user']['prenom']} {data['user']['nom']}")
            print(f"   Quotité: {data['user']['quotite_travail']}h")
            
            # Récupérer les cookies de session
            cookies = response.cookies
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test 2: Vérifier le planning actuel
        print(f"\n📅 Test du planning actuel...")
        response = requests.get(f'http://localhost:5001/api/planning/agent/{data["user"]["id"]}', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            planning_data = response.json()
            print(f"✅ Planning récupéré")
            
            # Vérifier le mercredi (jour 2)
            mercredi_planning = planning_data['planning'].get('2', {})
            if mercredi_planning.get('plannings'):
                planning = mercredi_planning['plannings'][0]
                print(f"   Mercredi: {planning['heure_debut']} - {planning['heure_fin']}")
                print(f"   Durée: {planning.get('duree_travail', 'N/A')}h")
            else:
                print(f"   Mercredi: Pas de planning configuré")
        else:
            print(f"⚠️ Planning non trouvé")
        
        # Test 3: Tester le calcul avec une demande RTT
        print(f"\n🧮 Test du calcul des heures avec demande RTT...")
        
        # Créer une demande RTT pour le mercredi
        demande_rtt = {
            'type_absence': 'RTT',
            'date_debut': '2024-12-18',  # Mercredi
            'date_fin': '2024-12-18',    # Mercredi
            'motif': 'Test calcul avec planning'
        }
        
        response = requests.post('http://localhost:5001/api/demandes', 
                               json=demande_rtt, cookies=cookies, timeout=5)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Demande RTT créée avec succès")
            print(f"   Date: Mercredi 18/12/2024")
            print(f"   Heures calculées: {result['nb_heures']}h")
            
            # Analyser le résultat
            if result['nb_heures'] == 3.5:
                print(f"✅ Calcul correct ! Le planning est utilisé (3.5h = 08:00-11:30)")
            elif result['nb_heures'] == 7.6:
                print(f"⚠️ Calcul avec quotité (7.6h) - Le planning n'est pas utilisé")
            else:
                print(f"❓ Calcul inattendu: {result['nb_heures']}h")
        else:
            error = response.json()
            print(f"❌ Erreur création demande: {error.get('error', 'Erreur inconnue')}")
            print(f"   Détails: {error}")
        
        print("\n✅ Tests de calcul terminés")
        print("\n🔧 Fonctionnalités testées:")
        print("   - Calcul des heures basé sur le planning")
        print("   - Utilisation du planning pour RTT/HS")
        print("   - Prise en compte des heures réelles de travail")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_calcul_simple()
