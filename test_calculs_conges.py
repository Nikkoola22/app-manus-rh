#!/usr/bin/env python3
"""
Test des calculs de congés avec les nouvelles unités
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Configuration portable
APP_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(APP_DIR))

from flask import Flask
from src.models.user import db
from src.models.agent import Agent
from src.models.demande_conge import DemandeConge

def create_app():
    """Crée l'application Flask pour les tests"""
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

def test_calculs():
    """Test des calculs de congés"""
    print("🧪 Test des calculs de congés")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        # Créer un agent de test
        agent = Agent(
            nom='Test',
            prenom='Agent',
            email='test@exemple.com',
            role='agent',
            service_id=1,
            solde_ca=25,  # 25 jours
            solde_hs=0,   # 0 heures
            quotite_travail=38.0  # RTT calculé automatiquement
        )
        agent.set_password('test123')
        
        # Vérifier les soldes
        print("📊 Soldes de l'agent:")
        print(f"   CA: {agent.get_solde_display('CA')}")
        print(f"   RTT: {agent.get_solde_display('RTT')}")
        print(f"   HS: {agent.get_solde_display('HS')}")
        
        # Test 1: Congés annuels (CA) - calcul en jours
        print("\n📅 Test 1: Congés annuels (CA)")
        demande_ca = DemandeConge(
            agent_id=1,
            type_absence='CA',
            date_debut=datetime.now() + timedelta(days=1),
            date_fin=datetime.now() + timedelta(days=3),
            demi_journees='journée complète',
            motif='Vacances'
        )
        demande_ca.calculate_duration()
        print(f"   Période: {demande_ca.date_debut} à {demande_ca.date_fin}")
        print(f"   Durée: {demande_ca.get_duration_display()}")
        print(f"   Jours: {demande_ca.nb_jours}")
        print(f"   Heures: {demande_ca.nb_heures}")
        
        # Test 2: CA demi-journée
        print("\n📅 Test 2: CA demi-journée")
        demande_ca_demi = DemandeConge(
            agent_id=1,
            type_absence='CA',
            date_debut=datetime.now() + timedelta(days=5),
            date_fin=datetime.now() + timedelta(days=5),
            demi_journees='matin',
            motif='Rendez-vous médical'
        )
        demande_ca_demi.calculate_duration()
        print(f"   Période: {demande_ca_demi.date_debut} (matin)")
        print(f"   Durée: {demande_ca_demi.get_duration_display()}")
        print(f"   Jours: {demande_ca_demi.nb_jours}")
        print(f"   Heures: {demande_ca_demi.nb_heures}")
        
        # Test 3: RTT - calcul en heures
        print("\n⏰ Test 3: RTT")
        demande_rtt = DemandeConge(
            agent_id=1,
            type_absence='RTT',
            date_debut=datetime.now() + timedelta(days=7),
            date_fin=datetime.now() + timedelta(days=7),
            demi_journees='journée complète',
            motif='RTT'
        )
        demande_rtt.calculate_duration()
        print(f"   Période: {demande_rtt.date_debut} (journée complète)")
        print(f"   Durée: {demande_rtt.get_duration_display()}")
        print(f"   Jours: {demande_rtt.nb_jours}")
        print(f"   Heures: {demande_rtt.nb_heures}")
        
        # Test 4: RTT demi-journée
        print("\n⏰ Test 4: RTT demi-journée")
        demande_rtt_demi = DemandeConge(
            agent_id=1,
            type_absence='RTT',
            date_debut=datetime.now() + timedelta(days=9),
            date_fin=datetime.now() + timedelta(days=9),
            demi_journees='après-midi',
            motif='RTT'
        )
        demande_rtt_demi.calculate_duration()
        print(f"   Période: {demande_rtt_demi.date_debut} (après-midi)")
        print(f"   Durée: {demande_rtt_demi.get_duration_display()}")
        print(f"   Jours: {demande_rtt_demi.nb_jours}")
        print(f"   Heures: {demande_rtt_demi.nb_heures}")
        
        # Test 5: Heures supplémentaires
        print("\n⏰ Test 5: Heures supplémentaires")
        demande_hs = DemandeConge(
            agent_id=1,
            type_absence='HS',
            date_debut=datetime.now() + timedelta(days=11),
            date_fin=datetime.now() + timedelta(days=11),
            demi_journees='matin',
            motif='Heures supplémentaires'
        )
        demande_hs.calculate_duration()
        print(f"   Période: {demande_hs.date_debut} (matin)")
        print(f"   Durée: {demande_hs.get_duration_display()}")
        print(f"   Jours: {demande_hs.nb_jours}")
        print(f"   Heures: {demande_hs.nb_heures}")
        
        print("\n✅ Tests terminés avec succès!")

if __name__ == "__main__":
    test_calculs()
