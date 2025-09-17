#!/usr/bin/env python3
"""
Test de la fonctionnalité d'annulation des demandes
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_annulation_demande():
    """Test de l'annulation des demandes par les agents"""
    print("🚫 Test de l'annulation des demandes")
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
            
            cookies = response.cookies
            sofiane_id = data['user']['id']
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test 2: Créer une demande RTT
        print(f"\n📝 Test de création d'une demande RTT...")
        nouvelle_demande = {
            'type_absence': 'RTT',
            'date_debut': '2024-12-25',  # Noël
            'date_fin': '2024-12-25',
            'motif': 'Test annulation'
        }
        
        response = requests.post('http://localhost:5001/api/demandes', 
                               json=nouvelle_demande, cookies=cookies, timeout=5)
        
        if response.status_code == 201:
            result = response.json()
            demande_id = result['id']
            print(f"✅ Demande RTT créée (ID: {demande_id})")
            print(f"   Statut: {result['statut']}")
            print(f"   Heures: {result['nb_heures']}h")
        else:
            error = response.json()
            print(f"❌ Erreur création demande: {error.get('error', 'Erreur inconnue')}")
            return
        
        # Test 3: Vérifier les demandes avant annulation
        print(f"\n📋 Test de récupération des demandes...")
        response = requests.get('http://localhost:5001/api/demandes', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            demandes = response.json()
            print(f"✅ Demandes récupérées: {len(demandes)}")
            
            # Trouver notre demande
            notre_demande = next((d for d in demandes if d['id'] == demande_id), None)
            if notre_demande:
                print(f"   Demande trouvée: {notre_demande['statut']}")
            else:
                print(f"   Demande non trouvée")
        else:
            print(f"❌ Erreur récupération demandes: {response.status_code}")
        
        # Test 4: Annuler la demande
        print(f"\n🚫 Test d'annulation de la demande...")
        response = requests.post(f'http://localhost:5001/api/demandes/{demande_id}/annuler', 
                               cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Demande annulée avec succès")
            print(f"   Message: {result['message']}")
            print(f"   Nouveau statut: {result['demande']['statut']}")
            print(f"   Date annulation: {result['demande']['date_annulation']}")
        else:
            error = response.json()
            print(f"❌ Erreur annulation: {error.get('error', 'Erreur inconnue')}")
        
        # Test 5: Vérifier les demandes après annulation
        print(f"\n📋 Test de vérification après annulation...")
        response = requests.get('http://localhost:5001/api/demandes', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            demandes = response.json()
            print(f"✅ Demandes récupérées: {len(demandes)}")
            
            # Trouver notre demande annulée
            notre_demande = next((d for d in demandes if d['id'] == demande_id), None)
            if notre_demande:
                print(f"   Demande trouvée: {notre_demande['statut']}")
                print(f"   Date annulation: {notre_demande['date_annulation']}")
            else:
                print(f"   Demande non trouvée")
        else:
            print(f"❌ Erreur récupération demandes: {response.status_code}")
        
        # Test 6: Tenter d'annuler une demande déjà annulée
        print(f"\n🚫 Test d'annulation d'une demande déjà annulée...")
        response = requests.post(f'http://localhost:5001/api/demandes/{demande_id}/annuler', 
                               cookies=cookies, timeout=5)
        
        if response.status_code == 400:
            error = response.json()
            print(f"✅ Erreur attendue: {error.get('error', 'Erreur inconnue')}")
        else:
            print(f"⚠️ Comportement inattendu: {response.status_code}")
        
        # Test 7: Tenter d'annuler une demande d'un autre agent
        print(f"\n👥 Test d'annulation d'une demande d'un autre agent...")
        
        # Se connecter comme Marie
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'marie.dupont@exemple.com', 'password': 'agent123'},
                               timeout=5)
        
        if response.status_code == 200:
            marie_cookies = response.cookies
            print(f"✅ Connexion Marie réussie")
            
            # Tenter d'annuler la demande de Sofiane
            response = requests.post(f'http://localhost:5001/api/demandes/{demande_id}/annuler', 
                                   cookies=marie_cookies, timeout=5)
            
            if response.status_code == 403:
                error = response.json()
                print(f"✅ Erreur attendue: {error.get('error', 'Erreur inconnue')}")
            else:
                print(f"⚠️ Comportement inattendu: {response.status_code}")
        else:
            print(f"❌ Erreur connexion Marie: {response.status_code}")
        
        print("\n✅ Tests d'annulation terminés")
        print("\n🔧 Fonctionnalités testées:")
        print("   - Annulation d'une demande en attente")
        print("   - Vérification du changement de statut")
        print("   - Enregistrement de la date d'annulation")
        print("   - Protection contre l'annulation multiple")
        print("   - Protection contre l'annulation d'autrui")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_annulation_demande()
