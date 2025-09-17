from src.models.user import db
from datetime import datetime, date

class ArretMaladie(db.Model):
    __tablename__ = 'arret_maladie'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    nb_jours = db.Column(db.Float, nullable=False)  # Nombre de jours d'arrêt
    motif = db.Column(db.Text, nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    cree_par = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)  # Qui a créé l'arrêt
    
    # Relations
    agent = db.relationship('Agent', foreign_keys=[agent_id], backref='arrets_maladie', lazy=True)
    createur = db.relationship('Agent', foreign_keys=[cree_par], backref='arrets_maladie_crees', lazy=True)
    
    def calculer_perte_rtt(self):
        """
        Calcule le nombre de jours de RTT perdus selon la règle :
        - Pour les agents à 38h : 13 jours de maladie = 1 jour de RTT perdu
        - Pour chaque multiple de 13 jours
        """
        if not self.agent or not self.agent.quotite_travail:
            return 0
        
        # Règle applicable seulement pour les agents à 38h et plus
        if self.agent.quotite_travail < 38:
            return 0
        
        # Calculer le nombre de RTT perdus
        rtt_perdus = int(self.nb_jours // 13)
        return rtt_perdus
    
    def get_nb_jours_restants_pour_prochain_rtt(self):
        """
        Retourne le nombre de jours restants avant de perdre un RTT supplémentaire
        """
        if not self.agent or not self.agent.quotite_travail or self.agent.quotite_travail < 38:
            return 0
        
        jours_restants = 13 - (self.nb_jours % 13)
        return jours_restants if jours_restants < 13 else 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'date_debut': self.date_debut.isoformat() if self.date_debut else None,
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'nb_jours': self.nb_jours,
            'motif': self.motif,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'cree_par': self.cree_par,
            'perte_rtt': self.calculer_perte_rtt(),
            'jours_restants_prochain_rtt': self.get_nb_jours_restants_pour_prochain_rtt(),
            'agent_nom': f"{self.agent.prenom} {self.agent.nom}" if self.agent else None,
            'createur_nom': f"{self.createur.prenom} {self.createur.nom}" if self.createur else None
        }
    
    def __repr__(self):
        return f'<ArretMaladie {self.agent.prenom} {self.agent.nom} {self.date_debut} - {self.date_fin}>'




