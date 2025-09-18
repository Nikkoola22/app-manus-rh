#!/usr/bin/env python3
"""
Launcher final simplifié et fiable pour l'application RH portable
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

class SimpleLauncher:
    def __init__(self):
        self.app_dir = Path(__file__).parent.absolute()
        self.flask_process = None
        self.vite_process = None
        
    def get_python_command(self):
        """Retourne la commande Python de l'environnement virtuel"""
        if os.name == 'nt':  # Windows
            return str(self.app_dir / "venv" / "Scripts" / "python.exe")
        else:  # Unix/Linux/macOS
            return str(self.app_dir / "venv" / "bin" / "python")
    
    def start_flask(self):
        """Démarre Flask"""
        print("🐍 Démarrage de Flask (port 5001)...")
        
        python_cmd = self.get_python_command()
        if not os.path.exists(python_cmd):
            print(f"❌ Python non trouvé: {python_cmd}")
            return False
        
        try:
            self.flask_process = subprocess.Popen(
                [python_cmd, "main.py"],
                cwd=self.app_dir
            )
            
            # Attendre un peu
            time.sleep(2)
            
            if self.flask_process.poll() is None:
                print("✅ Flask démarré")
                return True
            else:
                print("❌ Flask n'a pas démarré")
                return False
                
        except Exception as e:
            print(f"❌ Erreur Flask: {e}")
            return False
    
    def start_vite(self):
        """Démarre Vite"""
        print("⚡ Démarrage de Vite (port 5173)...")
        
        try:
            self.vite_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=self.app_dir
            )
            
            # Attendre un peu
            time.sleep(3)
            
            if self.vite_process.poll() is None:
                print("✅ Vite démarré")
                return True
            else:
                print("❌ Vite n'a pas démarré")
                return False
                
        except Exception as e:
            print(f"❌ Erreur Vite: {e}")
            return False
    
    def cleanup(self):
        """Arrête les processus"""
        print("\n🧹 Arrêt des serveurs...")
        
        if self.flask_process:
            try:
                self.flask_process.terminate()
                self.flask_process.wait(timeout=5)
                print("✅ Flask arrêté")
            except:
                try:
                    self.flask_process.kill()
                except:
                    pass
        
        if self.vite_process:
            try:
                self.vite_process.terminate()
                self.vite_process.wait(timeout=5)
                print("✅ Vite arrêté")
            except:
                try:
                    self.vite_process.kill()
                except:
                    pass
    
    def run(self):
        """Lance l'application"""
        print("🚀 Application RH - Launcher Simplifié")
        print("=" * 50)
        
        # Gestion des signaux pour arrêt propre
        def signal_handler(sig, frame):
            print("\n🛑 Arrêt demandé...")
            self.cleanup()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Démarrer Flask
            if not self.start_flask():
                print("❌ Impossible de démarrer Flask")
                return False
            
            # Démarrer Vite
            if not self.start_vite():
                print("⚠️  Vite n'a pas démarré, mais Flask fonctionne")
            
            print("\n🎉 Application démarrée!")
            print("\n🌐 URLs d'accès:")
            print("   Application: http://localhost:5173")
            print("   API Backend: http://localhost:5001")
            print("\n🔑 Identifiants de test:")
            print("   Admin: admin@exemple.com / admin123")
            print("   Responsable: jean.martin@exemple.com / resp123")
            print("   Agent: sofiane.bendaoud@exemple.com / agent123")
            print("\n📝 Pour arrêter: Ctrl+C")
            
            # Ouvrir le navigateur
            try:
                import webbrowser
                webbrowser.open('http://localhost:5173')
                print("🌐 Application ouverte dans le navigateur")
            except:
                print("⚠️  Ouvrez manuellement: http://localhost:5173")
            
            # Attendre
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
        finally:
            self.cleanup()
            print("\n👋 Application arrêtée")

if __name__ == "__main__":
    launcher = SimpleLauncher()
    launcher.run()

