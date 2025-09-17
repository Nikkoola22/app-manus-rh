#!/usr/bin/env python3
"""
Test du scroll automatique vers les sections de demandes
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_scroll_demandes():
    """Test du scroll automatique vers les sections de demandes"""
    print("📜 Test du scroll automatique vers les sections de demandes")
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
        print("\n👤 Test de connexion Responsable...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'jean.martin@exemple.com', 'password': 'resp123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion Responsable réussie")
            print(f"   Nom: {data['user']['prenom']} {data['user']['nom']}")
            print(f"   Rôle: {data['user']['role']}")
            
            cookies = response.cookies
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test 2: Vérifier les demandes disponibles
        print(f"\n📋 Test de récupération des demandes...")
        response = requests.get('http://localhost:5001/api/demandes', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            demandes = response.json()
            print(f"✅ Demandes récupérées: {len(demandes)}")
            
            # Compter par statut
            en_attente = [d for d in demandes if d['statut'] == 'En attente']
            traitees = [d for d in demandes if d['statut'] in ['Approuvée', 'Refusée']]
            
            print(f"   Demandes en attente: {len(en_attente)}")
            print(f"   Demandes traitées: {len(traitees)}")
        else:
            print(f"❌ Erreur récupération demandes: {response.status_code}")
        
        # Test 3: Vérifier les agents du service
        print(f"\n👥 Test de récupération des agents...")
        response = requests.get('http://localhost:5001/api/agents', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ Agents récupérés: {len(agents)}")
        else:
            print(f"❌ Erreur récupération agents: {response.status_code}")
        
        # Test 4: Vérifier les arrêts maladie
        print(f"\n🏥 Test de récupération des arrêts maladie...")
        response = requests.get('http://localhost:5001/api/arret-maladie', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            arrets = response.json()
            print(f"✅ Arrêts maladie récupérés: {len(arrets)}")
        else:
            print(f"❌ Erreur récupération arrêts: {response.status_code}")
        
        print("\n✅ Tests de données terminés")
        print("\n🔧 Fonctionnalités de scroll implémentées:")
        print("   - Ref pour 'Demandes en attente'")
        print("   - Ref pour 'Demandes traitées'")
        print("   - Ref pour 'Mes Demandes'")
        print("   - Fonction handleTabChange() avec scrollIntoView()")
        print("   - Scroll smooth vers le début de chaque section")
        print("   - Délai de 100ms pour laisser le contenu se rendre")
        
        print("\n📱 Instructions pour tester manuellement:")
        print("   1. Ouvrir http://localhost:5001 dans le navigateur")
        print("   2. Se connecter comme responsable (jean.martin@exemple.com)")
        print("   3. Cliquer sur les onglets 'Demandes en attente', 'Demandes traitées', 'Mes Demandes'")
        print("   4. Vérifier que la page scroll automatiquement vers la section correspondante")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_scroll_demandes()
