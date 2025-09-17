from flask import Blueprint, request, jsonify, session
from src.models.user import db
from src.models.agent import Agent
from src.models.planning import PlanningAgent, PlanningTemplate
from src.routes.auth import login_required, role_required
from datetime import time, datetime
import json

planning_bp = Blueprint('planning', __name__)

@planning_bp.route('/planning/agent/<int:agent_id>', methods=['GET'])
@login_required
def get_planning_agent(agent_id):
    """Récupère le planning d'un agent"""
    try:
        # Vérifier les permissions
        current_user = Agent.query.get(session['user_id'])
        if not current_user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # L'agent peut voir son propre planning, le responsable peut voir ses agents
        if current_user.role == 'Agent' and current_user.id != agent_id:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
        elif current_user.role == 'Responsable':
            target_agent = Agent.query.get(agent_id)
            if not target_agent or target_agent.service_id != current_user.service_id:
                return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        # Récupérer le planning de l'agent
        plannings = PlanningAgent.query.filter_by(agent_id=agent_id, actif=True).all()
        
        # Organiser par jour de la semaine
        planning_par_jour = {}
        for planning in plannings:
            jour = planning.jour_semaine
            if jour not in planning_par_jour:
                planning_par_jour[jour] = []
            planning_par_jour[jour].append(planning.to_dict())
        
        # Générer tous les créneaux de 30 minutes pour chaque jour
        creneaux_complets = {}
        for jour in range(6):  # Lundi à Samedi
            creneaux_complets[jour] = {
                'jour_nom': ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'][jour],
                'plannings': planning_par_jour.get(jour, []),
                'creneaux': []
            }
            
            # Si il y a un planning pour ce jour, générer les créneaux
            if jour in planning_par_jour and planning_par_jour[jour]:
                planning_obj = planning_par_jour[jour][0]  # Prendre le premier planning
                # Récupérer l'objet PlanningAgent depuis la base
                planning_db = PlanningAgent.query.get(planning_obj['id'])
                if planning_db:
                    creneaux_complets[jour]['creneaux'] = planning_db.get_creneaux_30min()
                else:
                    creneaux_complets[jour]['creneaux'] = []
            else:
                # Générer des créneaux vides
                creneaux_complets[jour]['creneaux'] = []
        
        return jsonify({
            'agent_id': agent_id,
            'planning': creneaux_complets
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@planning_bp.route('/planning/agent/<int:agent_id>', methods=['POST'])
@role_required(['Responsable', 'Admin'])
def create_planning_agent(agent_id):
    """Crée ou met à jour le planning d'un agent"""
    try:
        data = request.get_json()
        
        # Vérifier que l'agent existe
        agent = Agent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agent non trouvé'}), 404
        
        # Vérifier les permissions pour les responsables
        current_user = Agent.query.get(session['user_id'])
        if current_user.role == 'Responsable' and agent.service_id != current_user.service_id:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        # Désactiver les anciens plannings
        PlanningAgent.query.filter_by(agent_id=agent_id).update({'actif': False})
        
        # Créer les nouveaux plannings
        plannings_crees = []
        for jour_data in data.get('plannings', []):
            jour = jour_data.get('jour_semaine')
            heure_debut = time.fromisoformat(jour_data.get('heure_debut', '08:00'))
            heure_fin = time.fromisoformat(jour_data.get('heure_fin', '17:00'))
            pause_debut = time.fromisoformat(jour_data.get('pause_debut')) if jour_data.get('pause_debut') else None
            pause_fin = time.fromisoformat(jour_data.get('pause_fin')) if jour_data.get('pause_fin') else None
            
            planning = PlanningAgent(
                agent_id=agent_id,
                jour_semaine=jour,
                heure_debut=heure_debut,
                heure_fin=heure_fin,
                pause_debut=pause_debut,
                pause_fin=pause_fin,
                actif=True
            )
            
            db.session.add(planning)
            plannings_crees.append(planning)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Planning créé avec succès',
            'plannings': [p.to_dict() for p in plannings_crees]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@planning_bp.route('/planning/agent/<int:agent_id>/jour/<int:jour>', methods=['PUT'])
@role_required(['Responsable', 'Admin'])
def update_planning_jour(agent_id, jour):
    """Met à jour le planning d'un jour spécifique"""
    try:
        data = request.get_json()
        
        # Vérifier que l'agent existe
        agent = Agent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agent non trouvé'}), 404
        
        # Vérifier les permissions pour les responsables
        current_user = Agent.query.get(session['user_id'])
        if current_user.role == 'Responsable' and agent.service_id != current_user.service_id:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        # Désactiver l'ancien planning pour ce jour
        PlanningAgent.query.filter_by(agent_id=agent_id, jour_semaine=jour).update({'actif': False})
        
        # Créer le nouveau planning
        heure_debut = time.fromisoformat(data.get('heure_debut', '08:00'))
        heure_fin = time.fromisoformat(data.get('heure_fin', '17:00'))
        pause_debut = time.fromisoformat(data.get('pause_debut')) if data.get('pause_debut') else None
        pause_fin = time.fromisoformat(data.get('pause_fin')) if data.get('pause_fin') else None
        
        planning = PlanningAgent(
            agent_id=agent_id,
            jour_semaine=jour,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            pause_debut=pause_debut,
            pause_fin=pause_fin,
            actif=True
        )
        
        db.session.add(planning)
        db.session.commit()
        
        return jsonify({
            'message': 'Planning mis à jour avec succès',
            'planning': planning.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@planning_bp.route('/planning/service/<int:service_id>', methods=['GET'])
@role_required(['Responsable', 'Admin'])
def get_plannings_service(service_id):
    """Récupère tous les plannings d'un service"""
    try:
        # Vérifier les permissions
        current_user = Agent.query.get(session['user_id'])
        if current_user.role == 'Responsable' and current_user.service_id != service_id:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        # Récupérer tous les agents du service
        agents = Agent.query.filter_by(service_id=service_id, role='Agent').all()
        
        plannings_service = {}
        for agent in agents:
            plannings = PlanningAgent.query.filter_by(agent_id=agent.id, actif=True).all()
            plannings_service[agent.id] = {
                'agent': agent.to_dict(),
                'plannings': [p.to_dict() for p in plannings]
            }
        
        return jsonify({
            'service_id': service_id,
            'plannings': plannings_service
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@planning_bp.route('/planning/templates', methods=['GET'])
@role_required(['Responsable', 'Admin'])
def get_planning_templates():
    """Récupère les modèles de planning"""
    try:
        current_user = Agent.query.get(session['user_id'])
        
        # Filtrer par service si c'est un responsable
        if current_user.role == 'Responsable':
            templates = PlanningTemplate.query.filter_by(service_id=current_user.service_id, actif=True).all()
        else:
            templates = PlanningTemplate.query.filter_by(actif=True).all()
        
        return jsonify({
            'templates': [t.to_dict() for t in templates]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@planning_bp.route('/planning/templates', methods=['POST'])
@role_required(['Responsable', 'Admin'])
def create_planning_template():
    """Crée un nouveau modèle de planning"""
    try:
        data = request.get_json()
        current_user = Agent.query.get(session['user_id'])
        
        template = PlanningTemplate(
            nom=data.get('nom'),
            description=data.get('description'),
            service_id=current_user.service_id if current_user.role == 'Responsable' else data.get('service_id'),
            plannings=data.get('plannings', []),
            actif=True
        )
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify({
            'message': 'Modèle de planning créé avec succès',
            'template': template.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
