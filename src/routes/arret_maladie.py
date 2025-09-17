from flask import Blueprint, request, jsonify, session
from src.models.arret_maladie import ArretMaladie
from src.models.agent import Agent
from src.models.user import db
from src.routes.auth import login_required, role_required
from datetime import datetime, date, timedelta

arret_maladie_bp = Blueprint('arret_maladie', __name__)

@arret_maladie_bp.route('/arret-maladie', methods=['GET'])
@login_required
def get_arret_maladie():
    """Récupère les arrêts maladie selon les permissions de l'utilisateur"""
    try:
        current_user = Agent.query.get(session['user_id'])
        agent_id = request.args.get('agent_id')
        
        if current_user.role == 'Admin':
            # Admin peut voir tous les arrêts maladie
            if agent_id:
                arrets = ArretMaladie.query.filter_by(agent_id=agent_id).all()
            else:
                arrets = ArretMaladie.query.all()
        elif current_user.role == 'Responsable':
            # Responsable peut voir les arrêts de son service
            if agent_id:
                # Vérifier que l'agent appartient au service du responsable
                agent = Agent.query.get(agent_id)
                if agent and agent.service_id == current_user.service_id:
                    arrets = ArretMaladie.query.filter_by(agent_id=agent_id).all()
                else:
                    return jsonify({'error': 'Permissions insuffisantes'}), 403
            else:
                # Récupérer tous les agents du service
                agents_du_service = Agent.query.filter_by(service_id=current_user.service_id).all()
                agent_ids = [agent.id for agent in agents_du_service]
                arrets = ArretMaladie.query.filter(ArretMaladie.agent_id.in_(agent_ids)).all()
        elif current_user.role == 'Agent':
            # Agent peut voir seulement ses propres arrêts
            arrets = ArretMaladie.query.filter_by(agent_id=current_user.id).all()
        else:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        return jsonify([arret.to_dict() for arret in arrets]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arret_maladie_bp.route('/arret-maladie', methods=['POST'])
@login_required
@role_required(['Admin', 'Responsable'])
def create_arret_maladie():
    """Crée un nouvel arrêt maladie"""
    try:
        data = request.get_json()
        current_user = Agent.query.get(session['user_id'])
        
        # Validation des champs requis
        required_fields = ['agent_id', 'date_debut', 'date_fin']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ {field} est requis'}), 400
        
        agent_id = data['agent_id']
        
        # Vérifier les permissions
        if current_user.role == 'Responsable':
            agent = Agent.query.get(agent_id)
            if not agent or agent.service_id != current_user.service_id:
                return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        # Vérifier que l'agent existe
        agent = Agent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agent non trouvé'}), 404
        
        # Calculer le nombre de jours
        date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%d').date()
        date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%d').date()
        
        if date_debut > date_fin:
            return jsonify({'error': 'La date de début doit être antérieure à la date de fin'}), 400
        
        # Calculer le nombre de jours (inclus les deux dates)
        nb_jours = (date_fin - date_debut).days + 1
        
        # Créer l'arrêt maladie
        arret = ArretMaladie(
            agent_id=agent_id,
            date_debut=date_debut,
            date_fin=date_fin,
            nb_jours=nb_jours,
            motif=data.get('motif', ''),
            cree_par=current_user.id
        )
        
        db.session.add(arret)
        db.session.commit()
        
        # Calculer la perte de RTT et mettre à jour l'agent si nécessaire
        perte_rtt = arret.calculer_perte_rtt()
        if perte_rtt > 0:
            # Mettre à jour le solde RTT de l'agent
            agent.solde_rtt = max(0, agent.solde_rtt - perte_rtt)
            db.session.commit()
        
        return jsonify(arret.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': f'Format de date invalide: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@arret_maladie_bp.route('/arret-maladie/<int:arret_id>', methods=['PUT'])
@login_required
@role_required(['Admin', 'Responsable'])
def update_arret_maladie(arret_id):
    """Met à jour un arrêt maladie"""
    try:
        arret = ArretMaladie.query.get_or_404(arret_id)
        current_user = Agent.query.get(session['user_id'])
        
        # Vérifier les permissions
        if current_user.role == 'Responsable':
            if arret.agent.service_id != current_user.service_id:
                return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        data = request.get_json()
        
        # Sauvegarder l'ancienne perte de RTT pour la restauration
        ancienne_perte_rtt = arret.calculer_perte_rtt()
        
        # Mettre à jour les champs
        if 'date_debut' in data:
            arret.date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%d').date()
        if 'date_fin' in data:
            arret.date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%d').date()
        if 'motif' in data:
            arret.motif = data['motif']
        
        # Recalculer le nombre de jours
        if 'date_debut' in data or 'date_fin' in data:
            arret.nb_jours = (arret.date_fin - arret.date_debut).days + 1
        
        # Calculer la nouvelle perte de RTT
        nouvelle_perte_rtt = arret.calculer_perte_rtt()
        difference_rtt = nouvelle_perte_rtt - ancienne_perte_rtt
        
        # Mettre à jour le solde RTT de l'agent
        if difference_rtt != 0:
            agent = arret.agent
            agent.solde_rtt = max(0, agent.solde_rtt - difference_rtt)
        
        db.session.commit()
        
        return jsonify(arret.to_dict()), 200
        
    except ValueError as e:
        return jsonify({'error': f'Format de date invalide: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@arret_maladie_bp.route('/arret-maladie/<int:arret_id>', methods=['DELETE'])
@login_required
@role_required(['Admin', 'Responsable'])
def delete_arret_maladie(arret_id):
    """Supprime un arrêt maladie"""
    try:
        arret = ArretMaladie.query.get_or_404(arret_id)
        current_user = Agent.query.get(session['user_id'])
        
        # Vérifier les permissions
        if current_user.role == 'Responsable':
            if arret.agent.service_id != current_user.service_id:
                return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        # Calculer la perte de RTT pour la restaurer
        perte_rtt = arret.calculer_perte_rtt()
        
        # Restaurer le solde RTT de l'agent
        if perte_rtt > 0:
            agent = arret.agent
            agent.solde_rtt += perte_rtt
            db.session.commit()
        
        # Supprimer l'arrêt maladie
        db.session.delete(arret)
        db.session.commit()
        
        return jsonify({'message': 'Arrêt maladie supprimé avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@arret_maladie_bp.route('/arret-maladie/agent/<int:agent_id>/statistiques', methods=['GET'])
@login_required
def get_statistiques_arret_maladie(agent_id):
    """Récupère les statistiques d'arrêt maladie pour un agent"""
    try:
        current_user = Agent.query.get(session['user_id'])
        
        # Vérifier les permissions
        if current_user.role == 'Agent' and current_user.id != agent_id:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
        elif current_user.role == 'Responsable':
            agent = Agent.query.get(agent_id)
            if not agent or agent.service_id != current_user.service_id:
                return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        # Récupérer tous les arrêts maladie de l'agent
        arrets = ArretMaladie.query.filter_by(agent_id=agent_id).all()
        
        # Calculer les statistiques
        total_jours = sum(arret.nb_jours for arret in arrets)
        total_rtt_perdus = sum(arret.calculer_perte_rtt() for arret in arrets)
        nb_arrets = len(arrets)
        
        # Arrêts de l'année en cours
        annee_courante = datetime.now().year
        arrets_annee = [arret for arret in arrets if arret.date_debut.year == annee_courante]
        total_jours_annee = sum(arret.nb_jours for arret in arrets_annee)
        total_rtt_perdus_annee = sum(arret.calculer_perte_rtt() for arret in arrets_annee)
        
        return jsonify({
            'agent_id': agent_id,
            'total_arrets': nb_arrets,
            'total_jours_tous_arrets': total_jours,
            'total_rtt_perdus_tous_arrets': total_rtt_perdus,
            'total_jours_annee_courante': total_jours_annee,
            'total_rtt_perdus_annee_courante': total_rtt_perdus_annee,
            'arrets_annee_courante': len(arrets_annee)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500




