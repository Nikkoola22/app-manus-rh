from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Utiliser l'instance db partagée
from src.models.user import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_service = db.Column(db.String(100), nullable=False, unique=True)
    responsable_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    responsable = db.relationship('Agent', foreign_keys=[responsable_id], backref='service_responsable', lazy=True)

    def __repr__(self):
        return f'<Service {self.nom_service}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nom_service': self.nom_service,
            'responsable_id': self.responsable_id,
            'responsable': {
                'id': self.responsable.id,
                'nom': self.responsable.nom,
                'prenom': self.responsable.prenom
            } if self.responsable else None,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'nb_agents': len(self.agents) if self.agents else 0
        }

