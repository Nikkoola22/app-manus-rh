#!/usr/bin/env python3
"""
Test de configuration email
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_email_config():
    """Test de la configuration email"""
    print("📧 Test de configuration email")
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
            cookies = response.cookies
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test d'envoi d'email de test
        print("\n📧 Test d'envoi d'email...")
        response = requests.post('http://localhost:5001/api/test-email', 
                               json={'email': 'nikkoola@gmail.com'}, 
                               cookies=cookies, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Email de test envoyé: {result.get('message', 'Succès')}")
        else:
            error = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'error': 'Erreur inconnue'}
            print(f"❌ Erreur envoi email: {error.get('error', 'Erreur inconnue')}")
        
        print("\n🔧 Configuration email actuelle:")
        print("   MAIL_SERVER: smtp.gmail.com")
        print("   MAIL_PORT: 587")
        print("   MAIL_USE_TLS: True")
        print("   MAIL_USERNAME: (non configuré)")
        print("   MAIL_PASSWORD: (non configuré)")
        print("   MAIL_DEFAULT_SENDER: noreply@entreprise.com")
        
        print("\n📝 Pour configurer Gmail:")
        print("   1. Créer un mot de passe d'application Gmail")
        print("   2. Configurer les variables d'environnement:")
        print("      export MAIL_USERNAME='votre-email@gmail.com'")
        print("      export MAIL_PASSWORD='votre-mot-de-passe-app'")
        print("      export MAIL_DEFAULT_SENDER='votre-email@gmail.com'")
        print("   3. Redémarrer l'application")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_email_config()
