#!/usr/bin/env python3
"""
Script d'initialisation des données pour la version portable
Crée les données de base nécessaires au fonctionnement de l'application
"""

import os
import sys
from pathlib import Path

# Configuration portable
APP_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(APP_DIR))

from flask import Flask
from src.models.user import db
from src.models.agent import Agent
from src.models.service import Service
from src.models.demande_conge import DemandeConge
from src.models.historique_conge import HistoriqueConge
from src.models.arret_maladie import ArretMaladie
from src.models.presence import Presence

def create_app():
    """Crée l'application Flask pour l'initialisation"""
    app = Flask(__name__)
    
    # Configuration portable de la base de données
    DATABASE_FOLDER = APP_DIR / 'database'
    DATABASE_FOLDER.mkdir(exist_ok=True)
    DATABASE_PATH = DATABASE_FOLDER / 'app.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'conges-rtt-secret-key-2024'
    
    db.init_app(app)
    return app

def init_services():
    """Initialise les services de base"""
    print("🏢 Initialisation des services...")
    
    services = [
        {
            'nom_service': 'Direction Générale',
            'responsable_id': 1  # Admin sera créé en premier
        },
        {
            'nom_service': 'Ressources Humaines',
            'responsable_id': 1
        },
        {
            'nom_service': 'Informatique',
            'responsable_id': 1
        },
        {
            'nom_service': 'Comptabilité',
            'responsable_id': 1
        },
        {
            'nom_service': 'Commercial',
            'responsable_id': 1
        }
    ]
    
    for service_data in services:
        existing = Service.query.filter_by(nom_service=service_data['nom_service']).first()
        if not existing:
            service = Service(**service_data)
            db.session.add(service)
    
    db.session.commit()
    print("✅ Services initialisés")

def init_agents():
    """Initialise les agents de base"""
    print("👥 Initialisation des agents...")
    
    agents = [
        {
            'nom': 'Admin',
            'prenom': 'Administrateur',
            'email': 'admin@exemple.com',
            'role': 'Admin',
            'service_id': 1,
            'solde_ca': 25,  # 25 jours de CA
            'solde_hs': 0,   # 0 heures supplémentaires
            'quotite_travail': 38.0  # RTT calculé automatiquement
        },
        {
            'nom': 'Martin',
            'prenom': 'Jean',
            'email': 'jean.martin@exemple.com',
            'role': 'Responsable',
            'service_id': 2,
            'solde_ca': 25,  # 25 jours de CA
            'solde_hs': 0,   # 0 heures supplémentaires
            'quotite_travail': 38.0  # RTT calculé automatiquement
        },
        {
            'nom': 'Bendaoud',
            'prenom': 'Sofiane',
            'email': 'sofiane.bendaoud@exemple.com',
            'role': 'Agent',
            'service_id': 3,
            'solde_ca': 25,  # 25 jours de CA
            'solde_hs': 0,   # 0 heures supplémentaires
            'quotite_travail': 38.0  # RTT calculé automatiquement
        },
        {
            'nom': 'Dupont',
            'prenom': 'Marie',
            'email': 'marie.dupont@exemple.com',
            'role': 'Agent',
            'service_id': 2,
            'solde_ca': 25,  # 25 jours de CA
            'solde_hs': 0,   # 0 heures supplémentaires
            'quotite_travail': 38.0  # RTT calculé automatiquement
        },
        {
            'nom': 'Leroy',
            'prenom': 'Pierre',
            'email': 'pierre.leroy@exemple.com',
            'role': 'Agent',
            'service_id': 4,
            'solde_ca': 25,  # 25 jours de CA
            'solde_hs': 0,   # 0 heures supplémentaires
            'quotite_travail': 38.0  # RTT calculé automatiquement
        }
    ]
    
    for agent_data in agents:
        existing = Agent.query.filter_by(email=agent_data['email']).first()
        if not existing:
            agent = Agent(**agent_data)
            # Définir les mots de passe
            if agent_data['email'] == 'admin@exemple.com':
                agent.set_password('admin123')
            elif agent_data['email'] == 'jean.martin@exemple.com':
                agent.set_password('resp123')
            else:
                agent.set_password('agent123')
            db.session.add(agent)
    
    db.session.commit()
    print("✅ Agents initialisés")

def init_sample_data():
    """Initialise des données d'exemple"""
    print("📊 Initialisation des données d'exemple...")
    
    # Créer quelques demandes de congés d'exemple
    from datetime import datetime, timedelta
    
    sample_demandes = [
        {
            'agent_id': 3,  # Sofiane
            'date_debut': datetime.now() + timedelta(days=7),
            'date_fin': datetime.now() + timedelta(days=9),
            'type_absence': 'CA',
            'statut': 'En attente',
            'motif': 'Vacances d\'été',
            'demi_journees': 'journée complète'
        },
        {
            'agent_id': 4,  # Marie
            'date_debut': datetime.now() + timedelta(days=14),
            'date_fin': datetime.now() + timedelta(days=14),
            'type_absence': 'RTT',
            'statut': 'Approuvée',
            'motif': 'RTT',
            'demi_journees': 'matin'
        }
    ]
    
    for demande_data in sample_demandes:
        existing = DemandeConge.query.filter_by(
            agent_id=demande_data['agent_id'],
            date_debut=demande_data['date_debut']
        ).first()
        if not existing:
            demande = DemandeConge(**demande_data)
            # Calculer automatiquement la durée
            demande.calculate_duration()
            db.session.add(demande)
    
    db.session.commit()
    print("✅ Données d'exemple initialisées")

def main():
    """Fonction principale d'initialisation"""
    print("🚀 Initialisation des données pour l'application portable")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Créer toutes les tables
            print("🗄️ Création des tables de base de données...")
            db.create_all()
            print("✅ Tables créées")
            
            # Initialiser les données
            init_services()
            init_agents()
            init_sample_data()
            
            print("\n🎉 Initialisation terminée avec succès!")
            print("\n🔑 Comptes créés:")
            print("   Admin: admin@exemple.com / admin123")
            print("   Responsable: jean.martin@exemple.com / resp123")
            print("   Agent: sofiane.bendaoud@exemple.com / agent123")
            print("   Agent: marie.dupont@exemple.com / agent123")
            print("   Agent: pierre.leroy@exemple.com / agent123")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {e}")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
