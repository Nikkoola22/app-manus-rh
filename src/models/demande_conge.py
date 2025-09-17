from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Utiliser l'instance db partagée
from src.models.user import db

class DemandeConge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    type_absence = db.Column(db.String(50), nullable=False)  # CA, RTT, CET, Jours de sujétions, etc.
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    demi_journees = db.Column(db.String(20), nullable=True)  # matin, après-midi, journée complète
    motif = db.Column(db.Text, nullable=True)
    statut = db.Column(db.String(20), nullable=False, default='En attente')  # En attente, Approuvée, Refusée, Annulée
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    date_validation = db.Column(db.DateTime, nullable=True)
    date_annulation = db.Column(db.DateTime, nullable=True)
    validateur_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=True)
    commentaires = db.Column(db.Text, nullable=True)
    nb_heures = db.Column(db.Float, nullable=False, default=0.0)  # Nombre d'heures demandées (pour RTT, HS)
    nb_jours = db.Column(db.Float, nullable=False, default=0.0)  # Nombre de jours demandés (pour CA)
    # Relations - supprimées car définies dans Agent
    
    def __repr__(self):
        return f'<DemandeConge {self.type_absence} - {self.agent_id} - {self.statut}>'
    
    def calculate_duration(self):
        """Calcule la durée en jours ou heures selon le type d'absence"""
        from datetime import datetime, timedelta
        
        # Calculer la différence en jours
        if self.date_debut and self.date_fin:
            delta = self.date_fin - self.date_debut
            total_days = delta.days + 1  # +1 pour inclure le jour de fin
            
            # Pour les congés annuels (CA), calculer en jours
            if self.type_absence == 'CA':
                if self.demi_journees == 'matin' or self.demi_journees == 'après-midi':
                    self.nb_jours = total_days * 0.5  # Demi-journée
                else:
                    self.nb_jours = total_days  # Journée complète
                self.nb_heures = 0.0
                
            # Pour les RTT et heures supplémentaires, calculer en heures
            elif self.type_absence in ['RTT', 'HS']:
                if self.demi_journees == 'matin' or self.demi_journees == 'après-midi':
                    self.nb_heures = total_days * 4.0  # 4h par demi-journée
                else:
                    self.nb_heures = total_days * 8.0  # 8h par journée complète
                self.nb_jours = 0.0
                
            # Pour les autres types, utiliser la logique par défaut
            else:
                if self.demi_journees == 'matin' or self.demi_journees == 'après-midi':
                    self.nb_jours = total_days * 0.5
                    self.nb_heures = total_days * 4.0
                else:
                    self.nb_jours = total_days
                    self.nb_heures = total_days * 8.0
    
    def get_duration_display(self):
        """Retourne l'affichage de la durée selon le type"""
        if self.type_absence == 'CA':
            if self.nb_jours == 1.0:
                return "1 jour"
            elif self.nb_jours == 0.5:
                return "0.5 jour"
            else:
                return f"{self.nb_jours} jours"
        elif self.type_absence in ['RTT', 'HS']:
            if self.nb_heures == 1.0:
                return "1 heure"
            else:
                return f"{self.nb_heures} heures"
        else:
            return f"{self.nb_jours} jours / {self.nb_heures} heures"

    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'agent': {
                'id': self.agent.id,
                'nom': self.agent.nom,
                'prenom': self.agent.prenom
            } if self.agent else None,
            'type_absence': self.type_absence,
            'date_debut': self.date_debut.isoformat() if self.date_debut else None,
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'demi_journees': self.demi_journees,
            'motif': self.motif,
            'statut': self.statut,
            'date_demande': self.date_demande.isoformat() if self.date_demande else None,
            'date_validation': self.date_validation.isoformat() if self.date_validation else None,
            'date_annulation': self.date_annulation.isoformat() if self.date_annulation else None,
            'validateur_id': self.validateur_id,
            'validateur': {
                'id': self.validateur.id,
                'nom': self.validateur.nom,
                'prenom': self.validateur.prenom
            } if self.validateur else None,
            'commentaires': self.commentaires,
            'nb_heures': self.nb_heures,
            'nb_jours': self.nb_jours,
            'duration_display': self.get_duration_display()
        }

