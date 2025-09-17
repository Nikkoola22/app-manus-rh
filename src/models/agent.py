from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Utiliser l'instance db partagée
from src.models.user import db

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Agent')  # Agent, Responsable, Admin
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)
    annee_entree_fp = db.Column(db.Integer, nullable=True)
    date_debut_contrat = db.Column(db.Date, nullable=True)
    date_fin_contrat = db.Column(db.Date, nullable=True)
    quotite_travail = db.Column(db.Float, nullable=True)
    solde_ca = db.Column(db.Float, default=0.0)  # Congés annuels en jours
    solde_rtt = db.Column(db.Float, default=0.0)  # RTT en heures
    solde_cet = db.Column(db.Float, default=0.0)  # Compte Épargne Temps en heures
    solde_bonifications = db.Column(db.Float, default=0.0)  # Bonifications en heures
    solde_jours_sujetions = db.Column(db.Float, default=0.0)  # Jours de sujétions en jours
    solde_conges_formations = db.Column(db.Float, default=0.0)  # Congés formations en jours
    solde_hs = db.Column(db.Float, default=0.0)  # Heures supplémentaires en heures
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    service = db.relationship('Service', foreign_keys=[service_id], backref='agents', lazy=True)
    demandes = db.relationship('DemandeConge', foreign_keys='DemandeConge.agent_id', backref='agent', lazy=True)
    historiques = db.relationship('HistoriqueConge', backref='agent', lazy=True)
    demandes_validees = db.relationship('DemandeConge', foreign_keys='DemandeConge.validateur_id', backref='validateur', lazy=True)

    def set_password(self, password):
        self.mot_de_passe_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.mot_de_passe_hash, password)

    def __repr__(self):
        return f'<Agent {self.prenom} {self.nom}>'

    def calculate_rtt_from_quotite(self):
        """Calcule le nombre d'heures RTT en fonction de la quotité de travail"""
        if not self.quotite_travail:
            return 0
        
        quotite = self.quotite_travail
        
        # Règles de calcul des RTT selon la quotité (en heures)
        if quotite >= 38:
            return 18 * 8  # 18 RTT * 8h = 144h pour 38h et plus
        elif quotite >= 36:
            return 6 * 8   # 6 RTT * 8h = 48h pour 36h
        elif quotite >= 35:
            return 0       # Pas de RTT pour 35h
        else:
            return 0       # Pas de RTT pour moins de 35h
    
    def get_effective_rtt_solde(self):
        """Retourne le solde RTT effectif (calculé automatiquement)"""
        return self.calculate_rtt_from_quotite()
    
    def get_solde_by_type(self, type_absence):
        """Retourne le solde selon le type d'absence"""
        if type_absence == 'CA':
            return self.solde_ca  # En jours
        elif type_absence == 'RTT':
            return self.get_effective_rtt_solde()  # En heures
        elif type_absence == 'HS':
            return self.solde_hs  # En heures
        elif type_absence == 'CET':
            return self.solde_cet  # En heures
        elif type_absence == 'Jours de sujétions':
            return self.solde_jours_sujetions  # En jours
        elif type_absence == 'Congés formations':
            return self.solde_conges_formations  # En jours
        else:
            return 0
    
    def get_solde_display(self, type_absence):
        """Retourne l'affichage du solde selon le type"""
        solde = self.get_solde_by_type(type_absence)
        
        if type_absence in ['CA', 'Jours de sujétions', 'Congés formations']:
            if solde == 1.0:
                return "1 jour"
            else:
                return f"{solde} jours"
        else:  # RTT, HS, CET en heures
            if solde == 1.0:
                return "1 heure"
            else:
                return f"{solde} heures"

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'email': self.email,
            'role': self.role,
            'service_id': self.service_id,
            'service': {
                'id': self.service.id,
                'nom_service': self.service.nom_service
            } if self.service else None,
            'annee_entree_fp': self.annee_entree_fp,
            'date_debut_contrat': self.date_debut_contrat.isoformat() if self.date_debut_contrat else None,
            'date_fin_contrat': self.date_fin_contrat.isoformat() if self.date_fin_contrat else None,
            'quotite_travail': self.quotite_travail,
            'solde_ca': self.solde_ca,  # En jours
            'solde_rtt': self.get_effective_rtt_solde(),  # En heures
            'solde_cet': self.solde_cet,  # En heures
            'solde_bonifications': self.solde_bonifications,  # En heures
            'solde_jours_sujetions': self.solde_jours_sujetions,  # En jours
            'solde_conges_formations': self.solde_conges_formations,  # En jours
            'solde_hs': self.solde_hs,  # En heures
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            # Affichage des soldes avec unités
            'solde_ca_display': self.get_solde_display('CA'),
            'solde_rtt_display': self.get_solde_display('RTT'),
            'solde_hs_display': self.get_solde_display('HS')
        }

