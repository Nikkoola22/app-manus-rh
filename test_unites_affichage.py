#!/usr/bin/env python3
"""
Test de l'affichage des unités dans l'application
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_unites_affichage():
    """Test de l'affichage des unités"""
    print("📊 Test de l'affichage des unités")
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
        # Test 1: Connexion Admin
        print("\n👤 Connexion Admin...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'admin@exemple.com', 'password': 'admin123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            user = data['user']
            print(f"✅ Connexion réussie")
            print(f"   Nom: {user['prenom']} {user['nom']}")
            print(f"   Rôle: {user['role']}")
            
            # Vérifier les soldes avec les bonnes unités
            print(f"\n📊 Soldes de l'utilisateur:")
            print(f"   CA: {user['solde_ca']} jours")
            print(f"   RTT: {user['solde_rtt']} heures")
            print(f"   CET: {user['solde_cet']} heures")
            print(f"   HS: {user['solde_hs']} heures")
            
            # Test 2: Récupérer les agents
            print(f"\n👥 Récupération des agents...")
            response = requests.get('http://localhost:5001/api/agents', 
                                  headers={'Authorization': f"Bearer {data.get('token', '')}"},
                                  timeout=5)
            
            if response.status_code == 200:
                agents = response.json()
                print(f"✅ {len(agents)} agents trouvés")
                
                for agent in agents:
                    print(f"\n   {agent['prenom']} {agent['nom']} ({agent['role']}):")
                    print(f"     CA: {agent['solde_ca']} jours")
                    print(f"     RTT: {agent['solde_rtt']} heures")
                    print(f"     HS: {agent['solde_hs']} heures")
            else:
                print(f"❌ Erreur agents: {response.status_code}")
        
        # Test 3: Vérifier les demandes
        print(f"\n📋 Récupération des demandes...")
        response = requests.get('http://localhost:5001/api/demandes', 
                              headers={'Authorization': f"Bearer {data.get('token', '')}"},
                              timeout=5)
        
        if response.status_code == 200:
            demandes = response.json()
            print(f"✅ {len(demandes)} demandes trouvées")
            
            for demande in demandes[:3]:  # Afficher les 3 premières
                print(f"\n   Demande {demande['id']}:")
                print(f"     Type: {demande['type_absence']}")
                print(f"     Durée: {demande.get('nb_jours', demande.get('nb_heures', 0))}")
                print(f"     Période: {demande['date_debut']} - {demande['date_fin']}")
        else:
            print(f"❌ Erreur demandes: {response.status_code}")
        
        print("\n✅ Tests d'affichage terminés")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_unites_affichage()

