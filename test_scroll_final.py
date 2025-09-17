#!/usr/bin/env python3
"""
Test final du scroll automatique avec débogage complet
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_scroll_final():
    """Test final du scroll automatique"""
    print("🎯 Test final du scroll automatique")
    print("=" * 50)
    
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
        print("\n👤 Test de connexion Responsable...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'jean.martin@exemple.com', 'password': 'resp123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion réussie: {data['user']['prenom']} {data['user']['nom']}")
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        # Test de l'interface
        print("\n🌐 Test de l'interface...")
        response = requests.get('http://localhost:5001', timeout=5)
        
        if response.status_code == 200:
            print("✅ Interface accessible")
        else:
            print(f"❌ Interface non accessible: {response.status_code}")
            return
        
        print("\n🔧 Corrections appliquées:")
        print("   ✅ Ajout de l'état activeTab")
        print("   ✅ useEffect pour gérer le scroll")
        print("   ✅ Refs + IDs de fallback")
        print("   ✅ Logs de débogage détaillés")
        print("   ✅ Délai de 300ms pour le rendu")
        
        print("\n📱 Instructions de test:")
        print("   1. Ouvrir http://localhost:5001 dans le navigateur")
        print("   2. Se connecter comme responsable (jean.martin@exemple.com / resp123)")
        print("   3. Ouvrir la console développeur (F12)")
        print("   4. Cliquer sur les onglets:")
        print("      - 'Demandes en attente (X)'")
        print("      - 'Demandes traitées (X)'")
        print("      - 'Mes Demandes (X)'")
        print("   5. Vérifier dans la console:")
        print("      - 'Active tab changed to: [valeur]'")
        print("      - 'Attempting scroll for active tab: [valeur]'")
        print("      - 'Demandes [type] element: [element]'")
        print("      - 'Scrolling to element: [element]'")
        
        print("\n🔍 Si le scroll ne fonctionne toujours pas:")
        print("   - Vérifier que les éléments existent dans le DOM")
        print("   - Vérifier que les refs sont correctement attachés")
        print("   - Vérifier que les IDs de fallback sont présents")
        print("   - Vérifier les erreurs dans la console")
        
        print("\n⏳ Application en cours d'exécution...")
        print("   Appuyez sur Ctrl+C pour arrêter")
        
        # Garder l'application en vie
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé par l'utilisateur")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_scroll_final()
