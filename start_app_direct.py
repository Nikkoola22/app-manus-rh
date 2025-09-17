#!/usr/bin/env python3
"""
Script de démarrage direct pour l'application RH
Évite les problèmes de terminal en démarrant directement les serveurs
"""

import subprocess
import time
import os
import sys
import signal
import webbrowser
from threading import Thread

def start_flask():
    """Démarre Flask en arrière-plan"""
    print("🐍 Démarrage de Flask...")
    os.chdir('/Users/nikkoolagarnier/Downloads/app manus rh')
    cmd = ['bash', '-c', 'source venv/bin/activate && python main.py']
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_vite():
    """Démarre Vite en arrière-plan"""
    print("⚡ Démarrage de Vite...")
    os.chdir('/Users/nikkoolagarnier/Downloads/app manus rh')
    cmd = ['npm', 'run', 'dev']
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    print("🚀 Démarrage de l'Application RH")
    print("=" * 40)
    
    # Démarrer Flask
    flask_process = start_flask()
    time.sleep(3)
    
    # Démarrer Vite
    vite_process = start_vite()
    time.sleep(5)
    
    print("\n✅ Serveurs démarrés!")
    print("\n🌐 URLs d'accès:")
    print("   Application: http://localhost:5173")
    print("   API Backend: http://localhost:5001")
    print("\n🔑 Identifiants de test:")
    print("   Admin: admin@exemple.com / admin123")
    print("   Responsable: jean.martin@exemple.com / resp123")
    print("   Agent: sofiane.bendaoud@exemple.com / agent123")
    
    # Ouvrir l'application
    try:
        webbrowser.open('http://localhost:5173')
        print("\n🌐 Application ouverte dans le navigateur")
    except:
        print("\n⚠️  Ouvrez manuellement: http://localhost:5173")
    
    print("\n📝 Pour arrêter: Fermez cette fenêtre ou Ctrl+C")
    
    try:
        # Attendre indéfiniment
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt des serveurs...")
        flask_process.terminate()
        vite_process.terminate()
        print("✅ Serveurs arrêtés")

if __name__ == "__main__":
    main()




