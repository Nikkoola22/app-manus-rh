from flask import Blueprint, request, jsonify, session
from src.models.agent import Agent, db
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentification requise'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentification requise'}), 401
            
            user = Agent.query.get(session['user_id'])
            if not user or user.role not in roles:
                return jsonify({'error': 'Permissions insuffisantes'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email et mot de passe requis'}), 400
    
    agent = Agent.query.filter_by(email=email).first()
    
    if agent and agent.check_password(password):
        session['user_id'] = agent.id
        session['user_role'] = agent.role
        return jsonify({
            'message': 'Connexion réussie',
            'user': agent.to_dict()
        }), 200
    else:
        return jsonify({'error': 'Email ou mot de passe incorrect'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({'message': 'Déconnexion réussie'}), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    user = Agent.query.get(session['user_id'])
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        user = Agent.query.get(session['user_id'])
        if user:
            return jsonify({
                'authenticated': True,
                'user': user.to_dict()
            }), 200
    
    return jsonify({'authenticated': False}), 200

