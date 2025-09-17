#!/usr/bin/env python3
"""
Script d'initialisation des données de test pour le tableau de bord de gestion des congés et RTT
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.agent import Agent
from src.models.service import Service
from src.models.demande_conge import DemandeConge
from src.models.historique_conge import HistoriqueConge
from datetime import datetime, date, timedelta
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'conges-rtt-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    return app

def init_data():
    app = create_app()
    
    with app.app_context():
        # Supprimer toutes les données existantes
        print("Suppression des données existantes...")
        db.drop_all()
        db.create_all()
        
        # Créer les services
        print("Création des services...")
        service_rh = Service(nom_service="Ressources Humaines")
        service_it = Service(nom_service="Informatique")
        service_compta = Service(nom_service="Comptabilité")
        
        db.session.add_all([service_rh, service_it, service_compta])
        db.session.commit()
        
        # Créer l'administrateur général
        print("Création de l'administrateur général...")
        admin = Agent(
            nom="ADMIN",
            prenom="Super",
            email="admin@exemple.com",
            role="Admin",
            service_id=service_rh.id,
            annee_entree_fp=2020,
            date_debut_contrat=date(2020, 1, 1),
            quotite_travail=35,
            solde_ca=175,  # 25 jours * 7h
            solde_rtt=70,  # 10 jours * 7h
            solde_cet=35,  # 5 jours * 7h
            solde_bonifications=14,  # 2 jours * 7h
            solde_jours_sujetions=21,  # 3 jours * 7h
            solde_conges_formations=35  # 5 jours * 7h
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        
        # Mettre à jour les responsables de service
        service_rh.responsable_id = admin.id
        
        # Créer les responsables de service
        print("Création des responsables de service...")
        resp_it = Agent(
            nom="MARTIN",
            prenom="Jean",
            email="jean.martin@exemple.com",
            role="Responsable",
            service_id=service_it.id,
            annee_entree_fp=2018,
            date_debut_contrat=date(2018, 3, 1),
            quotite_travail=35,
            solde_ca=140,  # 20 jours * 7h
            solde_rtt=56,  # 8 jours * 7h
            solde_cet=28,  # 4 jours * 7h
            solde_bonifications=7,  # 1 jour * 7h
            solde_jours_sujetions=14,  # 2 jours * 7h
            solde_conges_formations=21  # 3 jours * 7h
        )
        resp_it.set_password("resp123")
        
        resp_compta = Agent(
            nom="DUPONT",
            prenom="Marie",
            email="marie.dupont@exemple.com",
            role="Responsable",
            service_id=service_compta.id,
            annee_entree_fp=2019,
            date_debut_contrat=date(2019, 6, 1),
            quotite_travail=35,
            solde_ca=161,  # 23 jours * 7h
            solde_rtt=63,  # 9 jours * 7h
            solde_cet=21,  # 3 jours * 7h
            solde_bonifications=10.5,  # 1.5 jours * 7h
            solde_jours_sujetions=17.5,  # 2.5 jours * 7h
            solde_conges_formations=28  # 4 jours * 7h
        )
        resp_compta.set_password("resp123")
        
        db.session.add_all([resp_it, resp_compta])
        db.session.commit()
        
        # Mettre à jour les responsables de service
        service_it.responsable_id = resp_it.id
        service_compta.responsable_id = resp_compta.id
        
        # Créer les agents
        print("Création des agents...")
        
        # Agents du service IT
        agent_it1 = Agent(
            nom="BENDAOUD",
            prenom="SOFIANE",
            email="sofiane.bendaoud@exemple.com",
            role="Agent",
            service_id=service_it.id,
            annee_entree_fp=2016,
            date_debut_contrat=date(2022, 1, 1),
            date_fin_contrat=date(2022, 12, 31),
            quotite_travail=21.5,
            solde_ca=107.5,  # Basé sur le fichier Excel
            solde_rtt=0,
            solde_cet=0,
            solde_bonifications=34.4,
            solde_jours_sujetions=0,
            solde_conges_formations=1
        )
        agent_it1.set_password("agent123")
        
        agent_it2 = Agent(
            nom="BERNARD",
            prenom="Pierre",
            email="pierre.bernard@exemple.com",
            role="Agent",
            service_id=service_it.id,
            annee_entree_fp=2021,
            date_debut_contrat=date(2021, 9, 1),
            quotite_travail=35,
            solde_ca=126,  # 18 jours * 7h
            solde_rtt=49,  # 7 jours * 7h
            solde_cet=14,  # 2 jours * 7h
            solde_bonifications=3.5,  # 0.5 jours * 7h
            solde_jours_sujetions=7,  # 1 jour * 7h
            solde_conges_formations=14  # 2 jours * 7h
        )
        agent_it2.set_password("agent123")
        
        # Agents du service Comptabilité
        agent_compta1 = Agent(
            nom="LEROY",
            prenom="Sophie",
            email="sophie.leroy@exemple.com",
            role="Agent",
            service_id=service_compta.id,
            annee_entree_fp=2020,
            date_debut_contrat=date(2020, 4, 1),
            quotite_travail=35,
            solde_ca=154,  # 22 jours * 7h
            solde_rtt=42,  # 6 jours * 7h
            solde_cet=35,  # 5 jours * 7h
            solde_bonifications=7,  # 1 jour * 7h
            solde_jours_sujetions=10.5,  # 1.5 jours * 7h
            solde_conges_formations=21  # 3 jours * 7h
        )
        agent_compta1.set_password("agent123")
        
        agent_compta2 = Agent(
            nom="MOREAU",
            prenom="Luc",
            email="luc.moreau@exemple.com",
            role="Agent",
            service_id=service_compta.id,
            annee_entree_fp=2022,
            date_debut_contrat=date(2022, 2, 1),
            quotite_travail=35,
            solde_ca=133,  # 19 jours * 7h
            solde_rtt=35,  # 5 jours * 7h
            solde_cet=7,  # 1 jour * 7h
            solde_bonifications=0,
            solde_jours_sujetions=3.5,  # 0.5 jours * 7h
            solde_conges_formations=7  # 1 jour * 7h
        )
        agent_compta2.set_password("agent123")
        
        db.session.add_all([agent_it1, agent_it2, agent_compta1, agent_compta2])
        db.session.commit()
        
        # Créer quelques demandes de congés
        print("Création des demandes de congés...")
        
        # Demande en attente
        demande1 = DemandeConge(
            agent_id=agent_it1.id,
            type_absence="CA",
            date_debut=date.today() + timedelta(days=7),
            date_fin=date.today() + timedelta(days=11),
            motif="Vacances d'été",
            nb_heures=35,  # 5 jours * 7h
            statut="En attente"
        )
        
        # Demande approuvée
        demande2 = DemandeConge(
            agent_id=agent_it2.id,
            type_absence="RTT",
            date_debut=date.today() - timedelta(days=3),
            date_fin=date.today() - timedelta(days=1),
            motif="Pont du weekend",
            nb_heures=21,  # 3 jours * 7h
            statut="Approuvée",
            date_validation=datetime.now() - timedelta(days=5),
            validateur_id=resp_it.id,
            commentaires="Approuvé, bon repos !"
        )
        
        # Demande refusée
        demande3 = DemandeConge(
            agent_id=agent_compta1.id,
            type_absence="CA",
            date_debut=date.today() + timedelta(days=1),
            date_fin=date.today() + timedelta(days=2),
            motif="Urgence familiale",
            nb_heures=14,  # 2 jours * 7h
            statut="Refusée",
            date_validation=datetime.now() - timedelta(days=1),
            validateur_id=resp_compta.id,
            commentaires="Délai trop court, merci de prévoir plus à l'avance"
        )
        
        # Demande en attente pour le service comptabilité
        demande4 = DemandeConge(
            agent_id=agent_compta2.id,
            type_absence="Congés formations",
            date_debut=date.today() + timedelta(days=14),
            date_fin=date.today() + timedelta(days=14),
            motif="Formation Excel avancé",
            nb_heures=7,  # 1 jour * 7h
            statut="En attente"
        )
        
        db.session.add_all([demande1, demande2, demande3, demande4])
        db.session.commit()
        
        # Créer un historique pour la demande approuvée
        print("Création de l'historique...")
        historique1 = HistoriqueConge(
            agent_id=agent_it2.id,
            type_evenement="Prise",
            date_evenement=demande2.date_debut,
            type_conge="RTT",
            heures_impactees=-21,
            solde_avant=70,  # Solde avant la prise
            solde_apres=49,  # Solde après la prise
            reference_demande_id=demande2.id,
            commentaire=f"Validation de la demande #{demande2.id}"
        )
        
        db.session.add(historique1)
        db.session.commit()
        
        print("Données de test créées avec succès !")
        print("\n=== COMPTES DE TEST ===")
        print("Admin général:")
        print("  Email: admin@exemple.com")
        print("  Mot de passe: admin123")
        print("\nResponsable IT:")
        print("  Email: jean.martin@exemple.com")
        print("  Mot de passe: resp123")
        print("\nResponsable Comptabilité:")
        print("  Email: marie.dupont@exemple.com")
        print("  Mot de passe: resp123")
        print("\nAgent IT (Sofiane Bendaoud - basé sur le fichier Excel):")
        print("  Email: sofiane.bendaoud@exemple.com")
        print("  Mot de passe: agent123")
        print("\nAgent IT (Pierre Bernard):")
        print("  Email: pierre.bernard@exemple.com")
        print("  Mot de passe: agent123")
        print("\nAgent Comptabilité (Sophie Leroy):")
        print("  Email: sophie.leroy@exemple.com")
        print("  Mot de passe: agent123")
        print("\nAgent Comptabilité (Luc Moreau):")
        print("  Email: luc.moreau@exemple.com")
        print("  Mot de passe: agent123")

if __name__ == "__main__":
    init_data()

