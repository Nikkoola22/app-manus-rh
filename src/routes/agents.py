from flask import Blueprint, request, jsonify, session
from src.models.agent import Agent, db
from src.models.service import Service
from src.routes.auth import login_required, role_required
from datetime import datetime
from sqlalchemy.orm import joinedload

agents_bp = Blueprint('agents', __name__)

@agents_bp.route('/agents', methods=['GET'])
@login_required
@role_required(['Admin', 'Responsable'])
def get_agents():
    current_user = Agent.query.get(session['user_id'])
    
    if current_user.role == 'Admin':
        # Admin peut voir tous les agents
        agents = Agent.query.all()
    elif current_user.role == 'Responsable':
        # Responsable ne peut voir que les agents de son service
        agents = Agent.query.filter_by(service_id=current_user.service_id).all()
    else:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    
    return jsonify([agent.to_dict() for agent in agents]), 200

@agents_bp.route('/agents/<int:agent_id>', methods=['GET'])
@login_required
def get_agent(agent_id):
    current_user = Agent.query.get(session['user_id'])
    # Charger l'agent avec la relation service
    agent = Agent.query.options(db.joinedload(Agent.service)).get_or_404(agent_id)
    
    # Vérifier les permissions
    if current_user.role == 'Agent' and current_user.id != agent_id:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    elif current_user.role == 'Responsable' and agent.service_id != current_user.service_id:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    
    return jsonify(agent.to_dict()), 200

@agents_bp.route('/agents', methods=['POST'])
@login_required
@role_required(['Admin'])
def create_agent():
    data = request.get_json()
    
    # Vérifier les champs requis
    required_fields = ['nom', 'prenom', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis'}), 400
    
    # Vérifier si l'email existe déjà
    if Agent.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Un agent avec cet email existe déjà'}), 400
    
    # Créer le nouvel agent
    agent = Agent(
        nom=data['nom'],
        prenom=data['prenom'],
        email=data['email'],
        role=data.get('role', 'Agent'),
        service_id=data.get('service_id'),
        annee_entree_fp=data.get('annee_entree_fp'),
        quotite_travail=data.get('quotite_travail'),
        solde_ca=data.get('solde_ca', 0.0),
        solde_rtt=data.get('solde_rtt', 0.0),
        solde_cet=data.get('solde_cet', 0.0),
        solde_bonifications=data.get('solde_bonifications', 0.0),
        solde_jours_sujetions=data.get('solde_jours_sujetions', 0.0),
        solde_conges_formations=data.get('solde_conges_formations', 0.0),
        solde_hs=data.get('solde_hs', 0.0)
    )
    
    # Traitement des dates
    if data.get('date_debut_contrat'):
        agent.date_debut_contrat = datetime.strptime(data['date_debut_contrat'], '%Y-%m-%d').date()
    if data.get('date_fin_contrat'):
        agent.date_fin_contrat = datetime.strptime(data['date_fin_contrat'], '%Y-%m-%d').date()
    
    agent.set_password(data['password'])
    
    db.session.add(agent)
    db.session.commit()
    
    return jsonify(agent.to_dict()), 201

@agents_bp.route('/agents/<int:agent_id>', methods=['PUT'])
@login_required
@role_required(['Admin'])
def update_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    data = request.get_json()
    
    # Mettre à jour les champs
    if 'nom' in data:
        agent.nom = data['nom']
    if 'prenom' in data:
        agent.prenom = data['prenom']
    if 'email' in data:
        # Vérifier si l'email existe déjà pour un autre agent
        existing_agent = Agent.query.filter_by(email=data['email']).first()
        if existing_agent and existing_agent.id != agent_id:
            return jsonify({'error': 'Un agent avec cet email existe déjà'}), 400
        agent.email = data['email']
    if 'role' in data:
        agent.role = data['role']
    if 'service_id' in data:
        agent.service_id = data['service_id']
    if 'annee_entree_fp' in data:
        agent.annee_entree_fp = data['annee_entree_fp']
    if 'quotite_travail' in data:
        agent.quotite_travail = data['quotite_travail']
    if 'solde_ca' in data:
        agent.solde_ca = data['solde_ca']
    if 'solde_rtt' in data:
        agent.solde_rtt = data['solde_rtt']
    if 'solde_cet' in data:
        agent.solde_cet = data['solde_cet']
    if 'solde_bonifications' in data:
        agent.solde_bonifications = data['solde_bonifications']
    if 'solde_jours_sujetions' in data:
        agent.solde_jours_sujetions = data['solde_jours_sujetions']
    if 'solde_conges_formations' in data:
        agent.solde_conges_formations = data['solde_conges_formations']
    if 'solde_hs' in data:
        agent.solde_hs = data['solde_hs']
    
    # Traitement des dates
    if 'date_debut_contrat' in data:
        agent.date_debut_contrat = datetime.strptime(data['date_debut_contrat'], '%Y-%m-%d').date() if data['date_debut_contrat'] else None
    if 'date_fin_contrat' in data:
        agent.date_fin_contrat = datetime.strptime(data['date_fin_contrat'], '%Y-%m-%d').date() if data['date_fin_contrat'] else None
    
    # Changer le mot de passe si fourni
    if 'password' in data:
        agent.set_password(data['password'])
    
    db.session.commit()
    
    return jsonify(agent.to_dict()), 200

@agents_bp.route('/agents/<int:agent_id>', methods=['DELETE'])
@login_required
@role_required(['Admin'])
def delete_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    
    # Ne pas permettre la suppression de son propre compte
    if agent_id == session['user_id']:
        return jsonify({'error': 'Vous ne pouvez pas supprimer votre propre compte'}), 400
    
    db.session.delete(agent)
    db.session.commit()
    
    return jsonify({'message': 'Agent supprimé avec succès'}), 200

# Routes de démonstration pour les utilisateurs simplifiés
@agents_bp.route('/demo/agents', methods=['GET'])
def get_demo_agents():
    """Route de démonstration pour récupérer les agents"""
    demo_agents = [
        {
            'id': 1,
            'nom': 'Dupont',
            'prenom': 'Jean',
            'email': 'jean.dupont@example.com',
            'role': 'Agent',
            'service_id': 1,
            'quotite_travail': 35,
            'solde_ca': 25,
            'solde_rtt': 18,
            'solde_hs': 0
        },
        {
            'id': 2,
            'nom': 'Martin',
            'prenom': 'Marie',
            'email': 'marie.martin@example.com',
            'role': 'Responsable',
            'service_id': 1,
            'quotite_travail': 35,
            'solde_ca': 30,
            'solde_rtt': 20,
            'solde_hs': 0
        },
        {
            'id': 3,
            'nom': 'Bernard',
            'prenom': 'Pierre',
            'email': 'pierre.bernard@example.com',
            'role': 'Agent',
            'service_id': 2,
            'quotite_travail': 35,
            'solde_ca': 22,
            'solde_rtt': 15,
            'solde_hs': 0
        }
    ]
    return jsonify(demo_agents), 200

@agents_bp.route('/demo/services', methods=['GET'])
def get_demo_services():
    """Route de démonstration pour récupérer les services"""
    demo_services = [
        {
            'id': 1,
            'nom_service': 'Ressources Humaines',
            'responsable_id': 2,
            'nb_agents': 2
        },
        {
            'id': 2,
            'nom_service': 'Informatique',
            'responsable_id': None,
            'nb_agents': 1
        }
    ]
    return jsonify(demo_services), 200

@agents_bp.route('/demo/demandes', methods=['GET'])
def get_demo_demandes():
    """Route de démonstration pour récupérer les demandes"""
    demo_demandes = [
        {
            'id': 1,
            'agent_id': 1,
            'type_absence': 'CA',
            'date_debut': '2024-01-15',
            'date_fin': '2024-01-19',
            'nb_heures': 35,
            'statut': 'En attente',
            'date_demande': '2024-01-10',
            'agent': {
                'prenom': 'Jean',
                'nom': 'Dupont',
                'service_id': 1
            }
        },
        {
            'id': 2,
            'agent_id': 2,
            'type_absence': 'RTT',
            'date_debut': '2024-01-22',
            'date_fin': '2024-01-22',
            'nb_heures': 7,
            'statut': 'Approuvée',
            'date_demande': '2024-01-12',
            'agent': {
                'prenom': 'Marie',
                'nom': 'Martin',
                'service_id': 1
            }
        }
    ]
    return jsonify(demo_demandes), 200

@agents_bp.route('/demo/arrets-maladie', methods=['GET'])
def get_demo_arrets_maladie():
    """Route de démonstration pour récupérer les arrêts maladie"""
    demo_arrets = [
        {
            'id': 1,
            'agent_id': 1,
            'date_debut': '2024-01-10',
            'date_fin': '2024-01-12',
            'motif': 'Grippe',
            'statut': 'En cours',
            'agent': {
                'prenom': 'Jean',
                'nom': 'Dupont'
            }
        }
    ]
    return jsonify(demo_arrets), 200

