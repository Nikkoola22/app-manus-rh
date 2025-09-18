#!/usr/bin/env python3
"""
Test simple des onglets cliquables
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_onglets_simple():
    """Test simple des onglets cliquables"""
    print("🔍 Test des onglets cliquables")
    print("=" * 40)
    
    app_dir = Path(__file__).parent.absolute()
    python_cmd = str(app_dir / "venv" / "bin" / "python")
    
    # Démarrer Flask
    print("🐍 Démarrage de Flask...")
    flask_process = subprocess.Popen(
        [python_cmd, "main.py"],
        cwd=app_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Attendre que Flask démarre
    time.sleep(3)
    
    try:
        # Test de connexion
        print("\n👤 Test de connexion...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'jean.martin@exemple.com', 'password': 'resp123'},
                               timeout=5)
        
        if response.status_code == 200:
            print("✅ Connexion réussie")
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test de l'interface
        print("\n🌐 Test de l'interface...")
        response = requests.get('http://localhost:5001', timeout=5)
        
        if response.status_code == 200:
            print("✅ Interface accessible")
            
            # Vérifier si le contenu contient les onglets
            content = response.text
            if 'Demandes en attente' in content:
                print("✅ Onglet 'Demandes en attente' trouvé dans le HTML")
            else:
                print("❌ Onglet 'Demandes en attente' non trouvé")
            
            if 'TabsList' in content or 'TabsTrigger' in content:
                print("✅ Composants Tabs trouvés dans le HTML")
            else:
                print("❌ Composants Tabs non trouvés")
                
        else:
            print(f"❌ Interface non accessible: {response.status_code}")
            return
        
        print("\n🔍 Problèmes possibles:")
        print("   1. Erreurs JavaScript dans la console")
        print("   2. Composants Tabs non chargés")
        print("   3. CSS qui bloque les clics")
        print("   4. Événements non attachés")
        print("   5. Problème avec les composants UI")
        
        print("\n📱 Instructions de diagnostic:")
        print("   1. Ouvrir http://localhost:5001")
        print("   2. Se connecter (jean.martin@exemple.com / resp123)")
        print("   3. Ouvrir la console (F12)")
        print("   4. Vérifier les erreurs JavaScript")
        print("   5. Inspecter les onglets (clic droit → Inspecter)")
        print("   6. Vérifier si les événements sont attachés")
        
        print("\n⏳ Application en cours... (Ctrl+C pour arrêter)")
        
        # Attendre
        time.sleep(30)
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_onglets_simple()


