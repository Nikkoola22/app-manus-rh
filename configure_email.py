#!/usr/bin/env python3
"""
Configuration email pour l'application RH
"""

import os
import sys
from pathlib import Path

def configure_email():
    """Configure l'envoi d'emails avec Gmail"""
    print("📧 Configuration Email pour l'Application RH")
    print("=" * 50)
    
    print("\n🔧 Configuration Gmail requise:")
    print("   1. Activer l'authentification à 2 facteurs sur votre compte Gmail")
    print("   2. Générer un mot de passe d'application")
    print("   3. Configurer les variables d'environnement")
    
    print("\n📝 Étapes détaillées:")
    print("   1. Aller sur https://myaccount.google.com/security")
    print("   2. Activer 'Authentification à 2 facteurs'")
    print("   3. Aller dans 'Mots de passe des applications'")
    print("   4. Sélectionner 'Autre' et nommer 'Application RH'")
    print("   5. Copier le mot de passe généré (16 caractères)")
    
    print("\n⚙️ Configuration des variables d'environnement:")
    
    email = input("\n📧 Votre adresse Gmail: ").strip()
    if not email or '@gmail.com' not in email:
        print("❌ Adresse Gmail invalide")
        return
    
    password = input("🔑 Mot de passe d'application Gmail: ").strip()
    if not password or len(password) != 16:
        print("❌ Mot de passe d'application invalide (doit faire 16 caractères)")
        return
    
    print(f"\n✅ Configuration détectée:")
    print(f"   MAIL_USERNAME: {email}")
    print(f"   MAIL_PASSWORD: {'*' * 16}")
    print(f"   MAIL_DEFAULT_SENDER: {email}")
    
    # Créer un fichier .env
    env_content = f"""# Configuration Email Gmail
MAIL_USERNAME={email}
MAIL_PASSWORD={password}
MAIL_DEFAULT_SENDER={email}
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
"""
    
    env_file = Path(__file__).parent / '.env'
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"\n💾 Configuration sauvegardée dans: {env_file}")
    
    # Modifier le service email pour charger le .env
    print("\n🔧 Modification du service email...")
    
    email_service_path = Path(__file__).parent / 'src' / 'services' / 'email_service.py'
    
    with open(email_service_path, 'r') as f:
        content = f.read()
    
    # Ajouter le chargement du .env au début
    if 'from dotenv import load_dotenv' not in content:
        new_content = content.replace(
            'from flask import current_app',
            'from flask import current_app\nfrom dotenv import load_dotenv\nimport os\n\n# Charger les variables d\'environnement\ntry:\n    load_dotenv()\nexcept ImportError:\n    pass'
        )
        
        with open(email_service_path, 'w') as f:
            f.write(new_content)
    
    print("✅ Service email modifié")
    
    # Installer python-dotenv si nécessaire
    print("\n📦 Installation de python-dotenv...")
    os.system(f"{sys.executable} -m pip install python-dotenv")
    
    print("\n🎉 Configuration terminée !")
    print("\n📱 Pour tester l'envoi d'emails:")
    print("   1. Redémarrer l'application")
    print("   2. Se connecter comme responsable")
    print("   3. Créer une demande de congé")
    print("   4. Valider la demande")
    print("   5. Vérifier l'email reçu")
    
    print(f"\n🧪 Test direct:")
    print(f"   python3 test_email_config.py")

if __name__ == "__main__":
    configure_email()

