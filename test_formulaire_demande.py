#!/usr/bin/env python3
"""
Test du formulaire de demande avec les unités correctes
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_formulaire_demande():
    """Test du formulaire de demande"""
    print("📝 Test du formulaire de demande")
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
        # Test 1: Connexion Agent
        print("\n👤 Connexion Agent...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'sofiane.bendaoud@exemple.com', 'password': 'agent123'},
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
            
            # Test 2: Vérifier les types d'absence disponibles
            print(f"\n📋 Types d'absence disponibles:")
            types_absence = [
                {'value': 'CA', 'label': 'Congés Annuels', 'solde': user['solde_ca']},
                {'value': 'RTT', 'label': 'RTT', 'solde': user['solde_rtt']},
                {'value': 'CET', 'label': 'Compte Épargne Temps', 'solde': user['solde_cet']},
                {'value': 'HS', 'label': 'Heures Supplémentaires', 'solde': user['solde_hs']}
            ]
            
            for type_abs in types_absence:
                if type_abs['value'] == 'CA':
                    print(f"   {type_abs['label']}: {type_abs['solde']} jours")
                else:
                    print(f"   {type_abs['label']}: {type_abs['solde']} heures")
            
            # Test 3: Créer une demande de test
            print(f"\n📝 Création d'une demande de test...")
            demande_data = {
                'type_absence': 'CA',
                'date_debut': '2024-12-20',
                'date_fin': '2024-12-20',
                'demi_journees': '',
                'motif': 'Test unités affichage'
            }
            
            response = requests.post('http://localhost:5001/api/demandes', 
                                  json=demande_data,
                                  headers={'Content-Type': 'application/json'},
                                  timeout=5)
            
            if response.status_code == 201:
                print(f"✅ Demande créée avec succès")
                demande = response.json()
                print(f"   Type: {demande['type_absence']}")
                print(f"   Durée: {demande.get('nb_jours', demande.get('nb_heures', 0))}")
                print(f"   Période: {demande['date_debut']} - {demande['date_fin']}")
            else:
                print(f"❌ Erreur création demande: {response.status_code}")
                print(f"   Réponse: {response.text}")
        
        print("\n✅ Tests du formulaire terminés")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_formulaire_demande()
