#!/usr/bin/env python3
"""
Script de test pour vérifier les données de l'admin
"""

import requests
import json

def test_admin_data():
    base_url = "http://localhost:5001"
    
    print("🔍 Test des données Admin")
    print("=" * 50)
    
    # Test 1: Connexion admin
    print("\n1️⃣ Test de connexion admin...")
    login_data = {
        "email": "admin@exemple.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Connexion admin réussie")
            session_cookies = response.cookies
        else:
            print(f"   ❌ Échec de connexion: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
        return
    
    # Test 2: Récupération des agents
    print("\n2️⃣ Test de récupération des agents...")
    try:
        response = requests.get(f"{base_url}/api/agents", cookies=session_cookies)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            agents = response.json()
            print(f"   ✅ Agents récupérés: {len(agents)} agents")
            print(f"   📋 Premier agent: {agents[0] if agents else 'Aucun'}")
        else:
            print(f"   ❌ Erreur agents: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur agents: {e}")
    
    # Test 3: Récupération des services
    print("\n3️⃣ Test de récupération des services...")
    try:
        response = requests.get(f"{base_url}/api/services", cookies=session_cookies)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            services = response.json()
            print(f"   ✅ Services récupérés: {len(services)} services")
            print(f"   📋 Premier service: {services[0] if services else 'Aucun'}")
        else:
            print(f"   ❌ Erreur services: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur services: {e}")
    
    # Test 4: Récupération des demandes
    print("\n4️⃣ Test de récupération des demandes...")
    try:
        response = requests.get(f"{base_url}/api/demandes", cookies=session_cookies)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            demandes = response.json()
            print(f"   ✅ Demandes récupérées: {len(demandes)} demandes")
        else:
            print(f"   ❌ Erreur demandes: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur demandes: {e}")
    
    # Test 5: Récupération des arrêts maladie
    print("\n5️⃣ Test de récupération des arrêts maladie...")
    try:
        response = requests.get(f"{base_url}/api/arret-maladie", cookies=session_cookies)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            arrets = response.json()
            print(f"   ✅ Arrêts récupérés: {len(arrets)} arrêts")
        else:
            print(f"   ❌ Erreur arrêts: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur arrêts: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Test terminé")

if __name__ == "__main__":
    test_admin_data()

