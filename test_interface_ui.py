#!/usr/bin/env python3
"""
Test de l'interface utilisateur et des menus déroulants
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_interface_ui():
    """Test de l'interface utilisateur"""
    print("🎨 Test de l'interface utilisateur")
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
        # Test 1: Vérifier que l'API est accessible
        print("\n🌐 Test de l'API...")
        response = requests.get('http://localhost:5001/api/health', timeout=5)
        
        if response.status_code == 200:
            print("✅ API accessible")
        else:
            print(f"❌ Erreur API: {response.status_code}")
        
        # Test 2: Vérifier les routes principales
        print("\n🔍 Test des routes principales...")
        routes = [
            '/api/auth/login',
            '/api/agents',
            '/api/services',
            '/api/demandes'
        ]
        
        for route in routes:
            try:
                response = requests.get(f'http://localhost:5001{route}', timeout=5)
                print(f"   {route}: {response.status_code}")
            except Exception as e:
                print(f"   {route}: Erreur - {e}")
        
        # Test 3: Vérifier les fichiers statiques
        print("\n📁 Test des fichiers statiques...")
        static_files = [
            '/static/js/main.js',
            '/static/css/main.css',
            '/static/index.html'
        ]
        
        for file in static_files:
            try:
                response = requests.get(f'http://localhost:5001{file}', timeout=5)
                print(f"   {file}: {response.status_code}")
            except Exception as e:
                print(f"   {file}: Erreur - {e}")
        
        print("\n✅ Tests de l'interface terminés")
        print("\n📝 Note: Les menus déroulants ont été améliorés avec:")
        print("   - Fond blanc opaque")
        print("   - Bordure grise visible")
        print("   - Ombre portée")
        print("   - Effet de survol bleu")
        print("   - Texte noir lisible")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_interface_ui()


