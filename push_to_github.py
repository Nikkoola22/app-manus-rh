#!/usr/bin/env python3
"""
Script pour pousser l'application sur GitHub
"""

import subprocess
import sys
import os
from pathlib import Path

def push_to_github():
    """Pousse l'application sur GitHub"""
    print("🚀 Push de l'application sur GitHub")
    print("=" * 40)
    
    app_dir = Path(__file__).parent.absolute()
    
    try:
        # Vérifier si git est configuré
        print("🔍 Vérification de la configuration Git...")
        result = subprocess.run(['git', 'config', '--global', 'user.name'], 
                              capture_output=True, text=True, cwd=app_dir)
        if not result.stdout.strip():
            print("❌ Git n'est pas configuré. Configuration nécessaire:")
            print("   git config --global user.name 'Votre Nom'")
            print("   git config --global user.email 'votre.email@example.com'")
            return False
        
        print("✅ Git configuré")
        
        # Vérifier l'état du dépôt
        print("\n📊 État du dépôt...")
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=app_dir)
        if result.stdout.strip():
            print("⚠️  Fichiers non commités détectés:")
            print(result.stdout)
            print("Committing les changements...")
            subprocess.run(['git', 'add', '.'], cwd=app_dir)
            subprocess.run(['git', 'commit', '-m', 'Update: Améliorations et corrections'], cwd=app_dir)
        
        # Vérifier les remotes
        print("\n🔗 Vérification des remotes...")
        result = subprocess.run(['git', 'remote', '-v'], 
                              capture_output=True, text=True, cwd=app_dir)
        
        if not result.stdout.strip():
            print("📝 Aucun remote configuré. Instructions pour créer le dépôt GitHub:")
            print("\n1. Aller sur https://github.com/new")
            print("2. Créer un nouveau dépôt nommé 'app-rh'")
            print("3. Ne pas initialiser avec README (déjà présent)")
            print("4. Copier l'URL du dépôt")
            print("5. Exécuter les commandes suivantes:")
            print("\n   git remote add origin https://github.com/VOTRE_USERNAME/app-rh.git")
            print("   git push -u origin main")
            return False
        
        print("✅ Remote configuré:")
        print(result.stdout)
        
        # Pousser vers GitHub
        print("\n🚀 Push vers GitHub...")
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                              cwd=app_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Push réussi !")
            print("🎉 Application disponible sur GitHub")
            return True
        else:
            print("❌ Erreur lors du push:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def create_github_repo_instructions():
    """Affiche les instructions pour créer le dépôt GitHub"""
    print("\n📋 Instructions pour créer le dépôt GitHub:")
    print("=" * 50)
    print("1. Aller sur https://github.com/new")
    print("2. Nom du dépôt: app-rh")
    print("3. Description: Application de Gestion RH complète")
    print("4. Visibilité: Public ou Privé (selon votre choix)")
    print("5. NE PAS cocher 'Add a README file'")
    print("6. NE PAS cocher 'Add .gitignore'")
    print("7. NE PAS cocher 'Choose a license'")
    print("8. Cliquer sur 'Create repository'")
    print("\n9. Copier l'URL du dépôt (ex: https://github.com/VOTRE_USERNAME/app-rh.git)")
    print("10. Exécuter les commandes suivantes:")
    print("\n   git remote add origin https://github.com/VOTRE_USERNAME/app-rh.git")
    print("   git push -u origin main")

if __name__ == "__main__":
    success = push_to_github()
    
    if not success:
        create_github_repo_instructions()
        
        # Demander l'URL du dépôt
        repo_url = input("\n📝 Entrez l'URL de votre dépôt GitHub: ").strip()
        
        if repo_url:
            try:
                app_dir = Path(__file__).parent.absolute()
                
                # Ajouter le remote
                print(f"\n🔗 Ajout du remote: {repo_url}")
                subprocess.run(['git', 'remote', 'add', 'origin', repo_url], cwd=app_dir)
                
                # Push
                print("🚀 Push vers GitHub...")
                result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                                      cwd=app_dir, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Push réussi !")
                    print(f"🎉 Application disponible sur: {repo_url}")
                else:
                    print("❌ Erreur lors du push:")
                    print(result.stderr)
                    
            except Exception as e:
                print(f"❌ Erreur: {e}")
        else:
            print("❌ URL non fournie. Push annulé.")

