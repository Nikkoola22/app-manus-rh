#!/usr/bin/env python3
"""
Configuration automatique de l'email
"""

import os
import sys
from pathlib import Path

def setup_email():
    """Configure l'email avec les paramètres par défaut"""
    print("📧 Configuration Email Automatique")
    print("=" * 40)
    
    # Configuration par défaut pour nikkoola@gmail.com
    email_config = {
        'MAIL_USERNAME': 'nikkoola@gmail.com',
        'MAIL_PASSWORD': 'votre-mot-de-passe-app-ici',  # À remplacer
        'MAIL_DEFAULT_SENDER': 'nikkoola@gmail.com',
        'MAIL_SERVER': 'smtp.gmail.com',
        'MAIL_PORT': '587',
        'MAIL_USE_TLS': 'True',
        'MAIL_USE_SSL': 'False'
    }
    
    # Créer le fichier .env
    env_content = "# Configuration Email Gmail\n"
    for key, value in email_config.items():
        env_content += f"{key}={value}\n"
    
    env_file = Path(__file__).parent / '.env'
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Fichier .env créé: {env_file}")
    print("\n📝 Configuration générée:")
    for key, value in email_config.items():
        if 'PASSWORD' in key:
            print(f"   {key}: {'*' * len(value)}")
        else:
            print(f"   {key}: {value}")
    
    print("\n🔧 Étapes suivantes:")
    print("   1. Aller sur https://myaccount.google.com/security")
    print("   2. Activer l'authentification à 2 facteurs")
    print("   3. Générer un mot de passe d'application")
    print("   4. Remplacer 'votre-mot-de-passe-app-ici' dans le fichier .env")
    print("   5. Tester avec: python3 test_email_config.py")
    
    print(f"\n📁 Fichier à modifier: {env_file}")
    
    # Installer python-dotenv
    print("\n📦 Installation de python-dotenv...")
    os.system(f"{sys.executable} -m pip install python-dotenv")
    
    print("\n🎉 Configuration terminée !")
    print("   Modifiez le fichier .env avec votre mot de passe d'application Gmail")

if __name__ == "__main__":
    setup_email()

