#!/usr/bin/env python3
"""
Test de débogage du scroll automatique
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_scroll_debug():
    """Test de débogage du scroll automatique"""
    print("🐛 Test de débogage du scroll automatique")
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
        
        # Test 2: Vérifier que l'application répond
        print(f"\n🌐 Test de l'interface web...")
        response = requests.get('http://localhost:5001', timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Interface web accessible")
            print(f"   Taille de la réponse: {len(response.text)} caractères")
        else:
            print(f"❌ Interface web non accessible: {response.status_code}")
        
        print("\n🔧 Instructions de débogage:")
        print("   1. Ouvrir http://localhost:5001 dans le navigateur")
        print("   2. Se connecter comme responsable (jean.martin@exemple.com / resp123)")
        print("   3. Ouvrir la console développeur (F12)")
        print("   4. Cliquer sur les onglets 'Demandes en attente', 'Demandes traitées', 'Mes Demandes'")
        print("   5. Vérifier les logs dans la console:")
        print("      - 'Tab changed to: [valeur]'")
        print("      - 'Attempting scroll for: [valeur]'")
        print("      - 'Scrolling to [section]' ou 'No scroll - ref not found'")
        
        print("\n🔍 Problèmes possibles:")
        print("   - Les refs ne sont pas correctement attachés")
        print("   - La fonction handleTabChange n'est pas appelée")
        print("   - Le composant Tabs n'utilise pas onValueChange")
        print("   - Les éléments ne sont pas encore rendus au moment du scroll")
        
        print("\n⏳ Application en cours d'exécution...")
        print("   Appuyez sur Ctrl+C pour arrêter")
        
        # Garder l'application en vie pour les tests manuels
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé par l'utilisateur")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_scroll_debug()

