#!/usr/bin/env python3
"""
Script de build pour créer une version portable de l'application RH
Génère un package complet avec toutes les dépendances
"""

import os
import sys
import shutil
import subprocess
import zipfile
import platform
from pathlib import Path
from datetime import datetime

class PortableBuilder:
    def __init__(self):
        self.app_dir = Path(__file__).parent.absolute()
        self.build_dir = self.app_dir / "build"
        self.portable_dir = self.build_dir / "app-manus-rh-portable"
        self.os_name = platform.system().lower()
        
    def clean_build_directory(self):
        """Nettoie le répertoire de build"""
        print("🧹 Nettoyage du répertoire de build...")
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        self.build_dir.mkdir(exist_ok=True)
        print("✅ Répertoire de build nettoyé")
    
    def create_portable_structure(self):
        """Crée la structure du package portable"""
        print("📁 Création de la structure portable...")
        
        # Créer le répertoire principal
        self.portable_dir.mkdir(exist_ok=True)
        
        # Créer les sous-répertoires nécessaires
        (self.portable_dir / "database").mkdir(exist_ok=True)
        (self.portable_dir / "static").mkdir(exist_ok=True)
        (self.portable_dir / "src").mkdir(exist_ok=True)
        
        print("✅ Structure portable créée")
    
    def copy_application_files(self):
        """Copie les fichiers de l'application"""
        print("📋 Copie des fichiers de l'application...")
        
        # Fichiers Python essentiels
        essential_files = [
            "main.py",
            "requirements.txt",
            "setup_portable.py",
            "init_data.py"
        ]
        
        for file in essential_files:
            src = self.app_dir / file
            if src.exists():
                shutil.copy2(src, self.portable_dir)
        
        # Copier le dossier src
        if (self.app_dir / "src").exists():
            shutil.copytree(self.app_dir / "src", self.portable_dir / "src", dirs_exist_ok=True)
        
        # Copier les fichiers de configuration
        config_files = [
            "package.json",
            "vite.config.js",
            "tailwind.config.js",
            "postcss.config.js"
        ]
        
        for file in config_files:
            src = self.app_dir / file
            if src.exists():
                shutil.copy2(src, self.portable_dir)
        
        # Copier les guides et documentation
        guide_files = [f for f in self.app_dir.glob("GUIDE_*.md")]
        for guide in guide_files:
            shutil.copy2(guide, self.portable_dir)
        
        # Copier README si il existe
        if (self.app_dir / "README.md").exists():
            shutil.copy2(self.app_dir / "README.md", self.portable_dir)
        
        print("✅ Fichiers de l'application copiés")
    
    def create_installation_script(self):
        """Crée le script d'installation automatique"""
        print("🔧 Création du script d'installation...")
        
        install_script = f'''#!/usr/bin/env python3
"""
Script d'installation automatique pour l'application RH portable
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def main():
    print("🚀 Installation de l'application RH portable")
    print("=" * 50)
    
    # Vérifier Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        return False
    
    print(f"✅ Python {{sys.version}} détecté")
    
    # Vérifier Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ Node.js {{result.stdout.strip()}} détecté")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js requis mais non trouvé")
        print("   Installez Node.js depuis https://nodejs.org")
        return False
    
    # Exécuter le setup
    try:
        subprocess.run([sys.executable, "setup_portable.py"], check=True)
        print("\\n🎉 Installation terminée avec succès!")
        print("\\n📝 Pour démarrer l'application:")
        if platform.system().lower() == "windows":
            print("   Double-cliquez sur start.bat")
        else:
            print("   Exécutez: ./start.sh")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {{e}}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''
        
        install_path = self.portable_dir / "install.py"
        with open(install_path, 'w', encoding='utf-8') as f:
            f.write(install_script)
        
        # Rendre exécutable sur Unix
        if self.os_name != "windows":
            os.chmod(install_path, 0o755)
        
        print("✅ Script d'installation créé")
    
    def create_readme(self):
        """Crée un README pour le package portable"""
        print("📖 Création du README portable...")
        
        readme_content = f'''# Application RH - Version Portable

## Description
Application de gestion des ressources humaines (congés, RTT, arrêts maladie, présence) - Version portable.

## Prérequis
- Python 3.8 ou supérieur
- Node.js 16 ou supérieur

## Installation rapide

### Windows
1. Double-cliquez sur `install.py`
2. Attendez la fin de l'installation
3. Double-cliquez sur `start.bat`

### macOS/Linux
1. Ouvrez un terminal dans ce dossier
2. Exécutez: `python3 install.py`
3. Exécutez: `./start.sh`

## Installation manuelle

1. Installez Python 3.8+ depuis https://python.org
2. Installez Node.js depuis https://nodejs.org
3. Exécutez: `python3 setup_portable.py`

## Utilisation

### Démarrage
- **Windows**: Double-cliquez sur `start.bat`
- **macOS/Linux**: Exécutez `./start.sh` ou `python3 launcher.py`

### Accès
- Application: http://localhost:5173
- API Backend: http://localhost:5001

### Identifiants de test
- **Admin**: admin@exemple.com / admin123
- **Responsable**: jean.martin@exemple.com / resp123
- **Agent**: sofiane.bendaoud@exemple.com / agent123

## Structure du package
```
app-manus-rh-portable/
├── install.py          # Script d'installation automatique
├── setup_portable.py   # Configuration de l'environnement
├── launcher.py         # Lanceur de l'application
├── start.bat           # Script de démarrage Windows
├── start.sh            # Script de démarrage Unix
├── main.py             # Application principale
├── requirements.txt    # Dépendances Python
├── package.json        # Dépendances Node.js
├── database/           # Base de données SQLite
├── static/             # Fichiers statiques
└── src/                # Code source de l'application
```

## Fonctionnalités
- ✅ Gestion des agents et services
- ✅ Demandes de congés et RTT
- ✅ Arrêts maladie
- ✅ Gestion de la présence
- ✅ Notifications email
- ✅ Interface moderne et responsive
- ✅ Base de données SQLite portable

## Support
Pour toute question ou problème, consultez les guides dans le dossier.

## Version
Générée le {datetime.now().strftime("%d/%m/%Y à %H:%M")}
'''
        
        readme_path = self.portable_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ README portable créé")
    
    def create_launcher_scripts(self):
        """Crée les scripts de lancement pour chaque OS"""
        print("🚀 Création des scripts de lancement...")
        
        # Launcher Python universel (déjà créé par setup_portable.py)
        launcher_content = f'''#!/usr/bin/env python3
"""
Launcher portable pour l'application RH
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class AppLauncher:
    def __init__(self):
        self.app_dir = Path(__file__).parent.absolute()
        self.flask_process = None
        self.vite_process = None
        self.running = True
        
    def get_python_command(self):
        """Retourne la commande Python appropriée"""
        if os.name == 'nt':  # Windows
            return str(self.app_dir / "venv" / "Scripts" / "python.exe")
        else:  # Unix/Linux/macOS
            return str(self.app_dir / "venv" / "bin" / "python")
    
    def get_node_command(self):
        """Retourne la commande Node.js appropriée"""
        return "node"
    
    def start_flask(self):
        """Démarre le serveur Flask"""
        print("🐍 Démarrage du serveur Flask (port 5001)...")
        try:
            python_cmd = self.get_python_command()
            cmd = [python_cmd, "main.py"]
            self.flask_process = subprocess.Popen(
                cmd, 
                cwd=self.app_dir,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Attendre que Flask démarre
            for i in range(10):
                try:
                    import requests
                    response = requests.get('http://localhost:5001/api/auth/check-session', timeout=2)
                    if response.status_code == 200:
                        print("✅ Serveur Flask démarré avec succès")
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"   Attente du démarrage de Flask... ({{i+1}}/10)")
            
            print("❌ Timeout lors du démarrage de Flask")
            return False
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage de Flask: {{e}}")
            return False
    
    def start_vite(self):
        """Démarre le serveur Vite"""
        print("⚡ Démarrage du serveur Vite (port 5173)...")
        try:
            node_cmd = self.get_node_command()
            cmd = [node_cmd, "run", "dev"]
            self.vite_process = subprocess.Popen(
                cmd,
                cwd=self.app_dir,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Attendre que Vite démarre
            for i in range(15):
                try:
                    import requests
                    response = requests.get('http://localhost:5173/', timeout=2)
                    if response.status_code == 200:
                        print("✅ Serveur Vite démarré avec succès")
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"   Attente du démarrage de Vite... ({{i+1}}/15)")
            
            print("❌ Timeout lors du démarrage de Vite")
            return False
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage de Vite: {{e}}")
            return False
    
    def cleanup(self):
        """Nettoie les processus"""
        print("\\n🧹 Arrêt des serveurs...")
        self.running = False
        
        if self.flask_process:
            try:
                self.flask_process.terminate()
                print("✅ Serveur Flask arrêté")
            except:
                pass
        
        if self.vite_process:
            try:
                self.vite_process.terminate()
                print("✅ Serveur Vite arrêté")
            except:
                pass
    
    def run(self):
        """Lance l'application"""
        print("🚀 Démarrage de l'application RH")
        print("=" * 50)
        
        try:
            # Démarrer Flask
            if not self.start_flask():
                print("❌ Impossible de démarrer Flask")
                return False
            
            # Démarrer Vite
            if not self.start_vite():
                print("❌ Impossible de démarrer Vite")
                return False
            
            print("\\n🎉 Application démarrée avec succès!")
            print("\\n🌐 URLs d'accès:")
            print("   Application: http://localhost:5173")
            print("   API Backend: http://localhost:5001")
            print("\\n🔑 Identifiants de test:")
            print("   Admin: admin@exemple.com / admin123")
            print("   Responsable: jean.martin@exemple.com / resp123")
            print("   Agent: sofiane.bendaoud@exemple.com / agent123")
            print("\\n📝 Pour arrêter l'application: Ctrl+C")
            
            # Ouvrir l'application
            try:
                import webbrowser
                webbrowser.open('http://localhost:5173')
                print("🌐 Application ouverte dans le navigateur")
            except:
                print("⚠️  Impossible d'ouvrir automatiquement le navigateur")
            
            # Attendre l'interruption
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\\n\\n🛑 Arrêt demandé par l'utilisateur")
        except Exception as e:
            print(f"\\n❌ Erreur inattendue: {{e}}")
        finally:
            self.cleanup()
            print("\\n👋 Application arrêtée")

if __name__ == "__main__":
    launcher = AppLauncher()
    launcher.run()
'''
        
        # Écrire le launcher Python
        launcher_path = self.portable_dir / "launcher.py"
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        # Rendre le script exécutable sur Unix
        if self.os_name != "windows":
            os.chmod(launcher_path, 0o755)
        
        # Créer des scripts batch/shell selon l'OS
        if self.os_name == "windows":
            # Script batch Windows
            batch_content = '''@echo off
echo 🚀 Démarrage de l'application RH
echo =================================
python launcher.py
pause
'''
            with open(self.portable_dir / "start.bat", 'w', encoding='utf-8') as f:
                f.write(batch_content)
        else:
            # Script shell Unix
            shell_content = '''#!/bin/bash
echo "🚀 Démarrage de l'application RH"
echo "================================="
python3 launcher.py
'''
            shell_path = self.portable_dir / "start.sh"
            with open(shell_path, 'w', encoding='utf-8') as f:
                f.write(shell_content)
            os.chmod(shell_path, 0o755)
        
        print("✅ Scripts de lancement créés")
    
    def create_zip_package(self):
        """Crée un package ZIP portable"""
        print("📦 Création du package ZIP...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"app-manus-rh-portable-{timestamp}.zip"
        zip_path = self.build_dir / zip_name
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.portable_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(self.portable_dir)
                    zipf.write(file_path, arc_path)
        
        print(f"✅ Package ZIP créé: {zip_path}")
        return zip_path
    
    def build(self):
        """Exécute le build complet"""
        print("🔨 Build de l'application portable")
        print("=" * 50)
        
        try:
            self.clean_build_directory()
            self.create_portable_structure()
            self.copy_application_files()
            self.create_installation_script()
            self.create_readme()
            self.create_launcher_scripts()
            
            zip_path = self.create_zip_package()
            
            print(f"\\n🎉 Build terminé avec succès!")
            print(f"📦 Package portable: {zip_path}")
            print(f"📁 Dossier portable: {self.portable_dir}")
            print("\\n📝 Instructions de distribution:")
            print("   1. Partagez le fichier ZIP")
            print("   2. L'utilisateur extrait le ZIP")
            print("   3. L'utilisateur exécute install.py")
            print("   4. L'utilisateur lance l'application avec start.bat/start.sh")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du build: {e}")
            return False

if __name__ == "__main__":
    builder = PortableBuilder()
    success = builder.build()
    sys.exit(0 if success else 1)
