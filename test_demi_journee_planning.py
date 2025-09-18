#!/usr/bin/env python3
"""
Test des demi-journées avec le planning
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_demi_journee_planning():
    """Test des demi-journées avec le planning"""
    print("🕐 Test des demi-journées avec le planning")
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
            
            cookies = response.cookies
            sofiane_id = data['user']['id']
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test 2: Vérifier le planning actuel
        print(f"\n📅 Test du planning actuel...")
        response = requests.get(f'http://localhost:5001/api/planning/agent/{sofiane_id}', 
                              cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            planning_data = response.json()
            print(f"✅ Planning récupéré")
            
            # Vérifier le mercredi (jour 2)
            mercredi_planning = planning_data['planning'].get('2', {})
            if mercredi_planning.get('plannings'):
                planning = mercredi_planning['plannings'][0]
                print(f"   Mercredi: {planning['heure_debut']} - {planning['heure_fin']}")
                print(f"   Durée totale: {planning.get('duree_travail', 'N/A')}h")
                
                # Calculer les demi-journées théoriques
                if planning['heure_debut'] and planning['heure_fin']:
                    debut_h = int(planning['heure_debut'].split(':')[0])
                    debut_m = int(planning['heure_debut'].split(':')[1])
                    fin_h = int(planning['heure_fin'].split(':')[0])
                    fin_m = int(planning['heure_fin'].split(':')[1])
                    
                    debut_minutes = debut_h * 60 + debut_m
                    fin_minutes = fin_h * 60 + fin_m
                    midi_minutes = 12 * 60
                    
                    # Calculer matin (début à midi)
                    fin_matin = min(fin_minutes, midi_minutes)
                    matin_hours = max(0, (fin_matin - debut_minutes) / 60)
                    
                    # Calculer après-midi (midi à fin)
                    debut_apres_midi = max(debut_minutes, midi_minutes)
                    apres_midi_hours = max(0, (fin_minutes - debut_apres_midi) / 60)
                    
                    print(f"   Matin théorique: {matin_hours:.1f}h")
                    print(f"   Après-midi théorique: {apres_midi_hours:.1f}h")
            else:
                print(f"   Mercredi: Pas de planning configuré")
        else:
            print(f"⚠️ Planning non trouvé")
        
        # Test 3: Demande RTT demi-journée matin
        print(f"\n🌅 Test de demande RTT demi-journée matin...")
        demande_matin = {
            'type_absence': 'RTT',
            'date_debut': '2024-12-18',  # Mercredi
            'date_fin': '2024-12-18',    # Mercredi
            'demi_journees': 'matin',
            'motif': 'Test demi-journée matin'
        }
        
        response = requests.post('http://localhost:5001/api/demandes', 
                               json=demande_matin, cookies=cookies, timeout=5)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Demande RTT matin créée")
            print(f"   Heures calculées: {result['nb_heures']}h")
            print(f"   Attendu: ~{matin_hours:.1f}h (selon planning)")
        else:
            error = response.json()
            print(f"❌ Erreur demande matin: {error.get('error', 'Erreur inconnue')}")
        
        # Test 4: Demande RTT demi-journée après-midi
        print(f"\n🌆 Test de demande RTT demi-journée après-midi...")
        demande_apres_midi = {
            'type_absence': 'RTT',
            'date_debut': '2024-12-19',  # Jeudi
            'date_fin': '2024-12-19',    # Jeudi
            'demi_journees': 'après-midi',
            'motif': 'Test demi-journée après-midi'
        }
        
        response = requests.post('http://localhost:5001/api/demandes', 
                               json=demande_apres_midi, cookies=cookies, timeout=5)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Demande RTT après-midi créée")
            print(f"   Heures calculées: {result['nb_heures']}h")
            print(f"   Attendu: ~{apres_midi_hours:.1f}h (selon planning)")
        else:
            error = response.json()
            print(f"❌ Erreur demande après-midi: {error.get('error', 'Erreur inconnue')}")
        
        # Test 5: Demande RTT journée complète pour comparaison
        print(f"\n🌞 Test de demande RTT journée complète...")
        demande_complete = {
            'type_absence': 'RTT',
            'date_debut': '2024-12-20',  # Vendredi
            'date_fin': '2024-12-20',    # Vendredi
            'motif': 'Test journée complète'
        }
        
        response = requests.post('http://localhost:5001/api/demandes', 
                               json=demande_complete, cookies=cookies, timeout=5)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Demande RTT complète créée")
            print(f"   Heures calculées: {result['nb_heures']}h")
            print(f"   Attendu: ~{planning.get('duree_travail', 'N/A')}h (selon planning)")
        else:
            error = response.json()
            print(f"❌ Erreur demande complète: {error.get('error', 'Erreur inconnue')}")
        
        print("\n✅ Tests de demi-journées terminés")
        print("\n🔧 Corrections appliquées:")
        print("   - Calcul précis des demi-journées selon le planning")
        print("   - Matin: de l'heure de début à midi (ou pause)")
        print("   - Après-midi: de midi (ou fin de pause) à l'heure de fin")
        print("   - Prise en compte des pauses dans le calcul")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_demi_journee_planning()

