#!/usr/bin/env python3
"""
Script de migration pour ajouter les tables de planning
"""

import os
import sys
from pathlib import Path

# Configuration portable
APP_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(APP_DIR))

from flask import Flask
from src.models.user import db
from src.models.planning import PlanningAgent, PlanningTemplate

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

def migrate_planning():
    """Ajoute les tables de planning à la base de données"""
    print("🗓️ Migration des tables de planning")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Créer les tables de planning
            db.create_all()
            print("✅ Tables de planning créées avec succès")
            
            # Vérifier que les tables existent
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'planning_agent' in tables:
                print("✅ Table 'planning_agent' créée")
            else:
                print("❌ Table 'planning_agent' manquante")
            
            if 'planning_template' in tables:
                print("✅ Table 'planning_template' créée")
            else:
                print("❌ Table 'planning_template' manquante")
            
            print("\n📊 Migration terminée avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la migration: {e}")
            return False

if __name__ == "__main__":
    success = migrate_planning()
    sys.exit(0 if success else 1)
