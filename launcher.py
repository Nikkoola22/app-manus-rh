#!/usr/bin/env python3
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
                print(f"   Attente du démarrage de Flask... ({i+1}/10)")
            
            print("❌ Timeout lors du démarrage de Flask")
            return False
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage de Flask: {e}")
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
                print(f"   Attente du démarrage de Vite... ({i+1}/15)")
            
            print("❌ Timeout lors du démarrage de Vite")
            return False
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage de Vite: {e}")
            return False
    
    def cleanup(self):
        """Nettoie les processus"""
        print("\n🧹 Arrêt des serveurs...")
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
            
            print("\n🎉 Application démarrée avec succès!")
            print("\n🌐 URLs d'accès:")
            print("   Application: http://localhost:5173")
            print("   API Backend: http://localhost:5001")
            print("\n🔑 Identifiants de test:")
            print("   Admin: admin@exemple.com / admin123")
            print("   Responsable: jean.martin@exemple.com / resp123")
            print("   Agent: sofiane.bendaoud@exemple.com / agent123")
            print("\n📝 Pour arrêter l'application: Ctrl+C")
            
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
            print("\n\n🛑 Arrêt demandé par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}")
        finally:
            self.cleanup()
            print("\n👋 Application arrêtée")

if __name__ == "__main__":
    launcher = AppLauncher()
    launcher.run()
