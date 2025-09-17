#!/usr/bin/env python3
"""
Script de démarrage final pour l'application RH portable
Utilise le bon Python de l'environnement virtuel
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def get_python_command():
    """Retourne la commande Python de l'environnement virtuel"""
    app_dir = Path(__file__).parent.absolute()
    if os.name == 'nt':  # Windows
        return str(app_dir / "venv" / "Scripts" / "python.exe")
    else:  # Unix/Linux/macOS
        return str(app_dir / "venv" / "bin" / "python")

def main():
    print("🚀 Application RH - Démarrage")
    print("=" * 40)
    
    app_dir = Path(__file__).parent.absolute()
    python_cmd = get_python_command()
    
    print(f"📁 Répertoire: {app_dir}")
    print(f"🐍 Python: {python_cmd}")
    
    if not os.path.exists(python_cmd):
        print("❌ Environnement virtuel non trouvé")
        print("   Exécutez d'abord: python3 setup_portable.py")
        return False
    
    # Lancer Flask
    print("\n🐍 Démarrage de Flask...")
    try:
        flask_process = subprocess.Popen(
            [python_cmd, "main.py"],
            cwd=app_dir
        )
        
        # Attendre que Flask démarre
        time.sleep(3)
        
        if flask_process.poll() is None:
            print("✅ Flask démarré avec succès")
            print("🌐 API disponible sur: http://localhost:5001")
        else:
            print("❌ Flask n'a pas démarré")
            return False
        
        # Lancer Vite
        print("\n⚡ Démarrage de Vite...")
        try:
            vite_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=app_dir
            )
            
            time.sleep(3)
            
            if vite_process.poll() is None:
                print("✅ Vite démarré avec succès")
                print("🌐 Application disponible sur: http://localhost:5173")
            else:
                print("⚠️  Vite n'a pas démarré, mais Flask fonctionne")
        except Exception as e:
            print(f"⚠️  Erreur Vite: {e}")
        
        print("\n🎉 Application démarrée!")
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
        
        # Gestion des signaux
        def signal_handler(sig, frame):
            print("\n🛑 Arrêt demandé...")
            flask_process.terminate()
            if 'vite_process' in locals():
                vite_process.terminate()
            print("👋 Application arrêtée")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Attendre
        try:
            flask_process.wait()
        except KeyboardInterrupt:
            signal_handler(None, None)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)