from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
from src.models.user import db

class PlanningAgent(db.Model):
    """Modèle pour les plannings des agents"""
    __tablename__ = 'planning_agent'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    jour_semaine = db.Column(db.Integer, nullable=False)  # 0=Lundi, 1=Mardi, ..., 5=Samedi
    heure_debut = db.Column(db.Time, nullable=False)  # Heure de début (ex: 08:00)
    heure_fin = db.Column(db.Time, nullable=False)    # Heure de fin (ex: 17:00)
    pause_debut = db.Column(db.Time, nullable=True)   # Début de pause (ex: 12:00)
    pause_fin = db.Column(db.Time, nullable=True)     # Fin de pause (ex: 13:00)
    actif = db.Column(db.Boolean, default=True)       # Planning actif ou non
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    agent = db.relationship('Agent', backref='plannings', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'jour_semaine': self.jour_semaine,
            'jour_nom': self.get_jour_nom(),
            'heure_debut': self.heure_debut.strftime('%H:%M') if self.heure_debut else None,
            'heure_fin': self.heure_fin.strftime('%H:%M') if self.heure_fin else None,
            'pause_debut': self.pause_debut.strftime('%H:%M') if self.pause_debut else None,
            'pause_fin': self.pause_fin.strftime('%H:%M') if self.pause_fin else None,
            'actif': self.actif,
            'duree_travail': self.calculer_duree_travail(),
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None
        }
    
    def get_jour_nom(self):
        """Retourne le nom du jour de la semaine"""
        jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
        return jours[self.jour_semaine] if 0 <= self.jour_semaine < 6 else 'Inconnu'
    
    def calculer_duree_travail(self):
        """Calcule la durée de travail en heures (sans les pauses)"""
        if not self.heure_debut or not self.heure_fin:
            return 0
        
        # Convertir en minutes pour faciliter les calculs
        debut_minutes = self.heure_debut.hour * 60 + self.heure_debut.minute
        fin_minutes = self.heure_fin.hour * 60 + self.heure_fin.minute
        
        duree_totale = fin_minutes - debut_minutes
        
        # Soustraire la durée de pause si elle existe
        if self.pause_debut and self.pause_fin:
            pause_debut_minutes = self.pause_debut.hour * 60 + self.pause_debut.minute
            pause_fin_minutes = self.pause_fin.hour * 60 + self.pause_fin.minute
            duree_pause = pause_fin_minutes - pause_debut_minutes
            duree_totale -= duree_pause
        
        return round(duree_totale / 60, 2)  # Convertir en heures
    
    def get_creneaux_30min(self):
        """Génère tous les créneaux de 30 minutes pour ce jour"""
        if not self.heure_debut or not self.heure_fin:
            return []
        
        creneaux = []
        current_time = self.heure_debut
        
        while current_time < self.heure_fin:
            # Vérifier si ce créneau est dans la pause
            est_en_pause = False
            if self.pause_debut and self.pause_fin:
                est_en_pause = self.pause_debut <= current_time < self.pause_fin
            
            creneaux.append({
                'heure': current_time.strftime('%H:%M'),
                'en_pause': est_en_pause,
                'travail': not est_en_pause and self.actif
            })
            
            # Ajouter 30 minutes
            current_minutes = current_time.hour * 60 + current_time.minute + 30
            # Gérer le dépassement de 24h
            if current_minutes >= 1440:  # 24h * 60min
                break
            current_time = time(current_minutes // 60, current_minutes % 60)
        
        return creneaux

class PlanningTemplate(db.Model):
    """Modèle pour les modèles de planning réutilisables"""
    __tablename__ = 'planning_template'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)
    plannings = db.Column(db.JSON, nullable=False)  # Stockage des plannings en JSON
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    service = db.relationship('Service', backref='planning_templates', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'service_id': self.service_id,
            'plannings': self.plannings,
            'actif': self.actif,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None
        }
