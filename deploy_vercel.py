#!/usr/bin/env python3
"""
Script de déploiement sur Vercel
"""

import subprocess
import sys
import os
from pathlib import Path

def deploy_vercel():
    """Déploie l'application sur Vercel"""
    print("🚀 Déploiement sur Vercel")
    print("=" * 30)
    
    app_dir = Path(__file__).parent.absolute()
    
    try:
        # Vérifier que nous sommes dans le bon répertoire
        if not (app_dir / "main.py").exists():
            print("❌ Erreur: main.py non trouvé")
            return False
        
        # Vérifier que vercel.json existe
        if not (app_dir / "vercel.json").exists():
            print("❌ Erreur: vercel.json non trouvé")
            return False
        
        print("✅ Fichiers de configuration trouvés")
        
        # Construire le frontend
        print("\n🔨 Construction du frontend...")
        result = subprocess.run(['npm', 'run', 'build'], cwd=app_dir, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Erreur lors de la construction: {result.stderr}")
            return False
        
        print("✅ Frontend construit avec succès")
        
        # Vérifier que le dossier dist existe
        if not (app_dir / "dist").exists():
            print("❌ Erreur: Dossier dist non créé")
            return False
        
        print("✅ Dossier dist créé")
        
        # Commiter les changements
        print("\n💾 Commit des changements...")
        subprocess.run(['git', 'add', '.'], cwd=app_dir)
        subprocess.run(['git', 'commit', '-m', 'Deploy: Configuration Vercel'], cwd=app_dir)
        
        # Pousser vers GitHub
        print("📤 Push vers GitHub...")
        result = subprocess.run(['git', 'push', 'origin', 'main'], cwd=app_dir, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Erreur lors du push: {result.stderr}")
            return False
        
        print("✅ Changements poussés vers GitHub")
        
        # Vérifier si Vercel CLI est installé
        print("\n🔍 Vérification de Vercel CLI...")
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("⚠️  Vercel CLI non installé")
            print("📦 Installation de Vercel CLI...")
            subprocess.run(['npm', 'install', '-g', 'vercel'], cwd=app_dir)
        
        print("✅ Vercel CLI prêt")
        
        # Déployer sur Vercel
        print("\n🚀 Déploiement sur Vercel...")
        print("📝 Suivez les instructions à l'écran")
        
        result = subprocess.run(['vercel', '--prod'], cwd=app_dir)
        
        if result.returncode == 0:
            print("✅ Déploiement réussi !")
            print("🌐 Votre application est maintenant en ligne")
            return True
        else:
            print("❌ Erreur lors du déploiement")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def check_requirements():
    """Vérifie les prérequis pour le déploiement"""
    print("🔍 Vérification des prérequis...")
    
    # Vérifier Node.js
    result = subprocess.run(['node', '--version'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Node.js non installé")
        return False
    print(f"✅ Node.js: {result.stdout.strip()}")
    
    # Vérifier npm
    result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ npm non installé")
        return False
    print(f"✅ npm: {result.stdout.strip()}")
    
    # Vérifier Git
    result = subprocess.run(['git', '--version'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Git non installé")
        return False
    print(f"✅ Git: {result.stdout.strip()}")
    
    return True

def show_manual_steps():
    """Affiche les étapes manuelles pour le déploiement"""
    print("\n📋 Étapes manuelles pour le déploiement Vercel:")
    print("=" * 50)
    print("1. Aller sur https://vercel.com")
    print("2. Se connecter avec GitHub")
    print("3. Cliquer sur 'New Project'")
    print("4. Sélectionner le dépôt 'app-manus-rh'")
    print("5. Configurer:")
    print("   - Framework Preset: Other")
    print("   - Build Command: npm run build")
    print("   - Output Directory: dist")
    print("   - Install Command: npm install")
    print("6. Cliquer sur 'Deploy'")
    print("\n7. Configurer les variables d'environnement:")
    print("   - MAIL_USERNAME=votre-email@gmail.com")
    print("   - MAIL_PASSWORD=votre-mot-de-passe-app")
    print("   - MAIL_DEFAULT_SENDER=votre-email@gmail.com")
    print("   - MAIL_SERVER=smtp.gmail.com")
    print("   - MAIL_PORT=587")
    print("   - MAIL_USE_TLS=true")

if __name__ == "__main__":
    print("🌐 Déploiement Vercel - Application de Gestion RH")
    print("=" * 55)
    
    if not check_requirements():
        print("\n❌ Prérequis manquants. Veuillez les installer d'abord.")
        sys.exit(1)
    
    print("\n✅ Tous les prérequis sont satisfaits")
    
    # Demander le mode de déploiement
    print("\n🔧 Choisissez le mode de déploiement:")
    print("1. Automatique (avec Vercel CLI)")
    print("2. Manuel (via interface web)")
    
    choice = input("\nVotre choix (1 ou 2): ").strip()
    
    if choice == "1":
        success = deploy_vercel()
        if not success:
            print("\n⚠️  Déploiement automatique échoué")
            show_manual_steps()
    elif choice == "2":
        show_manual_steps()
    else:
        print("❌ Choix invalide")
        show_manual_steps()
