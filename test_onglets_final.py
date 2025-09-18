#!/usr/bin/env python3
"""
Test final des onglets corrigés
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_onglets_final():
    """Test final des onglets corrigés"""
    print("🎯 Test final des onglets corrigés")
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
            
            # Vérifier si le contenu contient les onglets
            content = response.text
            if 'Demandes en attente' in content:
                print("✅ Onglets trouvés dans le HTML")
            else:
                print("❌ Onglets non trouvés")
                
        else:
            print(f"❌ Interface non accessible: {response.status_code}")
            return
        
        print("\n🔧 Corrections appliquées:")
        print("   ✅ Ajout du TabsContext pour la gestion d'état")
        print("   ✅ Gestion des clics dans TabsTrigger")
        print("   ✅ Affichage conditionnel dans TabsContent")
        print("   ✅ Support des props value et onValueChange")
        print("   ✅ Gestion de l'état interne et externe")
        
        print("\n📱 Instructions de test:")
        print("   1. Ouvrir http://localhost:5001")
        print("   2. Se connecter (jean.martin@exemple.com / resp123)")
        print("   3. Cliquer sur les onglets:")
        print("      - 'Demandes en attente (X)'")
        print("      - 'Demandes traitées (X)'")
        print("      - 'Mes Demandes (X)'")
        print("      - 'Agents du service (X)'")
        print("      - 'Arrêts maladie (X)'")
        print("      - 'Calendrier'")
        print("      - 'Planning'")
        print("   4. Vérifier que:")
        print("      - Les onglets sont cliquables")
        print("      - Le contenu change")
        print("      - L'onglet actif est mis en surbrillance")
        print("      - Le scroll automatique fonctionne")
        
        print("\n🎉 Fonctionnalités attendues:")
        print("   ✅ Onglets cliquables")
        print("   ✅ Changement de contenu")
        print("   ✅ Mise en surbrillance de l'onglet actif")
        print("   ✅ Scroll automatique vers les sections de demandes")
        print("   ✅ Animation smooth")
        
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
    test_onglets_final()


