from flask import Blueprint, request, jsonify, session
from src.models.demande_conge import DemandeConge, db
from src.models.agent import Agent
from src.models.historique_conge import HistoriqueConge
from src.routes.auth import login_required, role_required
from src.services.email_service import send_demande_conge_email, send_validation_email
from datetime import datetime, timedelta

demandes_bp = Blueprint('demandes', __name__)

def calculate_hours_between_dates(date_debut, date_fin, demi_journees=None, quotite_travail=35):
    """Calcule le nombre d'heures entre deux dates en tenant compte des demi-journées"""
    if date_debut > date_fin:
        return 0
    
    # Calcul simple : nombre de jours ouvrés * heures par jour
    days_diff = (date_fin - date_debut).days + 1
    hours_per_day = quotite_travail / 5  # Répartition sur 5 jours ouvrés
    
    if demi_journees == 'matin' or demi_journees == 'après-midi':
        if days_diff == 1:
            return hours_per_day / 2
        else:
            # Premier jour demi-journée + jours complets + dernier jour demi-journée
            return (hours_per_day / 2) + ((days_diff - 2) * hours_per_day) + (hours_per_day / 2)
    else:
        return days_diff * hours_per_day

def calculate_hours_from_planning(agent_id, date_debut, date_fin, demi_journees=None):
    """Calcule le nombre d'heures en utilisant le planning de l'agent"""
    from src.models.planning import PlanningAgent
    
    if date_debut > date_fin:
        return 0
    
    total_hours = 0
    current_date = date_debut
    
    while current_date <= date_fin:
        # Obtenir le jour de la semaine (0 = Lundi, 1 = Mardi, etc.)
        jour_semaine = current_date.weekday()
        
        # Chercher le planning pour ce jour
        planning = PlanningAgent.query.filter_by(
            agent_id=agent_id,
            jour_semaine=jour_semaine,
            actif=True
        ).first()
        
        if planning:
            # Calculer les heures de travail pour ce jour
            if planning.heure_debut and planning.heure_fin:
                # Convertir les heures en minutes pour le calcul
                debut_minutes = planning.heure_debut.hour * 60 + planning.heure_debut.minute
                fin_minutes = planning.heure_fin.hour * 60 + planning.heure_fin.minute
                
                # Soustraire la pause si elle existe
                if planning.pause_debut and planning.pause_fin:
                    pause_debut_minutes = planning.pause_debut.hour * 60 + planning.pause_debut.minute
                    pause_fin_minutes = planning.pause_fin.hour * 60 + planning.pause_fin.minute
                    pause_duration = pause_fin_minutes - pause_debut_minutes
                else:
                    pause_duration = 0
                
                # Calculer la durée de travail en minutes
                work_duration_minutes = (fin_minutes - debut_minutes) - pause_duration
                
                # Convertir en heures
                work_hours = work_duration_minutes / 60
                
                # Appliquer les demi-journées si nécessaire
                if demi_journees == 'matin' or demi_journees == 'après-midi':
                    # Pour les demi-journées, calculer les heures réelles du matin ou après-midi
                    if demi_journees == 'matin':
                        # Matin : de l'heure de début jusqu'à midi (ou heure de pause si avant midi)
                        midi_minutes = 12 * 60  # 12h00 en minutes
                        if planning.pause_debut and planning.pause_debut.hour < 12:
                            # Si pause avant midi, s'arrêter à la pause
                            fin_matin_minutes = planning.pause_debut.hour * 60 + planning.pause_debut.minute
                        else:
                            # Sinon, s'arrêter à midi
                            fin_matin_minutes = midi_minutes
                        
                        work_hours = max(0, (fin_matin_minutes - debut_minutes) / 60)
                    else:  # après-midi
                        # Après-midi : de midi (ou fin de pause) jusqu'à l'heure de fin
                        midi_minutes = 12 * 60  # 12h00 en minutes
                        if planning.pause_fin and planning.pause_fin.hour >= 12:
                            # Si pause après midi, commencer à la fin de pause
                            debut_apres_midi_minutes = planning.pause_fin.hour * 60 + planning.pause_fin.minute
                        else:
                            # Sinon, commencer à midi
                            debut_apres_midi_minutes = midi_minutes
                        
                        work_hours = max(0, (fin_minutes - debut_apres_midi_minutes) / 60)
                
                total_hours += work_hours
        else:
            # Si pas de planning, utiliser la quotité par défaut
            quotite_travail = 35  # Valeur par défaut
            hours_per_day = quotite_travail / 5
            
            if demi_journees == 'matin' or demi_journees == 'après-midi':
                total_hours += hours_per_day / 2
            else:
                total_hours += hours_per_day
        
        # Passer au jour suivant
        from datetime import timedelta
        current_date += timedelta(days=1)
    
    return round(total_hours, 1)

@demandes_bp.route('/demandes', methods=['GET'])
@login_required
def get_demandes():
    current_user = Agent.query.get(session['user_id'])
    
    if current_user.role == 'Agent':
        # Agent ne peut voir que ses propres demandes
        demandes = DemandeConge.query.filter_by(agent_id=current_user.id).all()
    elif current_user.role == 'Responsable':
        # Responsable peut voir les demandes de son service
        agents_service = Agent.query.filter_by(service_id=current_user.service_id).all()
        agent_ids = [agent.id for agent in agents_service]
        demandes = DemandeConge.query.filter(DemandeConge.agent_id.in_(agent_ids)).all()
    elif current_user.role == 'Admin':
        # Admin peut voir toutes les demandes
        demandes = DemandeConge.query.all()
    else:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    
    return jsonify([demande.to_dict() for demande in demandes]), 200

@demandes_bp.route('/demandes/mes-demandes', methods=['GET'])
@login_required
def get_mes_demandes():
    """Récupère les demandes de congés du responsable connecté"""
    current_user = Agent.query.get(session['user_id'])
    
    if current_user.role != 'Responsable':
        return jsonify({'error': 'Accès non autorisé'}), 403
    
    # Le responsable voit ses propres demandes
    demandes = DemandeConge.query.filter_by(agent_id=current_user.id).all()
    
    return jsonify([demande.to_dict() for demande in demandes])

@demandes_bp.route('/demandes/<int:demande_id>', methods=['GET'])
@login_required
def get_demande(demande_id):
    current_user = Agent.query.get(session['user_id'])
    demande = DemandeConge.query.get_or_404(demande_id)
    
    # Vérifier les permissions
    if current_user.role == 'Agent' and demande.agent_id != current_user.id:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    elif current_user.role == 'Responsable':
        agent_demande = Agent.query.get(demande.agent_id)
        if agent_demande.service_id != current_user.service_id:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
    
    return jsonify(demande.to_dict()), 200

@demandes_bp.route('/demandes/agent/<int:agent_id>', methods=['GET'])
@login_required
def get_demandes_agent(agent_id):
    current_user = Agent.query.get(session['user_id'])
    target_agent = Agent.query.get_or_404(agent_id)
    
    # Vérifier les permissions
    if current_user.role == 'Agent' and current_user.id != agent_id:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    elif current_user.role == 'Responsable' and target_agent.service_id != current_user.service_id:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    
    # Récupérer les demandes de l'agent
    demandes = DemandeConge.query.filter_by(agent_id=agent_id).all()
    
    return jsonify([demande.to_dict() for demande in demandes]), 200

@demandes_bp.route('/demandes', methods=['POST'])
@login_required
def create_demande():
    current_user = Agent.query.get(session['user_id'])
    data = request.get_json()
    
    # Vérifier les champs requis
    required_fields = ['type_absence', 'date_debut', 'date_fin']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis'}), 400
    
    # Convertir les dates
    try:
        date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%d').date()
        date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Format de date invalide (YYYY-MM-DD attendu)'}), 400
    
    # Vérifier que la date de début est antérieure ou égale à la date de fin
    if date_debut > date_fin:
        return jsonify({'error': 'La date de début doit être antérieure ou égale à la date de fin'}), 400
    
    # Calculer le nombre d'heures
    type_absence = data['type_absence']
    
    # Pour les types en heures (RTT, HS), utiliser le planning
    if type_absence in ['RTT', 'HS']:
        nb_heures = calculate_hours_from_planning(
            current_user.id,
            date_debut, 
            date_fin, 
            data.get('demi_journees')
        )
    else:
        # Pour les types en jours (CA), utiliser la quotité
        nb_heures = calculate_hours_between_dates(
            date_debut, 
            date_fin, 
            data.get('demi_journees'),
            current_user.quotite_travail or 35
        )
    
    # Vérifier si l'agent a suffisamment de solde
    solde_disponible = 0
    
    if type_absence == 'CA':
        solde_disponible = current_user.solde_ca
    elif type_absence == 'RTT':
        solde_disponible = current_user.get_effective_rtt_solde()  # Calcul automatique des RTT
    elif type_absence == 'CET':
        solde_disponible = current_user.solde_cet
    elif type_absence == 'Bonifications':
        solde_disponible = current_user.solde_bonifications
    elif type_absence == 'Jours de sujétions':
        solde_disponible = current_user.solde_jours_sujetions
    elif type_absence == 'Congés formations':
        solde_disponible = current_user.solde_conges_formations
    
    if nb_heures > solde_disponible:
        return jsonify({'error': f'Solde insuffisant. Disponible: {solde_disponible}h, Demandé: {nb_heures}h'}), 400
    
    # Créer la demande
    demande = DemandeConge(
        agent_id=current_user.id,
        type_absence=type_absence,
        date_debut=date_debut,
        date_fin=date_fin,
        demi_journees=data.get('demi_journees'),
        motif=data.get('motif'),
        nb_heures=nb_heures
    )
    
    db.session.add(demande)
    db.session.commit()
    
    # Envoyer un email selon le rôle de l'utilisateur
    try:
        if current_user.role == 'Responsable':
            # Les demandes des responsables sont envoyées à l'admin
            admin = Agent.query.filter_by(role='Admin').first()
            if admin:
                send_demande_conge_email(current_user, admin, demande)
        else:
            # Les demandes des agents sont envoyées au responsable du service
            responsable = Agent.query.filter_by(
                service_id=current_user.service_id,
                role='Responsable'
            ).first()
            
            if responsable:
                send_demande_conge_email(current_user, responsable, demande)
    except Exception as e:
        # Ne pas faire échouer la création de la demande si l'email échoue
        print(f"Erreur lors de l'envoi de l'email: {str(e)}")
    
    return jsonify(demande.to_dict()), 201

@demandes_bp.route('/demandes/<int:demande_id>/valider', methods=['POST'])
@login_required
@role_required(['Responsable', 'Admin'])
def valider_demande(demande_id):
    current_user = Agent.query.get(session['user_id'])
    demande = DemandeConge.query.get_or_404(demande_id)
    data = request.get_json()
    
    # Vérifier les permissions
    agent_demande = Agent.query.get(demande.agent_id)
    
    if current_user.role == 'Responsable':
        # Les responsables ne peuvent valider que les demandes des agents de leur service
        if agent_demande.service_id != current_user.service_id:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
        # Les responsables ne peuvent pas valider leurs propres demandes
        if agent_demande.id == current_user.id:
            return jsonify({'error': 'Vous ne pouvez pas valider vos propres demandes'}), 403
    elif current_user.role == 'Admin':
        # L'admin peut valider toutes les demandes
        pass
    else:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    
    # Vérifier que la demande est en attente
    if demande.statut != 'En attente':
        return jsonify({'error': 'Cette demande a déjà été traitée'}), 400
    
    # Récupérer l'action (approuver ou refuser)
    action = data.get('action')  # 'approuver' ou 'refuser'
    commentaires = data.get('commentaires', '')
    
    if action not in ['approuver', 'refuser']:
        return jsonify({'error': 'Action invalide. Utilisez "approuver" ou "refuser"'}), 400
    
    # Mettre à jour la demande
    demande.statut = 'Approuvée' if action == 'approuver' else 'Refusée'
    demande.date_validation = datetime.utcnow()
    demande.validateur_id = current_user.id
    demande.commentaires = commentaires
    
    # Si approuvée, déduire du solde de l'agent et créer un historique
    if action == 'approuver':
        agent = Agent.query.get(demande.agent_id)
        type_absence = demande.type_absence
        nb_heures = demande.nb_heures
        
        # Sauvegarder le solde avant modification
        solde_avant = 0
        
        if type_absence == 'CA':
            solde_avant = agent.solde_ca
            agent.solde_ca -= nb_heures
        elif type_absence == 'RTT':
            solde_avant = agent.solde_rtt
            agent.solde_rtt -= nb_heures
        elif type_absence == 'CET':
            solde_avant = agent.solde_cet
            agent.solde_cet -= nb_heures
        elif type_absence == 'Bonifications':
            solde_avant = agent.solde_bonifications
            agent.solde_bonifications -= nb_heures
        elif type_absence == 'Jours de sujétions':
            solde_avant = agent.solde_jours_sujetions
            agent.solde_jours_sujetions -= nb_heures
        elif type_absence == 'Congés formations':
            solde_avant = agent.solde_conges_formations
            agent.solde_conges_formations -= nb_heures
        
        # Créer un historique
        historique = HistoriqueConge(
            agent_id=agent.id,
            type_evenement='Prise',
            date_evenement=demande.date_debut,
            type_conge=type_absence,
            heures_impactees=-nb_heures,
            solde_avant=solde_avant,
            solde_apres=solde_avant - nb_heures,
            reference_demande_id=demande.id,
            commentaire=f'Validation de la demande #{demande.id}'
        )
        
        db.session.add(historique)
    
    db.session.commit()
    
    # Envoyer un email à l'agent pour l'informer de la décision
    try:
        agent = Agent.query.get(demande.agent_id)
        if agent:
            decision = 'Approuvée' if action == 'approuver' else 'Refusée'
            send_validation_email(agent, current_user, demande, decision)
    except Exception as e:
        # Ne pas faire échouer la validation si l'email échoue
        print(f"Erreur lors de l'envoi de l'email de validation: {str(e)}")
    
    return jsonify(demande.to_dict()), 200

@demandes_bp.route('/demandes/<int:demande_id>/annuler', methods=['POST'])
@login_required
def annuler_demande(demande_id):
    """Permet à un agent d'annuler sa propre demande tant qu'elle n'est pas validée"""
    current_user = Agent.query.get(session['user_id'])
    demande = DemandeConge.query.get_or_404(demande_id)
    
    # Seul l'agent qui a fait la demande peut l'annuler
    if demande.agent_id != current_user.id:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    
    # Vérifier que la demande est en attente
    if demande.statut != 'En attente':
        return jsonify({'error': 'Impossible d\'annuler une demande déjà traitée'}), 400
    
    # Changer le statut à "Annulée"
    demande.statut = 'Annulée'
    demande.date_annulation = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Demande annulée avec succès',
        'demande': demande.to_dict()
    }), 200

@demandes_bp.route('/demandes/<int:demande_id>', methods=['DELETE'])
@login_required
def delete_demande(demande_id):
    current_user = Agent.query.get(session['user_id'])
    demande = DemandeConge.query.get_or_404(demande_id)
    
    # Seul l'agent qui a fait la demande peut la supprimer, et seulement si elle est en attente
    if demande.agent_id != current_user.id:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    
    if demande.statut != 'En attente':
        return jsonify({'error': 'Impossible de supprimer une demande déjà traitée'}), 400
    
    db.session.delete(demande)
    db.session.commit()
    
    return jsonify({'message': 'Demande supprimée avec succès'}), 200

