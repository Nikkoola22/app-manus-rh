#!/usr/bin/env python3
"""
Launcher simplifié pour diagnostiquer les problèmes
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    print("🚀 Launcher simplifié - Diagnostic")
    print("=" * 40)
    
    app_dir = Path(__file__).parent.absolute()
    print(f"📁 Répertoire: {app_dir}")
    
    # Vérifier Python
    python_cmd = str(app_dir / "venv" / "bin" / "python")
    print(f"🐍 Python: {python_cmd}")
    
    if not os.path.exists(python_cmd):
        print("❌ Python de l'environnement virtuel non trouvé")
        return False
    
    # Vérifier main.py
    main_py = app_dir / "main.py"
    print(f"📄 main.py: {main_py}")
    
    if not main_py.exists():
        print("❌ main.py non trouvé")
        return False
    
    # Lancer Flask
    print("\n🐍 Lancement de Flask...")
    try:
        process = subprocess.Popen(
            [python_cmd, "main.py"],
            cwd=app_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("⏳ Attente du démarrage...")
        time.sleep(3)
        
        # Vérifier si le processus tourne toujours
        if process.poll() is None:
            print("✅ Flask démarré avec succès")
            print("🌐 Application disponible sur http://localhost:5001")
            print("📝 Appuyez sur Ctrl+C pour arrêter")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Arrêt demandé")
                process.terminate()
                process.wait()
        else:
            print("❌ Flask s'est arrêté")
            stdout, stderr = process.communicate()
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
