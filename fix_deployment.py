#!/usr/bin/env python3
"""
Script de correction du déploiement séparé Vercel + Render
"""

import subprocess
import sys
import os
from pathlib import Path

def fix_deployment():
    """Corrige le déploiement séparé"""
    print("🔧 Correction du déploiement séparé Vercel + Render")
    print("=" * 55)
    
    app_dir = Path(__file__).parent.absolute()
    
    try:
        # 1. Ajouter Flask-CORS aux requirements
        print("\n📦 Ajout de Flask-CORS...")
        requirements_file = app_dir / "requirements.txt"
        
        with open(requirements_file, 'r') as f:
            content = f.read()
        
        if "Flask-CORS" not in content:
            with open(requirements_file, 'a') as f:
                f.write("\nFlask-CORS==4.0.0\n")
            print("✅ Flask-CORS ajouté aux requirements")
        else:
            print("✅ Flask-CORS déjà présent")
        
        # 2. Modifier main.py pour Render
        print("\n🔧 Modification de main.py pour Render...")
        main_file = app_dir / "main.py"
        
        with open(main_file, 'r') as f:
            content = f.read()
        
        # Ajouter l'import Flask-CORS
        if "from flask_cors import CORS" not in content:
            content = content.replace(
                "from flask import Flask, request, jsonify, session",
                "from flask import Flask, request, jsonify, session\nfrom flask_cors import CORS"
            )
            print("✅ Import Flask-CORS ajouté")
        
        # Ajouter la configuration CORS
        if "CORS(app" not in content:
            # Trouver la ligne après l'initialisation de l'app
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "app = Flask(__name__" in line:
                    # Ajouter la configuration CORS après l'initialisation
                    lines.insert(i + 1, "")
                    lines.insert(i + 2, "# Configuration CORS pour Render")
                    lines.insert(i + 3, "CORS(app, origins=[")
                    lines.insert(i + 4, "    'https://app-manus-rh.vercel.app',")
                    lines.insert(i + 5, "    'http://localhost:3000',")
                    lines.insert(i + 6, "    'http://localhost:5173'")
                    lines.insert(i + 7, "])")
                    lines.insert(i + 8, "")
                    break
            
            content = '\n'.join(lines)
            print("✅ Configuration CORS ajoutée")
        
        # Ajouter la configuration pour Render
        if "os.environ.get('RENDER')" not in content:
            # Trouver la section de configuration de la base de données
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "app.config['SQLALCHEMY_DATABASE_URI']" in line:
                    # Remplacer par la configuration conditionnelle
                    lines[i] = "# Configuration de la base de données"
                    lines.insert(i + 1, "if os.environ.get('RENDER'):")
                    lines.insert(i + 2, "    # Mode production Render")
                    lines.insert(i + 3, "    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')")
                    lines.insert(i + 4, "    app.config['DEBUG'] = False")
                    lines.insert(i + 5, "else:")
                    lines.insert(i + 6, "    # Mode développement local")
                    lines.insert(i + 7, f"    app.config['SQLALCHEMY_DATABASE_URI'] = f\"sqlite:///{{DATABASE_PATH}}\"")
                    lines.insert(i + 8, "    app.config['DEBUG'] = True")
                    break
            
            content = '\n'.join(lines)
            print("✅ Configuration conditionnelle ajoutée")
        
        # Sauvegarder le fichier modifié
        with open(main_file, 'w') as f:
            f.write(content)
        
        # 3. Créer un fichier de configuration Render
        print("\n📄 Création du fichier de configuration Render...")
        render_config = app_dir / "render.yaml"
        
        render_content = """services:
  - type: web
    name: app-manus-rh-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: DATABASE_URL
        value: postgresql://user:password@host:port/database
      - key: MAIL_USERNAME
        value: your-email@gmail.com
      - key: MAIL_PASSWORD
        value: your-app-password
      - key: MAIL_DEFAULT_SENDER
        value: your-email@gmail.com
      - key: MAIL_SERVER
        value: smtp.gmail.com
      - key: MAIL_PORT
        value: 587
      - key: MAIL_USE_TLS
        value: true
"""
        
        with open(render_config, 'w') as f:
            f.write(render_content)
        
        print("✅ Fichier render.yaml créé")
        
        # 4. Commiter les changements
        print("\n💾 Commit des changements...")
        subprocess.run(['git', 'add', '.'], cwd=app_dir)
        subprocess.run(['git', 'commit', '-m', 'Fix: Configuration pour déploiement séparé Vercel + Render'], cwd=app_dir)
        
        # 5. Pousser vers GitHub
        print("📤 Push vers GitHub...")
        result = subprocess.run(['git', 'push', 'origin', 'main'], cwd=app_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Changements poussés vers GitHub")
            print("🔄 Vercel et Render redéploieront automatiquement")
        else:
            print(f"❌ Erreur lors du push: {result.stderr}")
            return False
        
        # 6. Afficher les instructions finales
        print("\n🎉 Corrections appliquées !")
        print("\n📋 Étapes suivantes :")
        print("1. Vérifier que Vercel redéploie : https://app-manus-rh.vercel.app")
        print("2. Vérifier que Render redéploie : https://app-manus-rh-api.onrender.com")
        print("3. Tester la connexion entre les deux services")
        print("4. Configurer les variables d'environnement sur Render")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def show_manual_steps():
    """Affiche les étapes manuelles"""
    print("\n📋 Étapes manuelles pour corriger le déploiement :")
    print("=" * 55)
    print("1. Sur Render (https://render.com) :")
    print("   - Aller dans le dashboard de votre service")
    print("   - Ajouter les variables d'environnement :")
    print("     * MAIL_USERNAME=votre-email@gmail.com")
    print("     * MAIL_PASSWORD=votre-mot-de-passe-app")
    print("     * MAIL_DEFAULT_SENDER=votre-email@gmail.com")
    print("     * MAIL_SERVER=smtp.gmail.com")
    print("     * MAIL_PORT=587")
    print("     * MAIL_USE_TLS=true")
    print("   - Redéployer le service")
    print("\n2. Sur Vercel (https://vercel.com) :")
    print("   - Vérifier que le déploiement s'est bien fait")
    print("   - Tester l'application : https://app-manus-rh.vercel.app")
    print("\n3. Tester la connexion :")
    print("   - Ouvrir https://app-manus-rh.vercel.app")
    print("   - Vérifier qu'il n'y a plus d'erreurs dans la console")
    print("   - Tester la connexion avec un compte par défaut")

if __name__ == "__main__":
    print("🔧 Correction du déploiement séparé")
    print("=" * 40)
    
    success = fix_deployment()
    
    if success:
        print("\n✅ Corrections appliquées avec succès !")
        show_manual_steps()
    else:
        print("\n❌ Erreur lors des corrections")
        show_manual_steps()
