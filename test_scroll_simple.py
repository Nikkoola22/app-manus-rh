#!/usr/bin/env python3
"""
Test simple du scroll automatique
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_scroll_simple():
    """Test simple du scroll automatique"""
    print("🔍 Test simple du scroll automatique")
    print("=" * 40)
    
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
        # Test de connexion
        print("\n👤 Test de connexion...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'jean.martin@exemple.com', 'password': 'resp123'},
                               timeout=5)
        
        if response.status_code == 200:
            print("✅ Connexion réussie")
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test de l'interface
        print("\n🌐 Test de l'interface...")
        response = requests.get('http://localhost:5001', timeout=5)
        
        if response.status_code == 200:
            print("✅ Interface accessible")
        else:
            print(f"❌ Interface non accessible: {response.status_code}")
            return
        
        print("\n📱 Instructions de test:")
        print("   1. Ouvrir http://localhost:5001")
        print("   2. Se connecter (jean.martin@exemple.com / resp123)")
        print("   3. Ouvrir la console (F12)")
        print("   4. Cliquer sur les onglets de demandes")
        print("   5. Vérifier les logs dans la console")
        
        print("\n⏳ Application en cours... (Ctrl+C pour arrêter)")
        
        # Attendre
        time.sleep(30)
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_scroll_simple()


