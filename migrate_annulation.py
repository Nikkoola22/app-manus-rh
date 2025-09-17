#!/usr/bin/env python3
"""
Migration pour ajouter le champ date_annulation aux demandes
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
app_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(app_dir))

from src.models.user import db
from src.models.demande_conge import DemandeConge
from main import app

def migrate_annulation():
    """Ajoute le champ date_annulation à la table demande_conge"""
    print("🔄 Migration pour ajouter le champ date_annulation...")
    
    with app.app_context():
        try:
            # Vérifier si la colonne existe déjà
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('demande_conge')]
            
            if 'date_annulation' in columns:
                print("✅ Le champ date_annulation existe déjà")
                return
            
            # Ajouter la colonne
            print("➕ Ajout de la colonne date_annulation...")
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE demande_conge ADD COLUMN date_annulation DATETIME'))
                conn.commit()
            
            print("✅ Migration terminée avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de la migration: {e}")
            return False
    
    return True

if __name__ == "__main__":
    migrate_annulation()
