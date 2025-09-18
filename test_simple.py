#!/usr/bin/env python3
"""
Test simple de l'application
"""

import subprocess
import time
import requests
from pathlib import Path

def test_app():
    print("🧪 Test simple de l'application")
    print("=" * 40)
    
    app_dir = Path(__file__).parent.absolute()
    python_cmd = str(app_dir / "venv" / "bin" / "python")
    
    print("🐍 Démarrage de Flask...")
    try:
        # Lancer Flask
        process = subprocess.Popen(
            [python_cmd, "main.py"],
            cwd=app_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Attendre
        time.sleep(3)
        
        # Tester l'API
        try:
            response = requests.get('http://localhost:5001/api/auth/check-session', timeout=5)
            if response.status_code in [200, 401, 403]:
                print("✅ API accessible")
                print(f"   Status: {response.status_code}")
            else:
                print(f"⚠️  API répond avec status: {response.status_code}")
        except Exception as e:
            print(f"❌ API non accessible: {e}")
        
        # Arrêter Flask
        process.terminate()
        process.wait()
        print("✅ Flask arrêté")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_app()


