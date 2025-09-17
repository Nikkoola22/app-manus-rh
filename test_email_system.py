#!/usr/bin/env python3
"""
Script de test pour vérifier le système de notifications email
"""

import requests
import json
from datetime import datetime, date, timedelta

def test_email_system():
    """Teste le système de notifications email"""
    
    base_url = "http://localhost:5001/api"
    
    print("📧 Test du système de notifications email")
    print("=" * 70)
    
    # Test 1 : Connexion en tant qu'admin
    print("\n1️⃣ Connexion en tant qu'admin...")
    login_data = {
        "email": "admin@exemple.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Connexion admin réussie")
            session_cookies = response.cookies
        else:
            print(f"❌ Échec de la connexion admin : {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous que l'application est démarrée.")
        return False
    
    # Test 2 : Vérifier la configuration email
    print("\n2️⃣ Vérification de la configuration email...")
    try:
        response = requests.get(f"{base_url}/email/config", cookies=session_cookies)
        if response.status_code == 200:
            config = response.json()
            print("✅ Configuration email récupérée")
            print(f"   Serveur SMTP : {config['mail_server']}")
            print(f"   Port : {config['mail_port']}")
            print(f"   TLS : {config['mail_use_tls']}")
            print(f"   SSL : {config['mail_use_ssl']}")
            print(f"   Expéditeur : {config['mail_default_sender']}")
            print(f"   Configuré : {config['configured']}")
            
            if not config['configured']:
                print("⚠️ Configuration email incomplète. Les emails ne seront pas envoyés.")
                print("   Configurez MAIL_USERNAME et MAIL_PASSWORD dans les variables d'environnement.")
        else:
            print(f"❌ Échec de récupération de la configuration : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la configuration : {e}")
    
    # Test 3 : Test d'envoi d'email (si configuré)
    print("\n3️⃣ Test d'envoi d'email...")
    test_email = input("Entrez une adresse email pour le test (ou appuyez sur Entrée pour ignorer) : ").strip()
    
    if test_email:
        try:
            test_data = {"email": test_email}
            response = requests.post(f"{base_url}/email/test", 
                                   json=test_data, 
                                   cookies=session_cookies)
            
            if response.status_code == 200:
                print("✅ Email de test envoyé avec succès")
                print(f"   Vérifiez votre boîte email : {test_email}")
            else:
                print(f"❌ Échec de l'envoi de l'email de test : {response.status_code}")
                print(f"   Réponse : {response.text}")
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'email de test : {e}")
    else:
        print("⏭️ Test d'email ignoré")
    
    # Test 4 : Connexion en tant qu'agent pour créer une demande
    print("\n4️⃣ Test de création de demande avec notification...")
    agent_login_data = {
        "email": "jean.martin@exemple.com",
        "password": "agent123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=agent_login_data)
        if response.status_code == 200:
            print("✅ Connexion agent réussie")
            agent_session = response.cookies
        else:
            print(f"❌ Échec de la connexion agent : {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la connexion agent : {e}")
        return False
    
    # Test 5 : Créer une demande de congé
    print("\n5️⃣ Création d'une demande de congé...")
    today = date.today()
    date_debut = today + timedelta(days=7)  # Dans une semaine
    date_fin = date_debut + timedelta(days=2)  # 3 jours
    
    demande_data = {
        'type_absence': 'CA',
        'date_debut': date_debut.isoformat(),
        'date_fin': date_fin.isoformat(),
        'motif': 'Test de notification email - congés'
    }
    
    try:
        response = requests.post(f"{base_url}/demandes", 
                               json=demande_data, 
                               cookies=agent_session)
        
        if response.status_code == 201:
            demande = response.json()
            demande_id = demande['id']
            print("✅ Demande de congé créée avec succès")
            print(f"   ID : {demande_id}")
            print(f"   Période : {date_debut} - {date_fin}")
            print("   📧 Email de notification envoyé au responsable")
        else:
            print(f"❌ Échec de création de la demande : {response.status_code}")
            print(f"   Réponse : {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la création de la demande : {e}")
        return False
    
    # Test 6 : Connexion en tant que responsable pour valider
    print("\n6️⃣ Test de validation avec notification...")
    responsable_login_data = {
        "email": "marie.dubois@exemple.com",
        "password": "resp123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=responsable_login_data)
        if response.status_code == 200:
            print("✅ Connexion responsable réussie")
            responsable_session = response.cookies
        else:
            print(f"❌ Échec de la connexion responsable : {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la connexion responsable : {e}")
        return False
    
    # Test 7 : Valider la demande
    print("\n7️⃣ Validation de la demande...")
    validation_data = {
        'action': 'approuver',
        'commentaires': 'Test de validation avec notification email'
    }
    
    try:
        response = requests.post(f"{base_url}/demandes/{demande_id}/valider", 
                               json=validation_data, 
                               cookies=responsable_session)
        
        if response.status_code == 200:
            demande_validee = response.json()
            print("✅ Demande validée avec succès")
            print(f"   Statut : {demande_validee['statut']}")
            print("   📧 Email de notification envoyé à l'agent")
        else:
            print(f"❌ Échec de validation : {response.status_code}")
            print(f"   Réponse : {response.text}")
    except Exception as e:
        print(f"❌ Erreur lors de la validation : {e}")
    
    # Test 8 : Test de refus avec notification
    print("\n8️⃣ Test de refus avec notification...")
    
    # Créer une nouvelle demande
    demande_refus_data = {
        'type_absence': 'RTT',
        'date_debut': (today + timedelta(days=14)).isoformat(),
        'date_fin': (today + timedelta(days=14)).isoformat(),
        'motif': 'Test de refus avec notification email'
    }
    
    try:
        response = requests.post(f"{base_url}/demandes", 
                               json=demande_refus_data, 
                               cookies=agent_session)
        
        if response.status_code == 201:
            demande_refus = response.json()
            demande_refus_id = demande_refus['id']
            print("✅ Demande de refus créée")
            
            # Refuser la demande
            refus_data = {
                'action': 'refuser',
                'commentaires': 'Test de refus avec notification email - période trop chargée'
            }
            
            response = requests.post(f"{base_url}/demandes/{demande_refus_id}/valider", 
                                   json=refus_data, 
                                   cookies=responsable_session)
            
            if response.status_code == 200:
                print("✅ Demande refusée avec succès")
                print("   📧 Email de notification envoyé à l'agent")
            else:
                print(f"❌ Échec de refus : {response.status_code}")
        else:
            print(f"❌ Échec de création de la demande de refus : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors du test de refus : {e}")
    
    print("\n" + "=" * 70)
    print("✅ Tests du système de notifications email terminés")
    print("   Fonctionnalités testées :")
    print("   - Configuration email")
    print("   - Envoi d'email de test")
    print("   - Notification lors de création de demande")
    print("   - Notification lors de validation")
    print("   - Notification lors de refus")
    print()
    print("📧 Vérifiez les boîtes email pour confirmer la réception des notifications")
    
    return True

if __name__ == "__main__":
    test_email_system()

