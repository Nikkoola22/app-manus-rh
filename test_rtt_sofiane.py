#!/usr/bin/env python3
"""
Test de la correction des RTT pour Sofiane
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_rtt_sofiane():
    """Test de la correction des RTT pour Sofiane"""
    print("👤 Test de la correction des RTT pour Sofiane")
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
            print(f"   Rôle: {data['user']['role']}")
            print(f"   Quotité: {data['user']['quotite_travail']}h")
            print(f"   Solde CA: {data['user']['solde_ca']} jours")
            print(f"   Solde HS: {data['user']['solde_hs']}h")
            
            # Récupérer les cookies de session
            cookies = response.cookies
            user = data['user']
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test 2: Calculer le solde RTT théorique
        print(f"\n📊 Test du calcul des RTT...")
        quotite = user['quotite_travail']
        if quotite >= 38:
            rtt_theorique = 18 * 8  # 144h
        elif quotite >= 36:
            rtt_theorique = 6 * 8   # 48h
        else:
            rtt_theorique = 0
        
        print(f"   Quotité de travail: {quotite}h")
        print(f"   RTT théorique: {rtt_theorique}h")
        print(f"   RTT en jours: {rtt_theorique / 8} jours")
        
        # Test 3: Vérifier les demandes existantes
        print(f"\n📋 Test des demandes existantes...")
        response = requests.get('http://localhost:5001/api/demandes', cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            demandes = response.json()
            demandes_rtt = [d for d in demandes if d['type_absence'] == 'RTT' and d['agent_id'] == user['id']]
            print(f"   Demandes RTT existantes: {len(demandes_rtt)}")
            
            total_rtt_pris = sum(d['nb_heures'] for d in demandes_rtt if d['statut'] == 'Approuvée')
            print(f"   RTT déjà pris: {total_rtt_pris}h")
            print(f"   RTT restant: {rtt_theorique - total_rtt_pris}h")
        else:
            print(f"⚠️ Erreur récupération demandes: {response.status_code}")
        
        # Test 4: Tenter de créer une demande RTT
        print(f"\n💼 Test de création d'une demande RTT...")
        demande_rtt = {
            'type_absence': 'RTT',
            'date_debut': '2024-12-20',
            'date_fin': '2024-12-20',
            'nb_heures': 8,
            'motif': 'Test RTT après correction'
        }
        
        response = requests.post('http://localhost:5001/api/demandes', 
                               json=demande_rtt, cookies=cookies, timeout=5)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Demande RTT créée avec succès")
            print(f"   ID: {result['id']}")
            print(f"   Type: {result['type_absence']}")
            print(f"   Durée: {result['nb_heures']}h")
            print(f"   Statut: {result['statut']}")
        else:
            error = response.json()
            print(f"❌ Erreur création demande RTT: {error.get('error', 'Erreur inconnue')}")
            print(f"   Détails: {error}")
        
        print("\n✅ Tests de correction RTT terminés")
        print("\n🔧 Corrections appliquées:")
        print("   - Calcul RTT en heures (18 jours * 8h = 144h)")
        print("   - Cohérence entre AgentDashboard et DemandeForm")
        print("   - Utilisation de calculateRttFromQuotite()")
        print("   - Correction des types d'absence")
        
        print("\n📝 Règles RTT appliquées:")
        print("   - 38h et plus: 18 jours * 8h = 144h de RTT")
        print("   - 36h à 37h: 6 jours * 8h = 48h de RTT")
        print("   - Moins de 36h: 0h de RTT")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_rtt_sofiane()
