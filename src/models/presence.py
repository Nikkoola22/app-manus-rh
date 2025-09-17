from src.models.user import db
from datetime import datetime, date

class Presence(db.Model):
    __tablename__ = 'presence'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    date_presence = db.Column(db.Date, nullable=False)
    creneau = db.Column(db.String(10), nullable=False, default='journee')  # 'matin', 'apres_midi', 'journee'
    statut = db.Column(db.String(20), nullable=False)  # 'present', 'absent', 'conges', 'maladie', 'rtt'
    motif = db.Column(db.Text, nullable=True)
    heure_debut = db.Column(db.Time, nullable=True)  # Heure de début pour les présences partielles
    heure_fin = db.Column(db.Time, nullable=True)    # Heure de fin pour les présences partielles
    duree_heures = db.Column(db.Float, nullable=True)  # Durée en heures (pour calculs)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    cree_par = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)  # Qui a créé l'entrée
    
    # Relations
    agent = db.relationship('Agent', foreign_keys=[agent_id], backref='presences', lazy=True)
    createur = db.relationship('Agent', foreign_keys=[cree_par], backref='presences_crees', lazy=True)
    
    # Contrainte unique pour éviter les doublons (agent + date + créneau)
    __table_args__ = (db.UniqueConstraint('agent_id', 'date_presence', 'creneau', name='unique_agent_date_creneau'),)
    
    def get_statut_color(self):
        """Retourne la couleur associée au statut"""
        colors = {
            'present': 'green',
            'absent': 'red',
            'conges': 'blue',
            'maladie': 'orange',
            'rtt': 'purple',
            'partiel': 'yellow'
        }
        return colors.get(self.statut, 'gray')
    
    def get_statut_label(self):
        """Retourne le libellé du statut"""
        labels = {
            'present': 'Présent',
            'absent': 'Absent',
            'conges': 'Congés',
            'maladie': 'Maladie',
            'rtt': 'RTT',
            'partiel': 'Présence partielle'
        }
        return labels.get(self.statut, self.statut)
    
    def get_creneau_label(self):
        """Retourne le libellé du créneau"""
        labels = {
            'matin': 'Matin',
            'apres_midi': 'Après-midi',
            'journee': 'Journée'
        }
        return labels.get(self.creneau, self.creneau)
    
    def get_creneau_color(self):
        """Retourne la couleur associée au créneau"""
        colors = {
            'matin': 'bg-blue-50 border-blue-200',
            'apres_midi': 'bg-green-50 border-green-200',
            'journee': 'bg-gray-50 border-gray-200'
        }
        return colors.get(self.creneau, 'bg-gray-50 border-gray-200')
    
    def get_duree_display(self):
        """Retourne l'affichage de la durée"""
        if self.duree_heures:
            if self.duree_heures == 7.0:
                return "Journée complète"
            elif self.duree_heures < 7.0:
                return f"{self.duree_heures}h"
            else:
                return f"{self.duree_heures}h"
        return ""
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'date_presence': self.date_presence.isoformat() if self.date_presence else None,
            'creneau': self.creneau,
            'statut': self.statut,
            'motif': self.motif,
            'heure_debut': self.heure_debut.isoformat() if self.heure_debut else None,
            'heure_fin': self.heure_fin.isoformat() if self.heure_fin else None,
            'duree_heures': self.duree_heures,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'cree_par': self.cree_par,
            'statut_color': self.get_statut_color(),
            'statut_label': self.get_statut_label(),
            'creneau_label': self.get_creneau_label(),
            'creneau_color': self.get_creneau_color(),
            'duree_display': self.get_duree_display(),
            'agent_nom': f"{self.agent.prenom} {self.agent.nom}" if self.agent else None,
            'createur_nom': f"{self.createur.prenom} {self.createur.nom}" if self.createur else None
        }
    
    def __repr__(self):
        return f'<Presence {self.agent.prenom} {self.agent.nom} {self.date_presence} - {self.statut}>'
