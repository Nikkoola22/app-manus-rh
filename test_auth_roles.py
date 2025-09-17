#!/usr/bin/env python3
"""
Test de l'authentification et des rôles
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_auth_roles():
    """Test de l'authentification et des rôles"""
    print("🔐 Test de l'authentification et des rôles")
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
        print("\n👤 Test 1: Connexion Admin")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'admin@exemple.com', 'password': 'admin123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion Admin réussie")
            print(f"   Rôle: {data['user']['role']}")
            print(f"   Nom: {data['user']['prenom']} {data['user']['nom']}")
        else:
            print(f"❌ Erreur connexion Admin: {response.status_code}")
            print(f"   Réponse: {response.text}")
        
        # Test 2: Connexion Responsable
        print("\n👤 Test 2: Connexion Responsable")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'jean.martin@exemple.com', 'password': 'resp123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion Responsable réussie")
            print(f"   Rôle: {data['user']['role']}")
            print(f"   Nom: {data['user']['prenom']} {data['user']['nom']}")
        else:
            print(f"❌ Erreur connexion Responsable: {response.status_code}")
            print(f"   Réponse: {response.text}")
        
        # Test 3: Connexion Agent
        print("\n👤 Test 3: Connexion Agent")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'sofiane.bendaoud@exemple.com', 'password': 'agent123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion Agent réussie")
            print(f"   Rôle: {data['user']['role']}")
            print(f"   Nom: {data['user']['prenom']} {data['user']['nom']}")
        else:
            print(f"❌ Erreur connexion Agent: {response.status_code}")
            print(f"   Réponse: {response.text}")
        
        # Test 4: Vérification des agents
        print("\n👥 Test 4: Liste des agents")
        response = requests.get('http://localhost:5001/api/agents', timeout=5)
        
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ {len(agents)} agents trouvés")
            for agent in agents:
                print(f"   {agent['prenom']} {agent['nom']}: {agent['role']}")
        else:
            print(f"❌ Erreur liste agents: {response.status_code}")
        
        print("\n✅ Tests d'authentification terminés")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_auth_roles()
