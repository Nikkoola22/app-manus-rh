from flask import Blueprint, request, jsonify, session
from src.models.service import Service, db
from src.models.agent import Agent
from src.routes.auth import login_required, role_required

services_bp = Blueprint('services', __name__)

@services_bp.route('/services', methods=['GET'])
@login_required
def get_services():
    services = Service.query.all()
    return jsonify([service.to_dict() for service in services]), 200

@services_bp.route('/services/<int:service_id>', methods=['GET'])
@login_required
def get_service(service_id):
    service = Service.query.get_or_404(service_id)
    return jsonify(service.to_dict()), 200

@services_bp.route('/services', methods=['POST'])
@login_required
@role_required(['Admin'])
def create_service():
    data = request.get_json()
    
    # Vérifier les champs requis
    if 'nom_service' not in data:
        return jsonify({'error': 'Le nom du service est requis'}), 400
    
    # Vérifier si le service existe déjà
    if Service.query.filter_by(nom_service=data['nom_service']).first():
        return jsonify({'error': 'Un service avec ce nom existe déjà'}), 400
    
    # Vérifier que le responsable existe et a le bon rôle
    responsable_id = data.get('responsable_id')
    if responsable_id:
        responsable = Agent.query.get(responsable_id)
        if not responsable:
            return jsonify({'error': 'Responsable non trouvé'}), 400
        if responsable.role not in ['Responsable', 'Admin']:
            return jsonify({'error': 'Le responsable doit avoir le rôle Responsable ou Admin'}), 400
    
    # Créer le nouveau service
    service = Service(
        nom_service=data['nom_service'],
        responsable_id=responsable_id
    )
    
    db.session.add(service)
    db.session.commit()
    
    return jsonify(service.to_dict()), 201

@services_bp.route('/services/<int:service_id>', methods=['PUT'])
@login_required
@role_required(['Admin'])
def update_service(service_id):
    service = Service.query.get_or_404(service_id)
    data = request.get_json()
    
    # Mettre à jour le nom du service
    if 'nom_service' in data:
        # Vérifier si le nom existe déjà pour un autre service
        existing_service = Service.query.filter_by(nom_service=data['nom_service']).first()
        if existing_service and existing_service.id != service_id:
            return jsonify({'error': 'Un service avec ce nom existe déjà'}), 400
        service.nom_service = data['nom_service']
    
    # Mettre à jour le responsable
    if 'responsable_id' in data:
        responsable_id = data['responsable_id']
        if responsable_id:
            responsable = Agent.query.get(responsable_id)
            if not responsable:
                return jsonify({'error': 'Responsable non trouvé'}), 400
            if responsable.role not in ['Responsable', 'Admin']:
                return jsonify({'error': 'Le responsable doit avoir le rôle Responsable ou Admin'}), 400
        service.responsable_id = responsable_id
    
    db.session.commit()
    
    return jsonify(service.to_dict()), 200

@services_bp.route('/services/<int:service_id>', methods=['DELETE'])
@login_required
@role_required(['Admin'])
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    # Vérifier s'il y a des agents dans ce service
    agents_count = Agent.query.filter_by(service_id=service_id).count()
    if agents_count > 0:
        return jsonify({'error': f'Impossible de supprimer le service. Il contient {agents_count} agent(s)'}), 400
    
    db.session.delete(service)
    db.session.commit()
    
    return jsonify({'message': 'Service supprimé avec succès'}), 200

@services_bp.route('/services/<int:service_id>/agents', methods=['GET'])
@login_required
def get_service_agents(service_id):
    current_user = Agent.query.get(session['user_id'])
    
    # Vérifier les permissions
    if current_user.role == 'Agent':
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    elif current_user.role == 'Responsable' and current_user.service_id != service_id:
        return jsonify({'error': 'Permissions insuffisantes'}), 403
    
    service = Service.query.get_or_404(service_id)
    agents = Agent.query.filter_by(service_id=service_id).all()
    
    return jsonify([agent.to_dict() for agent in agents]), 200

