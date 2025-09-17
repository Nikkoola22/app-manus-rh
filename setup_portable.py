#!/usr/bin/env python3
"""
Script de configuration portable pour l'application RH
Détecte automatiquement l'OS et configure l'environnement
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

class PortableSetup:
    def __init__(self):
        self.app_dir = Path(__file__).parent.absolute()
        self.os_name = platform.system().lower()
        self.python_cmd = self._get_python_command()
        self.node_cmd = self._get_node_command()
        
    def _get_python_command(self):
        """Détermine la commande Python à utiliser"""
        if self.os_name == "windows":
            return "python"
        else:
            # Essayer python3 d'abord, puis python
            for cmd in ["python3", "python"]:
                if shutil.which(cmd):
                    return cmd
            return "python"
    
    def _get_node_command(self):
        """Détermine la commande Node.js à utiliser"""
        if self.os_name == "windows":
            return "node"
        else:
            return "node"
    
    def check_python(self):
        """Vérifie que Python est installé"""
        print("🐍 Vérification de Python...")
        try:
            result = subprocess.run([self.python_cmd, "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Python trouvé: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Python n'est pas installé ou n'est pas dans le PATH")
            print("   Veuillez installer Python 3.8+ depuis https://python.org")
            return False
    
    def check_node(self):
        """Vérifie que Node.js est installé"""
        print("📦 Vérification de Node.js...")
        try:
            result = subprocess.run([self.node_cmd, "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Node.js trouvé: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Node.js n'est pas installé ou n'est pas dans le PATH")
            print("   Veuillez installer Node.js depuis https://nodejs.org")
            return False
    
    def create_virtual_environment(self):
        """Crée l'environnement virtuel Python"""
        print("🔧 Création de l'environnement virtuel...")
        venv_path = self.app_dir / "venv"
        
        if venv_path.exists():
            print("✅ Environnement virtuel existant trouvé")
            return True
        
        try:
            subprocess.run([self.python_cmd, "-m", "venv", str(venv_path)], 
                          check=True, cwd=self.app_dir)
            print("✅ Environnement virtuel créé")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de la création de l'environnement virtuel: {e}")
            return False
    
    def get_pip_command(self):
        """Retourne la commande pip appropriée selon l'OS"""
        if self.os_name == "windows":
            return str(self.app_dir / "venv" / "Scripts" / "pip.exe")
        else:
            return str(self.app_dir / "venv" / "bin" / "pip")
    
    def install_python_dependencies(self):
        """Installe les dépendances Python"""
        print("📦 Installation des dépendances Python...")
        pip_cmd = self.get_pip_command()
        
        try:
            # Mettre à jour pip
            subprocess.run([pip_cmd, "install", "--upgrade", "pip"], 
                          check=True, cwd=self.app_dir)
            
            # Installer les dépendances
            subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], 
                          check=True, cwd=self.app_dir)
            print("✅ Dépendances Python installées")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation des dépendances Python: {e}")
            return False
    
    def install_node_dependencies(self):
        """Installe les dépendances Node.js"""
        print("📦 Installation des dépendances Node.js...")
        
        try:
            subprocess.run(["npm", "install"], 
                          check=True, cwd=self.app_dir)
            print("✅ Dépendances Node.js installées")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation des dépendances Node.js: {e}")
            return False
    
    def create_database_directory(self):
        """Crée le répertoire de base de données"""
        print("🗄️ Configuration de la base de données...")
        db_dir = self.app_dir / "database"
        db_dir.mkdir(exist_ok=True)
        print("✅ Répertoire de base de données créé")
        return True
    
    def create_launcher_scripts(self):
        """Crée les scripts de lancement pour chaque OS"""
        print("🚀 Création des scripts de lancement...")
        
        # Script Python universel
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
        launcher_path = self.app_dir / "launcher.py"
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
            with open(self.app_dir / "start.bat", 'w', encoding='utf-8') as f:
                f.write(batch_content)
        else:
            # Script shell Unix
            shell_content = '''#!/bin/bash
echo "🚀 Démarrage de l'application RH"
echo "================================="
python3 launcher.py
'''
            shell_path = self.app_dir / "start.sh"
            with open(shell_path, 'w', encoding='utf-8') as f:
                f.write(shell_content)
            os.chmod(shell_path, 0o755)
        
        print("✅ Scripts de lancement créés")
        return True
    
    def initialize_database(self):
        """Initialise la base de données avec les données de base"""
        print("🗄️ Initialisation de la base de données...")
        
        try:
            # Utiliser le Python de l'environnement virtuel
            if self.os_name == "windows":
                python_cmd = str(self.app_dir / "venv" / "Scripts" / "python.exe")
            else:
                python_cmd = str(self.app_dir / "venv" / "bin" / "python")
            
            subprocess.run([python_cmd, "init_portable_data.py"], 
                          check=True, cwd=self.app_dir)
            print("✅ Base de données initialisée")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
            return False

    def run_setup(self):
        """Exécute la configuration complète"""
        print("🔧 Configuration portable de l'application RH")
        print("=" * 50)
        print(f"📁 Répertoire de l'application: {self.app_dir}")
        print(f"🖥️  Système d'exploitation: {self.os_name}")
        print()
        
        # Vérifications préalables
        if not self.check_python():
            return False
        
        if not self.check_node():
            return False
        
        # Configuration
        if not self.create_virtual_environment():
            return False
        
        if not self.install_python_dependencies():
            return False
        
        if not self.install_node_dependencies():
            return False
        
        if not self.create_database_directory():
            return False
        
        if not self.initialize_database():
            return False
        
        if not self.create_launcher_scripts():
            return False
        
        print("\n🎉 Configuration terminée avec succès!")
        print("\n📝 Pour démarrer l'application:")
        if self.os_name == "windows":
            print("   Double-cliquez sur start.bat")
            print("   ou exécutez: python launcher.py")
        else:
            print("   Exécutez: ./start.sh")
            print("   ou exécutez: python3 launcher.py")
        
        return True

if __name__ == "__main__":
    setup = PortableSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)
