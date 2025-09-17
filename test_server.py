#!/usr/bin/env python3
import requests
import time
import subprocess
import sys
import os

def test_connection():
    """Test de connexion aux serveurs"""
    print("🔍 Test de connexion aux serveurs...")
    
    # Test du serveur Flask (port 5001)
    try:
        response = requests.get('http://localhost:5001/api/auth/check-session', timeout=5)
        if response.status_code == 200:
            print("✅ Serveur Flask (port 5001) : OK")
        else:
            print(f"⚠️  Serveur Flask (port 5001) : Status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Serveur Flask (port 5001) : NON DÉMARRÉ")
        return False
    except Exception as e:
        print(f"❌ Serveur Flask (port 5001) : Erreur - {e}")
        return False
    
    # Test du serveur Vite (port 5173)
    try:
        response = requests.get('http://localhost:5173/', timeout=5)
        if response.status_code == 200:
            print("✅ Serveur Vite (port 5173) : OK")
        else:
            print(f"⚠️  Serveur Vite (port 5173) : Status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Serveur Vite (port 5173) : NON DÉMARRÉ")
        return False
    except Exception as e:
        print(f"❌ Serveur Vite (port 5173) : Erreur - {e}")
        return False
    
    return True

def start_flask_server():
    """Démarre le serveur Flask"""
    print("🚀 Démarrage du serveur Flask...")
    try:
        # Changer vers le répertoire du projet
        os.chdir('/Users/nikkoolagarnier/Downloads/app manus rh')
        
        # Activer l'environnement virtuel et démarrer Flask
        cmd = ['bash', '-c', 'source venv/bin/activate && python main.py']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre un peu pour que le serveur démarre
        time.sleep(5)
        
        # Vérifier si le processus est toujours en cours
        if process.poll() is None:
            print("✅ Serveur Flask démarré")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Erreur lors du démarrage de Flask: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de Flask: {e}")
        return None

def test_login():
    """Test de connexion utilisateur"""
    print("\n🔐 Test de connexion utilisateur...")
    
    try:
        response = requests.post('http://localhost:5001/api/auth/login', 
                               json={'email': 'admin@exemple.com', 'password': 'admin123'},
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connexion réussie: {data['prenom']} {data['nom']} ({data['role']})")
            print(f"   Quotité de travail: {data['quotite_travail']}h/semaine")
            print(f"   Date d'arrivée: {data['date_debut_contrat']}")
            return True
        else:
            print(f"❌ Erreur de connexion: Status {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Détails: {error_data}")
            except:
                print(f"   Détails: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de connexion: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Diagnostic de l'application RH")
    print("=" * 50)
    
    # Test initial
    if test_connection():
        print("\n🎉 Tous les serveurs sont opérationnels!")
        test_login()
    else:
        print("\n🔧 Tentative de démarrage du serveur Flask...")
        flask_process = start_flask_server()
        
        if flask_process:
            print("\n🔄 Nouveau test de connexion...")
            if test_connection():
                print("\n🎉 Serveurs opérationnels après démarrage!")
                test_login()
            else:
                print("\n❌ Problème persistant de connexion")
        else:
            print("\n❌ Impossible de démarrer le serveur Flask")
    
    print("\n" + "=" * 50)
    print("📝 Pour démarrer manuellement:")
    print("   Terminal 1: cd '/Users/nikkoolagarnier/Downloads/app manus rh' && source venv/bin/activate && python main.py")
    print("   Terminal 2: cd '/Users/nikkoolagarnier/Downloads/app manus rh' && npm run dev")
    print("\n🌐 URLs d'accès:")
    print("   Application: http://localhost:5173")
    print("   API Backend: http://localhost:5001")




