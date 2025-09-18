#!/usr/bin/env python3
"""
Script de migration pour mettre à jour la base de données avec les nouvelles unités
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
from src.models.demande_conge import DemandeConge

def create_app():
    """Crée l'application Flask pour la migration"""
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

def migrate_database():
    """Migre la base de données vers les nouvelles unités"""
    print("🔄 Migration de la base de données")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Recréer toutes les tables avec les nouveaux champs
            print("📊 Recréation des tables...")
            db.drop_all()
            db.create_all()
            print("✅ Tables recréées")
            
            # Réinitialiser les données
            print("📊 Réinitialisation des données...")
            from init_portable_data import init_services, init_agents, init_sample_data
            
            init_services()
            init_agents()
            init_sample_data()
            
            print("✅ Données réinitialisées")
            
            # Vérifier les agents
            print("\n👥 Vérification des agents:")
            agents = Agent.query.all()
            for agent in agents:
                print(f"   {agent.prenom} {agent.nom}:")
                print(f"     CA: {agent.get_solde_display('CA')}")
                print(f"     RTT: {agent.get_solde_display('RTT')}")
                print(f"     HS: {agent.get_solde_display('HS')}")
            
            # Vérifier les demandes
            print("\n📋 Vérification des demandes:")
            demandes = DemandeConge.query.all()
            for demande in demandes:
                print(f"   {demande.type_absence}: {demande.get_duration_display()}")
            
            print("\n🎉 Migration terminée avec succès!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la migration: {e}")
            return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)


