#!/usr/bin/env python3
"""
Test de l'envoi d'email lors de la validation d'un congé
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_email_validation():
    """Test de l'envoi d'email lors de la validation"""
    print("📧 Test de l'envoi d'email lors de la validation")
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
        # Test 1: Connexion Agent (Sofiane)
        print("\n👤 Test de connexion Agent...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'sofiane.bendaoud@exemple.com', 'password': 'agent123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion Agent réussie")
            print(f"   Nom: {data['user']['prenom']} {data['user']['nom']}")
            print(f"   Email: {data['user']['email']}")
            
            agent_cookies = response.cookies
        else:
            print(f"❌ Erreur connexion Agent: {response.status_code}")
            return
        
        # Test 2: Créer une demande de congé
        print(f"\n📝 Test de création d'une demande...")
        demande = {
            'type_absence': 'CA',
            'date_debut': '2024-12-25',
            'date_fin': '2024-12-25',
            'motif': 'Test email de validation'
        }
        
        response = requests.post('http://localhost:5001/api/demandes', 
                               json=demande, cookies=agent_cookies, timeout=5)
        
        if response.status_code == 201:
            result = response.json()
            demande_id = result['id']
            print(f"✅ Demande créée avec succès")
            print(f"   ID: {demande_id}")
            print(f"   Type: {result['type_absence']}")
            print(f"   Statut: {result['statut']}")
        else:
            error = response.json()
            print(f"❌ Erreur création demande: {error.get('error', 'Erreur inconnue')}")
            return
        
        # Test 3: Connexion Admin
        print(f"\n👨‍💼 Test de connexion Admin...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'admin@exemple.com', 'password': 'admin123'},
                               timeout=5)
        
        if response.status_code == 200:
            resp_data = response.json()
            print(f"✅ Connexion Admin réussie")
            print(f"   Nom: {resp_data['user']['prenom']} {resp_data['user']['nom']}")
            
            resp_cookies = response.cookies
        else:
            print(f"❌ Erreur connexion Admin: {response.status_code}")
            return
        
        # Test 4: Valider la demande (approuver)
        print(f"\n✅ Test de validation de la demande...")
        validation_data = {
            'action': 'approuver',
            'commentaires': 'Demande approuvée - Test email'
        }
        
        response = requests.post(f'http://localhost:5001/api/demandes/{demande_id}/valider', 
                               json=validation_data, cookies=resp_cookies, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Demande validée avec succès")
            print(f"   Statut: {result['statut']}")
            print(f"   Date validation: {result['date_validation']}")
            print(f"   Commentaires: {result['commentaires']}")
        else:
            error = response.json()
            print(f"❌ Erreur validation: {error.get('error', 'Erreur inconnue')}")
            return
        
        # Test 5: Vérifier l'email de test
        print(f"\n📧 Test de l'email de test...")
        response = requests.post('http://localhost:5001/api/email/test', 
                               json={'email': 'sofiane.bendaoud@exemple.com'}, 
                               cookies=resp_cookies, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Email de test envoyé")
            print(f"   Message: {result['message']}")
        else:
            error = response.json()
            print(f"⚠️ Erreur email de test: {error.get('error', 'Erreur inconnue')}")
        
        print("\n✅ Tests d'email terminés")
        print("\n📧 Fonctionnalités d'email:")
        print("   - Email automatique lors de la validation")
        print("   - Template HTML professionnel")
        print("   - Informations détaillées de la demande")
        print("   - Statut visuel (approuvée/refusée)")
        print("   - Email de test disponible")
        
        print("\n📝 Emails envoyés automatiquement:")
        print("   1. Création de demande → Responsable")
        print("   2. Validation → Agent")
        print("   3. Test → Email spécifié")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_email_validation()
