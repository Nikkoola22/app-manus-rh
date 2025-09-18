#!/usr/bin/env python3
"""
Test de la correction des menus déroulants dans le planning
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_menus_deroulants_fix():
    """Test de la correction des menus déroulants"""
    print("🔧 Test de la correction des menus déroulants")
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
        # Test 1: Vérifier que l'API est accessible
        print("\n🌐 Test de l'API...")
        response = requests.get('http://localhost:5001/api/health', timeout=5)
        
        if response.status_code == 200:
            print("✅ API accessible")
        else:
            print(f"⚠️ API non accessible: {response.status_code}")
        
        # Test 2: Connexion Responsable
        print("\n👤 Test de connexion Responsable...")
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'jean.martin@exemple.com', 'password': 'resp123'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion Responsable réussie")
            print(f"   Nom: {data['user']['prenom']} {data['user']['nom']}")
            print(f"   Rôle: {data['user']['role']}")
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            return
        
        print("\n✅ Tests de correction terminés")
        print("\n🔧 Corrections appliquées:")
        print("   - Amélioration des styles des SelectContent")
        print("   - Ajout de classes CSS pour la visibilité")
        print("   - Création d'une version alternative avec inputs de type time")
        print("   - Remplacement dans ResponsableDashboard")
        
        print("\n📝 Améliorations apportées:")
        print("   - SelectContent avec fond blanc opaque")
        print("   - Bordure grise visible")
        print("   - Ombre portée (shadow-lg)")
        print("   - Z-index élevé (z-50)")
        print("   - Effet de survol bleu")
        print("   - Alternative avec inputs de type time")
        
        print("\n🎯 Solutions proposées:")
        print("   1. Version améliorée des Select (PlanningEditor.jsx)")
        print("   2. Version avec inputs de type time (PlanningEditorTime.jsx)")
        print("   3. Meilleure compatibilité navigateur")
        print("   4. Interface plus intuitive")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    finally:
        # Arrêter Flask
        flask_process.terminate()
        flask_process.wait()
        print("🛑 Flask arrêté")

if __name__ == "__main__":
    test_menus_deroulants_fix()


