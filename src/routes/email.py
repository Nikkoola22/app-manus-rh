from flask import Blueprint, request, jsonify, session
from src.routes.auth import login_required, role_required
from src.services.email_service import send_test_email
import os

email_bp = Blueprint('email', __name__)

@email_bp.route('/email/test', methods=['POST'])
@login_required
@role_required(['Admin'])
def test_email():
    """Teste la configuration email en envoyant un email de test"""
    try:
        data = request.get_json()
        recipient_email = data.get('email')
        
        if not recipient_email:
            return jsonify({'error': 'Adresse email requise'}), 400
        
        # Envoyer l'email de test
        success = send_test_email(recipient_email)
        
        if success:
            return jsonify({'message': 'Email de test envoyé avec succès'}), 200
        else:
            return jsonify({'error': 'Erreur lors de l\'envoi de l\'email de test'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@email_bp.route('/email/config', methods=['GET'])
@login_required
@role_required(['Admin'])
def get_email_config():
    """Récupère la configuration email actuelle (sans les mots de passe)"""
    try:
        config = {
            'mail_server': os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
            'mail_port': int(os.getenv('MAIL_PORT', 587)),
            'mail_use_tls': os.getenv('MAIL_USE_TLS', 'True').lower() == 'true',
            'mail_use_ssl': os.getenv('MAIL_USE_SSL', 'False').lower() == 'true',
            'mail_username': os.getenv('MAIL_USERNAME', ''),
            'mail_default_sender': os.getenv('MAIL_DEFAULT_SENDER', 'noreply@entreprise.com'),
            'configured': bool(os.getenv('MAIL_USERNAME') and os.getenv('MAIL_PASSWORD'))
        }
        
        return jsonify(config), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@email_bp.route('/email/config', methods=['POST'])
@login_required
@role_required(['Admin'])
def update_email_config():
    """Met à jour la configuration email"""
    try:
        data = request.get_json()
        
        # Mettre à jour les variables d'environnement
        if 'mail_server' in data:
            os.environ['MAIL_SERVER'] = data['mail_server']
        if 'mail_port' in data:
            os.environ['MAIL_PORT'] = str(data['mail_port'])
        if 'mail_use_tls' in data:
            os.environ['MAIL_USE_TLS'] = str(data['mail_use_tls']).lower()
        if 'mail_use_ssl' in data:
            os.environ['MAIL_USE_SSL'] = str(data['mail_use_ssl']).lower()
        if 'mail_username' in data:
            os.environ['MAIL_USERNAME'] = data['mail_username']
        if 'mail_password' in data:
            os.environ['MAIL_PASSWORD'] = data['mail_password']
        if 'mail_default_sender' in data:
            os.environ['MAIL_DEFAULT_SENDER'] = data['mail_default_sender']
        
        return jsonify({'message': 'Configuration email mise à jour avec succès'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

