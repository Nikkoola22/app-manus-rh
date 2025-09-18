#!/usr/bin/env python3
"""
Test des onglets HTML simples
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_onglets_html():
    """Test des onglets HTML simples"""
    print("🔧 Test des onglets HTML simples")
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
            
            # Vérifier si le contenu contient les onglets HTML
            content = response.text
            if 'Test des onglets (Version HTML)' in content:
                print("✅ Version de test HTML trouvée")
            else:
                print("❌ Version de test HTML non trouvée")
            
            if 'Demandes en attente' in content:
                print("✅ Onglets trouvés dans le HTML")
            else:
                print("❌ Onglets non trouvés")
                
        else:
            print(f"❌ Interface non accessible: {response.status_code}")
            return
        
        print("\n🔧 Version de test utilisée:")
        print("   ✅ Boutons HTML simples au lieu du composant Tabs")
        print("   ✅ Gestion d'état React simple")
        print("   ✅ Logs de débogage dans la console")
        print("   ✅ Interface de test claire")
        
        print("\n📱 Instructions de test:")
        print("   1. Ouvrir http://localhost:5001")
        print("   2. Se connecter (jean.martin@exemple.com / resp123)")
        print("   3. Vérifier que vous voyez 'Test des onglets (Version HTML)'")
        print("   4. Cliquer sur les boutons d'onglets")
        print("   5. Vérifier que le contenu change")
        print("   6. Ouvrir la console (F12) pour voir les logs")
        
        print("\n🔍 Si cette version fonctionne:")
        print("   - Le problème vient du composant Tabs React")
        print("   - Il faut corriger le composant Tabs ou utiliser une alternative")
        
        print("\n🔍 Si cette version ne fonctionne pas:")
        print("   - Le problème est plus profond (JavaScript, CSS, etc.)")
        print("   - Il faut vérifier les erreurs dans la console")
        
        print("\n⏳ Application en cours... (Ctrl+C pour arrêter)")
        
        # Attendre
        time.sleep(60)
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_onglets_html()


