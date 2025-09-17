#!/usr/bin/env python3
"""
Script pour corriger les rôles dans la base de données
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

def create_app():
    """Crée l'application Flask"""
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

def fix_roles():
    """Corrige les rôles dans la base de données"""
    print("🔧 Correction des rôles dans la base de données")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Récupérer tous les agents
            agents = Agent.query.all()
            
            print(f"📊 {len(agents)} agents trouvés")
            
            # Corriger les rôles
            corrections = {
                'admin': 'Admin',
                'responsable': 'Responsable', 
                'agent': 'Agent'
            }
            
            corrected = 0
            for agent in agents:
                if agent.role in corrections:
                    old_role = agent.role
                    agent.role = corrections[old_role]
                    corrected += 1
                    print(f"   {agent.prenom} {agent.nom}: {old_role} → {agent.role}")
            
            if corrected > 0:
                db.session.commit()
                print(f"\n✅ {corrected} rôles corrigés")
            else:
                print("\n✅ Aucune correction nécessaire")
            
            # Vérifier les rôles finaux
            print("\n📋 Rôles finaux:")
            for agent in agents:
                print(f"   {agent.prenom} {agent.nom}: {agent.role}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False

if __name__ == "__main__":
    success = fix_roles()
    sys.exit(0 if success else 1)
