from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Utiliser l'instance db partagée
from src.models.user import db

class HistoriqueConge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    type_evenement = db.Column(db.String(50), nullable=False)  # Acquisition, Prise, Correction, etc.
    date_evenement = db.Column(db.Date, nullable=False)
    type_conge = db.Column(db.String(50), nullable=False)  # CA, RTT, CET, etc.
    heures_impactees = db.Column(db.Float, nullable=False)  # Nombre d'heures (positif ou négatif)
    solde_avant = db.Column(db.Float, nullable=False)
    solde_apres = db.Column(db.Float, nullable=False)
    reference_demande_id = db.Column(db.Integer, db.ForeignKey('demande_conge.id'), nullable=True)
    commentaire = db.Column(db.Text, nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    demande = db.relationship('DemandeConge', backref='historiques', lazy=True)

    def __repr__(self):
        return f'<HistoriqueConge {self.type_evenement} - {self.agent_id} - {self.type_conge}>'

    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'agent': {
                'id': self.agent.id,
                'nom': self.agent.nom,
                'prenom': self.agent.prenom
            } if self.agent else None,
            'type_evenement': self.type_evenement,
            'date_evenement': self.date_evenement.isoformat() if self.date_evenement else None,
            'type_conge': self.type_conge,
            'heures_impactees': self.heures_impactees,
            'solde_avant': self.solde_avant,
            'solde_apres': self.solde_apres,
            'reference_demande_id': self.reference_demande_id,
            'commentaire': self.commentaire,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None
        }

